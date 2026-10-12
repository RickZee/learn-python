# 66. Single Number — walkthrough

## Recognize it
Every value appears twice except one; find the singleton in linear time and constant extra space. Look-alike: single number II (triples). Another look-alike: find the duplicate (pigeonhole, different constraints).

## Brute force
Sort and scan for a value not matching its neighbor: O(n log n). Hash set: add on first see, remove on second—O(n) time but O(n) space, violating the constant-space ask.

## Key insight
XOR is commutative and associative; `x^x = 0` and `x^0 = x`. XOR all numbers: pairs cancel to 0, the singleton remains. Think of each bit column independently—every duplicated value contributes an even count of 1s that cancel, leaving only bits from the singleton.

## Algorithm
1. `acc = 0`.
2. For each value: `acc ^= value`.
3. Return `acc`.

## Trace
`nums = [4, 1, 2, 1, 2]`.

| value | acc after | note |
|---|---|---|
| 4 | 4 | first sight of 4 |
| 1 | 4^1 = 5 | |
| 2 | 5^2 = 7 | |
| 1 | 7^1 = 6 | first 1 cancelled |
| 2 | 6^2 = 4 | second 2 cancelled |

Answer 4. Pairs of 1 and of 2 cancelled; 4 remained.

## Complexity
O(n) time, O(1) space. Hashing is O(n) space; sorting is slower. Bit tricks win exactly because of the twice-vs-once constraint—if the frequencies were different, plain XOR would not isolate the answer.

## Edge cases
Single-element array → that element. Negatives (two's complement XOR still works in Python ints). Zero as the singleton. Large values—Python ints unbounded, still fine. Empty input is out of scope when the prompt guarantees one singleton.

## Alternatives and trade-offs
Math: `2*sum(set(nums)) - sum(nums)` uses a set (extra space). Sorting is simple for tiny n. For "everyone appears thrice except one," you need bit counts mod 3, not plain XOR. Prefer XOR when the prompt names the O(1)-space constraint up front.

## Common bugs
Using `+` or `|` instead of `^`. Starting `acc` at `nums[0]` and skipping it inconsistently. Assuming the singleton is positive. Hashing when the prompt insisted on O(1) space. Forgetting that XOR still works when the singleton sits in the middle of the array, not only at the ends.

## Follow-ups
Single Number II / III. Find missing number (XOR 0..n with the array). Missing two numbers.

## Related problems
Single Number II, Missing Number, Find the Duplicate Number, Counting Bits.
