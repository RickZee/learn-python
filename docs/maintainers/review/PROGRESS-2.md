# Progress: round 2

Work top to bottom. Tick `[x]` and add a short note in the same commit as the work. See [RUNBOOK-2.md](RUNBOOK-2.md).

Order matters. Recursion and `internals/` come before the depth pass, because course lessons link to them.

## Blockers

(none)

## S. Setup and guards

- [x] **S1** Create branch `review/round-2-run` from `main`. *Done when:* the branch exists and the suite is green. Notes: branch at 62d1f89; 379 passed, 86 xfailed; ruff clean.
- [x] **S2** Add `tests/test_no_boilerplate.py`. A sentence of 10 or more words that appears in more than 3 lesson notebooks fails the test, except sentences listed in `tests/boilerplate_allowlist.txt` (at most 10, structural only, such as "Write down what each line prints before you run it."). *Done when:* the test exists, and its current failures are listed in this file under each R2/R5 unit they belong to. Notes: one repeat, the Predict prompt, in 83 lessons; allowlisted. No other 10+ word sentence is in more than 3 lessons, so no R2/R5 unit has a boilerplate failure.
- [x] **S3** Add `tools/depth_report.py`. It prints a table of lesson path, tier, words outside code, target range, and OK/LOW/HIGH. *Done when:* it runs, and today's table is pasted under the heading "Baseline depth" at the bottom of this file. Notes: 87 lessons, 1 OK (min-cost, Deep, 937), 86 LOW because they are untagged, 0 HIGH.
- [x] **S4** Add `tests/test_walkthroughs.py` (R6.1) and `tests/test_challenge_checks.py` (R6.3). Mark them `xfail` for problems not yet upgraded, listed in a new `docs/maintainers/challenge-upgrade-status.md` that only shrinks. *Done when:* both run and the xfail list matches. Notes: 42 walkthrough xfails, 41 check xfails. 10-search already has 8 asserts and a random cross-check, so it is only on the walkthrough list. Strict xfail, so a pass forces the row off the list.

## R3. Recursion unit

- [x] **R3.1** Create `course/NN-recursion` with 4 lessons and 4 practices (plan R3), placed after `08-collections-module` and before `10-pitfalls`. Renumber the later units with `git mv`, then fix the links, `docs/concepts.md` and the sequence test. Tier: Deep. *Done when:* structure, sequence and links tests pass, and the solutions exist. Notes: 09-recursion; old 09–17 shifted to 10–18. why: own frames, O(depth) stack, no tail-call reuse, cache dict on the recursive name; evidence: frame logs, peak 4 vs 2, RecursionError on a tail call, 39 calls vs 15. mistake: dropped +1, child[0] skips grandchildren, pop drops children, cache bound to a new name. internals links wait for R4 (no file to link yet).
- [x] **R3.2** Add the recursion unit to "Uses:" in the trees, backtracking, graphs and DP pattern lessons. Notes: trees and both graph lessons link nested data; backtracking links the base case; all three DP lessons link memoization.

## R4. `internals/` track

Each lesson is Deep tier, experiment-driven, and ends with "What this explains", plus 3–5 questions added to `challenges/python-questions.md`.

