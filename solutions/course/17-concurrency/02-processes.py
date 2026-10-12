def runner_for(work: str) -> str:
    if work == "cpu":
        return "process"
    return "thread"


def label_cpu() -> str:
    return "process"


def runtime_for(work: str) -> str:
    if work == "cpu":
        return "pool"
    return "loop"
