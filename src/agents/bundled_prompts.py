"""Bundled system prompts (versioned registry for evals and reproducibility)."""

from __future__ import annotations

# Bump when prompt text changes in a way that affects evals or golden transcripts.
PROMPT_PACK_VERSION = "2026-04-04"

CODING_DEFAULT_PROMPT_ID = "coding_default"

_CODING_PROMPT_2026_04_04 = """You are an autonomous coding agent with tools for files, shell,
and (when configured) the web.

## Operating loop

Gather context, act, verify, and repeat. Prefer reading before editing.

## Tools

1. Read files before editing; never guess file contents.
2. Use `glob_search` / `list_directory` to locate relevant paths.
3. Prefer `edit_file` for small changes; use `write_file` for new files or full rewrites.
4. Inspect shell exit codes and stderr; diagnose failures before retrying.
5. If stuck after a few attempts, summarize what you tried.

## Style

Be concise. State what changed and why. Note assumptions when requirements are ambiguous.
"""

_BUNDLED_PROMPTS: dict[tuple[str, str], str] = {
    (CODING_DEFAULT_PROMPT_ID, "2026-04-04"): _CODING_PROMPT_2026_04_04,
}

DEFAULT_CODING_SYSTEM_PROMPT = _BUNDLED_PROMPTS[
    CODING_DEFAULT_PROMPT_ID,
    PROMPT_PACK_VERSION,
]


def load_bundled_prompt(prompt_id: str, *, version: str | None = None) -> str:
    """Return prompt body for ``prompt_id`` and ``version``.

    ``version`` defaults to :data:`PROMPT_PACK_VERSION`.
    """
    ver = PROMPT_PACK_VERSION if version is None else version
    key = (prompt_id, ver)
    try:
        return _BUNDLED_PROMPTS[key]
    except KeyError as e:
        known_ids = sorted({k[0] for k in _BUNDLED_PROMPTS})
        versions_for = sorted({v for (pid, v) in _BUNDLED_PROMPTS if pid == prompt_id})
        raise ValueError(
            f"Unknown bundled prompt {prompt_id!r} version {ver!r}. "
            f"Known ids: {known_ids}. Versions for {prompt_id!r}: {versions_for}"
        ) from e


def list_versions_for_prompt(prompt_id: str) -> tuple[str, ...]:
    """Return sorted version strings available for ``prompt_id``."""
    vers = sorted({v for (pid, v) in _BUNDLED_PROMPTS if pid == prompt_id})
    return tuple(vers)


def load_default_coding_system_prompt(*, version: str | None = None) -> str:
    """Return the default autonomous coding agent system prompt."""
    return load_bundled_prompt(CODING_DEFAULT_PROMPT_ID, version=version)
