# 35. Generate Parentheses — walkthrough

## Recognize it
Generate every string of n pairs of correctly matched parentheses. For n=3 that is the Catalan-number many strings such as `"((()))"`, `"(()())"`, etc. Look-alike: validate one parentheses string (stack). Another look-alike: generate all binary strings of length 2n (includes invalid ones).

## Brute force
Generate every string of n `'('` and n `')'` (choose n positions for opens) and filter with a balance check. There are C(2n, n) candidates; for each, O(n) validation. Works for tiny n; timed challenges want pruning so you never build invalid prefixes.

## Key insight
A prefix is valid-to-extend when `#open ≤ n` and `#close ≤ #open`. Depth-first search adds `'('` while opens remain, and adds `')'` only while closes trail opens. When the path length hits `2n`, the string is complete and valid by construction.

## Algorithm
1. `walk(opened, closed, path)`:
   - If `len(path) == 2*n`, append `path` to answers; return.
   - If `opened < n`, recurse with `opened+1` and `path + "("`.
   - If `closed < opened`, recurse with `closed+1` and `path + ")"`.
2. Start `walk(0, 0, "")`; return answers.

## Trace
`n = 2`.

| path | opened | closed | branches |
|---|---|---|---|
| "" | 0 | 0 | only "(" |
| "(" | 1 | 0 | "(" or ")" |
| "((" | 2 | 0 | only ")" |
| "(()" | 2 | 1 | only ")" |
| "(())" | 2 | 2 | record |
| "()" | 1 | 1 | only "(" (close blocked) |
| "()(" | 2 | 1 | only ")" |
| "()()" | 2 | 2 | record |

Answers `["(())","()()"]`.

## Complexity
Time and output size are Θ(C_n · n) where C_n is the nth Catalan number—you must write each character of each answer. Recursion depth O(n). No asymptotically faster listing exists because the output is that large.

## Edge cases
`n = 1` → `["()"]`. `n = 0` → `[""]` if allowed. Large n blows memory with the full list—sometimes prompts ask for a generator. Do not emit strings with closes first; the `closed < opened` guard prevents it.

## Alternatives and trade-offs
Insert a `"()"` into every position of every (n−1) solution, then dedupe with a set—slower and uglier. Catalan closed forms count without listing. BFS by string length also works; DFS is simpler. Prefer building only valid prefixes over generate-and-filter.

## Common bugs
Allowing `closed > opened` mid-string. Comparing `closed < n` without the open constraint (emits `")("`). Using a mutable list for `path` and forgetting to pop (string concat avoids that). Deduping permutations instead of pruning.

## Follow-ups
Generate parentheses with `[]` and `{}` too. Count only (Catalan). Longest valid parentheses substring. Remove invalid parentheses.

## Related problems
Valid Parentheses, Remove Invalid Parentheses, Combination Sum (backtracking), Different Ways to Add Parentheses.
