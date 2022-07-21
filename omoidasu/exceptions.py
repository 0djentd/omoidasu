class NotEnoughCardSidesException(Exception):
    filename: str
    sides_count: int

    def __init__(self, filename, sides_count):
        self.filename = str(filename)
        self.sides_count = int(sides_count)
