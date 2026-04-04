"""Provider-agnostic message shapes (foundation for decoupling from OpenAI wire types)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CanonicalRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class CanonicalContentPart:
    """A single segment of multimodal or structured content."""

    type: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class CanonicalMessage:
    """One turn in a conversation, without OpenAI-specific field names."""

    role: CanonicalRole
    parts: list[CanonicalContentPart] = field(default_factory=list)
    tool_call_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
