def present(data: dict[str, int], key: str) -> bool:
    return key in data


def index_by_city(people: list[tuple[str, str]]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for name, city in people:
        if city not in index:
            index[city] = []
        index[city].append(name)
    return index


def group_names(people: list[tuple[str, str]], cities: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for city in cities:
        groups[city] = []
    for name, city in people:
        groups[city].append(name)
    return groups


def merge_counts(first: dict[str, int], second: dict[str, int]) -> dict[str, int]:
    out = dict(first)
    for key, value in second.items():
        out[key] = out.get(key, 0) + value
    return out
