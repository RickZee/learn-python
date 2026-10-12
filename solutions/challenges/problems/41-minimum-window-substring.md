# 41. Minimum Window Substring — walkthrough

## Recognize it
Find the shortest substring of `s` that contains every character of `t` (with multiplicity). Look-alike: longest substring with at most k distinct (different shrink rule). Another look-alike: permutation in string (window of fixed length `|t|`).

## Brute force
For every pair `(left, right)`, test whether `s[left:right+1]` covers `t` via counts. That is O(n² · alphabet) and too slow for long `s`.

## Key insight
Grow a right pointer until the window satisfies all of `t`, then advance left as far as you can while still covering—each shrink may update the best answer. A deficit counter (`missing`) plus a need map makes "still covers" O(1) per move: when you add a needed character, `missing` drops; when you remove one that goes positive in need, `missing` rises.

## Algorithm
1. `need = Counter(t)`, `missing = len(t)`, `best = ""`, `left = 0`.
2. For `right, ch` in enumerate(`s`):
   - If `need[ch] > 0`, decrement `missing`. Always `need[ch] -= 1` (extras go negative).
   - While `missing == 0`: update `best` if this window is shorter; then put `s[left]` back into `need`; if that makes `need[s[left]] > 0`, increment `missing`; `left += 1`.
3. Return `best`.

## Trace
`s = "ADOBECODEBANC"`, `t = "ABC"`.

| right | window after grow | shrink to | best |
|---|---|---|---|
| … reaches C at 5 | ADOBEC | — | ADOBEC |
| … | … | shrink while covered | DOBEC / OBEC / BEC (still need A later) |
| C at 10 | CODEBA… | … | BANC length 4 wins |
| final | — | — | `"BANC"` |

Concrete mid state: when the window first covers at index 5 (`ADOBEC`), shrinking can drop `A` and `D` until `BEC` loses coverage. Later `BANC` is shorter than `ADOBEC`.

## Complexity
Each index moves left and right at most once: O(len(s) + len(t)) time. Need map is O(alphabet) or O(|t|). Better than O(n²) substring checks.

## Edge cases
Empty `s` or `t` → `""`. `t` longer than `s` → `""`. Multiple copies in `t` (`"AABC"`) require that many A's. Whole string is the only cover. Several windows of equal length—any shortest is fine unless the prompt picks the first.

## Alternatives and trade-offs
Binary search on window length + feasibility scan is O(n log n) and clumsier. Filtering `s` to only characters that appear in `t` can speed sparse alphabetic cases. Two maps (window vs need) is clearer for some people than the signed-need trick.

## Common bugs
Treating two required copies of a letter as one. Updating `best` with a longer window. Moving `left` past the optimum without recording. Forgetting extras (`need` negative) so shrink breaks too early. Building `best` with indexes off by one.

## Follow-ups
Smallest range covering elements from k lists. Substring with concatenation of all words. Minimum window that covers a subsequence (harder).

## Related problems
Longest Substring Without Repeating Characters, Find All Anagrams, Permutation in String, Sliding Window Maximum.
