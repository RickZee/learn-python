def kth_smallest_values(level: list[int | None], k: int) -> int:
    """Kth smallest value in a BST given as level-order with None holes.

    Approach: collect non-null values and sort (matches in-order for unique BSTs).
    Time: O(n log n)
    Space: O(n)
    Alternative: iterative in-order with a stack and stop at k (O(h + k)).
    Common bugs: off-by-one on k; counting None placeholders as values.
    """
    values = [v for v in level if v is not None]
    values.sort()
    return values[k - 1]
