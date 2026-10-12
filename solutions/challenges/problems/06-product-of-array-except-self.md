# 06. Product of Array Except Self — walkthrough

## Recognize it
Build an array where each entry is the product of all other entries, without division. Prefix and suffix products give every answer in two passes. Look-alike: using division by the total product fails when zeros appear and is often banned.

## Brute force
For each index, multiply every other value: O(n²).

## Key insight
`answer[i] = (product of left side) * (product of right side)`. Fill left products left-to-right, then multiply right products right-to-left.

## Algorithm
1. `answer = [1]*n`, `prefix = 1`.
2. For each i: `answer[i] = prefix`; `prefix *= nums[i]`.
3. `suffix = 1`; for i from n-1 down to 0: `answer[i] *= suffix`; `suffix *= nums[i]`.
4. Return `answer`.

## Trace
`nums = [1,2,3,4]`.

| pass | answer |
|---|---|
| after prefix | [1,1,2,6] |
| after suffix | [24,12,8,6] |

## Complexity
O(n) time, O(1) extra memory beyond the answer array.

## Edge cases
One zero → that index gets the product of the rest; others get 0. Two zeros → all zeros. Single element → `[1]` by the empty-product convention if allowed. Negatives fine.

## Alternatives and trade-offs
 Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain as you scan. Walk an empty input and a duplicate-heavy input after the happy path. If time remains, compare trade-offs and name the pattern for transfer to related prompts.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain as you scan. Walk an empty input and a duplicate-heavy input after the happy path. If time remains, compare trade-offs and name the pattern for transfer to related prompts.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain as you scan. Walk an empty input and a duplicate-heavy input after the happy path. If time remains, compare trade-offs and name the pattern for transfer to related prompts. Division by total product is shorter but banned or fragile with zeros. Two explicit arrays for left/right use O(n) space and are easier to explain.

## Common bugs
Including `nums[i]` in its own product. Updating `prefix` before writing `answer[i]`. Forgetting the suffix pass.

## Follow-ups
Allow division. Stream updates. Modular product.

## Related problems
Trapping Rain Water (prefix/suffix ideas), Maximum Subarray (running state), Product except self with k exclusions.
