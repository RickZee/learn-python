[Home](../README.md) › [Challenges](README.md) › Python questions

# Python questions

Short questions about how Python works. Each answer is the model answer, then the experiment that shows it, then the usual wrong answer. The bank grows with the `internals/` lessons.

## Objects, names, references

From [Objects, names, references](../internals/01-objects/01-names-lesson.ipynb).

### What does `is` compare?

`is` compares identity: whether two names point at the same object. That is the same question as `id(a) == id(b)`. It does not walk the contents. `==` does, by asking the objects whether they count as equal. Use `is` for `None` and `==` for values.

Experiment: the predict cell, where one list is `is` the other and a newly built equal list is not ([lesson](../internals/01-objects/01-names-lesson.ipynb)).

Usual wrong answer: "`is` is a stricter `==`" or "`is` means the values match."

### Why does appending through one name change the other?

Assignment stores a pointer. `right = left` writes the same pointer into a second name. `append` mutates the one list both pointers reach, so `left` sees the new element. Nothing copied the list. Rebinding `right` to a new list would leave `left` alone, because that write touches only one namespace slot.

Experiment: the evidence cell that prints `left is right` before the append, after the append, and after rebinding ([lesson](../internals/01-objects/01-names-lesson.ipynb)).

Usual wrong answer: "assignment copies, so the other name cannot change."

### Why is `a is b` a bad test that two numbers are equal?

Equal numbers can be two objects, and `is` will say false. CPython sometimes keeps one object for a small integer, so the test can also say true for a reason you must not depend on. The cache is an implementation detail. `==` asks whether the values count as equal, which is the question you meant.

Experiment: the volatile cell labelled as a CPython detail. Run it, then change the magnitude ([lesson](../internals/01-objects/01-names-lesson.ipynb)).

Usual wrong answer: "small integers are always identical, so `is` is fine for ints."

### Does `list(samples)` share the inner lists?

`list(samples)` allocates a new outer list and copies the pointers that were in the old one. The outer list is a different object. If an element is itself a list, that inner list object is still shared, and mutating it is visible through both outer lists. One level was copied. Nested structure was not.

Experiment: build `[[1]]`, copy it with `list`, append to the inner list, and print both outer lists. Compare with the snapshot in the worked example, which only needed one level ([lesson](../internals/01-objects/01-names-lesson.ipynb)).

Usual wrong answer: "`list(samples)` is a deep copy."

## Mutability and aliasing

From [Mutability and aliasing](../internals/02-mutability/01-aliasing-lesson.ipynb).

### If a function appends to its list parameter, does the caller see it?

Yes. The parameter is another name for the caller's object. `append` mutates that object. The caller's name still points at it, so the new element is visible after the call returns. No copy happened at the call.

Experiment: `accumulate` in the predict cell. The list grows from `[1]` to `[1, 2]` ([lesson](../internals/02-mutability/01-aliasing-lesson.ipynb)).

Usual wrong answer: "arguments are copied, so the caller is isolated."

### Why doesn't `readings = readings + [sample]` update the caller?

`+` allocates a new list. The assignment stores that pointer in the parameter slot, which lives in the callee's frame. The caller's slot is a different namespace entry and is not written. Unless the function returns the new list, the caller keeps the original pointer.

Experiment: `rebind` in the same predict cell. The caller's list stays `[1, 2]` ([lesson](../internals/02-mutability/01-aliasing-lesson.ipynb)).

Usual wrong answer: "assigning the parameter assigns the caller's variable."

### What does a shallow copy share?

The new container is a different object. The pointers inside it are the old ones, so mutable elements are shared. Appending to an inner list is visible through both outer lists. `list(grid)`, `grid.copy()`, `grid[:]`, and `copy.copy(grid)` all do this.

Experiment: the evidence cell that prints `grid[0] is shallow[0]` and then appends through the shallow copy ([lesson](../internals/02-mutability/01-aliasing-lesson.ipynb)).

Usual wrong answer: "any copy protects the whole structure."

### How does `deepcopy` handle a list that contains itself?

It copies each object once and remembers the copy by identity. When it reaches the self-reference, it points the new list at the new list instead of walking forever. Identity, not equality, is the key, because two equal objects can still be different objects that both need copying.

Experiment: the cell that builds `loop`, appends `loop` to itself, and prints `cloned[1] is cloned` ([lesson](../internals/02-mutability/01-aliasing-lesson.ipynb)).

