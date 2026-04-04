"""Unified permission modes for built-in and function tools."""

from __future__ import annotations

import dataclasses
import os
from collections.abc import Sequence
from enum import Enum

from .tool import FunctionTool, Tool

# Substrings often treated as dangerous in autonomous shell tools (substring match).
DEFAULT_SHELL_SUBSTRING_BLOCKLIST: frozenset[str] = frozenset(
    (
        "rm -rf /",
        "rm -rf /*",
        "mkfs",
        "dd if=",
        "> /dev/",
        "curl | sh",
        "wget | sh",
        "chmod 777",
    )
)


class PermissionMode(str, Enum):
    """High-level policy presets for autonomous agents.

    Use :attr:`~agents.run_config.RunConfig.permission_mode` to apply these defaults on each
    turn, or call :func:`apply_permission_mode_to_tools` yourself. For path and shell policies,
    combine with :func:`path_is_under_allowlist` and :func:`shell_command_matches_blocklist`
    inside custom ``needs_approval`` callables or guardrails.
    """

    FULL = "full"
    ACCEPT_EDITS = "accept_edits"
    READ_ONLY = "read_only"
    ASK = "ask"


_READ_TOOLS = frozenset(
    {
        "read_file",
        "glob_search",
        "list_directory",
        "web_search",
        "web_fetch",
    }
)
_WRITE_TOOLS = frozenset({"write_file", "edit_file", "multi_edit"})
_SHELL_TOOLS = frozenset({"bash"})


def default_needs_approval_for_tool(tool_name: str, mode: PermissionMode) -> bool:
    """Return whether a tool should require human approval by default for ``mode``."""
    if mode is PermissionMode.FULL:
        return False
    if mode is PermissionMode.ASK:
        return True
    if mode is PermissionMode.READ_ONLY:
        return tool_name not in _READ_TOOLS
    # ACCEPT_EDITS: auto-approve file mutations; ask for shell.
    if tool_name in _SHELL_TOOLS:
        return True
    if tool_name in _WRITE_TOOLS:
        return False
    if tool_name in _READ_TOOLS:
        return False
    return True


def apply_permission_mode_to_tools(tools: list[Tool], mode: PermissionMode) -> list[Tool]:
    """Return a new tool list with ``needs_approval`` set on each ``FunctionTool``."""
    out: list[Tool] = []
    for t in tools:
        if isinstance(t, FunctionTool):
            out.append(
                dataclasses.replace(
                    t,
                    needs_approval=default_needs_approval_for_tool(t.name, mode),
                )
            )
        else:
            out.append(t)
    return out


def shell_command_matches_blocklist(
    command: str,
    *,
    blocklist: frozenset[str] | None = None,
) -> bool:
    """Return True if ``command`` contains any substring from ``blocklist``."""
    fragments = DEFAULT_SHELL_SUBSTRING_BLOCKLIST if blocklist is None else blocklist
    return any(fragment in command for fragment in fragments)


def path_is_under_allowlist(path: str, allow_prefixes: Sequence[str] | None) -> bool:
    """Return True when ``path`` sits under one of ``allow_prefixes`` (or the list is empty).

    Prefixes and ``path`` are compared after ``abspath`` + ``expanduser`` normalization.
    When ``allow_prefixes`` is ``None`` or empty, every path is allowed.
    """
    if not allow_prefixes:
        return True
    target = os.path.normpath(os.path.abspath(os.path.expanduser(path)))
    sep = os.sep
    for prefix in allow_prefixes:
        root = os.path.normpath(os.path.abspath(os.path.expanduser(prefix)))
        if target == root or target.startswith(root + sep):
            return True
    return False


__all__ = [
    "DEFAULT_SHELL_SUBSTRING_BLOCKLIST",
    "PermissionMode",
    "apply_permission_mode_to_tools",
    "default_needs_approval_for_tool",
    "path_is_under_allowlist",
    "shell_command_matches_blocklist",
]
