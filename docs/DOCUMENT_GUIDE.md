# PromptKeep Documentation Guide

This guide describes the role of each project document and the recommended reading order to enable Document-Driven Development (DDD) for PromptKeep.

---

## Principles of Document-Driven Development

- Document-first: update specifications and docs before implementing code.
- Each change should include documentation updates (docs/ or README.md) alongside code changes.

Typical workflow:

1. Update docs -> commit with `docs:`
2. Implement code -> commit with `feat:` / `fix:`

Refer to `.clinerules` and `docs/ai_execution_guide.md` for automation and AI-driven implementation rules.

---

## Primary documents and their purposes

1. README.md (root)
   - Project overview, quick setup, and high-level DDD explanation.
   - Primary entry point for new contributors.

2. docs/ai_execution_guide.md
   - Target: AI tools (Roo Code, Copilot) and human developers when using AI.
   - Contains phase-specific execution commands, success-checklists, and validation steps.
   - Use this first when delegating implementation to AI.

3. docs/coding_style.md
   - Language versions, type hinting and docstring style (Google), import ordering, naming rules, error handling.
   - Required for both humans and AI when producing code.

4. docs/requirements.md
   - Functional and non-functional requirements, data models (JSON schema), constraints, component behavior.
   - Use to confirm the expected behavior before implementation.

5. docs/architecture.md
   - Full project structure, responsibilities of each layer (models, services, ui, utils), data flow and key class diagrams.
   - Use when deciding where to add or change files.

6. docs/implementation_plan.md
   - Phase breakdown (Phase 0–12), dependencies, recommended implementation order, and success criteria.

7. docs/git_workflow.md
   - Branch strategy, commit conventions, merge process, and examples (phase branches, `--no-ff` usage).

8. docs/CI.md
   - CI configuration and how CI enforces DDD, linters, tests and the `docs-first` gate.

9. docs/archive/
   - Research notes and historical documents. Not required for day-to-day development.

---

## Recommended reading order for contributors

1. README.md — grasp the project and DDD approach.
2. docs/ai_execution_guide.md — if using AI to generate code.
3. docs/requirements.md and docs/architecture.md — confirm scope and structure.
4. docs/coding_style.md — implement with correct style.
5. docs/CI.md and docs/git_workflow.md — ensure PRs and CI follow project rules.

---

## Docs-first workflow (detailed)

When adding or changing features:

1. Edit the relevant document under `docs/` and the README if necessary. Commit with:

   docs: <short description>

2. Open a new branch (e.g. `phase-5-editor`):

   git checkout -b phase-5-editor

3. Implement the change. Run local checks (linters, tests). Commit code with conventional messages:

   feat: add editor component

4. Open a Pull Request targeting `main`. Use the PR template and confirm the checklist (see below).

5. CI runs. The `docs-first` check will fail the build if code changed without corresponding doc changes.

6. After review and CI pass, merge with `--no-ff` to retain phase history:

   git checkout main
   git merge phase-5-editor --no-ff -m "Merge phase-5-editor: editor feature complete"

---

## Pull Request checklist (template)

- [ ] Updated relevant docs in `docs/` or `README.md` (required)
- [ ] New or updated tests in `tests/`
- [ ] Local `uv sync` and `uv run pytest` pass
- [ ] Linters / pre-commit hooks pass
- [ ] Commit messages follow Conventional Commits
- [ ] PR description includes which Phase this change belongs to

Include this checklist in the repository `.github/pull_request_template.md` for automation.

---

## CI and docs-first enforcement

- CI should run on `push` and `pull_request` for `main` and `phase-*` branches.
- Add a lightweight check that signals failure when code changes appear without docs updates — the heuristic can be adjusted to be a warning.
- See `docs/CI.md` for a sample GitHub Actions workflow.

---

## Updating documentation: best practices

- Keep docs concise and verifiable: include exact commands, success criteria, and example outputs where possible.
- Link to code locations using relative paths (e.g. `PromptKeep_V3/README.md`) so both humans and tools can find targets.
- Use `docs:` commits for doc changes and keep the commit message short but clear.

---

## AI-assisted implementation

- Provide AI with `docs/ai_execution_guide.md` and `docs/implementation_plan.md` sections for the Phase to implement.
- Make success criteria unambiguous and include test cases where possible.
- Review AI-generated code and update docs if the implementation deviates.

---

## Versioning and release notes

- Tag Phase-complete commits (e.g. `phase-5-complete`) to mark milestones.
- Summarize Phase changes in `docs/CHANGELOG.md` or RELEASE notes when releasing to users.

---

## Contact and contributions

- For questions about documentation workflow, contact the repository maintainers via Issues.
- Encourage contributors to open small, well-documented PRs to make review and CI validation easier.

---

**Last updated**: 2025-12-28
