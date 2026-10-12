# Agent plan, round 2: depth, coverage, internals, challenges section

For Cursor or Claude Code. The reasons are in [CRITIQUE-2.md](CRITIQUE-2.md). The ground rules in [AGENT_PLAN.md](AGENT_PLAN.md) still apply, except where section R0 below replaces them.

**How to run it.** One phase per session and one branch per phase. Start each session with:

> Read `review/CRITIQUE-2.md` and `review/AGENT_PLAN-2.md`. Do **Phase R*n*** only. Follow the ground rules in `AGENT_PLAN.md` and section R0. When done, run the acceptance checks, show me the results and a summary of the diff, and stop.

R1 is quick. R2, R5 and R6 are large, so do them one unit per commit and stop after every 3–4 units for review. R3 and R4 add new content.

---

## R0. Rule changes (put these into `AGENTS.md` first, in Phase R1)

Replace these authoring rules in `AGENTS.md`:

1. **Common mistakes are real mistakes.** Show the bug learners actually make in that topic. If it raises, tag the cell `raises-exception`. If it's silent, which is often the more valuable case, print the wrong result, then show the fix in the next cell with a sentence explaining *why* it was wrong. Banned: one-liners whose only point is that an error exists (`print([1][3])`, `None.value`, `[].pop()`).
2. **Every lesson explains why.** Every lesson gets two sections:
   - `## Why it works this way`: the mechanism underneath, what it costs (time and memory), and the design reason. Link the matching `internals/` lesson.
   - `## When to use it`: when this is the right tool, when it isn't, and what to use instead.
   A "why" answer must not just restate the fact: "`len()` calls `__len__`" doesn't answer "why `__len__`?".
3. **Depth scales with difficulty.** Tag every lesson in its first cell as **Core**, **Intermediate** or **Deep**. Target words, excluding code:

   | Tier | Words | Examples |
   |---|---|---|
   | Core | 350–600 | names, numbers, strings, lists |
   | Intermediate | 600–1,000 | functions and scope, errors, comprehensions, dicts and sets, classes |
   | Deep | 900–1,600, with a diagram or trace table | generators, decorators, data model, concurrency, async, every pattern lesson, every `internals/` lesson |

   Don't pad. If a lesson needs more than that, split it.
4. **Pattern lessons fully solve a sibling problem.** The lesson's worked example is a complete, realistic solution to a problem that is *not* in `challenges/problems/`, followed from start to end. Banned: placeholder functions and the phrase "not the practice problem".
5. **Loops come before collections.** `for` over `range` and strings is taught before lists and dicts (Phase R1.4). After that, unrolled code to avoid a loop is banned.
6. **Prerequisites are links.** `**Uses:**` must be Markdown links to the lessons it builds on, so `tests/test_links.py` checks them.
7. **Facts get checked by running them.** Any claim about behaviour ("`bool` is not an `int`") must be backed by a cell that prints the evidence (`isinstance(True, int)`). CPython-only details are labelled "CPython detail" and tagged `volatile` if the output can vary.

---

## R1. Corrections and sequence (quick)

1.1 **Update `AGENTS.md`** with R0. Also update the lesson template in `AGENT_PLAN.md` Phase 3: add the two new sections and the tier tag, and replace the old common-mistake rule.

1.2 **Fix the bool claim** in `course/01-basics/01-names-lesson.ipynb`:
- In the Predict check, write "`True` is a `bool`. `bool` is a subclass of `int`, so `True == 1` and `True + True == 2`."
- Add a cell that prints `isinstance(True, int)` and `True + True`.
- Rewrite Investigate question 2: "Why does `type(True).__name__` say `bool` even though `isinstance(True, int)` is `True`?"
- Search the whole repo for other statements that `bool` is not an `int`.

