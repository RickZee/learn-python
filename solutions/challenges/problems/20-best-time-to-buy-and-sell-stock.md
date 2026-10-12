# 20. Best Time to Buy and Sell Stock — walkthrough

## Recognize it
Prices for one stock over n days. You may buy once and sell once on a later day. Maximize `sell - buy`. If no profit is possible, return 0 (never return a negative "profit"). Look-alike: stock II (many non-overlapping trades). Another look-alike: stock with cooldown or transaction fee—same scan family, more state.

## Brute force
Try every pair of days `(i, j)` with `i < j` and track `max(prices[j] - prices[i])`, floored at 0. That is O(n²) time and O(1) space. For n = 1e5 it is too slow.

## Key insight
As you scan left to right, the best sell on day j uses the minimum price on days `0..j-1` (or j if you only update min). Track `lowest` so far and `best` gain `price - lowest`. You never need past prices after updating those two scalars.

## Algorithm
1. Set `lowest = None`, `best = 0`.
2. For each `price` in `prices`:
   - If `lowest` is `None` or `price < lowest`, set `lowest = price`.
   - Else if `price - lowest > best`, set `best = price - lowest`.
3. Return `best`.

(Equivalently: always update `lowest = min(lowest, price)` after seeding, and `best = max(best, price - lowest)`—careful that buying and selling on the same day yields 0, which is fine.)

## Trace
`prices = [7, 1, 5, 3, 6, 4]`.

| price | lowest | best |
|---|---|---|
| 7 | 7 | 0 |
| 1 | 1 | 0 |
| 5 | 1 | 4 |
| 3 | 1 | 4 |
| 6 | 1 | 5 |
| 4 | 1 | 5 |

Buy at 1, sell at 6 → profit 5. Strictly decreasing `[7,6,4,3,1]` keeps `best = 0`.

## Complexity
One pass: O(n) time, O(1) space. Better than O(n²) pairs when n grows. Kadane-style on day-to-day deltas (`max subarray of price[i]-price[i-1]`) is another O(n) view of the same one-buy-one-sell optimum.

## Edge cases
Empty or single-day prices → 0. Strictly decreasing → 0. Best buy at index 0 or best sell at the last day—both covered by the scan. Equal min appearing twice: either works. Integer prices; floats would need care with equality but are uncommon here.

## Alternatives and trade-offs
Pairwise brute force is the clarity baseline. Delta + Kadane connects this to maximum subarray. Segment trees or sparse tables for range min queries are overkill for one global min-so-far. For at-most-k transactions you need DP with more states; do not stretch this two-variable scan to k > 1 without new structure.

## Common bugs
Allowing sell before buy by scanning pairs without `i < j`. Returning a negative number when prices only fall. Updating `lowest` after computing profit in an order that uses today's price as both buy and a previous sell incorrectly (same-day trade is 0, which is OK, but using a future min is not). Tracking the max price without ensuring it comes after the min.

## Follow-ups
Unlimited transactions (sum every upward step). At most two transactions. Cooldown of one day after selling. Transaction fee per sell.

## Related problems
Maximum Subarray (Kadane), Best Time to Buy and Sell Stock II/III/IV, Trapping Rain Water (two-bound scans), House Robber (linear DP decisions).
