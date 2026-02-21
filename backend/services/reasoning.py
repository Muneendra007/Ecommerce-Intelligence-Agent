"""
AI Agent Reasoning Engine
The core intelligence layer that uses Gemini LLM as the brain for all analysis.

The LLM receives all retrieved context (reviews, competitor data, pricing, sales)
and generates structured business insights through reasoning — not templates.

Quick Mode (<30s): Focused analysis on the specific question
Deep Mode  (<3min): Comprehensive multi-dimensional diagnosis with strategic recommendations
"""

from __future__ import annotations
import json
import logging
import uuid
from typing import Optional
from collections import Counter

from config import settings
from data.dataset import get_product_by_sku, get_brand_products, GLOWSKIN_PRODUCTS, ALL_PRODUCTS
from retrieval.embedding_service import embedding_service
from retrieval.vector_store import vector_store, REVIEW_COLLECTION, COMPETITOR_COLLECTION
from memory.preference_store import preference_store
from services.clarifier import clarifier
from services.cost_tracker import cost_tracker
from services.llm_service import llm_service
from models.schemas import (
    ResearchMode, BusinessGoal, ConfidenceLevel,
    ResearchResponse, StructuredAnalysis,
    SentimentCluster, CompetitorAdvantage, PricingAnalysis,
    SalesTrendInsight, StrategicRecommendation, CostReport,
    ClarifyingQuestion,
)

logger = logging.getLogger(__name__)

# ── Agent System Prompt ──────────────────────────────────────

AGENT_SYSTEM_PROMPT = """You are an expert E-Commerce Intelligence Agent for GlowSkin, a D2C skincare brand on Amazon India.

Your role: Analyze customer reviews, competitor data, pricing, and sales trends to deliver actionable business insights.

RULES:
- Be data-driven: cite specific numbers, percentages, and patterns from the provided data
- Be actionable: every insight should lead to a clear recommendation
- Be honest: if data is insufficient, say so. Never fabricate statistics
- Speak like a senior business analyst — professional, concise, numbers-focused
- Focus on the specific business goal the user cares about
- Reference specific competitor advantages and customer pain points by name
- When analyzing sentiment, identify THEMES (not just counts) — what are people actually saying?
- Consider market trends and seasonal patterns in your analysis

FORMATTING RULES for executive_summary:
- Use **Bold** for critical metrics and key insights
- Use `---` (horizontal dividers) to separate major sections
- Use bullet points for lists
- Make it look like a professional intelligence report
"""


class SessionManager:
    """Tracks active research sessions for follow-up support."""

    def __init__(self):
        self._sessions: dict[str, dict] = {}

    def create(self, query: str, mode: ResearchMode, goal: BusinessGoal,
               sku: Optional[str] = None) -> str:
        sid = str(uuid.uuid4())[:8]
        self._sessions[sid] = {
            "id": sid, "query": query, "mode": mode,
            "goal": goal, "sku": sku, "history": [],
        }
        return sid

    def get(self, sid: str) -> Optional[dict]:
        return self._sessions.get(sid)

    def add_turn(self, sid: str, role: str, content: str):
        s = self._sessions.get(sid)
        if s:
            s["history"].append({"role": role, "content": content})


session_manager = SessionManager()


