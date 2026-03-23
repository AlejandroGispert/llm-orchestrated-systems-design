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
import time
from pathlib import Path

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

REPO_ROOT = Path(__file__).resolve().parents[1]


def _get_llm(tools: list):
    """Return LLM with tools bound. Supports Anthropic, Gemini, or Ollama."""
    provider = (os.environ.get("LLM_PROVIDER") or "").strip().lower()
    if provider == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError:
            print("Error: LLM_PROVIDER=ollama requires langchain-ollama. Run: pip install langchain-ollama", file=sys.stderr)
            sys.exit(1)
        model_name = os.environ.get("OLLAMA_MODEL", "llama3.1")
        return ChatOllama(model=model_name).bind_tools(tools)

    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print(
                "Error: GEMINI_API_KEY required when LLM_PROVIDER=gemini",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError:
            print(
                "Error: LLM_PROVIDER=gemini requires langchain-google-genai and google-genai. "
                "Run: pip install langchain-google-genai google-genai",
                file=sys.stderr,
            )
            sys.exit(1)
        model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        return ChatGoogleGenerativeAI(
            model=model_name,
            api_key=api_key,
        ).bind_tools(tools)

    if provider == "anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print(
                "Error: ANTHROPIC_API_KEY required when LLM_PROVIDER=anthropic",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError:
            print(
                "Error: LLM_PROVIDER=anthropic requires langchain-anthropic. "
                "Run: pip install langchain-anthropic",
                file=sys.stderr,
            )
            sys.exit(1)
        model_name = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
        return ChatAnthropic(
            model=model_name,
            api_key=api_key,
        ).bind_tools(tools)

    # Default provider order when LLM_PROVIDER is unset:
    # 1) Anthropic (if ANTHROPIC_API_KEY exists), else 2) Gemini (if GEMINI_API_KEY exists).
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError:
            print(
                "Error: ANTHROPIC_API_KEY is set but langchain-anthropic is missing. "
                "Run: pip install langchain-anthropic",
                file=sys.stderr,
            )
            sys.exit(1)
        model_name = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
        return ChatAnthropic(
            model=model_name,
            api_key=os.environ["ANTHROPIC_API_KEY"],
        ).bind_tools(tools)

    if os.environ.get("GEMINI_API_KEY"):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError:
            print(
                "Error: GEMINI_API_KEY is set but Gemini deps are missing. "
                "Run: pip install langchain-google-genai google-genai",
                file=sys.stderr,
            )
            sys.exit(1)
        model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        return ChatGoogleGenerativeAI(
            model=model_name,
            api_key=os.environ["GEMINI_API_KEY"],
        ).bind_tools(tools)

    print(
        "Error: No provider credentials found. Set one of:\n"
        "- ANTHROPIC_API_KEY (for Claude)\n"
        "- GEMINI_API_KEY (for Gemini)\n"
        "- or LLM_PROVIDER=ollama for local runs.",
        file=sys.stderr,
    )
    sys.exit(1)


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
def create_graph(day: int, date: str, time: str, compact: bool = False) -> StateGraph:
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

        # Compact mode is used after API rate-limit responses to reduce prompt size.
        journal_chars = 1200 if compact else 3000
        learnings_chars = 800 if compact else 2000
        takeaways_chars = 1800 if compact else 4000

        journal_snippet = journal[-journal_chars:] if len(journal) > journal_chars else journal
        learnings_snippet = learnings[-learnings_chars:] if len(learnings) > learnings_chars else learnings
        takeaways_snippet = takeaways[:takeaways_chars]

        return f"""You are an aerospace conceptual design agent. Your goal is to evolve toward flight-ready conceptual designs for reusable orbital access.

Today is Day {day} ({date} {time}).

=== IDENTITY ===
{identity}

=== JOURNAL (last ~20 lines) ===
{journal_snippet}

=== LEARNINGS ===
{learnings_snippet}

=== DESIGN BLUEPRINT (TAKEAWAYS.md) ===
{takeaways_snippet}...

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
            # Anthropic requires at least one non-system message.
            # Put all run context/instructions in the initial user prompt.
            user_prompt = (
                build_system_prompt(state)
                + "\n\nPlan and implement ONE improvement. Use your tools, then commit."
            )
            messages = [HumanMessage(content=user_prompt)]
        response = model.invoke(messages)
        return {"messages": messages + [response]}

    tool_node = ToolNode(tools)

    def tools_node(state: dict):
        # ToolNode returns only the new tool messages.
        # Preserve full conversation history so Anthropic can validate
        # tool_result <-> tool_use pairing across turns.
        result = tool_node.invoke(state)
        tool_messages = result.get("messages", [])
        return {"messages": state["messages"] + tool_messages}

    def should_continue(state: dict):
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"
        return "__end__"

    graph = StateGraph(dict)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)

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

    provider = (os.environ.get("LLM_PROVIDER") or "").strip().lower()
    if provider == "ollama":
        pass
    elif provider == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY required for LLM_PROVIDER=anthropic.", file=sys.stderr)
        sys.exit(1)
    elif provider == "gemini" and not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY required for LLM_PROVIDER=gemini.", file=sys.stderr)
        sys.exit(1)
    elif not provider and not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("GEMINI_API_KEY")):
        print(
            "Error: Set ANTHROPIC_API_KEY or GEMINI_API_KEY "
            "(or set LLM_PROVIDER=ollama for local Ollama).",
            file=sys.stderr,
        )
        sys.exit(1)

    graph = create_graph(args.day, args.date, args.time)
    try:
        graph.invoke({"messages": []})
    except Exception as e:
        msg = str(e)

        # Anthropic-specific common failure modes: provide actionable guidance
        # without dumping a full traceback for expected operational errors.
        if "credit balance is too low" in msg.lower():
            print(
                "Anthropic API error: insufficient API credits for this key/workspace.\n"
                "Fix: add API credits in Anthropic Console (Plans & Billing) OR use a key from a funded workspace.\n"
                "Temporary workaround: run with LLM_PROVIDER=gemini (if GEMINI_API_KEY is set) or LLM_PROVIDER=ollama.",
                file=sys.stderr,
            )
            sys.exit(2)
        if "invalid x-api-key" in msg.lower() or "authentication" in msg.lower():
            print(
                "Anthropic API error: invalid/unauthorized API key.\n"
                "Fix: update ANTHROPIC_API_KEY in .env (or environment) and retry.",
                file=sys.stderr,
            )
            sys.exit(2)
        if "model" in msg.lower() and ("not found" in msg.lower() or "not available" in msg.lower()):
            print(
                "Anthropic API error: requested model is unavailable for this account.\n"
                "Fix: set ANTHROPIC_MODEL to an allowed model and retry.",
                file=sys.stderr,
            )
            sys.exit(2)
        if "unexpected `tool_use_id` found in `tool_result` blocks" in msg:
            print(
                "Anthropic tool protocol error: received a tool_result without a matching prior tool_use.\n"
                "This run has been stopped to keep state consistent. Please retry the session.",
                file=sys.stderr,
            )
            sys.exit(2)
        if "rate_limit_error" in msg.lower() or "429" in msg.lower():
            # Retry once with a shorter prompt after a short backoff.
            wait_s = int(os.environ.get("RATE_LIMIT_RETRY_SECONDS", "20"))
            print(
                "Anthropic API rate-limit hit (429). Retrying once with reduced context "
                f"after {wait_s}s backoff...",
                file=sys.stderr,
            )
            time.sleep(max(1, wait_s))
            try:
                compact_graph = create_graph(args.day, args.date, args.time, compact=True)
                compact_graph.invoke({"messages": []})
                print("Recovered after rate-limit retry with compact context.", file=sys.stderr)
                return
            except Exception as retry_error:
                retry_msg = str(retry_error)
                if "rate_limit_error" in retry_msg.lower() or "429" in retry_msg.lower():
                    print(
                        "Anthropic API error: still rate-limited after compact retry.\n"
                        "Fix options:\n"
                        "- Wait 30-90s and retry\n"
                        "- Set LLM_PROVIDER=gemini or LLM_PROVIDER=ollama to avoid Anthropic TPM caps\n"
                        "- Reduce prompt footprint in docs/TAKEAWAYS.md and docs/JOURNAL.md\n"
                        "- Request higher org limits from Anthropic",
                        file=sys.stderr,
                    )
                    sys.exit(2)
                print(f"Agent runtime error after rate-limit retry: {retry_msg}", file=sys.stderr)
                raise

        # Unknown runtime error: keep details for debugging.
        print(f"Agent runtime error: {msg}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
