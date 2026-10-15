[Home](../../README.md) › [Docs](../README.md) › Course map


# Language map

Part 1 is notebooks. Part 2 adds an `exercise/` folder. Patterns live in `patterns/`.

Each link opens the first lesson. Contrast notes: [experienced path](../paths/experienced.md).

## Part 1

| Folder | You learn |
| --- | --- |
| [00-start](../../course/00-start/01-first-program-lesson.ipynb) | `print`, a first error, then `def`, `return`, and `check` |
| [01-basics](../../course/01-basics/01-names-lesson.ipynb) | Names, numbers, `True` / `False` / `None` |
| [02-strings](../../course/02-strings/01-indexing-lesson.ipynb) | Indexes, methods, f-strings, format specs, `re` |
| [03-control-flow](../../course/03-control-flow/01-decisions-lesson.ipynb) | `match`, `for`, `while` |
| [04-collections](../../course/04-collections/01-lists-lesson.ipynb) | Lists, tuples, dicts, sets, `zip`, `enumerate`, copying |
| [05-functions](../../course/05-functions/01-definitions-lesson.ipynb) | Definitions, arguments, scope, docstrings and hints, unpacking and keyword-only |
| [06-errors](../../course/06-errors/01-try-except-lesson.ipynb) | `try` / `except` / `else` / `finally`, `raise`, tracebacks |
| [07-iteration](../../course/07-iteration/01-comprehensions-lesson.ipynb) | List, dict, and set comprehensions, generators, `sorted` and `lambda` |
| [08-collections-module](../../course/08-collections-module/01-counter-lesson.ipynb) | `Counter`, `defaultdict`, `deque`, `heapq`, itertools, `cache`, `bisect` |
| [09-recursion](../../course/09-recursion/01-base-case-lesson.ipynb) | Base case, nested data, the call-stack limit, memoization |
| [10-pitfalls](../../course/10-pitfalls/01-mutable-defaults-lesson.ipynb) | Shared defaults, shared rows, `is`, late binding, `Decimal`, changing a list while you loop |
| [11-classes](../../course/11-classes/01-classes-lesson.ipynb) | `class`, `__repr__`, `__eq__`, dataclasses, inheritance, properties, enums, a custom exception |
| [12-data-model](../../course/12-data-model/01-dunder-lesson.ipynb) | dunders, `with`, `contextlib` |

## Part 2

| Folder | You learn |
| --- | --- |
| [13-modules](../../course/13-modules/01-imports-lesson.ipynb) | `import`, `__main__`, packages, `uv add` |
| [14-files](../../course/14-files/01-paths-lesson.ipynb) | Paths, JSON, CSV, text/bytes, dates |
| [15-testing](../../course/15-testing/00-pytest-lesson.ipynb) | pytest, tests, mocking |
| [16-decorators](../../course/16-decorators/01-decorators-lesson.ipynb) | Wrappers, class decorators, cache, `partial` |
| [17-concurrency](../../course/17-concurrency/01-threads-lesson.ipynb) | Threads, processes, async, races, TaskGroup |
| [18-tooling](../../course/18-tooling/01-tooling-lesson.ipynb) | ruff, logging, readable code, Protocols, generics, TypedDict |

## How Python works

Internals lessons: experiments, cost, link back to the course. See also the [question bank](../../challenges/python-questions.md).

| Lesson | You learn |
| --- | --- |
| [Objects, names, references](../../internals/01-objects/01-names-lesson.ipynb) | Names are pointers. `is` is identity. |
| [Mutability and aliasing](../../internals/02-mutability/01-aliasing-lesson.ipynb) | Call by sharing, shallow copy, `deepcopy` |
| [How list works](../../internals/03-lists/01-dynamic-array-lesson.ipynb) | The pointer block, `append`, `insert(0)` |
| [How dict and set work](../../internals/04-dicts/01-hash-table-lesson.ipynb) | The hash contract and insertion order |
| [Numbers and strings](../../internals/05-numbers/01-numbers-strings-lesson.ipynb) | Big ints, binary floats, immutable text |
| [Scopes and closures](../../internals/06-scopes/01-closures-lesson.ipynb) | LEGB, cells, late binding |
| [The iteration protocol](../../internals/07-iteration/01-protocol-lesson.ipynb) | `iter`, `next`, generators |
| [Attribute lookup](../../internals/08-attributes/01-lookup-lesson.ipynb) | The MRO, descriptors, `__slots__` |
| [The import system](../../internals/09-imports/01-import-system-lesson.ipynb) | `sys.modules`, `reload`, cycles |
| [Source to bytecode](../../internals/10-bytecode/01-bytecode-lesson.ipynb) | Code objects, locals versus globals |
| [Memory management](../../internals/11-memory/01-refcount-lesson.ipynb) | Reference counts, cycles, `weakref` |
| [The GIL and free-threading](../../internals/12-gil/01-gil-lesson.ipynb) | What the lock does not make atomic |

