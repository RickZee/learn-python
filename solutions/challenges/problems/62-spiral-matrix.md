# 62. Spiral Matrix — walkthrough

## Recognize it
Read an `m×n` matrix in clockwise spiral order into a flat list. Look-alike: generate spiral matrix (write 1..n² into a square). Another look-alike: diagonal traverse.

## Brute force
Simulate a robot with a direction vector and a visited set; turn right when the next cell is out of bounds or visited. Correct and O(m·n) time with O(m·n) visited space—or mark in place if mutation is allowed.

## Key insight
Maintain shrinking bounds `top, bottom, left, right`. Walk top row left→right, right column top→bottom, bottom row right→left (if a row remains), left column bottom→top (if a column remains), tightening the bound after each side. Guard the last two sides so a single middle row or column is not double-counted.

## Algorithm
1. If matrix empty, return `[]`.
2. `top, bottom, left, right = 0, m-1, 0, n-1`; `out = []`.
3. While `top <= bottom` and `left <= right`:
   - Append `matrix[top][c]` for `c` in left..right; `top += 1`.
   - Append `matrix[r][right]` for `r` in top..bottom; `right -= 1`.
   - If `top <= bottom`: append bottom row right→left; `bottom -= 1`.
   - If `left <= right`: append left column bottom→top; `left += 1`.
4. Return `out`.

## Trace
```
1 2 3
4 5 6
7 8 9
```

| layer walk | appended | bounds after |
|---|---|---|
| top row | 1,2,3 | top=1 |
| right col | 6,9 | right=1 |
| bottom row | 8,7 | bottom=1 |
| left col | 4 | left=1 |
| top row | 5 | done |

Result `[1,2,3,6,9,8,7,4,5]`.

## Complexity
Each cell appended once: O(m·n) time, O(1) extra besides the output. Visited-matrix simulation is the same time with more memory.

## Edge cases
Single row. Single column. `1×1`. Wide rectangle vs tall. Empty matrix. Even dimensions where the last ring is a 2×2.

## Alternatives and trade-offs
Direction + visited is shorter to type if you already know the turn trick. Layer bounds are clearer for proving no double visits. Generating a spiral (fill) uses the same bound machine.

## Common bugs
Omitting `if top <= bottom` so the bottom row reprints the top when one row remains. Shrinking `right` before the vertical walk uses the old bound incorrectly. Infinite loop when bounds cross without the while guard.

## Follow-ups
Spiral Matrix II (generate). Spiral Matrix III (walk off the board with steps). Anti-clockwise spiral.

## Related problems
Spiral Matrix II, Rotate Image, Diagonal Traverse, Pacific Atlantic Water Flow.
