"""UI utils."""


import logging
import time

import rich

from rich.table import Table
from rich.progress import track

from omoidasu.models import Card

logger = logging.getLogger(__name__)


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
        kwargs['title'] = f"{len(cards)} cards."
    table = Table(**kwargs)
    names = Card.__fields__.keys()
    for name in names:
        table.add_column(header=name)
    progressbar_text = f"Generating table for {len(cards)} cards..."
    for card in track(cards, progressbar_text):
        elements = [str(getattr(card, name)) for name in names]
        table.add_row(*elements)
        if context.obj.slow:
            time.sleep(0.05)
    rich.print(table)
