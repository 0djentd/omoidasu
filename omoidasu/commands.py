import time
import logging
import asyncio

from pprint import pprint

import click
import rich
import aiohttp

from rich.progress import track
from rich.prompt import Prompt

from omoidasu import crud, utils, models, auth

logger = logging.getLogger(__name__)


def _add_session(func):
    async def add_session_wrapper(context, *args, **kwargs):
        config = context.obj
        config.session = aiohttp.ClientSession(config.api)
        result = await func(context, *args, **kwargs)
        await config.session.close()
        return result
    return add_session_wrapper


@_add_session
async def list_cards(context, regular_expression):
    """List all cards."""
    cards = await crud.get_cards(context, regular_expression)
    utils.show_cards_list_table(context, cards)


@_add_session
async def review_cards(context, regular_expression, max_cards):
    """Review all cards."""
    cards = crud.get_cards(context, regular_expression)
    if len(cards) > max_cards:
        cards = cards[:max_cards]
    for card in cards:
        card.review(context)
        rich.print()
    for card in track(cards, description=f"Sync {len(cards)} cards..."):
        crud.update_card(context, card)
        if context.obj.slow:
            time.sleep(0.5)
    rich.print("[green]Done![/green]")


@_add_session
async def add_card(context):
    """Add new card."""
    adding = True
    cards: list[models.Card] = []
    while adding:
        question = Prompt.ask("[yellow]Q[/yellow]")
        answer = Prompt.ask("[yellow]A[/yellow]")
        card = crud.add_card(context, question=question, answer=answer)
        cards.append(card)
        adding = click.confirm("Add another card?", default=True)
    rich.print("[green]Done![/green]")
    utils.show_cards_list_table(context, cards)


@_add_session
async def remove_cards(context, regular_expression):
    """Remove cards."""
    cards = crud.get_cards(context, regular_expression)
    if len(cards) == 0:
        rich.print("No cards matching regular expression found.")
        raise click.Abort
    utils.show_cards_list_table(context, cards)
    if not click.confirm("Remove?", default=True):
        raise click.Abort
    for card in track(cards, f"Removing {len(cards)} cards..."):
        crud.remove_card(context, card)
    rich.print("[green]Done![/green]")


@_add_session
async def edit_card(context, card_id, question, answer):
    """Edit card."""
    card = crud.get_card_by_id(context, card_id)
    if not card:
        return
    card.question = question
    card.answer = answer
    card = crud.update_card(context, card)
    card.show(context)


@_add_session
async def status(context):
    """Show authentication status."""
    if context.obj.slow:
        time.sleep(3)
    user = auth.get_user(context)
    if user:
        rich.print(user)
    else:
        rich.print('[red]Use "omoidasu auth login" to login.[/red]')


@_add_session
async def login(context, username, password):
    """Login."""
    if context.obj.slow:
        time.sleep(3)
    user = auth.login(context, username, password)
    if not user:
        rich.print("[red]Failed to login.[/red]")
        raise click.Abort
    rich.print(f"[green]Logged in as {user.username}.[/green]")


@_add_session
async def logout(context):
    """Logout."""
    if context.obj.slow:
        time.sleep(3)
    if not auth.logout(context):
        rich.print("[red]Failed to logout.[/red]")
        raise click.Abort
