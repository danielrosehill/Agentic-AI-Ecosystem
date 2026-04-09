#!/usr/bin/env python3
"""Normalize project display labels in graph/nodes.json.

Rules (applied in order):
  1. Manual OVERRIDES dict wins absolutely.
  2. Strip "org/" prefix from "org/repo" labels → "repo" (then re-apply rules).
  3. If the label already contains an uppercase letter → leave alone
     (treat as intentional CamelCase / brand casing).
  4. All-lowercase single word → capitalize first letter.
  5. lowercase with hyphens/underscores → title-case each part joined with '-'.

Preserve the node id (it's the stable key). Only the `label` changes.
Run with --dry-run to print proposed renames without writing.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES_IN = ROOT / "graph" / "nodes.json"

# Manual overrides — proper brand casings that rules can't infer.
OVERRIDES = {
    "autogen":            "AutoGen",
    "camel":               "CAMEL",
    "trulens":            "TruLens",
    "deepeval":           "DeepEval",
    "langfuse":           "Langfuse",
    "langwatch":          "LangWatch",
    "langflow":           "Langflow",
    "letta":              "Letta",
    "mem0":               "Mem0",
    "cognee":             "Cognee",
    "agentmemory":        "AgentMemory",
    "graphiti":           "Graphiti",
    "dify":               "Dify",
    "goose":              "Goose",
    "parlant":            "Parlant",
    "firecrawl":          "Firecrawl",
    "activepieces":       "Activepieces",
    "mindsdb":            "MindsDB",
    "intentkit":          "IntentKit",
    "voltagent":          "VoltAgent",
    "livekit/agents":     "LiveKit Agents",
    "videosdk-live/agents": "VideoSDK Agents",
    "ten-framework":      "TEN Framework",
    "vercel/ai":          "Vercel AI SDK",
    "deepagents":         "DeepAgents",
    "tracecat":           "Tracecat",
    "microsoft/fara":     "Fara",
    "xataio/agent":       "Xata Agent",
    "openagents":         "OpenAgents",
    "agentchattr":        "AgentChattr",
    "connectonion":       "ConnectOnion",
    "crush":              "Crush",
    "gemini-cli":         "Gemini CLI",
    "qwen-code":          "Qwen Code",
    "openhands":          "OpenHands",
    "OpenHands":          "OpenHands",  # keep
    "biomni":             "Biomni",
    "Biomni":             "Biomni",
    "bolna":              "Bolna",
    "nanobot":            "Nanobot",
    "agentgateway":       "AgentGateway",
    "mcpo":               "MCPO",
    "ragflow":            "RAGFlow",
    "airweave":           "Airweave",
    "oasis":              "OASIS",
    "ml-agents":          "ML-Agents",
    "agentkit":           "AgentKit",
    "composio":           "Composio",
    "stagehand":          "Stagehand",
    "cua":                "cua",  # lowercase brand
    "n8n":                "n8n",  # intentional lowercase brand
    "acme":               "Acme",
    "graphiti":           "Graphiti",
    "hermes-agent":       "Hermes Agent",
    "uagents":            "uAgents",
    "uAgents":            "uAgents",
    "ii-agent":           "II-Agent",
    "agentforge":         "AgentForge",
    "AgentForge":         "AgentForge",
    "evoagentx":          "EvoAgentX",
    "EvoAgentX":          "EvoAgentX",
    "aiopslab":           "AIOpsLab",
    "AIOpsLab":           "AIOpsLab",
    "botsharp":           "BotSharp",
    "BotSharp":           "BotSharp",
    "agent-s":            "Agent-S",
    "Agent-S":            "Agent-S",
    "crewai":             "CrewAI",
    "crewAI":             "CrewAI",
    "ensoai":             "EnsoAI",
    "EnsoAI":             "EnsoAI",
    "concordia":          "Concordia",
    "moltbook":           "Moltbook",
    "pentagi":            "Pentagi",
    "inkos":              "INKOS",
    "crucix":             "Crucix",
    "Crucix":             "Crucix",
    "openclaw":           "OpenClaw",
    "leon":               "Leon",
    "lobehub":            "LobeHub",
    "wargamesai":         "WargamesAI",
    "WargamesAI":         "WargamesAI",
    "snowglobe":          "Snowglobe",
    "hive":               "Hive",
    "oh-my-openagent":    "oh-my-openagent",
    "plurals":            "Plurals",
    "Plurals":            "Plurals",
    "llm-council":        "LLM Council",
    "superdesign":        "Superdesign",
    "agency-agents":      "Agency Agents",
    "klavis":             "Klavis",
    "mcp-context-forge":  "MCP Context Forge",
    "mcp-server-airbnb":  "MCP Server Airbnb",
    "mcp_agent_mail":     "MCP Agent Mail",
    "openbb":             "OpenBB",
    "OpenBB":             "OpenBB",
    "julep":              "Julep",
    "hello-halo":         "Hello Halo",
    "agentrc":            "AgentRC",
    "coze-studio":        "Coze Studio",
    "coze-loop":          "Coze Loop",
    "openshell":          "OpenShell",
    "OpenShell":          "OpenShell",
    "opensandbox":        "OpenSandbox",
    "OpenSandbox":        "OpenSandbox",
    "deeplake":           "Deep Lake",
    "raga-ai-catalyst":   "RagaAI Catalyst",
    "RagaAI-Catalyst":    "RagaAI Catalyst",
    "be-more-agent":      "be-more-agent",
    "agentops":           "AgentOps",
    "shannon":            "Shannon",
    "Shannon":            "Shannon",
    "conductor":          "Conductor",
    "ai-maestro":         "AI Maestro",
    "agent-orchestrator": "Agent Orchestrator",
    "agent-squad":        "Agent Squad",
    "bub":                "Bub",
    "paper2agent":        "Paper2Agent",
    "Paper2Agent":        "Paper2Agent",
    "fairo":              "Fairo",
    "agentgateway":       "AgentGateway",
    "relayplane proxy":   "RelayPlane Proxy",
    "RelayPlane proxy":   "RelayPlane Proxy",
    "semantic-router":    "Semantic Router",
    "clawrouter":         "ClawRouter",
    "ClawRouter":         "ClawRouter",
    "microsandbox":       "Microsandbox",
    "rogue":              "Rogue",
    "marketingskills":    "Marketing Skills",
    "taste-skill":        "Taste Skill",
    "vercel-labs/skills": "Vercel Skills",
    "agent-skills (tech-leads-club)": "Agent Skills (tech-leads-club)",
    "agentskills":        "AgentSkills",
    "agent-skills":       "Agent Skills",
    "jupyter-ai":         "Jupyter AI",
    "webmcp":             "WebMCP",
    "WebMCP":             "WebMCP",
    "WebMCP (Chrome EPP)": "WebMCP (Chrome EPP)",
    "gitagent":           "GitAgent",
    "aiuc-1":             "AIUC-1",
    "AIUC-1":             "AIUC-1",
    "a2a (agent2agent protocol)": "A2A (Agent2Agent Protocol)",
    "A2A (Agent2Agent Protocol)": "A2A (Agent2Agent Protocol)",
    "ag-ui (agent user interaction protocol)": "AG-UI (Agent User Interaction Protocol)",
    "AG-UI (Agent User Interaction Protocol)": "AG-UI (Agent User Interaction Protocol)",
    "mcp (model context protocol)": "MCP (Model Context Protocol)",
    "MCP (Model Context Protocol)": "MCP (Model Context Protocol)",
    "ai-town":            "AI Town",
    "ai-data-science-team": "AI Data Science Team",
    "agentsmesh":         "AgentsMesh",
    "AgentsMesh":         "AgentsMesh",
    "gastown":            "Gastown",
    "miroFish":           "MiroFish",
    "MiroFish":           "MiroFish",
    "agenttorch":         "AgentTorch",
    "AgentTorch":         "AgentTorch",
    "osaurus":            "Osaurus",
    "browseros":          "BrowserOS",
    "BrowserOS":          "BrowserOS",
    "osworld":            "OSWorld",
    "OSWorld":            "OSWorld",
    "memos":              "MemOS",
    "MemOS":              "MemOS",
    "osgrep":             "osgrep",
    "gumloop":            "Gumloop",
    "Gumloop":            "Gumloop",
    "mindstudio":         "MindStudio",
    "MindStudio":         "MindStudio",
    "agent.ai":           "agent.ai",
    "abacus desktop":     "Abacus Desktop",
    "Abacus Desktop":     "Abacus Desktop",
    "cua.ai":             "cua.ai",
    "agen.cy marketplace": "agen.cy Marketplace",
    "ai agent store":     "AI Agent Store",
    "AI Agent Store":     "AI Agent Store",
    "packmind":           "Packmind",
    "toon":               "TOON",
    "agent-inbox":        "Agent Inbox",
    "orchestra":          "Orchestra",
    "aegis":              "Aegis",
    "Aegis":              "Aegis",
    "cordum":             "Cordum",
    "litellm":            "LiteLLM",
    "shellfirm":          "Shellfirm",
    "lightpanda browser": "Lightpanda Browser",
    "Lightpanda Browser": "Lightpanda Browser",
    "steel browser":      "Steel Browser",
    "Steel Browser":      "Steel Browser",
    "flowise":            "Flowise",
    "Flowise":            "Flowise",
    "macOS-use":          "macOS-use",
    "context-mode":       "context-mode",
    "contexto":           "Contexto",
    "dotai":              "dotai",
    "react-grab":         "react-grab",
    "context-lens":       "context-lens",
    "promptx":            "PromptX",
    "PromptX":            "PromptX",
    "weknora":            "WeKnora",
    "WeKnora":            "WeKnora",
    "openviking":         "OpenViking",
    "OpenViking":         "OpenViking",
    "agent-browser":      "Agent Browser",
    "agentation":         "Agentation",
    "goat":               "GOAT",
    "agentic-flow":       "Agentic Flow",
    "ui-venus":           "UI-Venus",
    "UI-Venus":           "UI-Venus",
    "unreal-engine-mcp":  "Unreal Engine MCP",
    "vibium":             "Vibium",
    "agent-lightning":    "Agent Lightning",
    "agent-deck":         "Agent Deck",
    "agent-ui":           "Agent UI",
    "operit":             "Operit",
    "Operit":             "Operit",
    "agent-device":       "Agent Device",
    "usecomputer":        "usecomputer",
    "cmux":               "cmux",
    "roo-code":           "Roo-Code",
    "Roo-Code":           "Roo-Code",
    "agent-reach":        "Agent-Reach",
    "Agent-Reach":        "Agent-Reach",
    "vllora":             "vLLora",
    "vision-agents":      "Vision Agents",
    "Vision-Agents":      "Vision Agents",
    "agent-os":           "agent-os",
    "agent-scan":         "agent-scan",
    "agentguard":         "AgentGuard",
    "bankrbot/skills":    "BankrBot Skills",
    "BankrBot/skills":    "BankrBot Skills",
    "ai-trader":          "AI-Trader",
    "AI-Trader":          "AI-Trader",
    "open-computer-use":  "open-computer-use",
    "squad":              "Squad",
    "ralph":              "Ralph",
    "aicgseceval":        "AICGSecEval",
    "AICGSecEval":        "AICGSecEval",
    "acontext":           "Acontext",
    "Acontext":           "Acontext",
    "agentic-context-engine": "Agentic Context Engine",
    "memvid":             "Memvid",
    "gibberlink":         "Gibberlink",
    "agentverse":         "AgentVerse",
    "AgentVerse":         "AgentVerse",
    "openclaw-mission-control": "OpenClaw Mission Control",
    "Agentic AI Industry Foundation (AAIF)": "Agentic AI Industry Foundation (AAIF)",
    "Gemini 3.1":         "Gemini 3.1",
    "Grok 4.20 Multi-Agent": "Grok 4.20 Multi-Agent",
    "fara":               "Fara",
    "qdrant":             "Qdrant",
    "Qdrant":             "Qdrant",
    "Context-Gateway":    "Context-Gateway",
}


def normalize(label: str) -> str:
    # 1. manual override (exact match, case-sensitive first)
    if label in OVERRIDES:
        return OVERRIDES[label]
    if label.lower() in OVERRIDES:
        return OVERRIDES[label.lower()]

    # 2. org/repo → repo, then recurse
    if "/" in label and label.count("/") == 1:
        org, repo = label.split("/")
        # Keep org/repo format only if explicitly overridden above; else use repo
        return normalize(repo)

    # 3. already has uppercase → leave alone
    if any(c.isupper() for c in label):
        return label

    # 4. all lowercase single word → Capitalize
    if re.fullmatch(r"[a-z0-9]+", label):
        return label[0].upper() + label[1:]

    # 5. lowercase with separators → title-case parts
    if re.fullmatch(r"[a-z0-9][a-z0-9\-_\. ]*", label):
        parts = re.split(r"([-_\. ])", label)
        return "".join(p if p in "-_. " else (p[:1].upper() + p[1:]) for p in parts)

    return label


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write changes back to nodes.json")
    args = ap.parse_args()

    data = json.loads(NODES_IN.read_text())
    changes: list[tuple[str, str, str]] = []  # (id, old, new)
    for n in data["nodes"]:
        if n["type"] != "Project":
            continue
        old = n["label"]
        new = normalize(old)
        if new != old:
            changes.append((n["id"], old, new))
            if args.apply:
                n["label"] = new

    print(f"{len(changes)} project labels would change:")
    for _id, old, new in changes:
        print(f"  {old!r:40} → {new!r}")

    if args.apply:
        NODES_IN.write_text(json.dumps(data, indent=2) + "\n")
        print(f"\napplied changes to {NODES_IN.relative_to(ROOT)}")
    else:
        print("\n(dry run — rerun with --apply to write)")


if __name__ == "__main__":
    main()
