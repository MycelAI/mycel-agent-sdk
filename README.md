# Mycel Agent SDK [PyPI](https://pypi.org/project/mycel-agent-sdk/)

The Mycel Agent SDK is a lightweight yet powerful framework for building multi-agent workflows. It is provider-agnostic, supporting the OpenAI Responses and Chat Completions APIs, as well as 100+ other LLMs. Python code still uses `import agents`; this distribution is published on PyPI as `mycel-agent-sdk`.

The companion **mycel-gateway** Rust service (OpenAI Chat Completions–compatible HTTP API) lives in `gateway/` in this monorepo. See [gateway/README.md](gateway/README.md) and [docker/README.md](docker/README.md).

> [!NOTE]
> Looking for the JavaScript/TypeScript version? Check out [Agents SDK JS/TS](https://github.com/openai/openai-agents-js).

### Core concepts:

1. **[Agents](https://mycelai.github.io/mycel-agent-sdk/agents)**: LLMs configured with instructions, tools, guardrails, and handoffs
2. **[Agents as tools](https://mycelai.github.io/mycel-agent-sdk/tools/#agents-as-tools) / [Handoffs](https://mycelai.github.io/mycel-agent-sdk/handoffs/)**: Delegating to other agents for specific tasks
3. **[Tools](https://mycelai.github.io/mycel-agent-sdk/tools/)**: Various Tools let agents take actions (functions, MCP, hosted tools)
4. **[Guardrails](https://mycelai.github.io/mycel-agent-sdk/guardrails/)**: Configurable safety checks for input and output validation
5. **[Human in the loop](https://mycelai.github.io/mycel-agent-sdk/human_in_the_loop/)**: Built-in mechanisms for involving humans across agent runs
6. **[Sessions](https://mycelai.github.io/mycel-agent-sdk/sessions/)**: Automatic conversation history management across agent runs
7. **[Tracing](https://mycelai.github.io/mycel-agent-sdk/tracing/)**: Built-in tracking of agent runs, allowing you to view, debug and optimize your workflows
8. **[Realtime Agents](https://mycelai.github.io/mycel-agent-sdk/realtime/quickstart/)**: Build powerful voice agents with `gpt-realtime-1.5` and full agent features

Explore the [examples](https://github.com/MycelAI/mycel-agent-sdk/tree/main/examples) directory to see the SDK in action, and read our [documentation](https://mycelai.github.io/mycel-agent-sdk/) for more details.

## Get started

To get started, set up your Python environment (Python 3.10 or newer required), and then install the Mycel Agent SDK package.

### venv

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install mycel-agent-sdk
```

For voice support, install with the optional `voice` group: `pip install 'mycel-agent-sdk[voice]'`. For Redis session support, install with the optional `redis` group: `pip install 'mycel-agent-sdk[redis]'`.

### uv

If you're familiar with [uv](https://docs.astral.sh/uv/), installing the package would be even easier:

```bash
uv init
uv add mycel-agent-sdk
```

For voice support, install with the optional `voice` group: `uv add 'mycel-agent-sdk[voice]'`. For Redis session support, install with the optional `redis` group: `uv add 'mycel-agent-sdk[redis]'`.

## Run your first agent

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
```

(*If running this, ensure you set the `OPENAI_API_KEY` environment variable*)

(*For Jupyter notebook users, see [hello_world_jupyter.ipynb](https://github.com/MycelAI/mycel-agent-sdk/blob/main/examples/basic/hello_world_jupyter.ipynb)*)

Explore the [examples](https://github.com/MycelAI/mycel-agent-sdk/tree/main/examples) directory to see the SDK in action, and read our [documentation](https://mycelai.github.io/mycel-agent-sdk/) for more details.

## Acknowledgements

This project builds on the [OpenAI Agents SDK for Python](https://github.com/openai/openai-agents-python). We'd like to acknowledge the excellent work of the open-source community, especially:

- [Pydantic](https://docs.pydantic.dev/latest/)
- [Requests](https://github.com/psf/requests)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Griffe](https://github.com/mkdocstrings/griffe)

This library has these optional dependencies:

- [websockets](https://github.com/python-websockets/websockets)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [any-llm](https://github.com/mozilla-ai/any-llm)

We also rely on the following tools to manage the project:

- [uv](https://github.com/astral-sh/uv) and [ruff](https://github.com/astral-sh/ruff)
- [mypy](https://github.com/python/mypy) and [Pyright](https://github.com/microsoft/pyright)
- [pytest](https://github.com/pytest-dev/pytest) and [Coverage.py](https://github.com/coveragepy/coveragepy)
- [MkDocs](https://github.com/squidfunk/mkdocs-material)

We're committed to continuing to develop the Mycel Agent SDK as an open source framework so others in the community can expand on our approach.

## Publisher / legal

The SDK is published by **Mycel UG (haftungsbeschränkt)**, Kollwitzstraße 76, 10435 Berlin, Germany (Amtsgericht Charlottenburg, HRB 278808 B; VAT ID DE458879972). Contact: [info@mycel-ai.de](mailto:info@mycel-ai.de). The statutory [imprint / Impressum](https://mycel-ai.de/en/imprint) is available on [mycel-ai.de](https://mycel-ai.de/en).

Licensing: this project is under the [MIT License](LICENSE). Upstream and third-party attribution is summarized in [NOTICE](NOTICE).
