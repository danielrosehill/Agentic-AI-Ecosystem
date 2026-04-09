#!/usr/bin/env python3
"""One-shot taxonomy restructure.

Applies the approved reorg:
  - Dissolve `Tools` segment (redistribute children to better homes)
  - Add new top-level segments for gap fills
  - Consolidate duplicates (Multiagent/Personal/Workspace/Desktop GUIs)
  - Promote Harnesses → Guardrails to top-level

Idempotent: rerunning after success is a no-op (operations check current
state before acting).

Run with --dry-run to print the plan without writing.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES_IN = ROOT / "graph" / "nodes.json"
EDGES_IN = ROOT / "graph" / "edges.json"


def slug(s: str) -> str:
    s = s.lower().strip()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "unnamed"


def cat_id_from_path(path: list[str]) -> str:
    return "cat:" + "/".join(slug(p) for p in path)


class Graph:
    def __init__(self, nodes, edges):
        self.nodes = {n["id"]: n for n in nodes}
        self.edges = list(edges)
        self.log: list[str] = []

    # ---- helpers ----
    def parent_of(self, cat_id):
        for e in self.edges:
            if e["type"] == "SUBCATEGORY_OF" and e["from"] == cat_id:
                return e["to"]
        return None

    def children_of(self, cat_id):
        return [e["from"] for e in self.edges if e["type"] == "SUBCATEGORY_OF" and e["to"] == cat_id]

    def projects_of(self, cat_id):
        return [e["from"] for e in self.edges if e["type"] == "CATEGORY_OF" and e["to"] == cat_id]

    def rename_node_id(self, old_id, new_id):
        """Change a node's id across nodes + edges (no data loss)."""
        if old_id == new_id:
            return
        if old_id not in self.nodes:
            return
        if new_id in self.nodes:
            raise ValueError(f"cannot rename {old_id} → {new_id}: target exists")
        n = self.nodes.pop(old_id)
        n["id"] = new_id
        self.nodes[new_id] = n
        for e in self.edges:
            if e["from"] == old_id:
                e["from"] = new_id
            if e["to"] == old_id:
                e["to"] = new_id

    def update_paths(self, cat_id):
        """Recursively recompute path + id for a category and all descendants."""
        parent = self.parent_of(cat_id)
        n = self.nodes[cat_id]
        if parent:
            new_path = list(self.nodes[parent]["path"]) + [n["label"]]
        else:
            new_path = [n["label"]]
        n["path"] = new_path
        new_id = cat_id_from_path(new_path)
        children = self.children_of(cat_id)
        self.rename_node_id(cat_id, new_id)
        for c in children:
            self.update_paths(c)

    # ---- high-level ops ----
    def add_category(self, parent_id, label, short_description=""):
        if parent_id and parent_id not in self.nodes:
            raise ValueError(f"parent missing: {parent_id}")
        parent_path = self.nodes[parent_id]["path"] if parent_id else []
        new_path = parent_path + [label]
        new_id = cat_id_from_path(new_path)
        if new_id in self.nodes:
            self.log.append(f"  · add_category exists: {new_id}")
            return new_id
        self.nodes[new_id] = {
            "id": new_id,
            "type": "Category",
            "label": label,
            "path": new_path,
            "short_description": short_description,
            "long_description": "",
            "examples_narrative": "",
        }
        if parent_id:
            self.edges.append({"from": new_id, "to": parent_id, "type": "SUBCATEGORY_OF"})
        self.log.append(f"  + add_category {new_id} — {short_description[:50]}")
        return new_id

    def move_category(self, cat_id, new_parent_id):
        """Re-parent a category subtree (updates paths and ids recursively)."""
        if cat_id not in self.nodes:
            self.log.append(f"  · move_category skip (missing): {cat_id}")
            return None
        if new_parent_id and new_parent_id not in self.nodes:
            raise ValueError(f"new parent missing: {new_parent_id}")
        # rewire SUBCATEGORY_OF
        for e in self.edges:
            if e["type"] == "SUBCATEGORY_OF" and e["from"] == cat_id:
                e["to"] = new_parent_id
                break
        else:
            if new_parent_id:
                self.edges.append({"from": cat_id, "to": new_parent_id, "type": "SUBCATEGORY_OF"})
        self.update_paths(cat_id)
        # cat_id has changed — find the new id
        new_id = cat_id_from_path(self.nodes_by_label_under(new_parent_id, cat_id))
        self.log.append(f"  → move_category to {new_parent_id}")
        return None

    def nodes_by_label_under(self, parent_id, _old):
        # helper used after rename — not needed; keep for clarity
        return []

    def merge_categories(self, src_id, dst_id):
        """Merge src into dst: move children and projects, then delete src."""
        if src_id not in self.nodes:
            self.log.append(f"  · merge skip (missing src): {src_id}")
            return
        if dst_id not in self.nodes:
            raise ValueError(f"merge dst missing: {dst_id}")
        if src_id == dst_id:
            return
        # Move children: each child's SUBCATEGORY_OF edge now points at dst, recompute paths.
        for child_id in list(self.children_of(src_id)):
            for e in self.edges:
                if e["type"] == "SUBCATEGORY_OF" and e["from"] == child_id and e["to"] == src_id:
                    e["to"] = dst_id
            self.update_paths(child_id)
        # Move projects: CATEGORY_OF edges pointing at src → dst.
        for e in self.edges:
            if e["type"] == "CATEGORY_OF" and e["to"] == src_id:
                e["to"] = dst_id
        # Delete src (and its own SUBCATEGORY_OF edge).
        self.edges = [
            e for e in self.edges
            if not (e["from"] == src_id and e["type"] == "SUBCATEGORY_OF")
        ]
        self.nodes.pop(src_id, None)
        self.log.append(f"  ⇄ merge {src_id} → {dst_id}")

    def delete_category(self, cat_id):
        """Delete an empty category (no children, no projects)."""
        if cat_id not in self.nodes:
            self.log.append(f"  · delete skip (missing): {cat_id}")
            return
        if self.children_of(cat_id):
            raise ValueError(f"cannot delete {cat_id}: has children")
        if self.projects_of(cat_id):
            raise ValueError(f"cannot delete {cat_id}: has projects")
        self.edges = [e for e in self.edges if e["from"] != cat_id and e["to"] != cat_id]
        self.nodes.pop(cat_id)
        self.log.append(f"  - delete_category {cat_id}")

    def promote_to_top_level(self, cat_id, new_label=None):
        """Re-parent a category to top-level (no parent)."""
        if cat_id not in self.nodes:
            self.log.append(f"  · promote skip (missing): {cat_id}")
            return None
        if new_label:
            self.nodes[cat_id]["label"] = new_label
        # Remove existing SUBCATEGORY_OF edge.
        self.edges = [
            e for e in self.edges
            if not (e["type"] == "SUBCATEGORY_OF" and e["from"] == cat_id)
        ]
        self.update_paths(cat_id)
        self.log.append(f"  ⇈ promote {cat_id} to top-level")

    def move_project(self, proj_id, new_cat_id):
        if proj_id not in self.nodes:
            self.log.append(f"  · move_project skip (missing): {proj_id}")
            return
        for e in self.edges:
            if e["type"] == "CATEGORY_OF" and e["from"] == proj_id:
                e["to"] = new_cat_id
                break
        self.log.append(f"  → move_project {proj_id} → {new_cat_id}")


