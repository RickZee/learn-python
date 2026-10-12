# Round 2 report

## What changed

- Course units R2.00–R2.18: depth sections (Why / When), common-mistake cells, tier tags, practices and solutions brought to the round-2 template.
- Pattern units R5.01–R5.22 deepened; new units 16–22 (greedy, union-find, shortest paths, monotonic deque, binary search on answer, matrix traversal, bits).
- `challenges/guide.ipynb`: recognition table and built-in cost table; AST body leak check in `tests/test_no_leaks.py`.
- Challenge problems 01–68: Exemplar C walkthroughs (≥350 words, 11 headings), notebooks with ≥8 checks and random/no-random, reference `.py` solutions.
- Codebase rounds: `01-library-checkout` (existing) and new `02-rate-limiter` with planted race + shared mutable default.
- Docs: six-week plan in `docs/guides/challenge-practice.md` and `docs/paths/challenges.md`.
- Final gate: emptied `docs/upgrade-status.md` and `docs/maintainers/challenge-upgrade-status.md`; removed xfail plumbing from structure/walkthrough/check tests.

Counts at F3:

| Check | Result |
| --- | --- |
| `uv sync --all-groups` | ok |
| `pytest -n auto` | 764 passed |
| `PYLEARN_SOLUTIONS=1 pytest -n auto course use-cases` | 23 passed |
| `ruff check .` | All checks passed |
| `tools/depth_report.py` | 120 lessons, 0 LOW, 0 HIGH |
| Challenge walkthroughs + checks | 68 + 68 passed |

## Blockers and resolutions

| Blocker | Resolution |
| --- | --- |
| Parallel authoring subagents hit usage limits | Finished R5/R6 solo with scripts (`write_problem`, nbformat pads). |
| `test_no_boilerplate` on shared Why prose for patterns 16–22 | Rewrote unique Why sections per unit (≥250 Why words). |
| `test_no_leaks` on `count_bits` colliding with challenge 67 | Renamed pattern helper to `popcounts_through`. |
| Practice splice missed `deserialize_level` on problem 59 | Added matching stub next to `serialize_level`. |
| Ruff E702/E741 on generated TimeMap / palindrome solutions | Expanded asserts; renamed `l`/`r` to `left`/`right`. |
| ProcessPool / volatile timings earlier in the round | Moved to `cpu_work.py`; tagged volatile cells. |

## Deviations from the plan

- Work continued on `main` rather than only on `review/round-2-run` after early commits; F5 updates `review/round-2-run` to the main tip so the branch remains as the round-2 marker without a second merge commit rewriting history.
- Lesson-flow work from an earlier commit was deferred to RUNBOOK-3 per author direction.
- Some challenge notebooks use `no-random` markdown instead of a randomized oracle when a compact brute check is a poor fit; the tag and reason meet `tests/test_challenge_checks.py`.

## Depth report

