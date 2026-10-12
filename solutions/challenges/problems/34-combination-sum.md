# 34. Combination Sum — walkthrough

## Recognize it
Given distinct positive candidates and a target, list every combination that sums to target. You may reuse the same candidate unlimited times. Order within a combination does not create duplicates—`[2,2,3]` counts once, not all permutations. Look-alike: combination sum II (candidates may duplicate; each index once). Another look-alike: coin change (min count only, not the lists).

## Brute force
Generate all multisets / recurse with every candidate at every step including permutations, then unique the sorted tuples. Explosion of duplicates and wasted work. Need ordered search that never revisits a lexicographically earlier choice.

## Key insight
Sort candidates. Backtrack with a `start` index: from the current position you may reuse the same index (stay) to take another copy, or move forward to larger values. Skipping earlier indexes prevents permutations of the same multiset. Prune when the next candidate exceeds the remaining sum.

## Algorithm
1. Sort `candidates` into `ordered`.
2. `walk(start, remain)`:
   - If `remain == 0`, record a copy of `choice`.
   - For `index` from `start` to end:
     - If `ordered[index] > remain`, break.
     - Append, recurse `walk(index, remain - value)` (reuse allowed), pop.
3. Start with `walk(0, target)`; return `answers`.

## Trace
`candidates = [2,3,6,7]`, `target = 7`.

| choice | remain | action |
|---|---|---|
| [] | 7 | try 2 |
| [2] | 5 | try 2 |
| [2,2] | 3 | try 2 |
| [2,2,2] | 1 | 2>1 break; 3>1 … fail |
| [2,2,3] | 0 | record [2,2,3] |
| [2,3] … | | eventually [2,2,3] done |
| [3] | 4 | … no valid |
| [7] | 0 | record [7] |

Answers `[[2,2,3],[7]]` (plus any other valid—here those two).

## Complexity
Output-sensitive exponential: branching limited by target / smallest coin. Time roughly O(n^{T/min}) in the worst case; space O(target / min) for the depth of `choice` plus the size of the answer list. DP that stores all combinations per sum uses more memory up front.

## Edge cases
`target = 0` → `[[]]` if allowed; usually target ≥ 1. Single candidate that divides target → one combination of repeats. Candidate larger than target → skipped by prune. Empty candidates → `[]`.

## Alternatives and trade-offs
DP: `dp[s]` lists combos summing to s—can be heavy on memory. Recursing with `index+1` only (no reuse) solves the 0/1 variant. Generating permutations then sorting unique is the approach to reject in timed challenges.

## Common bugs
Calling `walk(index + 1, …)` when reuse is allowed—misses `[2,2,3]`. Not sorting / not using `start`, emitting permutations as separate answers. Mutating the same `choice` list into `answers` without `.copy()`. Forgetting to pop after recurse.

## Follow-ups
Combination Sum II (skip duplicates). Combination Sum III (k numbers from 1..9). Factor combinations. Coin change II (count only).

## Related problems
Combination Sum II/III, Coin Change, Generate Parentheses (backtracking structure), Permutations.
