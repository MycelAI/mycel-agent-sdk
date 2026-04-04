from unittest.mock import MagicMock

import pytest

from agents import (
    CODING_TOOLKIT,
    FILE_TOOLS,
    SAFE_TOOLKIT,
    SHELL_TOOLS,
    WEB_TOOLS,
    PermissionMode,
    apply_permission_mode_to_tools,
)
from agents.run_context import RunContextWrapper
from agents.run_internal.turn_preparation import get_all_tools
from agents.tool import FunctionTool


def test_builtin_presets_non_empty() -> None:
    assert len(FILE_TOOLS) >= 1
    assert len(SHELL_TOOLS) == 1
    assert len(WEB_TOOLS) == 2
    assert len(CODING_TOOLKIT) == len(FILE_TOOLS) + len(SHELL_TOOLS)
    assert len(SAFE_TOOLKIT) == len(FILE_TOOLS) + len(WEB_TOOLS)


def test_apply_permission_mode_sets_needs_approval() -> None:
    adjusted = apply_permission_mode_to_tools(list(FILE_TOOLS), PermissionMode.ASK)
    assert all(getattr(t, "needs_approval", None) is True for t in adjusted)


@pytest.mark.asyncio
async def test_get_all_tools_applies_permission_mode_kwarg() -> None:
    agent = MagicMock()

    async def _tools(_ctx: RunContextWrapper[None]) -> list[FunctionTool]:
        return list(FILE_TOOLS)

    agent.get_all_tools = _tools
    ctx = RunContextWrapper(context=None)
    out = await get_all_tools(agent, ctx, permission_mode=PermissionMode.READ_ONLY)
    fn_tools = [t for t in out if isinstance(t, FunctionTool)]
    by_name = {t.name: t for t in fn_tools}
    assert by_name["read_file"].needs_approval is False
    assert by_name["write_file"].needs_approval is True
