"""
AEGIS REST API & Application Server
FastAPI-powered backend for the Autonomous Economic Growth & Intelligent Survival System.
"""

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
import hashlib
import hmac
import time
from pathlib import Path
from aegis.orchestrator import AegisOrchestrator
from aegis.core.models import (
    SurvivalStateEnum, RevenuePriorityEnum, GovernanceTypeEnum,
    KnowledgeCategoryEnum, Opportunity, Venture
)
from aegis.core.opportunity_scorer import OpportunityScorer
from aegis.core.decision_filter import DecisionFilter
from aegis.core.doc_generator import DocumentGenerator
from aegis.integrations.stripe_bridge import StripeBridge
from aegis.integrations.research_engine import LiveResearchEngine
from aegis.integrations.code_generator import VentureCodeGenerator
from aegis.daemon.daemon import AegisDaemon

app = FastAPI(
    title="AEGIS Autonomous Intelligence API",
    description="Autonomous Economic Growth & Intelligent Survival System API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("AEGIS_CORS_ORIGINS", "http://localhost:8000").split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def protect_mutations(request: Request, call_next):
    """Protect state-changing routes when AEGIS_API_KEY is configured."""
    configured_key = os.getenv("AEGIS_API_KEY")
    if configured_key and request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        supplied_key = request.headers.get("X-Aegis-Key", "")
        if not hmac.compare_digest(supplied_key, configured_key):
            return JSONResponse({"detail": "Missing or invalid X-Aegis-Key"}, status_code=401)
    return await call_next(request)

workspace_root = os.getenv("AEGIS_WORKSPACE", str(Path(__file__).resolve().parent))
static_dir = os.path.join(workspace_root, "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize Orchestrator, Stripe Bridge, and Daemon singletons
orchestrator = AegisOrchestrator(workspace_root=workspace_root)
stripe_bridge = StripeBridge(orchestrator)
daemon = AegisDaemon(orchestrator, interval_seconds=45)

# Ensure software bundles are present for active ventures
for v in orchestrator.state_mgr.ventures.values():
    v_dir = os.path.join(orchestrator.workspace_root, "ventures", v.slug)
    VentureCodeGenerator.generate_software_bundle(
        venture_dir=v_dir,
        name=v.name,
        slug=v.slug,
        category=v.category.value if hasattr(v.category, 'value') else str(v.category),
        tagline=v.tagline
    )


# ==========================================
# API Models
# ==========================================
class TreasuryUpdateRequest(BaseModel):
    cash_reserves: Optional[float] = None
    monthly_burn: Optional[float] = None
    monthly_revenue: Optional[float] = None


class OpportunityCreateRequest(BaseModel):
    title: str
    description: str
    category: str
    target_market: str = "B2B SMBs"
    profit_potential_monthly: float
    scalability_score: int
    sustainability_score: int
    time_to_revenue_days: int
    capital_required: float
    competitive_advantage_score: int
    defensibility_score: int
    risk_index: int
    operational_complexity: int


class DecisionFilterRequest(BaseModel):
    action_title: str
    action_description: str
    expected_cash_impact_monthly: float = 0.0
    capex_required: float = 0.0
    risk_level: str = "LOW"


class VentureCreateRequest(BaseModel):
    name: str
    tagline: str
    category: str
    target_mrr: float = 15000.0
    initial_budget: float = 2000.0


class GovernanceResolutionRequest(BaseModel):
    approved: bool
    notes: Optional[str] = None


class KnowledgeCreateRequest(BaseModel):
    category: str
    title: str
    content: str
    venture_id: Optional[str] = None
    tags: List[str] = []


class DivisionExecuteRequest(BaseModel):
    task_name: str
    parameters: Dict[str, Any] = {}
    venture_id: Optional[str] = None


class StripeSimulateRequest(BaseModel):
    event_type: str  # invoice.payment_succeeded, customer.subscription.deleted, charge.refunded
    amount: float = 149.0
    customer: str = "cus_aegis_corp"


class UrlAuditRequest(BaseModel):
    url: str


# ==========================================
# Endpoints
# ==========================================

@app.get("/api/status")
async def get_system_status():
    state = orchestrator.state_mgr.state
    return {
        "status": "OPERATIONAL",
        "name": state.name,
        "version": state.version,
        "survival_state": state.survival_state.value,
        "treasury": {
            "cash_reserves": state.treasury.cash_reserves,
            "monthly_burn": state.treasury.monthly_burn,
            "monthly_revenue": state.treasury.monthly_revenue,
            "net_burn": state.treasury.net_burn,
            "runway_days": round(state.treasury.runway_days, 1),
            "target_reserves": state.treasury.target_reserves,
            "updated_at": state.treasury.updated_at
        },
        "loop_active": daemon.is_running,
        "loop_iteration": state.loop_iteration,
        "last_loop_timestamp": state.last_loop_timestamp,
        "active_ventures_count": len([v for v in orchestrator.state_mgr.ventures.values() if v.status == "ACTIVE"]),
        "total_opportunities_count": len(orchestrator.state_mgr.opportunities),
        "pending_governance_count": len(orchestrator.governance.get_pending()),
        "knowledge_entries_count": len(orchestrator.knowledge_base.entries),
        "operational_efficiency_index": state.operational_efficiency_index
    }


@app.post("/api/daemon/start")
async def start_daemon():
    await daemon.start()
    return {"message": "AEGIS Autonomous Daemon activated", "status": daemon.get_status()}


@app.post("/api/daemon/stop")
async def stop_daemon():
    await daemon.stop()
    return {"message": "AEGIS Autonomous Daemon halted", "status": daemon.get_status()}


@app.get("/api/daemon/status")
async def get_daemon_status():
    return daemon.get_status()


@app.post("/api/treasury/update")
async def update_treasury(payload: TreasuryUpdateRequest):
    updated = orchestrator.state_mgr.update_treasury(
        cash_reserves=payload.cash_reserves,
        monthly_burn=payload.monthly_burn,
        monthly_revenue=payload.monthly_revenue
    )
    return {
        "message": "Treasury updated",
        "treasury": updated.model_dump(),
        "survival_state": orchestrator.state_mgr.state.survival_state.value,
        "runway_days": round(updated.runway_days, 1)
    }


@app.post("/api/loop/execute-step")
async def execute_loop_step():
    result = orchestrator.execute_single_loop_cycle()
    return result


@app.get("/api/loop/logs")
async def get_execution_logs(limit: int = 50):
    return orchestrator.execution_logs[:limit]


@app.get("/api/opportunities")
async def list_opportunities():
    all_opps = list(orchestrator.state_mgr.opportunities.values())
    ranked = OpportunityScorer.score_and_rank(all_opps, orchestrator.current_state)
    return ranked


@app.post("/api/opportunities/evaluate")
async def evaluate_opportunity(payload: OpportunityCreateRequest):
    opp = orchestrator.evaluate_custom_opportunity(payload.model_dump())
    return opp


@app.post("/api/filter/evaluate")
async def run_decision_filter(payload: DecisionFilterRequest):
    result = DecisionFilter.evaluate(
        action_title=payload.action_title,
        action_description=payload.action_description,
        current_state=orchestrator.current_state,
        expected_cash_impact_monthly=payload.expected_cash_impact_monthly,
        capex_required=payload.capex_required,
        risk_level=payload.risk_level
    )
    return result


@app.get("/api/ventures")
async def list_ventures():
    return list(orchestrator.state_mgr.ventures.values())


@app.get("/api/ventures/{venture_id}")
async def get_venture(venture_id: str):
    v = orchestrator.state_mgr.ventures.get(venture_id)
    if not v:
        raise HTTPException(status_code=404, detail="Venture not found")
    return v


@app.get("/api/ventures/{venture_id}/docs/{doc_name}")
async def get_venture_doc(venture_id: str, doc_name: str):
    v = orchestrator.state_mgr.ventures.get(venture_id)
    if not v:
        raise HTTPException(status_code=404, detail="Venture not found")
    
    if doc_name in v.documents:
        return {"venture_name": v.name, "doc_name": doc_name, "content": v.documents[doc_name]}
    
    v_dir = os.path.join(orchestrator.workspace_root, "ventures", v.slug)
    doc_path = os.path.join(v_dir, doc_name)
    if os.path.exists(doc_path):
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
            v.documents[doc_name] = content
            return {"venture_name": v.name, "doc_name": doc_name, "content": content}

    raise HTTPException(status_code=404, detail=f"Document '{doc_name}' not found for venture {v.name}")


@app.get("/api/ventures/{venture_id}/files/{filename}")
async def get_venture_code_file(venture_id: str, filename: str):
    v = orchestrator.state_mgr.ventures.get(venture_id)
    if not v:
        raise HTTPException(status_code=404, detail="Venture not found")
    
    v_dir = os.path.join(orchestrator.workspace_root, "ventures", v.slug)
    file_path = os.path.join(v_dir, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return {"venture_name": v.name, "filename": filename, "content": content}

    raise HTTPException(status_code=404, detail=f"File '{filename}' not found in venture bundle")


@app.post("/api/ventures/create")
async def create_venture(payload: VentureCreateRequest):
    venture = orchestrator.create_venture_and_docs(
        venture_name=payload.name,
        category=payload.category,
        tagline=payload.tagline,
        target_mrr=payload.target_mrr,
        budget=payload.initial_budget
    )
    return venture


@app.get("/api/knowledge")
async def list_knowledge(category: Optional[str] = None, search: Optional[str] = None):
    cat_enum = None
    if category:
        try:
            cat_enum = KnowledgeCategoryEnum(category.upper())
        except ValueError:
            cat_enum = None
    return {
        "stats": orchestrator.knowledge_base.get_summary_stats(),
        "entries": orchestrator.knowledge_base.list_entries(category=cat_enum, search=search)
    }


@app.post("/api/knowledge/create")
async def create_knowledge_entry(payload: KnowledgeCreateRequest):
    cat_enum = KnowledgeCategoryEnum(payload.category.upper()) if payload.category.upper() in [c.value for c in KnowledgeCategoryEnum] else KnowledgeCategoryEnum.LESSON
    entry = orchestrator.knowledge_base.add_entry(
        category=cat_enum,
        title=payload.title,
        content=payload.content,
        venture_id=payload.venture_id,
        tags=payload.tags
    )
    return entry


@app.get("/api/governance")
async def get_governance_requests():
    return {
        "pending": orchestrator.governance.get_pending(),
        "all": orchestrator.governance.get_all()
    }


@app.post("/api/governance/{item_id}/resolve")
async def resolve_governance(item_id: str, payload: GovernanceResolutionRequest):
    resolved = orchestrator.governance.resolve(item_id, approved=payload.approved, notes=payload.notes)
    if not resolved:
        raise HTTPException(status_code=404, detail="Governance item not found")
    
    orchestrator.knowledge_base.add_entry(
        category=KnowledgeCategoryEnum.DECISION,
        title=f"Governor {'Approved' if payload.approved else 'Rejected'}: {resolved.title}",
        content=f"Resolution: {'APPROVED' if payload.approved else 'REJECTED'}. Notes: {payload.notes or 'None'}",
        tags=["governance", "human_approval" if payload.approved else "human_rejection"]
    )

    return resolved


@app.post("/api/divisions/{division_name}/execute")
async def execute_division_directive(division_name: str, payload: DivisionExecuteRequest):
    div_name_upper = division_name.upper()
    venture = orchestrator.state_mgr.ventures.get(payload.venture_id) if payload.venture_id else None
    survival_state = orchestrator.current_state

    division_map = {
        "RESEARCH": orchestrator.research_div,
        "PRODUCT": orchestrator.product_div,
        "ENGINEERING": orchestrator.engineering_div,
        "MARKETING": orchestrator.marketing_div,
        "OPERATIONS": orchestrator.operations_div,
        "FINANCE": orchestrator.finance_div
    }

    if div_name_upper not in division_map:
        raise HTTPException(status_code=400, detail=f"Invalid division. Must be one of: {list(division_map.keys())}")

    div = division_map[div_name_upper]
    result = div.execute_directive(
        task_name=payload.task_name,
        parameters=payload.parameters,
        survival_state=survival_state,
        venture=venture
    )

    orchestrator._log(f"DIV_{div_name_upper}", f"Executed '{payload.task_name}' successfully.")
    return result


@app.post("/api/stripe/webhook")
async def receive_stripe_webhook(request: Request):
    """Receives live Stripe webhooks."""
    raw_body = await request.body()
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    signature = request.headers.get("Stripe-Signature")
    if webhook_secret:
        if not signature:
            raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")
        timestamp = next((part[2:] for part in signature.split(",") if part.startswith("t=")), None)
        signatures = [part[2:] for part in signature.split(",") if part.startswith("v1=")]
        signed_payload = f"{timestamp}.{raw_body.decode('utf-8')}" if timestamp else ""
        expected = hmac.new(webhook_secret.encode(), signed_payload.encode(), hashlib.sha256).hexdigest()
        try:
            timestamp_valid = timestamp is not None and abs(time.time() - int(timestamp)) <= 300
        except ValueError:
            timestamp_valid = False
        if not timestamp_valid or not signatures or not any(hmac.compare_digest(expected, item) for item in signatures):
            raise HTTPException(status_code=400, detail="Invalid Stripe webhook signature")
    try:
        payload = __import__("json").loads(raw_body)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    res = stripe_bridge.handle_webhook_event(payload)
    return res


@app.post("/api/stripe/simulate")
async def simulate_stripe_event(payload: StripeSimulateRequest):
    """Simulates a live billing or refund event to demonstrate real treasury reaction."""
    cents = int(payload.amount * 100)
    fake_event = {
        "id": f"evt_sim_{int(time.time())}",
        "type": payload.event_type,
        "data": {
            "object": {
                "amount_paid": cents,
                "amount": cents,
                "amount_refunded": cents,
                "customer": payload.customer,
                "plan": {"amount": cents}
            }
        }
    }
    res = stripe_bridge.handle_webhook_event(fake_event)
    return res


@app.post("/api/research/audit-url")
async def audit_url_endpoint(payload: UrlAuditRequest):
    """Audits any live URL in real-time."""
    try:
        result = LiveResearchEngine.audit_url(payload.url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result


@app.get("/", response_class=HTMLResponse)
async def serve_cockpit_dashboard():
    index_path = os.path.join(workspace_root, "templates", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    return HTMLResponse(content="<h1>AEGIS System Bootstrapping...</h1>", status_code=200)
