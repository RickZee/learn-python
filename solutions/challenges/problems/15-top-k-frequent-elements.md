# 15. Top K Frequent Elements — walkthrough

## Recognize it
Given an integer array and an integer k, return the k distinct values that appear most often. Order of the answer usually does not matter. Ties are rare in graded cases; if they appear, any valid set of k is often accepted unless the prompt freezes a rule. Look-alike: "kth largest element" ranks by value, not by frequency. Another look-alike: return the mode only (k = 1) or sort the whole array by frequency.

## Brute force
Count frequencies with a hash map (one pass), then sort all unique values by count descending and take the first k. Counting is O(n). Sorting u unique keys is O(u log u). For n up to 1e5 and u ≈ n this is acceptable in many contests, but timed challenges often push for better than full sort when k ≪ u—heap or bucket selection.

## Key insight
Frequency counting is unavoidable in the general case. After you have counts, you only need the top k keys, not a full ordering of every unique value. `Counter.most_common(k)` (heap under the hood) or bucket sort by frequency (index = count, list of values) both avoid sorting all uniques when that would dominate.

## Algorithm
1. Build `counts = Counter(nums)` so each distinct value maps to its frequency.
2. Ask for the k most common `(value, count)` pairs.
3. Return just the values: `[value for value, _ in counts.most_common(k)]`.

Bucket variant (also linear):
1. After counting, create `buckets` as an array of lists of length `n+1`.
2. Append each value into `buckets[count]`.
3. Scan buckets from high count to low, collecting values until you have k of them.

## Trace
`nums = [1,1,1,2,2,3]`, `k = 2`.

| value | count |
|---|---|
| 1 | 3 |
| 2 | 2 |
| 3 | 1 |

`most_common(2)` yields `(1,3)` then `(2,2)` → answer `[1,2]` (order among equals may vary by implementation; here frequencies differ).

Bucket view: index 3 holds `[1]`, index 2 holds `[2]`, index 1 holds `[3]`. Scanning down from 3 picks 1 then 2 and stops.

## Complexity
Counting: O(n) time and O(u) space. `most_common(k)` is O(u log k) with a heap of size k (CPython), which is fine when k is small. Pure bucket selection is O(n) time and O(n) space for the buckets. Full sort of uniques is O(u log u)—worse when u is large and k is tiny.

## Edge cases
`k` equals the number of unique values → return every unique. All elements identical → that one value if k = 1. Single-element array. Negative numbers and zeros hash fine as dict keys. Empty `nums` is usually out of contract when k ≥ 1.

## Alternatives and trade-offs
Full sort by frequency is shortest to explain and fine for small u. Heap of size k is the standard "top-k" story. Buckets exploit that counts lie in `1..n`, giving true linear time; the code is a bit longer. Quickselect on unique keys by count is average O(u) but awkward with hash maps and rarely worth it in a timed challenge unless asked.

## Common bugs
Sorting the values themselves instead of sorting by their counts. Returning the counts instead of the values. Off-by-one when building buckets of size n instead of n+1 (a value appearing n times needs index n). Assuming the answer must be sorted by value when the prompt only cares about membership.

## Follow-ups
Top k frequent words (tie-break by lexicographic order). Streaming data where you cannot store all counts (approximate sketches). Return elements with frequency exactly k.

## Related problems
Kth Largest Element (selection/heap on values), Group Anagrams (hashing into buckets), Sort Characters By Frequency, Word Frequency maps.
