from collections import defaultdict


def by_initial(words: list[str]) -> dict[str, list[str]]:
    groups = defaultdict(list)
    for word in words:
        groups[word[0]].append(word)
    return dict(groups)


def group_by_length(words: list[str]) -> dict[int, list[str]]:
    groups = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)
    return dict(groups)


def even_odd(nums: list[int]) -> dict[str, list[int]]:
    groups = defaultdict(list)
    for value in nums:
        key = "even" if value % 2 == 0 else "odd"
        groups[key].append(value)
    return dict(groups)
