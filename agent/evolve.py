"""
Design agent — one evolution cycle.
LangGraph-based: plan → implement → journal → commit.

LLM: set LLM_PROVIDER=ollama to use local Ollama (free); otherwise uses Anthropic.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

REPO_ROOT = Path(__file__).resolve().parents[1]


def _get_llm(tools: list):
    """Return LLM with tools bound. Uses Ollama if LLM_PROVIDER=ollama else Anthropic."""
    provider = (os.environ.get("LLM_PROVIDER") or "").strip().lower()
    if provider == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError:
            print("Error: LLM_PROVIDER=ollama requires langchain-ollama. Run: pip install langchain-ollama", file=sys.stderr)
            sys.exit(1)
        model_name = os.environ.get("OLLAMA_MODEL", "llama3.1")
        return ChatOllama(model=model_name).bind_tools(tools)
    # Default: Anthropic
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY required (or set LLM_PROVIDER=ollama for local Ollama)", file=sys.stderr)
        sys.exit(1)
    from langchain_anthropic import ChatAnthropic
    return ChatAnthropic(
        model="claude-sonnet-4-20250514",
        api_key=api_key,
    ).bind_tools(tools)


# ── Tools the agent can use ──
@tool
def read_file(path: str) -> str:
    """Read a file. Path is relative to repo root."""
    full = REPO_ROOT / path.lstrip("/")
    if not full.is_file():
        return f"File not found: {path}"
    return full.read_text(encoding="utf-8", errors="replace")


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file. Path is relative to repo root. Creates dirs if needed."""
    full = REPO_ROOT / path.lstrip("/")
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")
    return f"Wrote {path}"


@tool
def run_bash(command: str) -> str:
    """Run a shell command in the repo root. Use for git, ls, etc."""
    result = subprocess.run(
        command,
        shell=True,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    out = result.stdout or ""
    err = result.stderr or ""
    if result.returncode != 0:
        return f"Exit {result.returncode}\nstdout: {out}\nstderr: {err}"
    return out


# ── Graph state ──
def create_graph(day: int, date: str, time: str) -> StateGraph:
    tools = [read_file, write_file, run_bash]
    model = _get_llm(tools)

    def build_system_prompt(state: dict) -> str:
        docs = REPO_ROOT / "docs"
        identity = (docs / "IDENTITY.md").read_text(encoding="utf-8", errors="replace")
        journal = (docs / "JOURNAL.md").read_text(encoding="utf-8", errors="replace")
        lf = docs / "LEARNINGS.md"
        learnings = lf.read_text(encoding="utf-8", errors="replace") if lf.exists() else "(empty)"
        takeaways = (docs / "TAKEAWAYS.md").read_text(encoding="utf-8", errors="replace")
        designs_dir = REPO_ROOT / "designs"
        designs = "\n".join(
            f"- {f.name}" for f in designs_dir.iterdir() if f.is_file()
        ) if designs_dir.exists() else "(empty)"

        return f"""You are an aerospace conceptual design agent. Your goal is to evolve toward flight-ready conceptual designs for reusable orbital access.

Today is Day {day} ({date} {time}).

=== IDENTITY ===
{identity}

=== JOURNAL (last ~20 lines) ===
{journal[-3000:] if len(journal) > 3000 else journal}

=== LEARNINGS ===
{learnings[-2000:] if len(learnings) > 2000 else learnings}

=== DESIGN BLUEPRINT (TAKEAWAYS.md) ===
{takeaways[:4000]}...

=== FILES IN designs/ ===
{designs}

Your task: Make ONE focused improvement. Options:
- Add or refine a design document in designs/
- Create a first conceptual design (designs/concept-v1.md) if empty
- Update docs/JOURNAL.md (append at top)
- Update docs/LEARNINGS.md if you learned something
- Document a trade study or requirement in specs/

Rules:
- One focused change per session
- Only modify: designs/, simulations/, specs/, docs/JOURNAL.md, docs/LEARNINGS.md
- Never modify: docs/IDENTITY.md, .github/, scripts/, agent/
- End by committing: run_bash("git add -A && git commit -m 'Day {day} ({time}): <brief description>'")
"""

    def agent_node(state: dict):
        messages = state.get("messages", [])
        if not messages:
            sys_prompt = build_system_prompt(state)
            messages = [
                SystemMessage(content=sys_prompt),
                HumanMessage(content="Plan and implement ONE improvement. Use your tools, then commit."),
            ]
        response = model.invoke(messages)
        return {"messages": messages + [response]}

    tool_node = ToolNode(tools)

    def should_continue(state: dict):
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"
        return "__end__"

    graph = StateGraph({"messages": []})

    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", "__end__": END})
    graph.add_edge("tools", "agent")

    return graph.compile()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--time", required=True)
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY") and (os.environ.get("LLM_PROVIDER") or "").strip().lower() != "ollama":
        print("Error: ANTHROPIC_API_KEY required (or set LLM_PROVIDER=ollama for local Ollama)", file=sys.stderr)
        sys.exit(1)

    graph = create_graph(args.day, args.date, args.time)
    graph.invoke({"messages": []})


if __name__ == "__main__":
    main()
