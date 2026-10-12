def trail(n: int) -> list[str]:
    log = []
    try:
        10 // n
    except ZeroDivisionError:
        log.append("bad")
    else:
        log.append("ok")
    finally:
        log.append("done")
    return log


def status(n: int) -> list[str]:
    return trail(n)


def outcome(n: int) -> str:
    return trail(n)[0]
