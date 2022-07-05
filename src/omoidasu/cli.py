"""CLI module."""


import logging
import dataclasses
import click
import collections
from pprint import pprint
from omoidasu import config

logger = logging.getLogger(__name__)

argument_tag = click.argument("Tag", type=str, required=False)


@dataclasses.dataclass
class AppConfig():
    debug: bool
    verbose: bool


@click.group()
@click.option("--verbose/--no-verbose",
              help="Show additional information")
@click.option("-d", "--debug/--no-debug",
              help="Show debug information")
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
@argument_tag
@click.pass_context
def list_cards(context: click.Context, tag):
    """List all cards."""


@cli_commands.command()
@argument_tag
@click.pass_context
def review_cards(context: click.Context, tag):
    """Review all cards."""


@cli_commands.command()
@click.pass_context
def add_card():
    """Add new card."""


@cli_commands.command()
@click.pass_context
def remove_card():
    """Remove card."""


@cli_commands.command()
@click.pass_context
def edit_card():
    """Edit card."""


@cli_commands.command()
@click.pass_context
def stats():
    """Show user stats."""


def main():
    """Main function."""
    cli_commands()


if __name__ == "__main__":
    main()
