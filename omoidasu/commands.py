"""Async functions for CLI"""


import logging
import asyncio
import time

import rich
from rich.progress import track

from omoidasu import utils, crud

logger = logging.getLogger(__name__)


async def list_cards(context, regular_expression):
    """List all cards."""
    cards = await crud.get_cards(context, regular_expression)
    utils.show_cards_list_table(context, cards)


async def review_cards(context, regular_expression, max_cards):
    """Review all cards."""
    cards = await crud.get_cards(context, regular_expression)
    if not cards:
        raise ValueError
    if len(cards) > max_cards:
        cards = cards[:max_cards]
    for card in cards:
        card.review(context)
        rich.print()
    tasks = []
    for card in track(cards, description=f"Sync {len(cards)} cards..."):
        await asyncio.sleep(0.1)
    await asyncio.gather(*tasks)
    rich.print("[green]Done![/green]")
