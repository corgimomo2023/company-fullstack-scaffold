from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine, inspect, text

from alembic import command


def test_alembic_upgrades_fresh_database_to_head(tmp_path: Path) -> None:
    database = tmp_path / "migration.db"
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database}")

    command.upgrade(config, "head")

    engine = create_engine(f"sqlite:///{database}")
    assert "projects" in inspect(engine).get_table_names()
    with engine.connect() as connection:
        revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
    assert revision == "20260810_0001"