1.3 **Fix the "Uses:" labels.** Every lesson in `course/`, `patterns/` and `internals/` gets `**Uses:** [title](relative/path.ipynb)`, or `**Uses:** nothing yet`. Derive them from `docs/concepts.md` and each lesson's real prerequisites. Today the patterns cite old names ("03 Coin change", "01 Islands", "02 Three pointers").

1.4 **Move loops before collections.** Renumber `03-collections` ↔ `04-control-flow`. The new `03-control-flow` loops over `range` and strings, and `04-collections` follows it. Then:
- Move `zip`/`enumerate` to the end of `04-collections`.
- Update `docs/concepts.md`, `tests/test_sequence.py` expectations and all links.
- Rewrite `04-collections/03-dicts` and `01-lists` worked examples to use loops. Remove the unrolled `if len(words) > n` code.

1.5 **Rewrite `patterns/13-dynamic-programming/01-min-cost`** using Exemplar B below. It must solve **Min Cost Climbing Stairs** (LeetCode 746), not count climbs, because counting climbs is challenge problem 17. Remove `small(n)` and the `[][-1]` "mistake".

1.6 **Remove the boilerplate.** Replace the seven "A small function that is not the practice problem" worked examples with full sibling solutions (R0.4).

1.7 **Add `tests/test_lesson_structure.py`.** For every lesson in `course/`, `patterns/` and `internals/`, assert that:
- it has a `## Why it works this way` section of at least 120 words (Core) or 250 words (Intermediate or Deep)
- it has a `## When to use it` section
- the first cell has a tier tag
- `**Uses:**` contains a link or "nothing yet"
- the phrase "not the practice problem" is absent
- no common-mistake code cell is shorter than 3 lines unless it's tagged `real-mistake-short`, for the rare genuine one-liner

Mark the test `xfail` for lessons not yet upgraded. List those lessons in `docs/upgrade-status.md` and remove each from the list as its unit is done in R2.

**Acceptance:** `uv run pytest -n auto` passes (with xfails), the links test covers "Uses:", and the bool fact is fixed.

---

## R2. Depth pass on the language course

One unit per commit. For each lesson:
- Add **Why it works this way** and **When to use it**.
- Replace the common mistake with a real one.
- Make the Predict cell target a real misconception rather than a trivial print.
- Make **Modify** ask for a change that tests understanding, not a one-character edit.

Use Exemplar A as the quality bar. The table lists what each unit's *why* must cover. Every bullet must appear somewhere in that unit.

