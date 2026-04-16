import os
from dotenv import load_dotenv

load_dotenv()

# Detect run mode based on whether API key is set
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MOCK_MODE = not bool(ANTHROPIC_API_KEY)

# Mock responses keyed by intent - deterministic, no randomness
# These are realistic but clearly labelled as mock output
MOCK_RESPONSES = {
    "payment_issue": (
        "Thank you for reaching out. I'm sorry to hear your purchase didn't arrive. "
        "Could you please share your Player ID and the transaction ID from your receipt? "
        "Once I have those, I'll look into this right away."
    ),
    "refund_request": (
        "I understand you'd like a refund. I've noted your request and I'm escalating it "
        "to our billing team who handle refund reviews. Could you confirm your Player ID "
        "and the transaction ID for the purchase?"
    ),
    "account_access": (
        "I'm sorry you're having trouble accessing your account. "
        "Could you tell me which login method you use - Google, Facebook, Apple ID, email, or guest? "
        "That will help me point you in the right direction."
    ),
    "ban_appeal": (
        "I understand this is frustrating. Account restrictions are reviewed by our Trust and Safety team. "
        "I'm escalating your case now. Could you share your Player ID and the date you first noticed the restriction?"
    ),
    "bug_report": (
        "Thank you for reporting this. To help our technical team investigate, could you tell me "
        "your device model, OS version, and describe exactly what happens when the bug occurs?"
    ),
    "technical_issue": (
        "I'm sorry you're experiencing this. Let's start with a few basic steps: "
        "please close the app completely, wait 60 seconds, and reopen it. "
        "If the issue persists, could you share your device model and OS version?"
    ),
    "game_mechanic": (
        "Happy to help with that. Based on our documentation, the feature works as follows: "
        "please check the in-game help section for the most up-to-date guide, "
        "or let me know more specifically what you're trying to do and I'll explain further."
    ),
    "churn_risk": (
        "I'm really sorry to hear you're feeling this way - that's not the experience we want for you. "
        "I've flagged your case to our player relations team who will reach out to understand what happened "
        "and make sure it's addressed properly."
    ),
    "fraud_report": (
        "Thank you for reporting this. Our Trust and Safety team takes fair play seriously. "
        "Could you share the suspected player's username, the date of the incident, "
        "and any screenshots if you have them?"
    ),
    "unknown": (
        "Thank you for contacting us. I want to make sure I understand your issue correctly. "
        "Could you tell me a bit more about what's happening? For example, is this related to "
        "a purchase, your account, a technical problem, or something in the game?"
    ),
}


def generate_response(prompt: str, intent: str = "unknown") -> tuple[str, bool]:
    """
    Generate a response to a player support message.

    Parameters:
        prompt: The full assembled prompt (system prompt + context + player message)
        intent: The classified intent, used for mock mode fallback

    Returns:
        (response_text, is_mock) - the response and whether mock mode was used

    In MOCK MODE (no API key set):
        Returns a deterministic response based on intent.
        No API call is made. No cost incurred.
        Output is clearly labelled as mock.

    In LLM MODE (API key set):
        Calls the Anthropic Claude API with the full prompt.
        Returns the model's actual response.
    """
    if MOCK_MODE:
        response = MOCK_RESPONSES.get(intent, MOCK_RESPONSES["unknown"])
        return response, True

    # Real API call
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text, False
    except Exception as e:
        # Fall back to mock if API call fails
        fallback = MOCK_RESPONSES.get(intent, MOCK_RESPONSES["unknown"])
        return f"[API ERROR - FALLBACK MOCK] {str(e)}\n\n{fallback}", True


def get_mode_label() -> str:
    if MOCK_MODE:
        return "MOCK MODE (no API key - deterministic output, no cost)"
    return "LLM MODE (Anthropic Claude API)"
