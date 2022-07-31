"""CLI module."""

import os
import logging
import asyncio

from typing import Any

import appdirs
import click
import rich

from omoidasu import commands, config


# Default directories
app_dir_settings = {"appname": "omoidasu"}
_CONFIG_DIR = appdirs.user_config_dir(**app_dir_settings)
_DATA_DIR = appdirs.user_data_dir(**app_dir_settings)
_CACHE_DIR = appdirs.user_cache_dir(**app_dir_settings)
_STATE_DIR = appdirs.user_state_dir(**app_dir_settings)
_LOG_DIR = appdirs.user_log_dir(**app_dir_settings)

# Environment variables
_PREFIX = "OMOIDASU"
_CONFIG_DIR = os.environ.get(_PREFIX + "_CONFIG_DIR", _CONFIG_DIR)
_DATA_DIR = os.environ.get(_PREFIX + "_DATA_DIR", _DATA_DIR)
_CACHE_DIR = os.environ.get(_PREFIX + "_CACHE_DIR", _CACHE_DIR)
_STATE_DIR = os.environ.get(_PREFIX + "_STATE_DIR", _STATE_DIR)
_LOG_DIR = os.environ.get(_PREFIX + "_LOG_DIR", _LOG_DIR)

logger = logging.getLogger(__name__)


INFO_TEXT = """CLI for Omoidasu."""


def _run_async_command(func: Any, *args, **kwargs) -> Any:
    context = args[0]
    if context.obj.debug:
        rich.inspect(context.obj, title="Context")
        rich.inspect(args, title="Args")
        rich.inspect(kwargs, title="Kwargs")
    return asyncio.run(func(*args, **kwargs))


@click.group(help=INFO_TEXT)
@click.option("--data-dir",
              type=str, default=_DATA_DIR)
@click.option("--config-dir",
              type=str, default=_CONFIG_DIR)
@click.option("--cache-dir",
              type=str, default=_CACHE_DIR)
@click.option("--state-dir",
              type=str, default=_STATE_DIR)
@click.option("--log-dir",
              type=str, default=_LOG_DIR)
@click.option("--verbose/--no-verbose",
              help="Show additional information")
@click.option("--script/--no-script",
              help="Use interactive features.")
@click.option("--debug/--no-debug")
@click.pass_context
def cli_commands(context, **kwargs):
    """CLI commands"""
    context.obj = config.AppConfig(**kwargs)
    if kwargs['debug']:
        logger.setLevel(level=logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
        rich.inspect(context.obj)


@cli_commands.command("list")
@click.argument("regular_expression", default=".*", required=True, type=str)
@click.option("--max-cards", default=1000, type=int,
              help="Max number of cards to list.")
@click.pass_context
def list_cards(*args, **kwargs):
    """Writes all cards to stdout
    in following format:

    card_1_side_1
    card_1_side_2

    card_2_side_1
    card_2_side_2
    card_2_side_3
    """
    return _run_async_command(commands.list_cards, *args, **kwargs)


@cli_commands.command("review")
@click.argument("regular_expression", default=".*", required=True, type=str)
@click.option("--max-cards", default=1000, type=int,
              help="Max number of cards to review.")
@click.pass_context
def review_cards(*args, **kwargs):
    """Review all cards."""
    return _run_async_command(commands.review_cards, *args, **kwargs)


def main():
    """Main function."""
    cli_commands()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
