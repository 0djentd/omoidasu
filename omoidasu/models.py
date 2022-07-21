import logging

from pydantic import BaseModel

from omoidasu.exceptions import NotEnoughCardSidesException

logger = logging.getLogger(__name__)


class Side(BaseModel):
    """Card side model."""
    id: int
    content: str


class Card(BaseModel):
    """Card model."""
    filename: str
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
