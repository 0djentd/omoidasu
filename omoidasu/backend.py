"""Backend for omoidasu_cli"""

import logging
import dataclasses
import json
import time
import datetime

from pprint import pprint

import requests
import appdirs
import click
import colorama
import rich

from rich.table import Table
from rich.prompt import Prompt
from rich.progress import track

from omoidasu import config

logger = logging.getLogger(__name__)

user_state_dir = appdirs.user_state_dir(appname=config.APP_NAME,
                                        version=config.VERSION)
user_config_dir = appdirs.user_config_dir(appname=config.APP_NAME,
                                          version=config.VERSION)


@dataclasses.dataclass
class AppConfig():
    """App config object."""
    debug: bool
    verbose: bool
    api: str
    slow: bool


@dataclasses.dataclass
class Card():
    """Card model."""
    id: int
    question: str
    answer: str
    ok: int
    fail: int
    user_id: int

    def show(self, context) -> None:  # pylint: disable=unused-argument
        """Show card."""
        rich.inspect(self, title=f"Card #{self.id}", docs=False, value=False)

    def review(self, context) -> None:  # pylint: disable=unused-argument
        """Review card."""
        rich.print(f"[grey]Card[/grey] #{self.id}")
        rich.print(f"[yellow]Q[/yellow]: {self.question}")
        time.sleep(1)
        rich.print(f"[yellow]A[/yellow]: {self.answer}")
        answer = Prompt.ask("[[green]Y[/green]/[red]n[/red]]").lower()
        yes = ["", "yes", "y", "true", "t"]
        if answer in yes:
            rich.print("[green]Correct![/green]")
            self.ok += 1
        else:
            rich.print("[red]Wrong![/red]")
            self.fail += 1

    def sync(self, context) -> None:
        """Sync card to server."""
        time.sleep(0.5)


def show_cards_list_grid(context, cards: list[Card], col: int = 3) -> None:
    """Show cards list as grid"""
    table = Table.grid()
    for _ in range(col):
        table.add_column()
    for i in range(len(cards))[::col]:
        table.add_row(*[str(card.id) for card in cards[i:i+col]])
    rich.print(table)


def show_cards_list_table(context, cards: list[Card], **kwargs):
    """Show cards list as table"""
    if "title" not in kwargs:
        kwargs['title'] = f"Cards ({len(cards)})"
    table = Table(**kwargs)
    names = [field.name for field in dataclasses.fields(Card)]
    for name in names:
        table.add_column(header=name)
    progressbar_text = f"Generating table for {len(cards)} cards..."
    for card in track(cards, progressbar_text):
        elements = [str(getattr(card, name)) for name in names]
        table.add_row(*elements)
        if context.obj.slow:
            time.sleep(0.05)
    rich.print(table)


def get_cards(context, tags=None) -> list[Card]:
    """Get cards filtered by tags."""
    if tags is None:
        tags = []
    api = context.obj.api
    res = requests.get(f"{api}cards/", params={"tags": tags})
    return [Card(**card) for card in res.json()]


def add_card(context, question=None, answer=None) -> Card:
    """Add new card."""
    api = context.obj.api
    new_card = {"question": question, "answer": answer}
    data = json.dumps(new_card)
    res = requests.post(f"{api}cards/", data=data)
    card = Card(**res.json())
    return card


def remove_card(context, id):
    """Remove card."""
    api = context.obj.api
    res = requests.delete(f"{api}cards/{id}/")
    return res.json


def update_card(context, card: Card) -> Card:
    """Update card."""
    api = context.obj.api
    new_card = {"question": card.question, "answer": card.answer,
                "ok": card.ok, "fail": card.fail, }
    data = json.dumps(new_card)
    res = requests.patch(f"{api}cards/{card.id}/", data=data)
    card = Card(**res.json())
    return card
