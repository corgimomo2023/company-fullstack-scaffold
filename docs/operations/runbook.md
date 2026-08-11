# Operations runbook

## Health
- `/api/v1/health/live`: process liveness only.
- `/api/v1/health/ready`: verifies the database can execute a query.

## SQLite backup
Use the bundled SQLite online-backup operation from a trusted operator context; do not copy only `app.db` while WAL writes are active:

```bash
docker compose exec -T backend python -m app.ops.backup \
  --database /app/data/app.db \
  --output /app/data/backups/app-<UTC-timestamp>.db
container_id="$(docker compose ps -q backend)"
docker cp "$container_id:/app/data/backups/app-<UTC-timestamp>.db" ./backups/
docker cp "$container_id:/app/data/backups/app-<UTC-timestamp>.db.json" ./backups/
sha256sum -c <(jq -r '"\(.sha256)  app-<UTC-timestamp>.db"' ./backups/app-<UTC-timestamp>.db.json)
```

The operation uses SQLite's online backup API, runs `PRAGMA integrity_check`, refuses overwrite and emits a SHA-256 manifest. Copy the database and manifest to separate durable storage; a backup left only on the application volume is not a recovery copy. Test restoration on a disposable environment. For an incident restore, stop application writes, retain the damaged database, remove stale `-wal`/`-shm` sidecars only under the incident plan, place the verified backup, run migrations, then probe/read/write before reopening traffic.

## Deploy
1. Back up SQLite and verify free disk space.
2. Build immutable images and run CI.
3. Apply `alembic upgrade head` once before serving the new app (the included single-replica entrypoint does this).
4. Probe liveness/readiness, create/read/update a canary record, then remove it.
5. Watch 4xx/5xx rates, latency and SQLite busy/locked errors.

The first scaffold revision is tested by upgrading an empty database. Starting with the second revision, every migration change must add a fixture that upgrades from the previous real revision with representative data; document downgrade compatibility explicitly rather than assuming automatic rollback is safe.

## Rollback
Application rollback is only safe if the old code understands the upgraded schema. Prefer backward-compatible expand/contract migrations. Do not automatically downgrade a data migration. Restore the tested backup only under the incident plan.

## Scale trigger
Move to PostgreSQL before multiple backend replicas, sustained concurrent writers, online schema changes with tight availability, or database size/backup windows exceed the service objective.
