"""Async functions for CLI"""


import logging
import random

from omoidasu import crud, utils, models

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
    all_questions = []
    for card in cards:
        all_questions.extend(card.get_questions())
    random.shuffle(all_questions)
    for question in all_questions:
        question.ask()


async def add_card(context, sides: list[str]):
    card_content = [models.Side(
        id=i, content=content) for i, content in enumerate(sides)]
    card = models.Card(filename=None, sides=card_content)
    result = await crud.add_card(context, card)
    return result