Usual wrong answer: "a cycle makes `deepcopy` recurse until `RecursionError`."

## How `list` works

From [How list works](../internals/03-lists/01-dynamic-array-lesson.ipynb).

### Why is `append` usually cheap?

The list keeps spare slots past its length. `append` writes one pointer into a free slot. When the slots run out, the list allocates a larger block and copies the pointers once. Those copies are rare enough that, across a long series of appends, the work per append stays constant. One append that grows the block costs more than its neighbors, and the average is what "cheap" means.

Experiment: the volatile `getsizeof` cell. The size stays flat across several appends, then jumps ([lesson](../internals/03-lists/01-dynamic-array-lesson.ipynb)).

Usual wrong answer: "every append copies the whole list."

### Why is `insert(0, x)` slow on a long list?

The pointer block is contiguous, so a new front item has to sit at the start. Every live pointer shifts one slot right. A list of length n moves n pointers. Repeating that for every new item moves on the order of n² pointers. `append` writes at the end and shifts nothing.

Experiment: the volatile timing cell, append versus insert at the front, and the predict cell that prints `[3, 2, 1]` ([lesson](../internals/03-lists/01-dynamic-array-lesson.ipynb)).

Usual wrong answer: "insert at the front is like append, just at the other end."

### What does `sys.getsizeof` on a list leave out?

It reports the list header and the pointer block, including spare slots. It does not follow the pointers. The integers, strings, or inner lists live elsewhere, and a shallow copy can share them. Two lists with the same `getsizeof` can point at different amounts of data.

Experiment: build a list of one large nested list and compare `getsizeof` of the outer list with the nested structure you know is there. The dynamic-array lesson states this limit next to the size table ([lesson](../internals/03-lists/01-dynamic-array-lesson.ipynb)).

Usual wrong answer: "`getsizeof` is the total memory of the list and everything in it."

### Why is `x in some_list` a scan?

A list has no index from value to slot. `in` walks the live pointers and uses `==`. Worst case it looks at every element. A set answers membership with a hash table. The list keeps order and duplicates, which the set gives up.

Experiment: the timing cell's contains measurement, on a list long enough that the scan is visible next to append ([lesson](../internals/03-lists/01-dynamic-array-lesson.ipynb)).

Usual wrong answer: "membership on a list is a hash lookup, like a dict."

## How `dict` and `set` work

From [How dict and set work](../internals/04-dicts/01-hash-table-lesson.ipynb).

### What does a hash table use the hash for?

The hash is an integer that picks a starting slot in an array. The lookup then compares keys with `==` in that slot and the next ones, until it finds an equal key or an empty slot. The average lookup is short because many slots are empty. The worst case, one long collision chain, is a scan.

Experiment: the scoreboard cell, where a second `Player(4)` finds the entry stored under a different object with the same hash and equality ([lesson](../internals/04-dicts/01-hash-table-lesson.ipynb)).

Usual wrong answer: "the hash is the key, so equal hashes always mean the same key."

### Why is a key lost if its hash changes after insertion?

The entry stays in the slot chosen by the old hash. Lookup uses the new hash and starts in a different slot, so it never compares the stored key. `len` does not change, because nothing deleted the entry. The address is stale.

Experiment: the common-mistake cell. After `player_id` changes, `in` is false and the length is still 1 ([lesson](../internals/04-dicts/01-hash-table-lesson.ipynb)).

Usual wrong answer: "the dict notices the change and moves the entry."

### Why does defining `__eq__` make a class unhashable unless you also define `__hash__`?

The default hash is identity. If equality uses a field, two equal objects that are not the same object would hash differently, and the table would miss them. Python sets `__hash__` to `None` when you define `__eq__` and not `__hash__`, so the mistake fails immediately instead of corrupting a set.

Experiment: define equality on a field, leave `__hash__` out, and put an instance in a dict. You get `TypeError` ([lesson](../internals/04-dicts/01-hash-table-lesson.ipynb)).

Usual wrong answer: "you only need `__eq__` to use an object as a key."

### Why does updating a dict value not move the key?

Order is first insertion. The key is already in the table, so the assignment replaces the value in that entry and does not record a new position. Iteration order stays put.

Experiment: the predict cell. `ada` stays first after its value changes from 1 to 3 ([lesson](../internals/04-dicts/01-hash-table-lesson.ipynb)).

Usual wrong answer: "dicts are unordered" or "an update moves the key to the end."

## Numbers and strings

From [Numbers and strings](../internals/05-numbers/01-numbers-strings-lesson.ipynb).

