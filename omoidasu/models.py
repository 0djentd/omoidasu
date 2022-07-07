import logging
import time

from typing import Any

import rich

from rich.prompt import Prompt
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AppConfig(BaseModel):
    """App config object."""
    debug: bool
    verbose: bool
    api: str
    slow: bool
    session: Any | None = None


class CardBase(BaseModel):
    question: str
    answer: str
    ok: int = 0
    fail: int = 0


class Card(CardBase):
    """Card model."""
    id: int
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


class User(BaseModel):
    username: str
    email: str
