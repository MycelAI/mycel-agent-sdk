"""Built-in coding and research tools (``@function_tool`` wrappers)."""

from __future__ import annotations

from .file_tools import (
    edit_file,
    glob_search,
    list_directory,
    multi_edit,
    read_file,
    write_file,
)
from .shell_tools import bash
from .web_tools import web_fetch, web_search

FILE_TOOLS = [read_file, write_file, edit_file, multi_edit, glob_search, list_directory]
SHELL_TOOLS = [bash]
WEB_TOOLS = [web_search, web_fetch]

CODING_TOOLKIT = [*FILE_TOOLS, *SHELL_TOOLS]
RESEARCH_TOOLKIT = [*WEB_TOOLS, *FILE_TOOLS]
SAFE_TOOLKIT = [*FILE_TOOLS, *WEB_TOOLS]

__all__ = [
    "CODING_TOOLKIT",
    "FILE_TOOLS",
    "RESEARCH_TOOLKIT",
    "SAFE_TOOLKIT",
    "SHELL_TOOLS",
    "WEB_TOOLS",
    "bash",
    "edit_file",
    "glob_search",
    "list_directory",
    "multi_edit",
    "read_file",
    "web_fetch",
    "web_search",
    "write_file",
]
