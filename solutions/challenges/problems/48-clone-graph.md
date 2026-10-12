# 48. Clone Graph — walkthrough

## Recognize it
Deep-copy an undirected connected graph given as adjacency lists (or Node objects with neighbor lists). The clone must have new nodes and the same connectivity, with no shared object identity. Look-alike: clone a tree (no cycles—always one parent). Another look-alike: serialize/deserialize graph.

## Brute force
There is no slower correct "pair scan"—you must visit every node and edge. The failure mode is cloning a neighbor twice when a cycle or cross edge reappears, or returning the original nodes by accident.

## Key insight
Map each original node to its clone. When you first see a node, create its clone and recurse/iterate neighbors; when you see a node already in the map, reuse the clone. That breaks cycles and preserves sharing.

## Algorithm
(Value form used in this repo: adjacency list `adj` where index is the node id.)

1. Return `[list(row) for row in adj]` — each neighbor list is a new list so mutating the clone's edges does not touch the original's lists.
2. For a Node-pointer API (Node-pointer classic):
   - `cloned = {}`.
   - DFS/`BFS`: if `node` in `cloned`, return it; else create `Node(node.val)`, store it, then append `walk(nei)` for each neighbor.
   - Return `cloned[start]`.

## Trace
Graph: 1—2—3—1 (triangle) plus 4 attached to 1. Adjacency values `[[2,3,4],[1,3],[1,2],[1]]` (1-index shifted in prompts often).

| visit | map | action |
|---|---|---|
| 1 | 1→1' | create 1', explore neighbors |
| 2 | +2' | create 2', link 1'↔2' |
| 3 | +3' | create 3'; link; 3→1 already mapped → link 3' to 1' |
| 4 | +4' | create 4', link to 1' |

No second copy of 1' when the cycle closes.

## Complexity
Touch each node and edge once: O(V+E) time. Map and new nodes: O(V+E) space. Copying only the outer list of adj without copying rows would alias neighbor lists—wrong for mutation tests.

## Edge cases
Empty graph / null start → null. Single node with no neighbors. Single node with a self-loop (rare in prompts). Disconnected graphs if the API gives one component only—clone from the given start.

## Alternatives and trade-offs
BFS with a queue instead of DFS—same map. Serialize to adj dict then rebuild. For this repo's value-only stub, a deep copy of the lists is enough; in timed challenges, insist on the Node map so you prove cycle handling.

## Common bugs
`cloned[node] = Node(node.val)` after already recursing neighbors (infinite loop on cycles). Appending the original neighbor instead of the clone. Shallow copy of adj (`adj.copy()` still shares inner lists). Forgetting nodes unreachable if multiple components are in scope.

## Follow-ups
Clone graph with weights. Copy list with random pointer (same map idea). Deep copy of a nested dict structure.

## Related problems
Copy List with Random Pointer, Serialize and Deserialize Binary Tree, Course Schedule (graph walk without cloning).
