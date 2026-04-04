# Mycel agent SDK fork: gateway, builtins, and optional Rust tiers

This ExecPlan is a living document. The sections Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective must stay up to date as work proceeds.

If [PLANS.md](../../PLANS.md) is present in the repo, maintain this document in accordance with it and link back to it by path.

## Purpose / Big Picture

Deliver a fork-ready path where:

- Multi-provider LLM access goes through a **Rust gateway** exposing **OpenAI Chat Completions + SSE**, consumed by [`OpenAIChatCompletionsModel`](../../src/agents/models/openai_chatcompletions.py) and `AsyncOpenAI(base_url=..., api_key=...)`.
- **LiteLLM is removed** from the distribution; routing and provider keys live in the gateway.
- **Built-in coding/research tools** and a **unified permission mode** ship as first-class SDK surfaces.
- Optional **canonical wire types** and **Rust accelerators** can land incrementally without blocking the gateway migration.

After implementation, users can point `base_url` at the gateway and use builtin tool presets with `PermissionMode`.

## Progress

- [x] (2026-04-04) Authored in-repo ExecPlan; added gateway documentation; removed LiteLLM integration; added canonical wire foundation; builtins + permissions; prompts + eval harness; Rust accelerator stub; run-loop helper extraction.
- [x] (2026-04-04) Permission policy helpers (`path_is_under_allowlist`, `shell_command_matches_blocklist`) and `examples/evals` pointer.
- [x] (2026-04-04) In-monorepo Rust gateway under `gateway/`: JSON + SSE Chat Completions stub, `cargo test` contract coverage; CI build; not bundled in the Python wheel.
- [x] (2026-04-04) Versioned bundled prompts (`PROMPT_PACK_VERSION`, `load_bundled_prompt`, `list_versions_for_prompt`) + eval harness via `RunResult.new_items`.
- [ ] **(Product / infra)** Production gateway image/binary published, configured with real providers, and load-tested.

## Surprises & Discoveries

- Observation: `MultiProvider` previously treated `litellm/` as a built-in prefix; removal surfaces `UserError` unless `unknown_prefix_mode="model_id"` is used for OpenAI-compatible IDs.
  Evidence: [`multi_provider.py`](../../src/agents/models/multi_provider.py).

## Decision Log

- Decision: Remove LiteLLM optional extra and all `LitellmModel` / `LitellmProvider` code from the fork.
  Rationale: Supply-chain and routing centralized in the Rust gateway; no duplicate provider client in Python.
  Date/Author: 2026-04-04 / Mycel fork implementation.

- Decision: Keep `InternalChatCompletionMessage` / `InternalToolCall` as OpenAI-schema subclasses under `agents.models.internal_chat_completion` for converter and tests (no LiteLLM import).
  Rationale: Preserves reasoning/thinking test coverage without the LiteLLM package.
  Date/Author: 2026-04-04 / Mycel fork implementation.

## Outcomes & Retrospective

Gateway integration is documented under [Gateway model provider](../gateway_model_provider.md); source stub lives in [`gateway/`](../../gateway/). Builtin tools live in [`agents.tools.builtin`](../../src/agents/tools/builtin/). Further work: streaming + routing in the gateway, expand eval cases, flesh out PyO3 accelerator.

## Context and Orientation

- **Repository root:** `mycel-agent-sdk` (OpenAI Agents Python lineage).
- **Key modules:** `src/agents/models/openai_chatcompletions.py`, `src/agents/run_internal/run_loop.py`, `src/agents/tools/builtin/`, `src/agents/permissions.py`, `rust/mycel_accelerator/`.
- **Validation:** from repo root, run `make format`, `make lint`, `make typecheck`, `make tests` per [AGENTS.md](../../AGENTS.md).

## Plan of Work

See milestone sections in the strategy draft (M0–M7): gateway + LiteLLM removal, canonical types foundation, builtins + permissions, prompts/evals, optional Rust, run-loop modularization.

## Concrete Steps

    cd /path/to/mycel-agent-sdk
    make sync
    make format && make lint && make typecheck && make tests

## Validation and Acceptance

- Full test suite passes.
- `cargo test --manifest-path gateway/Cargo.toml` passes (Chat Completions JSON + SSE contract).
- `uv run pytest tests/test_gateway_model_example.py` passes (gateway client pattern).
- `uv run pytest tests/evals/test_eval_harness.py` and `tests/test_prompts_load.py` pass.

## Idempotence and Recovery

Re-run `make tests` after rebasing; restore deleted LiteLLM files from upstream only if intentionally reverting the fork policy.

## Artifacts and Notes

- English docs only for manual edits; translated docs under `docs/ja`, `docs/ko`, `docs/zh` are generated per AGENTS.md.

## Interfaces and Dependencies

- `agents.tools.builtin`: preset tool lists `FILE_TOOLS`, `SHELL_TOOLS`, `WEB_TOOLS`, `CODING_TOOLKIT`, etc.
- `agents.permissions`: `PermissionMode`, `default_needs_approval_for_tool`, `apply_permission_mode_to_tools`, `DEFAULT_SHELL_SUBSTRING_BLOCKLIST`, `shell_command_matches_blocklist`, `path_is_under_allowlist`.
- `agents.run_config.RunConfig.permission_mode`: optional per-run application of `apply_permission_mode_to_tools` during tool resolution.
- `agents.wire`: neutral DTOs (`CanonicalMessage`, etc.) for future boundary translation.
- `mycel_accelerator` (optional): PyO3 module `mycel_accelerator` with `echo_u64` stub.
