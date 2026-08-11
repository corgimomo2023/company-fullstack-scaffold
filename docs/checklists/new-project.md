# New project promotion checklist

## Ownership
- [ ] Product owner, technical owner and support channel named
- [ ] Placeholder CODEOWNERS replaced with real GitHub users/teams
- [ ] Branch protection requires CI and review

## Identity and data
- [ ] Approved SSO/session integration completed
- [ ] Server-side authorization tests cover every protected action
- [ ] Data classification, retention, export and deletion rules recorded
- [ ] Logs reviewed for secrets and PII

## Operations
- [ ] Environment secrets come from the approved secret manager
- [ ] TLS/ingress and trusted-host values configured
- [ ] SLOs, alerts and incident ownership defined
- [ ] SQLite volume is persistent; backup and restore exercised
- [ ] PostgreSQL migration trigger reviewed against expected workload

## Release
- [ ] `make check` passes from a clean clone
- [ ] `docker compose up --build` passes liveness/readiness and CRUD smoke tests
- [ ] Migration upgrade and application rollback compatibility reviewed
- [ ] Dependency locks and vulnerability scan reviewed
- [ ] Mobile, keyboard and error-state UI verified
