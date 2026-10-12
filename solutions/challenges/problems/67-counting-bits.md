# 67. Counting Bits — walkthrough

## Recognize it
For every `i` from 0 to `n`, return how many `1` bits are in its binary form. Look-alike: Hamming weight of one integer. Another look-alike: sum of two integers without `+` (bit ops, different goal).

## Brute force
For each `i`, count bits with `i.bit_count()` or a loop `while x: x &= x-1`. Total O(n log n) from bit widths—fine for small n, not the intended O(n) DP.

## Key insight
`out[i] = out[i >> 1] + (i & 1)`: dropping the last bit gives a smaller index already solved, then add back whether the last bit was set. Equivalently, `out[i] = out[i & (i-1)] + 1` using the lowest-set-bit clear.

## Algorithm
1. `out = [0] * (n + 1)`.
2. For `i` in 1..n: `out[i] = out[i >> 1] + (i & 1)`.
3. Return `out`.

## Trace
`n = 5`.

| i | binary | i>>1 | i&1 | out[i] |
|---|---|---|---|---|
| 0 | 0 | — | — | 0 |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 10 | 1 | 0 | 1 |
| 3 | 11 | 1 | 1 | 2 |
| 4 | 100 | 2 | 0 | 1 |
| 5 | 101 | 2 | 1 | 2 |

Result `[0,1,1,2,1,2]`.

## Complexity
O(n) time, O(n) space for the answer array (required). Per-number popcount is O(n log n) total. The DP reuses previous answers so each i is O(1).

## Edge cases
`n = 0` → `[0]`. Powers of two have a single bit. Odd numbers always add one to `out[i>>1]`. Large n up to typical 1e5 still linear.

## Alternatives and trade-offs
`out[i] = out[i & (i-1)] + 1` is a common variant. Built-in `bit_count` in a list comprehension is clear in modern Python but may miss the DP lesson. Prefer the shift recurrence in timed challenges.

## Common bugs
Off-by-one allocating `n` instead of `n+1`. Using `/` instead of `>>`. Starting the loop at 0 and reading `out[-1]`. Returning counts for 1..n without the leading zero.

## Follow-ups
Count bits in a range. Next number with same popcount. Maximum XOR of two numbers in an array.

## Related problems
Number of 1 Bits, Hamming Distance, Single Number, Sum of Two Integers.
