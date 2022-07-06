import logging
import json
import re

import requests

from omoidasu.models import Card

logger = logging.getLogger(__name__)


def get_cards(context, regular_expression) -> list[Card]:
    """Get cards filtered by tags."""
    api = context.obj.api
    res = requests.get(f"{api}cards/")
    cards = [Card(**card) for card in res.json()]
    result: list[Card] = []
    for card in cards:
        card_str = str(card)[5:-1]
        if re.findall(regular_expression, card_str):
            result.append(card)
    return result


def get_card_by_id(context, card_id: int) -> Card | None:
    """Get cards filtered by tags."""
    api = context.obj.api
    res = requests.get(f"{api}cards/{card_id}/")
    return Card(**res.json())


def add_card(context, question=None, answer=None) -> Card:
    """Add new card."""
    api = context.obj.api
    new_card = {"question": question, "answer": answer}
    data = json.dumps(new_card)
    res = requests.post(f"{api}cards/", data=data)
    card = Card(**res.json())
    return card


def remove_card(context, card_id):
    """Remove card."""
    api = context.obj.api
    res = requests.delete(f"{api}cards/{card_id}/")
    return res.json


def update_card(context, card: Card) -> Card:
    """Update card."""
    api = context.obj.api
    new_card = {"question": card.question, "answer": card.answer,
                "ok": card.ok, "fail": card.fail, }
    data = json.dumps(new_card)
    res = requests.patch(f"{api}cards/{card.id}/", data=data)
    card = Card(**res.json())
    return card
