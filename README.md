<div align="center">

<a href="https://mycel-ai.de/en" title="Mycel">
  <img src="https://raw.githubusercontent.com/MycelAI/.github/main/profile/logo-dark.png"
       alt="Mycel"
       width="320">
</a>

# Mycel Agent SDK

**Multi-agent workflows in Python — gateways, built-in tools, and clear permission
models for production-grade agents.**

*Cultivating intelligent transformation — [mycel-ai.de](https://mycel-ai.de/en)*

[![PyPI version](https://img.shields.io/pypi/v/mycel-agent-sdk.svg)](https://pypi.org/project/mycel-agent-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/mycel-agent-sdk.svg)](https://pypi.org/project/mycel-agent-sdk/)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-0d9488.svg)](https://mycelai.github.io/mycel-agent-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-0d9488.svg)](LICENSE)
[![Website](https://img.shields.io/badge/Website-mycel--ai.de-0d9488.svg)](https://mycel-ai.de/en)
[![Organization](https://img.shields.io/badge/GitHub-MycelAI-0d9488.svg)](https://github.com/MycelAI)

[Documentation](https://mycelai.github.io/mycel-agent-sdk/) ·
[Examples](examples/) ·
[Gateway](gateway/README.md) ·
[Org profile](https://github.com/MycelAI/.github/blob/main/profile/README.md)

</div>

---

## Fork lineage and release status

This repository is a **fork** of
**[openai/openai-agents-python](https://github.com/openai/openai-agents-python)**
(the OpenAI Agents SDK for Python). We track **our own SemVer** on PyPI as
**[`mycel-agent-sdk`](https://pypi.org/project/mycel-agent-sdk/)** while keeping
the familiar **`import agents`** module layout.

**Release posture:** `main` carries **ongoing fork development**. Published
versions are listed in [**CHANGELOG.md**](CHANGELOG.md); behaviour and APIs may
diverge from upstream between syncs. Treat **migration to this fork** like any
major dependency: pin versions, read the changelog, and validate gateways or
providers in staging.

Upstream JS/TS SDK: **[openai/openai-agents-js](https://github.com/openai/openai-agents-js)**.

---

## Vision (why this fork exists)

The roadmap is captured in the living **ExecPlan**
[**`docs/execplans/mycel-fork-gateway-and-rust-tiers.md`**](docs/execplans/mycel-fork-gateway-and-rust-tiers.md)
and in **[`PLANS.md`](PLANS.md)** (how ExecPlans are written here). In short:

| Theme | Intent |
| --- | --- |
| **Rust gateway** | Multi-provider access through an **OpenAI Chat Completions + SSE**-compatible HTTP service in [`gateway/`](gateway/), consumed from Python via `OpenAIChatCompletionsModel` and `AsyncOpenAI(base_url=..., api_key=...)`. Routing and provider keys **belong at the gateway**, not scattered across Python adapters. |
| **LiteLLM removed** | **No built-in LiteLLM** dependency or `Litellm*` classes in this distribution. That cuts a large optional surface area and keeps **one** opinionated path: OpenAI-native APIs, **Any-LLM** where appropriate, or **your gateway**. See [models](https://mycelai.github.io/mycel-agent-sdk/models/) and [**Gateway model provider**](https://mycelai.github.io/mycel-agent-sdk/gateway_model_provider/). |
| **Built-ins & permissions** | First-class **coding and research tool presets** under **`agents.tools.builtin`** (file, shell, web helpers) plus a **unified permission model** (`PermissionMode`, allowlists/blocklists, `RunConfig.permission_mode`) so agent runs behave more like **modern agent products**—the same *class* of ergonomics people expect from **Claude-style agent CLIs and similar SDKs**—without implying any endorsement or shared codebase with Anthropic. |
| **Wire types & optional Rust** | **Canonical DTOs** in **`agents.wire`** and an optional **PyO3** accelerator stub in [`rust/mycel_accelerator/`](rust/mycel_accelerator/) so hot paths can tighten over time **without** blocking Python workflows. |
| **Bundled prompts & evals** | Versioned **bundled prompts** and a small **eval harness** (`examples/evals/`, `tests/evals/`) to regress behaviour on real `RunResult` traces—not only mocks. |

Operational detail, decision log, and validation commands live in the ExecPlan;
day-to-day contributor rules are in **[`AGENTS.md`](AGENTS.md)**.

---

## Highlights

| | |
| --- | --- |
| **Agents** | Instructions, tools, guardrails, handoffs — [docs](https://mycelai.github.io/mycel-agent-sdk/agents) |
| **Tools & MCP** | Function tools, MCP, hosted tools — [docs](https://mycelai.github.io/mycel-agent-sdk/tools/) |
| **Built-in toolkits** | Presets such as `FILE_TOOLS`, `SHELL_TOOLS`, `WEB_TOOLS`, `CODING_TOOLKIT` — [`agents.tools.builtin`](src/agents/tools/builtin/) |
| **Sessions** | Conversation history across runs — [docs](https://mycelai.github.io/mycel-agent-sdk/sessions/) |
| **Tracing** | Debug and optimize runs — [docs](https://mycelai.github.io/mycel-agent-sdk/tracing/) |
| **Realtime** | Voice agents — [quickstart](https://mycelai.github.io/mycel-agent-sdk/realtime/quickstart/) |
| **Providers** | OpenAI Responses / Chat Completions, gateway, **Any-LLM** (optional extra) — [models](https://mycelai.github.io/mycel-agent-sdk/models/) |

---

## Install

**Python 3.10+** required.

### pip

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install mycel-agent-sdk
```

Optional extras:

- Voice: `pip install 'mycel-agent-sdk[voice]'`
- Redis sessions: `pip install 'mycel-agent-sdk[redis]'`
- Any-LLM: `pip install 'mycel-agent-sdk[any-llm]'`

### uv

```bash
uv init
uv add mycel-agent-sdk
```

---

## Minimal example

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

Set **`OPENAI_API_KEY`** (or point `base_url` at your **gateway**) before running.

**Notebook:**
[`examples/basic/hello_world_jupyter.ipynb`](examples/basic/hello_world_jupyter.ipynb)

---

## Monorepo layout (this repo)

| Path | Role |
| --- | --- |
| [`src/agents/`](src/agents/) | Python SDK (`import agents`) |
| [`gateway/`](gateway/) | Rust OpenAI Chat Completions–shaped gateway (JSON + SSE); **not** bundled in the wheel |
| [`docker/`](docker/), [`docker-compose.yml`](docker-compose.yml) | Optional container recipes |
| [`rust/mycel_accelerator/`](rust/mycel_accelerator/) | Optional PyO3 accelerator stub |
| [`docs/`](docs/) | MkDocs source; **live site:** **https://mycelai.github.io/mycel-agent-sdk/** |

Gateway client pattern: [`examples/model_providers/gateway_chatcompletions.py`](examples/model_providers/gateway_chatcompletions.py).

---

## Development & contributing

Clone the repository, run **`make sync`**, then follow **[`AGENTS.md`](AGENTS.md)**
(format, lint, typecheck, tests). External contributors work in **feature
branches** and open PRs — see **[`CONTRIBUTING.md`](CONTRIBUTING.md)** (direct
pushes to `main` are restricted to maintainers).

---

## Governance, legal, and policies

| Resource | Description |
| --- | --- |
| [**LICENSE**](LICENSE) | MIT License |
| [**NOTICE**](NOTICE) | Third-party and upstream attribution |
| [**CHANGELOG.md**](CHANGELOG.md) | **Keep a Changelog** + SemVer history |
| [**CONTRIBUTING.md**](CONTRIBUTING.md) | Branch / PR workflow and expectations |
| [**CODE_OF_CONDUCT.md**](CODE_OF_CONDUCT.md) | **Contributor Covenant 3.0** |
| [**AGENTS.md**](AGENTS.md) | Maintainer and contributor operations guide |
| [**PLANS.md**](PLANS.md) | ExecPlan discipline for substantial work |
| [**ExecPlan (fork vision)**](docs/execplans/mycel-fork-gateway-and-rust-tiers.md) | Gateway, builtins, Rust tiers — living spec |
| [**Pull request template**](.github/PULL_REQUEST_TEMPLATE/pull_request_template.md) | Use when opening PRs here |

**Security:** there is no `SECURITY.md` yet; report sensitive issues privately via
**[info@mycel-ai.de](mailto:info@mycel-ai.de)** (see **CONTRIBUTING**).

---

## Acknowledgements

Built on **[OpenAI Agents SDK for Python](https://github.com/openai/openai-agents-python)**.
We also depend on **Pydantic**, **MCP**, **Griffe**, **uv**, **ruff**, **pytest**,
**MkDocs Material**, and optional stacks such as **websockets**, **SQLAlchemy**,
and **any-llm**. Full attribution: **[NOTICE](NOTICE)**.

---

<!-- Footer -->
<div align="center">

<br>

<img src="https://raw.githubusercontent.com/MycelAI/.github/main/profile/logo-dark.png"
     alt="Mycel"
     width="160">

<br><br>

<sub>*Like mycelia networks that connect forests underground, we build systems that link what matters.*<br>
<strong>Silently. Reliably. At scale.</strong></sub>

<br>

[![Website](https://img.shields.io/badge/Website-mycel--ai.de-0d9488?style=for-the-badge&logo=link)](https://mycel-ai.de/en)
[![Contact](https://img.shields.io/badge/Contact-info%40mycel--ai.de-0d9488?style=for-the-badge&logo=minutemailer)](mailto:info@mycel-ai.de)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mycel%20AI-0d9488?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/company/mycel-ai)
[![Docs](https://img.shields.io/badge/Docs-GitHub%20Pages-0d9488?style=for-the-badge&logo=readthedocs)](https://mycelai.github.io/mycel-agent-sdk/)
[![PyPI](https://img.shields.io/badge/PyPI-mycel--agent--sdk-0d9488?style=for-the-badge&logo=pypi)](https://pypi.org/project/mycel-agent-sdk/)

<br>

**Mycel UG (haftungsbeschränkt)** · Kollwitzstraße 76, 10435 Berlin, Germany  
Amtsgericht Charlottenburg · HRB 278808 B · VAT ID DE458879972

<br>

[**mycel-ai.de**](https://mycel-ai.de/en) ·
[**About**](https://mycel-ai.de/en/about) ·
[**Contact**](https://mycel-ai.de/en/contact) ·
[**Imprint**](https://mycel-ai.de/en/imprint) ·
[**Privacy**](https://mycel-ai.de/en/privacy) ·
[**GitHub Org**](https://github.com/MycelAI)

<br>

**[MIT License](LICENSE)** · **[NOTICE](NOTICE)** · **[CHANGELOG](CHANGELOG.md)**

<br>

<sub>© Mycel UG (haftungsbeschränkt). Open source under MIT; see NOTICE for upstream and third-party attribution.</sub>

</div>