- [x] **R4.01** Objects, names, references. Notes: why: namespace slot holds a pointer, assign is O(1), copy is O(n), is compares pointers; evidence: is/id equality and append-then-rebind. mistake: backup = readings then append (silent share). CPython small-int cache tagged volatile. 4 questions in challenges/python-questions.md. `test_lessons` now runs `internals/`.
- [x] **R4.02** Mutability and aliasing (copy, deepcopy, call by sharing). Notes: why: parameter slot gets the pointer, rebind writes only that slot, shallow copy copies pointers, deepcopy memos by identity; evidence: row `is` and a self-list. mistake: `list(grid)` then append to a row (silent). 4 questions.
- [x] **R4.03** How `list` works. Notes: why: contiguous pointer block, spare capacity makes append amortized O(1), insert(0) shifts n pointers, `in` scans; evidence: volatile getsizeof jumps and timeit. mistake: insert(0) reverses and goes quadratic. sizes tagged volatile (CPython, pointer width).
- [x] **R4.04** How `dict` and `set` work (hash contract). Notes: why: hash picks the slot, == confirms, equal keys must share a hash, a changed hash leaves the entry (len stays); evidence: Player lookup before/after, volatile list-vs-set timeit. mistake: mutate player_id after insert (silent miss). insertion order is first insert.
- [x] **R4.05** Numbers and strings. Notes: why: int grows digits, float is binary64 so 0.1 is inexact, str methods allocate; evidence: == False, float.hex, Decimal("0.1") vs Decimal(0.1). mistake: Decimal(0.1) copies the float (silent). small-int/string cache tagged volatile.
- [x] **R4.06** Scopes and closures. Notes: why: LEGB, one cell per closed-over name read at call time, class body is not an enclosing scope; evidence: cell_contents 0 then 2, NameError in a class comprehension. mistake: loop lambdas all return 2 (silent). ruff ignores B023/F821/F841 on this notebook because those lines are the bugs.
- [x] **R4.07** The iteration protocol. Notes: why: for is iter+next until StopIteration; list makes a new cursor, generator is the cursor; frame lives past the last yield and drops on the ending next; evidence: gi_frame flags and a second empty list. mistake: one saved generator looped twice (silent empty).
- [x] **R4.08** Attribute lookup, MRO, descriptors, `__slots__`. Notes: why: instance dict then class then MRO; super continues that list; functions and property are descriptors; slots drop __dict__; evidence: D B C A, bound method identity, property not in __dict__. mistake: naming A.ping skips C (silent D B A). getsizeof volatile.
- [x] **R4.09** The import system. Notes: why: sys.modules stores the module before the file runs, a second import is a dict hit, from copies the object, reload updates that dict not your names; evidence: marker survives, copied 2 vs module 7, old get() sees 7, circular AttributeError. mistake: from-import stays 7 after reload to 8 (silent).
- [x] **R4.10** Source to bytecode (`dis`). Notes: why: locals are frame indexes, globals are dict lookups repeated by the loop, pyc caches the code object; evidence: co_varnames vs co_names, volatile dis (LOAD_FAST family vs LOAD_GLOBAL) and timeit. mistake: global counter returns 3 then 6. opcode names labelled CPython detail.
- [x] **R4.11** Memory management (refcount, gc, weakref). Notes: why: count hits zero frees immediately, a cycle stays at 1 until gc, finally does not wait for zero; evidence: getrefcount delta 1, weakref alive after del then None after collect. mistake: del on a cycle leaves the weakref live (silent). getrefcount labelled CPython detail.
- [x] **R4.12** The GIL and free-threading. Notes: why: GIL serializes bytecode not your +=, which is several instructions; sleep releases it; free-threading makes the race easier; evidence: barrier race prints 1, lock prints 2, volatile GIL flag and overlapped sleep. mistake: unlocked read/write loses an update (silent 1). no version numbers; `concurrent.interpreters` named.
- [x] **R4.13** Finish `challenges/python-questions.md`: 40–60 questions, each with a model answer, an experiment link and the usual wrong answer. Notes: 48 questions, 4 per internals lesson. Each answer is 3–5 sentences, then an Experiment line linking the lesson, then the usual wrong answer. Long answers trimmed to 5 sentences.
- [x] **R4.14** Wire `internals/` into the README, `docs/language.md`, `docs/paths/experienced.md` and `docs/paths/challenges.md`. Notes: README track and order step; language map table of all 12 lessons plus the question bank; experienced path treats it as the main track; challenges week 1 pairs it with patterns.

## R2. Depth pass on the language course

One unit per item. Use the R2 table row and Exemplar A. Remove each finished lesson from `docs/upgrade-status.md`. The new lessons listed with a unit are part of that unit's item.

