# 60. Reorder List — walkthrough

## Recognize it
Reorder `L0→L1→…→Ln` into `L0→Ln→L1→Ln-1→…` in place on a linked list. Look-alike: reverse linked list (one piece of the puzzle). Another look-alike: reorder array by interleaving halves (same idea on indexes).

## Brute force
Copy values to an array, build the interleaved order, rewrite the list—O(n) time and O(n) space. Allowed if the prompt does not demand O(1) extra space; the classic follow-up forbids the array.

## Key insight
Three steps on Nodes: (1) find midpoint with slow/fast; (2) reverse the second half; (3) merge by alternating nodes from first half and reversed second. This repo mirrors that on a value list: split at mid, reverse the right piece, zip.

## Algorithm
1. If length ≤ 2, return a copy.
2. `mid = (len+1)//2`; `left = values[:mid]`; `right = reversed(values[mid:])`.
3. Interleave: append from left, then from right while right remains.
4. Return the new list (Node version mutates pointers instead of building a new array).

## Trace
`values = [1,2,3,4]`.

| step | result |
|---|---|
| mid=2 | left=[1,2], right=[4,3] |
| zip | 1,4,2,3 |

`[1,2,3,4,5]` → left `[1,2,3]`, right `[5,4]` → `[1,5,2,4,3]`.

| index | left | right | out growth |
|---|---|---|---|
| 0 | 1 | 5 | [1,5] |
| 1 | 2 | 4 | [1,5,2,4] |
| 2 | 3 | — | [1,5,2,4,3] |

## Complexity
O(n) time. Value-list form uses O(n) space; Node form uses O(1) extra besides the reverse. Finding mid is O(n), reverse O(n), merge O(n).

## Edge cases
0–2 nodes: unchanged. Odd length: middle stays before the end of the first half. Already alternating shape. Single pass mistakes that lose the mid node.

## Alternatives and trade-offs
Array of pointers then reconnect—clearer, O(n) space. Recursion that pops from the end uses O(n) stack. Prefer the three-phase Node method in timed challenges when O(1) space is required.

## Common bugs
Off-by-one midpoint so halves overlap or leave a gap. Forgetting to cut `slow.next = None` before reverse (cycles). Merging without alternating. Reversing the whole list instead of the second half.

## Follow-ups
Reorder in other patterns (k-way). Palindrome list check (reverse second half shared technique). Zip two lists.

## Related problems
Reverse Linked List, Palindrome Linked List, Middle of the Linked List, Reverse Nodes in k-Group.