| Unit | The *why* the lessons must explain |
|---|---|
| 00-start | What the interpreter does with a `.py` file (reads, compiles, runs top to bottom). Why notebooks keep state between cells and the dangers of running cells out of order. How to read a traceback. |
| 01-basics | Names are labels on objects, not boxes (link a Python Tutor visualization). `int` has unlimited size. `float` is binary floating point (preview of 0.1 + 0.2). `//` floors toward negative infinity (`-7 // 2 == -4`) and why. `bool` subclasses `int`. Truthiness comes from `__bool__`/`__len__`. `and`/`or` return an operand, which is why `x or default` works and when it bites (0 and ""). |
| 02-strings | Strings are immutable, so methods return new strings. Why `"".join` beats `+=` in a loop (quadratic copying), measured with `timeit`. Slicing copies. A `str` is Unicode code points, with `len("é")` vs encoded byte length. Why regex patterns are raw strings, and catastrophic backtracking in one sentence. |
| 03-control-flow (renumbered) | `for` uses the iteration protocol, so it works on anything iterable. `range` is lazy and constant-memory. `while`/`else` and `for`/`else` semantics. `match` is structural pattern matching, not a C switch: capture patterns and the "bare name captures" trap. |
| 04-collections (renumbered) | A list is a dynamic array: amortized O(1) append (show `sys.getsizeof` growing in steps), O(n) `insert(0)` and `in`. A tuple is immutable and hashable, so it can be a dict key and lists can't. A dict or set is a hash table: average O(1) lookup, keys must be hashable, insertion order is guaranteed. A cost table for common operations. `zip(strict=True)` and why silent truncation is a bug. |
| 05-functions | Functions are objects. Arguments are passed by sharing: mutating a parameter is visible to the caller, rebinding it isn't (show both). Default values are evaluated once, at `def` time. LEGB lookup. Closures capture variables, not values. Keyword-only (`*`) and positional-only (`/`) parameters and why APIs use them. `*`/`**` unpacking at the call site. Type hints are not enforced at runtime, and who uses them (tools, readers, pydantic). |
| 06-errors | EAFP vs LBYL and why Python prefers EAFP. The exception hierarchy and why to catch narrowly (`except Exception` vs bare `except`, which also catches `KeyboardInterrupt`). `else`/`finally` order. `raise ... from` chaining. Frames in a traceback. `breakpoint()` and the 5 `pdb` commands you need. |
| 07-iteration | Comprehensions have their own scope. Generator laziness: memory measured with `sys.getsizeof` on a list vs a generator. Iterators are single-pass, and the silent empty second loop. `iter()`/`next()`/`StopIteration` under `for`. `sorted` is stable, so sorting by two keys works in two passes. `key=` vs `cmp`. `lambda` limits. |
| 08-collections-module | `Counter` and `defaultdict` are dict subclasses (`__missing__`). `deque` is O(1) at both ends where a list is O(n) at the front. `heapq` is a list with an invariant, and why it's a min-heap only. `heapify` is O(n). `itertools` is lazy. `bisect` for sorted lists (new lesson). `functools.cache`, and what it needs from its arguments (hashable). |
| 09-pitfalls | Tie each pitfall to its mechanism and link the internals lesson. Add a lesson on shallow vs deep copy (`copy`, `deepcopy`, `list(x)`, `x[:]`). Small-int and string caching as a CPython detail, never to be relied on. |
| 10-classes | Instance vs class attributes, with the shared-mutable-class-attribute bug. Why `self` is explicit (methods are functions, binding happens on lookup). Attribute lookup order. What `@dataclass` generates (`__init__`, `__repr__`, `__eq__`), and `frozen=True` → `__hash__`. MRO and cooperative `super()` (diamond example, print `__mro__`). `property` is a descriptor. Enum members are singletons. |
| 11-data-model | Protocols: the language calls dunders, so built-ins and syntax work on your objects. The `__eq__`/`__hash__` contract: defining `__eq__` sets `__hash__` to `None`, and why equal objects need equal hashes. `__bool__`/`__len__` truthiness. Context managers guarantee cleanup through `__exit__`. `contextlib.contextmanager` (new lesson). |
| 12-modules | Import runs the module once and caches it in `sys.modules`. The `sys.path` search order. Why circular imports half-work. `python -m`. What `uv add` changes (`pyproject.toml`, `uv.lock`, `.venv`). |
| 13-files | Text vs bytes. Encodings, and why `encoding="utf-8"` stays explicit even though 3.15 defaults to UTF-8. Why `with` (guaranteed close, buffered data flushed). How JSON types map to Python types (tuples become lists, keys become strings). `newline=""` for csv. |
| 14-testing | What a test buys you. pytest assertion rewriting. Fixtures and `tmp_path`. **Mocking and `monkeypatch`** for I/O (new lesson). Isolation, and why order-dependent tests are a bug. |
| 15-decorators | Functions are values, plus closures, so `@` is sugar for `f = deco(f)`. Why `functools.wraps`. Decorators with arguments as three layers. |
| 16-concurrency | What the GIL protects and when it's released. Why `x += 1` isn't atomic: a **race condition and `Lock`** lesson (new). Make the race deterministic with a read–sleep–write so it shows up every run. Processes pickle their arguments, which is why lambdas fail. The event loop is cooperative: one blocking call stalls everything. **`TaskGroup` and `asyncio.timeout`** (new). Free-threaded builds make locks matter more, not less. |
| 17-tooling | Static vs runtime checking. What a type checker catches that tests don't, and the reverse. `logging` configuration and levels vs `print`. |

