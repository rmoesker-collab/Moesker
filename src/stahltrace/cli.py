import anyio
import typer
from rich.console import Console

from . import __version__
from .agent import run_agent
from .db import record_run

app = typer.Typer(help="StahlTrace — agent-driven workflows over Postgres.")
console = Console()


@app.command()
def version() -> None:
    """Print the installed StahlTrace version."""
    console.print(f"stahltrace {__version__}")


@app.command()
def ask(
    prompt: str = typer.Argument(..., help="Prompt to send to the agent."),
    system: str | None = typer.Option(None, "--system", "-s", help="Optional system prompt."),
    persist: bool = typer.Option(True, "--persist/--no-persist", help="Record the run in Postgres."),
) -> None:
    """Run a one-shot agent query."""
    async def _go() -> object:
        return await run_agent(prompt, system=system)

    result = anyio.run(_go)
    console.print(result.text)
    if persist:
        run_id = record_run(result.model, result.prompt, result.text)
        console.print(f"[dim]recorded run #{run_id}[/dim]")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", help="Interface to bind."),
    port: int = typer.Option(8080, "--port", help="Port to listen on."),
) -> None:
    """Run the HTTP API (used by the Fly.io deployment)."""
    import uvicorn

    uvicorn.run("stahltrace.server:app", host=host, port=port)


@app.command(name="db-migrate")
def db_migrate() -> None:
    """Apply pending SQL migrations from the migrations/ directory."""
    from .db import apply_migrations

    applied = apply_migrations()
    if applied:
        for name in applied:
            console.print(f"applied {name}")
    else:
        console.print("no pending migrations")


@app.command()
def db_check() -> None:
    """Verify database connectivity and that pgvector is installed."""
    from .db import get_conn

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector'")
        has_vector = cur.fetchone() is not None
    console.print(f"connected: True  pgvector: {has_vector}")


if __name__ == "__main__":
    app()
