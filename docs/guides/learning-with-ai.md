[Home](../../README.md) › [Docs](../README.md) › Learning with an AI tutor

# Learning with an AI tutor

This page is for anyone taking the course with Cursor, Claude, or another AI coding tool. It shows how to get help that makes you better at Python, instead of help that does the course for you.

On this page: [the one rule](#the-one-rule) · [set up](#set-up-your-tool-once) · [study session](#a-study-session-with-an-ai) · [what to ask](#what-to-ask) · [red flags](#red-flags)

## The one rule

**The AI explains. You write the code.**

Ask it anything about how Python works, and expect a full answer. On exercises, it gives hints, reviews your code, and asks you questions, but it doesn't write the solution.

The reason is simple: you learn by doing the hard part yourself. In a study of about 1,000 students, those with unrestricted AI help did 48% better on practice problems. Once the AI was taken away, they did 17% *worse* on the exam than students who never had it. Students whose AI only gave hints did not lose out ([Bastani et al., PNAS 2025](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education)).

## Set up your tool once

The repo ships with tutor instructions for each tool. Follow [AI setup](ai-setup.md) once (Learn mode per tool, then Build mode when you hit a project).

**Turn off inline autocomplete** (Cursor Tab, GitHub Copilot) while you do practice and challenge problems. The tutor instructions can't control it, and it will happily type the answer for you.

## A study session with an AI

1. **Read why the topic matters, then the explanation and worked example.** Stay with **Why you'd use this**, **The idea**, and **See it work**. No AI yet.
2. **Answer Check yourself on your own.** Then run the cells. When something surprises you, ask why. Good questions start with "why" or "what happens if".
3. **Try the practice alone for 10–15 minutes.** Being stuck for a while is normal and useful.
4. **When you're stuck, ask for a hint, not an answer.** Each follow-up gets you one step closer.
5. **When your checks pass, ask for a review.** Have it ask you about cost and edge cases.
6. **Explain it back.** Tell the AI in your own words why your solution works, and let it point out gaps.
7. **Tomorrow, write it again from memory.** If you can't, you haven't learned it yet. That's fine: go back to step 4.

## What to ask

| You want to… | Try asking |
| --- | --- |
| Understand an idea | "Explain what a dict is like I've only used lists. Then ask me a question to check." |
| Go deeper, step by step | "Explain why `in` on a set is fast. Start with the intuition, and stop there until I ask for more." |
| See what's underneath | "Now the mechanism: what does Python actually do when I look up a key? Is there a [How Python works](../../internals/README.md) lesson on it?" |
| Read an error | "Here is my traceback. Help me read it. Don't fix my code." |
| Get unstuck | "I've tried X and Y. Give me the smallest hint that points me in the right direction." |
| Check your thinking | "I think this needs two pointers because… Am I on the right track? Don't tell me the answer." |
| Review working code | "My checks pass. Review this with questions, not rewrites. What edge case did I miss? What's the time cost?" |
| Test yourself | "Quiz me with 5 questions on today's lesson, one at a time." |
| Timed challenge practice | "Act as a timed-practice partner for this problem. Ask clarifying questions back, and push on my complexity analysis." |

## Going deeper, one level at a time

Every idea in this course has three levels. Ask for them in order, and only move on when the current one makes sense.

1. **Intuition:** what it does and when you'd use it.
2. **Mechanism:** how it works, and why it was designed that way.
3. **Under the hood:** memory, cost, and what CPython does. The [How Python works](../../internals/README.md) section covers this level with experiments you can run.

A good habit: after each level, ask the AI to give you one question that checks it, and answer it before going on.

## Red flags

- **You accepted code you couldn't explain line by line.** Delete it and write it yourself.
- **You asked the AI to "just fix it".** Ask what's wrong instead, and fix it yourself.
- **You opened `solutions/` before your checks passed.** Close it. Try again tomorrow from memory.
- **You're asking about every line.** Re-read the lesson's "Why it works this way" section first. The answer is often there.

If you really need to see an answer, write SHOW SOLUTION. The tutor will walk you through it. Then close it and re-write it from memory before you move on.

## When AI-written code is allowed

The **codebase rounds** in `challenges/` and the **projects** in `use-cases/` are different. Using an assistant well is part of the skill there, as it is at work. In Claude Code, switch to the built-in Learning style (`/output-style learning`). Claude writes the routine parts and leaves the important decisions for you to write. Still:

- run the tests after every change
- explain each change in one sentence before you accept it
- never commit code you couldn't rewrite yourself

**Next:** [Set up your tool](ai-setup.md), then [start the course](../../course/README.md).
