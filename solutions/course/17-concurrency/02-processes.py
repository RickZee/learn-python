def runner_for(work: str) -> str:
    if work == "cpu":
        return "process"
    return "thread"


def label_cpu() -> str:
    return "process"


def runtime_for(work: str) -> str:
    if work == "cpu":
        kind = "pool"
        return kind
    return "loop"


def pick_worker() -> str:
    choice = "top-level function"
    reason = "picklable"
    ok = choice.startswith("top-level")
    return choice if ok else reason
