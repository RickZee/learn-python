# 19. Coin Change — walkthrough

## Recognize it
You have coin denominations and a target amount. Return the fewest coins that sum to that amount, or -1 if impossible. Order does not matter; unlimited supply of each coin. Amount 0 needs 0 coins. Look-alike: coin change II (count combinations, not min coins). Another look-alike: 0/1 knapsack where each coin may be used once.

## Brute force
Recurse on the remaining amount: try every coin ≤ remaining, take `1 + min` over those branches. Without memoization this explores an exponential tree of multisets. Even with pruning it is too slow for amount in the thousands and a handful of denominations.

## Key insight
Let `fewest[x]` be the minimum coins to make sum x. Then `fewest[x] = min over coins c ≤ x of fewest[x-c] + 1`, with `fewest[0] = 0`. Impossible amounts stay at a sentinel larger than any real answer (for example `amount + 1`). Filling by increasing x, or by coin-outer loops that update ascending x, reuses smaller subproblems.

## Algorithm
1. Create `fewest = [0] + [amount + 1] * amount` (sentinel means "not yet possible").
2. For each `coin` in `coins`:
   - For `value` from `coin` to `amount` inclusive:
     - `fewest[value] = min(fewest[value], fewest[value - coin] + 1)`.
3. If `fewest[amount] <= amount`, return it; else return `-1`.

The outer-coin loop yields the unbounded-knapsack order that allows reusing the same coin many times while scanning upward.

## Trace
`coins = [1, 2, 5]`, `amount = 11`.

After processing all coins (sketch of final table):

| amount x | fewest[x] | example combo |
|---|---|---|
| 0 | 0 | — |
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 3 | 2 | 1+2 |
| 4 | 2 | 2+2 |
| 5 | 1 | 5 |
| 6 | 2 | 5+1 |
| 11 | 3 | 5+5+1 |

Return 3. If coins were `[2]` and amount `3`, every odd slot stays at the sentinel → `-1`.

## Complexity
Time O(amount · len(coins)): each coin touches each value once. Space O(amount) for the table. BFS by remaining amount also finds the minimum number of coins (shortest path in the additive graph) in O(amount · len(coins)) worst case with a queue and visited set—same class, different shape.

## Edge cases
`amount = 0` → 0 without looking at coins. Empty `coins` and positive amount → `-1`. Coin larger than amount is skipped naturally. Single coin that divides amount → `amount // coin`. Sentinel must be `> amount` so a real answer of `amount` ones still wins over "impossible."

## Alternatives and trade-offs
Top-down `@cache` on remaining amount is easy to write and only fills reachable states. BFS layers correspond to adding one coin—nice if you think in graphs. Greedy (always take largest coin) is wrong for many systems (for example coins `[1, 3, 4]` and amount `6` wants two 3s, not 4+1+1). Do not greedy unless denominations are canonical (like US coins under usual sets)—prove or avoid.

## Common bugs
Initializing `fewest[0]` to the sentinel so nothing can grow from zero. Using 0 as "impossible," which makes unreachable amounts look free. Mixing combination-count DP (sum ways) with min-coin DP (take min). Iterating `value` downward with a 0/1 mindset when coins are unbounded, or the reverse mistake when each coin is unique.

## Follow-ups
Coin Change II (number of combinations). Minimum coins with limited quantities. Largest amount that cannot be formed (Frobenius for two coprime coins). Reconstruct one optimal multiset, not only the count.

## Related problems
Combination Sum (list the combinations), Perfect Squares (min count with square coins), Climbing Stairs (count ways), Knapsack variants.
