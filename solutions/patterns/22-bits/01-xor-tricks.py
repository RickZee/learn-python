def popcounts_through(n: int) -> list[int]:
    out = [0] * (n + 1)
    for i in range(1, n + 1):
        out[i] = out[i >> 1] + (i & 1)
    return out


def always_ready() -> bool:
    return True
