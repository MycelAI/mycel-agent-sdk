"""Local shell execution as a ``@function_tool`` (use ``ShellTool`` for sandboxed runs)."""

from __future__ import annotations

import os
import subprocess

from ...tool import function_tool


@function_tool
def bash(command: str, timeout: int = 30) -> str:
    """Run a shell command in the current working directory; returns stdout/stderr (truncated)."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd(),
            env={**os.environ, "TERM": "dumb"},
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += f"\n[stderr]\n{result.stderr}"
        if result.returncode != 0:
            output += f"\n[exit code: {result.returncode}]"
        if len(output) > 15000:
            output = output[:7000] + "\n\n... [truncated] ...\n\n" + output[-7000:]
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return f"ERROR: Command timed out after {timeout}s"
    except Exception as e:
        return f"ERROR: {e!s}"
