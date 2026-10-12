def assign_cookies(greed: list[int], sizes: list[int]) -> int:
    greed = sorted(greed)
    sizes = sorted(sizes)
    i = j = 0
    while i < len(greed) and j < len(sizes):
        if sizes[j] >= greed[i]:
            i += 1
        j += 1
    return i
