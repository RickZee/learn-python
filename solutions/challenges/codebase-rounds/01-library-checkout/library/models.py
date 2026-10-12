class Book:
    def __init__(self, title: str) -> None:
        self.title = title

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Book) and self.title == other.title
