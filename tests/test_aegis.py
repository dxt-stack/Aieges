"""
Unit and Integration Test Suite for AEGIS Core Systems
"""

import pytest
import os
import shutil
from aegis.core.models import (
    Treasury, SurvivalStateEnum, RevenuePriorityEnum, Opportunity, Venture,
    KnowledgeCategoryEnum, GovernanceTypeEnum, GovernanceStatusEnum
)
from aegis.core.opportunity_scorer import OpportunityScorer
from aegis.core.decision_filter import DecisionFilter
from aegis.core.doc_generator import DocumentGenerator, MANDATORY_DOC_NAMES
from aegis.core.knowledge_base import KnowledgeBase
from aegis.governance import GovernanceManager
from aegis.orchestrator import AegisOrchestrator


def test_treasury_and_survival_states():
    # 1. Critical state: < 30 days runway
    # Reserves $5,000, Burn $8,000, Revenue $1,000 -> Net Burn $7,000/mo -> 5000/7000 * 30 = 21.4 days (< 30)
    t_crit = Treasury(cash_reserves=5000, monthly_burn=8000, monthly_revenue=1000)
    assert t_crit.calculated_survival_state == SurvivalStateEnum.CRITICAL
    assert t_crit.runway_days < 30

    # 2. Warning state: 30-90 days runway
    # Reserves $15,000, Burn $8,000, Revenue $0 -> Net Burn $8,000/mo -> 15000/8000 * 30 = 56.25 days (30-90)
    t_warn = Treasury(cash_reserves=15000, monthly_burn=8000, monthly_revenue=0)
    assert t_warn.calculated_survival_state == SurvivalStateEnum.WARNING

    # 3. Stable state: 90-365 days runway
    # Reserves $50,000, Burn $8,000, Revenue $3,000 -> Net Burn $5,000/mo -> 50000/5000 * 30 = 300 days (90-365)
    t_stable = Treasury(cash_reserves=50000, monthly_burn=8000, monthly_revenue=3000)
    assert t_stable.calculated_survival_state == SurvivalStateEnum.STABLE

    # 4. Strong state: 1-5 years (365-1825 days)
    # Reserves $200,000, Burn $10,000, Revenue $5,000 -> Net Burn $5,000/mo -> 200000/5000 * 30 = 1200 days
    t_strong = Treasury(cash_reserves=200000, monthly_burn=10000, monthly_revenue=5000)
    assert t_strong.calculated_survival_state == SurvivalStateEnum.STRONG

    # 5. Fortress state: > 5 years (> 1825 days) or Profitable
    t_fortress = Treasury(cash_reserves=500000, monthly_burn=5000, monthly_revenue=2000)
    assert t_fortress.calculated_survival_state == SurvivalStateEnum.FORTRESS

    # 6. Infinite runway when Profitable (Revenue >= Burn)
    t_prof = Treasury(cash_reserves=50000, monthly_burn=5000, monthly_revenue=7000)
    assert t_prof.net_burn == 0
    assert t_prof.calculated_survival_state == SurvivalStateEnum.FORTRESS


def test_opportunity_scorer_hierarchy_and_states():
    # SaaS vs Advertising priority
    opp_saas = Opportunity(
        title="B2B AI API",
        category=RevenuePriorityEnum.SAAS,
        target_market="SMBs",
        profit_potential_monthly=10000,
        scalability_score=9,
        sustainability_score=9,
        time_to_revenue_days=20,
        capital_required=1000,
        competitive_advantage_score=8,
        defensibility_score=8,
        risk_index=2,
        operational_complexity=2,
        description="Autonomous API"
    )

    opp_ad = Opportunity(
        title="Ad-supported Blog",
        category=RevenuePriorityEnum.ADVERTISING,
        target_market="General Web",
        profit_potential_monthly=10000,
        scalability_score=9,
        sustainability_score=9,
        time_to_revenue_days=20,
        capital_required=1000,
        competitive_advantage_score=8,
        defensibility_score=8,
        risk_index=2,
        operational_complexity=2,
        description="Ad revenue site"
    )

    ev_saas, raroe_saas, _ = OpportunityScorer.calculate_ev(opp_saas, SurvivalStateEnum.STABLE)
    ev_ad, raroe_ad, _ = OpportunityScorer.calculate_ev(opp_ad, SurvivalStateEnum.STABLE)

    # SaaS must score substantially higher than Advertising due to priority hierarchy weight (1.0 vs 0.4)
    assert ev_saas > ev_ad
    assert raroe_saas > raroe_ad

    # In CRITICAL state, fast revenue (< 14d) gets urgency boost
    opp_fast = Opportunity(
        title="Immediate Retainer B2B",
        category=RevenuePriorityEnum.B2B_SERVICES,
        target_market="Startups",
        profit_potential_monthly=5000,
        scalability_score=6,
        sustainability_score=7,
        time_to_revenue_days=7,
        capital_required=200,
        competitive_advantage_score=6,
        defensibility_score=5,
        risk_index=2,
        operational_complexity=3,
        description="Fast cashflow service"
    )
    ev_fast_crit, _, _ = OpportunityScorer.calculate_ev(opp_fast, SurvivalStateEnum.CRITICAL)
    ev_fast_fort, _, _ = OpportunityScorer.calculate_ev(opp_fast, SurvivalStateEnum.FORTRESS)
    assert ev_fast_crit > ev_fast_fort


