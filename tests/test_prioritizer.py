from engine.prioritizer import prioritize
from engine.classifier import ClassificationResult, Intent, Tone


def make_classification(intent, tone=Tone.NEUTRAL, confidence=0.8, flags=None):
    return ClassificationResult(
        intent=intent,
        tone=tone,
        confidence=confidence,
        requires_human=False,
        flags=flags or [],
    )


class TestPrioritizer:

    def test_fraud_report_is_critical(self):
        c = make_classification(Intent.FRAUD_REPORT)
        result = prioritize(c)
        assert result.score == 5
        assert result.sla_hours == 0.5

    def test_churn_risk_is_critical(self):
        c = make_classification(Intent.CHURN_RISK)
        result = prioritize(c)
        assert result.score == 5

    def test_threatening_tone_is_critical(self):
        c = make_classification(Intent.PAYMENT_ISSUE, tone=Tone.THREATENING)
        result = prioritize(c)
        assert result.score == 5

    def test_vip_player_is_urgent(self):
        c = make_classification(Intent.GAME_MECHANIC)
        result = prioritize(c, is_vip=True)
        assert result.score >= 4

    def test_standard_ticket_gets_default_priority(self):
        c = make_classification(Intent.GAME_MECHANIC)
        result = prioritize(c)
        assert result.score == 2
        assert result.sla_hours == 24.0

    def test_repeat_contact_escalates_priority(self):
        c = make_classification(Intent.TECHNICAL_ISSUE, flags=["repeat_contact"])
        result = prioritize(c)
        assert result.score >= 4
