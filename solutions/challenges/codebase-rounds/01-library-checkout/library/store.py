class Store:
    def __init__(self, titles: list[str]) -> None:
        self.titles = list(titles)
        self.index = {title: index for index, title in enumerate(self.titles)}

    def find(self, title: str) -> int:
        return self.index.get(title, -1)
