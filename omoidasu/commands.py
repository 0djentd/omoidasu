"""Async functions for CLI"""


import logging

from omoidasu import utils, crud

logger = logging.getLogger(__name__)


async def list_cards(context, regular_expression, max_cards):
    """List all cards."""
    cards = await crud.get_cards(context, regular_expression)
    if len(cards) > max_cards:
        cards = cards[:max_cards]
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
