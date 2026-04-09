#!/usr/bin/env python3
"""One-shot script: add new gap-filling categories to the graph."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES = ROOT / "graph" / "nodes.json"
EDGES = ROOT / "graph" / "edges.json"

def slug(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")

def cat_id(path):
    return "cat:" + "/".join(slug(p) for p in path)

# Each entry: (parent_path_tuple, [child_labels]) OR nested dict
# We use a flat list of full paths to create. Missing ancestors must already exist.
NEW_PATHS = [
    # --- Agents/Experiments (new subtree) ---
    ["Agents", "Experiments"],
    ["Agents", "Experiments", "Emergent Communication"],
    ["Agents", "Experiments", "Self-Replication Studies"],
    ["Agents", "Experiments", "Deception & Sandbagging Studies"],
    ["Agents", "Experiments", "Power-Seeking Probes"],
    ["Agents", "Experiments", "Self-Rewriting Agents"],

    # --- Agents/Multiagent additions ---
    ["Agents", "Multiagent", "Debate & Deliberation"],
    ["Agents", "Multiagent", "Market & Auction Mechanisms"],

    # --- Agents/Simulations & Worlds additions ---
    ["Agents", "Simulations & Worlds", "Economic Simulation"],
    ["Agents", "Simulations & Worlds", "Epidemiological & Policy Simulation"],

    # --- Agents/Autonomous additions ---
    ["Agents", "Autonomous", "Open-Ended Exploration"],

    # --- Agents/Domain Specific expansions ---
    ["Agents", "Domain Specific", "Legal"],
    ["Agents", "Domain Specific", "Medical & Clinical"],
    ["Agents", "Domain Specific", "Finance"],
    ["Agents", "Domain Specific", "Scientific Research"],
    ["Agents", "Domain Specific", "Mathematics & Theorem Proving"],
    ["Agents", "Domain Specific", "Education & Tutoring"],
    ["Agents", "Domain Specific", "Customer Support"],
    ["Agents", "Domain Specific", "Sales & SDR"],
    ["Agents", "Domain Specific", "Recruiting & Sourcing"],
    ["Agents", "Domain Specific", "GIS & Geospatial"],
    ["Agents", "Domain Specific", "Robotics & Embodied Tasks"],
    ["Agents", "Domain Specific", "Gaming & NPC"],
    ["Agents", "Domain Specific", "Creative Writing"],
    ["Agents", "Domain Specific", "Music Composition"],
    ["Agents", "Domain Specific", "Translation & Localization"],

    # --- Agents/Security (new top-level under Agents) ---
    ["Agents", "Security"],
    ["Agents", "Security", "SOC & Incident Response"],
    ["Agents", "Security", "Threat Intelligence & OSINT"],
    ["Agents", "Security", "Vulnerability Research & Bug Bounty"],
    ["Agents", "Security", "Malware Analysis & Reverse Engineering"],
    ["Agents", "Security", "Digital Forensics & DFIR"],
    ["Agents", "Security", "Fuzzing & Exploit Generation"],
    ["Agents", "Security", "Code Security Review"],
    ["Agents", "Security", "Phishing Analysis & Takedown"],
    ["Agents", "Security", "Compliance & Audit"],
    ["Agents", "Security", "Cloud Security Posture"],
    ["Agents", "Security", "Network Defense"],
    ["Agents", "Security", "Deception & Honeypots"],

    # --- Agents/Operations (new top-level under Agents) ---
    ["Agents", "Operations"],
    ["Agents", "Operations", "SRE & Sysadmin"],
    ["Agents", "Operations", "SRE & Sysadmin", "Incident Response & On-Call"],
    ["Agents", "Operations", "SRE & Sysadmin", "Log Analysis & Triage"],
    ["Agents", "Operations", "SRE & Sysadmin", "Root Cause Analysis"],
    ["Agents", "Operations", "SRE & Sysadmin", "Runbook Execution"],
    ["Agents", "Operations", "SRE & Sysadmin", "Config Management"],
    ["Agents", "Operations", "SRE & Sysadmin", "Patch & Upgrade"],
    ["Agents", "Operations", "SRE & Sysadmin", "Capacity Planning & Rightsizing"],
    ["Agents", "Operations", "SRE & Sysadmin", "Database Administration"],
    ["Agents", "Operations", "SRE & Sysadmin", "Observability Exploration"],
    ["Agents", "Operations", "SRE & Sysadmin", "Shell & Terminal Agents"],
    ["Agents", "Operations", "Containers & Orchestration"],
    ["Agents", "Operations", "Containers & Orchestration", "Docker"],
    ["Agents", "Operations", "Containers & Orchestration", "Kubernetes"],
    ["Agents", "Operations", "Containers & Orchestration", "Helm Charts"],
    ["Agents", "Operations", "Containers & Orchestration", "Cluster Diagnostics"],
    ["Agents", "Operations", "Containers & Orchestration", "Pod & Workload Remediation"],
    ["Agents", "Operations", "Containers & Orchestration", "Service Mesh"],
    ["Agents", "Operations", "Containers & Orchestration", "GitOps"],
    ["Agents", "Operations", "Infrastructure as Code"],
    ["Agents", "Operations", "Infrastructure as Code", "Terraform & OpenTofu"],
    ["Agents", "Operations", "Infrastructure as Code", "Pulumi"],
    ["Agents", "Operations", "Infrastructure as Code", "CloudFormation & CDK"],
    ["Agents", "Operations", "Cloud"],
    ["Agents", "Operations", "Cloud", "Cost Optimization"],
    ["Agents", "Operations", "Cloud", "Migration"],
    ["Agents", "Operations", "Cloud", "Multi-Cloud Orchestration"],
    ["Agents", "Operations", "Networking"],
    ["Agents", "Operations", "Networking", "Troubleshooting"],
    ["Agents", "Operations", "Networking", "Firewall & Policy Generation"],
    ["Agents", "Operations", "Networking", "Network Config"],

    # --- Agents/Memory additions ---
    ["Agents", "Memory", "Forgetting & Decay Policies"],
    ["Agents", "Memory", "Memory Consolidation"],

    # --- Agents/Purpose Specific misc additions ---
    ["Agents", "Purpose Specific", "Data Labeling"],
    ["Agents", "Purpose Specific", "Academic Literature Review"],

    # --- Agents/Collective Intelligence (new) ---
    ["Agents", "Collective Intelligence"],

    # --- Agents/Creative Collaboration (new) ---
    ["Agents", "Creative Collaboration"],

    # --- Context, Memory & Data/Data additions ---
    ["Context, Memory & Data", "Data", "Synthetic Trajectory Generation"],

    # --- Observability & Evals/Benchmarks additions ---
    ["Observability & Evals", "Benchmarks", "Tool-Use Benchmarks"],
    ["Observability & Evals", "Benchmarks", "Long-Horizon Task Benchmarks"],
    ["Observability & Evals", "Benchmarks", "Multi-Agent Benchmarks"],
    ["Observability & Evals", "Benchmarks", "Safety & Red-Team Benchmarks"],

    # --- Safety & Governance/Security/Red Team additions ---
    ["Safety & Governance", "Security", "Red Team", "Jailbreak Corpora"],
    ["Safety & Governance", "Security", "Red Team", "Agent Hijacking Testbeds"],

    # --- Tools & Integrations/Actions additions ---
    ["Tools & Integrations", "Actions", "Physical World Actuation"],
    ["Tools & Integrations", "Actions", "Email as a Tool"],
    ["Tools & Integrations", "Actions", "Calendar as a Tool"],
    ["Tools & Integrations", "Actions", "Filesystem Tools"],

    # --- Frameworks & Runtimes/Runtimes additions ---
    ["Frameworks & Runtimes", "Runtimes", "GPU & Resource Schedulers"],
    ["Frameworks & Runtimes", "Runtimes", "Agent Migration & Hot-Swap"],

    # --- Interfaces/Control Surfaces additions ---
    ["Interfaces", "Control Surfaces", "Replay & Forking UIs"],

    # --- Models & Inference/Models/Reinforcement Learning additions ---
    ["Models & Inference", "Models", "Reinforcement Learning", "Self-Play Environments"],
    ["Models & Inference", "Models", "Reinforcement Learning", "Curriculum Generation"],

    # --- Ecosystem additions ---
    ["Ecosystem", "Organisations", "Research Labs"],
    ["Ecosystem", "Publications & Newsletters"],

    # --- Dev Tools & Skills/Prompts additions ---
    ["Dev Tools & Skills", "Prompts", "Prompt Versioning & Diffing"],
]

def main():
    nodes_doc = json.loads(NODES.read_text())
    edges_doc = json.loads(EDGES.read_text())
    existing_ids = {n["id"] for n in nodes_doc["nodes"]}
    existing_edges = {(e["from"], e["to"], e["type"]) for e in edges_doc["edges"]}

    added_n = 0
    added_e = 0
    for path in NEW_PATHS:
        cid = cat_id(path)
        if cid not in existing_ids:
            nodes_doc["nodes"].append({
                "id": cid,
                "type": "Category",
                "label": path[-1],
                "path": list(path),
                "description": "",
            })
            existing_ids.add(cid)
            added_n += 1
        # parent edge
        if len(path) > 1:
            parent_id = cat_id(path[:-1])
            if parent_id not in existing_ids:
                raise SystemExit(f"Missing parent {parent_id} for {cid}")
            edge = (cid, parent_id, "SUBCATEGORY_OF")
            if edge not in existing_edges:
                edges_doc["edges"].append({"from": cid, "to": parent_id, "type": "SUBCATEGORY_OF"})
                existing_edges.add(edge)
                added_e += 1

    nodes_doc["updated"] = "2026-04-10"
    edges_doc["updated"] = "2026-04-10"
    NODES.write_text(json.dumps(nodes_doc, indent=2) + "\n")
    EDGES.write_text(json.dumps(edges_doc, indent=2) + "\n")
    print(f"Added {added_n} nodes, {added_e} edges.")

if __name__ == "__main__":
    main()