class ReasoningEngine:
    """
    AI Agent reasoning engine.
    Retrieves relevant data via semantic search, then uses Gemini LLM
    to reason over the data and produce structured business analysis.
    Falls back to rule-based analysis if LLM is unavailable.
    """

    # ── Public API ──────────────────────────────────────────

    async def research(
        self,
        query: str,
        mode: ResearchMode,
        goal: Optional[BusinessGoal] = None,
        sku: Optional[str] = None,
        skip_clarification: bool = False,
    ) -> ResearchResponse:
        """Execute a research query in Quick or Deep mode."""

        session_id = session_manager.create(query, mode, goal, sku)
        session_manager.add_turn(session_id, "user", query)

        # Check if the query is a casual/greeting message (not a business question)
        conversational_reply = await self._handle_conversational(query, session_id, mode)
        if conversational_reply:
            return conversational_reply

        # Parallelize early detection tasks: Goal, SKU/Context, and start embedding the query
        # This saves significant time by not waiting for LLM sequentially
        import asyncio
        detection_tasks = [
            self._detect_goal(query) if not goal else asyncio.sleep(0, result=goal),
            asyncio.to_thread(clarifier.enrich_query_context, query),
            embedding_service.embed_text(query)
        ]
        
        # Wait for all three to complete concurrently
        goal_result, context, query_embedding = await asyncio.gather(*detection_tasks)
        
        resolved_goal = goal_result
        resolved_sku = sku or context.get("detected_sku")
        
        if not goal:
            logger.info(f"🧠 Auto-detected business goal: {resolved_goal.value}")

        # Check if clarification is needed
        if not skip_clarification:
            questions = clarifier.needs_clarification(query, resolved_sku, resolved_goal.value)
            if questions and not resolved_sku:
                return ResearchResponse(
                    session_id=session_id,
                    mode=mode,
                    query=query,
                    sku=resolved_sku,
                    clarifying_questions=questions,
                )

        # Validate SKU
        product = None
        if resolved_sku:
            product = get_product_by_sku(resolved_sku)
            if not product:
                return self._error_response(
                    session_id, mode, query,
                    f"SKU '{resolved_sku}' not found. Available: VITC30, HYALU50, RETA15"
                )

        # Apply memory preferences
        await asyncio.gather(
            preference_store.get_all_preferences(),
            preference_store.update_from_query(sku=resolved_sku, goal=resolved_goal.value)
        )

        # Retrieve reviews and competitor data in parallel using the pre-computed embedding
        retrieval_tasks = [
            self._retrieve_reviews_with_embedding(query, resolved_sku, query_embedding),
            self._retrieve_competitor_features_with_embedding(query, query_embedding)
        ]
        reviews, competitors = await asyncio.gather(*retrieval_tasks)

        # Handle data gaps logic
        if len(reviews) < 5:
            data_gaps = ["Low review volume retrieved. Results may have limited statistical significance."]
        else:
            data_gaps = []

        # Execute mode-specific analysis
        if mode == ResearchMode.QUICK:
            analysis = await self._quick_analysis(query, resolved_sku, resolved_goal, product, reviews, competitors)
        else:
            analysis = await self._deep_analysis(query, resolved_sku, resolved_goal, product, reviews, competitors)

        # Track cost
        cost = cost_tracker.track_usage(session_id, 0, 0)
        analysis.cost = CostReport(**cost)

        if not llm_service.is_live:
            data_gaps.append("Running in basic mode — add GOOGLE_API_KEY for AI-powered insights")

        response = ResearchResponse(
            session_id=session_id,
            mode=mode,
            query=query,
            sku=resolved_sku,
            detected_goal=resolved_goal.value,
            analysis=analysis,
            data_gaps=data_gaps,
        )

        session_manager.add_turn(session_id, "assistant", analysis.executive_summary)
        return response

    async def followup(self, session_id: str, message: str) -> ResearchResponse:
        """Handle follow-up in an existing session."""
        session = session_manager.get(session_id)
        if not session:
            return self._error_response(session_id, ResearchMode.QUICK, message,
                                        "Session not found. Start a new query.")

        session_manager.add_turn(session_id, "user", message)

        # Build enriched context
        enriched = f"Original: {session['query']}\nFollow-up: {message}"
        context = clarifier.enrich_query_context(message)
        new_sku = context.get("detected_sku") or session.get("sku")
        new_goal = BusinessGoal(context.get("detected_goal") or session["goal"].value)

        return await self.research(
            query=enriched,
            mode=session["mode"],
            goal=new_goal,
            sku=new_sku,
            skip_clarification=True,
        )
    # ── Conversational Intent Detection ─────────────────────

    async def _handle_conversational(self, query: str, session_id: str,
                                      mode: ResearchMode) -> Optional[ResearchResponse]:
        """Detect greetings, casual chat, or vague queries and respond naturally."""
        is_casual = await self._is_casual_query(query)
        if not is_casual:
            return None

        # Generate a friendly response using LLM if available
        if llm_service.is_live:
            try:
                prompt = (
                    "You are an AI E-Commerce Intelligence Agent for GlowSkin skincare brand. "
                    "The user sent a casual or greeting message instead of a business question.\n\n"
                    f"User message: \"{query}\"\n\n"
                    "Respond warmly in 2-3 sentences. Greet them, introduce yourself briefly, "
                    "and suggest what they can ask you. Mention you can analyze customer reviews, "
                    "compare competitors, and provide business insights for their skincare products "
                    "(Vitamin C Serum, Hyaluronic Moisturizer, Retinol Cream). "
                    "Keep it friendly and professional."
                )
                reply = await llm_service.generate(prompt)
            except Exception:
                reply = self._default_greeting()
        else:
            reply = self._default_greeting()

        return ResearchResponse(
            session_id=session_id,
            mode=mode,
            query=query,
            detected_goal="conversational",
            analysis=StructuredAnalysis(executive_summary=reply),
        )

    async def _is_casual_query(self, query: str) -> bool:
        """Detect if a query is casual/greeting rather than a business question."""
        q = query.strip().lower()

        # Quick keyword check first (fast path)
        casual_patterns = [
            "hi", "hello", "hey", "hii", "hiii", "yo", "sup",
            "good morning", "good afternoon", "good evening", "good night",
            "thanks", "thank you", "bye", "goodbye", "see you",
            "how are you", "what's up", "whats up", "wassup",
            "who are you", "what are you", "what can you do",
            "help", "ok", "okay", "cool", "nice", "great",
        ]
        if q in casual_patterns or len(q) <= 3:
            return True

        # For longer but ambiguous queries, ask LLM
        if llm_service.is_live and len(q) < 50:
            try:
                prompt = (
                    "Is this a business/product question about e-commerce, skincare, sales, "
                    "reviews, competitors, or pricing? Or is it casual chat/greeting?\n\n"
                    f"Query: \"{query}\"\n\n"
                    "Respond with ONLY 'business' or 'casual', nothing else."
                )
                result = await llm_service.generate(prompt)
                return "casual" in result.strip().lower()
            except Exception:
                pass

        return False

    def _default_greeting(self) -> str:
        return (
            "👋 Hello! I'm your GlowSkin E-Commerce Intelligence Agent. "
            "I can analyze customer reviews, compare you against competitors like DermaCare "
            "and PureSkin, diagnose sales trends, and provide strategic recommendations. "
            "Try asking me something like: \"What are the top complaints for our Vitamin C Serum?\" "
            "or \"How do we compare against DermaCare?\""
        )

    # ── AI Goal Detection ────────────────────────────────────

    async def _detect_goal(self, query: str) -> BusinessGoal:
        """Use LLM to infer the business goal from the user's query."""
        if llm_service.is_live:
            try:
                prompt = (
                    "Classify this business query into exactly one category: "
                    "growth, retention, profitability, margin, revenue.\n\n"
                    f"Query: \"{query}\"\n\n"
                    "Respond with ONLY the category word."
                )
                raw = await llm_service.generate(prompt)
                detected = raw.strip().lower().replace('"', '').replace("'", "")

                # Map to valid enum
                goal_map = {
                    "growth": BusinessGoal.GROWTH,
                    "retention": BusinessGoal.RETENTION,
                    "profitability": BusinessGoal.PROFITABILITY,
                    "margin": BusinessGoal.MARGIN,
                    "revenue": BusinessGoal.REVENUE,
                }
                if detected in goal_map:
                    return goal_map[detected]

                logger.warning(f"LLM returned unexpected goal '{detected}', falling back to keyword detection")
            except Exception as e:
                logger.warning(f"LLM goal detection failed: {e}, falling back to keywords")

        # Fallback: keyword-based detection
        return self._detect_goal_by_keywords(query)

    def _detect_goal_by_keywords(self, query: str) -> BusinessGoal:
        """Fallback keyword-based goal detection."""
        q = query.lower()
        keyword_map = {
            BusinessGoal.RETENTION: ["return", "churn", "losing", "leave", "cancel", "refund", "complaint", "unhappy", "dissatisfied"],
            BusinessGoal.PROFITABILITY: ["profit", "margin", "cost", "expensive", "cheap", "pricing", "markup", "savings"],
            BusinessGoal.MARGIN: ["price", "pricing", "discount", "premium", "value", "worth"],
            BusinessGoal.REVENUE: ["revenue", "sales volume", "order value", "upsell", "cross-sell", "basket"],
            BusinessGoal.GROWTH: ["grow", "increase", "expand", "acquire", "new customer", "market share", "scale"],
        }
        for goal, keywords in keyword_map.items():
            if any(kw in q for kw in keywords):
                return goal
        return BusinessGoal.GROWTH  # Default

    # ── Retrieval ───────────────────────────────────────────

    async def _retrieve_reviews(self, query: str, sku: Optional[str],
                                 limit: int = 30) -> list[dict]:
        """Retrieve top-k relevant reviews using semantic search."""
        query_embedding = await embedding_service.embed_text(query)
        return await self._retrieve_reviews_with_embedding(query, sku, query_embedding, limit)
    async def _retrieve_reviews_with_embedding(self, query: str, sku: Optional[str],
                                              query_embedding: list[float],
                                              limit: int = 30) -> list[dict]:
        """Internal retrieval using pre-computed embedding."""
        filters = {}
        if sku:
            filters["sku"] = sku

        results = vector_store.search(
            collection=REVIEW_COLLECTION,
            query_vector=query_embedding,
            limit=limit,
            filters=filters if filters else None,
        )

        return [r["payload"] for r in results]

    async def _retrieve_competitor_features(self, query: str) -> list[dict]:
        """Retrieve competitor features relevant to the query."""
        query_embedding = await embedding_service.embed_text(query)
        return await self._retrieve_competitor_features_with_embedding(query, query_embedding)

    async def _retrieve_competitor_features_with_embedding(self, query: str,
                                                         query_embedding: list[float]) -> list[dict]:
        """Internal retrieval using pre-computed embedding."""
        results = vector_store.search(
            collection=COMPETITOR_COLLECTION,
            query_vector=query_embedding,
            limit=6,
        )

        return [r["payload"] for r in results]

    # ── LLM-Powered Analysis ────────────────────────────────

    async def _quick_analysis(
        self, query: str, sku: Optional[str], goal: BusinessGoal,
        product: Optional[dict], reviews: list[dict], competitors: list[dict],
    ) -> StructuredAnalysis:
        """Quick mode: AI-powered concise insights."""

        # Compute base data
        sentiment = self._compute_sentiment(reviews)
        pricing = self._compute_pricing(sku)

        if llm_service.is_live:
            # Build comprehensive context for the AI agent
            context = self._build_context_prompt(
                query, sku, goal, product, reviews, competitors, pricing, mode="quick"
            )

            prompt = f"""{AGENT_SYSTEM_PROMPT}

{context}

TASK: Provide a QUICK analysis responding to the user's question.
Respond ONLY with valid JSON in this exact format (no markdown, no code fences):
{{
    "executive_summary": "2-3 sentence professional summary with specific numbers",
    "key_sentiment_themes": ["theme1: description", "theme2: description", "theme3: description"],
    "competitor_gaps": [
        {{"competitor": "name", "advantage": "what they do better", "our_gap": "what we should do"}}
    ],
    "recommendations": [
        {{"action": "specific action", "priority": "high/medium/low", "expected_impact": "measurable outcome"}}
    ]
}}"""

            try:
                raw = await llm_service.generate(prompt)
                return self._parse_llm_quick_response(raw, sentiment, pricing, reviews)
            except Exception as e:
                logger.error(f"LLM quick analysis failed: {e}")

        # Fallback to rule-based analysis
        return self._fallback_quick_analysis(query, sku, goal, product, reviews, competitors, sentiment, pricing)

    async def _deep_analysis(
        self, query: str, sku: Optional[str], goal: BusinessGoal,
        product: Optional[dict], reviews: list[dict], competitors: list[dict],
    ) -> StructuredAnalysis:
        """Deep mode: comprehensive AI-powered analysis."""

        # Compute base data
        sentiment = self._compute_sentiment(reviews, detailed=True)
        pricing = self._compute_pricing(sku)
        sales_trend = self._analyze_sales_trend(product)

        if llm_service.is_live:
            context = self._build_context_prompt(
                query, sku, goal, product, reviews, competitors, pricing,
                sales_trend=sales_trend, mode="deep"
            )

            prompt = f"""{AGENT_SYSTEM_PROMPT}

{context}

TASK: Provide a DEEP, comprehensive analysis responding to the user's question.
Think step-by-step through each dimension. Be thorough and data-driven.
Respond ONLY with valid JSON in this exact format (no markdown, no code fences):
{{
    "executive_summary": "3-4 sentence professional summary highlighting risks, opportunities, and specific metrics",
    "sentiment_analysis": {{
        "overall_assessment": "detailed paragraph about customer sentiment patterns",
        "positive_themes": ["theme with evidence"],
        "negative_themes": ["theme with evidence"],
        "critical_insight": "the most important finding from reviews"
    }},
    "competitor_gaps": [
        {{"competitor": "name (SKU)", "advantage": "specific advantage", "impact": "business impact", "our_gap": "recommended action"}}
    ],
    "pricing_insight": "paragraph about pricing position and strategy",
    "sales_trend_analysis": "paragraph about sales trajectory and root causes",
    "recommendations": [
        {{"action": "specific actionable step", "priority": "high/medium/low", "expected_impact": "quantified outcome", "confidence": "high/medium/low"}}
    ],
    "risk_factors": ["risk1", "risk2"]
}}"""

            try:
                raw = await llm_service.generate(prompt)
                return self._parse_llm_deep_response(raw, sentiment, pricing, sales_trend, reviews)
            except Exception as e:
                logger.error(f"LLM deep analysis failed: {e}")

        # Fallback to rule-based analysis
        return self._fallback_deep_analysis(query, sku, goal, product, reviews, competitors, sentiment, pricing, sales_trend)

    # ── Context Builder ─────────────────────────────────────

    def _build_context_prompt(
        self, query: str, sku: Optional[str], goal: BusinessGoal,
        product: Optional[dict], reviews: list[dict], competitors: list[dict],
        pricing: Optional[PricingAnalysis], sales_trend: Optional[SalesTrendInsight] = None,
        mode: str = "quick",
    ) -> str:
        """Build a rich context prompt with all retrieved data for the LLM."""

        parts = [f"USER QUESTION: {query}", f"BUSINESS GOAL: {goal.value}"]

        # Product info
        if product:
            parts.append(f"\nPRODUCT: {product['name']} (SKU: {product['sku']})")
            parts.append(f"Price: ₹{product['price']} | Rating: {product['rating']}★")
            parts.append(f"Features: {', '.join(product['features'])}")
            if product.get("market_trends"):
                trends = product["market_trends"]
                parts.append(f"Market Trends: Category growing {trends.get('category_growth_rate', 'N/A')}, "
                           f"Peak season: {trends.get('seasonal_peak', 'N/A')}, "
                           f"Online share: {trends.get('online_share', 'N/A')}")

        # Sales data
        if sales_trend:
            parts.append(f"\nSALES TREND: {sales_trend.trend}")
            parts.append(f"Analysis: {sales_trend.analysis}")

        # Pricing data
        if pricing:
            parts.append(f"\nPRICING: Our price ₹{pricing.our_price} | {pricing.price_position}")
            if pricing.competitor_prices:
                price_str = ", ".join(f"{k}: ₹{v}" for k, v in pricing.competitor_prices.items())
                parts.append(f"Competitor prices: {price_str}")

        # Reviews (sample)
        if reviews:
            parts.append(f"\nCUSTOMER REVIEWS ({len(reviews)} retrieved):")
            # Group by rating for better context
            by_rating = {}
            for r in reviews:
                rating = r.get("rating", 3)
                by_rating.setdefault(rating, []).append(r["review_text"])

            for rating in sorted(by_rating.keys(), reverse=True):
                texts = by_rating[rating]
                sample_size = 5 if mode == "deep" else 3
                sample = texts[:sample_size]
                parts.append(f"  {rating}★ ({len(texts)} reviews): " + " | ".join(sample))

        # Competitor data
        if competitors:
            parts.append(f"\nCOMPETITOR DATA ({len(competitors)} products):")
            for comp in competitors:
                parts.append(f"  {comp['brand']} - {comp['name']} (SKU: {comp['sku']}) "
                           f"₹{comp['price']} | {comp['rating']}★")
                parts.append(f"    Features: {comp.get('features_text', 'N/A')}")

        return "\n".join(parts)

    # ── LLM Response Parsers ────────────────────────────────

    def _parse_llm_quick_response(
        self, raw: str, sentiment: list[SentimentCluster],
        pricing: Optional[PricingAnalysis], reviews: list[dict],
    ) -> StructuredAnalysis:
        """Parse LLM JSON response into StructuredAnalysis for quick mode."""
        try:
            # Clean potential markdown code fences
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
                if cleaned.endswith("```"):
                    cleaned = cleaned.rsplit("```", 1)[0]
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("Failed to parse LLM JSON response, using raw text")
            return StructuredAnalysis(
                executive_summary=raw[:500],
                sentiment_breakdown=sentiment,
                pricing_analysis=pricing,
                confidence_score=ConfidenceLevel.MEDIUM if len(reviews) > 10 else ConfidenceLevel.LOW,
            )

        # Build competitor advantages
        comp_advantages = []
        for gap in data.get("competitor_gaps", []):
            comp_advantages.append(CompetitorAdvantage(
                competitor=gap.get("competitor", "Unknown"),
                advantage=gap.get("advantage", ""),
                impact="Market share pressure",
                our_gap=gap.get("our_gap", ""),
            ))

        # Build recommendations
        recommendations = []
        for rec in data.get("recommendations", []):
            recommendations.append(StrategicRecommendation(
                action=rec.get("action", ""),
                priority=rec.get("priority", "medium"),
                expected_impact=rec.get("expected_impact", ""),
                confidence="medium",
            ))

        # Merge qualitative AI themes into sentiment clusters
        ai_themes = data.get("key_sentiment_themes", [])
        combined_sentiment = list(sentiment)
        for theme in ai_themes:
            combined_sentiment.append(SentimentCluster(
                label="Insight",
                percentage=0, # Informative
                sample_reviews=[theme],
                review_count=0
            ))

        return StructuredAnalysis(
            executive_summary=data.get("executive_summary", raw[:300]),
            sentiment_breakdown=combined_sentiment,
            competitor_advantages=comp_advantages,
            pricing_analysis=pricing,
            recommendations=recommendations,
            confidence_score=ConfidenceLevel.MEDIUM if len(reviews) > 10 else ConfidenceLevel.LOW,
        )

    def _parse_llm_deep_response(
        self, raw: str, sentiment: list[SentimentCluster],
        pricing: Optional[PricingAnalysis], sales_trend: Optional[SalesTrendInsight],
        reviews: list[dict],
    ) -> StructuredAnalysis:
        """Parse LLM JSON response into StructuredAnalysis for deep mode."""
        try:
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
                if cleaned.endswith("```"):
                    cleaned = cleaned.rsplit("```", 1)[0]
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("Failed to parse LLM deep JSON response, using raw text")
            return StructuredAnalysis(
                executive_summary=raw[:500],
                sentiment_breakdown=sentiment,
                pricing_analysis=pricing,
                sales_trend=sales_trend,
                confidence_score=self._compute_confidence(reviews, None),
            )

        # Build competitor advantages
        comp_advantages = []
        for gap in data.get("competitor_gaps", []):
            comp_advantages.append(CompetitorAdvantage(
                competitor=gap.get("competitor", "Unknown"),
                advantage=gap.get("advantage", ""),
                impact=gap.get("impact", "Competitive pressure"),
                our_gap=gap.get("our_gap", ""),
            ))

        # Build recommendations
        recommendations = []
        for rec in data.get("recommendations", []):
            recommendations.append(StrategicRecommendation(
                action=rec.get("action", ""),
                priority=rec.get("priority", "medium"),
                expected_impact=rec.get("expected_impact", ""),
                confidence=rec.get("confidence", "medium"),
            ))

        # Enrich executive summary with sales/pricing insights from LLM
        exec_summary = data.get("executive_summary", raw[:500])
        if data.get("sales_trend_analysis") and sales_trend:
            sales_trend = SalesTrendInsight(
                trend=sales_trend.trend,
                data_points=sales_trend.data_points,
                analysis=data["sales_trend_analysis"],
            )

        # Merge qualitative AI themes into sentiment clusters
        ai_themes = data.get("key_sentiment_themes", [])
        combined_sentiment = list(sentiment)
        for theme in ai_themes:
            combined_sentiment.append(SentimentCluster(
                label="Insight",
                percentage=0,
                sample_reviews=[theme],
                review_count=0
            ))

        return StructuredAnalysis(
            executive_summary=exec_summary,
            sentiment_breakdown=combined_sentiment,
            competitor_advantages=comp_advantages,
            pricing_analysis=pricing,
            sales_trend=sales_trend,
            recommendations=recommendations,
            confidence_score=self._compute_confidence(reviews, None),
        )

    # ── Fallback Rule-Based Analysis ────────────────────────

    def _fallback_quick_analysis(
        self, query, sku, goal, product, reviews, competitors, sentiment, pricing,
    ) -> StructuredAnalysis:
        """Fallback when LLM is unavailable — template-based quick analysis."""
        negative_reviews = [r for r in reviews if r.get("rating", 5) <= 2]
        complaint_texts = [r["review_text"] for r in negative_reviews[:5]]

        competitor_summary = self._quick_competitor_gap(product, competitors)

        product_name = product["name"] if product else "GlowSkin products"
        exec_summary = (
            f"Quick analysis for {product_name}. "
            f"Sentiment: {sentiment[0].percentage:.0f}% positive, "
            f"{sentiment[-1].percentage:.0f}% negative across {len(reviews)} retrieved reviews. "
        )
        if complaint_texts:
            exec_summary += f"Top complaint theme: '{complaint_texts[0][:80]}...'. "
        if pricing:
            exec_summary += f"Price position: {pricing.price_position}. "

        recommendations = []
        if negative_reviews:
            recommendations.append(StrategicRecommendation(
                action=f"Address top complaint: {complaint_texts[0][:100] if complaint_texts else 'quality concerns'}",
                priority="high",
                expected_impact="Could improve rating by 0.2-0.3 stars",
                confidence="medium",
            ))
        if pricing and "above" in pricing.price_position.lower():
            recommendations.append(StrategicRecommendation(
                action=pricing.recommendation,
                priority="medium",
                expected_impact="Increase unit volume by 10-15%",
                confidence="medium",
            ))

        return StructuredAnalysis(
            executive_summary=exec_summary,
            sentiment_breakdown=sentiment,
            competitor_advantages=competitor_summary,
            pricing_analysis=pricing,
            recommendations=recommendations,
            confidence_score=ConfidenceLevel.MEDIUM if len(reviews) > 10 else ConfidenceLevel.LOW,
        )

    def _fallback_deep_analysis(
        self, query, sku, goal, product, reviews, competitors, sentiment, pricing, sales_trend,
    ) -> StructuredAnalysis:
        """Fallback when LLM is unavailable — template-based deep analysis."""
        competitor_advantages = self._deep_competitor_analysis(product, competitors)
        recommendations = self._generate_recommendations(
            goal, product, reviews, sentiment, competitor_advantages, pricing, sales_trend
        )
        confidence = self._compute_confidence(reviews, product)

        product_name = product["name"] if product else "GlowSkin portfolio"
        neg_pct = next((s.percentage for s in sentiment if s.label == "Negative"), 0)
        pos_pct = next((s.percentage for s in sentiment if s.label == "Positive"), 0)

        exec_summary = (
            f"Deep analysis for {product_name}. "
            f"Analysis based on {len(reviews)} semantically retrieved reviews. "
            f"Sentiment: {pos_pct:.0f}% positive, {neg_pct:.0f}% negative. "
        )
        if sales_trend and "declining" in sales_trend.trend.lower():
            exec_summary += f"⚠️ Sales trend: {sales_trend.trend}. "
        if competitor_advantages:
            exec_summary += f"Identified {len(competitor_advantages)} competitive gaps. "
        exec_summary += f"Overall confidence: {confidence.value}."

        return StructuredAnalysis(
            executive_summary=exec_summary,
            sentiment_breakdown=sentiment,
            competitor_advantages=competitor_advantages,
            pricing_analysis=pricing,
            sales_trend=sales_trend,
            recommendations=recommendations,
            confidence_score=confidence,
        )

    # ── Analysis Helpers ────────────────────────────────────

    def _compute_sentiment(self, reviews: list[dict], detailed: bool = False) -> list[SentimentCluster]:
        """Compute sentiment breakdown from review ratings."""
        if not reviews:
            return [SentimentCluster(label="No-Data", percentage=100)]

        total = len(reviews)
        rating_counts = Counter(r.get("rating", 3) for r in reviews)

        positive = rating_counts.get(5, 0) + rating_counts.get(4, 0)
        neutral = rating_counts.get(3, 0)
        negative = rating_counts.get(2, 0) + rating_counts.get(1, 0)

        clusters = [
            SentimentCluster(
                label="Positive",
                percentage=round((positive / total) * 100, 1) if total else 0,
                review_count=positive,
                sample_reviews=[r["review_text"] for r in reviews if r.get("rating", 0) >= 4][:3],
            ),
            SentimentCluster(
                label="Neutral",
                percentage=round((neutral / total) * 100, 1) if total else 0,
                review_count=neutral,
                sample_reviews=[r["review_text"] for r in reviews if r.get("rating", 0) == 3][:2],
            ),
            SentimentCluster(
                label="Negative",
                percentage=round((negative / total) * 100, 1) if total else 0,
                review_count=negative,
                sample_reviews=[r["review_text"] for r in reviews if r.get("rating", 0) <= 2][:3],
            ),
        ]

        if detailed:
            for star in range(5, 0, -1):
                count = rating_counts.get(star, 0)
                clusters.append(SentimentCluster(
                    label=f"{star}★",
                    percentage=round((count / total) * 100, 1) if total else 0,
                    review_count=count,
                    sample_reviews=[r["review_text"] for r in reviews if r.get("rating") == star][:2],
                ))

        return clusters

    def _compute_pricing(self, sku: Optional[str]) -> Optional[PricingAnalysis]:
        """Compute pricing analysis against competitors."""
        if not sku:
            return None

        product = get_product_by_sku(sku)
        if not product:
            return None

        competitor_prices = {}
        for p in ALL_PRODUCTS:
            if p["brand"] != "GlowSkin" and p["category"] == product["category"]:
                competitor_prices[f"{p['brand']} {p['name'].split()[-2]} {p['name'].split()[-1]}"] = p["price"]

        avg_competitor = sum(competitor_prices.values()) / len(competitor_prices) if competitor_prices else product["price"]
        diff_pct = ((product["price"] - avg_competitor) / avg_competitor) * 100

        if diff_pct > 5:
            position = f"Priced {diff_pct:.0f}% above competitor average (₹{avg_competitor:.0f})"
            rec = f"Consider price test at ₹{int(avg_competitor * 1.02)} to close competitive gap"
        elif diff_pct < -5:
            position = f"Priced {abs(diff_pct):.0f}% below competitor average — room for premium positioning"
            rec = f"Evaluate price increase to ₹{int(product['price'] * 1.08)} if quality perception supports it"
        else:
            position = f"Competitively priced within {abs(diff_pct):.0f}% of market average"
            rec = "Maintain current pricing; differentiate on value-adds"

        return PricingAnalysis(
            our_price=product["price"],
            competitor_prices=competitor_prices,
            price_position=position,
            recommendation=rec,
        )

    def _analyze_sales_trend(self, product: Optional[dict]) -> Optional[SalesTrendInsight]:
        """Analyze 3-month sales trend for a product."""
        if not product or "sales_data" not in product:
            return None

        sales = product["sales_data"]
        if len(sales) < 2:
            return None

        units = [s["units_sold"] for s in sales]
        revenue = [s["revenue"] for s in sales]
        returns = [s["returns"] for s in sales]

        unit_change = ((units[-1] - units[0]) / units[0]) * 100
        return_rate_latest = (returns[-1] / units[-1]) * 100 if units[-1] else 0
        return_rate_first = (returns[0] / units[0]) * 100 if units[0] else 0

        if unit_change < -10:
            trend = f"Declining — units down {abs(unit_change):.0f}% over 3 months"
        elif unit_change > 10:
            trend = f"Growing — units up {unit_change:.0f}% over 3 months"
        else:
            trend = f"Stable — {unit_change:+.0f}% change over 3 months"

        analysis = (
            f"Monthly units: {' → '.join(str(u) for u in units)}. "
            f"Return rate: {return_rate_first:.1f}% → {return_rate_latest:.1f}%. "
        )
        if return_rate_latest > return_rate_first + 2:
            analysis += "⚠️ Return rate increasing — investigate quality or expectation mismatch."

        return SalesTrendInsight(
            trend=trend,
            data_points=[
                {"month": s["month"], "units": s["units_sold"],
                 "revenue": s["revenue"], "returns": s["returns"]}
                for s in sales
            ],
            analysis=analysis,
        )

    def _quick_competitor_gap(self, product: Optional[dict],
                               competitors: list[dict]) -> list[CompetitorAdvantage]:
        """Quick overview of competitor advantages."""
        if not product or not competitors:
            return []

        our_features = set(f.lower() for f in product.get("features", []))
        advantages = []

        for comp in competitors[:3]:
            advantage = ""
            gap = ""

            if comp.get("price", 9999) < product["price"]:
                advantage = f"Lower price point (₹{comp['price']} vs ₹{product['price']})"
                gap = "Price premium not justified by current feature set"
            elif comp.get("rating", 0) > product["rating"]:
                advantage = f"Higher rating ({comp['rating']}★ vs {product['rating']}★)"
                gap = "Customer satisfaction gap needs addressing"
            else:
                advantage = f"Comparable at ₹{comp.get('price', 'N/A')}"
                gap = "Monitor for differentiation opportunities"

            advantages.append(CompetitorAdvantage(
                competitor=f"{comp['brand']} ({comp['sku']})",
                advantage=advantage,
                impact="Market share pressure" if "lower" in advantage.lower() else "Brand perception",
                our_gap=gap,
            ))

        return advantages

    def _deep_competitor_analysis(self, product: Optional[dict],
                                   competitors: list[dict]) -> list[CompetitorAdvantage]:
        """Deep competitor analysis with feature gap matrix."""
        if not product:
            return []

        our_features = set(f.lower() for f in product.get("features", []))
        advantages = []

        feature_keywords = {
            "spf": "SPF protection/booster",
            "warranty": "Product warranty/guarantee",
            "money-back": "Money-back guarantee",
            "clinical study": "Clinical study documentation",
            "iso": "ISO certification",
            "organic": "Organic certification",
            "eco": "Eco-friendly packaging",
            "gradual release": "Gradual release technology",
            "aquaporin": "Advanced hydration technology",
            "subscription": "Subscription model",
            "loyalty": "Loyalty program",
        }

        for comp in competitors:
            comp_text = comp.get("features_text", "").lower()

            for keyword, feature_name in feature_keywords.items():
                if keyword in comp_text and not any(keyword in f for f in our_features):
                    advantages.append(CompetitorAdvantage(
                        competitor=f"{comp['brand']} ({comp['sku']})",
                        advantage=f"Offers {feature_name}",
                        impact=f"Differentiation advantage in {feature_name.lower()}",
                        our_gap=f"GlowSkin lacks {feature_name.lower()} — consider adding",
                    ))

            if comp.get("price", 9999) < product["price"] * 0.9:
                advantages.append(CompetitorAdvantage(
                    competitor=f"{comp['brand']} ({comp['sku']})",
                    advantage=f"Significantly lower price (₹{comp['price']} vs ₹{product['price']})",
                    impact=f"Captures price-sensitive segment ({((product['price'] - comp['price']) / product['price'] * 100):.0f}% cheaper)",
                    our_gap="Need value-tier SKU or enhanced value proposition to justify premium",
                ))

        return advantages

    def _generate_recommendations(
        self, goal, product, reviews, sentiment, competitor_gaps, pricing, sales_trend,
    ) -> list[StrategicRecommendation]:
        """Generate strategic recommendations based on all analysis dimensions."""
        recs = []

        neg_cluster = next((s for s in sentiment if s.label == "Negative"), None)
        if neg_cluster and neg_cluster.percentage > 15:
            recs.append(StrategicRecommendation(
                action=f"Address negative sentiment ({neg_cluster.percentage:.0f}% of reviews). "
                       f"Top concern: {neg_cluster.sample_reviews[0][:80] if neg_cluster.sample_reviews else 'Quality issues'}",
                priority="high",
                expected_impact=f"Reducing negative reviews by 50% could improve rating by ~0.3★",
                confidence="medium",
            ))

        if sales_trend and "declining" in sales_trend.trend.lower():
            recs.append(StrategicRecommendation(
                action="Investigate declining sales trend — review pricing, inventory, and ad spend",
                priority="high",
                expected_impact="Arrest decline could recover ₹1-3L monthly revenue",
                confidence="medium",
            ))

        for gap in competitor_gaps[:2]:
            recs.append(StrategicRecommendation(
                action=f"Close gap vs {gap.competitor}: {gap.our_gap}",
                priority="medium",
                expected_impact=f"Address {gap.advantage.lower()} competitive disadvantage",
                confidence="medium",
            ))

        if pricing and pricing.recommendation:
            recs.append(StrategicRecommendation(
                action=pricing.recommendation,
                priority="medium" if "maintain" in pricing.recommendation.lower() else "high",
                expected_impact="Optimize price-volume tradeoff",
                confidence="medium",
            ))

        if goal == BusinessGoal.MARGIN or goal == BusinessGoal.PROFITABILITY:
            recs.append(StrategicRecommendation(
                action="Focus on reducing return rate — each 1% reduction saves ~₹50K/quarter",
                priority="medium",
                expected_impact="Direct margin improvement through reduced reverse logistics",
                confidence="high",
            ))
        elif goal == BusinessGoal.GROWTH:
            recs.append(StrategicRecommendation(
                action="Increase review velocity — implement post-purchase follow-up campaign",
                priority="medium",
                expected_impact="Higher review count improves organic ranking and conversion by 8-12%",
                confidence="medium",
            ))

        return recs

    def _compute_confidence(self, reviews: list[dict], product: Optional[dict]) -> ConfidenceLevel:
        """Compute overall analysis confidence."""
        score = 0

        if len(reviews) >= 20:
            score += 3
        elif len(reviews) >= 10:
            score += 2
        else:
            score += 1

        if product and product.get("sales_data"):
            score += 2
        else:
            score += 1

        if reviews:
            ratings = [r.get("rating", 3) for r in reviews]
            avg = sum(ratings) / len(ratings)
            if product and abs(avg - product.get("rating", 0)) < 0.5:
                score += 2
            else:
                score += 1

        if score >= 6:
            return ConfidenceLevel.HIGH
        elif score >= 4:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW

    def _error_response(self, session_id: str, mode: ResearchMode,
                        query: str, message: str) -> ResearchResponse:
        """Generate graceful error response."""
        return ResearchResponse(
            session_id=session_id,
            mode=mode,
            query=query,
            analysis=StructuredAnalysis(executive_summary=f"⚠️ {message}"),
            data_gaps=[message],
        )


# Singleton
reasoning_engine = ReasoningEngine()
