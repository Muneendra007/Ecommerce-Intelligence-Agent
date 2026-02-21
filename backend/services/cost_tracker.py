"""
Cost Tracker
Tracks input/output tokens, displays cost per query, enforces budget limits.
"""

from __future__ import annotations
import logging
from config import settings

logger = logging.getLogger(__name__)

# Pricing per million tokens (GPT-4o estimates)
INPUT_COST_PER_M = 5.0    # $5 per 1M input tokens
OUTPUT_COST_PER_M = 15.0   # $15 per 1M output tokens


class CostTracker:
    """
    Tracks LLM token usage and cost per query.
    Enforces configurable max token budget.
    """

    def __init__(self):
        self._session_costs: dict[str, dict] = {}
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_cost_usd = 0.0

    def get_budget(self, mode: str) -> dict:
        """Get token budget for a mode."""
        if mode == "quick":
            return {
                "max_tokens": settings.QUICK_MODE_TOKEN_BUDGET,
                "max_cost_usd": 0.05,
                "timeout_sec": 30,
            }
        else:
            return {
                "max_tokens": settings.DEEP_MODE_TOKEN_BUDGET,
                "max_cost_usd": settings.MAX_COST_PER_REQUEST,
                "timeout_sec": 180,
            }

    def check_budget(self, mode: str) -> bool:
        """Check if current session is within budget."""
        budget = self.get_budget(mode)
        return self._total_cost_usd < budget["max_cost_usd"]

    def track_usage(self, session_id: str, input_tokens: int,
                    output_tokens: int) -> dict:
        """Track token usage for a query and return cost report."""
        input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_M
        output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_M
        total_cost = input_cost + output_cost

        self._total_input_tokens += input_tokens
        self._total_output_tokens += output_tokens
        self._total_cost_usd += total_cost

        cost_report = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "estimated_cost_usd": round(total_cost, 6),
        }

        self._session_costs[session_id] = cost_report
        logger.info(
            f"Cost [{session_id}]: {input_tokens}+{output_tokens} tokens, "
            f"${total_cost:.6f}"
        )
        return cost_report

    def get_session_cost(self, session_id: str) -> dict:
        """Get cost report for a specific session."""
        return self._session_costs.get(session_id, {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "estimated_cost_usd": 0.0,
        })

    def get_total_cost(self) -> dict:
        """Get cumulative cost across all sessions."""
        return {
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "total_cost_usd": round(self._total_cost_usd, 6),
            "sessions_tracked": len(self._session_costs),
        }


# Singleton
cost_tracker = CostTracker()