**New lessons in R2** (full template):
- `04-collections/05-copying`
- `05-functions/05-unpacking-and-keyword-only`
- `08-collections-module/06-bisect`
- `11-data-model/03-contextlib`
- `14-testing/02-mocking`
- `16-concurrency/04-race-conditions`
- `16-concurrency/05-taskgroup-timeouts`
- `13-files/04-text-and-bytes`
- `13-files/05-dates-and-times` (`datetime`, `zoneinfo`, why naive datetimes are a bug)
- `17-tooling/02-protocols-and-generics` (`Protocol`, generics with 3.12+ syntax, `TypedDict`)

**Acceptance per unit:** the structure test passes for every lesson in the unit (no xfail left), outputs are regenerated, and `docs/upgrade-status.md` is updated.

---

## R3. A recursion unit, before the patterns

New `course/09-recursion` (renumber later units). Lessons:
1. Base case and recursive case. Trace the call stack as a table.
2. Recursion on structures: nested lists, then a tiny tree.
3. `RecursionError` and the default limit (~1000). Why Python has no tail-call optimization. Converting to iteration with an explicit stack.
4. Memoization with `functools.cache`. Count the calls before and after (Exemplar B shows how).

The patterns for trees, backtracking, graphs and DP list this unit in "Uses:".

---

## R4. New track: `internals/` ("How Python works")

Twelve **Deep** lessons. Each is built around runnable experiments, ends with "What this explains", which links back to the course lessons and pitfalls it explains, and adds 3–5 questions to the question bank (R4.2). Label CPython-specific behaviour, and tag cells `volatile` when output varies.

| # | Lesson | Experiments |
|---|---|---|
| 01 | Objects, names, references | `id`, `type`, `is`; two names, one object; a Python Tutor link for each example |
| 02 | Mutability and aliasing | assignment never copies; call by sharing; `copy` vs `deepcopy` on nested data |
| 03 | How `list` works | `sys.getsizeof` across 0–64 appends (over-allocation steps); `timeit` of `append` vs `insert(0)` vs `in` |
| 04 | How `dict` and `set` work | `hash()` values; a key whose hash changes after insertion → lost entry; `__eq__`/`__hash__` contract; insertion order; `timeit` list `in` vs set `in` |
| 05 | Numbers and strings | big ints; `0.1 + 0.2`; `float.hex`; `Decimal`/`Fraction`; string immutability; small-int and string caching labelled as a CPython detail |
| 06 | Scopes and closures | LEGB; `f.__closure__[0].cell_contents`; late binding; `global`/`nonlocal`; the class-scope surprise in comprehensions |
| 07 | The iteration protocol | `iter`, `next`, `StopIteration`; a `for` loop rewritten by hand; generator objects and their frames (`gi_frame`); `yield from` |
| 08 | Attribute lookup | instance `__dict__` → class → MRO; descriptors (`property`; functions become bound methods); `__getattr__` vs `__getattribute__`; `__slots__` memory |
| 09 | The import system | `sys.modules` caching; `sys.path`; a module is an object; a reproducible circular-import failure; `importlib.reload` caveats |
| 10 | From source to bytecode | `compile`, `dis.dis` on a loop; `__pycache__`/`.pyc`; why local variables are faster than globals (`LOAD_FAST` vs `LOAD_GLOBAL`), measured |
| 11 | Memory management | `sys.getrefcount`; reference cycles and `gc.collect()`; `weakref`; why to rely on `with`/`finally`, not `__del__` |
| 12 | The GIL and free-threading | what the GIL protects; I/O releases it; a CPU-bound thread vs process timing; why races still exist with the GIL; what `python3.14t` changes; a pointer to `concurrent.interpreters` (3.14) |

