"""
AEGIS Opportunity Scoring Engine
Calculates Expected Value (EV), Risk-Adjusted Return on Effort (RAROE), and Survival Fit
"""

from typing import Dict, Any, Tuple
from aegis.core.models import Opportunity, RevenuePriorityEnum, SurvivalStateEnum


REVENUE_WEIGHTS: Dict[RevenuePriorityEnum, float] = {
    RevenuePriorityEnum.SAAS: 1.00,
    RevenuePriorityEnum.SUBSCRIPTION: 0.95,
    RevenuePriorityEnum.LICENSING: 0.90,
    RevenuePriorityEnum.B2B_SERVICES: 0.85,
    RevenuePriorityEnum.AUTOMATION_SERVICES: 0.80,
    RevenuePriorityEnum.DIGITAL_PRODUCTS: 0.70,
    RevenuePriorityEnum.EDUCATION: 0.65,
    RevenuePriorityEnum.MARKETPLACES: 0.60,
    RevenuePriorityEnum.MEDIA: 0.50,
    RevenuePriorityEnum.ADVERTISING: 0.40,
}


class OpportunityScorer:
    """
    Computes rigorous economic scoring for prospective ventures and initiatives.
    """

    @staticmethod
    def calculate_ev(opportunity: Opportunity, survival_state: SurvivalStateEnum = SurvivalStateEnum.STABLE) -> Tuple[float, float, str]:
        """
        Calculates:
        1. raw_ev: Pure expected value in dollar-equivalents/utility
        2. raroe: Risk-Adjusted Return on Effort (0-100 index)
        3. notes: Strategic justification tailored to survival state
        """
        rev_weight = REVENUE_WEIGHTS.get(opportunity.category, 0.75)

        # Scale Factors (1 to 10 normalized to 0.1 to 1.0)
        scale_factor = opportunity.scalability_score / 10.0
        sustain_factor = opportunity.sustainability_score / 10.0
        moat_factor = opportunity.competitive_advantage_score / 10.0
        defensibility_factor = opportunity.defensibility_score / 10.0

        # Risk & Friction Multipliers (1.0 to 3.0+)
        risk_multiplier = 1.0 + (opportunity.risk_index / 10.0)
        complexity_multiplier = 1.0 + (opportunity.operational_complexity / 10.0)
        
        # Capital Drag (every $1,000 adds friction, scaling logarithmically)
        capital_drag = 1.0 + (opportunity.capital_required / 5000.0)
        
        # Time-to-revenue penalty/urgency modifier based on survival state
        days = max(1, opportunity.time_to_revenue_days)
        time_drag = 1.0 + (days / 60.0)

        # State-specific survival adjustment
        state_urgency_bonus = 1.0
        if survival_state == SurvivalStateEnum.CRITICAL:
            if days <= 14:
                state_urgency_bonus = 2.5
            elif days > 45:
                state_urgency_bonus = 0.25  # Massive penalty in CRITICAL state for slow revenue
        elif survival_state == SurvivalStateEnum.WARNING:
            if days <= 30:
                state_urgency_bonus = 1.6
            elif days > 90:
                state_urgency_bonus = 0.5
        elif survival_state == SurvivalStateEnum.STRONG or survival_state == SurvivalStateEnum.FORTRESS:
            # Rewards defensibility and moat over quick hacks
            state_urgency_bonus = 1.0 + ((moat_factor + defensibility_factor) * 0.4)

        # Core Value numerator (Monthly profit * compounding quality factors * revenue priority weight)
        value_numerator = (
            opportunity.profit_potential_monthly
            * (0.35 * scale_factor + 0.35 * sustain_factor + 0.15 * moat_factor + 0.15 * defensibility_factor)
            * rev_weight
            * state_urgency_bonus
        )

        # Friction denominator
        friction_denominator = risk_multiplier * complexity_multiplier * capital_drag * time_drag

        # EV Score ($ expected utility)
        raw_ev = round(value_numerator / friction_denominator, 2)

        # RAROE (Risk-Adjusted Return on Effort) mapped onto a calibrated 0 - 100 benchmark
        # A project with $15k/mo profit, low capital, 14 days time-to-revenue, 9 scale -> ~90-95
        benchmark_base = (opportunity.profit_potential_monthly / 10000.0) * 20.0
        quality_score = (scale_factor * 20) + (sustain_factor * 20) + (moat_factor * 15) + (defensibility_factor * 15)
        risk_penalty = (opportunity.risk_index * 2.5) + (opportunity.operational_complexity * 2.5)
        
        raw_raroe = (benchmark_base + quality_score - risk_penalty) * rev_weight * (1.0 / (1.0 + (days / 180.0)))
        raroe = max(5.0, min(99.4, round(raw_raroe, 1)))

        # Strategic commentary
        notes = (
            f"Evaluated under {survival_state.value} posture. "
            f"Category weight: {rev_weight:.2f} ({opportunity.category.value}). "
            f"Time-to-revenue: {opportunity.time_to_revenue_days}d (urgency mod: {state_urgency_bonus:.2f}x). "
            f"Cap-efficiency: ${opportunity.profit_potential_monthly:,.0f}/mo on ${opportunity.capital_required:,.0f} capex."
        )

        return raw_ev, raroe, notes

    @classmethod
    def score_and_rank(cls, opportunities: list[Opportunity], survival_state: SurvivalStateEnum) -> list[Opportunity]:
        """
        Scores all opportunities and returns them sorted by RAROE descending.
        """
        scored = []
        for opp in opportunities:
            ev, raroe, notes = cls.calculate_ev(opp, survival_state)
            opp.expected_value_score = ev
            opp.raroe_score = raroe
            opp.scoring_notes = notes
            scored.append(opp)
        
        return sorted(scored, key=lambda x: x.raroe_score, reverse=True)
