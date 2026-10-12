# 50. Redundant Connection — walkthrough

## Recognize it
Undirected graph that started as a tree plus one extra edge. Return that redundant edge (the one that closes a cycle); if several appear in the list, return the last one in input order that creates a cycle when edges are added left to right. Look-alike: critical connections / bridges (edges whose removal disconnects). Another look-alike: redundant connection II (directed).

## Brute force
For each edge, temporarily remove it and DFS/BFS to see if the graph stays connected—O(E·(V+E)). Works but heavier than union-find for this "exactly one cycle" setup.

## Key insight
Add edges one by one with union-find. If the two endpoints are already in the same component, that edge is redundant—return it immediately. Path compression keeps finds cheap.

## Algorithm
1. `parent = {}`. `find(x)` with path compression; `setdefault` so unseen nodes are their own parents.
2. For each edge `[a, b]`:
   - If `find(a) == find(b)`, return `[a, b]`.
   - Else union: `parent[find(b)] = find(a)`.
3. Return `[]` if none (should not happen on valid inputs).

## Trace
Edges `[[1,2],[1,3],[2,3]]`.

| edge | find(a), find(b) | action |
|---|---|---|
| 1-2 | 1, 2 | union → parent[2]=1 |
| 1-3 | 1, 3 | union → parent[3]=1 |
| 2-3 | 1, 1 | same → return [2,3] |

## Complexity
Nearly O(E · α(V)) with path compression (and union by rank if you add it). Space O(V). Far better than rebuilding connectivity per edge.

## Edge cases
Triangle is the smallest cycle. Redundant edge in the middle of a longer list—later edges are not processed once you return. Nodes numbered from 1..n with some never appearing until late. Self-loop would also be redundant (rare in prompts).

## Alternatives and trade-offs
DFS with parent tracking to find any back edge—must carefully return the last input edge on the cycle, which union-find does naturally by insertion order. Kruskal without stopping also builds a spanning tree and skips the bad edge.

## Common bugs
Union before the same-component check. Returning the first edge of the cycle in tree order instead of the input edge that closed it. Forgetting path compression so deep trees slow finds. Using rank incorrectly and breaking parents.

## Follow-ups
Redundant Connection II (directed with possible two parents). Number of provinces. Accounts merge (union by email).

## Related problems
Number of Connected Components, Graph Valid Tree, Regions Cut by Slashes, Smallest String With Swaps.
