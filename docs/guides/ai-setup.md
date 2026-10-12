[Home](../../README.md) › [Docs](../README.md) › AI setup

# AI setup

This page is only setup: Learn mode and Build mode for each tool. For how to study with an AI, see [Learning with an AI tutor](learning-with-ai.md).

Turn off inline autocomplete (Cursor Tab, Copilot) while you practice. Instructions do not govern autocomplete.

## Learn mode

You are doing a practice notebook, an exercise folder, or a challenge problem. The tutor gives a hint, not the solution.

**Cursor.** Ask for help in the chat. The practice-tutor rule applies when you are working as a learner. You can also type `@practice-tutor`.

**Claude Code.** In a terminal, inside the `learn-python` folder:

```bash
claude --settings .claude/learner-settings.json
```

That turns on the Python tutor output style. It also blocks edits to practice files and reads of `solutions/`.

**Claude app** (web, desktop, or mobile). Follow [the Claude project instructions](ai-prompts/claude-project-instructions.md). In each chat, choose the **Learning** style from the style menu.

**Anything else.** Paste [the tutor prompt](ai-prompts/tutor-prompt.md) in as the instructions.

## Build mode

You are building a project under `use-cases/`. Drop the learner profile. In Claude Code, run `/output-style learning`. The assistant writes routine parts and leaves `TODO(human)` sections for you.

**Next:** [Learning with an AI tutor](learning-with-ai.md)
