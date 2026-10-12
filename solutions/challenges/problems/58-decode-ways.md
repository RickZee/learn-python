# 58. Decode Ways — walkthrough

## Recognize it
Digits map A=1 … Z=26. Count ways to partition string `s` into valid codes. Look-alike: decode ways II (`*` wildcards). Another look-alike: climbing stairs (same recurrence shape when every digit is non-zero).

## Brute force
At each index, take one digit if valid, and/or two digits if 10–26, recurse. Without memo, Fibonacci-like branching with pruning still explodes on long digit strings of 1/2.

## Key insight
Let `prev1` = ways to decode `s[:i]`, `prev2` = ways for `s[:i-1]`. For position `i` (0-based ending index), a single digit `s[i] != '0'` adds `prev1` ways; a valid two-digit `s[i-1:i+1]` adds `prev2`. Leading zero → whole answer 0.

## Algorithm
1. If `s` empty or `s[0]=='0'`, return 0.
2. `prev2, prev1 = 1, 1` (empty prefix and first digit already validated).
3. For `i` from 1 to n-1:
   - `cur = 0`; if `s[i] != '0'`, `cur += prev1`; if `10 <= int(s[i-1:i+1]) <= 26`, `cur += prev2`.
   - `prev2, prev1 = prev1, cur`.
4. Return `prev1`.

## Trace
`s = "226"`.

| i | digit | one | two | cur | meaning |
|---|---|---|---|---|---|
| start | | | | prev1=1 | "2" → B |
| 1 | 2 | +1 | 22 ok +1 | 2 | "2,2" / "22" |
| 2 | 6 | +2 | 26 ok +1 | 3 | "2,2,6" / "22,6" / "2,26" |

Answer 3.

`s = "06"` → 0 at the start check.

## Complexity
O(n) time, O(1) extra space. DP array of size n+1 is the same time with clearer indexes for teaching.

## Edge cases
`"0"`, `"10"`, `"27"` (27 invalid as two-digit; 7 ok alone). Long runs of zeros (`"100"` → 0). `"110"` carefully: 1,1,0 only as 1,10. Empty string policies vary—here empty returns 0 via the guard.

## Alternatives and trade-offs
Explicit `dp[i]` array. DFS + cache. Mapping to climbing stairs only when no zeros. Prefer the rolling pair in timed challenges after drawing the array once.

## Common bugs
Accepting `'0'` as a single digit. Treating `05` as 5. Using `prev2`/`prev1` in the wrong order after update. Integer overflow in other languages (not Python).

## Follow-ups
Decode Ways II. Return one decoding. Number of ways with a custom alphabet.

## Related problems
Climbing Stairs, Decode Ways II, Word Break, Restore IP Addresses.
