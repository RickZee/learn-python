# 23. Daily Temperatures — walkthrough

## Recognize it
For each day, how many days until a strictly warmer temperature appears? If none, answer 0 for that day. Output an array of the same length. Look-alike: next greater element in a circular array (wrap-around). Another look-alike: stock span (counts consecutive less-or-equal days backward), which also uses a monotonic stack but aggregates differently.

## Brute force
From each index i, scan j = i+1..n-1 until `temperatures[j] > temperatures[i]`, then store `j - i`. Worst case O(n²) when the array is non-increasing. Too slow for large n.

## Key insight
Maintain a stack of indexes whose temperatures are waiting for a warmer day, kept in decreasing temperature order (monotonic decreasing stack). When today's temperature is warmer than the stack top, you have found the next warmer day for that earlier index—pop and fill `answer[earlier] = today - earlier`. Each index is pushed and popped at most once.

## Algorithm
1. Allocate `answer = [0] * n` (zeros already mean "no warmer day").
2. `stack = []` will hold indexes.
3. For `index, temperature` in enumerate(`temperatures`):
   - While `stack` is non-empty and `temperatures[stack[-1]] < temperature`:
     - `earlier = stack.pop()`
     - `answer[earlier] = index - earlier`
   - Push `index` onto `stack`.
4. Return `answer`. Leftover indexes in the stack keep 0.

## Trace
`temperatures = [73, 74, 75, 71, 69, 72, 76, 73]`.

| index | temp | stack after | answer updates |
|---|---|---|---|
| 0 | 73 | [0] | |
| 1 | 74 | [1] | answer[0]=1 |
| 2 | 75 | [2] | answer[1]=1 |
| 3 | 71 | [2,3] | |
| 4 | 69 | [2,3,4] | |
| 5 | 72 | [2,5] | answer[4]=1, answer[3]=2 |
| 6 | 76 | [6] | answer[5]=1, answer[2]=4 |
| 7 | 73 | [6,7] | |

Final answer `[1,1,4,2,1,1,0,0]`.

## Complexity
Each index enters and leaves the stack at most once: O(n) time. Stack holds at most n indexes: O(n) space. Beats O(n²) forward scans on descending weather.

## Edge cases
Strictly decreasing → all zeros. Strictly increasing → all ones except last zero. Single day → `[0]`. Equal temperatures are not "warmer"—use strict `<` when comparing, so equals stay on the stack. Plateaus of the same temp wait for a truly higher day.

## Alternatives and trade-offs
Forward scan from each day is fine for tiny n. Next-greater via sparse table / RMQ is overkill. Computing from the right with a stack of values (not indexes) loses the distance unless you also store indexes—always store indexes when the answer is a gap. Circular next-greater needs a second pass or doubled array.

## Common bugs
Storing temperatures on the stack instead of indexes, then you cannot compute `index - earlier`. Using `<=` so equal temps wrongly resolve. Forgetting to initialize the answer with zeros for days that never pop. Popping without a while loop so only one waiting day resolves when today warms several.

## Follow-ups
Next greater element I/II. Online stock span. Largest rectangle in histogram (monotonic stack for spans). Daily temperatures with "at least k degrees warmer."

## Related problems
Next Greater Element, Online Stock Span, Largest Rectangle in Histogram, Trapping Rain Water (stack variant).
