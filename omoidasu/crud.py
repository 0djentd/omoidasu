import logging
import json
import re

import requests

from omoidasu.models import Card, CardAdd

logger = logging.getLogger(__name__)


async def get_cards(context, regular_expression) -> list[Card] | None:
    """Get cards filtered by tags."""
    async with context.obj.session as session:
        async with session.get("/api/cards/") as res:
            if res.status != 200:
                return None
            data = await res.json()
    cards = [Card(**card) for card in data]
    result: list[Card] = []
    for card in cards:
        if re.findall(regular_expression, card.json()):
            result.append(card)
    return result


def get_card_by_id(context, card_id: int) -> Card | None:
    """Get cards filtered by tags."""
    res = requests.get("/api/cards/{card_id}/")
    if res.status_code == 200:
        return Card(**res.json())
    return None


def add_card(context, **kwargs) -> Card | None:
    """Add new card."""
    new_card = CardAdd(**kwargs)
    res = requests.post("/api/cards/", data=new_card.json())
    if res.status_code == 200:
        return Card(**res.json())
    return None


def remove_card(context, card: Card) -> bool:
    """Remove card."""
    res = requests.delete("/api/cards/{card.id}/")
    if res.status_code == 200:
        return True
    return False


def update_card(context, card: Card) -> Card | None:
    """Update card."""
    res = requests.patch("/api/cards/{card.id}/", data=card.json())
    if res.status_code == 200:
        return Card(**res.json())
    return None
