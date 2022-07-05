"""CLI module."""


import logging
import dataclasses
import click
import collections
from pprint import pprint
from omoidasu import backend

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class AppConfig():
    debug: bool
    verbose: bool
    api: str


@click.group()
@click.option("--verbose/--no-verbose",
              help="Show additional information")
@click.option("-d", "--debug/--no-debug",
              help="Show debug information")
@click.option("--api", type=str, default="http://localhost:8000/api/")
@click.pass_context
def cli_commands(context: click.Context, **kwargs):
    """CLI commands"""
    context.obj = AppConfig(**kwargs)
    if kwargs['debug']:
        click.echo(f"debug: {context.obj.debug}")
        logger.setLevel(level=logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
        pprint(context.obj)


@cli_commands.command()
@click.pass_context
def list_cards(context):
    """List all cards."""
    cards = backend.get_cards(context)
    for card in cards:
        card.show(context)


@cli_commands.command()
@click.pass_context
def review_cards(context):
    """Review all cards."""


@cli_commands.command()
@click.option("--question", type=str, prompt="Question")
@click.option("--answer", type=str, prompt="Answer")
@click.pass_context
def add_card(context, **kwargs):
    """Add new card."""
    card = backend.add_card(context, **kwargs)
    card.show(context)


@cli_commands.command()
@click.pass_context
@click.option("--id", type=int, prompt="id")
def remove_card(context, id: int):
    """Remove card."""
    res = backend.remove_card(context, id)
    pprint(res)


@cli_commands.command()
@click.pass_context
@click.option("--id", type=int, prompt="id")
@click.option("--question", type=str, prompt="Question")
@click.option("--answer", type=str, prompt="Answer")
def edit_card(context, id, question, answer):
    """Edit card."""
    card = backend.update_card(context, id, question, answer)
    card.show(context)



def main():
    """Main function."""
    cli_commands()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
