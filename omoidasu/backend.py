"""Backend for Omoidasu"""

import logging
import dataclasses

import requests
import appdirs
import click

from omoidasu import config

logger = logging.getLogger(__name__)

user_state_dir = appdirs.user_state_dir(appname=config.APP_NAME,
                                        version=config.VERSION)
user_config_dir = appdirs.user_config_dir(appname=config.APP_NAME,
                                          version=config.VERSION)


@dataclasses.dataclass
class Card():
    id: int
    question: str
    answer: str

    def show(self, context):
        click.echo()
        click.echo(f"Card #{self.id}")
        click.echo(f"question: {self.question}")
        click.echo(f"answer: {self.answer}")


def get_cards(context):
    api = context.obj.api
    res = requests.get(api + "cards/")
    return [Card(**card) for card in res.json()]
