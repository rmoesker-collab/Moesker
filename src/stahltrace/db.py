from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from psycopg import Connection, connect
from psycopg.rows import dict_row

from .config import settings


@contextmanager
def get_conn() -> Iterator[Connection]:
    conn = connect(settings.database_url, row_factory=dict_row, autocommit=False)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def record_run(model: str, prompt: str, response: str, metadata: dict[str, Any] | None = None) -> int:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO agent_runs (model, prompt, response, metadata, finished_at)
            VALUES (%s, %s, %s, %s::jsonb, now())
            RETURNING id
            """,
            (model, prompt, response, _json(metadata or {})),
        )
        row = cur.fetchone()
        assert row is not None
        return row["id"]


def _json(value: dict[str, Any]) -> str:
    import json

    return json.dumps(value)


def _migrations_dir() -> Path:
    candidates = [
        Path(__file__).resolve().parents[2] / "migrations",
        Path.cwd() / "migrations",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(f"migrations directory not found (looked in {candidates})")


def apply_migrations() -> list[str]:
    """Apply pending migrations/*.sql in order; track them in schema_migrations."""
    applied: list[str] = []
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                filename   TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )
        cur.execute("SELECT filename FROM schema_migrations")
        done = {row["filename"] for row in cur.fetchall()}
        for path in sorted(_migrations_dir().glob("*.sql")):
            if path.name in done:
                continue
            cur.execute(path.read_text(encoding="utf-8"))
            cur.execute(
                "INSERT INTO schema_migrations (filename) VALUES (%s)", (path.name,)
            )
            applied.append(path.name)
    return applied
