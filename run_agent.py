#!/usr/bin/env python3
"""
run_agent.py - End-to-end agent runner

Runs a single support message through the complete pipeline:
  1. Classify intent and tone
  2. Check immediate escalation conditions
  3. Assign priority and SLA
  4. Make escalation decision
  5. Generate response strategy
  6. Assemble prompt
  7. Call LLM (or mock)
  8. Print full execution trace

Usage:
  python run_agent.py
  python run_agent.py --message "I was charged but didn't receive my coins"
  python run_agent.py --contact-count 3 --vip

Run modes:
  Mock mode:  No ANTHROPIC_API_KEY set. Returns deterministic response. Free.
  LLM mode:   ANTHROPIC_API_KEY set. Calls Claude API. Costs credits.
"""
import argparse
import sys
from pathlib import Path

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).parent))

from engine.pipeline import run, TicketContext
from engine.logging_config import configure_logging
from llm_client import generate_response, get_mode_label, MOCK_MODE

configure_logging(level="WARNING")  # Suppress engine info logs during interactive run

SEPARATOR = "=" * 60
SECTION = "-" * 60


def load_system_prompt() -> str:
    """Load the system prompt from system-prompt.md."""
    prompt_path = Path(__file__).parent / "system-prompt.md"
    if prompt_path.exists():
        with open(prompt_path) as f:
            return f.read()
    return "You are a Tier 1 customer support assistant for a mobile strategy game."


def assemble_prompt(
    system_prompt: str,
    player_message: str,
    strategy,
    rag_context: str = "",
) -> str:
    """
    Assemble the full prompt sent to the LLM.

    Structure:
      1. System prompt (rules and behavior contract)
      2. RAG context (relevant KB sections, if available)
      3. Response strategy (from the triage engine)
      4. Player message

    This is what the LLM actually sees.
    """
    parts = []

    parts.append("=== SYSTEM PROMPT ===")
    # Truncate for display - full prompt goes to LLM
    parts.append(system_prompt[:500] + "... [truncated for display]")

    if rag_context:
        parts.append("\n=== KNOWLEDGE BASE CONTEXT ===")
        parts.append(rag_context[:400] + "... [truncated for display]" if len(rag_context) > 400 else rag_context)

    parts.append("\n=== RESPONSE STRATEGY ===")
    parts.append(f"Tone: {strategy.tone_instruction}")
    parts.append(f"Opening: {strategy.opening}")
    parts.append(f"Action: {strategy.action}")
    parts.append(f"Collect: {', '.join(strategy.collect)}")

    parts.append("\n=== PLAYER MESSAGE ===")
    parts.append(player_message)

    # The actual prompt sent to LLM uses the FULL system prompt, not truncated
    full_prompt = (
        system_prompt
        + "\n\n"
        + (f"KNOWLEDGE BASE CONTEXT:\n{rag_context}\n\n" if rag_context else "")
        + f"RESPONSE GUIDANCE:\nTone: {strategy.tone_instruction}\nAction: {strategy.action}\n\n"
        + f"PLAYER MESSAGE:\n{player_message}"
    )

    display_prompt = "\n".join(parts)
    return full_prompt, display_prompt


def try_rag_retrieval(message: str) -> str:
    """Attempt RAG retrieval. Returns empty string if KB not synced."""
    try:
        from rag.retriever import retrieve_and_format
        context, results = retrieve_and_format(message, top_k=2)
        return context
    except Exception:
        return ""  # KB not synced - proceed without context


