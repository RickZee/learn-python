[Home](../../README.md) › [Docs](../README.md) › AI setup

# AI setup

This page is only setup: Learn mode and Build mode for each tool. For how to study with an AI, see [Learning with an AI tutor](learning-with-ai.md).

Turn off inline autocomplete (Cursor Tab, Copilot) while you practice. Instructions do not govern autocomplete.

## Learn mode

You are doing a practice notebook, an exercise folder, or a challenge problem. The tutor gives a hint, not the solution.

**Cursor.** Run once from the repo root:

```bash
uv run python tools/learner_mode.py on
```

That writes a git-ignored `.cursorignore` (blocks `solutions/`) and an always-on learner rule. Undo with `uv run python tools/learner_mode.py off`. You can also type `@practice-tutor` in chat.

**Claude Code.** In a terminal, inside the `learn-python` folder:

```bash
claude --settings .claude/learner-settings.json
```

That turns on the Python tutor output style. It also blocks the Read tool on `solutions/` and edits to practice files. Shell commands are not blocked, so the tutor prompt is the second line of defense: do not ask the assistant to `cat` files under `solutions/`.

**Claude app** (web, desktop, or mobile). Follow [the Claude project instructions](ai-prompts/claude-project-instructions.md). In each chat, choose the **Learning** style from the style menu.

**Anything else.** Paste [the tutor prompt](ai-prompts/tutor-prompt.md) in as the instructions.

## Build mode

You are building a project under `use-cases/`. Drop the learner profile. In Claude Code, run `/output-style learning`. The assistant writes routine parts and leaves `TODO(human)` sections for you.

**Next:** [Learning with an AI tutor](learning-with-ai.md)
