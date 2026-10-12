# 12. Number of Islands — walkthrough

## Recognize it
Count connected components of land on a grid; 4-direction adjacency. DFS/BFS flood fill from each unvisited land cell. Look-alike: max area of island (same walk, different aggregate).

## Brute force
Union-Find on every land cell with neighbor unions, then count roots—correct but heavier to code.

## Key insight
Each DFS/BFS from a land cell sinks an entire island (mark visited). The number of times you start a walk equals the island count.

## Algorithm
1. If grid empty, return 0.
2. For each cell, if land `"1"`, increment count and sink via DFS/BFS (set to `"0"` or mark visited).
3. Return count.

## Trace
Grid:
```
11000
11000
00100
00011
```
Three starts: top-left blob, middle 1, bottom-right blob → 3.

## Complexity
O(rows * cols) time—each cell visited once. Space O(rows * cols) worst-case recursion/queue.

## Edge cases
Empty grid. All water. All land (one island). Single cell. Diagonal-only touch (not connected).

## Alternatives and trade-offs
 Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure. BFS queue avoids deep recursion. Union-Find is natural if you already need components elsewhere.

## Common bugs
Counting diagonals. Not marking visited so you recount. Mutating a shared grid without restoring when required.

## Follow-ups
Max area of island. Number of distinct islands by shape. Surrounded regions.

## Related problems
Pacific Atlantic Water Flow, Rotting Oranges, Course Schedule (components on graphs).
