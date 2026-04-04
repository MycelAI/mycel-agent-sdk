"""Small pure helpers shared by streaming and non-streaming run-loop paths."""

from __future__ import annotations

from ..exceptions import (
    InputGuardrailTripwireTriggered,
    ModelBehaviorError,
    OutputGuardrailTripwireTriggered,
)
from ..items import ItemHelpers, RunItem, TResponseInputItem
from ..run_config import ReasoningItemIdPolicy
from .items import prepare_model_input_items, run_items_to_input_items


def should_attach_generic_agent_error(exc: Exception) -> bool:
    """Return True when a span should record a generic agent error for this exception."""
    return not isinstance(
        exc,
        (
            ModelBehaviorError,
            InputGuardrailTripwireTriggered,
            OutputGuardrailTripwireTriggered,
        ),
    )


def prepare_turn_input_items(
    caller_input: str | list[TResponseInputItem],
    generated_items: list[RunItem],
    reasoning_item_id_policy: ReasoningItemIdPolicy | None,
) -> list[TResponseInputItem]:
    """Merge caller input with generated run items for the next model call."""
    caller_items = ItemHelpers.input_to_new_input_list(caller_input)
    continuation_items = run_items_to_input_items(generated_items, reasoning_item_id_policy)
    return prepare_model_input_items(caller_items, continuation_items)
