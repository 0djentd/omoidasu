"""Async functions for CLI"""


import time
import logging
import asyncio

from rich.progress import track
from rich.prompt import Prompt

from omoidasu import utils, models

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
        tasks.append(asyncio.create_task(crud.update_card(context, card)))
    await asyncio.gather(*tasks)
    rich.print("[green]Done![/green]")


async def add_card(context):
    """Add new card."""
    adding = True
    cards: list[models.CardBase] = []
    while adding:
        question = Prompt.ask("[yellow]Q[/yellow]")
        answer = Prompt.ask("[yellow]A[/yellow]")
        cards.append(models.CardBase(question=question, answer=answer))
        adding = click.confirm("Add another card?", default=True)

    tasks = []
    for card in cards:
        task = asyncio.create_task(crud.add_card(
                context, card))
        tasks.append(task)
    tasks_result = await asyncio.gather(*tasks)
    created_cards: list[models.Card] = [x for x in tasks_result if x]
    rich.print("[green]Done![/green]")
    utils.show_cards_list_table(context, created_cards)


async def remove_cards(context, regular_expression):
    """Remove cards."""
    cards = await crud.get_cards(context, regular_expression)
    if cards is None:
        raise TypeError
    if len(cards) == 0:
        rich.print("No cards matching regular expression found.")
        raise click.Abort
    utils.show_cards_list_table(context, cards)
    if not click.confirm("Remove?", default=True):
        raise click.Abort
    for card in track(cards, f"Removing {len(cards)} cards..."):
        await crud.remove_card(context, card)
    rich.print("[green]Done![/green]")


async def edit_card(context, card_id, question, answer):
    """Edit card."""
    card = await crud.get_card_by_id(context, card_id)
    if card is None:
        raise TypeError
    card.question = question
    card.answer = answer
    card = await crud.update_card(context, card)
    if card is None:
        raise TypeError
    card.show(context)
