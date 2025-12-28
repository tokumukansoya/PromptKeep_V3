# Git Workflow Guide

This document describes the recommended Git workflow for PromptKeep, including branch strategy, commit conventions, PR checklist, and how Document-Driven Development (DDD) integrates with CI.

---

## Branch strategy

- main: stable, always deployable
- phase-{n}-{short}: feature branches for each Phase (e.g. `phase-4-card-ui`)
- hotfix-{short}: urgent fixes

Naming: `phase-{number}-{short-description}`

---

## Commit conventions

Follow Conventional Commits:

- feat: new feature
- fix: bug fix
- docs: documentation change
- refactor: code refactor
- test: add/update tests
- chore: tooling/config

Examples:

```bash
git commit -m "docs: update Phase 5 spec"
git commit -m "feat: add CardBody component"
```

---

## Docs-first (Document-Driven Development)

1. Update affected documentation in `docs/` or `README.md` first.
2. Commit documentation with prefix `docs:`.
3. Create a phase branch and implement the code changes.
4. Include docs and tests in the same branch/PR.

Example:

```bash
# Update docs and commit
git add docs/requirements.md
git commit -m "docs: describe editor auto-save behavior"

# Start implementation branch
git checkout -b phase-5-editor
# implement code, add tests
git add .
git commit -m "feat: implement editor auto-save"
```

CI will run a lightweight docs-first check: if code under `PromptKeep_V3/` changes without related docs changes in `docs/` or `README.md`, the CI job is configured to fail (or warn). See [`docs/CI.md`](PromptKeep_V3/docs/CI.md:1).

---

## Development flow

1. Sync with main:

```bash
git checkout main
git pull origin main
```

2. Create phase branch:

```bash
git checkout -b phase-4-card-ui
```

3. Implement in small commits (one component/idea per commit).
4. Run linters and tests locally (`uv sync` / `uv run pytest`).
5. Push branch and open PR to `main`.

---

## Pull Request and merge

- Target branch: `main`.
- Provide clear PR description referencing the Phase and docs changes.
- Use `--no-ff` merge to preserve Phase history.

Merge example:

```bash
git checkout main
git merge phase-4-card-ui --no-ff -m "Merge phase-4-card-ui: card UI implemented"
git push origin main
git branch -d phase-4-card-ui
```

---

## PR checklist (recommended)

- [ ] Documentation updated in `docs/` or `README.md` (required)
- [ ] Tests added/updated under `PromptKeep_V3/tests/`
- [ ] Linters / pre-commit pass locally
- [ ] Commit messages use Conventional Commits
- [ ] CI checks pass (lint, tests, docs-first)
- [ ] PR description states which Phase this belongs to

Add this checklist to `.github/pull_request_template.md` to make it automatic.

---

## Troubleshooting

- If CI fails with a docs-first error: ensure docs changes are included in the same branch/PR.
- To amend a commit message:

```bash
git commit --amend -m "fix: corrected message"
```

- To undo last commit but keep changes:

```bash
git reset --soft HEAD~1
```

---

## Notes

- Keep PRs small and focused to make reviews and CI quicker.
- Tag Phase-complete points with `phase-{n}-complete` when a Phase is finished.

---

Last updated: 2025-12-28
