"""CRUD functions."""


import os
import logging

from omoidasu.models import Card, Side

logger = logging.getLogger(__name__)


def load_flashcard(filename) -> Card:
    """Loads flashcard from file."""
    sides: list[Side] = []
    if not os.path.isfile(filename):
        raise TypeError
    with open(filename, encoding="utf-8") as file:
        for index, line in enumerate(file.readlines()):
            sides.append(Side(id=index, content=line))
    return Card(filename=filename, sides=sides)


async def get_cards(context, regular_expression) -> list[Card]:
    """Get cards filtered by regular expression."""
    directory = context.obj.flashcards_dir
    os.makedirs(directory)
    flashcards = [load_flashcard(file) for file in os.scandir(directory)]
    return flashcards


# async def add_card(context, card: Card) -> Card:
#     """Add new card. Returns created card."""
#     result: Card
#     return result


# async def remove_card(context, card: Card) -> bool:
#     """Remove card. Returns true, if successfully removed."""
#     return False


# async def update_card(context, card: Card) -> Card:
#     """Update card. Returns updated card."""
#     result: Card
#     return result
