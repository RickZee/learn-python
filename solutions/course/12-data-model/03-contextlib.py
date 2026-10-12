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
