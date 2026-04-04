# Changelog

All notable changes to **mycel-agent-sdk** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **`CHANGELOG.md`** (Keep a Changelog) and **SemVer / changelog policy** in
  **`AGENTS.md`**.
- **`CONTRIBUTING.md`**, **`CODE_OF_CONDUCT.md`**, and a refreshed **`README.md`**
  (after the `v0.14.0` tag).

### Changed

- **`CODE_OF_CONDUCT.md`** follows **Contributor Covenant 3.0**.

## [0.14.0] - 2026-04-04

First tracked release of **mycel-agent-sdk** as the Mycel-maintained Python
agents package (package name on PyPI: `mycel-agent-sdk`). Versioning continues
with SemVer from this baseline.

### Added

- Optional **OpenAI Chat Completions–compatible** Rust **gateway** (`gateway/`)
  and Docker layout (`docker/`, `docker-compose.yml`).
- **Bundled prompts**, **permissions** helpers, **wire** canonical types, and
  **builtin** tool modules under `src/agents/tools/builtin/`.
- **`docs/gateway_model_provider.md`** (and localized stubs), **evals** examples
  and tests, and **`docs/scripts/sync_i18n_heading_ids.py`** with Makefile
  targets `sync-i18n-heading-ids` and `build-docs-all`.
- **`README.md`** and branded documentation entry points for the fork.
- CI/workflow and test coverage updates for the fork.

### Changed

- **Models / providers:** documentation and examples emphasize gateway and
  **Any-LLM** paths; `MultiProvider` / **AnyLLM** integration adjustments.
- **Runtime:** run loop, tool execution, turn preparation/resolution, and related
  wiring refactored or extended without diverging stream vs non-stream behavior.
- **Branding & docs:** Mycel naming, corrected docs homepage URLs, refreshed
  English and locale docs (including heading anchor alignment where applied).
- **Examples & dependencies:** Twilio and hosted MCP examples updated; **`uv.lock`**
  and optional extras revised for the new dependency set.

### Removed

- Built-in **LiteLLM** extension modules (`litellm_model`, `litellm_provider`),
  related examples, tests, and reference stubs.
- Redundant locale **`docs/{ja,ko,zh}/sessions.md`** stubs in favor of
  **`sessions/index.md`**.

### Fixed

- i18n heading alignment and doc link consistency for the new documentation
  layout (ongoing practice via `sync_i18n_heading_ids` / `build-docs-all`).

[Unreleased]: https://github.com/MycelAI/mycel-agent-sdk/compare/v0.14.0...HEAD
[0.14.0]: https://github.com/MycelAI/mycel-agent-sdk/releases/tag/v0.14.0
