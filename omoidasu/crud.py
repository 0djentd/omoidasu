import logging
import json
import re
import asyncio

import requests
import aiohttp

from omoidasu.models import Card, CardAdd

logger = logging.getLogger(__name__)


async def get_cards(context, regular_expression) -> list[Card] | None:
    """Get cards filtered by tags."""
    context.obj.session = aiohttp.ClientSession(context.obj.api)
    response_data = None
    async with context.obj.session as session:
        async with session.get("/api/cards/") as res:
            if res.status != 200:
                return None
            response_data = await res.json()
    cards = [Card(**card) for card in response_data]
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


async def remove_cards(context, cards: list[Card]):
    context.obj.session = aiohttp.ClientSession(context.obj.api)
    tasks = []
    for card in cards:
        task = asyncio.create_task(remove_card(context, card))
        tasks.append(task)
    result = asyncio.gather(*tasks)
    await result


async def remove_card(context, card: Card) -> bool:
    """Remove card."""
    async with context.obj.session as session:
        async with session.delete(f"/api/cards/{card.id}/") as res:
            if res.status == 200:
                return True
            return False


def update_card(context, card: Card) -> Card | None:
    """Update card."""
    api = context.obj.api
    res = requests.patch(f"{api}cards/{card.id}/", data=card.json())
    if res.status_code == 200:
        return Card(**res.json())
    return None
