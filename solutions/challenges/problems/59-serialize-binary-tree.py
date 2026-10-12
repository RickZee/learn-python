def serialize_level(values: list[int | None]) -> str:
    """Encode a level-order value list with null markers.

    Approach: join numbers and the token null with commas.
    Time: O(n)
    Space: O(n) for the string
    Alternative: preorder with nulls on Node objects.
    Common bugs: dropping nulls so structure is ambiguous.
    """
    return ",".join("null" if v is None else str(v) for v in values)


def deserialize_level(data: str) -> list[int | None]:
    """Decode a level-order string back into values with None holes.

    Approach: split on commas; map null → None and other tokens → int.
    Time: O(n)
    Space: O(n)
    Alternative: BFS wiring of Node children from the same token stream.
    Common bugs: using eval; mishandling negative numbers as null.
    """
    if not data:
        return []
    out = []
    for part in data.split(","):
        out.append(None if part == "null" else int(part))
    return out
