# 39. Implement Trie — walkthrough

## Recognize it
You need `insert`, `search` (exact word), and `starts_with` (any word with that prefix), all fast in the length of the query. Look-alike: a hash set of words—exact search is fine, but prefix queries scan everything. Another look-alike: sorted list + binary search for prefixes (works, heavier constants).

## Brute force
Store every inserted word in a set. `search` is O(1) expected. `starts_with` walks the whole set and checks `word.startswith(prefix)`—O(total characters stored) per call, too slow when the dictionary is large and prefixes are frequent.

## Key insight
Share prefixes in a tree: each edge is a character, each node may mark "a word ends here." Walking the characters of a query visits one node per character. `search` requires ending on a marked node; `starts_with` only needs the walk to succeed.

## Algorithm
1. Node = map of char → child node, plus boolean `end`.
2. `insert(word)`: from the root, for each character `setdefault` a child; mark `end` on the final node.
3. `_walk(text)`: follow children; return the node or `None` if a character is missing.
4. `search(word)`: walk succeeds and `node.end` is True.
5. `starts_with(prefix)`: walk succeeds (ignore `end`).

## Trace
Insert `"app"`, then `"apple"`, then search / prefix checks.

| op | path nodes | end flags | result |
|---|---|---|---|
| insert app | a→p→p | last end=True | — |
| insert apple | reuse app, +l→e | e end=True | — |
| search app | reach 2nd p | end True | True |
| search appl | reach l | end False | False |
| starts_with appl | reach l | — | True |
| search bat | missing b | — | False |

## Complexity
Each operation is O(L) time for query length L. Space is O(total characters inserted) in the worst case (no shared prefixes); shared prefixes save nodes. Alphabet maps (dict) beat fixed arrays when the alphabet is sparse.

## Edge cases
Empty string insert/search—define whether `end` on the root counts (usually words are non-empty). `starts_with` of a full word → True. Inserting a word that is a prefix of an existing word must set `end` on the intermediate node without removing longer words. Duplicate inserts are idempotent.

## Alternatives and trade-offs
Array of size 26 per node is faster for lowercase-only and uses more memory on sparse tries. A set plus a separate prefix set updated on insert also works but uses more string storage. Ternary search trees are rarer in timed challenges.

## Common bugs
`search` returning True for a prefix that was never inserted as its own word (`apple` inserted, `app` not). Forgetting to mark `end`. Sharing one global `end` instead of per node. Mutating during walk without creating missing children only in `insert`.

## Follow-ups
Word Search II (trie on the board). Autocomplete (DFS from the prefix node). Delete a word (optional unmark / prune).

## Related problems
Word Search II, Design Add and Search Words, Replace Words, Longest Word in Dictionary.
