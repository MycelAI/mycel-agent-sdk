"""Minimal eval harness patterns using ``RunResult.new_items``."""

from __future__ import annotations

from typing import Any, cast

from agents import PROMPT_PACK_VERSION, RunResult, load_bundled_prompt
from agents.bundled_prompts import CODING_DEFAULT_PROMPT_ID
from agents.items import ToolCallItem


def _tool_names_from_result(result: RunResult) -> list[str]:
    names: list[str] = []
    for item in result.new_items:
        if isinstance(item, ToolCallItem):
            raw = cast(Any, item.raw_item)
            name = getattr(raw, "name", None)
            if name is not None:
                names.append(str(name))
    return names


def test_eval_harness_extracts_tool_names_from_new_items() -> None:
    """Document the supported way to inspect tool usage (not ``result.tool_calls``)."""

    class _FakeResult:
        new_items: list[Any] = []

    names = _tool_names_from_result(cast(RunResult, _FakeResult()))
    assert names == []


def test_eval_harness_can_pin_prompt_pack_version() -> None:
    """Evals should load prompts by id + version for reproducible runs."""
    text = load_bundled_prompt(CODING_DEFAULT_PROMPT_ID, version=PROMPT_PACK_VERSION)
    assert "autonomous" in text.lower()
