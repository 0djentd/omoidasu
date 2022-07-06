"""CLI module."""


import time
import logging

from pprint import pprint

import click
import rich

from rich.progress import track

from omoidasu import crud, utils, models

logger = logging.getLogger(__name__)

INFO_TEXT = """CLI for Omoidasu.
"""


@click.group(help=INFO_TEXT)
@click.option("--verbose/--no-verbose",
              help="Show additional information")
@click.option("-d", "--debug/--no-debug",
              help="Show debug information")
@click.option("--api", type=str, default="http://localhost:8000/api/",
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
        pprint(context.obj)


@cli_commands.command("list")
@click.pass_context
def list_cards(context):
    """List all cards."""
    cards = crud.get_cards(context)
    utils.show_cards_list_table(context, cards)


@cli_commands.command("review")
@click.pass_context
def review_cards(context):
    """Review all cards."""
    cards = crud.get_cards(context)
    for card in cards:
        card.review(context)
        rich.print()
    for card in track(cards, description=f"Sync {len(cards)} cards..."):
        card.sync(context)
        if context.obj.slow:
            time.sleep(0.5)
    rich.print("[green]Done![/green]")


@cli_commands.command("add")
@click.option("--question", type=str, prompt="Question")
@click.option("--answer", type=str, prompt="Answer")
@click.pass_context
def add_card(context, **kwargs):
    """Add new card."""
    card = crud.add_card(context, **kwargs)
    card.show(context)


@cli_commands.command("remove")
@click.pass_context
@click.option("--id", type=int, prompt="id")
def remove_card(context, id: int):
    """Remove card."""
    res = crud.remove_card(context, id)
    pprint(res)


@cli_commands.command("edit")
@click.pass_context
@click.option("--id", type=int, prompt="id")
@click.option("--question", type=str, prompt="Question")
@click.option("--answer", type=str, prompt="Answer")
def edit_card(context, id, question, answer):
    """Edit card."""
    card = crud.get_card_by_id(context, id)
    if not card:
        return
    card.question = question
    card.answer = answer
    card = crud.update_card(context, card)
    card.show(context)


def main():
    """Main function."""
    cli_commands()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