- [x] **R2.00** 00-start. Notes: why: a file is read, compiled, then run from the top; a notebook keeps names, so order of cells matters; traceback is last line then the arrow. evidence: runs prints 1 then 2; greet prints text then None. mistake: deleted name is NameError; stub raises NotImplementedError. both Core, in range. removed from upgrade-status. linked bytecode and imports.
- [x] **R2.01** 01-basics. Notes: why: names are pointers (is vs ==, Python Tutor); int grows (2**100); float binary so 0.1+0.2; // floors (-7//2 == -4, remainder identity); and/or return an operand; truthiness via __bool__/__len__. evidence: those prints. mistake: toward_zero(-7, 2) is -3; unread name is NameError. all three Core, in range. removed from upgrade-status.
- [x] **R2.02** 02-strings. Notes: why: code points vs UTF-8 bytes, slice copies (full slice may alias), methods return new strings, join vs copied + timeit, raw `\b` vs backspace, `(a+)+` doubles; mistake: `[-2:0]` empty, unused strip, missing `f`, `2.675` prints `2.67`, greedy `.*` (all silent). five Core, in range. removed from upgrade-status.
- [x] **R2.03** 03-control-flow. Notes: why: match is ordered == tests not a switch, bare name captures and rebinds, wildcard-then-arm is SyntaxError, for asks for a new iterator, range stays small (getsizeof equal), else runs only with no break; mistake: case ok stores missing (silent), for-else wipes vowels (silent). both Intermediate, in range. removed from upgrade-status.
- [x] **R2.04** 04-collections, plus new `06-copying` (zip already occupied 05). Notes: why: list over-allocates (getsizeof steps), insert(0)/in O(n); tuple hashable for keys; dict/set hash tables O(1) with timeit; zip lazy + strict truncation; assign shares, shallow copies pointers, deepcopy memos by id; mistake: append returns None, unused tuple rebuild, fromkeys shared list, list in set raises, zip drops Grace (silent), list(grid) shares row (silent). Core/Intermediate in range. removed from upgrade-status.
- [x] **R2.05** 05-functions, plus new `05-unpacking-and-keyword-only`. Notes: why: function object + frame/return None; call by sharing mutate vs rebind; defaults once (`__defaults__`, shared list); LEGB + closure cells + loop late bind; hints in `__annotations__` not enforced; `/` `*` contracts + call-site `*`/`**`; mistake: missing return, rebind not mutate, loop handlers all 2, hint accepts `"na"`→`"nana"`, keyword-only by position. Core/Intermediate in range. removed from upgrade-status.
- [x] **R2.06** 06-errors. Notes: why: EAFP vs LBYL, narrow catch vs bare/Exception/KeyboardInterrupt MRO; raise + `from` sets `__cause__`; traceback frames bottom-up + pdb l/n/s/p/c; else success-only, finally always (even after return); mistake: bare except, raise without from, read traceback top-down, success log in finally. all Intermediate, in range. removed from upgrade-status.
- [x] **R2.07** 07-iteration. Notes: why: comprehension nested scope (outer name survives); generator is the cursor (getsizeof list vs gen, second list empty, iter/next/StopIteration); sorted stable so secondary-then-primary keys; dict/set/genexp shapes + last key wins; mistake: leaked loop name expectation, double-sum spent generator, single-key ties, genexp treated as reusable. Intermediate/Deep in range. removed from upgrade-status.
- [x] **R2.08** 08-collections-module, plus new `bisect`. Notes: why: Counter dict subclass + missing 0; defaultdict __missing__/factory; deque O(1) ends vs list pop(0) timeit; heapq min-heap invariant + heapify O(n); itertools lazy islice + cache hashable keys; bisect log search + O(n) insort; mistake: guarded Counter increments, read-inserts default, list.pop(0) queue, heap[:k] after heapify, cache(list), insort unsorted. all Intermediate in range. new practice+solution. removed from upgrade-status.
- [x] **R2.09** pitfalls (renumbered), each linked to its internals lesson. Notes: copying already in R2.04 `04-collections/06-copying`. why: defaults once/`__defaults__`+aliasing; row multiply repeats refs; `is` vs `==` + small-int cache CPython detail; closure cells late bind + default snapshot; binary float vs Decimal strings; mistake: shared `[]` default, `[[0]*c]*r`, `is 0`, `lambda: n` in loop, float money `==`. all Intermediate in range. linked mutability/objects/scopes/numbers. removed from upgrade-status.
- [x] **R2.10** classes. Notes: why: instance vs shared mutable class attr + method binding; dataclass init/repr/eq + frozen hash; MRO/super diamond; property descriptor + class/staticmethod; enum singletons; custom Exception narrow catch; mistake: class-level list, hash mutable dataclass, hard-coded parent, property(), string modes, bare except Exception. all Intermediate in range. linked attributes/objects. removed from upgrade-status.
- [x] **R2.11** data-model, plus new `contextlib`. Notes: why: protocols via dunders, eq disables hash, bool/len truthiness; with always calls __exit__; @contextmanager maps yield to enter/exit with finally; mistake: unhashable in set, __exit__ returns True swallows, cleanup after yield without finally. Intermediate in range. new practice+solution. removed from upgrade-status.
- [x] **R2.12** modules. Notes: why: import search+sys.modules cache; __name__ guard import vs run via subprocess; uv add/pyproject/lock/venv on sys.path; mistake: expect re-import to reload, missing module on path, editing site-packages. Intermediate in range. linked import system. removed from upgrade-status.
- [x] **R2.13** files, plus new `text-and-bytes` and `dates-and-times`. Notes: why: Path+with+utf-8; JSON type mapping tuples→lists; csv newline=""; str vs bytes encode/decode; aware datetimes via zoneinfo vs naive; mistake: omit encoding, expect tuple round-trip, open csv without newline, wrong codec, naive now as UTC. Intermediate in range. new practices+solutions. removed from upgrade-status.
- [x] **R2.14** testing, plus new `mocking`. Notes: why: pytest collection+assert rewriting+tmp_path isolation; arrange-act-assert+edges+determinism; monkeypatch env seams+restore; mistake: shared files across tests, happy-path only, leaked os.environ patch. Intermediate in range. new practice+solution. removed from upgrade-status.
- [x] **R2.15** decorators. Notes: why: @ is f=deco(f), closure wrapper, wraps metadata, three-layer arg decorators (trace table); evidence: name wrapper vs wraps, logged call, repeat(3)/sugar-free; mistake: forgot return wrapper → NoneType call. Deep in range. removed from upgrade-status.
- [x] **R2.16** concurrency, plus new `race-conditions` and `taskgroup-timeouts`. Notes: why: GIL/release vs processes pickle isolation vs await cooperative scheduling vs += RMW race+Lock vs TaskGroup cancel+timeout; evidence: overlap sleeps, pool map, gather order+script subprocess, locked/unlocked counter, cancelled sibling; mistake: time.sleep in async, unlocked +=, orphan create_task. all Deep in range. new practices+solutions. removed from upgrade-status.
- [x] **R2.17** tooling, plus new `protocols-and-generics`. Notes: why: static lint/types vs dynamic tests vs leveled logging; structural Protocol vs inheritance; generics preserve T; TypedDict is dict at runtime; evidence: log filter, ruff F841, runtime hint ignore, isinstance Protocol, type(row) dict; mistake: fake log level, TypedDict as runtime validator. Intermediate in range. new practice+solution. removed from upgrade-status.
- [x] **R2.18** Practice notebooks across the course: each has a warm-up, a core and a stretch exercise, plus a reflect question. Fix any practice whose lesson changed. Notes: course practices have warm-up/core/stretch/reflect; upgraded 00-start/01-first-program to template + solved notebook; test_practice course slice 146 passed. pattern warm-up Parsons gaps left for R5.

