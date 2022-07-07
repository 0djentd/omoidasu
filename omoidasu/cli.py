"""CLI module."""


import logging
import asyncio

from pprint import pprint
from types import FunctionType
from typing import Any

import click
import rich

from rich.progress import track
from rich.prompt import Prompt

from omoidasu import models, commands

logger = logging.getLogger(__name__)


INFO_TEXT = """CLI for Omoidasu."""


def _run_async_command(func: Any, *args, **kwargs) -> Any:
    return asyncio.run(func(*args, **kwargs))


@click.group(help=INFO_TEXT)
@click.option("--verbose/--no-verbose",
              help="Show additional information")
@click.option("-d", "--debug/--no-debug",
              help="Show debug information")
@click.option("--api", type=str, default="http://localhost:8000",
              help="API url.")
@click.option("--slow/--no-slow", default=False)
@click.pass_context
def cli_commands(context, **kwargs):
    """CLI commands"""
    context.obj = models.AppConfig(**kwargs)
    if kwargs['debug']:
        click.echo(f"debug: {context.obj.debug}")
        logger.setLevel(level=logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
        pprint(context.obj)


@cli_commands.command("list")
@click.argument("regular_expression", required=True, default=".*", type=str)
@click.pass_context
def list_cards(*args, **kwargs):
    """List all cards."""
    return _run_async_command(commands.list_cards, *args, **kwargs)


@cli_commands.command("review")
@click.argument("regular_expression", required=True, default=".*", type=str)
@click.option("--max-cards", required=False, default=100, type=int)
@click.pass_context
def review_cards(*args, **kwargs):
    """Review all cards."""
    return _run_async_command(commands.review_cards, *args, **kwargs)


@cli_commands.command("add")
@click.pass_context
def add_card(*args, **kwargs):
    """Add new card."""
    return _run_async_command(commands.add_card, *args, **kwargs)


@cli_commands.command("remove")
@click.argument("regular_expression", required=True, type=str)
@click.pass_context
def remove_cards(*args, **kwargs):
    """Remove cards."""
    return _run_async_command(commands.remove_cards, *args, **kwargs)


@cli_commands.command("edit")
@click.pass_context
@click.argument("card_id", type=int, required=True)
@click.option("--question", type=str, prompt="Question")
@click.option("--answer", type=str, prompt="Answer")
def edit_card(*args, **kwargs):
    """Edit card."""
    return _run_async_command(commands.edit_card, *args, **kwargs)


@cli_commands.group("auth")
@click.pass_context
def auth_commands(context):  # pylint: disable=unused-argument
    """Authentication."""


@auth_commands.command()
@click.pass_context
def status(*args, **kwargs):
    """Show authentication status."""
    return _run_async_command(commands.status, *args, **kwargs)


@auth_commands.command()
@click.pass_context
@click.option("--username", prompt="Username")
@click.password_option("--password", prompt="Password")
def login(*args, **kwargs):
    """Login."""
    return _run_async_command(commands.login, *args, **kwargs)


@auth_commands.command()
@click.pass_context
def logout(*args, **kwargs):
    """Logout."""
    return _run_async_command(commands.logout, *args, **kwargs)


def main():
    """Main function."""
    cli_commands()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
