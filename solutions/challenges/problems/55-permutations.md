# 55. Permutations — walkthrough

## Recognize it
Return all orderings of a list of distinct numbers. Look-alike: permutations II (with duplicates—need skipping). Another look-alike: combinations / subsets (order irrelevant or element choice only).

## Brute force
Same as the solution: you must emit n! lists. The "brute" mistake is generating with nested loops for fixed n, or using `itertools` without understanding the swap recursion the challenge wants.

## Key insight
Heap's algorithm / swap-based backtracking: for position `start`, try every index `i >= start` as the next choice by swapping into `start`, recurse `start+1`, then swap back. When `start == n`, record a copy of the array.

## Algorithm
1. `out = []`; work on a mutable copy of `nums`.
2. `go(start)`: if `start == len(nums)`, append `list(nums)` and return; for `i` in `start..n-1`, swap `start` with `i`, `go(start+1)`, swap back.
3. `go(0)`; return `out`.

## Trace
`nums = [1,2,3]`.

| start | array before choices | emissions |
|---|---|---|
| 0 | [1,2,3] | try i=0,1,2 |
| 1 (after fix 1) | [1,2,3] | → [1,2,3], [1,3,2] |
| 1 (after fix 2) | [2,1,3] | → [2,1,3], [2,3,1] |
| 1 (after fix 3) | [3,2,1] | → [3,2,1], [3,1,2] |

Six permutations.

## Complexity
Time O(n · n!) to build and copy each permutation—you cannot do asymptotically better if the output lists every ordering. Extra space O(n) for the recursion stack (output stores Θ(n·n!) anyway). Generating without storing is the same time if the consumer is slow; timed challenges still expect you to materialize the full list.

## Edge cases
Empty list → `[[]]`. Single element. n=2. Distinctness assumed—duplicates would produce duplicate outputs without extra skip logic.

## Alternatives and trade-offs
Used-boolean array + path building (clearer for some). `itertools.permutations` in production Python. Recursive choose-next from a remaining set. Swap method is cache-friendly and in-place.

## Common bugs
Appending the same list object without copying. Forgetting to swap back. Looping `i` from 0 instead of `start` (duplicates and wrong counts). Mutating the caller's list permanently.

## Follow-ups
Permutations with duplicates. Next permutation. Permutation sequence (k-th).

## Related problems
Permutations II, Combinations, Subsets, Next Permutation, Letter Case Permutation.
