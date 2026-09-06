"""
AEGIS System State Manager
Maintains persistent system telemetry, treasury reserves, survival states, and active metrics.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from aegis.core.utils import utc_now_iso
from aegis.core.models import SystemState, Treasury, SurvivalStateEnum, Venture, Opportunity


class StateManager:
    """
    Coordinates persistent storage and state evaluation for AEGIS.
    """

    def __init__(self, state_file: Optional[str] = None, ventures_file: Optional[str] = None, opps_file: Optional[str] = None):
        data_dir = Path(os.getenv("AEGIS_DATA_DIR", Path(__file__).resolve().parents[1] / "data"))
        self.state_file = state_file or str(data_dir / "system_state.json")
        self.ventures_file = ventures_file or str(data_dir / "ventures.json")
        self.opps_file = opps_file or str(data_dir / "opportunities.json")
        
        self.state: SystemState = SystemState()
        self.ventures: Dict[str, Venture] = {}
        self.opportunities: Dict[str, Opportunity] = {}
        
        self._load()

    def _load(self):
        # 1. Load System State
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.state = SystemState(**data)
            except Exception:
                self.state = SystemState()
        else:
            self._save_state()

        # 2. Load Ventures
        if os.path.exists(self.ventures_file):
            try:
                with open(self.ventures_file, "r", encoding="utf-8") as f:
                    vdata = json.load(f)
                    self.ventures = {k: Venture(**v) for k, v in vdata.items()}
            except Exception:
                self.ventures = {}
        else:
            self._seed_default_ventures()

        # 3. Load Opportunities
        if os.path.exists(self.opps_file):
            try:
                with open(self.opps_file, "r", encoding="utf-8") as f:
                    odata = json.load(f)
                    self.opportunities = {k: Opportunity(**o) for k, o in odata.items()}
            except Exception:
                self.opportunities = {}
        else:
            self._seed_default_opportunities()

        self._recalculate_state()

    def _save_state(self):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state.model_dump(), f, indent=2)

    def _save_ventures(self):
        os.makedirs(os.path.dirname(self.ventures_file), exist_ok=True)
        with open(self.ventures_file, "w", encoding="utf-8") as f:
            json.dump({k: v.model_dump() for k, v in self.ventures.items()}, f, indent=2)

    def _save_opps(self):
        os.makedirs(os.path.dirname(self.opps_file), exist_ok=True)
        with open(self.opps_file, "w", encoding="utf-8") as f:
            json.dump({k: o.model_dump() for k, o in self.opportunities.items()}, f, indent=2)

    def _recalculate_state(self):
        # Dynamically evaluate survival state from treasury runway
        calculated = self.state.treasury.calculated_survival_state
        self.state.survival_state = calculated
        self.state.active_ventures_count = len([v for v in self.ventures.values() if v.status in ["ACTIVE", "SCALING"]])
        self.state.total_opportunities_evaluated = len(self.opportunities)
        self.state.updated_at = utc_now_iso()
        self._save_state()

    def update_treasury(self, cash_reserves: Optional[float] = None, monthly_burn: Optional[float] = None, monthly_revenue: Optional[float] = None) -> Treasury:
        if cash_reserves is not None:
            self.state.treasury.cash_reserves = max(0.0, cash_reserves)
        if monthly_burn is not None:
            self.state.treasury.monthly_burn = max(0.0, monthly_burn)
        if monthly_revenue is not None:
            self.state.treasury.monthly_revenue = max(0.0, monthly_revenue)
        self.state.treasury.updated_at = utc_now_iso()
        self._recalculate_state()
        return self.state.treasury

    def add_venture(self, venture: Venture) -> Venture:
        self.ventures[venture.id] = venture
        self._save_ventures()
        self._recalculate_state()
        return venture

    def add_opportunity(self, opportunity: Opportunity) -> Opportunity:
        self.opportunities[opportunity.id] = opportunity
        self._save_opps()
        self._recalculate_state()
        return opportunity

    def _seed_default_ventures(self):
        v1 = Venture(
            id="v-docuflow",
            name="DocuFlow AI",
            slug="docuflow",
            tagline="Autonomous Invoice & Contract Extraction API for ERP Networks",
            category="SaaS",  # type: ignore
            status="ACTIVE",
            target_mrr=18500.0,
            current_mrr=3200.0,
            initial_budget=1500.0,
            spent_to_date=420.0,
            key_metrics={
                "active_accounts": 28,
                "uptime_percentage": 99.98,
                "monthly_docs_processed": 142800,
                "gross_margin": 87.4
            }
        )
        self.ventures[v1.id] = v1
        self._save_ventures()

    def _seed_default_opportunities(self):
        from aegis.core.models import RevenuePriorityEnum
        from aegis.core.opportunity_scorer import OpportunityScorer

        opps = [
            Opportunity(
                id="opp-cloudsentinel",
                title="CloudCostSentinel",
                description="Zero-config read-only cloud auditor that reaps idle disks, orphan IPs, and unattached volumes.",
                category=RevenuePriorityEnum.SAAS,
                target_market="Series A-C Tech Startups & Dev Agencies",
                profit_potential_monthly=24000.0,
                scalability_score=10,
                sustainability_score=9,
                time_to_revenue_days=28,
                capital_required=1500.0,
                competitive_advantage_score=9,
                defensibility_score=8,
                risk_index=2,
                operational_complexity=2
            ),
            Opportunity(
                id="opp-datalease",
                title="DataLease GraphQL API",
                description="High-frequency verified executive contact and firmographic data stream for outbound CRMs.",
                category=RevenuePriorityEnum.LICENSING,
                target_market="Outbound Sales Tech Platforms & CRMs",
                profit_potential_monthly=32000.0,
                scalability_score=9,
                sustainability_score=8,
                time_to_revenue_days=35,
                capital_required=2500.0,
                competitive_advantage_score=8,
                defensibility_score=7,
                risk_index=3,
                operational_complexity=4
            ),
            Opportunity(
                id="opp-fastaudit",
                title="FastAudit B2B Compliance Guard",
                description="Automated weekly GDPR & Cookie consent verification and PDF compliance generator.",
                category=RevenuePriorityEnum.SUBSCRIPTION,
                target_market="E-Commerce Merchants & SaaS Operators",
                profit_potential_monthly=12000.0,
                scalability_score=9,
                sustainability_score=8,
                time_to_revenue_days=14,
                capital_required=800.0,
                competitive_advantage_score=7,
                defensibility_score=6,
                risk_index=2,
                operational_complexity=2
            )
        ]

        for op in opps:
            ev, raroe, notes = OpportunityScorer.calculate_ev(op, SurvivalStateEnum.STABLE)
            op.expected_value_score = ev
            op.raroe_score = raroe
            op.scoring_notes = notes
            self.opportunities[op.id] = op
            
        self._save_opps()
