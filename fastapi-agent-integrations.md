# Open-source–style integration layers for FastAPI agents

This note summarizes options when you want something **like [Corsair](https://corsair.dev/)** (a unified integration layer for AI agents) but your app is built with **FastAPI** and you need **broad third-party coverage** (often described as “~90% of integrations”).

There is **no single** fully open-source, self-contained, Python-native package that matches Corsair’s *entire* model (prebuilt plugins, auth, local DB, agent tool surface) **and** covers most arbitrary enterprise SaaS products out of the box. What you can do is pick a **pattern** and accept tradeoffs: **hosted vs self-hosted**, **breadth vs control**, **one vendor vs many packages**.

---

## 1. Composio — closest to “one integration layer,” Python-first

**What it is:** A large catalog of agent-oriented **toolkits** (marketing/docs often cite **1000+** apps). First-class **Python SDK**: `pip install composio`. Integrates with **OpenAI Agents, Anthropic, LangChain, LangGraph, LlamaIndex**, and others.

**License:** **MIT** for the SDK repository ([ComposioHQ/composio](https://github.com/ComposioHQ/composio)).

**Important caveat:** Tool execution, auth orchestration, and the integration catalog are backed by **Composio’s cloud service** (API key). The **SDK is open source**, but this is **not** the same as “all integration logic runs only on your machine” in the Corsair self-hosted DB sense.

**FastAPI:** Natural fit—instantiate Composio in dependencies or services, run the agent loop in route handlers or background tasks, and forward tool calls through the SDK.

**Docs:** [https://docs.composio.dev/](https://docs.composio.dev/)

---

## 2. Nango — self-hostable auth and API access; FastAPI talks over HTTP

**What it is:** Platform for **product integrations** with **700+ APIs**, strong at **OAuth, token storage, and proxying**. Positions **AI tool calling and MCP** for higher tiers; **free self-hosted** edition focuses on **authorization** (see [Nango self-hosting docs](https://docs.nango.dev/guides/self-hosting/free-self-hosting/overview) for feature comparison vs cloud/enterprise).

**License:** **Elastic License** (vendor “open source”; **not** MIT/Apache—check compliance with your organization).

**FastAPI:** Keep **Python** for the API; run Nango as a **separate service**; call it via **REST** from FastAPI. Integration **functions** in Nango are often **TypeScript** in their runtime model.

**Docs:** [https://docs.nango.dev/](https://docs.nango.dev/)

---

## 3. LangChain / LangGraph — OSS ecosystem, you assemble coverage

**What it is:** Large **Python** ecosystem (`langchain-community`, etc.) with many **tools** and patterns for agents. **Apache-2.0** for core pieces you typically depend on (verify per package).

**Caveat:** Breadth is **fragmented**—many integrations, uneven maintenance, and **authentication** is often **your** responsibility unless you pair with Nango or another auth layer.

**FastAPI:** Very common: define agents and tools in Python, expose them behind FastAPI routes or workers.

---

## 4. LlamaIndex — similar role to LangChain for tools and connectors

**What it is:** **Python**-first stack for agents, RAG, and tool use; connector surface grows by module.

**Caveat:** Same as LangChain: **no single gateway**—you **curate** integrations and auth.

**FastAPI:** Fits well for APIs that run retrieval + agent steps.

---

## 5. MCP-first stack — fully composable OSS, no single catalog owner

**What it is:** [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) with an official **Python SDK**. You run or subscribe to **MCP servers** (community or internal) that expose tools; your app acts as an **MCP client**.

**Caveat:** “90% coverage” means **operating and selecting many servers**, not one product. You own **composition, security, and lifecycle**.

**FastAPI:** Orchestrate the agent in Python; connect to MCP servers from workers or dedicated processes.

---

## 6. OpenAI Agents SDK (Python) — agent runtime, not a connector catalog

**What it is:** **MIT**-licensed [OpenAI Agents SDK for Python](https://github.com/openai/openai-agents-python)—strong **orchestration**, **tools**, **MCP** support.

**Caveat:** It does **not** replace an integration catalog; pair it with **Composio**, **MCP**, or **custom tools**.

**FastAPI:** Use inside routes/tasks as the agent engine.

---

## Practical recommendations (FastAPI + “~90%” integrations)

| Goal | Stack | Why |
|------|--------|-----|
| **Fastest path to many SaaS tools** | **FastAPI + Composio (Python)** | Widest prebuilt **agent tools**; accept **hosted** execution/auth plane. |
| **Bias toward self-hosted credentials / proxy** | **FastAPI + Nango (self-hosted) + your tool layer** | Central **OAuth and proxy**; you may still implement **actions** or use paid Nango features for full agent/MCP parity. |
| **Fully OSS runtime, no integration SaaS** | **FastAPI + LangChain or LlamaIndex + MCP (+ optional Nango for OAuth only)** | Maximum control; **more assembly and maintenance**. |

---

## Bottom line

- If **“90%”** means **hundreds of SaaS products with managed OAuth and ready-made tools**, **Composio** is the closest **Python** experience to Corsair’s *product shape*, with the major difference that **much of the system runs as a cloud service**.
- If **“90%”** means **your data and control plane stay on your infrastructure**, expect **Nango (or similar) for auth** plus **MCP servers, generated API clients, and a small tool registry in FastAPI**—not one drop-in library.

For Corsair specifically (TypeScript, local DB, plugins), see [`corsair.md`](./corsair.md) in this repo, including the **FastAPI + MCP bridge** pattern.

---

*This document is operational guidance, not legal advice on licenses. Confirm each project’s current license and terms before production use.*