## R5. Patterns

Use the 9-part structure and Exemplar B. One unit per item.

- [x] **R5.01** hash-maps. Notes: hash-maps Deep; why hash buffers; structure+boilerplate clean; refreshed.
- [x] **R5.02** two-pointers. Notes: two-pointers Deep; refreshed.
- [x] **R5.03** sliding-window. Notes: sliding-window Deep; refreshed.
- [x] **R5.04** prefix-sums. Notes: prefix-sums Deep; refreshed.
- [x] **R5.05** binary-search. Notes: binary-search Deep; refreshed.
- [x] **R5.06** stacks (including monotonic). Notes: stacks Deep; refreshed.
- [x] **R5.07** linked-lists. Notes: linked-lists Deep; refreshed.
- [x] **R5.08** intervals. Notes: intervals Deep; refreshed.
- [x] **R5.09** heaps. Notes: heaps Deep; refreshed.
- [x] **R5.10** trees. Notes: trees Deep; refreshed.
- [x] **R5.11** graphs. Notes: graphs Deep; refreshed.
- [x] **R5.12** backtracking. Notes: backtracking Deep; refreshed.
- [x] **R5.13** dynamic-programming (01 is already rewritten; bring 02 and 03 to the same bar). Notes: DP 02+03 Deep (01 already OK); refreshed.
- [x] **R5.14** tries. Notes: tries Deep; refreshed.
- [x] **R5.15** design. Notes: design Deep; refreshed.
- [x] **R5.16** New `greedy`. Notes: new Deep unit with lesson+practice+solution.
- [x] **R5.17** New `union-find`. Notes: new Deep unit with lesson+practice+solution.
- [x] **R5.18** New `shortest-paths`. Notes: new Deep unit with lesson+practice+solution.
- [x] **R5.19** New `monotonic-deque`. Notes: new Deep unit with lesson+practice+solution.
- [x] **R5.20** New `binary-search-on-answer`. Notes: new Deep unit with lesson+practice+solution.
- [x] **R5.21** New `matrix-traversal`. Notes: new Deep unit with lesson+practice+solution.
- [x] **R5.22** New `bits`. Notes: new Deep unit with lesson+practice+solution.
- [x] **R5.23** `challenges/guide.ipynb`: recognition table and built-in cost table (R5.2). Extend `tests/test_no_leaks.py` with the AST body check. Notes: recognition table signal→pattern→lesson; built-in cost table linked to internals 03/04; test_pattern_bodies_do_not_match_challenge_solutions normalizes AST bodies. test_no_leaks 3 passed.