def print_trace(message, contact_count, is_vip, result, display_prompt, response, is_mock, rag_available):
    """Print the full execution trace in a readable format."""

    c = result.classification
    p = result.priority
    e = result.escalation
    s = result.strategy

    print(f"\n{SEPARATOR}")
    print(" PLAYER CARE AI - EXECUTION TRACE")
    print(SEPARATOR)

    print(f"\n{'Run mode:':20} {get_mode_label()}")
    print(f"{'RAG context:':20} {'Available' if rag_available else 'Not available (run: python rag/kb_sync.py)'}")

    print(f"\n{SECTION}")
    print(" STEP 1: INPUT")
    print(SECTION)
    print(f"Message:       {message}")
    print(f"Contact count: {contact_count}")
    print(f"VIP player:    {is_vip}")

    print(f"\n{SECTION}")
    print(" STEP 2: CLASSIFICATION (rules-based, deterministic)")
    print(SECTION)
    print(f"Intent:        {c.intent.value}")
    print(f"Confidence:    {c.confidence}")
    print(f"Tone:          {c.tone.value}")
    print(f"Flags:         {c.flags if c.flags else 'none'}")
    print(f"Requires human:{c.requires_human}")
    if c.confidence < 0.65:
        print(f"NOTE: Confidence below threshold (0.65). Routing to human regardless of intent.")

    print(f"\n{SECTION}")
    print(" STEP 3: PRIORITY (rules-based, deterministic)")
    print(SECTION)
    print(f"Score:         P{p.score} - {p.label}")
    print(f"SLA:           {p.sla_hours} hours")
    print(f"Reason:        {p.reason}")

    print(f"\n{SECTION}")
    print(" STEP 4: ESCALATION DECISION (rules-based, deterministic)")
    print(SECTION)
    print(f"Escalate:      {e.should_escalate}")
    if e.should_escalate:
        print(f"Route to:      {e.team}")
        print(f"Reason:        {e.reason}")
        if e.notes:
            print(f"Notes:         {e.notes}")
    else:
        print(f"Action:        Handle at Tier 1")

    print(f"\n{SECTION}")
    print(" STEP 5: RESPONSE STRATEGY (rules-based, deterministic)")
    print(SECTION)
    print(f"Tone guidance: {s.tone_instruction}")
    print(f"Opening:       {s.opening}")
    print(f"Action:        {s.action}")
    print(f"Collect:       {', '.join(s.collect)}")

    print(f"\n{SECTION}")
    print(" STEP 6: PROMPT (assembled from system prompt + strategy + message)")
    print(SECTION)
    print(display_prompt)

    print(f"\n{SECTION}")
    print(f" STEP 7: LLM RESPONSE {'[MOCK]' if is_mock else '[REAL - Claude API]'}")
    print(SECTION)
    if is_mock:
        print("NOTE: Mock mode active. This is a deterministic pre-written response.")
        print("      Set ANTHROPIC_API_KEY in .env to get real Claude responses.\n")
    print(response)

    print(f"\n{SEPARATOR}")
    print(" TRACE COMPLETE")
    print(SEPARATOR)
    print(f"Processing time: {result.processing_time_ms}ms (triage engine only, excludes LLM)")
    print()


def run_agent(message: str, contact_count: int = 1, is_vip: bool = False):
    """Run a single message through the full agent pipeline."""

    # Step 1-5: Triage engine (all rules-based, no LLM)
    ctx = TicketContext(
        message=message,
        player_id="interactive_session",
        contact_count=contact_count,
        is_vip=is_vip,
    )
    result = run(ctx)

    # Step 6a: RAG retrieval (optional - works if KB is synced)
    rag_context = try_rag_retrieval(message)
    rag_available = bool(rag_context)

    # Step 6b: Load system prompt and assemble full prompt
    system_prompt = load_system_prompt()
    full_prompt, display_prompt = assemble_prompt(
        system_prompt=system_prompt,
        player_message=message,
        strategy=result.strategy,
        rag_context=rag_context,
    )

    # Step 7: Generate response (LLM or mock)
    response, is_mock = generate_response(
        prompt=full_prompt,
        intent=result.classification.intent.value,
    )

    # Print full trace
    print_trace(
        message=message,
        contact_count=contact_count,
        is_vip=is_vip,
        result=result,
        display_prompt=display_prompt,
        response=response,
        is_mock=is_mock,
        rag_available=rag_available,
    )


def get_input_interactive() -> tuple[str, int, bool]:
    """Get input interactively from the user."""
    print("\n" + SEPARATOR)
    print(" PLAYER CARE AI AGENT")
    print(SEPARATOR)
    print(f"Mode: {get_mode_label()}")
    print()
    message = input("Enter player message: ").strip()
    if not message:
        print("No message entered. Using example: 'I was charged but didn't receive my coins'")
        message = "I was charged but didn't receive my coins"

    try:
        contact_count = int(input("Contact count (how many times player has contacted us) [default: 1]: ").strip() or "1")
    except ValueError:
        contact_count = 1

    vip_input = input("Is VIP player? (y/n) [default: n]: ").strip().lower()
    is_vip = vip_input == "y"

    return message, contact_count, is_vip


def main():
    parser = argparse.ArgumentParser(
        description="Run a support message through the Player Care AI agent pipeline."
    )
    parser.add_argument(
        "--message", "-m",
        type=str,
        default=None,
        help="Player message to process. If not provided, prompts for input.",
    )
    parser.add_argument(
        "--contact-count", "-c",
        type=int,
        default=1,
        help="How many times this player has contacted support (default: 1)",
    )
    parser.add_argument(
        "--vip",
        action="store_true",
        default=False,
        help="Flag the player as VIP",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        default=False,
        help="Run with a preset demo message instead of prompting for input",
    )

    args = parser.parse_args()

    if args.demo:
        message = "I bought gems but they never showed up in my account. I've already tried restarting."
        contact_count = 1
        is_vip = False
    elif args.message:
        message = args.message
        contact_count = args.contact_count
        is_vip = args.vip
    else:
        message, contact_count, is_vip = get_input_interactive()

    run_agent(message, contact_count, is_vip)


if __name__ == "__main__":
    main()
