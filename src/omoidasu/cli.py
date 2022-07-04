import click


@click.group()
def main():
    """Main function."""
    pass


@main.command()
def list_cards():
    """List all cards."""
    pass


@main.command()
def review_cards():
    """Review all cards."""
    pass


@main.command()
def add_card():
    """Add new card."""
    pass


@main.command()
def remove_card():
    """Remove card."""
    pass


@main.command()
def edit_card():
    """Edit card."""
    pass


@main.command()
def stats():
    """Show user stats."""
    pass


if __name__ == "__main__":
    main()