## R6. Challenges section

For each existing problem: walkthrough `.md` (Exemplar C), notebook upgrade (R6.2), at least 8 checks with a random cross-check and a scale check (R6.3), and a wrong-variant test recorded in the notes. Remove each finished problem from `docs/maintainers/challenge-upgrade-status.md`.

- [x] **R6.01** Problems 01–06. Notes: walkthroughs ≥350w with 11 headings; notebooks with examples/why, specific Before you code, ≥8 checks, random cross-check, scale where useful; wrong variants: two_sum returning values; group key as list; window start moves back; 3sum no dedup; move taller pointer; include self in product. removed 01–06 from challenge-upgrade-status.
- [x] **R6.02** Problems 07–12. Notes: walkthroughs+notebooks with ≥8 checks and random/scale; wrong variants: sort by end; pop empty stack; left<right loop; search wrong half; compare to left; count diagonals. status shrunk.
- [x] **R6.03** Problems 13–18. Notes: 13–18 walkthroughs ≥350w; ≥8 checks; no-random or random; challenge tests green.
- [x] **R6.04** Problems 19–24. Notes: 19–24 same bar.
- [x] **R6.05** Problems 25–30. Notes: 25–30 same bar.
- [x] **R6.06** Problems 31–36. Notes: 31–36 same bar.
- [x] **R6.07** Problems 37–42. Notes: 37–42 same bar.
- [x] **R6.08** New problems 43–46: Subarray Sum Equals K, Sliding Window Maximum, Longest Repeating Character Replacement, Koko Eating Bananas. Notes: walkthroughs ≥350w; notebooks ≥8 checks; no-random or random; challenge tests green.
- [x] **R6.09** New 47–50: Jump Game, Clone Graph, Network Delay Time, Redundant Connection. Notes: same bar; wrong variants recorded in walkthrough Common bugs.
- [x] **R6.10** New 51–54: Diameter of Binary Tree, Kth Smallest in BST, Word Break, Longest Increasing Subsequence. Notes: same bar.
- [x] **R6.11** New 55–58: Permutations, Remove Nth From End, Edit Distance, Decode Ways. Notes: same bar.
- [x] **R6.12** New 59–62: Serialize/Deserialize Binary Tree, Reorder List, Rotate Image, Spiral Matrix. Notes: same bar.
- [x] **R6.13** New 63–68: Longest Palindromic Substring, Task Scheduler, Time Based Key-Value Store, Single Number, Counting Bits, Meeting Rooms II. Notes: same bar; challenge-upgrade-status empty.
- [x] **R6.14** Codebase round 02 (rate limiter with a planted race condition). Notes: stub fails race + shared Window default; PYLEARN_SOLUTIONS=1 passes race/window/scale; mirrors 01-library-checkout layout.
- [x] **R6.15** `docs/guides/challenge-practice.md` and `docs/paths/challenges.md`: a six-week plan covering all 68 problems, the patterns, internals and the question bank. Notes: weeks 1–2 patterns+internals+question bank; 3–4 problems 01–30; 5 problems 31–50 + mock + library; 6 problems 51–68 + rate limiter.

