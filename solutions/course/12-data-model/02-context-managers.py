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
    last = entered.log[-1]
    text = str(last)
    return text


def run_door() -> str:
    try:
        with Door():
            raise RuntimeError("boom")
        return "swallowed"
    except RuntimeError:
        return "raised"
