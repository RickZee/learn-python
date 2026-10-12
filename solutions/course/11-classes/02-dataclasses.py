
def label(item) -> str:
    return item.name + " " + str(item.qty)


def describe(item) -> str:
    return item.name + " " + str(item.qty)


def same_qty(left, right) -> bool:
    return left.qty == right.qty
