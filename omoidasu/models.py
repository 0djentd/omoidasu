import logging
import dataclasses
import time

import rich

from rich.prompt import Prompt

logger = logging.getLogger(__name__)


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


@dataclasses.dataclass
class User():
    username: str
    email: str
