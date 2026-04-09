# Agentic AI Ecosystem Map

## Purpose

This project maps the **categories, subcategories, and connections** between emerging tooling in the agentic AI space. It is a taxonomy, not a project directory.

The primary mechanism is **real project → taxonomy**: example projects are collected as evidence that a functional slot exists, and the taxonomy is refined backwards from those examples. A category with one example (or even zero) is valid if it represents a distinct functional slot in an agentic stack.

Every category has a stable ID (`cat:<slug-path>`) so the taxonomy can be referenced as a foreign key, a Neo4j constraint, or a uniqueness guarantee in downstream tools.

**Source of truth**: [`graph/nodes.json`](./graph/nodes.json) + [`graph/edges.json`](./graph/edges.json). [`ecosystem.json`](./ecosystem.json) is a regenerated tree view for human reading.

**Interactive 3D viz**: [danielrosehill.github.io/Agentic-AI-Ecosystem/viz/](https://danielrosehill.github.io/Agentic-AI-Ecosystem/viz/)

## Segments

- [Agent Analytics](#agent-analytics)
- [Agent Clusters](#agent-clusters)
- [Agent Collaboration](#agent-collaboration)
- [Agent to Agent](#agent-to-agent)
- [Agent Tools](#agent-tools)
- [Agents](#agents)
- [AI Browsers](#ai-browsers)
- [Annotation](#annotation)
- [Automation](#automation)
- [Backend Querying](#backend-querying)
- [Benchmarks](#benchmarks)
- [Browser Automation](#browser-automation)
- [Browser Tooling](#browser-tooling)
- [Computer Use](#computer-use)
- [Context](#context)
- [Conversational Control](#conversational-control)
- [Data Extraction and Structuring](#data-extraction-and-structuring)
- [Data Sources](#data-sources)
- [Databases](#databases)
- [Deployment Platforms](#deployment-platforms)
- [Dev Tools](#dev-tools)
- [Development Platforms](#development-platforms)
- [Embedding Models](#embedding-models)
- [Embedding Pipeline Orchestrators](#embedding-pipeline-orchestrators)
- [Engineering Platforms](#engineering-platforms)
- [Environments](#environments)
- [Evals and Experiment Tracking](#evals-and-experiment-tracking)
- [Feedback Formatting](#feedback-formatting)
- [Financial Tools](#financial-tools)
- [Formatting](#formatting)
- [Foundations](#foundations)
- [Frameworks](#frameworks)
- [Frontends](#frontends)
- [Gateways](#gateways)
- [Geopolitical Simulation](#geopolitical-simulation)
- [Guardrails](#guardrails)
- [Harnesses](#harnesses)
- [Identity and Auth](#identity-and-auth)
- [Inference Servers](#inference-servers)
- [Integrations](#integrations)
- [LLMs](#llms)
- [Loops](#loops)
- [Marketplaces](#marketplaces)
- [MCP](#mcp)
- [Memory](#memory)
- [Multiagent](#multiagent)
- [Networks](#networks)
- [Observability](#observability)
- [On Device Agents](#on-device-agents)
- [Operations](#operations)
- [Optimisation Platform](#optimisation-platform)
- [Orchestration](#orchestration)
- [Personal AI](#personal-ai)
- [Personification](#personification)
- [PII and Redaction](#pii-and-redaction)
- [Pipelines](#pipelines)
- [Platforms](#platforms)
- [Prompt Management](#prompt-management)
- [Proxy](#proxy)
- [RAG](#rag)
- [Reinforcement Learning](#reinforcement-learning)
- [Routers](#routers)
- [Runtimes](#runtimes)
- [SaaS Builders](#saas-builders)
- [Security](#security)
- [Semantic Caching](#semantic-caching)
- [Semantic Search](#semantic-search)
- [Skills](#skills)
- [Societal Simulations](#societal-simulations)
- [Software Extensions](#software-extensions)
- [Standards](#standards)
- [Starter Kits](#starter-kits)
- [Structured Output](#structured-output)
- [Synthesised Perspectives](#synthesised-perspectives)
- [Synthetic Data](#synthetic-data)
- [Task Specific](#task-specific)
- [Trainers](#trainers)
- [Uncategorized](#uncategorized)
- [Upserting Tools](#upserting-tools)
- [UX](#ux)
- [Vector Databases](#vector-databases)
- [Voice](#voice)
- [Workflow Definition](#workflow-definition)
- [Workspaces](#workspaces)
- [World Generation](#world-generation)

---

## Agent Analytics
<sub>`cat:agent-analytics`</sub>

*Product analytics for agent behaviour: funnels, retention, conversation quality, task success.*

## Agent Clusters
<sub>`cat:agent-clusters`</sub>

*Systems that run many agents together as a managed group or fleet.*

- [IntentKit](https://github.com/crestalnetwork/intentkit)

## Agent Collaboration
<sub>`cat:agent-collaboration`</sub>

*Protocols, patterns and platforms for agents to collaborate on shared tasks.*

- [AgentVerse](https://github.com/Peiiii/AgentVerse)

## Agent to Agent
<sub>`cat:agent-to-agent`</sub>

*Communication protocols and transports that let agents talk directly to other agents.*

- [AgentChattr](https://github.com/bcurts/agentchattr)
- [ConnectOnion](https://github.com/openonion/connectonion)
- [OpenAgents](https://github.com/openagents-org/openagents)

### Experiments
<sub>`cat:agent-to-agent/experiments`</sub>

#### Voices
<sub>`cat:agent-to-agent/experiments/voices`</sub>

- [Gibberlink](https://github.com/PennyroyalTea/gibberlink)

## Agent Tools
<sub>`cat:agent-tools`</sub>

### Comms
<sub>`cat:agent-tools/comms`</sub>

- [MCP Agent Mail](https://github.com/Dicklesworthstone/mcp_agent_mail)

## Agents
<sub>`cat:agents`</sub>

*General agent projects and agent subtypes that do not fit more specific segments.*

- [Xata Agent](https://github.com/xataio/agent)

### Autonomous
<sub>`cat:agents/autonomous`</sub>

#### Trading
<sub>`cat:agents/autonomous/trading`</sub>

- [AI-Trader](https://github.com/HKUDS/AI-Trader)

### Autonomous Agent Creation
<sub>`cat:agents/autonomous-agent-creation`</sub>

- [BankrBot Skills](https://github.com/BankrBot/skills)

### Backend Platforms
<sub>`cat:agents/backend-platforms`</sub>

- [Dify](https://github.com/langgenius/dify)

### CLIs/Toolkits
<sub>`cat:agents/clis-toolkits`</sub>

#### Vendor
<sub>`cat:agents/clis-toolkits/vendor`</sub>

- [Qwen Code](https://github.com/QwenLM/qwen-code)

### Computer Use
<sub>`cat:agents/computer-use`</sub>

*Agents and frameworks that operate a computer the way a human would (mouse, keyboard, screen).*

- [open-computer-use](https://github.com/coasty-ai/open-computer-use)

### Desktop GUIs
<sub>`cat:agents/desktop-guis`</sub>

*Desktop graphical interfaces for interacting with agents.*

- [Hello Halo](https://github.com/openkursar/hello-halo)

### Development
<sub>`cat:agents/development`</sub>

- [OpenHands](https://github.com/OpenHands/OpenHands)

### Domain Specific
<sub>`cat:agents/domain-specific`</sub>

#### Biotech
<sub>`cat:agents/domain-specific/biotech`</sub>

- [Biomni](https://github.com/snap-stanford/Biomni)

### Frameworks
<sub>`cat:agents/frameworks`</sub>

*General-purpose frameworks for building agents and agentic applications.*

#### Open Source
<sub>`cat:agents/frameworks/open-source`</sub>

- [Hermes Agent](https://github.com/NousResearch/hermes-agent)

### Frontends
<sub>`cat:agents/frontends`</sub>

*User-facing interfaces — web, desktop, mobile, terminal — for interacting with agents.*

- [OpenClaw Mission Control](https://github.com/abhi1693/openclaw-mission-control)

### Harnesses
<sub>`cat:agents/harnesses`</sub>

*Test harnesses and runner frameworks that host and exercise agents.*

#### CLIs
<sub>`cat:agents/harnesses/clis`</sub>

##### Third Party
<sub>`cat:agents/harnesses/clis/third-party`</sub>

- [Crush](https://github.com/charmbracelet/crush)

##### Vendor
<sub>`cat:agents/harnesses/clis/vendor`</sub>

- [Gemini CLI](https://github.com/google-gemini/gemini-cli)

### Memory
<sub>`cat:agents/memory`</sub>

*Memory systems for agents — short-term, long-term, episodic, file-backed, graph-backed.*

#### Graph Builders
<sub>`cat:agents/memory/graph-builders`</sub>

- [Graphiti](https://github.com/getzep/graphiti)

### Purpose Specific
<sub>`cat:agents/purpose-specific`</sub>

- [INKOS](https://github.com/Narcooo/inkos)

#### Penetration Testing
<sub>`cat:agents/purpose-specific/penetration-testing`</sub>

- [Pentagi](https://github.com/vxcontrol/pentagi)

### Team Formation
<sub>`cat:agents/team-formation`</sub>

- [Squad](https://github.com/bradygaster/squad)

### Teams
<sub>`cat:agents/teams`</sub>

- [AI Data Science Team](https://github.com/business-science/ai-data-science-team)

### Vision
<sub>`cat:agents/vision`</sub>

- [Vision Agents](https://github.com/GetStream/Vision-Agents)

## AI Browsers
<sub>`cat:ai-browsers`</sub>

*Browsers built or adapted specifically for AI agent use, including headless variants optimised for programmatic navigation.*

- [BrowserOS](https://github.com/browseros-ai/BrowserOS)

### Headless
<sub>`cat:ai-browsers/headless`</sub>

- [Lightpanda Browser](https://github.com/lightpanda-io/browser)
- [Steel Browser](https://github.com/steel-dev/steel-browser)

## Annotation
<sub>`cat:annotation`</sub>

*Human labeling, RLHF, and feedback-collection platforms for agent training data.*

## Automation
<sub>`cat:automation`</sub>

*General-purpose automation tools and frameworks, including GUI-driven and script-driven flows.*

### Open Source
<sub>`cat:automation/open-source`</sub>

#### GUI Based
<sub>`cat:automation/open-source/gui-based`</sub>

- [Activepieces](https://github.com/activepieces/activepieces)
- [Flowise](https://github.com/FlowiseAI/Flowise)

## Backend Querying
<sub>`cat:backend-querying`</sub>

*Tools that let agents query backend systems, databases and APIs.*

- [MindsDB](https://github.com/mindsdb/mindsdb)

## Benchmarks
<sub>`cat:benchmarks`</sub>

*Standardised benchmarks for evaluating agent and model capabilities.*

- [AICGSecEval](https://github.com/Tencent/AICGSecEval)
- [OSWorld](https://github.com/xlang-ai/OSWorld)

## Browser Automation
<sub>`cat:browser-automation`</sub>

*Libraries and services for driving real browsers under agent control.*

- [Vibium](https://github.com/VibiumDev/vibium)

## Browser Tooling
<sub>`cat:browser-tooling`</sub>

*Utilities and SDKs that sit alongside browsers to support agentic workflows.*

- [Agent Browser](https://github.com/vercel-labs/agent-browser)
- [Stagehand](https://github.com/browserbase/stagehand)

## Computer Use
<sub>`cat:computer-use`</sub>

*Agents and frameworks that operate a computer the way a human would (mouse, keyboard, screen).*

- [cua](https://github.com/trycua/cua)

### CLI
<sub>`cat:computer-use/cli`</sub>

*CLI-based computer-use agents and tools.*

- [usecomputer](https://github.com/remorses/usecomputer)

### Platform Specific
<sub>`cat:computer-use/platform-specific`</sub>

#### macOS
<sub>`cat:computer-use/platform-specific/macos`</sub>

- [cmux](https://github.com/manaflow-ai/cmux)
- [macOS-use](https://github.com/browser-use/macOS-use)

### Vision UI
<sub>`cat:computer-use/vision-ui`</sub>

*Vision-based UI understanding models for computer-use agents.*

- [UI-Venus](https://github.com/inclusionAI/UI-Venus)

## Context
<sub>`cat:context`</sub>

*Tools for building, optimising, managing and visualising the context window supplied to LLMs.*

- [PromptX](https://github.com/Deepractice/PromptX)
- [WeKnora](https://github.com/Tencent/WeKnora)

### Context Optimisation
<sub>`cat:context/context-optimisation`</sub>

- [context-mode](https://github.com/mksglu/context-mode)

### Engines
<sub>`cat:context/engines`</sub>

- [Contexto](https://github.com/ekailabs/contexto)

### Frontend Tools
<sub>`cat:context/frontend-tools`</sub>

- [react-grab](https://github.com/aidenybai/react-grab)

### Tools
<sub>`cat:context/tools`</sub>

*Utility tools, SDKs and toolkits for building, debugging and extending agentic systems.*

#### Context Managers
<sub>`cat:context/tools/context-managers`</sub>

- [dotai](https://github.com/udecode/dotai)

### Visualisation
<sub>`cat:context/visualisation`</sub>

- [context-lens](https://github.com/larsderidder/context-lens)

## Conversational Control
<sub>`cat:conversational-control`</sub>

*Systems that steer or constrain multi-turn conversations with agents.*

- [Parlant](https://github.com/emcie-co/parlant)

## Data Extraction and Structuring
<sub>`cat:data-extraction-and-structuring`</sub>

*Tools that convert unstructured data into structured form for agents to consume.*

- [Firecrawl](https://github.com/firecrawl/firecrawl)

## Data Sources
<sub>`cat:data-sources`</sub>

*Curated data feeds and providers that agents can draw on.*

### Financial
<sub>`cat:data-sources/financial`</sub>

- [OpenBB](https://github.com/OpenBB-finance/OpenBB)

## Databases
<sub>`cat:databases`</sub>

*Database systems used in agentic stacks, including purpose-built context and vector stores.*

### Context Databases
<sub>`cat:databases/context-databases`</sub>

*Databases specifically designed for storing and retrieving agent/LLM context.*

- [OpenViking](https://github.com/volcengine/OpenViking)

## Deployment Platforms
<sub>`cat:deployment-platforms`</sub>

*Platforms for deploying and hosting agents and agentic services.*

### Serverless
<sub>`cat:deployment-platforms/serverless`</sub>

- [Julep](https://github.com/julep-ai/julep)

## Dev Tools
<sub>`cat:dev-tools`</sub>

*Developer tooling that uses agents or supports agent development workflows.*

### Debugging
<sub>`cat:dev-tools/debugging`</sub>

*Debugging and introspection tools for agent development.*

- [vLLora](https://github.com/vllora/vllora)

### IDE Integrations
<sub>`cat:dev-tools/ide-integrations`</sub>

*IDE extensions and plugins for agent-assisted development.*

- [Roo-Code](https://github.com/RooCodeInc/Roo-Code)

### Repo Refactoring
<sub>`cat:dev-tools/repo-refactoring`</sub>

- [AgentRC](https://github.com/microsoft/agentrc)

## Development Platforms
<sub>`cat:development-platforms`</sub>

*End-to-end platforms for building agentic applications.*

- [Coze Studio](https://github.com/coze-dev/coze-studio)

## Embedding Models
<sub>`cat:embedding-models`</sub>

*Models used to produce embeddings for retrieval and RAG pipelines.*

## Embedding Pipeline Orchestrators
<sub>`cat:embedding-pipeline-orchestrators`</sub>

*Orchestration tools that manage embedding generation and ingestion pipelines.*

## Engineering Platforms
<sub>`cat:engineering-platforms`</sub>

*Platforms targeted at engineering teams building with LLMs and agents.*

- [VoltAgent](https://github.com/VoltAgent/voltagent)

## Environments
<sub>`cat:environments`</sub>

*Sandboxed environments — OS, simulated worlds, virtual machines — in which agents run.*

### OS
<sub>`cat:environments/os`</sub>

- [agent-os](https://github.com/rivet-dev/agent-os)

### Remote Desktops
<sub>`cat:environments/remote-desktops`</sub>

*Hosted remote desktop / VM services providing agents with a persistent GUI environment to operate.*

- [Abacus Desktop](https://desktop.abacus.ai/)
- [cua.ai](https://cua.ai/)

## Evals and Experiment Tracking
<sub>`cat:evals-and-experiment-tracking`</sub>

*Frameworks, harnesses and platforms for evaluating agents and tracking experiments.*

- [LangWatch](https://github.com/langwatch/langwatch)
- [TruLens](https://github.com/truera/trulens)

### Frameworks
<sub>`cat:evals-and-experiment-tracking/frameworks`</sub>

*General-purpose frameworks for building agents and agentic applications.*

- [DeepEval](https://github.com/confident-ai/deepeval)

### Observability
<sub>`cat:evals-and-experiment-tracking/observability`</sub>

*Logging, tracing and observability specifically for agent and LLM systems.*

- [Langfuse](https://github.com/langfuse/langfuse)

## Feedback Formatting
<sub>`cat:feedback-formatting`</sub>

*Tools that shape feedback signals (tool output, user input) into forms agents can act on.*

- [Agentation](https://github.com/benjitaylor/agentation)

## Financial Tools
<sub>`cat:financial-tools`</sub>

*Agent-oriented tools targeted at financial workflows.*

- [AgentKit](https://github.com/coinbase/agentkit)
- [GOAT](https://github.com/goat-sdk/goat)

## Formatting
<sub>`cat:formatting`</sub>

*Token-efficient serialisation and data-formatting schemes for passing structured data to and from LLMs.*

- [TOON](https://github.com/toon-format/toon)

## Foundations
<sub>`cat:foundations`</sub>

*Industry foundations, consortia and non-profits shaping the agentic AI ecosystem.*

- [Agentic AI Industry Foundation (AAIF)](https://aaif.io/)

## Frameworks
<sub>`cat:frameworks`</sub>

*General-purpose frameworks for building agents and agentic applications.*

- [AgentForge](https://github.com/DataBassGit/AgentForge)
- [AIOpsLab](https://github.com/microsoft/AIOpsLab)
- [AutoGen](https://github.com/microsoft/autogen)
- [EvoAgentX](https://github.com/EvoAgentX/EvoAgentX)
- [II-Agent](https://github.com/Intelligent-Internet/ii-agent)
- [Langflow](https://github.com/langflow-ai/langflow)
- [uAgents](https://github.com/fetchai/uAgents)
- [Vercel AI SDK](https://github.com/vercel/ai)

### .NET
<sub>`cat:frameworks/net`</sub>

- [BotSharp](https://github.com/SciSharp/BotSharp)

### Computer Use
<sub>`cat:frameworks/computer-use`</sub>

*Agents and frameworks that operate a computer the way a human would (mouse, keyboard, screen).*

- [Agent-S](https://github.com/simular-ai/Agent-S)

### Multiagent Orchestration
<sub>`cat:frameworks/multiagent-orchestration`</sub>

- [CAMEL](https://github.com/camel-ai/camel)
- [CrewAI](https://github.com/crewAIInc/crewAI)

### Multimodal
<sub>`cat:frameworks/multimodal`</sub>

- [VideoSDK Agents](https://github.com/videosdk-live/agents)

### Optimisation
<sub>`cat:frameworks/optimisation`</sub>

#### Parallelisation
<sub>`cat:frameworks/optimisation/parallelisation`</sub>

- [EnsoAI](https://github.com/J3n5en/EnsoAI)

### Social Simulations
<sub>`cat:frameworks/social-simulations`</sub>

- [Concordia](https://github.com/google-deepmind/concordia)
- Moltbook

### Stateful Design
<sub>`cat:frameworks/stateful-design`</sub>

- [Letta](https://github.com/letta-ai/letta)

### Voice
<sub>`cat:frameworks/voice`</sub>

*Voice-first agents and voice interaction frameworks.*

- [LiveKit Agents](https://github.com/livekit/agents)
- [TEN Framework](https://github.com/TEN-framework/ten-framework)

## Frontends
<sub>`cat:frontends`</sub>

*User-facing interfaces — web, desktop, mobile, terminal — for interacting with agents.*

### Android
<sub>`cat:frontends/android`</sub>

- [Operit](https://github.com/AAswordman/Operit)

### Chat UIs
<sub>`cat:frontends/chat-uis`</sub>

- [Agent UI](https://github.com/agno-agi/agent-ui)

### GUIs and CLIs
<sub>`cat:frontends/guis-and-clis`</sub>

- [Goose](https://github.com/aaif-goose/goose)

### TUIs and CLIs
<sub>`cat:frontends/tuis-and-clis`</sub>

- [Agent Deck](https://github.com/asheshgoplani/agent-deck)

## Gateways
<sub>`cat:gateways`</sub>

*Gateway services that sit between agents and upstream services (LLMs, tools, data).*

### Context Compression
<sub>`cat:gateways/context-compression`</sub>

- [Context-Gateway](https://github.com/Compresr-ai/Context-Gateway)

## Geopolitical Simulation
<sub>`cat:geopolitical-simulation`</sub>

*Simulations focused specifically on geopolitical scenarios and dynamics.*

- [Snowglobe](https://github.com/IQTLabs/snowglobe)
- [WargamesAI](https://github.com/user1342/WargamesAI)

## Guardrails
<sub>`cat:guardrails`</sub>

*Guardrails and pre-execution safety checks that gate what running agents can do.*

- [Shellfirm](https://github.com/kaplanelad/shellfirm)

## Harnesses
<sub>`cat:harnesses`</sub>

*Test harnesses and runner frameworks that host and exercise agents.*

- [Hive](https://github.com/aden-hive/hive)
- [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)

### Deep Research
<sub>`cat:harnesses/deep-research`</sub>

- [DeepAgents](https://github.com/langchain-ai/deepagents)

### macOS
<sub>`cat:harnesses/macos`</sub>

*Harnesses that run agents natively on macOS.*

- [Osaurus](https://github.com/osaurus-ai/osaurus)

## Identity and Auth
<sub>`cat:identity-and-auth`</sub>

*Agent identity, credential vaulting, and delegated authentication for tool access.*

## Inference Servers
<sub>`cat:inference-servers`</sub>

*LLM inference servers and runtimes (vLLM, TGI, llama.cpp, SGLang) that agents call into.*

## Integrations
<sub>`cat:integrations`</sub>

*Agent-to-SaaS connector platforms: Composio-style libraries exposing third-party APIs as agent tools.*

- [Composio](https://github.com/ComposioHQ/composio)

## LLMs
<sub>`cat:llms`</sub>

*Language models, including those trained or tuned specifically for agentic use cases.*

- Gemini 3.1

### Agent Specific
<sub>`cat:llms/agent-specific`</sub>

- [Grok 4.20 Multi-Agent](https://openrouter.ai/x-ai/grok-4.20-multi-agent)

### By Use Case
<sub>`cat:llms/by-use-case`</sub>

#### Computer Use
<sub>`cat:llms/by-use-case/computer-use`</sub>

*Agents and frameworks that operate a computer the way a human would (mouse, keyboard, screen).*

- [Fara](https://github.com/microsoft/fara)

## Loops
<sub>`cat:loops`</sub>

*Agent loop implementations — the core think/act/observe cycle.*

- [Ralph](https://github.com/snarktank/ralph)

## Marketplaces
<sub>`cat:marketplaces`</sub>

*Marketplaces and stores for discovering, listing, or transacting agents and agent-based services.*

- [agen.cy Marketplace](https://marketplace.agen.cy/)
- [AI Agent Store](https://aiagentstore.ai/)

## MCP
<sub>`cat:mcp`</sub>

*Projects in the Model Context Protocol ecosystem — servers, gateways, aggregators, clients.*

### Aggregation
<sub>`cat:mcp/aggregation`</sub>

- [Klavis](https://github.com/Klavis-AI/klavis)

### Gateways
<sub>`cat:mcp/gateways`</sub>

*Gateway services that sit between agents and upstream services (LLMs, tools, data).*

- [MCP Context Forge](https://github.com/IBM/mcp-context-forge)

### Third Party
<sub>`cat:mcp/third-party`</sub>

- [MCP Server Airbnb](https://github.com/openbnb-org/mcp-server-airbnb)

## Memory
<sub>`cat:memory`</sub>

*Memory systems for agents — short-term, long-term, episodic, file-backed, graph-backed.*

- [AgentMemory](https://github.com/rohitg00/agentmemory)
- [Cognee](https://github.com/topoteretes/cognee)
- [Mem0](https://github.com/mem0ai/mem0)
- [MemOS](https://github.com/MemTensor/MemOS)

### File
<sub>`cat:memory/file`</sub>

- [Memvid](https://github.com/memvid/memvid)

### Regressive
<sub>`cat:memory/regressive`</sub>

- [Agentic Context Engine](https://github.com/kayba-ai/agentic-context-engine)

### Skills
<sub>`cat:memory/skills`</sub>

*Agent skills ecosystems — registries, bundles, standards, guides and package libraries.*

- [Acontext](https://github.com/memodb-io/Acontext)

## Multiagent
<sub>`cat:multiagent`</sub>

*Systems built around multiple cooperating or competing agents.*

### Large Scale Experiments
<sub>`cat:multiagent/large-scale-experiments`</sub>

- [AgentTorch](https://github.com/AgentTorch/AgentTorch)

### Swarm Prediction
<sub>`cat:multiagent/swarm-prediction`</sub>

- [MiroFish](https://github.com/666ghj/MiroFish)

## Networks
<sub>`cat:networks`</sub>

*Agent networks and directories — social/professional platforms where agents and their creators are listed and interconnected.*

- [agent.ai](https://agent.ai/)

## Observability
<sub>`cat:observability`</sub>

*Logging, tracing and observability specifically for agent and LLM systems.*

- [RagaAI Catalyst](https://github.com/raga-ai-hub/RagaAI-Catalyst)

## On Device Agents
<sub>`cat:on-device-agents`</sub>

*Agents designed to run on-device, including phones, SBCs and edge hardware.*

### Android
<sub>`cat:on-device-agents/android`</sub>

*Android-specific agent runtimes and device-level automation.*

- [Agent Device](https://github.com/callstackincubator/agent-device)

### SBCs
<sub>`cat:on-device-agents/sbcs`</sub>

- [be-more-agent](https://github.com/brenpoly/be-more-agent)

## Operations
<sub>`cat:operations`</sub>

*Operational concerns for running agents in production — cost, monitoring, reliability.*

### Cost Monitoring
<sub>`cat:operations/cost-monitoring`</sub>

- [AgentOps](https://github.com/AgentOps-AI/agentops)

## Optimisation Platform
<sub>`cat:optimisation-platform`</sub>

*Platforms focused on optimising agent/LLM pipelines.*

- [Coze Loop](https://github.com/coze-dev/coze-loop)

## Orchestration
<sub>`cat:orchestration`</sub>

*Orchestration engines for coordinating agents, tools and workflows.*

- [Agent Orchestrator](https://github.com/ComposioHQ/agent-orchestrator)
- [AI Maestro](https://github.com/23blocks-OS/ai-maestro)
- [Conductor](https://github.com/conductor-oss/conductor)
- [Shannon](https://github.com/Kocoro-lab/Shannon)

### Platform-Specific
<sub>`cat:orchestration/platform-specific`</sub>

- [Agent Squad](https://github.com/awslabs/agent-squad)

## Personal AI
<sub>`cat:personal-ai`</sub>

*Personal AI assistants and related projects.*

- [Crucix](https://github.com/calesthio/Crucix)
- [Nanobot](https://github.com/HKUDS/nanobot)

### Assistants
<sub>`cat:personal-ai/assistants`</sub>

- [Leon](https://github.com/leon-ai/leon)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Personification
<sub>`cat:personification`</sub>

*Tools for giving agents distinct personas, voices and identities.*

- [Bub](https://github.com/bubbuild/bub)

## PII and Redaction
<sub>`cat:pii-and-redaction`</sub>

*PII detection, content sanitization, and safety filtering for agent I/O.*

## Pipelines
<sub>`cat:pipelines`</sub>

*Reusable pipelines for common agentic workloads.*

- [Paper2Agent](https://github.com/jmiao24/Paper2Agent)

## Platforms
<sub>`cat:platforms`</sub>

*General platforms that host or enable agentic applications.*

### Embodied
<sub>`cat:platforms/embodied`</sub>

- [Fairo](https://github.com/facebookresearch/fairo)

## Prompt Management
<sub>`cat:prompt-management`</sub>

*Versioning, registries, and lifecycle management for prompts as first-class artifacts.*

## Proxy
<sub>`cat:proxy`</sub>

*Proxy services that sit between clients and LLM/agent backends.*

### Gateways
<sub>`cat:proxy/gateways`</sub>

*Gateway services that sit between agents and upstream services (LLMs, tools, data).*

- [AgentGateway](https://github.com/agentgateway/agentgateway)
- [LiteLLM](https://github.com/BerriAI/litellm)

### MCP to OpenAI
<sub>`cat:proxy/mcp-to-openai`</sub>

- [MCPO](https://github.com/open-webui/mcpo)

## RAG
<sub>`cat:rag`</sub>

*Retrieval-augmented generation engines, frameworks and components.*

- [Airweave](https://github.com/airweave-ai/airweave)

### Engines
<sub>`cat:rag/engines`</sub>

- [RAGFlow](https://github.com/infiniflow/ragflow)

### Ingestion
<sub>`cat:rag/ingestion`</sub>

*Pipelines that ingest and process documents into retrieval systems.*

- [Agent-Reach](https://github.com/Panniantong/Agent-Reach)

## Reinforcement Learning
<sub>`cat:reinforcement-learning`</sub>

*RL frameworks and environments used to train agentic behaviour.*

- [Acme](https://github.com/google-deepmind/acme)
- [RLinf](https://github.com/RLinf/RLinf)

## Routers
<sub>`cat:routers`</sub>

*Routing layers that select between models, tools or agents based on cost, capability or intent.*

### Cost Optimisation
<sub>`cat:routers/cost-optimisation`</sub>

- [RelayPlane Proxy](https://github.com/RelayPlane/proxy)

### Intelligent
<sub>`cat:routers/intelligent`</sub>

- [Agentic Flow](https://github.com/ruvnet/agentic-flow)
- [Semantic Router](https://github.com/vllm-project/semantic-router)

### Tool Specific
<sub>`cat:routers/tool-specific`</sub>

- [ClawRouter](https://github.com/BlockRunAI/ClawRouter)

## Runtimes
<sub>`cat:runtimes`</sub>

*Execution runtimes — sandboxes, data layers, kernels — that host running agents.*

- [OpenShell](https://github.com/NVIDIA/OpenShell)

### Data Layers
<sub>`cat:runtimes/data-layers`</sub>

- [Deep Lake](https://github.com/activeloopai/deeplake)

### Policy Engines
<sub>`cat:runtimes/policy-engines`</sub>

*Runtime policy engines that evaluate and enforce rules on agent actions.*

- [Aegis](https://github.com/Justin0504/Aegis)

### Sandboxes
<sub>`cat:runtimes/sandboxes`</sub>

- [OpenSandbox](https://github.com/alibaba/OpenSandbox)

## SaaS Builders
<sub>`cat:saas-builders`</sub>

*Hosted SaaS platforms for building agents and agentic workflows, spanning no-code, visual, and code-defined paradigms.*

### Code-Defined
<sub>`cat:saas-builders/code-defined`</sub>

*Hosted builders where agents and workflows are primarily defined in code (SDK, DSL, or config-as-code).*

### No Code
<sub>`cat:saas-builders/no-code`</sub>

*Builders targeted at non-programmers, typically form- and config-driven with minimal visual wiring.*

### Visual Programming
<sub>`cat:saas-builders/visual-programming`</sub>

*Builders where flows are expressed as node-and-edge graphs or canvas-based visual programs.*

- [n8n](https://n8n.io/)

#### Workflow Focused
<sub>`cat:saas-builders/visual-programming/workflow-focused`</sub>

*Visual builders oriented around structured, multi-step workflows rather than free-form agents.*

- [Gumloop](https://www.gumloop.com/)
- [MindStudio](https://www.mindstudio.ai/)

## Security
<sub>`cat:security`</sub>

*Security tooling for agents: sandboxing, red teaming, defensive automation.*

- [agent-scan](https://github.com/snyk/agent-scan)
- [AgentGuard](https://github.com/GoPlusSecurity/agentguard)

### Automation
<sub>`cat:security/automation`</sub>

*General-purpose automation tools and frameworks, including GUI-driven and script-driven flows.*

- [Tracecat](https://github.com/TracecatHQ/tracecat)

### Control Planes
<sub>`cat:security/control-planes`</sub>

*Centralised control planes for governing, auditing, and enforcing policy across agent fleets.*

- [Cordum](https://github.com/cordum-io/cordum)

### Red Team
<sub>`cat:security/red-team`</sub>

- [Rogue](https://github.com/qualifire-dev/rogue)

### Sandboxing
<sub>`cat:security/sandboxing`</sub>

- [Microsandbox](https://github.com/superradcompany/microsandbox)

## Semantic Caching
<sub>`cat:semantic-caching`</sub>

*Cache layers that serve semantically equivalent LLM responses to cut cost and latency.*

## Semantic Search
<sub>`cat:semantic-search`</sub>

*Semantic search tools for agents operating over codebases and local content.*

- [osgrep](https://github.com/Ryandonofrio3/osgrep)

## Skills
<sub>`cat:skills`</sub>

*Agent skills ecosystems — registries, bundles, standards, guides and package libraries.*

- [Agent Skills](https://github.com/addyosmani/agent-skills)

### Bundles
<sub>`cat:skills/bundles`</sub>

#### Claude Code
<sub>`cat:skills/bundles/claude-code`</sub>

- [Marketing Skills](https://github.com/coreyhaines31/marketingskills)

### Guides
<sub>`cat:skills/guides`</sub>

- [Taste Skill](https://github.com/Leonxlnx/taste-skill)

### Package Library
<sub>`cat:skills/package-library`</sub>

- [Vercel Skills](https://github.com/vercel-labs/skills)

### Registries
<sub>`cat:skills/registries`</sub>

- [Agent Skills (tech-leads-club)](https://github.com/tech-leads-club/agent-skills)

### Standards
<sub>`cat:skills/standards`</sub>

*Proposed and emerging standards across the agentic ecosystem.*

- [AgentSkills](https://github.com/agentskills/agentskills)

## Societal Simulations
<sub>`cat:societal-simulations`</sub>

*Large-scale simulations of societies and human behaviour using agent populations.*

- [OASIS](https://github.com/camel-ai/oasis)

## Software Extensions
<sub>`cat:software-extensions`</sub>

*Extensions and plugins that add agentic capabilities to existing software.*

- [Jupyter AI](https://github.com/jupyterlab/jupyter-ai)

## Standards
<sub>`cat:standards`</sub>

*Proposed and emerging standards across the agentic ecosystem.*

### Emerging (Ecosystem-Tied)
<sub>`cat:standards/emerging-ecosystem-tied`</sub>

*Emerging standards whose adoption is tied to a specific host ecosystem (e.g. a browser engine or platform vendor) rather than being fully vendor-neutral.*

- [WebMCP](https://webmcp.dev/)
- [WebMCP (Chrome EPP)](https://developer.chrome.com/blog/webmcp-epp)

### Proposed
<sub>`cat:standards/proposed`</sub>

- [AIUC-1](https://www.aiuc-1.com/)
- [GitAgent](https://github.com/open-gitagent/gitagent)

### Ratified
<sub>`cat:standards/ratified`</sub>

*Standards with a published specification and active governance.*

- [A2A (Agent2Agent Protocol)](https://github.com/a2aproject/A2A)
- [AG-UI (Agent User Interaction Protocol)](https://docs.ag-ui.com/introduction)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/specification/2025-11-25)

## Starter Kits
<sub>`cat:starter-kits`</sub>

*Opinionated starter kits and templates for kicking off agentic projects.*

### Social Simulations
<sub>`cat:starter-kits/social-simulations`</sub>

- [AI Town](https://github.com/a16z-infra/ai-town)

## Structured Output
<sub>`cat:structured-output`</sub>

*Libraries that constrain LLM outputs to typed schemas, JSON, or formal grammars.*

## Synthesised Perspectives
<sub>`cat:synthesised-perspectives`</sub>

*Tools that synthesise multiple viewpoints or agent outputs into a unified perspective.*

- [LLM Council](https://github.com/karpathy/llm-council)
- [Plurals](https://github.com/josh-ashkinaze/plurals)

## Synthetic Data
<sub>`cat:synthetic-data`</sub>

*Tools for generating synthetic training and evaluation data for agents.*

## Task Specific
<sub>`cat:task-specific`</sub>

*Agents and tools built for a single specific task rather than general use.*

### Product Design
<sub>`cat:task-specific/product-design`</sub>

- [Superdesign](https://github.com/superdesigndev/superdesign)

## Trainers
<sub>`cat:trainers`</sub>

*Training frameworks and tools for agent models.*

- [Agent Lightning](https://github.com/microsoft/agent-lightning)

## Uncategorized
<sub>`cat:uncategorized`</sub>

*Holding area for projects awaiting classification. Entries here are a todo list, not a destination.*

- [Agency Agents](https://github.com/msitarzewski/agency-agents)

## Upserting Tools
<sub>`cat:upserting-tools`</sub>

*Tools that manage upserting data into vector stores and retrieval indexes.*

## UX
<sub>`cat:ux`</sub>

*User-experience patterns and components specifically for agent systems.*

### Human in the Loop
<sub>`cat:ux/human-in-the-loop`</sub>

*Interfaces and workflows for inserting humans into agent execution — approvals, task handoff, review queues.*

- [Agent Inbox](https://github.com/langchain-ai/agent-inbox)
- [Orchestra](https://github.com/b12io/orchestra)

## Vector Databases
<sub>`cat:vector-databases`</sub>

*Vector databases used for embedding storage and similarity search.*

- [Qdrant](https://github.com/qdrant/qdrant)

## Voice
<sub>`cat:voice`</sub>

*Voice-first agents and voice interaction frameworks.*

- [Bolna](https://github.com/bolna-ai/bolna)

## Workflow Definition
<sub>`cat:workflow-definition`</sub>

*Tools and DSLs for authoring agent workflows as first-class, portable artifacts.*

- [Packmind](https://github.com/PackmindHub/packmind)

## Workspaces
<sub>`cat:workspaces`</sub>

*Shared workspaces where agents and humans (or multiple agents) collaborate.*

- [AgentsMesh](https://github.com/AgentsMesh/AgentsMesh)
- [Gastown](https://github.com/gastownhall/gastown)
- [LobeHub](https://github.com/lobehub/lobehub)

## World Generation
<sub>`cat:world-generation`</sub>

*Tools and models for generating simulated worlds for agents to operate in.*

- [ML-Agents](https://github.com/Unity-Technologies/ml-agents)

### MCP
<sub>`cat:world-generation/mcp`</sub>

*MCP servers for world and scene generation.*

- [Unreal Engine MCP](https://github.com/flopperam/unreal-engine-mcp)
