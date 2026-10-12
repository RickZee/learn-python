# Review, round 2: depth, coverage, internals, challenges section

Reviewed 2026-10-11 at `main` (53 commits). The fixes are in [AGENT_PLAN-2.md](AGENT_PLAN-2.md). Round 1 is in [CRITIQUE.md](CRITIQUE.md).

## Verdict

The repo is now well built. Setup is reproducible, CI runs every notebook, every exercise has a reference solution, and there's an AI tutor mode for Cursor and Claude. Random-input comparisons against brute force show the solutions are correct. What's still missing is the teaching. The lessons now show the *what* in a consistent shape, but they rarely explain the *why*: the mechanism underneath, what it costs, and why Python was designed that way. Three rules I wrote in round 1 made this worse; details below.

There is no "how Python works" section, and the repo needs one. The challenges section has good breadth (42 problems), but its tests are uneven and its solution explanations are too thin to learn from.

## How I checked

- Ran the whole suite on a clean checkout: **376 passed**. `ruff` is clean.
- Wrote brute-force references for 21 challenge problems and compared them with the repo's solutions on 400 random inputs each. **No mismatches.**
- Read lessons from every unit and pattern, plus a sample of challenge notebooks and solutions.
- Measured word counts, search hits for topics, and cell shapes across all 60 course lessons, 27 pattern lessons and 42 problems.

## What improved since round 1

- Lessons went from a median of 19 words with 1 code cell to about 256 words with 3 code cells. They now follow predict → worked example → mistake → investigate → modify.
- The course is one sequence, and patterns are separate. There are 42 challenge problems, including trees, graphs, backtracking, tries and heaps. There is also a codebase round, six real projects, audience paths, a skip test and a facilitator guide.
- `solutions/` is complete and correct. The challenge functions use snake_case.

## 1. Lessons explain *what*, rarely *why*

Every lesson has nearly the same length (209–376 words) whatever the topic. "Names" gets the same space as generators, decorators, async or dynamic programming. The questions in the "Why" sections are often answered by restating the fact:

| Lesson | Question it asks | Answer it gives | What a learner actually needs |
|---|---|---|---|
| `11-data-model/01-dunder` | "Why write `__len__` instead of a method named `length`?" | "`len()` looks for `__len__`." | Python's protocols: the language calls these hooks, so one function such as `len` works for every type, and your class plugs into built-ins, `for`, `in` and sorting. |
| `03-collections/03-dicts` | (no why) | — | A dict is a hash table. That's why lookups are fast, why keys must be hashable, why order is insertion order, and when a list scan is the better choice. |
| `07-iteration/02-generators` | "How is `yield` different from `return`?" | "`yield` pauses." | Why you'd want laziness: memory, streams, pipelines. The iterator protocol underneath (`iter`, `next`, `StopIteration`). And the real trap: a generator works once, and a second loop over it is silently empty. |
| `03-collections/04-sets` | Shows `{[1, 2]}` raising `TypeError` | (no explanation of hashing) | Why lists can't go in a set, and why tuples can. |

**Common mistakes are contrived.** 63 of the 87 "Common mistake" cells are 1–3 lines that raise an obvious error: `print([1][3])`, `None.value`, `[].pop()`, `pool.shutdown(); pool.map(...)`. The bugs people really hit are often **silent**:
- iterating a used generator gives nothing
- `dict.fromkeys(keys, [])` shares one list across every key
- a recorded backtracking path that wasn't copied
- off-by-one errors in DP tables

This one is my fault: the round-1 template said the mistake should be "run so it raises".

**Other defects:**
- **Factual error.** `01-basics/01-names` says "`True` is a `bool`, not an `int`" and asks "why is that not `int`?". But `bool` is a subclass of `int` (`isinstance(True, int)` is `True`, and `True + True == 2`). The older conditions text said the opposite, so the course now contradicts itself.
- **Stale prerequisite labels.** The "Uses:" lines in pattern lessons point at old or wrong lessons: "Uses: 03 Coin change" on prefix sums, "01 Islands" on DP, "02 Three pointers", "01 Classes" on hash maps. They're plain text, so the link test can't catch them.
- **Hollow worked examples.**
  - `patterns/13-dynamic-programming/01-min-cost` is titled *Min cost* but teaches counting climbs, which is challenge problem 17. Its worked example `small(n)` returns `n` on both branches. Its "mistake" (`[][-1]`) is explained wrongly as "a negative stair count".
  - Seven lessons say "A small function that is not the practice problem" and then show something trivial, such as `subset_count` returning `2 ** len(nums)`.
- **Contorted examples.** `03-dicts` counts words with three unrolled `if len(words) > n` checks, because loops come after collections in the sequence. My concept-order rule forced that.

## 2. Coverage

The big gaps from round 1 are closed. These remain. Each one matters for writing real Python or timed challenges:

