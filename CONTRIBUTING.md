# Contributing

1. Create a short-lived branch from `main`.
2. Write an issue/acceptance statement before implementation.
3. Follow TDD for behavior changes and add an Alembic migration for schema changes.
4. Run `make check` and complete the PR template.
5. Require CODEOWNERS review for owned areas and one security reviewer for auth, permissions, secrets or data-export changes.

Use Conventional Commit types (`feat`, `fix`, `refactor`, `test`, `docs`, `build`, `ci`). Keep PRs vertically complete and reviewable.
