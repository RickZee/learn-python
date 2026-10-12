def count_bits(n: int) -> list[int]:
    """Popcount for every integer from 0 through n.

    Approach: out[i] = out[i >> 1] + (i & 1).
    Time: O(n)
    Space: O(n) for the answer
    Alternative: per-number bit_count in O(n log n) total.
    Common bugs: allocating length n instead of n+1; using / instead of >>.
    """
    out = [0] * (n + 1)
    for i in range(1, n + 1):
        out[i] = out[i >> 1] + (i & 1)
    return out
