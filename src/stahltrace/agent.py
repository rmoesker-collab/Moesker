from dataclasses import dataclass

from claude_agent_sdk import ClaudeAgentOptions, query

from .config import settings


@dataclass
class AgentResult:
    model: str
    prompt: str
    text: str


async def run_agent(prompt: str, *, system: str | None = None) -> AgentResult:
    """Run a one-shot Claude agent query and return the assembled text response."""
    options = ClaudeAgentOptions(
        model=settings.model,
        system_prompt=system,
    )

    chunks: list[str] = []
    async for message in query(prompt=prompt, options=options):
        for block in getattr(message, "content", []) or []:
            text = getattr(block, "text", None)
            if text:
                chunks.append(text)

    return AgentResult(model=settings.model, prompt=prompt, text="".join(chunks))
