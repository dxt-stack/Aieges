"""
AEGIS Knowledge Compounding Ledger
Stores and compounds decisions, assumptions, experiments, outcomes, failures, and lessons learned.
Policy: 'Knowledge compounds. Undocumented knowledge is lost capital.'
"""

import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from aegis.core.models import KnowledgeEntry, KnowledgeCategoryEnum


class KnowledgeBase:
    """
    Manages structured organizational memory and compounding insights.
    """

    def __init__(self, storage_path: str = "/home/user/aegis/data/knowledge_base.json"):
        self.storage_path = storage_path
        self.entries: List[KnowledgeEntry] = []
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.entries = [KnowledgeEntry(**item) for item in data]
            except Exception:
                self.entries = []
        else:
            self._seed_initial_knowledge()
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump([entry.model_dump() for entry in self.entries], f, indent=2)

    def _seed_initial_knowledge(self):
        self.entries = [
            KnowledgeEntry(
                category=KnowledgeCategoryEnum.DECISION,
                title="Adopt Headless Autonomous Micro-SaaS Architecture",
                content="AEGIS will exclusively build and deploy headless API-first software services that require near-zero human labor and support automated billing through Stripe.",
                tags=["architecture", "automation", "saas"]
            ),
            KnowledgeEntry(
                category=KnowledgeCategoryEnum.ASSUMPTION,
                title="Programmatic Inbound CAC is Sub-$150",
                content="Assuming niche programmatic SEO pages and curated tool listings convert B2B operators at an effective customer acquisition cost under $150.",
                tags=["marketing", "cac", "seo"]
            ),
            KnowledgeEntry(
                category=KnowledgeCategoryEnum.EXPERIMENT,
                title="Automated Dunning Sequences on Churn Reduction",
                content="Testing a 3-step automated webhook dunning sequence on payment failures against single retry baseline.",
                tags=["retention", "billing", "experiment"]
            ),
            KnowledgeEntry(
                category=KnowledgeCategoryEnum.LESSON,
                title="Multi-Cloud API Redundancy is Essential",
                content="Relying on a single AI inference endpoint creates an existential single point of failure. Always maintain instant hot-failover providers.",
                tags=["engineering", "resilience", "redundancy"]
            )
        ]

    def add_entry(self, category: KnowledgeCategoryEnum, title: str, content: str, venture_id: Optional[str] = None, tags: Optional[List[str]] = None) -> KnowledgeEntry:
        entry = KnowledgeEntry(
            category=category,
            title=title,
            content=content,
            venture_id=venture_id,
            tags=tags or []
        )
        self.entries.insert(0, entry)
        self._save()
        return entry

    def list_entries(self, category: Optional[KnowledgeCategoryEnum] = None, venture_id: Optional[str] = None, search: Optional[str] = None) -> List[KnowledgeEntry]:
        results = self.entries
        if category:
            results = [e for e in results if e.category == category]
        if venture_id:
            results = [e for e in results if e.venture_id == venture_id]
        if search:
            q = search.lower()
            results = [e for e in results if q in e.title.lower() or q in e.content.lower() or any(q in t.lower() for t in e.tags)]
        return results

    def get_summary_stats(self) -> Dict[str, int]:
        stats = {cat.value: 0 for cat in KnowledgeCategoryEnum}
        for entry in self.entries:
            stats[entry.category.value] = stats.get(entry.category.value, 0) + 1
        stats["TOTAL"] = len(self.entries)
        return stats