4.1 Link each course lesson's "Why it works this way" to the matching internals lesson, and each pitfall to its mechanism.

4.2 **Python-knowledge question bank: `challenges/python-questions.md`.** 40–60 questions grouped by internals lesson. Each has a 3–5 sentence model answer, the experiment that proves it (a link), and the usual wrong answer. For example: "Is `x += 1` thread-safe?", "What does `is` compare?", "Why can't a list be a dict key?", "What does `@dataclass(frozen=True)` give you?", "Generator vs list comprehension: when?", "What is the MRO?".

4.3 Add `internals/` to `docs/paths/experienced.md` (main track), `docs/paths/challenges.md` (week 1, alongside patterns) and `docs/language.md`.

**Acceptance:** 12 lessons pass the lesson and structure tests, and the question bank links resolve.

---

## R5. Pattern lessons: teach recognition, not just code

Every pattern lesson uses this structure. It's **Deep** tier, and Exemplar B shows the bar.

1. **Recognize it.** The signals in a problem statement that point to this pattern (for example, "contiguous subarray" plus "longest/shortest with a condition" → sliding window), plus one look-alike that *isn't* this pattern.
2. **Brute force, and why it's slow.** Code it and measure it, or count its operations.
3. **The key insight or invariant**, stated in one sentence and shown on the example.
4. **Worked solution** of the sibling problem, complete, with subgoal comments.
5. **Trace table** for the first example: one row per step.
6. **Cost**, derived rather than asserted.
7. **Variants.** Which challenge problems use this pattern: list them by name *without* solving them.
8. **Real mistakes** (R0.1).
9. **Python idioms** for this pattern (`deque` for BFS, `heapq` tuples for tie-breaks, `bisect`, `functools.cache`).

5.1 **New pattern units:**
- `16-greedy` (lesson: Assign Cookies; practice: Lemonade Change)
- `17-union-find` (lesson: count components; practice: Find if Path Exists, via union-find)
- `18-shortest-paths` (lesson: BFS on an unweighted grid, then Dijkstra on a small weighted graph; practice: Path With Minimum Effort, small inputs)
- `19-monotonic-deque` (lesson: max of every window of size 3 traced by hand; practice: the minimum version)
- `20-binary-search-on-answer` (lesson: smallest divisor under a threshold; practice: Capacity to Ship, small inputs)
- `21-matrix-traversal` (lesson: transpose and reverse rows; practice: diagonal order)
- `22-bits` (lesson: XOR tricks and `bin`; practice: count set bits)

5.2 **Add to `challenges/guide.ipynb`:**
- a **recognition table**: signal → pattern → link
- a **cost table for Python built-ins**: `list`, `dict`, `set`, `deque`, `heapq`, `str` operations with their Big-O, linking internals 03 and 04

**Acceptance:** every pattern lesson passes the structure test, plus `tests/test_no_leaks.py`, which now also checks that no pattern lesson's function body matches a challenge solution's AST.

---

## R6. Challenges section: walkthroughs, stronger checks, more problems

6.1 **A walkthrough per problem**, at `solutions/challenges/problems/NN-name.md`, next to the `.py`. Required headings, in order:

```
## Recognize it
## Brute force
## Key insight
## Algorithm
## Trace
## Complexity
## Edge cases
## Alternatives and trade-offs
## Common bugs
## Follow-ups
## Related problems
```

Minimum 350 words. The trace is a Markdown table on the first example. Exemplar C is the bar. Add `tests/test_walkthroughs.py`, which asserts that every `.py` has a `.md` with these headings in order and at least 350 words.

6.2 **Problem notebooks:**
- Show 2–3 examples as input → output in Markdown, with one sentence each on *why* that's the answer.
- Replace the identical "Before you code" with 2–3 problem-specific prompts. For example, for Coin Change: "Does picking the largest coin first always work? Try coins [1, 3, 4], amount 6."
- Make follow-ups specific: Coin Change → "count the combinations instead (and why the loop order changes)".

