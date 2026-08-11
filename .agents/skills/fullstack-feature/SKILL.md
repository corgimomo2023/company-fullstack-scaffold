---
name: fullstack-feature
description: Use when adding a feature to this company scaffold.
version: 1.0.0
author: Platform Engineering
license: Internal
metadata:
  hermes:
    tags: [fullstack, fastapi, react, sqlalchemy, delivery]
    related_skills: []
---
# Full-Stack Feature Delivery

## Overview
Deliver the smallest complete vertical slice while preserving API, persistence, UI and operational contracts.

## When to use
Use for new or changed user-visible behavior spanning any scaffold module. Do not use for documentation-only edits.

## Procedure
1. Read root and nearest `AGENTS.md`; completion means constraints and commands are listed in working notes.
2. Define acceptance criteria including validation, not-found/conflict, loading/empty/error/success, authorization assumption and rollback; completion means each has an observable test target.
3. Add one failing backend or frontend test and run it; completion means failure is caused by missing behavior, not setup.
4. Implement a thin vertical slice: migration → model/schema → repository → service/UoW → route → typed client → query/form → UI. Completion means the narrow test is green and repositories do not commit/rollback.
5. Add edge-case tests and refactor duplication only while green.
6. Run `make check`; completion means every configured format, lint, type, test and build gate passes.
7. For deployable changes, run the production topology and probe liveness, readiness, API failure/success and SPA route. Completion means exact command output is recorded.

## Pitfalls
- Do not put SQL in FastAPI routes or `fetch` in React pages.
- Do not use frontend-only validation or silently swallow API request IDs.
- Do not edit an applied migration; add a new one.
- Do not imply async SQLite provides parallel writes.
- Do not add fake auth; integrate the approved identity boundary.

## Verification checklist
- [ ] Test failed first and now passes
- [ ] API contract and migration reviewed
- [ ] Loading, empty, error, success and pending states covered
- [ ] Keyboard/mobile behavior checked
- [ ] Logs avoid secrets/PII and include request ID
- [ ] `make check` passed
- [ ] Rollout and rollback documented
