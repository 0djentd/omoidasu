from secrets import token_urlsafe
from typing import Iterable
from unittest import TestCase

from omoidasu.exceptions import NotEnoughCardSidesException
from omoidasu.models import Card, Question, Side


def generate_card_sides(count):
    result = []
    for i in range(count):
        side = Side(id=i, content=token_urlsafe())
        result.append(side)
    return result

class ModelsTests(TestCase):
    def test_card_constructor(self):
        sides = generate_card_sides(2)
        card = Card(filename=None, sides=sides)
        self.assertEqual(card.filename, None)

    def test_card_constructor_exception(self):
        with self.assertRaises(NotEnoughCardSidesException):
            Card(filename=None, sides=generate_card_sides(1))
