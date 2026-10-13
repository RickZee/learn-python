from contextlib import contextmanager


@contextmanager
def marker():
    try:
        yield "open"
    finally:
        pass


@contextmanager
def tracked():
    events = ["open"]
    try:
        yield events
    finally:
        events.append("close")


@contextmanager
def scratch():
    data = {}
    try:
        yield data
    finally:
        data.clear()


@contextmanager
def marked():
    events = ["open"]
    try:
        yield events
    finally:
        events.append("close")


def run_marked() -> list[str]:
    try:
        with marked() as events:
            events.append("inside")
            raise RuntimeError("boom")
    except RuntimeError:
        return events
