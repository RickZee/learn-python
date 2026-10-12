
def marker() -> str:
    return "close"


class Door:
    def __enter__(self):
        self.log = ["open"]
        return self

    def __exit__(self, exc_type, exc, tb):
        self.log.append("close")
        return False


def visit() -> list[str]:
    with Door() as entered:
        entered.log.append("inside")
        return entered.log


def closed() -> str:
    with Door() as entered:
        entered.log.append("inside")
    return entered.log[-1]
