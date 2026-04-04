# Evaluation patterns

Use **`RunResult.new_items`** (and types such as [`ToolCallItem`][agents.items.ToolCallItem]) to assert tool usage after a run. The SDK does not provide `result.tool_calls` or `result.messages`.

Reference implementation: [`tests/evals/test_eval_harness.py`](../../tests/evals/test_eval_harness.py).

Pin prompts in evals with `load_bundled_prompt(..., version=PROMPT_PACK_VERSION)` (see
[`agents.bundled_prompts`](../../src/agents/bundled_prompts.py)).

For filesystem assertions, run agents against a temporary working directory and check outputs on disk.
