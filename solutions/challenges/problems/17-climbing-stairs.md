# 17. Climbing Stairs — walkthrough

## Recognize it
You can climb 1 or 2 stairs at a time. Given n stairs, count the distinct sequences that reach the top. Order matters: 1 then 2 is different from 2 then 1. Look-alike: min cost climbing stairs (optimize cost, not count ways). Another look-alike: coin change with orderless combinations—here sequences are ordered, so this is Fibonacci-style path counting, not unbounded knapsack combinations.

## Brute force
Recurse: `ways(n) = ways(n-1) + ways(n-2)` with bases `ways(1)=1`, `ways(2)=2`. Without memoization the call tree recomputes the same subproblems exponentially often—roughly O(φⁿ) time. That dies for n in the dozens. Even with a full recursion tree drawn on paper you see massive overlap.

## Key insight
The only ways to step onto stair n are from n−1 (take a single) or from n−2 (take a double). So the answer is exactly the Fibonacci recurrence. Once you believe that, you only need the previous two answers at each step—no full table unless you want one for debugging.

## Algorithm
1. If `n <= 2`, return `n` (1 way for one stair, 2 ways for two).
2. Set `previous, current = 1, 2` meaning ways(1) and ways(2).
3. For `i` from 3 to n inclusive: set `previous, current = current, previous + current`.
4. Return `current`.

## Trace
`n = 5`.

| i | previous (ways i-2) | current (ways i-1) | ways(i) = sum |
|---|---|---|---|
| start | 1 | 2 | — |
| 3 | 2 | 3 | 1+2 |
| 4 | 3 | 5 | 2+3 |
| 5 | 5 | 8 | 3+5 |

Sequences for n=5: eight of them (Fibonacci). Spot-check n=3: `1+1+1`, `1+2`, `2+1` → 3.

## Complexity
The loop runs O(n) iterations with O(1) work each: O(n) time, O(1) extra space. A DP array of size n+1 is O(n) space for the same time—useful to show intermediates, unnecessary for the answer alone. Matrix exponentiation or fast doubling can reach O(log n) time for huge n; timed challenges rarely require that unless n is enormous and they ask.

## Edge cases
`n = 1` and `n = 2` hit the base return. `n = 0` is usually out of contract; if allowed, define 1 empty way or 0 per prompt. Integer overflow appears in fixed-width languages for large n; Python ints grow automatically. If steps could be any set `{1,2,...,k}`, the recurrence widens to a sum of k prior terms.

## Alternatives and trade-offs
Top-down recursion with `@cache` mirrors the recurrence and is easy to extend to more step sizes; space is O(n) for the cache and call stack. Bottom-up rolling variables are best for the classic 1-or-2 problem. Combinatorial closed form `C(n; number of 2-steps)` summed over possible double counts also works but is slower and easier to miscount.

## Common bugs
Plain recursion without a cache—timeouts on medium n. Off-by-one bases (`ways(0)=1` mixed with `ways(1)=1` inconsistently). Returning `previous` instead of `current` after the loop. Confusing this with min-cost or with unordered coin combinations.

## Follow-ups
Min cost climbing stairs. Steps of size in a given set. Modulo a prime for huge n. Count ways with exactly k steps.

## Related problems
House Robber (linear DP on an array), Fibonacci Number, Decode Ways (similar recurrence with validity checks), Unique Paths (2D path counting).
