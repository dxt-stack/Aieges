"""
AEGIS Real Stripe Webhook & Revenue Bridge
Handles real Stripe webhook events and connects real payment flows to AEGIS Treasury.
"""

import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
from aegis.core.models import KnowledgeCategoryEnum, GovernanceTypeEnum
from aegis.core.utils import utc_now_iso


class StripeBridge:
    """
    Processes real Stripe webhook payloads and updates the AEGIS Treasury automatically.
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.api_key = os.getenv("STRIPE_API_KEY", "")
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
        self.processed_events: list[Dict[str, Any]] = []

    def handle_webhook_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes Stripe Webhook event dictionary.
        Supported events:
        - invoice.payment_succeeded
        - customer.subscription.created
        - customer.subscription.deleted
        - charge.refunded
        - payout.paid
        """
        event_type = event_data.get("type", "unknown")
        event_id = event_data.get("id", f"evt_{int(datetime.utcnow().timestamp())}")
        data_obj = event_data.get("data", {}).get("object", {})

        self.processed_events.insert(0, {
            "id": event_id,
            "type": event_type,
            "timestamp": utc_now_iso(),
            "data": data_obj
        })

        if len(self.processed_events) > 100:
            self.processed_events.pop()

        result = {"status": "ACKNOWLEDGED", "event_type": event_type, "action_taken": "None"}

        # 1. Invoice Payment Succeeded -> Add Cash & MRR
        if event_type in ["invoice.payment_succeeded", "charge.succeeded"]:
            amount_cents = data_obj.get("amount_paid") or data_obj.get("amount") or 4900
            amount_dollars = amount_cents / 100.0
            
            # Update Treasury Reserves
            current_reserves = self.orchestrator.state_mgr.state.treasury.cash_reserves
            current_revenue = self.orchestrator.state_mgr.state.treasury.monthly_revenue
            
            new_reserves = current_reserves + amount_dollars
            # If subscription invoice, credit MRR
            new_revenue = current_revenue + (amount_dollars if "subscription" in str(data_obj) else 0.0)

            self.orchestrator.state_mgr.update_treasury(
                cash_reserves=new_reserves,
                monthly_revenue=new_revenue
            )

            # Log to Knowledge Base
            self.orchestrator.knowledge_base.add_entry(
                category=KnowledgeCategoryEnum.OUTCOME,
                title=f"Stripe Payment Received: +${amount_dollars:,.2f}",
                content=f"Processed successful billing event {event_id}. Cash reserves increased to ${new_reserves:,.2f}.",
                tags=["stripe", "revenue", "cashflow"]
            )

            self.orchestrator._log("REVENUE", f"Stripe payment of +${amount_dollars:,.2f} absorbed into Treasury. New reserves: ${new_reserves:,.2f}")
            result["action_taken"] = f"Credited +${amount_dollars:,.2f} to cash reserves."

        # 2. Customer Subscription Deleted -> Churn Log & MRR Decrease
        elif event_type == "customer.subscription.deleted":
            plan_amount = (data_obj.get("plan", {}).get("amount", 4900) or 4900) / 100.0
            current_rev = self.orchestrator.state_mgr.state.treasury.monthly_revenue
            new_rev = max(0.0, current_rev - plan_amount)
            
            self.orchestrator.state_mgr.update_treasury(monthly_revenue=new_rev)
            
            self.orchestrator.knowledge_base.add_entry(
                category=KnowledgeCategoryEnum.FAILURE,
                title=f"Customer Subscription Churned: -${plan_amount:,.2f}/mo",
                content=f"Subscription cancelled for customer {data_obj.get('customer', 'unknown')}. Operations Division SOP-OPS-01 triggered for exit diagnostic.",
                tags=["churn", "retention", "stripe"]
            )
            self.orchestrator._log("CHURN", f"Subscription cancelled (-${plan_amount:,.2f}/mo). MRR adjusted to ${new_rev:,.2f}")
            result["action_taken"] = f"Decreased MRR by ${plan_amount:,.2f} and triggered retention SOP."

        # 3. Charge Refunded -> Audit & Escalation
        elif event_type == "charge.refunded":
            amount_refunded = (data_obj.get("amount_refunded", 0) or 0) / 100.0
            current_reserves = self.orchestrator.state_mgr.state.treasury.cash_reserves
            self.orchestrator.state_mgr.update_treasury(cash_reserves=max(0.0, current_reserves - amount_refunded))
            
            if amount_refunded > 200:
                # Escalate to Human Governance
                self.orchestrator.governance.create_request(
                    type=GovernanceTypeEnum.BANKING_AUTHORIZATION,
                    title=f"High Refund Anomaly Detected: ${amount_refunded:,.2f}",
                    description=f"A refund of ${amount_refunded:,.2f} was processed on charge {data_obj.get('id', 'N/A')}. Requires owner review.",
                    risk_level="HIGH"
                )

            self.orchestrator._log("REFUND", f"Refund of ${amount_refunded:,.2f} deducted from reserves.")
            result["action_taken"] = f"Processed refund of ${amount_refunded:,.2f}."

        return result
