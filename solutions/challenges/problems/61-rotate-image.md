# 61. Rotate Image — walkthrough

## Recognize it
Rotate an `n×n` matrix 90° clockwise in place. Look-alike: rotate anti-clockwise (transpose then reverse columns, or reverse rows then transpose). Another look-alike: spiral copy into a new array (not in place).

## Brute force
Allocate an `n×n` result and set `result[j][n-1-i] = matrix[i][j]`, then copy back. Correct, uses O(n²) extra memory—rejected when the prompt says in-place.

## Key insight
A 90° clockwise turn equals transpose (swap across the main diagonal) followed by reversing each row. After transpose, the old column `j` becomes row `j`; reversing that row sends the former top entry to the right.

## Algorithm
1. For `i` in `0..n-1`, for `j` in `i+1..n-1`: swap `matrix[i][j]` with `matrix[j][i]`.
2. For each row: `row.reverse()`.
3. Return the same matrix object (mutated).

## Trace
```
1 2 3      transpose      1 4 7      reverse rows      7 4 1
4 5 6   →               2 5 8   →                  8 5 2
7 8 9                   3 6 9                      9 6 3
```

| step | matrix |
|---|---|
| start | [[1,2,3],[4,5,6],[7,8,9]] |
| after transpose | [[1,4,7],[2,5,8],[3,6,9]] |
| after reverse | [[7,4,1],[8,5,2],[9,6,3]] |

Layer-by-layer cycle `(i,j)→(j,n-1-i)→…` is an equivalent single-pass view.

## Complexity
Each element moved a constant number of times: O(n²) time, O(1) extra space. The copy-out approach is the same time with O(n²) space.

## Edge cases
`n = 1` no-op. `n = 2` one swap on the diagonal pair then reverse. Even vs odd `n` (center cell stays on transpose). Rectangular matrices are out of scope for this problem.

## Alternatives and trade-offs
Four-way swaps on concentric rings avoid an explicit transpose—same cost, easier to get indexes wrong. Anti-clockwise: reverse rows first, then transpose. Prefer transpose+reverse in timed challenges for clarity.

## Common bugs
Transposing the full square including rewriting the diagonal twice harmlessly, but looping `j` from 0 doubles-swaps off-diagonal back. Reversing columns instead of rows. Building a new matrix when in-place was required. Off-by-one `n-1-i`.

## Follow-ups
Rotate by 180° / 270°. Rotate an image represented sparsely. Circumferential reverse for anti-clockwise.

## Related problems
Spiral Matrix, Set Matrix Zeroes, Flipping an Image, Rotate Array.
