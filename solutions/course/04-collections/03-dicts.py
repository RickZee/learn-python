def present(data: dict[str, int], key: str) -> bool:
    return key in data


def lookup(data: dict[str, int], key: str, default: int) -> int:
    return data.get(key, default)


def get_or_set(data: dict[str, int], key: str, default: int) -> int:
    if key not in data:
        data[key] = default
    return data[key]
