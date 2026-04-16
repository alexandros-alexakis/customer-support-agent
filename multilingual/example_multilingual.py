"""
Example: multilingual support demonstration.

Shows how the assistant detects player language and responds accordingly.
All support policies remain identical regardless of language.

Requires: ANTHROPIC_API_KEY environment variable
Run: python multilingual/example_multilingual.py
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from multilingual.language_handler import respond_multilingual

# Load the base system prompt
SYSTEM_PROMPT_PATH = Path(__file__).parent.parent / "system-prompt.md"
try:
    with open(SYSTEM_PROMPT_PATH) as f:
        base_system_prompt = f.read()
except FileNotFoundError:
    base_system_prompt = "You are a Tier 1 customer support assistant for a mobile strategy game."

example_messages = [
    ("English", "I was charged for coins but they never appeared in my account."),
    ("Spanish", "Me cobraron por monedas pero nunca aparecieron en mi cuenta."),
    ("French", "J'ai été débité pour des pièces mais elles n'ont jamais été créditées sur mon compte."),
    ("Turkish", "Ödeme yapıldı fakat paralar hesabıma yüklenmedi."),
    ("Portuguese", "Fui cobrado por moedas mas elas nunca apareceram na minha conta."),
]

for expected_lang, message in example_messages:
    print(f"\n{'='*60}")
    print(f"Expected language: {expected_lang}")
    print(f"Message: {message}")
    print("-"*60)

    result = respond_multilingual(
        player_message=message,
        base_system_prompt=base_system_prompt,
    )

    print(f"Detected: {result['detected_language']}")
    print(f"Prompt modified: {result['prompt_modified']}")
    print(f"Response (first 200 chars):")
    print(result["response"][:200] + "..." if len(result["response"]) > 200 else result["response"])
