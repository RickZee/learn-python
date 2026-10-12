# 08. Valid Parentheses — walkthrough

## Recognize it
Brackets must nest and close in LIFO order. A stack of openers is the pattern. Look-alike: score of parentheses (still stack, different return).

## Brute force
Repeatedly remove `"()"`, `"[]"`, `"{}"` until stuck: O(n²) with string rebuilds.

## Key insight
Every closer must match the most recent unmatched opener. Push openers; on a closer, pop and compare.

## Algorithm
1. Map closers to openers.
2. For each character: push if opener; else if stack empty or top mismatch → False; else pop.
3. Return whether the stack is empty.

## Trace
`"{[]}"`.

| char | stack |
|---|---|
| { | { |
| [ | {[ |
| ] | { |
| } | empty → True |

## Complexity
O(n) time, O(n) space.

## Edge cases
Empty string → True. Single opener → False. Wrong order `"(]"` → False. Extra closer first → False.

## Alternatives and trade-offs
 Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure.  Narrate the brute force and its cost before coding the faster approach. State the invariant you maintain. Walk empty and duplicate-heavy inputs after the happy path. Name the pattern so you can transfer it to related prompts under time pressure. Counter of opens vs closes is not enough (order matters). Recursive descent is overkill for a timed challenge.

## Common bugs
Popping an empty stack. Not checking the stack is empty at the end. Matching across types.

## Follow-ups
Longest valid parentheses. Generate parentheses. Minimum removals to make valid.

## Related problems
Daily Temperatures (stack), Min Stack, Decode String.