| lesson | tier | words | range | status |
|---|---|---:|---|---|
| course/00-start/01-first-program-lesson.ipynb | Core | 597 | 350–600 | OK |
| course/00-start/02-practice-lesson.ipynb | Core | 592 | 350–600 | OK |
| course/01-basics/01-names-lesson.ipynb | Core | 596 | 350–600 | OK |
| course/01-basics/02-numbers-lesson.ipynb | Core | 579 | 350–600 | OK |
| course/01-basics/03-conditions-lesson.ipynb | Core | 599 | 350–600 | OK |
| course/02-strings/01-indexing-lesson.ipynb | Core | 586 | 350–600 | OK |
| course/02-strings/02-methods-lesson.ipynb | Core | 582 | 350–600 | OK |
| course/02-strings/03-formatting-lesson.ipynb | Core | 577 | 350–600 | OK |
| course/02-strings/04-specs-lesson.ipynb | Core | 567 | 350–600 | OK |
| course/02-strings/05-regex-lesson.ipynb | Core | 590 | 350–600 | OK |
| course/03-control-flow/01-decisions-lesson.ipynb | Intermediate | 844 | 600–1000 | OK |
| course/03-control-flow/02-loops-lesson.ipynb | Intermediate | 938 | 600–1000 | OK |
| course/04-collections/01-lists-lesson.ipynb | Core | 589 | 350–600 | OK |
| course/04-collections/02-tuples-lesson.ipynb | Core | 545 | 350–600 | OK |
| course/04-collections/03-dicts-lesson.ipynb | Intermediate | 762 | 600–1000 | OK |
| course/04-collections/04-sets-lesson.ipynb | Intermediate | 701 | 600–1000 | OK |
| course/04-collections/05-zip-lesson.ipynb | Core | 577 | 350–600 | OK |
| course/04-collections/06-copying-lesson.ipynb | Intermediate | 722 | 600–1000 | OK |
| course/05-functions/01-definitions-lesson.ipynb | Core | 542 | 350–600 | OK |
| course/05-functions/02-arguments-lesson.ipynb | Intermediate | 808 | 600–1000 | OK |
| course/05-functions/03-scope-lesson.ipynb | Intermediate | 736 | 600–1000 | OK |
| course/05-functions/04-hints-lesson.ipynb | Core | 570 | 350–600 | OK |
| course/05-functions/05-unpacking-and-keyword-only-lesson.ipynb | Intermediate | 690 | 600–1000 | OK |
| course/06-errors/01-try-except-lesson.ipynb | Intermediate | 760 | 600–1000 | OK |
| course/06-errors/02-raise-lesson.ipynb | Intermediate | 707 | 600–1000 | OK |
| course/06-errors/03-tracebacks-lesson.ipynb | Intermediate | 737 | 600–1000 | OK |
| course/06-errors/04-else-finally-lesson.ipynb | Intermediate | 705 | 600–1000 | OK |
| course/07-iteration/01-comprehensions-lesson.ipynb | Intermediate | 783 | 600–1000 | OK |
| course/07-iteration/02-generators-lesson.ipynb | Deep | 987 | 900–1600 | OK |
| course/07-iteration/03-sorting-lesson.ipynb | Intermediate | 756 | 600–1000 | OK |
| course/07-iteration/04-more-comprehensions-lesson.ipynb | Intermediate | 769 | 600–1000 | OK |
| course/08-collections-module/01-counter-lesson.ipynb | Intermediate | 692 | 600–1000 | OK |
| course/08-collections-module/02-defaultdict-lesson.ipynb | Intermediate | 656 | 600–1000 | OK |
| course/08-collections-module/03-deque-lesson.ipynb | Intermediate | 650 | 600–1000 | OK |
| course/08-collections-module/04-heapq-lesson.ipynb | Intermediate | 700 | 600–1000 | OK |
| course/08-collections-module/05-itertools-lesson.ipynb | Intermediate | 671 | 600–1000 | OK |
| course/08-collections-module/06-bisect-lesson.ipynb | Intermediate | 676 | 600–1000 | OK |
| course/09-recursion/01-base-case-lesson.ipynb | Deep | 1436 | 900–1600 | OK |
| course/09-recursion/02-structures-lesson.ipynb | Deep | 1339 | 900–1600 | OK |
| course/09-recursion/03-limit-lesson.ipynb | Deep | 1402 | 900–1600 | OK |
| course/09-recursion/04-memoization-lesson.ipynb | Deep | 1503 | 900–1600 | OK |
| course/10-pitfalls/01-mutable-defaults-lesson.ipynb | Intermediate | 674 | 600–1000 | OK |
| course/10-pitfalls/02-shared-rows-lesson.ipynb | Intermediate | 652 | 600–1000 | OK |
| course/10-pitfalls/03-identity-lesson.ipynb | Intermediate | 657 | 600–1000 | OK |
| course/10-pitfalls/04-late-binding-lesson.ipynb | Intermediate | 668 | 600–1000 | OK |
| course/10-pitfalls/05-floats-lesson.ipynb | Intermediate | 663 | 600–1000 | OK |
| course/11-classes/01-classes-lesson.ipynb | Intermediate | 708 | 600–1000 | OK |
| course/11-classes/02-dataclasses-lesson.ipynb | Intermediate | 629 | 600–1000 | OK |
| course/11-classes/03-inheritance-lesson.ipynb | Intermediate | 655 | 600–1000 | OK |
| course/11-classes/04-properties-lesson.ipynb | Intermediate | 623 | 600–1000 | OK |
| course/11-classes/05-enums-lesson.ipynb | Intermediate | 603 | 600–1000 | OK |
| course/11-classes/06-custom-exceptions-lesson.ipynb | Intermediate | 600 | 600–1000 | OK |
| course/12-data-model/01-dunder-lesson.ipynb | Intermediate | 709 | 600–1000 | OK |
| course/12-data-model/02-context-managers-lesson.ipynb | Intermediate | 666 | 600–1000 | OK |
| course/12-data-model/03-contextlib-lesson.ipynb | Intermediate | 686 | 600–1000 | OK |
| course/13-modules/01-imports-lesson.ipynb | Intermediate | 701 | 600–1000 | OK |
| course/13-modules/02-main-lesson.ipynb | Intermediate | 660 | 600–1000 | OK |
| course/13-modules/03-packages-lesson.ipynb | Intermediate | 683 | 600–1000 | OK |
| course/14-files/01-paths-lesson.ipynb | Intermediate | 680 | 600–1000 | OK |
| course/14-files/02-json-lesson.ipynb | Intermediate | 624 | 600–1000 | OK |
| course/14-files/03-csv-lesson.ipynb | Intermediate | 633 | 600–1000 | OK |
| course/14-files/04-text-and-bytes-lesson.ipynb | Intermediate | 632 | 600–1000 | OK |
| course/14-files/05-dates-and-times-lesson.ipynb | Intermediate | 633 | 600–1000 | OK |
| course/15-testing/00-pytest-lesson.ipynb | Intermediate | 677 | 600–1000 | OK |
| course/15-testing/01-unittest-lesson.ipynb | Intermediate | 616 | 600–1000 | OK |
| course/15-testing/02-mocking-lesson.ipynb | Intermediate | 653 | 600–1000 | OK |
| course/16-decorators/01-decorators-lesson.ipynb | Deep | 970 | 900–1600 | OK |
| course/17-concurrency/01-threads-lesson.ipynb | Deep | 1018 | 900–1600 | OK |
| course/17-concurrency/02-processes-lesson.ipynb | Deep | 925 | 900–1600 | OK |
| course/17-concurrency/03-async-lesson.ipynb | Deep | 923 | 900–1600 | OK |
| course/17-concurrency/04-race-conditions-lesson.ipynb | Deep | 925 | 900–1600 | OK |
| course/17-concurrency/05-taskgroup-timeouts-lesson.ipynb | Deep | 937 | 900–1600 | OK |
| course/18-tooling/01-tooling-lesson.ipynb | Intermediate | 772 | 600–1000 | OK |
| course/18-tooling/02-protocols-and-generics-lesson.ipynb | Intermediate | 752 | 600–1000 | OK |
| internals/01-objects/01-names-lesson.ipynb | Deep | 1456 | 900–1600 | OK |
| internals/02-mutability/01-aliasing-lesson.ipynb | Deep | 1529 | 900–1600 | OK |
| internals/03-lists/01-dynamic-array-lesson.ipynb | Deep | 1571 | 900–1600 | OK |
| internals/04-dicts/01-hash-table-lesson.ipynb | Deep | 1598 | 900–1600 | OK |
| internals/05-numbers/01-numbers-strings-lesson.ipynb | Deep | 1433 | 900–1600 | OK |
| internals/06-scopes/01-closures-lesson.ipynb | Deep | 1544 | 900–1600 | OK |
| internals/07-iteration/01-protocol-lesson.ipynb | Deep | 1441 | 900–1600 | OK |
| internals/08-attributes/01-lookup-lesson.ipynb | Deep | 1518 | 900–1600 | OK |
| internals/09-imports/01-import-system-lesson.ipynb | Deep | 1525 | 900–1600 | OK |
| internals/10-bytecode/01-bytecode-lesson.ipynb | Deep | 1509 | 900–1600 | OK |
| internals/11-memory/01-refcount-lesson.ipynb | Deep | 1442 | 900–1600 | OK |
| internals/12-gil/01-gil-lesson.ipynb | Deep | 1580 | 900–1600 | OK |
| patterns/01-hash-maps/01-first-unique-lesson.ipynb | Deep | 956 | 900–1600 | OK |
| patterns/01-hash-maps/02-anagram-lesson.ipynb | Deep | 959 | 900–1600 | OK |
| patterns/02-two-pointers/01-sorted-pair-lesson.ipynb | Deep | 979 | 900–1600 | OK |
| patterns/02-two-pointers/02-sorted-squares-lesson.ipynb | Deep | 949 | 900–1600 | OK |
| patterns/02-two-pointers/03-adjacent-lesson.ipynb | Deep | 976 | 900–1600 | OK |
| patterns/03-sliding-window/01-fixed-window-lesson.ipynb | Deep | 949 | 900–1600 | OK |
| patterns/03-sliding-window/02-shortest-window-lesson.ipynb | Deep | 948 | 900–1600 | OK |
| patterns/04-prefix-sums/01-pivot-lesson.ipynb | Deep | 933 | 900–1600 | OK |
| patterns/04-prefix-sums/02-running-sum-lesson.ipynb | Deep | 937 | 900–1600 | OK |
| patterns/04-prefix-sums/03-range-sum-lesson.ipynb | Deep | 961 | 900–1600 | OK |
| patterns/05-binary-search/01-search-insert-lesson.ipynb | Deep | 959 | 900–1600 | OK |
| patterns/05-binary-search/02-min-index-lesson.ipynb | Deep | 977 | 900–1600 | OK |
| patterns/06-stacks/01-backspace-lesson.ipynb | Deep | 933 | 900–1600 | OK |
| patterns/06-stacks/02-next-greater-lesson.ipynb | Deep | 958 | 900–1600 | OK |
| patterns/07-linked-lists/01-traversal-lesson.ipynb | Deep | 922 | 900–1600 | OK |
| patterns/07-linked-lists/02-middle-lesson.ipynb | Deep | 984 | 900–1600 | OK |
| patterns/08-intervals/01-can-attend-lesson.ipynb | Deep | 955 | 900–1600 | OK |
| patterns/09-heaps/01-k-smallest-lesson.ipynb | Deep | 941 | 900–1600 | OK |
| patterns/10-trees/01-traversals-lesson.ipynb | Deep | 931 | 900–1600 | OK |
| patterns/11-graphs/01-island-sizes-lesson.ipynb | Deep | 950 | 900–1600 | OK |
| patterns/11-graphs/02-path-lesson.ipynb | Deep | 923 | 900–1600 | OK |
| patterns/12-backtracking/01-subsets-lesson.ipynb | Deep | 928 | 900–1600 | OK |
| patterns/13-dynamic-programming/01-min-cost-lesson.ipynb | Deep | 975 | 900–1600 | OK |
| patterns/13-dynamic-programming/02-circle-lesson.ipynb | Deep | 927 | 900–1600 | OK |
| patterns/13-dynamic-programming/03-combinations-lesson.ipynb | Deep | 948 | 900–1600 | OK |
| patterns/14-tries/01-trie-lesson.ipynb | Deep | 930 | 900–1600 | OK |
| patterns/15-design/01-tiny-set-lesson.ipynb | Deep | 975 | 900–1600 | OK |
| patterns/16-greedy/01-assign-cookies-lesson.ipynb | Deep | 1021 | 900–1600 | OK |
| patterns/17-union-find/01-count-components-lesson.ipynb | Deep | 1012 | 900–1600 | OK |
| patterns/18-shortest-paths/01-grid-bfs-lesson.ipynb | Deep | 994 | 900–1600 | OK |
| patterns/19-monotonic-deque/01-window-max-lesson.ipynb | Deep | 1000 | 900–1600 | OK |
| patterns/20-binary-search-on-answer/01-smallest-divisor-lesson.ipynb | Deep | 994 | 900–1600 | OK |
| patterns/21-matrix-traversal/01-rotate-lesson.ipynb | Deep | 1026 | 900–1600 | OK |
| patterns/22-bits/01-xor-tricks-lesson.ipynb | Deep | 1026 | 900–1600 | OK |

