# 03. Longest Substring Without Repeating Characters — walkthrough

## Recognize it
You want the longest contiguous substring with a uniqueness constraint. That is a sliding window with a map or set of characters inside the window. Look-alike: longest subsequence (not contiguous) is a different problem.

## Brute force
For every start index, grow end until a repeat appears. O(n²) checks with a set rebuilt each time.

## Key insight
As `end` advances, the window start only moves forward. Store the last index of each character; when a repeat falls inside the window, jump `start` to `last[c] + 1`.

## Algorithm
1. `last = {}`, `start = 0`, `best = 0`.
2. For each index `i` and character `c`: if `c` was seen at or after `start`, set `start = last[c] + 1`.
3. Update `last[c] = i` and `best = max(best, i - start + 1)`.
4. Return `best`.

## Trace
`s = "abba"`.

| i | c | start | last | best |
|---|---|---|---|---|
| 0 | a | 0 | a0 | 1 |
| 1 | b | 0 | b1 | 2 |
| 2 | b | 2 | b2 | 2 |
| 3 | a | 2 | a3 | 2 |

## Complexity
Each index enters and leaves the window once: O(n) time. Space O(min(n, alphabet)).

## Edge cases
Empty string → 0. All unique → n. All same character → 1. Single character → 1.

## Alternatives and trade-offs
A set with explicit shrink loops is clearer but similar asymptotically. Regex or DP over all substrings is slower. Window is the expected challenge answer.

## Common bugs
Moving `start` backward. Forgetting to update `last` after adjusting start. Using length `i - start` without `+ 1`.

## Follow-ups
Return the substring, not only the length — keep the start index when you update `best`. At most k distinct characters is a different window: track counts and shrink while the distinct count exceeds k. Streaming characters works the same way if you only need the length; recovering the string needs a buffer of the current window. Narrate the O(n²) scan and its cost before coding the O(n) jump. State the invariant: every character in `[start, i]` is unique. Walk an empty input and a duplicate-heavy input after the happy path. Name the pattern so it transfers to related prompts.

## Related problems
Longest Repeating Character Replacement, Minimum Window Substring, Subarray Sum Equals K (prefix, not window).
