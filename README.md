# Agentic AI Ecosystem Map

A hand-curated **taxonomy** of the agentic AI ecosystem — categories, sub-areas, and representative projects as evidence that each functional slot exists. This is a classification map, not a project directory.

- **Full taxonomy tree**: [SCHEMA.md](./SCHEMA.md) *(generated)*
- **Source of truth**: [`graph/nodes.json`](./graph/nodes.json) + [`graph/edges.json`](./graph/edges.json)
- **Derived tree view**: [`ecosystem.json`](./ecosystem.json)
- **Interactive 3D viz**: [danielrosehill.github.io/Agentic-AI-Ecosystem/viz/](https://danielrosehill.github.io/Agentic-AI-Ecosystem/viz/)
- **Sister project — runtime architecture model**: [Agentic-AI-Architecture-Visualisation](https://github.com/danielrosehill/Agentic-AI-Architecture-Visualisation)

## At a glance

**24** top-level clusters · **223** sub-areas · **196** example projects.

## Clusters

Each row is a top-level functional cluster. Sub-areas and examples are truncated — see [SCHEMA.md](./SCHEMA.md) for the complete tree.

| Cluster | What it covers | Sub-areas | Example projects |
| --- | --- | --- | --- |
| **Actions** | — | `AI Browsers` · `Browser Automation` · `Browser Tooling` · `Computer Use` · `Data Extraction and Structuring` · `Financial Tools` · +5 | [BrowserOS](https://github.com/browseros-ai/BrowserOS), [Lightpanda Browser](https://github.com/lightpanda-io/browser), [Steel Browser](https://github.com/steel-dev/steel-browser), [Vibium](https://github.com/VibiumDev/vibium), +15 |
| **Agent to Agent** | Communication protocols and transports that let agents talk directly to other agents. | `Experiments` | [AgentChattr](https://github.com/bcurts/agentchattr), [ConnectOnion](https://github.com/openonion/connectonion), [OpenAgents](https://github.com/openagents-org/openagents), [Gibberlink](https://github.com/PennyroyalTea/gibberlink) |
| **Agent Tools** | Tools and services that agents invoke as capabilities, rather than frameworks for building agents themselves. | `Comms` | [MCP Agent Mail](https://github.com/Dicklesworthstone/mcp_agent_mail) |
| **Agents** | General agent projects and agent subtypes that do not fit more specific segments. | `Agent Clusters` · `Agent Collaboration` · `Autonomous` · `Autonomous Agent Creation` · `Backend Platforms` · `CLIs/Toolkits` · +17 | [Xata Agent](https://github.com/xataio/agent), [IntentKit](https://github.com/crestalnetwork/intentkit), [AgentVerse](https://github.com/Peiiii/AgentVerse), [AI-Trader](https://github.com/HKUDS/AI-Trader), +24 |
| **Builders & Platforms** | — | `Automation` · `Deployment Platforms` · `Development Platforms` · `Engineering Platforms` · `On Device Agents` · `Optimisation Platform` · +2 | [Activepieces](https://github.com/activepieces/activepieces), [Flowise](https://github.com/FlowiseAI/Flowise), [Julep](https://github.com/julep-ai/julep), [Coze Studio](https://github.com/coze-dev/coze-studio), +8 |
| **Context Store** | — | `Context` · `Context Optimisation` · `Embedding Pipeline Orchestrators` · `Memory` · `Personal AI` · `RAG` · +3 | [PromptX](https://github.com/Deepractice/PromptX), [WeKnora](https://github.com/Tencent/WeKnora), [context-mode](https://github.com/mksglu/context-mode), [Contexto](https://github.com/ekailabs/contexto), +19 |
| **Destinations** | — | — | — |
| **Dev Tools & Skills** | — | `Dev Tools` · `Skills` | [vLLora](https://github.com/vllora/vllora), [Roo-Code](https://github.com/RooCodeInc/Roo-Code), [AgentRC](https://github.com/microsoft/agentrc), [Agent Skills](https://github.com/addyosmani/agent-skills), +5 |
| **Frameworks & Runtimes** | — | `Environments` · `Frameworks` · `Harnesses` · `Loops` · `Orchestration` · `Runtimes` · +1 | [agent-os](https://github.com/rivet-dev/agent-os), [Abacus Desktop](https://desktop.abacus.ai/), [cua.ai](https://cua.ai/), [AgentForge](https://github.com/DataBassGit/AgentForge), +33 |
| **Frontends** | User-facing interfaces — web, desktop, mobile, terminal — for interacting with agents. | `Android` · `Chat UIs` · `Desktop Clients` · `GUIs and CLIs` · `Mobile Clients` · `Server Software` · +3 | [Operit](https://github.com/AAswordman/Operit), [Agent UI](https://github.com/agno-agi/agent-ui), [Goose](https://github.com/aaif-goose/goose), [Agent Deck](https://github.com/asheshgoplani/agent-deck) |
| **Grounding** | — | `Data Sources` · `Grounding Tools` · `Search Utilities` | [OpenBB](https://github.com/OpenBB-finance/OpenBB) |
| **Inference** | — | `Gateways` · `Inference Servers` · `Proxy` · `Routers` · `Semantic Caching` | [Context-Gateway](https://github.com/Compresr-ai/Context-Gateway), [AgentGateway](https://github.com/agentgateway/agentgateway), [LiteLLM](https://github.com/BerriAI/litellm), [MCPO](https://github.com/open-webui/mcpo), +4 |
| **Interfaces & Workspaces** | — | `Annotation` · `UX` · `Workspaces` | [Agent Inbox](https://github.com/langchain-ai/agent-inbox), [Orchestra](https://github.com/b12io/orchestra), [AgentsMesh](https://github.com/AgentsMesh/AgentsMesh), [Gastown](https://github.com/gastownhall/gastown), +1 |
| **MCP** | Projects in the Model Context Protocol ecosystem — servers, gateways, aggregators, clients. | `Aggregation` · `Gateways` · `Third Party` | [Klavis](https://github.com/Klavis-AI/klavis), [MCP Context Forge](https://github.com/IBM/mcp-context-forge), [MCP Server Airbnb](https://github.com/openbnb-org/mcp-server-airbnb) |
| **Models** | — | `Embedding Models` · `LLMs` · `Reinforcement Learning` · `Synthetic Data` · `Trainers` | Gemini 3.1, [Grok 4.20 Multi-Agent](https://openrouter.ai/x-ai/grok-4.20-multi-agent), [Fara](https://github.com/microsoft/fara), [Acme](https://github.com/google-deepmind/acme), +2 |
| **Observability** | Logging, tracing and observability specifically for agent and LLM systems. | `Agent Analytics` · `Benchmarks` · `Evals and Experiment Tracking` · `Operations` | [RagaAI Catalyst](https://github.com/raga-ai-hub/RagaAI-Catalyst), [AICGSecEval](https://github.com/Tencent/AICGSecEval), [OSWorld](https://github.com/xlang-ai/OSWorld), [LangWatch](https://github.com/langwatch/langwatch), +4 |
| **Organisations** | — | `Companies` · `Foundations` · `Foundations & Consortia` · `Government Bodies` | [Agentic AI Industry Foundation (AAIF)](https://aaif.io/) |
| **Pipelines** | Reusable pipelines for common agentic workloads. | — | [Paper2Agent](https://github.com/jmiao24/Paper2Agent) |
| **Prompts** | — | `Conversational Control` · `Feedback Formatting` · `Formatting` · `Prompt Management` · `Structured Output` · `Workflow Definition` | [Parlant](https://github.com/emcie-co/parlant), [Agentation](https://github.com/benjitaylor/agentation), [TOON](https://github.com/toon-format/toon), [Packmind](https://github.com/PackmindHub/packmind) |
| **Safety** | — | `Agent in the Loop` · `Guardrails` · `Human in the Loop` · `Identity and Auth` · `PII and Redaction` · `Security` | [Shellfirm](https://github.com/kaplanelad/shellfirm), [agent-scan](https://github.com/snyk/agent-scan), [AgentGuard](https://github.com/GoPlusSecurity/agentguard), [Tracecat](https://github.com/TracecatHQ/tracecat), +3 |
| **Simulations & Worlds** | — | `Character & Roleplay` · `Geopolitical Simulation` · `Societal Simulations` · `World Generation` | [Snowglobe](https://github.com/IQTLabs/snowglobe), [WargamesAI](https://github.com/user1342/WargamesAI), [OASIS](https://github.com/camel-ai/oasis), [ML-Agents](https://github.com/Unity-Technologies/ml-agents), +1 |
| **Standards** | Proposed and emerging standards across the agentic ecosystem. | `Emerging (Ecosystem-Tied)` · `Proposed` · `Ratified` | [WebMCP](https://webmcp.dev/), [WebMCP (Chrome EPP)](https://developer.chrome.com/blog/webmcp-epp), [AIUC-1](https://www.aiuc-1.com/), [GitAgent](https://github.com/open-gitagent/gitagent), +3 |
| **Storage** | — | `Backend Querying` · `Databases` | [MindsDB](https://github.com/mindsdb/mindsdb), [OpenViking](https://github.com/volcengine/OpenViking) |
| **Uncategorized** | Holding area for projects awaiting classification. Entries here are a todo list, not a destination. | — | [Agency Agents](https://github.com/msitarzewski/agency-agents) |

---

*README generated from `ecosystem.json` by `scripts/generate_readme.py`. Full tree generated into `SCHEMA.md` by `scripts/generate_schema.py`.*