def apply_plan(g: Graph) -> None:
    # ==================================================================
    # TOOLS DISSOLUTION
    # ==================================================================
    g.log.append("\n=== TOOLS DISSOLUTION ===")

    # Move `Tools → Android` under `On Device Agents` as a new subcat.
    tools_android_children = g.projects_of("cat:tools/android")
    new_android = g.add_category("cat:on-device-agents", "Android",
        "Android-specific agent runtimes and device-level automation.")
    for p in tools_android_children:
        g.move_project(p, new_android)
    g.delete_category("cat:tools/android")

    # `Tools → Browser Utils → SDK` merges into `Browser Tooling`.
    # First move the SDK subcategory's projects up to Browser Tooling directly,
    # since Browser Tooling already has an examples slot.
    for p in g.projects_of("cat:tools/browser-utils/sdk"):
        g.move_project(p, "cat:browser-tooling")
    g.delete_category("cat:tools/browser-utils/sdk")
    for p in g.projects_of("cat:tools/browser-utils"):
        g.move_project(p, "cat:browser-tooling")
    g.delete_category("cat:tools/browser-utils")

    # `Tools → Computer Use` merges into top-level `Computer Use`.
    # Move its CLI subcategory over as a subcat of top-level Computer Use.
    computer_use_cli_new = g.add_category("cat:computer-use", "CLI",
        "CLI-based computer-use agents and tools.")
    for p in g.projects_of("cat:tools/computer-use/cli"):
        g.move_project(p, computer_use_cli_new)
    g.delete_category("cat:tools/computer-use/cli")
    # Move Tools → Computer Use direct projects to Computer Use.
    for p in g.projects_of("cat:tools/computer-use"):
        g.move_project(p, "cat:computer-use")
    g.delete_category("cat:tools/computer-use")

    # `Tools → Data Ingestion` → `RAG → Ingestion` (new subcat).
    rag_ingestion = g.add_category("cat:rag", "Ingestion",
        "Pipelines that ingest and process documents into retrieval systems.")
    for p in g.projects_of("cat:tools/data-ingestion"):
        g.move_project(p, rag_ingestion)
    g.delete_category("cat:tools/data-ingestion")

    # `Tools → Debugging` → `Dev Tools → Debugging` (new subcat).
    devtools_debugging = g.add_category("cat:dev-tools", "Debugging",
        "Debugging and introspection tools for agent development.")
    for p in g.projects_of("cat:tools/debugging"):
        g.move_project(p, devtools_debugging)
    g.delete_category("cat:tools/debugging")

    # `Tools → Financial` merges into top-level `Financial Tools`.
    for p in g.projects_of("cat:tools/financial"):
        g.move_project(p, "cat:financial-tools")
    g.delete_category("cat:tools/financial")

    # `Tools → IDE Tools` → `Dev Tools → IDE Integrations`.
    devtools_ide = g.add_category("cat:dev-tools", "IDE Integrations",
        "IDE extensions and plugins for agent-assisted development.")
    for p in g.projects_of("cat:tools/ide-tools"):
        g.move_project(p, devtools_ide)
    g.delete_category("cat:tools/ide-tools")

    # `Tools → Integration Platforms → SaaS` promotes to new top-level `Integrations`.
    integrations_root = g.add_category(None, "Integrations",
        "Agent-to-SaaS connector platforms: Composio-style libraries exposing third-party APIs as agent tools.")
    for p in g.projects_of("cat:tools/integration-platforms/saas"):
        g.move_project(p, integrations_root)
    g.delete_category("cat:tools/integration-platforms/saas")
    for p in g.projects_of("cat:tools/integration-platforms"):
        g.move_project(p, integrations_root)
    g.delete_category("cat:tools/integration-platforms")

    # `Tools → macOS` merges into `Computer Use → Platform Specific → macOS`.
    for p in g.projects_of("cat:tools/macos"):
        g.move_project(p, "cat:computer-use/platform-specific/macos")
    g.delete_category("cat:tools/macos")

    # `Tools → Model Routing` merges into `Routers → Intelligent`.
    for p in g.projects_of("cat:tools/model-routing"):
        g.move_project(p, "cat:routers/intelligent")
    g.delete_category("cat:tools/model-routing")

    # `Tools → Semantic Search` promotes to top-level.
    g.promote_to_top_level("cat:tools/semantic-search")

    # `Tools → Vision UI` → `Computer Use → Vision UI` (new subcat).
    cu_vision = g.add_category("cat:computer-use", "Vision UI",
        "Vision-based UI understanding models for computer-use agents.")
    for p in g.projects_of("cat:tools/vision-ui"):
        g.move_project(p, cu_vision)
    g.delete_category("cat:tools/vision-ui")

    # `Tools → World Creation → MCP` merges into `World Generation`.
    wg_mcp = g.add_category("cat:world-generation", "MCP",
        "MCP servers for world and scene generation.")
    for p in g.projects_of("cat:tools/world-creation/mcp"):
        g.move_project(p, wg_mcp)
    g.delete_category("cat:tools/world-creation/mcp")
    for p in g.projects_of("cat:tools/world-creation"):
        g.move_project(p, "cat:world-generation")
    g.delete_category("cat:tools/world-creation")

    # Projects directly under Tools (vercel-ai-sdk, langflow) → Frameworks.
    for p in g.projects_of("cat:tools"):
        g.move_project(p, "cat:frameworks")

    # Finally, delete Tools itself.
    g.delete_category("cat:tools")

    # ==================================================================
    # GAP FILLS — new top-level segments
    # ==================================================================
    g.log.append("\n=== GAP FILLS ===")

    g.add_category(None, "Prompt Management",
        "Versioning, registries, and lifecycle management for prompts as first-class artifacts.")
    g.add_category(None, "Structured Output",
        "Libraries that constrain LLM outputs to typed schemas, JSON, or formal grammars.")
    g.add_category(None, "Semantic Caching",
        "Cache layers that serve semantically equivalent LLM responses to cut cost and latency.")
    g.add_category(None, "Inference Servers",
        "LLM inference servers and runtimes (vLLM, TGI, llama.cpp, SGLang) that agents call into.")
    g.add_category(None, "Synthetic Data",
        "Tools for generating synthetic training and evaluation data for agents.")
    g.add_category(None, "Annotation",
        "Human labeling, RLHF, and feedback-collection platforms for agent training data.")
    g.add_category(None, "Identity and Auth",
        "Agent identity, credential vaulting, and delegated authentication for tool access.")
    g.add_category(None, "PII and Redaction",
        "PII detection, content sanitization, and safety filtering for agent I/O.")
    g.add_category(None, "Agent Analytics",
        "Product analytics for agent behaviour: funnels, retention, conversation quality, task success.")

    # Promote Harnesses → Guardrails to a top-level `Guardrails` segment.
    g.promote_to_top_level("cat:harnesses/guardrails")

    # ==================================================================
    # CONSOLIDATIONS
    # ==================================================================
    g.log.append("\n=== CONSOLIDATIONS ===")

    # Frameworks → Multi-agent + Frameworks → Multiagent Orchestration are near-duplicates.
    # Merge Multi-agent into Multiagent Orchestration (keep the more specific name).
    g.merge_categories("cat:frameworks/multi-agent", "cat:frameworks/multiagent-orchestration")

    # Personal (top-level, nanobot) + Personal AI (top-level) + Agents → Personal Focused (Crucix)
    # → fold everything into top-level Personal AI.
    g.merge_categories("cat:personal", "cat:personal-ai")
    g.merge_categories("cat:agents/personal-focused", "cat:personal-ai")

    # Multiagent → Workspace (typo) + Multiagent → Workspaces + top-level Workspaces
    # → fold into top-level Workspaces.
    g.merge_categories("cat:multiagent/workspace", "cat:workspaces")
    g.merge_categories("cat:multiagent/workspaces", "cat:workspaces")

    # Desktop GUIs (top-level, hello-halo) folds into `Agents → Desktop GUIs` (new).
    agents_desktop = g.add_category("cat:agents", "Desktop GUIs",
        "Desktop graphical interfaces for interacting with agents.")
    for p in g.projects_of("cat:desktop-guis"):
        g.move_project(p, agents_desktop)
    g.delete_category("cat:desktop-guis")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    nodes_data = json.loads(NODES_IN.read_text())
    edges_data = json.loads(EDGES_IN.read_text())

    g = Graph(nodes_data["nodes"], edges_data["edges"])
    apply_plan(g)

    for line in g.log:
        print(line)

    cats = sum(1 for n in g.nodes.values() if n["type"] == "Category")
    projs = sum(1 for n in g.nodes.values() if n["type"] == "Project")
    print(f"\nafter: {len(g.nodes)} nodes ({cats} categories, {projs} projects), {len(g.edges)} edges")

    if args.dry_run:
        print("\n(dry run — no files written)")
        return

    nodes_data["nodes"] = list(g.nodes.values())
    edges_data["edges"] = g.edges
    NODES_IN.write_text(json.dumps(nodes_data, indent=2) + "\n")
    EDGES_IN.write_text(json.dumps(edges_data, indent=2) + "\n")
    print(f"\nwrote {NODES_IN.relative_to(ROOT)} + {EDGES_IN.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
