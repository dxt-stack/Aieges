"""
AEGIS Base Organizational Division
Abstract base class for all 6 autonomous operating divisions.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from aegis.core.models import DivisionEnum, SurvivalStateEnum, Venture, Opportunity


class BaseDivision(ABC):
    """
    Base autonomous division worker.
    """

    def __init__(self, division_type: DivisionEnum):
        self.division_type = division_type

    @abstractmethod
    def execute_directive(
        self,
        task_name: str,
        parameters: Dict[str, Any],
        survival_state: SurvivalStateEnum,
        venture: Venture | None = None
    ) -> Dict[str, Any]:
        """
        Executes a domain-specific directive for the division.
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Returns list of autonomous workflows this division can run.
        """
        pass
