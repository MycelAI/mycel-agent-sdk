from __future__ import annotations

import json
from pathlib import Path

import pytest

from agents import Agent, RunConfig
from agents.tool import invoke_function_tool
from agents.tool_context import ToolContext
from agents.tools.builtin import glob_search, read_file, write_file
from agents.usage import Usage


def _minimal_tool_context() -> ToolContext[None]:
    return ToolContext(
        context=None,
        usage=Usage(),
        tool_name="test",
        tool_call_id="call-1",
        tool_arguments="{}",
        agent=Agent(name="agent", instructions=""),
        run_config=RunConfig(model="gpt-4o-mini"),
    )


@pytest.mark.asyncio
async def test_write_read_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "sample.txt"
    ctx = _minimal_tool_context()
    await invoke_function_tool(
        function_tool=write_file,
        context=ctx,
        arguments=json.dumps({"path": str(p), "content": "hello"}),
    )
    text = await invoke_function_tool(
        function_tool=read_file,
        context=ctx,
        arguments=json.dumps({"path": str(p)}),
    )
    assert "hello" in str(text)


@pytest.mark.asyncio
async def test_glob_search_finds_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "a.py").write_text("x", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    ctx = _minimal_tool_context()
    result = await invoke_function_tool(
        function_tool=glob_search,
        context=ctx,
        arguments=json.dumps({"pattern": "*.py", "directory": "."}),
    )
    assert "a.py" in str(result)
