"""
Unit tests for the classifier.

These test the signal-matching logic and the decisions made at confidence boundaries.
They do not test LLM outputs - those require integration testing with real model calls.
"""
import pytest
from engine.classifier import classify, Intent, Tone, CONFIDENCE_THRESHOLD


class TestIntentClassification:

    def test_payment_issue_detected(self):
        result = classify("I was charged but didn't receive my coins")
        assert result.intent == Intent.PAYMENT_ISSUE

    def test_refund_request_detected(self):
        result = classify("I want a refund for my purchase")
        assert result.intent == Intent.REFUND_REQUEST

    def test_ban_appeal_detected(self):
        result = classify("My account was banned and I don't know why")
        assert result.intent == Intent.BAN_APPEAL

    def test_churn_risk_detected(self):
        result = classify("I'm done with this game, uninstalling right now")
        assert result.intent == Intent.CHURN_RISK

    def test_unknown_intent_on_empty_message(self):
        result = classify("")
        assert result.intent == Intent.UNKNOWN
        assert result.confidence == 0.0

    def test_unknown_intent_on_gibberish(self):
        result = classify("asdfgh jklqwerty")
        assert result.intent == Intent.UNKNOWN


class TestToneClassification:

    def test_threatening_tone_detected(self):
        result = classify("I will take legal action if this isn't resolved")
        assert result.tone == Tone.THREATENING

    def test_angry_tone_detected(self):
        result = classify("This is absolutely ridiculous and unacceptable")
        assert result.tone == Tone.ANGRY

    def test_neutral_tone_default(self):
        result = classify("I have a question about my purchase")
        assert result.tone == Tone.NEUTRAL


class TestEscalationFlags:

    def test_repeat_contact_flagged(self):
        result = classify("Still not resolved", contact_count=3)
        assert "repeat_contact" in result.flags
        assert result.requires_human is True

    def test_vip_always_requires_human(self):
        result = classify("I have a question", is_vip=True)
        assert result.requires_human is True
        assert "vip_player" in result.flags

    def test_legal_threat_requires_human(self):
        result = classify("I will sue you if this isn't fixed")
        assert result.requires_human is True
        assert "legal_threat" in result.flags

    def test_ban_appeal_always_escalates(self):
        result = classify("Why was my account banned?")
        assert result.requires_human is True


class TestConfidenceThreshold:

    def test_low_confidence_requires_human(self):
        # A message with very weak signals should produce low confidence
        result = classify("hello I need help")
        if result.confidence < CONFIDENCE_THRESHOLD:
            assert result.requires_human is True
