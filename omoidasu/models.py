import logging
from typing import Optional

import rich
from pydantic import BaseModel

from omoidasu.exceptions import NotEnoughCardSidesException

logger = logging.getLogger(__name__)


class Side(BaseModel):
    """Card side model."""
    id: int  # Line number.
    content: str


class Card(BaseModel):
    """Card model."""
    filename: Optional[str]  # Can be None, if not saved to file.
    sides: list[Side]

    @classmethod
    def load_from_file(cls, filename: str):
        """Loads card from file."""
        logger.info("Loading card from %s", filename)
        sides: list[Side] = []
        with open(filename, "r", encoding="utf-8") as file:
            for i, line in enumerate(file.readline()):
                side = Side(id=i, content=line)
                sides.append(side)
        if len(sides) == 0:
            raise NotEnoughCardSidesException(filename, len(sides))
        card = cls(filename=filename, sides=sides)
        logger.info("Loaded %s from %s", card, filename)
        return card

    def review(self):
        """Review all combinations."""
        sides = self.sides
        for question in sides:
            for answer in sides:
                _ = input(question)
                result = input(answer)
                if result not in ["", "y", "Y", "\n"]:
                    rich.print("[red]Wrong.[/red]")
                else:
                    rich.print("[green]Correct.[/green]")
