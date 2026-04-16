from anthropic import Anthropic

client = Anthropic()

# Languages the assistant can detect and respond in.
# Claude handles these natively - no translation service required.
# Quality degrades for less common languages; this is documented in the README.
SUPPORTED_LANGUAGES = [
    "English", "Spanish", "French", "German", "Portuguese",
    "Italian", "Russian", "Turkish", "Arabic", "Polish",
    "Dutch", "Japanese", "Korean", "Chinese (Simplified)",
]


def detect_language(message: str) -> str:
    """
    Detect the language of a player message.

    Uses Claude for detection rather than a separate language detection library.
    This keeps dependencies minimal and handles mixed-language messages better
    than regex or statistical approaches.

    Returns the detected language name in English (e.g. "Spanish", "French").
    Returns "English" as default if detection is uncertain.
    """
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=20,
        system="Detect the language of the following text. Reply with only the language name in English (e.g. 'Spanish', 'French', 'English'). If uncertain, reply 'English'.",
        messages=[{"role": "user", "content": message}],
    )
    detected = response.content[0].text.strip()
    return detected if detected in SUPPORTED_LANGUAGES else "English"


def build_multilingual_system_prompt(detected_language: str, base_system_prompt: str) -> str:
    """
    Prepend a language instruction to the base system prompt.

    The language instruction is prepended rather than appended because
    Claude processes system prompts from top to bottom and language
    is the highest-priority formatting instruction.
    """
    if detected_language == "English":
        return base_system_prompt

    language_instruction = (
        f"LANGUAGE INSTRUCTION: The player has written in {detected_language}. "
        f"Respond in {detected_language} throughout this entire conversation. "
        f"Do not switch to English unless the player does so first. "
        f"All policies and procedures remain the same regardless of language.\n\n"
    )
    return language_instruction + base_system_prompt


def respond_multilingual(
    player_message: str,
    base_system_prompt: str,
    conversation_history: list[dict] = None,
) -> dict:
    """
    Respond to a player message in their detected language.

    Returns:
    - response: The assistant's response text
    - detected_language: What language was detected
    - used_base_prompt: Whether the base prompt was modified
    """
    detected_language = detect_language(player_message)
    system_prompt = build_multilingual_system_prompt(detected_language, base_system_prompt)

    messages = conversation_history or []
    messages = messages + [{"role": "user", "content": player_message}]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system_prompt,
        messages=messages,
    )

    return {
        "response": response.content[0].text,
        "detected_language": detected_language,
        "prompt_modified": detected_language != "English",
    }
