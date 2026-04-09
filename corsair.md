# The Agent Integration Problem & Corsair

> **Note:** Some demos and scripts refer to the product as “Corsier.” The open-source integration layer is **Corsair** ([GitHub](https://github.com/corsairdev/corsair), [docs](https://docs.corsair.dev/)). This file follows your video’s ideas and flow; package and CLI names below match the real project.

---

## What Is the Agent Integration Problem?

In a typical **web application**—whether the backend is **Node.js**, **FastAPI (Python)**, or something else—integrations follow a familiar pattern:

- **Slack:** `npm install` the Slack SDK (or use APIs), proxy calls on the user’s behalf, store and use their token, talk to Slack.
- **GitHub:** Same idea—install the GitHub SDK and proxy requests with user credentials.

Each new integration means a new package, new auth flow, and new code paths. That is workable when humans click buttons and your server makes deliberate API calls.

The **agentic** world is different: users often do not drive UI flows or explicit API calls. Instead, an **AI agent** must act on their behalf. The model still needs real integrations—Slack, GitHub, Gmail, etc.—but the way you expose capability changes.

Without a shared layer, you end up doing one of the following:

1. **Hand-building tools** for every operation (send Slack message, read channel, update profile, open a PR, list repos, …)—dozens of tools per service, duplicated effort across projects.
2. **Prompting the model to “just curl” APIs**—weak auth story, brittle behavior, and a poor experience for real agents.

**The core issue:** Users expect an agent to “do anything” (e.g. read a GitHub profile, post to Slack). Integrations are table stakes, yet there is no single standard library or gateway that exposes them all in an agent-friendly way—so teams keep rebuilding the same glue.

---

## How Corsair Fits In

**Corsair** is a **free, open-source integration layer** for agents:

- Your agent talks to **one interface** (Corsair—often via a small set of MCP tools such as setup, list operations, get schema, and run).
- Corsair **proxies** to services like Slack, Linear, GitHub, Gmail, Google Calendar, and others using **prebuilt plugins / operations**.
- You **configure** which integrations apply (e.g. credentials in your DB); the agent discovers and invokes operations through Corsair instead of you reimplementing every tool.

Conceptually:

| Without a gateway | With Corsair |
|-------------------|--------------|
| Workflow glue, SDKs, and ad hoc HTTP per vendor | One adapter; consistent tool surface per integration |
| Reinventing auth and schemas each time | Centralized plumbing (auth, storage, rate limits, etc.—per project docs) |

Corsair is **open-source** ([corsairdev/corsair](https://github.com/corsairdev/corsair)) and is designed so **your data stays in your database** (e.g. SQLite or Postgres), not in a third-party integration hub.

---

## Quick Start (Demo Flow)

The following mirrors a minimal local setup like the video walkthrough.

### 1. Project setup

- Create a directory (e.g. `corsair-demo`) and open it in your editor.
- Initialize: `pnpm init`
- Install Corsair (see [Installation](https://docs.corsair.dev/) for the exact packages your stack needs—for example `corsair` and, for MCP, `@corsair-dev/mcp`):

  ```bash
  pnpm add corsair
  ```

### 2. Environment and database

- Set a **key encryption key (KEK)** for Corsair (e.g. `CORSAIR_KEK` in `.env`)—this is **not** the same as vendor API keys. Follow the official docs for generation and format.
- Use **SQLite** for simplicity (Postgres is supported): e.g. `better-sqlite3` or the driver the docs recommend.
- Run the **database migration** from the docs so Corsair has the right schema.

### 3. Connect GitHub (example)

- Create a **GitHub Classic personal access token** with the scopes you need (repos, user, notifications, etc.) and **omit** scopes you do not want (e.g. delete).
- Store the token securely and register it with Corsair using the **CLI** (`corsair setup`, **backfill**, or the current equivalent—see docs).

### 4. `corsair.ts` / `corsair.js` entry

Declare integrations in one place (pattern from [docs](https://docs.corsair.dev/)):

```typescript
import { createCorsair, github /* , slack, gmail, linear, googlecalendar */ } from "corsair";

export const corsair = createCorsair({
  plugins: [github()],
  database: db,
  kek: process.env.CORSAIR_KEK!,
});
```

Instantiate the DB and export the Corsair instance so credentials and plugins match what you configured.

### 5. Agent with Anthropic (example)

- Install: `pnpm add @anthropic-ai/sdk` (and `dotenv` if needed).
- Set `ANTHROPIC_API_KEY`.
- Use `"type": "module"` in `package.json` if you use ESM.
- Wire Corsair into your agent (direct SDK or **MCP**—see [MCP Adapters](https://docs.corsair.dev/)). Example prompts:

  - *“Use Corsair to fetch my account information on GitHub.”*
  - *“Use Corsair to fetch my repo count and latest repo on GitHub.”*

The model uses Corsair’s operations instead of a long list of custom GitHub tools you wrote by hand.

### 6. Adding more integrations

Add plugins to the `plugins` array—**Slack, Gmail, Linear, Google Calendar**, etc.—so one gateway exposes many services.

---

## Can you implement the same thing with FastAPI?

**Short answer:** You cannot drop **Corsair’s own SDK** into FastAPI today—Corsair is a **TypeScript / Node.js** library ([corsair](https://www.npmjs.com/package/corsair) on npm). The official docs list frameworks like the Anthropic SDK, OpenAI Agents, and Vercel AI SDK in the **JavaScript** ecosystem, not a Python package.

You **can** still get a **very similar outcome** (one integration surface your agent calls instead of dozens of hand-made tools) by choosing one of these patterns:

### 1. FastAPI orchestrates the agent; Corsair runs as an MCP server (recommended hybrid)

Corsair exposes a small **MCP** tool surface (`corsair_setup`, `list_operations`, `get_schema`, execution tools—see [docs](https://docs.corsair.dev/)). Typical setup uses a **stdio MCP server** from Node (`@corsair-dev/mcp`).

- Keep **credentials, migrations, and plugins** in the **Node + Corsair** process (same as the quick start).
- In **Python**, use an **MCP client** (e.g. the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) or your agent framework’s MCP support) to connect to that server.
- **FastAPI** can own HTTP routes, auth, sessions, and job queues; a route or background worker runs the **agent loop** (Anthropic/OpenAI Python SDK) and forwards **tool calls** to the Corsair MCP server.

Conceptually:

```text
User → FastAPI → Python agent (LLM + tool loop) → MCP → Node (Corsair) → Slack / GitHub / …
```

This matches how many stacks combine **Python APIs** with **non-Python tools** without reimplementing Corsair in Python.

### 2. Two services: FastAPI + a small Node “integration” service

If you prefer not to use MCP from Python, you can run Corsair in a **dedicated Node service** and call it from FastAPI over **internal HTTP** only if you add a thin API wrapper yourself (Corsair’s primary agent-facing interface is MCP-oriented, so pattern **1** is usually simpler).

### 3. “All in FastAPI” without Corsair

If everything must stay in **Python** only, there is **no official Corsair equivalent** in one `pip install`. You would:

- Use **vendor SDKs** (`httpx`, `slack-sdk`, `PyGithub`, etc.) and register them as **tools** for your agent (LangChain, LlamaIndex, OpenAI Agents for Python, custom tool schemas), or  
- Use a **third-party agent integration platform** (commercial or OSS) that targets Python—evaluating those is separate from Corsair.

That gives you the same *idea* (agents + integrations) but **not** the same prebuilt plugin catalog and DB/auth model as Corsair unless you adopt a different product.

### Summary table

| Approach | Same as video’s embedded `corsair` in Node? | Notes |
|----------|---------------------------------------------|--------|
| Corsair MCP server + FastAPI + Python agent | **Behaviorally yes** (one gateway, many integrations) | Two runtimes; production needs process supervision or containers. |
| Rewrite integrations only in FastAPI | **No** (you rebuild tools) | Full control, more maintenance. |
| Wait for / contribute a Python port of Corsair | **N/A** | Not available as of current upstream project scope. |

---

## Platform Features (from the overview)

- **MCP adapters** and support for common stacks (Claude, Anthropic, OpenAI-style agents, Vercel AI SDK, Mastra, etc.—per docs).
- Docs cover **authentication**, **APIs**, **database**, **hooks**, and **multi-tenancy** (isolated credentials per tenant for SaaS).
- Guides for **custom plugins** and new integrations.
- **Prebuilt integrations** include Slack, GitHub, Gmail, Linear, Google Calendar, and others; the list grows over time.

---

## Summary

**Corsair** is an **adapter and gateway** for the agent layer: configure integrations once, let Corsair expose a consistent discovery/execution model, and avoid rebuilding OAuth, token storage, and per-vendor tool matrices from scratch for every project.

If you are in the agent space and hitting this problem, try Corsair, read [docs.corsair.dev](https://docs.corsair.dev/), and consider **contributing** new integrations on [GitHub](https://github.com/corsairdev/corsair).

---

## Links

- **Repository:** [https://github.com/corsairdev/corsair](https://github.com/corsairdev/corsair)
- **Documentation:** [https://docs.corsair.dev/](https://docs.corsair.dev/)
- **Site:** [https://corsair.dev/](https://corsair.dev/)

---

*Derived from a video walkthrough. CLI flags, env variable names, and migration steps can change—always use the latest README and docs.*
