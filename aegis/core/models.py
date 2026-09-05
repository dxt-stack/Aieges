"""
AEGIS Core Models & Types
Autonomous Economic Growth & Intelligent Survival System
"""

from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import uuid
from aegis.core.utils import utc_now_iso


class SurvivalStateEnum(str, Enum):
    CRITICAL = "CRITICAL"    # Runway < 30 days
    WARNING = "WARNING"      # Runway 30–90 days
    STABLE = "STABLE"        # Runway 3–12 months (90–365 days)
    STRONG = "STRONG"        # Runway 1–5 years (365–1825 days)
    FORTRESS = "FORTRESS"    # Runway > 5 years (> 1825 days)


class RevenuePriorityEnum(str, Enum):
    SAAS = "SaaS"
    SUBSCRIPTION = "Subscription businesses"
    LICENSING = "Licensing"
    B2B_SERVICES = "B2B services"
    AUTOMATION_SERVICES = "Automation services"
    DIGITAL_PRODUCTS = "Digital products"
    EDUCATION = "Education"
    MARKETPLACES = "Marketplaces"
    MEDIA = "Media"
    ADVERTISING = "Advertising"


class DivisionEnum(str, Enum):
    RESEARCH = "RESEARCH"
    PRODUCT = "PRODUCT"
    ENGINEERING = "ENGINEERING"
    MARKETING = "MARKETING"
    OPERATIONS = "OPERATIONS"
    FINANCE = "FINANCE"


class GovernanceTypeEnum(str, Enum):
    LEGAL_SIGNATURE = "Legal Signature Required"
    IDENTITY_VERIFICATION = "Identity Verification (KYC/AML)"
    BANKING_AUTHORIZATION = "Banking / Treasury Authorization"
    REGULATORY_APPROVAL = "Regulatory Approval"
    OWNERSHIP_DECISION = "Ownership / Equity Decision"
    PHYSICAL_WORLD = "Physical-World Action"


class GovernanceStatusEnum(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class KnowledgeCategoryEnum(str, Enum):
    DECISION = "DECISION"
    ASSUMPTION = "ASSUMPTION"
    EXPERIMENT = "EXPERIMENT"
    OUTCOME = "OUTCOME"
    FAILURE = "FAILURE"
    LESSON = "LESSON"


class Treasury(BaseModel):
    cash_reserves: float = Field(default=50000.0, description="Current cash reserves in USD")
    monthly_burn: float = Field(default=8000.0, description="Monthly cash burn rate in USD")
    monthly_revenue: float = Field(default=4500.0, description="Current MRR in USD")
    target_reserves: float = Field(default=250000.0, description="Target cash fortress reserves")
    updated_at: str = Field(default_factory=utc_now_iso)

    @property
    def net_burn(self) -> float:
        return max(0.0, self.monthly_burn - self.monthly_revenue)

    @property
    def runway_days(self) -> float:
        if self.net_burn <= 0:
            return 9999.0  # Profitable / infinite runway
        months = self.cash_reserves / self.net_burn
        return months * 30.0

    @property
    def calculated_survival_state(self) -> SurvivalStateEnum:
        days = self.runway_days
        if days < 30:
            return SurvivalStateEnum.CRITICAL
        elif days < 90:
            return SurvivalStateEnum.WARNING
        elif days < 365:
            return SurvivalStateEnum.STABLE
        elif days <= 1825:
            return SurvivalStateEnum.STRONG
        else:
            return SurvivalStateEnum.FORTRESS


class Opportunity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str
    description: str
    category: RevenuePriorityEnum
    target_market: str
    profit_potential_monthly: float = Field(description="Projected monthly net profit after stabilization ($)")
    scalability_score: int = Field(ge=1, le=10, description="1-10 rating on ability to scale with near-zero marginal cost")
    sustainability_score: int = Field(ge=1, le=10, description="1-10 rating on long-term durability & churn resistance")
    time_to_revenue_days: int = Field(description="Estimated days to first dollar of revenue")
    capital_required: float = Field(description="Initial capital requirement ($)")
    competitive_advantage_score: int = Field(ge=1, le=10, description="1-10 moat & competitive edge")
    defensibility_score: int = Field(ge=1, le=10, description="1-10 IP / switching cost / barrier to entry")
    risk_index: int = Field(ge=1, le=10, description="1-10 risk of failure or market rejection")
    operational_complexity: int = Field(ge=1, le=10, description="1-10 human / mechanical overhead")
    expected_value_score: float = Field(default=0.0, description="Computed multi-factor EV score")
    raroe_score: float = Field(default=0.0, description="Risk-Adjusted Return on Effort (0-100)")
    status: str = Field(default="EVALUATED", description="DISCOVERED, EVALUATED, APPROVED, IN_DEVELOPMENT, LAUNCHED, ARCHIVED")
    created_at: str = Field(default_factory=utc_now_iso)
    scoring_notes: str = ""


class DecisionFilterResult(BaseModel):
    approved: bool
    increase_survival: bool
    increase_durable_cashflow: bool
    reduce_risk: bool
    strengthen_competitive_advantage: bool
    improve_sustainability: bool
    violates_absolute_rules: bool = False
    ethical_compliance: bool = True
    score: int
    rationale: str
    action_item: str


class GovernanceItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: GovernanceTypeEnum
    title: str
    description: str
    venture_id: Optional[str] = None
    risk_level: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    status: GovernanceStatusEnum = GovernanceStatusEnum.PENDING
    created_at: str = Field(default_factory=utc_now_iso)
    resolved_at: Optional[str] = None
    resolver_notes: Optional[str] = None


class KnowledgeEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    category: KnowledgeCategoryEnum
    title: str
    content: str
    venture_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=utc_now_iso)


class Venture(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str
    slug: str
    tagline: str
    category: RevenuePriorityEnum
    status: str = "ACTIVE"  # PLANNING, ACTIVE, SCALING, PAUSED, TERMINATED
    target_mrr: float = 0.0
    current_mrr: float = 0.0
    initial_budget: float = 0.0
    spent_to_date: float = 0.0
    created_at: str = Field(default_factory=utc_now_iso)
    documents: Dict[str, str] = Field(default_factory=dict)
    key_metrics: Dict[str, Any] = Field(default_factory=dict)


class SystemState(BaseModel):
    version: str = "1.0.0"
    name: str = "AEGIS"
    survival_state: SurvivalStateEnum = SurvivalStateEnum.STABLE
    treasury: Treasury = Field(default_factory=Treasury)
    loop_active: bool = False
    loop_iteration: int = 0
    last_loop_timestamp: Optional[str] = None
    active_ventures_count: int = 0
    total_opportunities_evaluated: int = 0
    governance_pending_count: int = 0
    operational_efficiency_index: float = 94.5
    updated_at: str = Field(default_factory=utc_now_iso)
