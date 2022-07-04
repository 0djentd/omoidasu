"""CLI module."""


import click


@click.group()
def main():
    """Main function."""


@main.command()
def list_cards():
    """List all cards."""


@main.command()
def review_cards():
    """Review all cards."""


@main.command()
def add_card():
    """Add new card."""


@main.command()
def remove_card():
    """Remove card."""


@main.command()
def edit_card():
    """Edit card."""


@main.command()
def stats():
    """Show user stats."""


if __name__ == "__main__":
    main()