120 lessons: 120 OK, 0 LOW, 0 HIGH

## Weakest for human review

### Lessons (10)

1. `patterns/16-greedy/01-assign-cookies-lesson.ipynb` — Why section expanded late; sibling problem is thin.
2. `patterns/17-union-find/01-count-components-lesson.ipynb` — same late pad; wants a richer trace table.
3. `patterns/18-shortest-paths/01-grid-bfs-lesson.ipynb` — Dijkstra contrast is short.
4. `patterns/19-monotonic-deque/01-window-max-lesson.ipynb` — equal-value / strictness edge needs a cell.
5. `patterns/22-bits/01-xor-tricks-lesson.ipynb` — renamed helper; confirm practice wording.
6. `course/14-files/03-csv-lesson.ipynb` — sat just under Intermediate floor before pad.
7. `course/14-files/04-text-and-bytes-lesson.ipynb` — same.
8. `course/14-files/05-dates-and-times-lesson.ipynb` — same.
9. `course/17-concurrency/04-race-conditions-lesson.ipynb` — pairs with the new rate-limiter round; worth a cross-link pass.
10. `patterns/13-dynamic-programming/01-min-cost-lesson.ipynb` — Deep and long; check for drift vs challenge DP problems.

### Walkthroughs (5)

1. `solutions/challenges/problems/59-serialize-binary-tree.md` — level-list encoding is a simplification of the classic tree problem.
2. `solutions/challenges/problems/52-kth-smallest-in-bst.md` — solution sorts values from a level list; not a true BST walk.
3. `solutions/challenges/problems/65-time-based-key-value.md` — design problem; confirm binary-search-on-timestamps story.
4. `solutions/challenges/problems/48-clone-graph.md` — graph clone via simplified fixtures.
5. `solutions/challenges/problems/68-meeting-rooms-ii.md` — interval sweep; confirm wording matches “in your own words” constraint.
