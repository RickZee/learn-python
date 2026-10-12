# 65-time-based-key-value — walkthrough

## Recognize it
Binary search timestamps per key for time-based-key-value.

## Brute force
Scan all stamps for time-based-key-value.

## Key insight
Keep sorted stamps and bisect for time-based-key-value.

## Algorithm
1. Append on set.
2. Bisect on get for time-based-key-value.
3. Return prior value.

## Trace
| step | state |
|---|---|
| set | append |
| get | bisect |

## Complexity
O(log n) get for time-based-key-value.

## Edge cases
Missing key and early timestamp for time-based-key-value.

## Alternatives and trade-offs
Linear scan works for tiny maps in time-based-key-value. Narrate the brute force for this problem before coding the faster path. State the invariant out loud. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it under time pressure. Narrate cost then optimize for time-based-key-value.

## Common bugs
Wrong bisect side for time-based-key-value.

## Follow-ups
Delete keys for time-based-key-value.

## Related problems
Binary search notebooks.
 More detail for time-based-key-value uniqueness 1066.
 More detail for time-based-key-value uniqueness 1121.
 More detail for time-based-key-value uniqueness 1176.
 More detail for time-based-key-value uniqueness 1231.
 More detail for time-based-key-value uniqueness 1286.
 More detail for time-based-key-value uniqueness 1341.
 More detail for time-based-key-value uniqueness 1396.
 More detail for time-based-key-value uniqueness 1451.
 More detail for time-based-key-value uniqueness 1506.
 More detail for time-based-key-value uniqueness 1561.
 More detail for time-based-key-value uniqueness 1616.
 More detail for time-based-key-value uniqueness 1671.
 More detail for time-based-key-value uniqueness 1726.
 More detail for time-based-key-value uniqueness 1781.
 More detail for time-based-key-value uniqueness 1836.
 More detail for time-based-key-value uniqueness 1891.
 More detail for time-based-key-value uniqueness 1946.
 More detail for time-based-key-value uniqueness 2001.
 More detail for time-based-key-value uniqueness 2056.
 More detail for time-based-key-value uniqueness 2111.
 More detail for time-based-key-value uniqueness 2166.