## Challenge patterns

Use beside [challenge practice](../guides/challenge-practice.md).

| Folder | Pattern |
| --- | --- |
| [01-hash-maps](../../patterns/01-hash-maps/01-first-unique-lesson.ipynb) | Complements and grouping |
| [02-two-pointers](../../patterns/02-two-pointers/01-sorted-pair-lesson.ipynb) | Sorted pairs, sorted squares, adjacent values |
| [03-sliding-window](../../patterns/03-sliding-window/01-fixed-window-lesson.ipynb) | A fixed window, then a window that grows and shrinks |
| [04-prefix-sums](../../patterns/04-prefix-sums/01-pivot-lesson.ipynb) | A pivot index, running sums, a range sum |
| [05-binary-search](../../patterns/05-binary-search/01-search-insert-lesson.ipynb) | Sorted search, then the minimum index |
| [06-stacks](../../patterns/06-stacks/01-backspace-lesson.ipynb) | Backspace compare, then the next greater value |
| [07-linked-lists](../../patterns/07-linked-lists/01-traversal-lesson.ipynb) | Walk a chain, then find its middle |
| [08-intervals](../../patterns/08-intervals/01-can-attend-lesson.ipynb) | Sort, then merge |
| [09-heaps](../../patterns/09-heaps/01-k-smallest-lesson.ipynb) | The k smallest values, then the last stone |
| [10-trees](../../patterns/10-trees/01-traversals-lesson.ipynb) | Preorder, inorder, and whether two trees match |
| [11-graphs](../../patterns/11-graphs/01-island-sizes-lesson.ipynb) | Flood fill, then a path along edges |
| [12-backtracking](../../patterns/12-backtracking/01-subsets-lesson.ipynb) | Subsets, then letter case |
| [13-dynamic-programming](../../patterns/13-dynamic-programming/01-min-cost-lesson.ipynb) | Min cost, a circle of houses, combinations |
| [14-tries](../../patterns/14-tries/01-trie-lesson.ipynb) | A tree of letters, then a shared prefix |
| [16-greedy](../../patterns/16-greedy/01-assign-cookies-lesson.ipynb) | Assign cookies / lemonade |
| [17-union-find](../../patterns/17-union-find/01-count-components-lesson.ipynb) | Components / path exists |
| [18-shortest-paths](../../patterns/18-shortest-paths/01-grid-bfs-lesson.ipynb) | Grid BFS / effort |
| [19-monotonic-deque](../../patterns/19-monotonic-deque/01-window-max-lesson.ipynb) | Window max/min |
| [20-binary-search-on-answer](../../patterns/20-binary-search-on-answer/01-smallest-divisor-lesson.ipynb) | Divisor / ship capacity |
| [21-matrix-traversal](../../patterns/21-matrix-traversal/01-rotate-lesson.ipynb) | Rotate / diagonals |
| [22-bits](../../patterns/22-bits/01-xor-tricks-lesson.ipynb) | XOR / bit counts |
| [15-design](../../patterns/15-design/01-tiny-set-lesson.ipynb) | A small set that drops the oldest key |

Style and common mistakes: [Style guide](style-guide.md) · [Dos and don'ts](dos-and-donts.md) · [Resources](resources.md).

Next: [challenge practice](../guides/challenge-practice.md).

**Next:** [Challenge practice](../guides/challenge-practice.md)
