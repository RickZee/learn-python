[Home](../../../README.md) › [Projects](../../README.md) › tidy

# tidy

Sort a folder of files into directories named by suffix. `--dry-run` prints the plan and moves nothing. A real run writes `undo.json` so you can see what moved.

## Milestones

1. Plan the moves from suffix to folder.
2. Dry-run leaves the files where they are.
3. Apply moves the files and writes the undo log.

```bash
uv run pytest use-cases/01-automation/project
```

**Next:** [Field](../README.md)
