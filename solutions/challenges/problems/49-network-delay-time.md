# 49. Network Delay Time — walkthrough

## Recognize it
Directed weighted edges `(u, v, w)`; signal starts at node `k`. Return how long until every node has received the signal—the maximum shortest-path distance from `k`—or `-1` if some node is unreachable. Look-alike: cheapest flights within k stops (limit hops). Another look-alike: unweighted BFS (all weights 1).

## Brute force
Bellman-Ford for `|V|-1` rounds over all edges: O(V·E). Correct on this non-negative setting but slower than Dijkstra when E is large. DFS exploring every path without pruning is exponential.

## Key insight
With non-negative weights, Dijkstra grows a set of finalized distances. A min-heap of `(distance, node)` always pops the next closest unsettled node. When the heap empties, if you visited all `n` nodes, the answer is the max distance in the map; otherwise `-1`.

## Algorithm
1. Build adjacency list `u → [(v, w), ...]`.
2. `dist = {k: 0}`, heap `[(0, k)]`.
3. While heap: pop `(d, node)`; skip if `d` is stale; for each neighbor, if `d+w` improves `dist[nei]`, update and push.
4. If `len(dist) == n`, return `max(dist.values())`, else `-1`.

## Trace
`n = 4`, `k = 2`, times `[[2,1,1],[2,3,1],[3,4,1]]`.

| pop | dist map | note |
|---|---|---|
| (0,2) | {2:0} | start |
| (1,1) | {2:0,1:1} | edge 2→1 |
| (1,3) | {…,3:1} | edge 2→3 |
| (2,4) | {…,4:2} | via 3 |

All four nodes reached; max distance 2.

## Complexity
Binary heap Dijkstra: O((V+E) log V) time. Dist map and heap O(V). Bellman-Ford is simpler to code but O(V·E). Floyd-Warshall O(V³) is for all-pairs and overkill.

## Edge cases
`n = 1` → 0. Start with no outgoing edges and n>1 → -1. Multiple edges; keep the improving one. Disconnected node not reachable from k. Zero-weight edges are fine; negative weights are out of scope for this heap Dijkstra.

## Alternatives and trade-offs
Adjacency matrix + dense Dijkstra O(V²) when E ~ V². SPFA is unnecessary here. If the prompt allowed negatives, switch to Bellman-Ford and detect cycles.

## Common bugs
Returning the sum of distances instead of the max. Forgetting `-1` when `len(dist) < n`. Not skipping stale heap entries so you "finalize" a worse distance. 0-based vs 1-based node labels.

## Follow-ups
Cheapest flights within k stops. Path with exactly k edges. Print the actual path tree (store parents).

## Related problems
Cheapest Flights Within K Stops, Path With Minimum Effort, Swim in Rising Water, Course Schedule II.
