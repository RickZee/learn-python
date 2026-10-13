from dataclasses import dataclass


def label(item) -> str:
    return item.name + " " + str(item.qty)


def describe(item) -> str:
    name = item.name
    qty = item.qty
    text = name + " " + str(qty)
    return text


def same_qty(left, right) -> bool:
    return left.qty == right.qty


@dataclass(frozen=True)
class Item:
    name: str
    qty: int


def keyed_qty(item: Item) -> int:
    store = {item: item.qty}
    # frozen: cannot mutate; lookup with equal key
    other = Item(item.name, item.qty)
    return store[other]
