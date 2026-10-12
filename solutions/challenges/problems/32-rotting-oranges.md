# 32. Rotting Oranges — walkthrough

## Recognize it
Grid cells are empty (0), fresh orange (1), or rotten (2). Each minute, every rotten orange simultaneously rots adjacent fresh ones (4-direction). Return minutes until no fresh remain, or -1 if impossible. Look-alike: number of islands (flood one component). Another look-alike: walls-and-gates (multi-source distance fill).

## Brute force
Simulate minute by minute: scan the whole grid, collect cells that should rot, apply updates, count minutes—until a round changes nothing. Each minute is O(rows·cols), and minutes can be O(rows·cols), so O((rows·cols)²) worst case. Correct but slower to code cleanly and easier to miscount the last empty round.

## Key insight
All initially rotten oranges are simultaneous sources. Multi-source BFS starts with all of them in the queue; each BFS layer is one minute. Track the fresh count; when the queue runs dry, either fresh is 0 (answer = minutes) or some fresh were unreachable (-1).

## Algorithm
1. Count `fresh`, enqueue every cell with value 2.
2. `minutes = 0`.
3. While `queue` and `fresh > 0`:
   - Build `nxt` of cells newly rotten this minute.
   - For each cell in `queue`, for each 4-neighbor that is fresh: mark 2, decrement `fresh`, append to `nxt`.
   - `queue = nxt`; if `nxt` non-empty, `minutes += 1`.
4. Return `minutes` if `fresh == 0` else `-1`.

## Trace
```
2 1 1
1 1 0
0 1 1
```

| minute | queue (rotten fronts) | fresh left |
|---|---|---|
| start | (0,0) | 6 |
| 1 | (0,1),(1,0) | 4 |
| 2 | (0,2),(1,1) | 2 |
| 3 | (2,1) | 1 |
| 4 | (2,2) | 0 |

Answer 4. If a fresh orange sits isolated with no path through fresh cells from any rotten, BFS ends with `fresh > 0` → -1.

## Complexity
Each cell enqueued at most once: O(rows·cols) time and space. Beats repeated full-grid scans when the infection frontier is small. Mutating the grid to 2 marks visited; a separate visited matrix costs extra space.

## Edge cases
No fresh oranges → 0 minutes (already done). No rotten but some fresh → -1. Single cell grid. Rotting that does not need an extra minute after the last successful round—only increment minutes when `nxt` is non-empty (the code's `if nxt` guard).

## Alternatives and trade-offs
Minute-by-minute full scans are clearer for tiny grids. Multi-source BFS is the standard challenge answer. DFS depth does not model simultaneous minutes correctly without careful timestamps. Copying a new grid each minute wastes allocations.

## Common bugs
Incrementing minutes after a round that rotted nothing. Forgetting multi-source start (only one rotten in the queue). Using 8-direction adjacency. Returning the BFS depth of the last cell without checking leftover fresh oranges.

## Follow-ups
Shortest path to get food. Walls and gates. Pacific Atlantic water flow (multi-source from borders).

## Related problems
Number of Islands, Word Ladder (BFS layers), Surrounded Regions, Course Schedule (graph reachability, different structure).
