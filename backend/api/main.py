"""
FastAPI Application — E-Commerce Intelligence Agent API

Endpoints:
  GET  /api/health   — System health and status
  GET  /api/skus     — List available GlowSkin SKUs
  POST /api/research — Execute research query (Quick / Deep)
  POST /api/followup — Follow-up refinement on existing session
  GET  /api/memory   — Retrieve user preferences
  POST /api/memory   — Store user preference
"""

from __future__ import annotations
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Ensure backend root is on path
sys.path.insert(0, ".")

from config import settings
from models.schemas import (
    ResearchRequest, FollowUpRequest, MemoryStoreRequest,
    ResearchResponse, HealthResponse, SKUListResponse,
    ResearchMode, BusinessGoal, Product, SalesData,
)
from data.dataset import GLOWSKIN_PRODUCTS
from retrieval.ingestion import ingest_all_data, get_total_indexed
from memory.preference_store import preference_store
from services.reasoning import reasoning_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-30s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Lifespan ────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: ingest data into vector store. Shutdown: cleanup."""
    logger.info("🚀 Starting E-Commerce Intelligence Agent...")
    await preference_store.initialize()
    total = await ingest_all_data()
    logger.info(f"✅ Agent ready — {total} vectors indexed")
    yield
    logger.info("👋 Agent shutting down")


# ── App ─────────────────────────────────────────────────────

app = FastAPI(
    title="E-Commerce Intelligence Agent",
    description="AI-powered growth analyst for D2C skincare brand GlowSkin",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ──────────────────────────────────────────────────

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """System health check."""
    return HealthResponse(
        status="ok",
        llm_configured=settings.is_llm_configured(),
        qdrant_status="connected" if settings.is_qdrant_configured() else "in-memory-fallback",
        demo_mode=not settings.is_llm_configured(),
        total_reviews_indexed=get_total_indexed(),
        version="2.1.0",
    )


@app.get("/api/skus", response_model=SKUListResponse)
async def list_skus():
    """List available GlowSkin SKUs with product details."""
    products = [
        Product(
            sku=p["sku"],
            name=p["name"],
            brand=p["brand"],
            price=p["price"],
            rating=p["rating"],
            marketplace=p["marketplace"],
            category=p["category"],
            features=p["features"],
            sales_data=[SalesData(**s) for s in p["sales_data"]],
        )
        for p in GLOWSKIN_PRODUCTS
    ]
    return SKUListResponse(skus=products)


@app.post("/api/research", response_model=ResearchResponse)
async def research(req: ResearchRequest):
    """
    Execute a research query.

    Modes:
      - quick: Top complaints, sentiment summary, price comparison (<30s)
      - deep: Full diagnosis with all analysis dimensions (<3min)
    """
    try:
        result = await reasoning_engine.research(
            query=req.query,
            mode=req.mode,
            goal=req.goal,
            sku=req.sku,
        )
        return result
    except Exception as e:
        logger.error(f"Research error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/followup", response_model=ResearchResponse)
async def followup(req: FollowUpRequest):
    """Handle follow-up refinements on an existing research session."""
    try:
        result = await reasoning_engine.followup(
            session_id=req.session_id,
            message=req.message,
        )
        return result
    except Exception as e:
        logger.error(f"Follow-up error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/memory")
async def get_memory():
    """Retrieve stored user preferences."""
    prefs = await preference_store.get_all_preferences()
    return {"preferences": prefs}


@app.post("/api/memory")
async def store_memory(req: MemoryStoreRequest):
    """Store a user preference."""
    await preference_store.set_preference(req.key, req.value)
    return {"status": "stored", "key": req.key, "value": req.value}
