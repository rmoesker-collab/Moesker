import anyio.to_thread
from fastapi import FastAPI
from pydantic import BaseModel

from . import __version__
from .agent import run_agent
from .config import settings
from .db import record_run

app = FastAPI(title="StahlTrace", version=__version__)


class AskRequest(BaseModel):
    prompt: str
    system: str | None = None
    persist: bool = True


class AskResponse(BaseModel):
    model: str
    text: str
    run_id: int | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__, "model": settings.model}


@app.get("/health/db")
async def health_db() -> dict[str, bool]:
    def _check() -> bool:
        from .db import get_conn

        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector'")
            return cur.fetchone() is not None

    has_vector = await anyio.to_thread.run_sync(_check)
    return {"connected": True, "pgvector": has_vector}


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    result = await run_agent(req.prompt, system=req.system)
    run_id: int | None = None
    if req.persist:
        run_id = await anyio.to_thread.run_sync(
            record_run, result.model, result.prompt, result.text
        )
    return AskResponse(model=result.model, text=result.text, run_id=run_id)