6.3 **Checks.** At least 8 per problem:
- examples
- edge cases: empty, single element, duplicates, negatives, maximum constraint
- a **randomized cross-check against a brute force** written in the notebook (all 42; today only 13 have one)
- a **scale check** wherever the target complexity is better than the brute force (today 26 have one)

For problems with many valid answers (Two Sum, Top K, Group Anagrams), check against the definition, as Top K already does. If a problem can't be randomized, tag the cell `no-random` and give the reason. Add `tests/test_challenge_checks.py`, which enforces ≥ 8 checks plus a random check or the `no-random` tag.

6.4 **New problems** (43–64). Priority A first.
- **Priority A:**
  - Subarray Sum Equals K (560)
  - Sliding Window Maximum (239)
  - Longest Repeating Character Replacement (424)
  - Koko Eating Bananas (875)
  - Jump Game (55)
  - Clone Graph (133)
  - Network Delay Time (743)
  - Redundant Connection (684)
  - Diameter of Binary Tree (543)
  - Kth Smallest Element in a BST (230)
  - Word Break (139)
  - Longest Increasing Subsequence (300)
  - Permutations (46)
  - Remove Nth Node From End (19)
- **Priority B:**
  - Edit Distance (72)
  - Decode Ways (91)
  - Serialize and Deserialize Binary Tree (297)
  - Reorder List (143)
  - Rotate Image (48)
  - Spiral Matrix (54)
  - Longest Palindromic Substring (5)
  - Task Scheduler (621)
  - Time Based Key-Value Store (981, uses `bisect`)
  - Single Number (136)
  - Counting Bits (338)
  - Meeting Rooms II (253; state it in your own words)

Each comes with a solution `.py`, a walkthrough `.md`, checks to R6.3 and links in `docs/guides/challenge-practice.md`. Extend the day plan in `docs/guides/challenge-practice.md` and `docs/paths/challenges.md` to six weeks.

6.5 **Codebase round 02** on a different domain, for example a rate limiter with a planted race condition. It practises the R2 locks lesson and the AI-enabled-round skills.

**Acceptance:** all walkthrough, check and leak tests pass. The random cross-check cells pass against the solutions and fail against a deliberately wrong solution. For each new problem, write one quick wrong variant and confirm the checks catch it, then note it in the commit message.

---

## Exemplar A: a course lesson with *why* (`04-collections/03-dicts`, Intermediate)

> Lesson cell order is now in `AGENTS.md` ("Lesson flow"). Use that, not the Predict-first shape below.

All code below was run and checked.

````markdown
# 03. Dicts

**Tier:** Intermediate. **You will be able to:** predict lookups and counts; explain why dict lookup is fast and why keys must be hashable; choose between a dict, a list, and `get`.
About 30 minutes. **Uses:** [Loops](../03-control-flow/02-loops-lesson.ipynb), [Tuples](02-tuples-lesson.ipynb).
````

**Predict.** Ask "what order, and which `in` is faster?":

```python
counts = {}
words = ["to", "be", "or", "not", "to", "be"]
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)
print(list(counts))
print("to" in counts, "to" in words)
```

Output: `{'to': 2, 'be': 2, 'or': 1, 'not': 1}`, then `['to', 'be', 'or', 'not']` (insertion order, guaranteed since Python 3.7), then `True True`.

**Why it works this way**, about 250 words, along these lines:

