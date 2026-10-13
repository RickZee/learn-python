@AGENTS.md

## Claude Code
- If the "Python tutor" output style is active, this is a learner session:
  follow the tutor instructions and don't edit exercise files. Otherwise
  `AGENTS.md` routing decides (tutor by default; authoring only when the user
  says so or points at docs/maintainers/, a RUNBOOK, or a PROGRESS file).
- Authoring sessions start with plain `claude`. Learner sessions start with
  `claude --settings .claude/learner-settings.json`.
- Edit notebooks with the notebook edit tool or an nbformat script, never by
  rewriting the JSON by hand.
