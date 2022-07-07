"""CLI module."""


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

INFO_TEXT = """CLI for Omoidasu.
"""


@click.group(help=INFO_TEXT)
@click.option("--verbose/--no-verbose",
              help="Show additional information")
@click.option("-d", "--debug/--no-debug",
              help="Show debug information")
@click.option("--api", type=str, default="http://localhost:8000",
              help="API url.")
@click.option("--slow/--no-slow", default=False)
@click.pass_context
def cli_commands(context: click.Context, **kwargs):
    """CLI commands"""
    context.obj = models.AppConfig(**kwargs)
    if kwargs['debug']:
        click.echo(f"debug: {context.obj.debug}")
        logger.setLevel(level=logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
        rich.inspect(context.obj)


@cli_commands.command("list")
@click.argument("regular_expression", required=True, default=".*", type=str)
@click.pass_context
def list_cards(context, regular_expression):
    """List all cards."""
    cards = asyncio.run(crud.get_cards(context, regular_expression))
    utils.show_cards_list_table(context, cards)


@cli_commands.command("review")
@click.argument("regular_expression", required=True, default=".*", type=str)
@click.option("--max-cards", required=False, default=100, type=int)
@click.pass_context
def review_cards(context, regular_expression, max_cards):
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


@cli_commands.command("add")
@click.pass_context
def add_card(context):
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


@cli_commands.command("remove")
@click.argument("regular_expression", required=True, type=str)
@click.pass_context
def remove_cards(context, regular_expression):
    """Remove cards."""
    cards = asyncio.run(crud.get_cards(context, regular_expression))
    if not cards:
        rich.print("Error")
        raise click.Abort
    if len(cards) == 0:
        rich.print("No cards matching regular expression found.")
        raise click.Abort
    utils.show_cards_list_table(context, cards)
    if not click.confirm("Remove?", default=True):
        raise click.Abort
    asyncio.run(crud.remove_cards(context, cards))
    rich.print("[green]Done![/green]")


@cli_commands.command("edit")
@click.pass_context
@click.argument("card_id", type=int, required=True)
@click.option("--question", type=str, prompt="Question")
@click.option("--answer", type=str, prompt="Answer")
def edit_card(context, card_id, question, answer):
    """Edit card."""
    card = crud.get_card_by_id(context, card_id)
    if not card:
        return
    card.question = question
    card.answer = answer
    card = crud.update_card(context, card)
    card.show(context)


@cli_commands.group("auth")
@click.pass_context
def auth_commands(context):  # pylint: disable=unused-argument
    """Authentication."""


@auth_commands.command()
@click.pass_context
def status(context):
    """Show authentication status."""
    if context.obj.slow:
        time.sleep(3)
    user = auth.get_user(context)
    if user:
        rich.print(user)
    else:
        rich.print('[red]Use "omoidasu auth login" to login.[/red]')


@auth_commands.command()
@click.pass_context
@click.option("--username", prompt="Username")
@click.password_option("--password", prompt="Password")
def login(context, username, password):
    """Login."""
    if context.obj.slow:
        time.sleep(3)
    user = auth.login(context, username, password)
    if not user:
        rich.print("[red]Failed to login.[/red]")
        raise click.Abort
    rich.print(f"[green]Logged in as {user.username}.[/green]")


@auth_commands.command()
@click.pass_context
def logout(context):
    """Logout."""
    if context.obj.slow:
        time.sleep(3)
    if not auth.logout(context):
        rich.print("[red]Failed to logout.[/red]")
        raise click.Abort


def main():
    """Main function."""
    cli_commands()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