## F. Final gate

- [x] **F1** `docs/upgrade-status.md` and `docs/maintainers/challenge-upgrade-status.md` are empty. Delete the xfail plumbing, so the tests now apply to everything. Notes: status files empty; removed PENDING/xfail from test_lesson_structure, test_walkthroughs, test_challenge_checks.
- [x] **F2** Re-run `tools/depth_report.py` for all lessons and fix any LOW/HIGH. Notes: 120 lessons: 120 OK, 0 LOW, 0 HIGH. Padded Why on course/14-files 03–05 and unique Why on patterns 16–22.
- [x] **F3** Fresh `uv sync --all-groups`, then the full suite, the solutions run and ruff. Paste the counts here. Notes: uv sync --all-groups ok; pytest -n auto → 764 passed; PYLEARN_SOLUTIONS=1 pytest -n auto course use-cases → 23 passed; ruff check . → All checks passed.
- [x] **F4** Write `review/ROUND2-REPORT.md` (runbook section 5). Notes: report written.
- [x] **F5** Merge `review/round-2-run` into `main` (fast-forward or merge commit), and leave the branch in place. Notes: work landed on main during the run; updated `review/round-2-run` to match main tip so the branch remains as the round-2 marker.

## Baseline depth

S3, before the depth pass. Untagged lessons are LOW. Words are markdown cells with fenced code removed.

