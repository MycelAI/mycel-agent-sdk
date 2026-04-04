<div align="center">

# Mycel Agent SDK

**Multi-agent workflows for Python — OpenAI Responses & Chat Completions, gateways, and pluggable providers.**

[![PyPI version](https://img.shields.io/pypi/v/mycel-agent-sdk.svg)](https://pypi.org/project/mycel-agent-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/mycel-agent-sdk.svg)](https://pypi.org/project/mycel-agent-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-0366d6.svg)](https://mycelai.github.io/mycel-agent-sdk/)
[![Mycel](https://img.shields.io/badge/Mycel-mycel--ai.de-5c4ee5.svg)](https://mycel-ai.de/en)

[Documentation](https://mycelai.github.io/mycel-agent-sdk/) ·
[Examples](https://github.com/MycelAI/mycel-agent-sdk/tree/main/examples) ·
[Contributing](CONTRIBUTING.md) ·
[Code of conduct](CODE_OF_CONDUCT.md)

</div>

---

The **Mycel Agent SDK** is a focused framework for building **multi-agent**
workflows in Python. Your code still uses `import agents`; this package ships on
**[PyPI](https://pypi.org/project/mycel-agent-sdk/)** as **`mycel-agent-sdk`**.

A companion **Rust gateway** (`gateway/`) exposes an **OpenAI Chat
Completions–compatible** HTTP API for routing models. See
[`gateway/README.md`](gateway/README.md) and [`docker/README.md`](docker/README.md).

> [!NOTE]
> Prefer the **JS/TS** stack? See
> [Agents SDK JS/TS](https://github.com/openai/openai-agents-js).

## Highlights

| | |
| --- | --- |
| **Agents** | Instructions, tools, guardrails, handoffs — [docs](https://mycelai.github.io/mycel-agent-sdk/agents) |
| **Tools & MCP** | Function tools, MCP, hosted tools — [docs](https://mycelai.github.io/mycel-agent-sdk/tools/) |
| **Sessions** | Conversation history across runs — [docs](https://mycelai.github.io/mycel-agent-sdk/sessions/) |
| **Tracing** | Debug and optimize runs — [docs](https://mycelai.github.io/mycel-agent-sdk/tracing/) |
| **Realtime** | Voice agents with Realtime models — [quickstart](https://mycelai.github.io/mycel-agent-sdk/realtime/quickstart/) |
| **Providers** | OpenAI, gateways, **Any-LLM** (optional extra), custom providers — [models](https://mycelai.github.io/mycel-agent-sdk/models/) |

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

## Minimal example

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

Set **`OPENAI_API_KEY`** (or configure your provider / gateway) before running.

**Notebook:** [`hello_world_jupyter.ipynb`](https://github.com/MycelAI/mycel-agent-sdk/blob/main/examples/basic/hello_world_jupyter.ipynb)

## Development

Clone the repo, install dev deps (see **[AGENTS.md](AGENTS.md)**), then use
`make sync`, `make tests`, etc. **Contributions** must follow
**[CONTRIBUTING.md](CONTRIBUTING.md)** (feature branches + PRs; `main` is
maintainer-controlled).

## Acknowledgements

Built on ideas and code from the **[OpenAI Agents SDK for Python](https://github.com/openai/openai-agents-python)**.
We also depend on great tools and libraries — notably **Pydantic**, **MCP**,
**Griffe**, **uv**, **ruff**, **pytest**, **MkDocs Material**, and optional stacks
such as **websockets**, **SQLAlchemy**, and **any-llm**. See **[NOTICE](NOTICE)**
for attribution detail.

## Publisher / legal

Published by **Mycel UG (haftungsbeschränkt)**, Kollwitzstraße 76, 10435 Berlin,
Germany (Amtsgericht Charlottenburg, HRB 278808 B; VAT ID DE458879972).
Contact: **[info@mycel-ai.de](mailto:info@mycel-ai.de)**.
**[Imprint](https://mycel-ai.de/en/imprint)** · **[mycel-ai.de](https://mycel-ai.de/en)**

Licensed under the **[MIT License](LICENSE)**.
