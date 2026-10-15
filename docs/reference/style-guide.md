[Home](../../README.md) › [Docs](../README.md) › Style guide

# Style guide

How code in this repo looks. Follow it in your own exercises so the checks and the linter stay quiet.

## The short version

Python's official style is [PEP 8](https://peps.python.org/pep-0008/). This repo follows it, and `ruff` enforces the parts a machine can check. The lesson [Readable code](../../course/18-tooling/03-readable-code-lesson.ipynb) teaches it hands-on. Run ruff with:

```bash
uv run ruff check .
```

## Names

| Thing | Style | Example |
| --- | --- | --- |
| Variable, function, method, module | `snake_case` | `word_count`, `read_rows` |
| Class, exception | `CapWords` | `ShoppingCart`, `ParseError` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Internal helper | leading underscore | `_normalize` |

- Use names that say what the value is: `prices`, not `lst`.
- Don't use one-letter names except for short loop counters such as `i`, or `x` in a comprehension.
- Never name something after a built-in (`list`, `dict`, `str`, `id`, `max`, `sum`). It hides the built-in.
- Use `snake_case` even for LeetCode problems. Keep the original title in the heading, not in the code.

## Layout

- Indent with four spaces. Never use tabs.
- Keep lines to 100 characters. That is the limit set in `pyproject.toml`.
- Put two blank lines between top-level functions and classes, and one between methods.
- Put imports at the top, in three groups: standard library, third party, your own. `ruff` sorts them for you.
- Use one statement per line.

## Comparisons and conditions

- Compare to `None` with `is` and `is not`. Use `==` for values.
- Test truth directly: `if items:`, not `if len(items) > 0:`.
- Don't compare to `True` or `False`: write `if ready:`.
- Prefer `x in (1, 2, 3)` to a chain of `or` comparisons.

## Functions

- Give every function a one-line docstring that says what it returns.
- Add type hints to the signature once you have met them in [hints](../../course/05-functions/04-hints-lesson.ipynb).
- Return a value. Don't print inside a function you want to test.
- Keep a function to one job. If you need "and" to describe it, split it.

## Strings and formatting

- Use f-strings: `f"{name} has {count} items"`.
- Use double quotes for text, unless the text contains a double quote.
- Use `pathlib.Path`, not string joins, for file paths.

## Comments

- Explain why, not what. The code already says what.
- Keep a comment true. A stale comment is worse than none.
- Don't leave commented-out code. Git remembers it.

## This repo's own rules

- American spelling in all text.
- Short, plain, declarative sentences. Define a term the first time you use it.
- Standard library only in `course/` and `patterns/`.

**See also:** [Dos and don'ts](dos-and-donts.md) · [Resources](resources.md) · [Glossary](glossary.md)
