"""
AEGIS Decision Filter & Absolute Rules Validator
Evaluates actions, plans, and initiatives through the 5 survival questions and absolute ethical rules.
"""

from typing import Dict, Any, List
from aegis.core.models import DecisionFilterResult, SurvivalStateEnum


class DecisionFilter:
    """
    AEGIS Absolute Ethics & Survival Evaluation Filter.
    Every proposal must pass this filter before execution.
    """

    FORBIDDEN_PATTERNS = [
        "hack", "crack", "scrape private", "bypass auth", "exploit", "steal",
        "fake review", "counterfeit", "deceive", "scam", "pyramid", "ponzi",
        "spam unauthorized", "manipulate market", "insider trading", "violate gdpr",
        "phishing", "malware", "ddos", "unlicensed", "tax evasion", "money laundering"
    ]

    @classmethod
    def evaluate(
        cls,
        action_title: str,
        action_description: str,
        current_state: SurvivalStateEnum = SurvivalStateEnum.STABLE,
        expected_cash_impact_monthly: float = 0.0,
        capex_required: float = 0.0,
        risk_level: str = "LOW"
    ) -> DecisionFilterResult:
        combined_text = f"{action_title} {action_description}".lower()

        # 1. Absolute Rules Check (Zero Tolerance)
        violates_absolute = False
        violation_reason = ""
        for pattern in cls.FORBIDDEN_PATTERNS:
            if pattern in combined_text:
                violates_absolute = True
                violation_reason = f"Action triggers absolute prohibition against '{pattern}'. Long-term survival requires absolute trust."
                break

        if violates_absolute:
            return DecisionFilterResult(
                approved=False,
                increase_survival=False,
                increase_durable_cashflow=False,
                reduce_risk=False,
                strengthen_competitive_advantage=False,
                improve_sustainability=False,
                violates_absolute_rules=True,
                ethical_compliance=False,
                score=0,
                rationale=f"REJECTED: {violation_reason}",
                action_item="Reject immediately and purge proposal."
            )

        # 2. Survival Questions
        # Q1: Will this increase survival?
        # In CRITICAL state, capex without immediate cash return threatens survival
        inc_survival = True
        if current_state == SurvivalStateEnum.CRITICAL and capex_required > 1000 and expected_cash_impact_monthly == 0:
            inc_survival = False
        elif expected_cash_impact_monthly < 0 and capex_required > 5000:
            inc_survival = False

        # Q2: Will this increase durable cash flow?
        inc_cashflow = expected_cash_impact_monthly > 0 or ("recurring" in combined_text or "saas" in combined_text or "subscription" in combined_text or "retainer" in combined_text or "license" in combined_text or "automation" in combined_text)

        # Q3: Will this reduce risk?
        red_risk = risk_level.upper() in ["LOW", "NEGLIGIBLE"] or ("redundancy" in combined_text or "backup" in combined_text or "diversif" in combined_text or "security" in combined_text or "audit" in combined_text)

        # Q4: Will this strengthen competitive advantage?
        str_moat = ("proprietary" in combined_text or "ip" in combined_text or "patent" in combined_text or "brand" in combined_text or "moat" in combined_text or "efficiency" in combined_text or "automation" in combined_text or "software" in combined_text or "unique" in combined_text)

        # Q5: Will this improve long-term sustainability?
        imp_sustain = not ("short term hack" in combined_text or "churn and burn" in combined_text or "one-off gig" in combined_text)

        positive_count = sum([inc_survival, inc_cashflow, red_risk, str_moat, imp_sustain])
        score = int((positive_count / 5.0) * 100)

        approved = (positive_count >= 3) and inc_survival

        rationale_items = []
        if inc_survival: rationale_items.append("Supports system survival.")
        else: rationale_items.append("Does not provide sufficient survival buffer.")
        if inc_cashflow: rationale_items.append("Expected to enhance durable cashflow.")
        if str_moat: rationale_items.append("Strengthens competitive positioning or operational leverage.")
        if red_risk: rationale_items.append("Maintains risk within acceptable bounds.")

        rationale = " ".join(rationale_items)
        if approved:
            action_item = f"PROCEED: Proposal meets {positive_count}/5 survival criteria (Score: {score}%)."
        else:
            action_item = f"HOLD / REVISE: Proposal only meets {positive_count}/5 criteria. Optimize for durability and cash generation before re-submitting."

        return DecisionFilterResult(
            approved=approved,
            increase_survival=inc_survival,
            increase_durable_cashflow=inc_cashflow,
            reduce_risk=red_risk,
            strengthen_competitive_advantage=str_moat,
            improve_sustainability=imp_sustain,
            violates_absolute_rules=False,
            ethical_compliance=True,
            score=score,
            rationale=rationale,
            action_item=action_item
        )