| Gap | Search hits in `course/` | Why it matters |
|---|---|---|
| **Recursion** as a topic: base case, call stack, `RecursionError`, recursion vs iteration | 1 | Trees, backtracking and DP depend on it. Today learners meet it first inside patterns. |
| **Cost of built-in operations** (`in` on list vs set, `insert(0)`, string `+=`, slicing copies) | 0 hits for O(1) | Needed to make any performance judgment, and asked in every timed challenge. |
| **Copying** (`copy`, `deepcopy`, slices) and argument passing ("call by sharing") | 0 | The source of most aliasing bugs. |
| **Hashing** and the `__eq__`/`__hash__` contract | 0 | Dict keys, sets, dataclasses with `frozen=True`. |
| **Text vs bytes**, Unicode, `encoding=` | 0 | Every file and network task. |
| **Dates and times** (`datetime`, `zoneinfo`) | 0 | Every business or data task. |
| **Keyword-only and positional-only parameters**, `*`/`**` unpacking at the call site | 0–1 | Reading any modern API. |
| **Mocking and monkeypatching**, test isolation | 0 | Testing code that does I/O. |
| **`contextlib.contextmanager`**, `ExitStack` | 0 | The everyday way to write context managers. |
| **Race conditions and `Lock`**; asyncio `TaskGroup` and timeouts | 0 / 1 | Concurrency without correctness is a trap, even more so with free-threading arriving. |
| **Typing beyond hints:** `Protocol`, generics, `TypedDict` | 0 | Reading typed codebases and tools like pydantic. |
| **Debugging with `pdb`**, `logging` configuration | 1 / 2 | Day-to-day work. |
| **`bisect`**, `functools.cache` in depth, walrus operator | 0–1 | Idiomatic Python for timed challenges and DP. |

## 3. Yes: add a "How Python works" track

Nothing currently explains the machine underneath: objects and references, how `list` and `dict` are built, what reference counting and the garbage collector do, how attribute lookup and the MRO work, how imports resolve, what bytecode is, what the GIL actually protects. Experienced developers and Python-specific challenges care about exactly this ("why is `in` on a set fast?", "what does `is` compare?", "why is my default list shared?", "is `x += 1` thread-safe?"). It's also the shortest path to the *why* that the lessons lack. Every pitfall in `09-pitfalls` is a symptom of one of these mechanisms.

**Recommendation:** a 12-lesson `internals/` track (outline in the plan). Each lesson is built on runnable experiments (`id`, `sys.getrefcount`, `sys.getsizeof`, `dis.dis`, `__mro__`, `timeit`), with CPython-specific details labelled as such. Course lessons link to it from a new "Why it works this way" section.

## 4. Challenges section: good breadth, thin explanations, uneven tests

**Strengths.** 42 problems cover all the core families. Each has constraints, a target, a three-step hint ladder and an "after you pass" prompt. Solutions are correct and carry Approach / Time / Space / Alternative / Common bugs.

**Gaps:**
- **Solution explanations are too short to learn from.** The median docstring is **50 words**. Coin Change says "try every coin that fits and keep the minimum". It doesn't explain why greedy fails (coins `[1, 3, 4]`, amount 6: greedy uses 4+1+1, the best is 3+3), how the recurrence is derived, how the table fills, or why the loop order matters for the "count the ways" variant. Learners who get stuck need a full walkthrough: how to recognize the pattern, brute force, key insight, a trace table, the complexity derivation, alternatives and follow-ups.
- **Tests are uneven.** Only **13 of 42** problems have randomized cross-checks, and **26 of 42** have a scale check. The median is 4.5 checks per problem, so a half-right solution often passes.
- **The problem notebooks are templated.** "Before you code" is identical boilerplate in all 42. Examples exist only inside the asserts, not as worked input → output pairs. Follow-ups are generic.
- **Coverage holes** against common lists (NeetCode 150, Grind 75):
  - prefix sum + hash map (Subarray Sum Equals K)
  - monotonic deque (Sliding Window Maximum)
  - binary search on the answer (Koko Eating Bananas)
  - greedy (Jump Game, Gas Station)
  - union-find (Redundant Connection)
  - shortest paths (Network Delay Time)
  - Clone Graph
  - tree depth combos (Diameter), BST order (Kth Smallest), Serialize/Deserialize
  - DP (Word Break, Longest Increasing Subsequence, Edit Distance, Decode Ways)
  - Permutations
  - linked lists (Remove Nth From End, Reorder List)
  - matrix (Rotate Image, Spiral)
  - strings (Longest Palindromic Substring)
  - bits (Single Number, Counting Bits)
  - Time-Based Key-Value Store (`bisect`)
- **No Python-knowledge round.** Python roles often ask language questions: mutability, GIL, generators, decorators, `__eq__`/`__hash__`, MRO. The internals track should feed a question bank.
- **The guide has no pattern-recognition table** (signal → pattern) and no cost table for Python built-ins.

## 5. Three round-1 rules backfired

These were my rules, and the agent followed them faithfully. They need changing, not just the content.

1. **"Common mistake must raise."** This produced contrived one-liners. Replace it with: show the bug learners actually make. If it's silent, print the wrong result next to the fix.
2. **"No concept before its lesson," with collections taught before loops.** This produced unrolled code. Teach `for` before collections (over `range` and strings), and keep the ledger.
3. **"Pattern lessons must not solve challenge problems."** This produced hollowed-out lessons. Keep the rule, but require each lesson to *fully* solve a genuinely different sibling problem, end to end.

## Fix order

1. Fix the facts, the "Uses:" labels and the hollow DP lesson. Change the three rules in `AGENTS.md`. Move loops before collections.
2. Add the "Why it works this way" and "When to use it" sections to every lesson, scaled to difficulty. Use the per-lesson checklist in the plan.
3. Add the recursion unit and the other coverage units.
4. Build the `internals/` track and the Python-knowledge question bank.
5. Upgrade the pattern lessons to the recognize → brute force → insight → trace → cost template.
6. Challenges section: a walkthrough per problem, randomized and edge-case checks everywhere, about 20 new problems, and a recognition table and cost table in the guide.
7. Add tests that enforce these structures, so the next pass can't drift back.
