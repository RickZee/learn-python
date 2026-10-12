# 37. Unique Paths — walkthrough

## Recognize it
An `m` by `n` grid; you start at the top-left and may move only right or down. Count paths to the bottom-right. Look-alike: unique paths with obstacles (same recurrence, skip blocked cells). Another look-alike: shortest path in a grid (BFS for length, not count).

## Brute force
Recurse from `(0,0)`: at each cell try right and down, add the two subtree counts. Without memoization the same cell is solved exponentially often—roughly binomial many overlapping subproblems—so it blows past typical limits once `m` and `n` reach the mid-teens.

## Key insight
Every path to `(r, c)` arrives from the cell above or the cell to the left. So `ways[r][c] = ways[r-1][c] + ways[r][c-1]`, with the first row and first column equal to 1 (only one way along each edge). You only need the previous row (or even one rolling row) because each cell depends on left and "above," which is the same array before you overwrite it left-to-right.

## Algorithm
1. `row = [1] * n` — the first grid row: only right moves.
2. For each of the remaining `m - 1` rows:
   - For `col` from 1 to `n - 1`: `row[col] += row[col - 1]` (add left neighbor; `row[col]` still holds the value from the row above).
3. Return `row[-1]`.

## Trace
`m = 3`, `n = 3`. Start `row = [1, 1, 1]`.

| after row | row | note |
|---|---|---|
| start | [1, 1, 1] | top edge |
| +1 | [1, 2, 3] | col1: 1+1; col2: 1+2 |
| +2 | [1, 3, 6] | col1: 1+2; col2: 2+3 |

Bottom-right is 6: RRD, RDR, DRR, and the three paths that mix order differently among two rights and one down—wait, for 3×3 you need two rights and two downs: C(4,2) = 6.

## Complexity
Each of `m` rows touches `n` cells once: O(m·n) time. One array of length `n`: O(n) space. A full table is O(m·n) space for the same time. The closed form C(m+n-2, m-1) is O(min(m,n)) arithmetic but easy to overflow or mis-index in a timed challenge; the DP is clearer and matches the obstacle follow-up.

## Edge cases
`m = 1` or `n = 1` → answer 1 (only one corridor). `1×1` → 1. Large grids where recursion without cache times out. Swapping `m` and `n` must leave the answer unchanged.

## Alternatives and trade-offs
Full 2D table is easiest to explain on a whiteboard. Top-down `@cache` on `(r, c)` is the same math with recursion depth O(m+n). Combinatorial formula is fastest when you trust big-integer or modular arithmetic; skip it if the next question adds obstacles.

## Common bugs
Recursion with no memo (recomputes every cell). Filling right-to-left so you destroy the "above" value before using it when rolling one row. Off-by-one treating paths as needing `m` rights instead of `m-1`. Returning `row[0]` instead of the last cell.

## Follow-ups
Unique Paths II (obstacles). Count paths with exactly k turns. Large m,n with modular answer via factorials.

## Related problems
Climbing Stairs, Unique Paths II, Minimum Path Sum, Dungeon Game.
