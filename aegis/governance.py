"""
AEGIS Governance Engine (Human-in-the-Loop Protocol)
Handles human approvals strictly when required by charter:
- Legal signatures
- Identity verification (KYC/AML)
- Banking / Treasury authorization
- Regulatory approval
- Ownership decisions
- Physical-world actions
"""

import json
import os
from typing import List, Optional
from aegis.core.utils import utc_now_iso
from aegis.core.models import GovernanceItem, GovernanceTypeEnum, GovernanceStatusEnum


class GovernanceManager:
    """
    Manages human governance escalation queues.
    """

    def __init__(self, storage_path: str = "/home/user/aegis/data/governance.json"):
        self.storage_path = storage_path
        self.items: List[GovernanceItem] = []
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.items = [GovernanceItem(**item) for item in data]
            except Exception:
                self.items = []
        else:
            self._seed_sample_items()
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump([item.model_dump() for item in self.items], f, indent=2)

    def _seed_sample_items(self):
        self.items = [
            GovernanceItem(
                type=GovernanceTypeEnum.BANKING_AUTHORIZATION,
                title="Stripe Payout Sweep to Fortress Treasury Account",
                description="AEGIS is scheduling an automated sweep of $12,500 accumulated merchant balance into the secure high-yield reserve vault.",
                risk_level="MEDIUM",
                status=GovernanceStatusEnum.PENDING
            ),
            GovernanceItem(
                type=GovernanceTypeEnum.LEGAL_SIGNATURE,
                title="Cloudflare Enterprise Data Processing Addendum (DPA)",
                description="Sign updated data privacy addendum to maintain strict GDPR/SOC2 compliance for European proxy nodes.",
                risk_level="LOW",
                status=GovernanceStatusEnum.PENDING
            )
        ]

    def create_request(self, type: GovernanceTypeEnum, title: str, description: str, risk_level: str = "MEDIUM", venture_id: Optional[str] = None) -> GovernanceItem:
        item = GovernanceItem(
            type=type,
            title=title,
            description=description,
            risk_level=risk_level,
            venture_id=venture_id,
            status=GovernanceStatusEnum.PENDING
        )
        self.items.insert(0, item)
        self._save()
        return item

    def resolve(self, item_id: str, approved: bool, notes: Optional[str] = None) -> Optional[GovernanceItem]:
        for item in self.items:
            if item.id == item_id:
                item.status = GovernanceStatusEnum.APPROVED if approved else GovernanceStatusEnum.REJECTED
                item.resolved_at = utc_now_iso()
                item.resolver_notes = notes or ("Approved by Governor" if approved else "Rejected by Governor")
                self._save()
                return item
        return None

    def get_pending(self) -> List[GovernanceItem]:
        return [item for item in self.items if item.status == GovernanceStatusEnum.PENDING]

    def get_all(self) -> List[GovernanceItem]:
        return self.items
