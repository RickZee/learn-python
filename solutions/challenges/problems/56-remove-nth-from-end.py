def remove_nth_from_end_list(values: list[int], n: int) -> list[int]:
    """Remove the n-th value from the end of a list (linked-list two-pointer idea).

    Approach: dummy + gap of n+1 between fast and slow indexes, then delete.
    Time: O(L)
    Space: O(L) for the copied list (O(1) pointers on real nodes)
    Alternative: two passes with an explicit length.
    Common bugs: gap of n instead of n+1; no dummy when deleting the head.
    """
    dummy = [0] + values
    fast = slow = 0
    for _ in range(n + 1):
        fast += 1
    while fast < len(dummy):
        fast += 1
        slow += 1
    del dummy[slow + 1]
    return dummy[1:]
