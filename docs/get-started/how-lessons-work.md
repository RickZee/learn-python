[Home](../../README.md) › [Docs](../README.md) › How lessons work

# How lessons work

Every course and internals lesson follows the same order so you always know what comes next.

## Inside a lesson

1. **Why you'd use this** — a real situation, so you know why the topic matters.
2. **After this lesson you can** — plain goals tied to that situation.
3. **Quick review** — a few questions from earlier lessons (skipped only in the very first lesson).
4. **The idea** — the explanation and analogy, with an optional "Explain more" layer.
5. **See it work** — a worked example that solves the situation from the top.
6. **Check yourself** — short questions *after* the teaching, so most learners should get most of them right.
7. **Why it works this way** / **When to use it** — mechanism, cost, and alternatives.
8. **Common mistake** — a bug people actually make here.
9. **Try it** — change the example to do something new.
10. **Recap** — then a link to the practice.

Questions come after the explanation on purpose: guessing before any teaching is a weak way to start, and retrieval works better once you have a model.

## Lesson → practice → exercise → project

| Step | What you open |
| --- | --- |
| Lesson | `NN-name-lesson.ipynb` |
| Practice | `NN-name-practice.ipynb` — warm-up, core, stretch, reflect |
| Part 2 exercise | an `exercise/` folder with `.py` stubs and `test_*.py` |
| Project | a page under `use-cases/` with a small app to build |

## What a check looks like

Practice cells use `check(...)`. A pass prints a ✓ line. A fail raises an error; read the last line first. Stubs ship as `raise NotImplementedError` until you replace them.

## Solutions

Reference answers live under `solutions/` at the mirrored path. Open one only after you have tried. Lesson notebooks never link there.

**Next:** [Troubleshooting](troubleshooting.md)
