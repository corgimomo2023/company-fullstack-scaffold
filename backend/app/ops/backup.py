import argparse
import hashlib
import json
import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path


def backup_database(source: Path, output: Path) -> Path:
    source = source.expanduser().resolve()
    output = output.expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"database does not exist: {source}")
    if source == output:
        raise ValueError("backup output must differ from source")
    if output.exists():
        raise FileExistsError(f"refusing to overwrite backup: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.tmp-{os.getpid()}")
    try:
        with (
            sqlite3.connect(source) as source_connection,
            sqlite3.connect(temporary) as backup_connection,
        ):
            source_connection.backup(backup_connection)
            result = backup_connection.execute("PRAGMA integrity_check").fetchone()
            if result != ("ok",):
                raise RuntimeError(f"backup integrity check failed: {result!r}")
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    manifest_path = output.with_suffix(output.suffix + ".json")
    manifest = {
        "source": str(source),
        "backup": str(output),
        "created_at": datetime.now(UTC).isoformat(),
        "bytes": output.stat().st_size,
        "sha256": digest,
        "integrity_check": "ok",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a verified online SQLite backup")
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = backup_database(args.database, args.output)
    print(manifest)


if __name__ == "__main__":
    main()
