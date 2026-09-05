"""
AEGIS Orchestrator & Autonomous Value Creation Loop Engine
Implements:
Observe -> Analyze -> Discover -> Prioritize -> Plan -> Build -> Deploy -> Measure -> Improve -> Repeat
"""

import os
import time
from typing import Dict, Any, List, Optional

from aegis.core.utils import utc_now_iso
from aegis.core.models import (
    SystemState, SurvivalStateEnum, Opportunity, Venture,
    KnowledgeCategoryEnum, GovernanceTypeEnum, RevenuePriorityEnum
)
from aegis.core.state import StateManager
from aegis.core.opportunity_scorer import OpportunityScorer
from aegis.core.decision_filter import DecisionFilter
from aegis.core.doc_generator import DocumentGenerator
from aegis.core.knowledge_base import KnowledgeBase
from aegis.governance import GovernanceManager

from aegis.divisions.research import ResearchDivision
from aegis.divisions.product import ProductDivision
from aegis.divisions.engineering import EngineeringDivision
from aegis.divisions.marketing import MarketingDivision
from aegis.divisions.operations import OperationsDivision
from aegis.divisions.finance import FinanceDivision


class AegisOrchestrator:
    """
    The central operational brain of AEGIS.
    Coordinates all autonomous divisions, evaluates opportunities,
    enforces survival constraints, and executes the Value Creation Loop.
    """

    def __init__(self, workspace_root: str = "/home/user/aegis"):
        self.workspace_root = workspace_root
        self.state_mgr = StateManager()
        self.knowledge_base = KnowledgeBase()
        self.governance = GovernanceManager()

        # Instantiate the 6 autonomous divisions
        self.research_div = ResearchDivision()
        self.product_div = ProductDivision()
        self.engineering_div = EngineeringDivision()
        self.marketing_div = MarketingDivision()
        self.operations_div = OperationsDivision()
        self.finance_div = FinanceDivision()

        self.execution_logs: List[Dict[str, Any]] = []
        self._log("INIT", "AEGIS Autonomous Intelligence initialized. Identity: Self-Directed Economic Organism.")

    def _log(self, stage: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        entry = {
            "timestamp": utc_now_iso(),
            "stage": stage,
            "message": message,
            "metadata": metadata or {}
        }
        self.execution_logs.insert(0, entry)
        if len(self.execution_logs) > 500:
            self.execution_logs.pop()

    @property
    def current_state(self) -> SurvivalStateEnum:
        return self.state_mgr.state.survival_state

    def execute_single_loop_cycle(self) -> Dict[str, Any]:
        """
        Executes one full cycle of the Value Creation Loop:
        1. OBSERVE (Telemetry, Burn, Runway, Survival State)
        2. ANALYZE (Runway Stress Tests, Operational Bottlenecks)
        3. DISCOVER (Research scan for asymmetric revenue opportunities)
        4. PRIORITIZE (Score opportunities by EV & Survival Fit)
        5. PLAN (Generate specifications & 16-Doc Suite for top candidate)
        6. BUILD & DEPLOY (Engineering & Marketing automated scaffolding)
        7. MEASURE & IMPROVE (Record Knowledge, log metrics, compound learnings)
        """
        cycle_start = time.time()
        self.state_mgr.state.loop_iteration += 1
        it_num = self.state_mgr.state.loop_iteration
        self.state_mgr.state.last_loop_timestamp = utc_now_iso()

        # Step 1: OBSERVE
        survival_state = self.state_mgr.state.survival_state
        runway_days = self.state_mgr.state.treasury.runway_days
        reserves = self.state_mgr.state.treasury.cash_reserves
        self._log("OBSERVE", f"Cycle #{it_num}: Treasury reserves ${reserves:,.2f} | Net Runway: {runway_days:.1f} days | Posture: {survival_state.value}")

        # Step 2: ANALYZE
        stress_results = self.finance_div.execute_directive("run_treasury_stress_test", {"treasury": self.state_mgr.state.treasury}, survival_state)
        self._log("ANALYZE", f"Cycle #{it_num}: Treasury stress analysis complete. Buffer requirement: {stress_results.get('recommended_capital_buffer')}")

        # Step 3: DISCOVER
        discovery = self.research_div.execute_directive("discover_niche_opportunities", {}, survival_state)
        new_opps_raw = discovery.get("opportunities", [])
        discovered_candidates = []

        for opp_dict in new_opps_raw:
            opp = Opportunity(
                title=opp_dict["title"],
                category=RevenuePriorityEnum(opp_dict["category"]),
                target_market=opp_dict["target_market"],
                profit_potential_monthly=opp_dict["profit_potential_monthly"],
                scalability_score=opp_dict["scalability_score"],
                sustainability_score=opp_dict["sustainability_score"],
                time_to_revenue_days=opp_dict["time_to_revenue_days"],
                capital_required=opp_dict["capital_required"],
                competitive_advantage_score=opp_dict["competitive_advantage_score"],
                defensibility_score=opp_dict["defensibility_score"],
                risk_index=opp_dict["risk_index"],
                operational_complexity=opp_dict["operational_complexity"],
                description=opp_dict["description"]
            )
            discovered_candidates.append(opp)
            self.state_mgr.add_opportunity(opp)

        self._log("DISCOVER", f"Cycle #{it_num}: Discovered {len(discovered_candidates)} high-potential automated opportunities.")

        # Step 4: PRIORITIZE
        all_opps = list(self.state_mgr.opportunities.values())
        ranked_opps = OpportunityScorer.score_and_rank(all_opps, survival_state)
        top_opportunity = ranked_opps[0] if ranked_opps else None
        
        self._log("PRIORITIZE", f"Cycle #{it_num}: Scored and ranked {len(ranked_opps)} opportunities. Top priority: '{top_opportunity.title if top_opportunity else 'None'}' (RAROE: {top_opportunity.raroe_score if top_opportunity else 0})")

        # Step 5: PLAN (Run Decision Filter & Generate 16-Doc Suite)
        action_plan_summary = "Idle cycle"
        new_venture_created = None

        if top_opportunity:
            # Filter check
            filter_res = DecisionFilter.evaluate(
                action_title=top_opportunity.title,
                action_description=top_opportunity.description,
                current_state=survival_state,
                expected_cash_impact_monthly=top_opportunity.profit_potential_monthly,
                capex_required=top_opportunity.capital_required
            )

            if filter_res.approved:
                # Provision Venture & 16-doc artifacts
                slug = top_opportunity.title.lower().split("(")[0].strip().replace(" ", "-").replace("_", "")
                existing_v = next((v for v in self.state_mgr.ventures.values() if v.slug == slug), None)
                
                if not existing_v:
                    new_venture = Venture(
                        name=top_opportunity.title.split("(")[0].strip(),
                        slug=slug,
                        tagline=top_opportunity.description,
                        category=top_opportunity.category,
                        status="ACTIVE",
                        target_mrr=top_opportunity.profit_potential_monthly,
                        initial_budget=top_opportunity.capital_required
                    )

                    # Generate 16 Docs
                    docs = DocumentGenerator.generate_full_suite(new_venture, top_opportunity)
                    new_venture.documents = docs
                    
                    # Write to workspace disk
                    v_dir = os.path.join(self.workspace_root, "ventures", slug)
                    DocumentGenerator.write_to_disk(v_dir, docs)

                    self.state_mgr.add_venture(new_venture)
                    new_venture_created = new_venture
                    action_plan_summary = f"Provisioned autonomous venture '{new_venture.name}' with complete 16-artifact documentation."
                    
                    self._log("PLAN", f"Cycle #{it_num}: Approved by Decision Filter. Created venture '{new_venture.name}' with 16 core documents in {v_dir}.")
                    
                    # Log Knowledge Entry
                    self.knowledge_base.add_entry(
                        category=KnowledgeCategoryEnum.DECISION,
                        title=f"Greenlit Venture {new_venture.name}",
                        content=f"Evaluated opportunity with EV score ${top_opportunity.expected_value_score} and RAROE {top_opportunity.raroe_score}. Generated 16-doc architectural and financial suite.",
                        venture_id=new_venture.id,
                        tags=["venture_launch", new_venture.slug, "ev_prioritization"]
                    )
            else:
                self._log("PLAN", f"Cycle #{it_num}: Top opportunity rejected by Decision Filter: {filter_res.rationale}")

        # Step 6: BUILD & DEPLOY (Execute Divisional Workflows)
        eng_res = self.engineering_div.execute_directive("audit_system_resilience_and_security", {}, survival_state)
        mkt_res = self.marketing_div.execute_directive("compile_programmatic_seo_matrix", {"venture_name": top_opportunity.title if top_opportunity else "Core Platform"}, survival_state)
        ops_res = self.operations_div.execute_directive("audit_operational_efficiency", {}, survival_state)
        
        self._log("BUILD_DEPLOY", f"Cycle #{it_num}: Engineering security score {eng_res.get('security_audit_score')} | Ops efficiency: {ops_res.get('efficiency_score')}")

        # Step 7: MEASURE & IMPROVE
        cycle_duration = round(time.time() - cycle_start, 3)
        self._log("MEASURE", f"Cycle #{it_num} completed in {cycle_duration}s. System state: {survival_state.value}. All systems optimized.")

        return {
            "cycle_number": it_num,
            "timestamp": utc_now_iso(),
            "duration_seconds": cycle_duration,
            "survival_state": survival_state.value,
            "runway_days": round(runway_days, 1),
            "top_opportunity": top_opportunity.title if top_opportunity else None,
            "action_taken": action_plan_summary,
            "new_venture": new_venture_created.name if new_venture_created else None,
            "knowledge_entries_total": len(self.knowledge_base.entries),
            "status": "HEALTHY"
        }

    def evaluate_custom_opportunity(self, opp_data: Dict[str, Any]) -> Opportunity:
        """
        Takes raw user input, creates an Opportunity object, calculates EV & RAROE, and stores it.
        """
        cat_val = opp_data.get("category", "SaaS")
        cat_enum = RevenuePriorityEnum(cat_val) if cat_val in [c.value for c in RevenuePriorityEnum] else RevenuePriorityEnum.SAAS

        opp = Opportunity(
            title=opp_data.get("title", "Custom Automated Opportunity"),
            description=opp_data.get("description", "Automated cashflow mechanism"),
            category=cat_enum,
            target_market=opp_data.get("target_market", "B2B"),
            profit_potential_monthly=float(opp_data.get("profit_potential_monthly", 10000.0)),
            scalability_score=int(opp_data.get("scalability_score", 8)),
            sustainability_score=int(opp_data.get("sustainability_score", 8)),
            time_to_revenue_days=int(opp_data.get("time_to_revenue_days", 30)),
            capital_required=float(opp_data.get("capital_required", 1000.0)),
            competitive_advantage_score=int(opp_data.get("competitive_advantage_score", 7)),
            defensibility_score=int(opp_data.get("defensibility_score", 7)),
            risk_index=int(opp_data.get("risk_index", 3)),
            operational_complexity=int(opp_data.get("operational_complexity", 3))
        )

        ev, raroe, notes = OpportunityScorer.calculate_ev(opp, self.state_mgr.state.survival_state)
        opp.expected_value_score = ev
        opp.raroe_score = raroe
        opp.scoring_notes = notes

        self.state_mgr.add_opportunity(opp)
        self._log("EVALUATE", f"Custom opportunity '{opp.title}' scored: EV=${ev:,.2f}, RAROE={raroe}")
        return opp

    def create_venture_and_docs(self, venture_name: str, category: str, tagline: str, target_mrr: float = 15000.0, budget: float = 2000.0) -> Venture:
        slug = venture_name.lower().replace(" ", "-").replace("_", "")
        cat_enum = RevenuePriorityEnum(category) if category in [c.value for c in RevenuePriorityEnum] else RevenuePriorityEnum.SAAS

        venture = Venture(
            name=venture_name,
            slug=slug,
            tagline=tagline,
            category=cat_enum,
            status="ACTIVE",
            target_mrr=target_mrr,
            initial_budget=budget,
            key_metrics={"uptime_percentage": 99.99, "active_users": 0}
        )

        docs = DocumentGenerator.generate_full_suite(venture)
        venture.documents = docs

        v_dir = os.path.join(self.workspace_root, "ventures", slug)
        DocumentGenerator.write_to_disk(v_dir, docs)

        self.state_mgr.add_venture(venture)
        
        self.knowledge_base.add_entry(
            category=KnowledgeCategoryEnum.DECISION,
            title=f"Initialized Venture: {venture.name}",
            content=f"Created {venture.name} under {cat_enum.value} category. Generated canonical 16 markdown artifacts.",
            venture_id=venture.id,
            tags=["venture_creation", slug]
        )

        self._log("VENTURE_CREATED", f"Initialized {venture.name} ({venture.slug}) with 16 core documentation files in {v_dir}")
        return venture
