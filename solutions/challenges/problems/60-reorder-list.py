def reorder_values(values: list[int]) -> list[int]:
    """Interleave the front half with the reversed back half.

    Approach: split at mid, reverse the right piece, zip into a new list.
    On real nodes: mid + reverse second half + alternate merge (O(1) extra).
    Time: O(n)
    Space: O(n) here (O(1) on linked nodes)
    Alternative: copy to an array of pointers then reconnect.
    Common bugs: wrong midpoint; leaving a cycle when reversing nodes.
    """
    if len(values) <= 2:
        return list(values)
    mid = (len(values) + 1) // 2
    left = values[:mid]
    right = list(reversed(values[mid:]))
    out: list[int] = []
    for index, a in enumerate(left):
        out.append(a)
        if index < len(right):
            out.append(right[index])
    return out
