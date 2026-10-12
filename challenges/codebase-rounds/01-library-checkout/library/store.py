class Store:
    def __init__(self, titles: list[str]) -> None:
        self.titles = list(titles)

    def find(self, title: str) -> int:
        for index, item in enumerate(self.titles):
            if item == title:
                return index
        return -1
