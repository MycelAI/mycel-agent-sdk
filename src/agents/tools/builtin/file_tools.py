"""File-oriented ``@function_tool`` helpers for coding agents."""

from __future__ import annotations

import glob as glob_mod
import os
from pathlib import Path

from typing_extensions import NotRequired, TypedDict

from ...tool import function_tool


class _MultiEditEntry(TypedDict):
    """One search-and-replace step for :func:`multi_edit`."""

    old_str: str
    new_str: NotRequired[str]


@function_tool
def read_file(path: str, start_line: int = 1, end_line: int = -1) -> str:
    """Read a UTF-8 text file.

    ``start_line`` / ``end_line`` are 1-based; ``end_line=-1`` reads through EOF.
    """
    p = Path(path).expanduser()
    text = p.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)
    if end_line == -1:
        end_line = len(lines)
    start = max(0, start_line - 1)
    end = min(len(lines), end_line)
    selected = lines[start:end]
    numbered = [f"{i + start + 1:4d} | {line.rstrip()}" for i, line in enumerate(selected)]
    return "\n".join(numbered) if numbered else "(empty selection)"


@function_tool
def write_file(path: str, content: str) -> str:
    """Create or overwrite a file. Creates parent directories as needed."""
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} characters to {p}"


@function_tool
def edit_file(path: str, old_str: str, new_str: str) -> str:
    """Replace exactly one occurrence of ``old_str`` with ``new_str``."""
    p = Path(path).expanduser()
    content = p.read_text(encoding="utf-8")
    count = content.count(old_str)
    if count == 0:
        return f"ERROR: old_str not found in {p}"
    if count > 1:
        return f"ERROR: old_str appears {count} times in {p}; must be unique."
    updated = content.replace(old_str, new_str, 1)
    p.write_text(updated, encoding="utf-8")
    return f"Edited {p}: replaced {len(old_str)} chars with {len(new_str)} chars"


@function_tool
def multi_edit(path: str, edits: list[_MultiEditEntry]) -> str:
    """Apply multiple ``old_str`` / ``new_str`` edits in order."""
    p = Path(path).expanduser()
    content = p.read_text(encoding="utf-8")
    results: list[str] = []
    for i, edit in enumerate(edits):
        old = edit["old_str"]
        new = edit.get("new_str", "")
        if content.count(old) != 1:
            results.append(f"Edit {i}: FAILED (not found or ambiguous)")
            continue
        content = content.replace(old, new, 1)
        results.append(f"Edit {i}: OK")
    p.write_text(content, encoding="utf-8")
    return f"Applied edits to {p}:\n" + "\n".join(results)


@function_tool
def glob_search(pattern: str, directory: str = ".") -> str:
    """Recursive glob from ``directory`` (e.g. ``'**/*.py'``). Caps at 200 paths."""
    base = Path(directory).expanduser()
    matches = sorted(
        glob_mod.glob(str(base / pattern), recursive=True),
    )[:200]
    if not matches:
        return f"No files match {pattern!r} in {directory!r}"
    return "\n".join(matches)


@function_tool
def list_directory(path: str = ".", max_depth: int = 2) -> str:
    """Walk ``path`` up to ``max_depth`` and list files (capped)."""
    root = Path(path).expanduser()
    lines: list[str] = []
    base_depth = len(root.parts)

    for dirpath, dirnames, filenames in os.walk(root):
        depth = len(Path(dirpath).parts) - base_depth
        if depth >= max_depth:
            dirnames.clear()
            continue
        indent = "  " * depth
        name = Path(dirpath).name or str(dirpath)
        lines.append(f"{indent}{name}/")
        for fname in sorted(filenames)[:50]:
            lines.append(f"{indent}  {fname}")
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))

    return "\n".join(lines[:500]) if lines else "(empty)"
