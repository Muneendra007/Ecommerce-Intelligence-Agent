"""
Pydantic models for all request/response schemas.
Covers products, reviews, research I/O, structured output, and cost tracking.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────────────

class ResearchMode(str, Enum):
    QUICK = "quick"
    DEEP = "deep"

class BusinessGoal(str, Enum):
    GROWTH = "growth"
    RETENTION = "retention"
    PROFITABILITY = "profitability"
    MARGIN = "margin"
    REVENUE = "revenue"

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ── Product & Review Models ──────────────────────────────────

class SalesData(BaseModel):
    month: str
    units_sold: int
    revenue: int
    returns: int

class Product(BaseModel):
    sku: str
    name: str
    brand: str
    price: int
    rating: float
    marketplace: str
    category: str
    features: list[str]
    sales_data: list[SalesData] = []

class Review(BaseModel):
    brand: str
    sku: str
    rating: int
    review_text: str
    marketplace: str = "Amazon"
    date: str = ""
    verified_purchase: bool = True


# ── Research Request / Response ──────────────────────────────

class ResearchRequest(BaseModel):
    query: str
    mode: ResearchMode = ResearchMode.QUICK
    goal: Optional[BusinessGoal] = None
    sku: Optional[str] = None

class FollowUpRequest(BaseModel):
    session_id: str
    message: str

class MemoryStoreRequest(BaseModel):
    key: str
    value: str
    category: str = "preference"


# ── Structured Output Format ────────────────────────────────

class SentimentCluster(BaseModel):
    label: str
    percentage: float
    sample_reviews: list[str] = []
    review_count: int = 0

class CompetitorAdvantage(BaseModel):
    competitor: str
    advantage: str
    impact: str
    our_gap: str

class PricingAnalysis(BaseModel):
    our_price: int
    competitor_prices: dict[str, int] = {}
    price_position: str = ""
    recommendation: str = ""

class SalesTrendInsight(BaseModel):
    trend: str
    data_points: list[dict] = []
    analysis: str = ""

class StrategicRecommendation(BaseModel):
    action: str
    priority: str = "medium"
    expected_impact: str = ""
    confidence: str = "medium"

class CostReport(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0

class ClarifyingQuestion(BaseModel):
    question: str
    options: list[str] = []
    context: str = ""


# ── Full Structured Response ────────────────────────────────

class StructuredAnalysis(BaseModel):
    """The exact output format required by the spec."""
    executive_summary: str = ""
    sentiment_breakdown: list[SentimentCluster] = []
    competitor_advantages: list[CompetitorAdvantage] = []
    pricing_analysis: Optional[PricingAnalysis] = None
    sales_trend: Optional[SalesTrendInsight] = None
    recommendations: list[StrategicRecommendation] = []
    confidence_score: ConfidenceLevel = ConfidenceLevel.MEDIUM
    cost: CostReport = CostReport()

class ResearchResponse(BaseModel):
    session_id: str = ""
    mode: ResearchMode = ResearchMode.QUICK
    query: str = ""
    sku: Optional[str] = None
    detected_goal: Optional[str] = None
    analysis: StructuredAnalysis = StructuredAnalysis()
    clarifying_questions: list[ClarifyingQuestion] = []
    data_gaps: list[str] = []
    raw_response: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class HealthResponse(BaseModel):
    status: str
    llm_configured: bool
    qdrant_status: str
    demo_mode: bool
    total_reviews_indexed: int = 0
    version: str = "1.0.0"

class SKUListResponse(BaseModel):
    skus: list[Product]
    brand: str = "GlowSkin"
