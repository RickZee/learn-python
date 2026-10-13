import json


def to_json(data) -> str:
    return json.dumps(data)


def from_json(text: str):
    return json.loads(text)


def dump_list(items: list[int]) -> str:
    return json.dumps(items)


def keys_of(text: str) -> list[str]:
    data = json.loads(text)
    keys = list(data)
    result = sorted(keys)
    return result


def pair_type() -> str:
    data = json.loads(json.dumps({"pair": (1, 2)}))
    return type(data["pair"]).__name__
