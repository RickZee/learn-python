# 36. Word Search — walkthrough

## Recognize it
Board of letters; return whether `word` appears as a path of 4-adjacent cells (no diagonal), each cell used at most once in the path. Look-alike: word search II (many words—trie + DFS). Another look-alike: exist as a subsequence in a flattened row (no adjacency).

## Brute force
From every starting cell matching `word[0]`, try all walks of length `len(word)` without revisiting cells. That is the real algorithm; "brute" is doing it without pruning on letter mismatch or without marking visited, which wastes work and can reuse cells illegally.

## Key insight
Backtracking DFS: at step `index`, you must stand on a cell equal to `word[index]`. Mark the cell used (for example `'#'`), try four neighbors for `index+1`, then restore the letter so other branches can use it. Success when `index == len(word)`.

## Algorithm
1. `walk(row, col, index)`:
   - If `index == len(word)`, return True.
   - If out of bounds or `board[row][col] != word[index]`, return False.
   - Save letter, set cell to `'#'`.
   - Recurse on four neighbors for `index+1`; if any True, success.
   - Restore letter; return whether found.
2. Return True if `walk(r, c, 0)` succeeds for any start cell.

## Trace
Board:
```
A B C E
S F C S
A D E E
```
Word `ABCCED`.

| step | cell | index letter | next |
|---|---|---|---|
| 0 | (0,0) A | A | → right |
| 1 | (0,1) B | B | → right |
| 2 | (0,2) C | C | → down |
| 3 | (1,2) C | C | → down |
| 4 | (2,2) E | E | → left |
| 5 | (2,1) D | D | done |

Path uses each cell once; restore marks let a later start retry cleanly. Word `ABCB` fails because after ABC the board's B is already used.

## Complexity
Up to rows·cols starts; each path explores up to 4^{L} branches with L = len(word), pruned heavily by mismatches: O(rows·cols·4^L) worst case. Stack depth O(L). Marking in place uses O(1) extra besides the stack; a visited set is O(L).

## Edge cases
Single-letter word. Word longer than rows·cols → False. Reusing the same cell illegally (must mark). Multiple identical letters—marking prevents diamond revisits. Empty board. First letter absent → quick False after scanning starts.

## Alternatives and trade-offs
Explicit stack DFS same idea. Building a trie for word search II amortizes shared prefixes across many queries. Copying the board per branch is simpler but slower. Prefer in-place mark/restore in timed challenges.

## Common bugs
Forgetting to restore the cell after recurse—later starts see holes. Allowing diagonal moves. Checking `index == len(word) - 1` after matching instead of before accessing the next letter. Starting walk at index 0 without verifying the start letter (the bound check handles it if you compare first).

## Follow-ups
Word Search II (list all words from a dictionary). Longest path of unique letters. Boggle scoring.

## Related problems
Word Search II, Number of Islands (DFS flood), Combination Sum (backtracking restore), Surrounded Regions.
