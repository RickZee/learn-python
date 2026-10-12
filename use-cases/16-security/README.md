[Home](../../README.md) › [Projects](../README.md) › Security

# Security

Passwords, tokens, and checks that must not leak through a timing accident or a half-compared string.

## Tools

- hashlib for a digest
- secrets for tokens and for compare_digest
- The cryptography package when you need real encryption
- Never invent a password hash. Use a dedicated algorithm from a maintained library.

## Do this first

1. Open [01-lesson.ipynb](01-lesson.ipynb) and run it.
2. Compare a digest to the wrong value and print that they differ, without using `==`.
3. Keep the change small enough to finish in one sitting.

## Where it sits

Compare secrets with `compare_digest`. Cover the check with a [test](../../course/15-testing/01-unittest-lesson.ipynb).

**Next:** [Projects](../README.md)
