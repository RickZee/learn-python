# 02. Group Anagrams — walkthrough

## Recognize it
Words that share the same letter multiset belong together. Sorting each word, or counting letters, produces a hashable key for a dict of lists. Look-alike: grouping by first letter only is not anagram grouping.

## Brute force
For each word, compare its sorted form to every other word. O(n² * k log k) for n words of length k.

## Key insight
Anagrams share a canonical key: `tuple(sorted(word))` or a 26-length count tuple. Bucket words by that key.

## Algorithm
1. Create `groups = {}`.
2. For each word, key = `tuple(sorted(word))`.
3. Append the word to `groups.setdefault(key, [])`.
4. Return `list(groups.values())`.

## Trace
Input `["eat","tea","tan","ate","nat","bat"]`.

| word | key | buckets |
|---|---|---|
| eat | aet | {aet:[eat]} |
| tea | aet | {aet:[eat,tea]} |
| tan | ant | adds ant |
| ate | aet | aet grows |
| nat | ant | ant grows |
| bat | abt | new |

## Complexity
O(n * k log k) with sorting keys, or O(n * k) with counts. Space O(n * k) for the buckets.

## Edge cases
Empty list → `[]`. Single word → one group. Empty string words group together. Unicode beyond a–z needs a count dict instead of 26 slots.

## Alternatives and trade-offs
 In a timed challenge, narrate the brute force first so the prompt sees you can estimate cost before optimizing. State invariants out loud while you code. After the happy path, walk an empty or single-element case and one duplicate case. If time remains, compare the space trade-off of hashing versus sorting. Name the pattern so the prompt can map this problem to others you have practiced.  In a timed challenge, narrate the brute force first so the prompt sees you can estimate cost before optimizing. State invariants out loud while you code. After the happy path, walk an empty or single-element case and one duplicate case. If time remains, compare the space trade-off of hashing versus sorting. Name the pattern so the prompt can map this problem to others you have practiced. Count array as key is faster for lowercase English. Sorting is shorter to code. Returning groups in any order is fine unless the prompt freezes order.

## Common bugs
Using `sorted(word)` (a list) as a dict key → TypeError. Mutating the key. Comparing with `==` on unsorted strings.

## Follow-ups
Return group sizes only. Stream words. Case folding.

## Related problems
Valid Anagram, Top K Frequent Elements (hashing), Group shifted strings.