### Why is `0.1 + 0.2 == 0.3` false?

A float stores a fixed binary fraction. `0.1` is not a sum of powers of one-half, so the stored value is the nearest binary value. Adding two such approximations need not land on the binary value stored for `0.3`. The error is small and real. Display rounding hides it, and `==` does not.

Experiment: the evidence cell prints the comparison and `float.hex` for `0.1`, the sum, and `0.3` ([lesson](../internals/05-numbers/01-numbers-strings-lesson.ipynb)).

Usual wrong answer: "decimal fractions are exact in a float" or "it is a Python bug."

### When does `Decimal` still get `0.1` wrong?

`Decimal(0.1)` copies the float, which is already rounded. The decimal digits you wanted were never in that float. `Decimal("0.1")` parses the characters and keeps base-10 digits, so adding `"0.2"` lands on `"0.3"`.

Experiment: the common-mistake cell versus the fix cell ([lesson](../internals/05-numbers/01-numbers-strings-lesson.ipynb)).

Usual wrong answer: "wrapping the addition in Decimal repairs a float."

### Why can an `int` hold `2**100` exactly?

The integer is a sign plus a growable array of digits. Extra magnitude allocates more digits instead of wrapping at a fixed width. The result is exact. Arithmetic then takes time proportional to the number of digits, so the unlimited range is not free.

Experiment: the predict cell prints `2**100` as a positive integer ([lesson](../internals/05-numbers/01-numbers-strings-lesson.ipynb)).

Usual wrong answer: "integers wrap at 32 or 64 bits."

### Why does `replace` leave the original string unchanged?

A string's code points cannot be overwritten. `replace` allocates a new string. Every name that still points at the original sees the old text. Immutability is also why a string can be a dict key: the hash cannot be invalidated by a later write.

Experiment: the cell that prints the replaced text, the original, and `updated is name` ([lesson](../internals/05-numbers/01-numbers-strings-lesson.ipynb)).

Usual wrong answer: "string methods edit the string in place."

## Scopes and closures

From [Scopes and closures](../internals/06-scopes/01-closures-lesson.ipynb).

### What does a closure capture?

It captures the variable, stored in a cell, not the value at the moment `def` runs. The inner function reads the cell when it is called. Several functions created in one loop share that cell, so they all see whatever value is left when they run. `function.__closure__[0].cell_contents` is the current object in the cell.

Experiment: the predict cell prints `[2, 2, 2]`, and the counter cell prints `cell_contents` before and after `nonlocal` updates ([lesson](../internals/06-scopes/01-closures-lesson.ipynb)).

Usual wrong answer: "a nested function copies the outer variable's value when it is defined."

### Why does assigning a name anywhere in a function make it local?

The compiler marks the name local if the body binds it. Every use of that name in the function loads the local slot, including a read that appears above the assignment. If the slot has not been written yet, Python raises `UnboundLocalError` instead of continuing the LEGB search.

Experiment: `surprise` in the lesson reads `n` and then assigns it. The cell raises `UnboundLocalError` ([lesson](../internals/06-scopes/01-closures-lesson.ipynb)).

Usual wrong answer: "Python looks up a global if the local has not been assigned yet."

### What do `global` and `nonlocal` change?

`global` means assignment writes the module slot, not a new local. `nonlocal` means assignment writes an enclosing function's cell. Reading a global needs no keyword. `nonlocal` requires that an enclosing function already uses that name. Neither keyword looks through a class body.

Experiment: the counter cell. `bump` increments `count` after `counter` has returned, and `cell_contents` follows the new integer ([lesson](../internals/06-scopes/01-closures-lesson.ipynb)).

Usual wrong answer: "`global` is how you read any variable from outside the function."

### Why does a comprehension in a class body not see the class's names?

A comprehension runs as a nested function. LEGB does not include the class body that is currently executing, because a class body is not an enclosing function. The name exists in the temporary class dict, and the comprehension never looks there. A method later reads the attribute off the instance instead.

Experiment: the `Room` cell raises `NameError` for `code` even though the line above assigned it ([lesson](../internals/06-scopes/01-closures-lesson.ipynb)).

Usual wrong answer: "the class body is a scope, so nested code can see its variables."

## The iteration protocol

From [The iteration protocol](../internals/07-iteration/01-protocol-lesson.ipynb).

### What does `for` actually call?