> A dict is a hash table. To store a key, Python calls `hash(key)`, turns that number into a slot in an internal array, and puts the key and value there. To look a key up, it hashes it again and jumps straight to that slot. It doesn't walk the entries, so lookup takes about the same time with 10 keys or 10 million. That's "average O(1)". A list has no such shortcut: `"to" in words` compares against each item in turn, which is O(n).
>
> That speed has one requirement: a key's hash must never change while it's in the dict. Otherwise the next lookup would jump to the wrong slot. So keys must be **hashable**, which for built-ins means immutable: numbers, strings and tuples of those work, lists don't. That's why the error is `unhashable type: 'list'`, and why you use a tuple for a two-part key.
>
> Since Python 3.7, dicts remember insertion order. The design is a compact array of entries plus a smaller index table, which also saves memory. Deep dive: [internals 04](../../internals/04-dict-and-set-lesson.ipynb).

```python
import timeit

items = list(range(100_000))
lookup = dict.fromkeys(items)
print("list in:", timeit.timeit(lambda: 99_999 in items, number=200))
print("dict in:", timeit.timeit(lambda: 99_999 in lookup, number=200))
print(hash((1, 2)) == hash((1, 2)))
```

(Tag `volatile`; the list is consistently more than 50× slower.)

**When to use it.** Use a dict to look things up by a key, count, or group. Use a list when order and position matter and you scan everything anyway. Use a set when you only need membership. Use `get(key, default)` when a missing key is normal, and `d[key]` when a missing key is a bug you want to hear about.

**Common mistakes** (both real; the second is silent):

```python
counts = {}
for word in ["a", "b", "a"]:
    counts[word] += 1   # KeyError on the first sighting: there is nothing to add 1 to
```

```python
groups = dict.fromkeys(["a", "b"], [])
groups["a"].append(1)
print(groups)   # {'a': [1], 'b': [1]}: both keys share ONE list
```

The fix cell builds a new list per key with a loop. Then explain: `fromkeys` stores the *same* object under every key, which is the aliasing from [internals 02](../../internals/02-mutability-lesson.ipynb).

- **Investigate:** "Why can `(1, 2)` be a key but `[1, 2]` can't?" and "What would go wrong if a key's hash changed after insertion?"
- **Modify:** "Count words case-insensitively. Which line changes, and why don't you change the dict itself?"

---

## Exemplar B: a pattern lesson (`patterns/13-dynamic-programming/01-min-cost`, Deep)

Problem: **Min Cost Climbing Stairs** (LeetCode 746). `cost[i]` is what you pay to step off stair `i`. You may start on stair 0 or 1, climb 1 or 2 at a time, and want the cheapest way to reach the top (just past the last stair).

1. **Recognize it.** Signals: "minimum/maximum/number of ways", choices at each step, and the best answer is built from the best answers to smaller versions. Look-alike that isn't DP: if one locally best choice is always safe, it's greedy (see `16-greedy`).

2. **Brute force, and why it's slow.** Count the calls:

```python
def min_cost_slow(cost):
    calls = 0

    def best(i):  # cheapest total from standing on stair i to the top
        nonlocal calls
        calls += 1
        if i >= len(cost):
            return 0
        return cost[i] + min(best(i + 1), best(i + 2))

    answer = min(best(0), best(1))
    return answer, calls


for n in (10, 20, 25):
    print(n, min_cost_slow([1] * n))
```

Output: `10 (5, 464)`, `20 (10, 57312)`, `25 (12, 635620)`. The number of calls grows exponentially because `best(i)` is recomputed again and again: overlapping subproblems.

3. **Key insight.** Let `reach[i]` be the cheapest cost to *stand on* stair `i`. You arrive from `i - 1` (paying `cost[i - 1]`) or from `i - 2` (paying `cost[i - 2]`), so `reach[i] = min(reach[i-1] + cost[i-1], reach[i-2] + cost[i-2])`. Each value needs only the two before it.

4. **Worked solution:**

