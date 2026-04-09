# Agentic AI Ecosystem Map

A hand-curated **taxonomy** of the agentic AI ecosystem — categories, sub-areas, and representative projects as evidence that each functional slot exists. This is a classification map, not a project directory.

- **Full taxonomy tree**: [SCHEMA.md](./SCHEMA.md) *(generated)*
- **Source of truth**: [`graph/nodes.json`](./graph/nodes.json) + [`graph/edges.json`](./graph/edges.json)
- **Derived tree view**: [`ecosystem.json`](./ecosystem.json)
- **Interactive 3D viz**: [danielrosehill.github.io/Agentic-AI-Ecosystem/viz/](https://danielrosehill.github.io/Agentic-AI-Ecosystem/viz/)
- **Sister project — runtime architecture model**: [Agentic-AI-Architecture-Visualisation](https://github.com/danielrosehill/Agentic-AI-Architecture-Visualisation)

## At a glance

**11** top-level clusters · **435** sub-areas · **307** example projects.

## Clusters

Each row is a top-level functional cluster. Sub-areas and examples are truncated — see [SCHEMA.md](./SCHEMA.md) for the complete tree.

| Cluster | What it covers | Sub-areas | Example projects |
| --- | --- | --- | --- |
| **Agents** | Agent runtimes, frameworks, harnesses, and surfaces that define, host, or coordinate individual and multi-agent systems. | `Agent Clusters` · `Agent Collaboration` · `Agent to Agent` · `Autonomous` · `Autonomous Agent Creation` · `Backend Platforms` · +25 | [Xata Agent](https://github.com/xataio/agent), [IntentKit](https://github.com/crestalnetwork/intentkit), [AgentVerse](https://github.com/Peiiii/AgentVerse), [AgentChattr](https://github.com/bcurts/agentchattr), +37 |
| **Builders & Platforms** | Platforms and products for building, deploying, and operating agents — the IDE and PaaS layer of the ecosystem. | `Automation` · `Deployment Platforms` · `Development Platforms` · `Engineering Platforms` · `On Device Agents` · `Optimisation Platform` · +2 | [Activepieces](https://github.com/activepieces/activepieces), [Flowise](https://github.com/FlowiseAI/Flowise), [Julep](https://github.com/julep-ai/julep), [Coze Studio](https://github.com/coze-dev/coze-studio), +8 |
| **Context, Memory & Data** | Everything that feeds agents with context, persistent memory, and structured data. | `Context` · `Data` · `Memory` | [PromptX](https://github.com/Deepractice/PromptX), [WeKnora](https://github.com/Tencent/WeKnora), [context-mode](https://github.com/mksglu/context-mode), [Contexto](https://github.com/ekailabs/contexto), +40 |
| **Dev Tools & Skills** | Tooling, reusable skills, and prompt assets that developers use to build and operate agents. | `Dev Tools` · `Prompts` · `Skills` | [Aider](https://github.com/Aider-AI/aider), [OpenDevin/OpenHands](https://github.com/All-Hands-AI/OpenHands), [SWE-agent](https://github.com/princeton-nlp/SWE-agent), [vLLora](https://github.com/vllora/vllora), +19 |
| **Ecosystem** | Meta-layer covering non-tool entities in the agentic AI landscape: organisations, destinations, and uncategorised items. | `Destinations` · `Organisations` · `Publications & Newsletters` · `Uncategorized` | [Agentic AI Industry Foundation (AAIF)](https://aaif.io/), [Agency Agents](https://github.com/msitarzewski/agency-agents) |
| **Frameworks & Runtimes** | Top-level domain for the software substrate that executes agents: frameworks, runtimes, harnesses, loops, and orchestration. | `Environments` · `Frameworks` · `Harnesses` · `Loops` · `Orchestration` · `Pipelines` · +2 | [agent-os](https://github.com/rivet-dev/agent-os), [Abacus Desktop](https://desktop.abacus.ai/), [cua.ai](https://cua.ai/), [AgentForge](https://github.com/DataBassGit/AgentForge), +48 |
| **Interfaces** | User-facing surfaces through which humans interact with agents — frontends, workspaces, UX patterns, and annotation tools. | `Annotation` · `Control Surfaces` · `Frontends` · `UX` · `Workspaces` | [Operit](https://github.com/AAswordman/Operit), [Agent UI](https://github.com/agno-agi/agent-ui), [Goose](https://github.com/aaif-goose/goose), [Agent Deck](https://github.com/asheshgoplani/agent-deck), +5 |
| **Models & Inference** | The model layer: base models themselves and the infrastructure that serves them to agents. | `Inference` · `Models` | [Context-Gateway](https://github.com/Compresr-ai/Context-Gateway), [LMDeploy](https://github.com/InternLM/lmdeploy), [SGLang](https://github.com/sgl-project/sglang), [Text Generation Inference](https://github.com/huggingface/text-generation-inference), +27 |
| **Observability & Evals** | Telemetry, evaluation, and operational monitoring for LLM and agent systems across their lifecycle. | `Agent Analytics` · `Benchmarks` · `Evals and Experiment Tracking` · `Operations` · `Research & Experimentation` | [RagaAI Catalyst](https://github.com/raga-ai-hub/RagaAI-Catalyst), [AICGSecEval](https://github.com/Tencent/AICGSecEval), [OSWorld](https://github.com/xlang-ai/OSWorld), [AgentBench](https://github.com/THUDM/AgentBench), +22 |
| **Safety & Governance** | Controls, policies, and oversight mechanisms that keep agents safe, compliant, and accountable in production. | `Agent in the Loop` · `Guardrails` · `Hallucination & Factuality` · `Human in the Loop` · `Identity and Auth` · `PII and Redaction` · +3 | [Shellfirm](https://github.com/kaplanelad/shellfirm), [Guardrails AI](https://github.com/guardrails-ai/guardrails), [Invariant Labs](https://github.com/invariantlabs-ai/invariant), [Llama Guard](https://github.com/meta-llama/PurpleLlama), +14 |
| **Tools & Integrations** | Tools, actions, and integration layers that connect agents to the outside world — MCP, standards, and action surfaces. | `Actions` · `MCP` · `Standards` | [BrowserOS](https://github.com/browseros-ai/BrowserOS), [Lightpanda Browser](https://github.com/lightpanda-io/browser), [Steel Browser](https://github.com/steel-dev/steel-browser), [Arcade.dev](https://www.arcade.dev/), +45 |

---

*README generated from `ecosystem.json` by `scripts/generate_readme.py`. Full tree generated into `SCHEMA.md` by `scripts/generate_schema.py`.*
