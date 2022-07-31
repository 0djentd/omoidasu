"""CRUD functions."""


import logging
import re

from omoidasu.models import Card

logger = logging.getLogger(__name__)


async def get_cards(context, regular_expression) -> list[Card]:
    """Get cards filtered by regular expression."""
    result = []
    return result


async def add_card(context, card: Card) -> Card:
    """Add new card. Returns created card."""
    result: Card
    return result


async def remove_card(context, card: Card) -> bool:
    """Remove card. Returns true, if successfully removed."""
    return False


async def update_card(context, card: Card) -> Card:
    """Update card. Returns updated card."""
    result: Card
    return result