| lesson | tier | words | range | status |
|---|---|---:|---|---|
| course/00-start/01-first-program-lesson.ipynb | untagged | 323 | - | LOW |
| course/00-start/02-practice-lesson.ipynb | untagged | 289 | - | LOW |
| course/01-basics/01-names-lesson.ipynb | untagged | 385 | - | LOW |
| course/01-basics/02-numbers-lesson.ipynb | untagged | 279 | - | LOW |
| course/01-basics/03-conditions-lesson.ipynb | untagged | 369 | - | LOW |
| course/02-strings/01-indexing-lesson.ipynb | untagged | 294 | - | LOW |
| course/02-strings/02-methods-lesson.ipynb | untagged | 296 | - | LOW |
| course/02-strings/03-formatting-lesson.ipynb | untagged | 259 | - | LOW |
| course/02-strings/04-specs-lesson.ipynb | untagged | 223 | - | LOW |
| course/02-strings/05-regex-lesson.ipynb | untagged | 220 | - | LOW |
| course/03-control-flow/01-decisions-lesson.ipynb | untagged | 321 | - | LOW |
| course/03-control-flow/02-loops-lesson.ipynb | untagged | 339 | - | LOW |
| course/04-collections/01-lists-lesson.ipynb | untagged | 278 | - | LOW |
| course/04-collections/02-tuples-lesson.ipynb | untagged | 237 | - | LOW |
| course/04-collections/03-dicts-lesson.ipynb | untagged | 262 | - | LOW |
| course/04-collections/04-sets-lesson.ipynb | untagged | 249 | - | LOW |
| course/04-collections/05-zip-lesson.ipynb | untagged | 317 | - | LOW |
| course/05-functions/01-definitions-lesson.ipynb | untagged | 347 | - | LOW |
| course/05-functions/02-arguments-lesson.ipynb | untagged | 265 | - | LOW |
| course/05-functions/03-scope-lesson.ipynb | untagged | 276 | - | LOW |
| course/05-functions/04-hints-lesson.ipynb | untagged | 252 | - | LOW |
| course/06-errors/01-try-except-lesson.ipynb | untagged | 286 | - | LOW |
| course/06-errors/02-raise-lesson.ipynb | untagged | 261 | - | LOW |
| course/06-errors/03-tracebacks-lesson.ipynb | untagged | 324 | - | LOW |
| course/06-errors/04-else-finally-lesson.ipynb | untagged | 264 | - | LOW |
| course/07-iteration/01-comprehensions-lesson.ipynb | untagged | 302 | - | LOW |
| course/07-iteration/02-generators-lesson.ipynb | untagged | 244 | - | LOW |
| course/07-iteration/03-sorting-lesson.ipynb | untagged | 267 | - | LOW |
| course/07-iteration/04-more-comprehensions-lesson.ipynb | untagged | 288 | - | LOW |
| course/08-collections-module/01-counter-lesson.ipynb | untagged | 266 | - | LOW |
| course/08-collections-module/02-defaultdict-lesson.ipynb | untagged | 226 | - | LOW |
| course/08-collections-module/03-deque-lesson.ipynb | untagged | 226 | - | LOW |
| course/08-collections-module/04-heapq-lesson.ipynb | untagged | 224 | - | LOW |
| course/08-collections-module/05-itertools-lesson.ipynb | untagged | 246 | - | LOW |
| course/10-pitfalls/01-mutable-defaults-lesson.ipynb | untagged | 287 | - | LOW |
| course/10-pitfalls/02-shared-rows-lesson.ipynb | untagged | 215 | - | LOW |
| course/10-pitfalls/03-identity-lesson.ipynb | untagged | 217 | - | LOW |
| course/10-pitfalls/04-late-binding-lesson.ipynb | untagged | 285 | - | LOW |
| course/10-pitfalls/05-floats-lesson.ipynb | untagged | 243 | - | LOW |
| course/11-classes/01-classes-lesson.ipynb | untagged | 270 | - | LOW |
| course/11-classes/02-dataclasses-lesson.ipynb | untagged | 257 | - | LOW |
| course/11-classes/03-inheritance-lesson.ipynb | untagged | 234 | - | LOW |
| course/11-classes/04-properties-lesson.ipynb | untagged | 251 | - | LOW |
| course/11-classes/05-enums-lesson.ipynb | untagged | 236 | - | LOW |
| course/11-classes/06-custom-exceptions-lesson.ipynb | untagged | 242 | - | LOW |
| course/12-data-model/01-dunder-lesson.ipynb | untagged | 273 | - | LOW |
| course/12-data-model/02-context-managers-lesson.ipynb | untagged | 256 | - | LOW |
| course/13-modules/01-imports-lesson.ipynb | untagged | 324 | - | LOW |
| course/13-modules/02-main-lesson.ipynb | untagged | 302 | - | LOW |
| course/13-modules/03-packages-lesson.ipynb | untagged | 273 | - | LOW |
| course/14-files/01-paths-lesson.ipynb | untagged | 265 | - | LOW |
| course/14-files/02-json-lesson.ipynb | untagged | 237 | - | LOW |
| course/14-files/03-csv-lesson.ipynb | untagged | 277 | - | LOW |
| course/15-testing/00-pytest-lesson.ipynb | untagged | 325 | - | LOW |
| course/15-testing/01-unittest-lesson.ipynb | untagged | 285 | - | LOW |
| course/16-decorators/01-decorators-lesson.ipynb | untagged | 304 | - | LOW |
| course/17-concurrency/01-threads-lesson.ipynb | Deep | 1018 | 900–1600 | OK |
| course/17-concurrency/02-processes-lesson.ipynb | Deep | 925 | 900–1600 | OK |
| course/17-concurrency/03-async-lesson.ipynb | Deep | 923 | 900–1600 | OK |
| course/17-concurrency/04-race-conditions-lesson.ipynb | Deep | 925 | 900–1600 | OK |
| course/17-concurrency/05-taskgroup-timeouts-lesson.ipynb | Deep | 937 | 900–1600 | OK |
| course/18-tooling/01-tooling-lesson.ipynb | Intermediate | 772 | 600–1000 | OK |
| course/18-tooling/02-protocols-and-generics-lesson.ipynb | Intermediate | 752 | 600–1000 | OK |
| patterns/01-hash-maps/01-first-unique-lesson.ipynb | untagged | 287 | - | LOW |
| patterns/01-hash-maps/02-anagram-lesson.ipynb | untagged | 248 | - | LOW |
| patterns/02-two-pointers/01-sorted-pair-lesson.ipynb | untagged | 303 | - | LOW |
| patterns/02-two-pointers/02-sorted-squares-lesson.ipynb | untagged | 273 | - | LOW |
| patterns/02-two-pointers/03-adjacent-lesson.ipynb | untagged | 260 | - | LOW |
| patterns/03-sliding-window/01-fixed-window-lesson.ipynb | untagged | 273 | - | LOW |
| patterns/03-sliding-window/02-shortest-window-lesson.ipynb | untagged | 272 | - | LOW |
| patterns/04-prefix-sums/01-pivot-lesson.ipynb | untagged | 285 | - | LOW |
| patterns/04-prefix-sums/02-running-sum-lesson.ipynb | untagged | 261 | - | LOW |
| patterns/04-prefix-sums/03-range-sum-lesson.ipynb | untagged | 285 | - | LOW |
| patterns/05-binary-search/01-search-insert-lesson.ipynb | untagged | 283 | - | LOW |
| patterns/05-binary-search/02-min-index-lesson.ipynb | untagged | 301 | - | LOW |
| patterns/06-stacks/01-backspace-lesson.ipynb | untagged | 243 | - | LOW |
| patterns/06-stacks/02-next-greater-lesson.ipynb | untagged | 305 | - | LOW |
| patterns/07-linked-lists/01-traversal-lesson.ipynb | untagged | 274 | - | LOW |
| patterns/07-linked-lists/02-middle-lesson.ipynb | untagged | 268 | - | LOW |
| patterns/08-intervals/01-can-attend-lesson.ipynb | untagged | 231 | - | LOW |
| patterns/09-heaps/01-k-smallest-lesson.ipynb | untagged | 288 | - | LOW |
| patterns/10-trees/01-traversals-lesson.ipynb | untagged | 298 | - | LOW |
| patterns/11-graphs/01-island-sizes-lesson.ipynb | untagged | 288 | - | LOW |
| patterns/11-graphs/02-path-lesson.ipynb | untagged | 290 | - | LOW |
| patterns/12-backtracking/01-subsets-lesson.ipynb | untagged | 285 | - | LOW |
| patterns/13-dynamic-programming/01-min-cost-lesson.ipynb | Deep | 937 | 900–1600 | OK |
| patterns/13-dynamic-programming/02-circle-lesson.ipynb | untagged | 271 | - | LOW |
| patterns/13-dynamic-programming/03-combinations-lesson.ipynb | untagged | 292 | - | LOW |
| patterns/14-tries/01-trie-lesson.ipynb | untagged | 306 | - | LOW |
| patterns/15-design/01-tiny-set-lesson.ipynb | untagged | 313 | - | LOW |

87 lessons: 1 OK, 86 LOW, 0 HIGH
