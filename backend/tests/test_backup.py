import hashlib
import json
import sqlite3
from pathlib import Path

from app.ops.backup import backup_database


def test_online_backup_is_readable_and_checksummed(tmp_path: Path) -> None:
    source = tmp_path / "source.db"
    output = tmp_path / "backup.db"
    with sqlite3.connect(source) as connection:
        connection.execute("CREATE TABLE records (value TEXT NOT NULL)")
        connection.execute("INSERT INTO records VALUES ('kept')")

    manifest_path = backup_database(source, output)

    with sqlite3.connect(output) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        assert connection.execute("SELECT value FROM records").fetchone() == ("kept",)
    manifest = json.loads(manifest_path.read_text())
    assert manifest["sha256"] == hashlib.sha256(output.read_bytes()).hexdigest()
    assert manifest["source"] == str(source.resolve())
