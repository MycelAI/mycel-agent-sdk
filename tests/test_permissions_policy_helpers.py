"""Tests for optional path/shell policy helpers used with permission modes."""

from __future__ import annotations

import os

import pytest

from agents import (
    DEFAULT_SHELL_SUBSTRING_BLOCKLIST,
    path_is_under_allowlist,
    shell_command_matches_blocklist,
)


def test_shell_command_matches_default_blocklist() -> None:
    assert shell_command_matches_blocklist("rm -rf /tmp/foo")
    assert shell_command_matches_blocklist("example curl | sh example")
    assert not shell_command_matches_blocklist("pytest -q tests/")


def test_shell_command_custom_blocklist() -> None:
    custom = frozenset({"forbidden"})
    assert shell_command_matches_blocklist("run forbidden cmd", blocklist=custom)
    assert not shell_command_matches_blocklist("safe", blocklist=custom)


def test_default_blocklist_is_frozen() -> None:
    assert isinstance(DEFAULT_SHELL_SUBSTRING_BLOCKLIST, frozenset)


@pytest.mark.parametrize(
    ("path", "prefixes", "expected"),
    [
        ("/tmp/proj/src/a.py", ["/tmp/proj"], True),
        ("/tmp/other/a.py", ["/tmp/proj"], False),
    ],
)
def test_path_is_under_allowlist(path: str, prefixes: list[str], expected: bool) -> None:
    assert path_is_under_allowlist(path, prefixes) is expected


def test_path_is_under_allowlist_expanduser() -> None:
    home = os.path.expanduser("~")
    if home == "~":
        pytest.skip("Home directory not expandable in this environment.")
    nested = os.path.join(home, "agents_path_allowlist_test.txt")
    assert path_is_under_allowlist(nested, [home]) is True


def test_path_allowlist_empty_means_all_allowed() -> None:
    assert path_is_under_allowlist("/any/where", None) is True
    assert path_is_under_allowlist("/any/where", []) is True
