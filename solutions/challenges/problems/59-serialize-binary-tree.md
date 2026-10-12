# 59. Serialize and Deserialize Binary Tree — walkthrough

## Recognize it
Turn a binary tree into a string and rebuild an identical tree (structure and values). Look-alike: serialize BST (can omit nulls with bounds). Another look-alike: codec for N-ary trees.

## Brute force
Any complete dump works if reversible—e.g. write every pointer as an id. The usual constraint is a clean BFS or DFS encoding with null markers so structure is unambiguous.

## Key insight
Level-order with explicit `null` placeholders preserves missing children. Join values with commas; parse by splitting. Empty tree ↔ empty string (or a single `null`, depending on convention). This repo's solution serializes a level-order value list already used by the harness.

## Algorithm
1. `serialize_level(values)`: `",".join("null" if v is None else str(v) for v in values)`.
2. `deserialize_level(data)`: if empty return `[]`; else split on comma and map `"null"` → `None`, else `int`.
3. Node-pointer challenge form: BFS queue writing `val` or `null`; deserialize creates nodes in the same order and wires children.

## Trace
Tree values `[1,2,3,None,None,4,5]`.

Serialize → `"1,2,3,null,null,4,5"`.

| token | meaning |
|---|---|
| 1 | root |
| 2,3 | children of 1 |
| null,null | children of 2 |
| 4,5 | children of 3 |

Deserialize rebuilds the same list; a Node builder would enqueue 1, attach 2 and 3, skip nulls under 2, attach 4 and 5 under 3.

## Complexity
O(n) time and O(n) space for n nodes (plus null markers in the string). Preorder with nulls is the same asymptotics; inorder alone cannot rebuild without BST constraints.

## Edge cases
Empty tree. Single node. Skewed left/right (many nulls on one side). Negative values—do not treat `"-1"` as null. Trailing nulls: some codecs trim them; keep them if your pair expects a full level dump.

## Alternatives and trade-offs
Preorder recursive codec (`val,left,right`) is shorter to code with Nodes. JSON of nested dicts is fine in production, not in whiteboard challenges. Bracket notation is harder to parse.

## Common bugs
Losing null markers so `[1,null,2]` and `[1,2]` collide. Splitting on comma without handling empties. Using `eval`. Forgetting to skip null nodes when assigning children in BFS deserialize.

## Follow-ups
Serialize N-ary tree. Compact BST serialization. Serialize with only preorder values for BST.

## Related problems
Serialize and Deserialize BST, Clone Graph, Construct from Preorder and Inorder, Flatten Binary Tree to Linked List.
