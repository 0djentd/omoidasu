"""Backend for omoidasu_cli"""

import logging
import dataclasses
import json

from pprint import pprint

import requests
import appdirs
import click
import colorama

from omoidasu import config

logger = logging.getLogger(__name__)

user_state_dir = appdirs.user_state_dir(appname=config.APP_NAME,
                                        version=config.VERSION)
user_config_dir = appdirs.user_config_dir(appname=config.APP_NAME,
                                          version=config.VERSION)


@dataclasses.dataclass
class Card():
    """Card model."""
    id: int
    question: str
    answer: str

    def show(self, context) -> None:
        """Show card."""
        if context.obj.debug:
            logger.debug("card: %s", self)
        click.echo(colorama.Style.DIM + f"Card #{self.id}")
        click.echo(colorama.Style.NORMAL + f"question: {self.question}")
        click.echo(f"answer: {self.answer}")


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


def update_card(context, id: int, question: str, answer: str) -> Card:
    """Add new card."""
    api = context.obj.api
    new_card = {"question": question, "answer": answer}
    data = json.dumps(new_card)
    res = requests.patch(f"{api}cards/{id}/", data=data)
    card = Card(**res.json())
    return card