```python
def min_cost(cost: list[int]) -> int:
    # 1. State: the cheapest way to stand on the previous two stairs.
    # 2. Base: standing on stair 0 or 1 is free.
    two_back, one_back = 0, 0
    # 3. Transition: arrive from one below or two below, paying for the stair you leave.
    for i in range(2, len(cost) + 1):
        two_back, one_back = one_back, min(one_back + cost[i - 1], two_back + cost[i - 2])
    # 4. The top is stair len(cost), one past the last.
    return one_back


print(min_cost([10, 15, 20]))                          # 15
print(min_cost([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]))  # 6
```

5. **Trace** for `[10, 15, 20]`:

| i | from i−1 | from i−2 | reach[i] |
|---|---|---|---|
| 0 | — | — | 0 |
| 1 | — | — | 0 |
| 2 | 0 + 15 | 0 + 10 | 10 |
| 3 (top) | 10 + 20 | 0 + 15 | **15** |

6. **Cost.** One pass with two variables: O(n) time, O(1) space. That beats exponential because each stair is solved once.

7. **Variants** (not solved here): Climbing Stairs (#17), House Robber (#18), Coin Change (#19), Unique Paths (#37).

8. **Real mistake** (silent): the loop stops one stair early and returns the last stair instead of the top.

```python
def min_cost_wrong(cost):
    reach = [0, 0]
    for i in range(2, len(cost)):          # stops one short of the top
        reach.append(min(reach[i - 1] + cost[i - 1], reach[i - 2] + cost[i - 2]))
    return reach[-1]


print(min_cost_wrong([10, 15, 20]))  # 10, but the answer is 15
```

9. **Python idioms.** Tuple assignment to roll the two variables. `functools.cache` turns `best(i)` into the memoized top-down version in one line. Show it, and show `best.cache_info()`.

---

## Exemplar C: a solution walkthrough (`solutions/challenges/problems/19-coin-change.md`)

````markdown
# 19. Coin Change — walkthrough

## Recognize it
"Fewest coins" is a minimum over choices, and the best way to make `amount` is built from the best way to make a smaller amount. That's dynamic programming. The trap is greedy: it looks right with US coins and fails in general.

## Brute force
Try every coin, recurse on the remainder, keep the minimum. Without memoization the same remainders are solved over and over, so the cost is exponential in `amount`.

## Key insight
`fewest[x] = 1 + min(fewest[x - c] for c in coins if c <= x)`, with `fewest[0] = 0`. Greedy fails: with coins `[1, 3, 4]` and amount 6, taking the largest coin first gives 4 + 1 + 1 (3 coins), but 3 + 3 uses 2.

## Algorithm
1. `fewest = [0] + [amount + 1] * amount`. The value `amount + 1` stands for "impossible", because no answer can need more than `amount` coins.
2. For each coin, for each total from `coin` to `amount`: `fewest[total] = min(fewest[total], fewest[total - coin] + 1)`.
3. Return `fewest[amount]` if it's at most `amount`, else `-1`.

## Trace
coins `[1, 3, 4]`, amount 6:

| total | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| fewest | 0 | 1 | 2 | 1 | 1 | 2 | **2** |

`fewest[6] = min(fewest[5] + 1, fewest[3] + 1, fewest[2] + 1) = min(3, 2, 3) = 2`.

## Complexity
Each of `amount` totals tries each coin once: O(amount × coins) time, O(amount) space.

## Edge cases
amount 0 → 0. No coin fits → -1. A single coin that divides the amount. Coins larger than the amount are skipped.

## Alternatives and trade-offs
Top-down recursion with `functools.cache` (same cost, deeper recursion; watch the recursion limit at amount 10,000). BFS over remainders finds the fewest coins level by level, and is good when the answer is small.

## Common bugs
Initialising the table with 0 (impossible amounts look free). Using `float("inf")` and then returning it. Greedy.

## Follow-ups
"Count the number of combinations" (Coin Change II): loop coins on the outside so each combination is counted once. With totals on the outside you count permutations instead. "Return the coins used": store the last coin per total and walk back.

## Related problems
Climbing Stairs (#17), Word Break (new), Perfect Squares.
````
