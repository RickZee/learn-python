# 05. Container With Most Water — walkthrough

## Recognize it
Two vertical lines form a container; area is `min(height[l], height[r]) * (r - l)`. Maximize over pairs. Two pointers from the ends beat checking every pair. Look-alike: Trapping Rain Water (many bars, different formula).

## Brute force
Every pair of indexes: O(n²).

## Key insight
The wide container starts at the ends. The only way to beat the current area is to find a taller short side, so move the pointer at the shorter line inward.

## Algorithm
1. `left, right = 0, n-1`, `best = 0`.
2. While `left < right`, update `best` with the current area.
3. If `height[left] < height[right]`, `left += 1`, else `right -= 1`.
4. Return `best`.

## Trace
`height = [1,8,6,2,5,4,8,3,7]`.

| left | right | area | move |
|---|---|---|---|
| 0 | 8 | min(1,7)*8=8 | left |
| 1 | 8 | min(8,7)*7=49 | right |
| ... | ... | ... | ... |

Best stays 49.

## Complexity
O(n) time, O(1) space.

## Edge cases
Two lines only. Strictly decreasing heights. Zeros. n < 2 → 0 if you guard.

## Alternatives and trade-offs
 Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain as you scan. Walk an empty input and a duplicate-heavy input after the happy path. If time remains, compare trade-offs and name the pattern for transfer to related prompts.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain as you scan. Walk an empty input and a duplicate-heavy input after the happy path. If time remains, compare trade-offs and name the pattern for transfer to related prompts.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain as you scan. Walk an empty input and a duplicate-heavy input after the happy path. If time remains, compare trade-offs and name the pattern for transfer to related prompts. Brute force is fine for tiny n. Two pointers need a short proof: moving the taller side cannot help while width shrinks.

## Common bugs
Moving the taller line. Off-by-one on width (`right - left`). Using max instead of min for height.

## Follow-ups
Trapping Rain Water. Maximize area with at least k width.

## Related problems
Two Sum II, Trapping Rain Water, 3Sum (also two pointers after a sort).