def test_decision_filter_ethical_and_survival_rules():
    # 1. Illegal / Malicious action must be rejected immediately
    res_bad = DecisionFilter.evaluate(
        action_title="Phishing tool for account cracking",
        action_description="Scrapes private credentials and exploits APIs"
    )
    assert not res_bad.approved
    assert res_bad.violates_absolute_rules
    assert not res_bad.ethical_compliance
    assert "absolute prohibition" in res_bad.rationale

    # 2. Legitimate automated SaaS service must pass
    res_good = DecisionFilter.evaluate(
        action_title="Deploy automated billing webhook microservice",
        action_description="Provides recurring SaaS invoice automation with proprietary algorithm",
        current_state=SurvivalStateEnum.STABLE,
        expected_cash_impact_monthly=4500,
        capex_required=500,
        risk_level="LOW"
    )
    assert res_good.approved
    assert not res_good.violates_absolute_rules
    assert res_good.score >= 60


def test_16_mandatory_documents_generation():
    test_venture = Venture(
        name="ApexMetrics",
        slug="apexmetrics",
        tagline="Real-Time Autonomous Analytics for Stripe Merchants",
        category=RevenuePriorityEnum.SAAS,
        target_mrr=20000.0,
        initial_budget=1500.0
    )

    docs = DocumentGenerator.generate_full_suite(test_venture)

    # Must contain exactly the 16 mandatory files
    assert len(docs) == 16
    for required_file in MANDATORY_DOC_NAMES:
        assert required_file in docs
        assert len(docs[required_file]) > 100
        assert test_venture.name in docs[required_file]

    # Test writing to disk
    test_dir = "/tmp/aegis_test_venture"
    DocumentGenerator.write_to_disk(test_dir, docs)
    for required_file in MANDATORY_DOC_NAMES:
        assert os.path.exists(os.path.join(test_dir, required_file))
    shutil.rmtree(test_dir, ignore_errors=True)


def test_knowledge_base_compounding():
    kb_path = "/tmp/test_kb.json"
    if os.path.exists(kb_path):
        os.remove(kb_path)

    kb = KnowledgeBase(storage_path=kb_path)
    initial_count = len(kb.entries)

    entry = kb.add_entry(
        category=KnowledgeCategoryEnum.DECISION,
        title="Test Architectural Invariant",
        content="Stateless microservices ensure horizontal auto-scaling without session stickiness.",
        tags=["architecture", "scale"]
    )
    assert entry.id is not None
    assert len(kb.entries) == initial_count + 1

    decisions = kb.list_entries(category=KnowledgeCategoryEnum.DECISION)
    assert any(e.title == "Test Architectural Invariant" for e in decisions)

    if os.path.exists(kb_path):
        os.remove(kb_path)


def test_governance_escalation():
    gov_path = "/tmp/test_gov.json"
    if os.path.exists(gov_path):
        os.remove(gov_path)

    gov = GovernanceManager(storage_path=gov_path)
    req = gov.create_request(
        type=GovernanceTypeEnum.BANKING_AUTHORIZATION,
        title="Approve $10,000 payout to reserve treasury",
        description="Sweep operational profit",
        risk_level="MEDIUM"
    )

    assert req.status == GovernanceStatusEnum.PENDING
    resolved = gov.resolve(req.id, approved=True, notes="Approved by Governor")
    assert resolved is not None
    assert resolved.status == GovernanceStatusEnum.APPROVED
    assert resolved.resolved_at is not None

    if os.path.exists(gov_path):
        os.remove(gov_path)


def test_aegis_orchestrator_cycle():
    orchestrator = AegisOrchestrator(workspace_root="/tmp/aegis-test-workspace")
    result = orchestrator.execute_single_loop_cycle()

    assert result["status"] == "HEALTHY"
    assert result["cycle_number"] >= 1
    assert result["survival_state"] in [s.value for s in SurvivalStateEnum]
    assert len(orchestrator.execution_logs) > 0
