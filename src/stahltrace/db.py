from collections.abc import Iterator
from contextlib import contextmanager
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