It calls `iter` once on the object, then `next` on the iterator until that raises `StopIteration`. Any other exception escapes. The container and the cursor are different objects when the container's `__iter__` returns a new iterator. `for` is that loop with the end exception hidden.

Experiment: `first_positive` is the loop written out. It returns on the first positive value and never pulls the rest ([lesson](../internals/07-iteration/01-protocol-lesson.ipynb)).

Usual wrong answer: "`for` indexes from 0 to `len`."

### Why is a generator empty the second time you loop it?

A generator's `__iter__` returns itself. The first loop runs the frame until it returns, and `gi_frame` becomes `None`. The second loop asks the same object for more values and gets the end immediately. Calling the generator function again builds a new frame.

Experiment: the predict cell prints `[2, 1]` and then `[]`. The evidence cell shows the frame still alive after the two yields, then `None` once `StopIteration` ends it. A fresh call walks again ([lesson](../internals/07-iteration/01-protocol-lesson.ipynb)).

Usual wrong answer: "a generator is a list that can be replayed."

### What does `yield from` do?

It runs the iteration protocol on another iterator. Values from that iterator are yielded as this generator's values. When the other iterator raises `StopIteration`, `yield from` ends and the outer generator continues. It is the nested `next` loop, written as one expression.

Experiment: `chain([[1, 2], [3]])` prints `[1, 2, 3]` ([lesson](../internals/07-iteration/01-protocol-lesson.ipynb)).

Usual wrong answer: "`yield from` copies the other sequence into a list first."

### Why can two loops share a list but not a generator?

Each `for` on a list calls `iter`, and the list returns a fresh iterator with its own index. A generator is already an iterator and will not make a second one. The list pays a small iterator object per loop. The generator's one frame is the cursor.

Experiment: call `positives(readings)` twice in the fix cell. Both prints are `[4, 9]`. One saved generator, in the mistake cell, prints `[4, 9]` and then `[]` ([lesson](../internals/07-iteration/01-protocol-lesson.ipynb)).

Usual wrong answer: "the second loop fails because the list was consumed."

## Attribute lookup

From [Attribute lookup](../internals/08-attributes/01-lookup-lesson.ipynb).

### Where does `obj.name` look?

The instance `__dict__` first, then the class, then each class in the method resolution order. The first hit wins. An instance assignment shadows a class attribute without deleting it. Other instances that never assigned the name still find the class value.

Experiment: the predict cell. `Child` overrides `label`, the instance stores `note`, and `ping` is found on `Base` ([lesson](../internals/08-attributes/01-lookup-lesson.ipynb)).

Usual wrong answer: "the search starts on the class where the method was defined."

### What does `super()` call?

The next class in the MRO of `type(self)`, after the class whose method is running. It is not "my first base". In a diamond `D(B, C)` with both `B` and `C` inheriting `A`, `B.ping`'s `super()` reaches `C` when `self` is a `D`, and reaches `A` when `self` is a `B`.

Experiment: `D.__mro__` prints `D, B, C, A, object`, and `D().ping()` prints `D B C A` ([lesson](../internals/08-attributes/01-lookup-lesson.ipynb)).

Usual wrong answer: "`super()` means the parent I named in the class line."

### How is a function on a class different from a bound method?

The function object lives on the class once. Looking it up on an instance calls its `__get__` and returns a bound method that holds the instance. Each lookup builds a new bound method, so `obj.method is obj.method` is false. A `property` uses the same descriptor hook to run a getter.

Experiment: the predict cell prints that `ping.__self__` is the instance and that two lookups are not the same object. The property cell prints the value while `"n" in reading.__dict__` is false ([lesson](../internals/08-attributes/01-lookup-lesson.ipynb)).

Usual wrong answer: "methods are copied onto each instance."

### What does `__slots__` remove?

The per-instance `__dict__`. Listed names live in fixed fields on the object. An unlisted name raises `AttributeError`. The object is smaller, which matters for a very large number of instances and not for a few. Multiple inheritance with slots is awkward, so slots are an optimization, not a default.

Experiment: the volatile cell prints `False` for `hasattr(slotted, "__dict__")` and `True` for a normal instance, plus `getsizeof` numbers that depend on the build ([lesson](../internals/08-attributes/01-lookup-lesson.ipynb)).

Usual wrong answer: "`__slots__` is how you make attributes private."

## The import system

From [The import system](../internals/09-imports/01-import-system-lesson.ipynb).

### Why doesn't a second import run the file again?

