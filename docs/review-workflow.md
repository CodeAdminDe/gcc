# Review Workflow (gh-address-comments)

Use this flow when PR review comments arrive.

## Steps

1. Verify GitHub auth:
   - `gh auth status`
2. Open PR review threads and comments:
   - `gh pr view <number> --comments`
3. Address comments in small commits with explicit references to changed files/tests.
4. Push updates and post a concise resolution note per addressed thread.
5. Re-run quality gates before final reviewer ping:
   - `python3 -m ruff check src tests`
   - `python3 -m pytest -q`

## Skill usage

Use the `gh-address-comments` skill in this repository when handling active PR review feedback.
