"""CRUD functions."""


import logging
from pprint import pprint
import re
import asyncio

import requests
import rich

from omoidasu.models import Card, CardBase

logger = logging.getLogger(__name__)


async def get_cards(context, regular_expression) -> list[Card] | None:
    """Get cards filtered by tags."""
    async with context.obj.session.get("/api/cards/") as res:
        if res.status != 200:
            return None
        data = await res.json()
    cards = [Card(**card) for card in data]
    result: list[Card] = []

    async def check(card: Card, regular_expression) -> Card | None:
        text = card.json()
        if re.findall(regular_expression, text):
            return card
        return None

    checks = []
    for card in cards:
        task = asyncio.create_task(check(card, regular_expression))
        checks.append(task)
    checks_result = await asyncio.gather(*checks)
    result = [card for card in checks_result if isinstance(card, Card)]
    return result


async def get_card_by_id(context, card_id: int) -> Card | None:
    """Get cards filtered by tags."""
    async with context.obj.session.get(
            f"/api/cards/{card_id}") as res:
        if res.status != 200:
            return None
        data = await res.json()
        return Card(**data)


async def add_card(context, card: CardBase) -> Card | None:
    """Add new card."""
    json_data = {"json": card.dict()}
    async with context.obj.session.post(
            "/api/cards/", **json_data) as res:
        if res.status != 200:
            return None
        data = await res.json()
        return Card(**data)


async def remove_card(context, card: Card) -> bool:
    """Remove card."""
    async with context.obj.session.delete(
            f"/api/cards/{card.id}/") as res:
        if res.status != 200:
            return False
        return True


async def update_card(context, card: Card) -> Card | None:
    """Update card."""
    card_add = CardBase(question=card.question,
                          answer=card.answer,
                          ok=card.ok,
                          fail=card.fail
                          ).dict()
    async with context.obj.session.patch(
            f"/api/cards/{card.id}/", json=card_add) as res:
        if res.status != 200:
            return None
        data = await res.json()
        return Card(**data)