The first import stores the module object in `sys.modules` before the file finishes, and the second import returns that object. Top-level code does not run again. An attribute you attached is still there. Editing the file on disk changes nothing until the process restarts or something calls `reload`.

Experiment: the predict cell sets `json.marker` and imports `json` again. The same object still has `marker` ([lesson](../internals/09-imports/01-import-system-lesson.ipynb)).

Usual wrong answer: "every import executes the module from the top."

### What does `from module import name` actually bind?

Your local name points at the object that attribute was at that moment. It is not a live view. After `reload`, the module attribute may be a new object while your name still holds the old one. An integer copied this way stays the old integer.

Experiment: the common-mistake cell prints the copied rate and `rate.rate` after the file changes and reload runs. They differ ([lesson](../internals/09-imports/01-import-system-lesson.ipynb)).

Usual wrong answer: "`from` keeps a link, so reload updates every importer."

### Why can an old function see a global that reload just changed?

The old function object is not the new one, so `get is module.get` is false. Its `__globals__` is still the module dictionary. Reload executes into that same dictionary, so a global read inside the old function sees the new assignment. The function object is stale. The namespace it reads is not.

Experiment: the evidence cell prints `get is rate.get` as false and `get()` as the new rate ([lesson](../internals/09-imports/01-import-system-lesson.ipynb)).

Usual wrong answer: "reload rebuilds every function that was imported, or the old function is frozen with the old globals."

### Why does a circular import see a half-initialized module?

Import puts the module object into `sys.modules` before running the file. The other module's import finds that entry and does not start a second copy. Names that have not been assigned yet are missing, so the use raises `AttributeError` and the message mentions a circular import. Move the use below both modules' definitions, or import inside the function that needs it.

Experiment: the cell that writes `left.py` and `right.py` prints `AttributeError` and that the message contains `circular import` ([lesson](../internals/09-imports/01-import-system-lesson.ipynb)).

Usual wrong answer: "Python detects the cycle and skips the second import."

## Source to bytecode

From [Source to bytecode](../internals/10-bytecode/01-bytecode-lesson.ipynb).

### What does `compile` return?

A code object: bytecode plus tables of names and constants. It does not run the source. `co_names` lists global and attribute names. `co_varnames` lists locals. Executing the code object is a later step.

Experiment: the predict cell prints the type name `code` and `co_names` of `('answer',)` for `answer = 1 + 2`. The notebook never binds `answer` ([lesson](../internals/10-bytecode/01-bytecode-lesson.ipynb)).

Usual wrong answer: "`compile` runs the code and returns the result."

### Why is a local faster to load than a global?

The compiler gives each local an index into the frame's array. The load is that index. A global load looks a string up in the module dictionary, and then in builtins on a miss. A loop repeats the load once per pass. Copying a global into a local moves the dictionary lookup to a single instruction before the loop.

Experiment: `with_global` keeps `base` in `co_names`. `with_local` puts `local_base` in `co_varnames`. The volatile `dis` cell shows the local load versus `LOAD_GLOBAL`, and the timing cell measures the gap ([lesson](../internals/10-bytecode/01-bytecode-lesson.ipynb)).

Usual wrong answer: "locals and globals are both dictionary lookups."

### What is a `.pyc` file?

A cache of the code object, under `__pycache__`, so a later process can skip parsing when the source has not changed. It is not a copy of the module's data. If the cache looks newer than the source, import may ignore an edit made in the same second.

Experiment: importing a freshly written module prints that `__cached__` ends with `.pyc` and contains `__pycache__` ([lesson](../internals/10-bytecode/01-bytecode-lesson.ipynb)).

Usual wrong answer: "Python interprets the `.py` source from scratch on every import."

### Why do two calls to a `global` counter return 3 and then 6?

`global` stores the name in `co_names`. Each assignment writes the module dictionary, not a slot that dies with the call. The second call starts from the integer the first call left behind. A local `total = 0` inside the function gives each call its own slot, and both calls return 3.

Experiment: the common-mistake cell prints `3`, `6`, and that `total` is in `co_names`. The fix prints `3`, `3`, and that `total` is in `co_varnames` ([lesson](../internals/10-bytecode/01-bytecode-lesson.ipynb)).

Usual wrong answer: "each call starts from the module value but the function's writes stay inside the call."

## Memory management

From [Memory management](../internals/11-memory/01-refcount-lesson.ipynb).

### When does CPython free an object?

