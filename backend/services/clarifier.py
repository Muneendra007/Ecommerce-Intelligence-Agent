"""
Interactive Clarifier
Asks clarifying questions when the user's objective is unclear.
Generates context-aware clarifications based on query analysis.
"""

from __future__ import annotations
import logging
from typing import Optional

from models.schemas import ClarifyingQuestion, BusinessGoal

logger = logging.getLogger(__name__)

# Keywords that indicate specific intent
GOAL_KEYWORDS = {
    "margin": BusinessGoal.MARGIN,
    "profit": BusinessGoal.PROFITABILITY,
    "revenue": BusinessGoal.REVENUE,
    "growth": BusinessGoal.GROWTH,
    "retention": BusinessGoal.RETENTION,
    "churn": BusinessGoal.RETENTION,
    "cost": BusinessGoal.MARGIN,
}

SKU_KEYWORDS = ["vitc30", "hyalu50", "reta15", "vitamin c", "moisturizer",
                "hyaluronic", "retinol", "night cream", "serum"]

FOCUS_KEYWORDS = {
    "negative": "negative_reviews",
    "complaint": "negative_reviews",
    "problem": "negative_reviews",
    "issue": "negative_reviews",
    "bad": "negative_reviews",
    "positive": "positive_reviews",
    "good": "positive_reviews",
    "love": "positive_reviews",
    "competitor": "competitors",
    "compare": "competitors",
    "vs": "competitors",
}


class Clarifier:
    """
    Analyzes user queries and generates clarifying questions
    when the objective is ambiguous.
    """

    def needs_clarification(self, query: str, sku: Optional[str],
                            goal: Optional[str]) -> list[ClarifyingQuestion]:
        """
        Determine if the query needs clarification.
        Returns a list of questions if clarification is needed.
        """
        questions = []
        query_lower = query.lower()

        # Check if business goal is clear
        detected_goal = self._detect_goal(query_lower)
        if not detected_goal and not goal:
            questions.append(ClarifyingQuestion(
                question="What business objective should I optimize for?",
                options=["Revenue growth", "Margin optimization", "Customer retention", "Market share"],
                context="Different objectives lead to different analysis and recommendations.",
            ))

        # Check if SKU is specified
        detected_sku = self._detect_sku(query_lower)
        if not detected_sku and not sku:
            # Only ask if query seems product-specific
            if any(w in query_lower for w in ["product", "sku", "which", "specific", "underperforming"]):
                questions.append(ClarifyingQuestion(
                    question="Which SKU would you like me to analyze?",
                    options=["VITC30 — Vitamin C Serum", "HYALU50 — Hyaluronic Acid Moisturizer", "RETA15 — Retinol Night Cream", "All SKUs"],
                    context="Focusing on a specific SKU enables deeper analysis.",
                ))

        # Check marketplace scope
        if "flipkart" in query_lower or "all marketplace" in query_lower:
            questions.append(ClarifyingQuestion(
                question="Should I focus on Amazon only or include other marketplaces?",
                options=["Amazon only", "All marketplaces"],
                context="Currently we have Amazon data. Other marketplace data is limited.",
            ))

        # Check review focus
        if not self._detect_focus(query_lower):
            if "review" in query_lower or "sentiment" in query_lower:
                questions.append(ClarifyingQuestion(
                    question="Should I analyze all reviews or focus on specific ones?",
                    options=["All reviews", "Negative reviews only (1-2★)", "Recent reviews (last 30 days)"],
                    context="Focusing on negative reviews surfaces actionable improvement areas.",
                ))

        return questions

    def _detect_goal(self, query: str) -> Optional[str]:
        """Detect business goal from query keywords."""
        for keyword, goal in GOAL_KEYWORDS.items():
            if keyword in query:
                return goal.value
        return None

    def _detect_sku(self, query: str) -> Optional[str]:
        """Detect SKU reference in query."""
        sku_map = {
            "vitc30": "VITC30", "vitamin c": "VITC30", "serum": "VITC30",
            "hyalu50": "HYALU50", "hyaluronic": "HYALU50", "moisturizer": "HYALU50",
            "reta15": "RETA15", "retinol": "RETA15", "night cream": "RETA15",
        }
        for keyword, sku in sku_map.items():
            if keyword in query:
                return sku
        return None

    def _detect_focus(self, query: str) -> Optional[str]:
        """Detect review focus from query."""
        for keyword, focus in FOCUS_KEYWORDS.items():
            if keyword in query:
                return focus
        return None

    def enrich_query_context(self, query: str) -> dict:
        """Extract all detectable context from query text."""
        query_lower = query.lower()
        return {
            "detected_goal": self._detect_goal(query_lower),
            "detected_sku": self._detect_sku(query_lower),
            "detected_focus": self._detect_focus(query_lower),
        }


# Singleton
clarifier = Clarifier()
