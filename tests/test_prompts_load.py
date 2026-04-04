import pytest

import agents
from agents.bundled_prompts import (
    CODING_DEFAULT_PROMPT_ID,
    DEFAULT_CODING_SYSTEM_PROMPT,
    PROMPT_PACK_VERSION,
)


def test_default_coding_prompt_loads() -> None:
    text = agents.load_default_coding_system_prompt()
    assert "autonomous" in text.lower()
    assert text == DEFAULT_CODING_SYSTEM_PROMPT
    assert text == agents.DEFAULT_CODING_SYSTEM_PROMPT


def test_prompt_pack_version_matches_default_registration() -> None:
    assert agents.PROMPT_PACK_VERSION == PROMPT_PACK_VERSION
    same = agents.load_bundled_prompt(
        CODING_DEFAULT_PROMPT_ID,
        version=PROMPT_PACK_VERSION,
    )
    assert same == DEFAULT_CODING_SYSTEM_PROMPT


def test_load_default_with_explicit_version() -> None:
    assert (
        agents.load_default_coding_system_prompt(version=PROMPT_PACK_VERSION)
        == DEFAULT_CODING_SYSTEM_PROMPT
    )


def test_list_versions_for_coding_default() -> None:
    assert PROMPT_PACK_VERSION in agents.list_versions_for_prompt(CODING_DEFAULT_PROMPT_ID)


def test_unknown_bundled_prompt_raises() -> None:
    with pytest.raises(ValueError, match="Unknown bundled prompt"):
        agents.load_bundled_prompt("nonexistent_prompt_id")