When the count of references reaches zero. A name, a slot in a list or dict, and a frame each count. Rebinding a name, dropping a container entry, or returning from a frame decrements. `del` only drops the name you named, so another reference keeps the object. This is a CPython detail: other implementations may not use reference counts.

Experiment: the predict cell. Binding a second name raises `sys.getrefcount` by 1, once the temporary reference inside each call is subtracted out ([lesson](../internals/11-memory/01-refcount-lesson.ipynb)).

Usual wrong answer: "`del` destroys the object."

### Why does a cycle survive `del`?

Each object still points at the other, so neither count reaches zero. Reference counting cannot see that the group is unreachable from your code. `gc.collect` finds groups that only point inside themselves and frees them. A `weakref` does not count, so it becomes `None` when that happens and does not itself keep the cycle alive.

Experiment: after `del` of both nodes, the weak reference is still live. After `gc.collect`, it is `None`. A node that is not in a cycle dies at `del` with no collect ([lesson](../internals/11-memory/01-refcount-lesson.ipynb)).

Usual wrong answer: "`del` runs the garbage collector."

### Why is `__del__` the wrong place to close a file?

It runs, if it runs, only when the count hits zero. A leftover name, a cycle, or interpreter shutdown can delay it or skip it. Several `__del__` methods have no promised order. `finally` and `with` run at the end of the block, including when the block raises, while you may still hold a name.

Experiment: the worked example sets `handle.closed` in `finally` after a `ValueError`, then still prints `closed` because the name exists ([lesson](../internals/11-memory/01-refcount-lesson.ipynb)).

Usual wrong answer: "`__del__` is Python's `finally`."

### What does a weak reference change about the count?

Nothing. It does not increment, and when the object is freed, calling the weak reference returns `None`. Use it for a cache that should not keep keys alive. Do not use it as a second ordinary name. You must handle `None`.

Experiment: `weakref.ref` on the cycle nodes stays live until `gc.collect`, then returns `None`. On an object that is not in a cycle, `del` of the only name makes the weak reference `None` immediately ([lesson](../internals/11-memory/01-refcount-lesson.ipynb)).

Usual wrong answer: "a weak reference is a reference that does not get counted, so the object leaks."

## The GIL and free-threading

From [The GIL and free-threading](../internals/12-gil/01-gil-lesson.ipynb).

### Does the GIL make `x += 1` thread-safe?

No. The statement is a load, an add, and a store, and the GIL can switch threads between those instructions. Both threads can read the old value and write the same result back, so one update is lost. A `Lock` must cover the whole update. A free-threaded build removes the serialization of bytecode and makes this easier to hit, not harder.

Experiment: two threads read a shared `0`, wait on a barrier, then each store `seen + 1`. The print is `1`. The locked version prints `2` ([lesson](../internals/12-gil/01-gil-lesson.ipynb)).

Usual wrong answer: "the GIL makes increments atomic."

### What does the GIL protect?

The interpreter's own structures on the usual build: one thread runs Python bytecode at a time, so C code inside the interpreter can update reference counts without a lock on every object. It does not protect your counters, lists, or dicts against logical races. Extensions can release it around I/O and around some C work.

Experiment: `sys._is_gil_enabled` on the usual build, in the volatile cell. The sleep cell shows waits overlapping because sleep releases the lock ([lesson](../internals/12-gil/01-gil-lesson.ipynb)).

Usual wrong answer: "the GIL is a lock around your data."

### When do threads help, and when do processes?

Threads help when the work releases the GIL: I/O, sleep, and many C libraries that drop the lock. They do not speed up pure Python bytecode on a build where the GIL stays on, because only one thread runs it. A process has its own interpreter and can use another core. It pays startup and must pickle what it sends. A short task can be slower in a process than in a thread even when the work is CPU-bound.

Experiment: the lesson's volatile timings. Read them as measurements of this machine, including process startup if you add one, not as a fixed ranking ([lesson](../internals/12-gil/01-gil-lesson.ipynb)).

Usual wrong answer: "more threads always use more cores."

### What is `concurrent.interpreters` for?

Separate interpreters in one process. They do not share the main interpreter's module globals. You pass messages. Each interpreter has its own GIL behavior. It does not make a shared `+=` atomic, because the point is that they do not share that variable.

Experiment: `hasattr(concurrent.interpreters, "create")` is true in this lesson's cell ([lesson](../internals/12-gil/01-gil-lesson.ipynb)).

Usual wrong answer: "subinterpreters are threads with the GIL turned off."

**Next:** [Challenges](README.md)
