import logging
import json
import re

import requests

from omoidasu.models import Card, CardAdd

logger = logging.getLogger(__name__)


def get_cards(context, regular_expression) -> list[Card] | None:
    """Get cards filtered by tags."""
    api = context.obj.api
    res = requests.get(f"{api}cards/")
    if res.status_code != 200:
        return None
    cards = [Card(**card) for card in res.json()]
    result: list[Card] = []
    for card in cards:
        if re.findall(regular_expression, card.json()):
            result.append(card)
    return result


def get_card_by_id(context, card_id: int) -> Card | None:
    """Get cards filtered by tags."""
    api = context.obj.api
    res = requests.get(f"{api}cards/{card_id}/")
    if res.status_code == 200:
        return Card(**res.json())
    return None


def add_card(context, **kwargs) -> Card | None:
    """Add new card."""
    api = context.obj.api
    new_card = CardAdd(**kwargs)
    res = requests.post(f"{api}cards/", data=new_card.json())
    if res.status_code == 200:
        return Card(**res.json())
    return None


def remove_card(context, card: Card) -> bool:
    """Remove card."""
    api = context.obj.api
    res = requests.delete(f"{api}cards/{card.id}/")
    if res.status_code == 200:
        return True
    return False


def update_card(context, card: Card) -> Card | None:
    """Update card."""
    api = context.obj.api
    res = requests.patch(f"{api}cards/{card.id}/", data=card.json())
    if res.status_code == 200:
        return Card(**res.json())
    return None
