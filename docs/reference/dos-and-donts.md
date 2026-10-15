[Home](../../README.md) › [Docs](../README.md) › Dos and don'ts

# Dos and don'ts

The mistakes that catch most learners, each with the lesson that explains it. Skim this before you review your own code.

## Defaults and sharing

**Don't** use a list, dict, or set as a default argument. It is created once and shared by every call.

```python
def add(item, bucket=[]):  # don't
    bucket.append(item)
    return bucket

def add(item, bucket=None):  # do
    bucket = [] if bucket is None else bucket
    bucket.append(item)
    return bucket
```

Lessons: [mutable defaults](../../course/10-pitfalls/01-mutable-defaults-lesson.ipynb), [shared rows](../../course/10-pitfalls/02-shared-rows-lesson.ipynb).

**Don't** build a grid with `[[0] * 3] * 3`. All rows are the same list. **Do** use `[[0] * 3 for _ in range(3)]`.

## Identity and equality

**Don't** use `is` to compare values. It checks whether two names point at one object. **Do** use `==`, and keep `is` for `None`. See [identity](../../course/10-pitfalls/03-identity-lesson.ipynb).

## Errors

**Don't** write a bare `except:`. It also catches `KeyboardInterrupt`. **Do** catch the specific error you expect. See [try and except](../../course/06-errors/01-try-except-lesson.ipynb).

**Don't** swallow an error with `pass`. **Do** handle it, log it, or let it propagate.

**Do** re-raise with `raise NewError(...) from err` so the original cause stays visible. See [raise](../../course/06-errors/02-raise-lesson.ipynb).

## Loops and collections

**Don't** change a list while you loop over it. **Do** loop over a copy, or build a new list. See [mutating while looping](../../course/10-pitfalls/06-mutating-while-looping-lesson.ipynb).

**Don't** loop with `range(len(items))` just to get the item. **Do** loop over `items`, or use `enumerate`.

**Don't** name a variable after a built-in (`list`, `sum`, `max`, `id`). It hides the built-in until you `del` your name. Same lesson as above.

**Don't** build a list by hand to loop over it once. **Do** use a generator expression.

**Do** use `zip(a, b, strict=True)` when the lengths must match.

## Numbers and money

**Don't** compare floats with `==`. **Do** use `math.isclose`. See [floats](../../course/10-pitfalls/05-floats-lesson.ipynb).

**Don't** store money in a float. **Do** use `Decimal` or whole cents.

## Scope

**Don't** rely on a loop variable inside a closure you create in the loop. All closures see the last value. See [late binding](../../course/10-pitfalls/04-late-binding-lesson.ipynb).

**Don't** use `global` to pass data around. **Do** pass arguments and return values.

## Files and text

**Do** open files with `with`, so they close even when an error occurs.

**Do** pass `encoding="utf-8"` when you read or write text.

## Habits

- **Do** run the code to check a claim. Don't trust your memory.
- **Do** read the whole traceback, from the bottom up.
- **Don't** copy a solution you can't explain.

**See also:** [Style guide](style-guide.md) · [Resources](resources.md)
