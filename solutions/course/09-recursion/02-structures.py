def leaf_count(items: list) -> int:
    total = 0
    for item in items:
        if isinstance(item, list):
            total += leaf_count(item)
        else:
            total += 1
    return total


def nested_max(items: list) -> int | None:
    best = None
    for item in items:
        found = nested_max(item) if isinstance(item, list) else item
        if found is not None and (best is None or found > best):
            best = found
    return best


def tree_depth(node: tuple) -> int:
    children = node[1]
    if not children:
        return 1
    best = 0
    for child in children:
        best = max(best, tree_depth(child))
    return 1 + best


def tree_sum(node: tuple) -> int:
    value, children = node
    total = value
    for child in children:
        total += tree_sum(child)
    return total
