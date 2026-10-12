import json


def to_json(data: dict) -> str:
    return json.dumps(data)


def from_json(text: str) -> dict:
    return json.loads(text)


def dump_list(items: list) -> str:
    return json.dumps(items)


def keys_of(text: str) -> list:
    return list(json.loads(text))
