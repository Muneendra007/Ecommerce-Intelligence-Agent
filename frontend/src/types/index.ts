// API Types matching backend schemas

export type ResearchMode = 'quick' | 'deep';
export type BusinessGoal = 'growth' | 'retention' | 'profitability' | 'margin' | 'revenue';
export type ConfidenceLevel = 'high' | 'medium' | 'low';

export interface SalesData {
    month: string;
    units_sold: number;
    revenue: number;
    returns: number;
}

export interface Product {
    sku: string;
    name: string;
    brand: string;
    price: number;
    rating: number;
    marketplace: string;
    category: string;
    features: string[];
    sales_data: SalesData[];
}

export interface SentimentCluster {
    label: string;
    percentage: number;
    sample_reviews: string[];
    review_count: number;
}

export interface CompetitorAdvantage {
    competitor: string;
    advantage: string;
    impact: string;
    our_gap: string;
}

export interface PricingAnalysis {
    our_price: number;
    competitor_prices: Record<string, number>;
    price_position: string;
    recommendation: string;
}

export interface SalesTrendInsight {
    trend: string;
    data_points: Array<{ month: string; units?: number; units_sold?: number; revenue: number; returns: number }>;
    analysis: string;
}

export interface StrategicRecommendation {
    action: string;
    priority: string;
    expected_impact: string;
    confidence: string;
}

export interface CostReport {
    input_tokens: number;
    output_tokens: number;
    total_tokens: number;
    estimated_cost_usd: number;
}

export interface ClarifyingQuestion {
    question: string;
    options: string[];
    context: string;
}

export interface StructuredAnalysis {
    executive_summary: string;
    sentiment_breakdown: SentimentCluster[];
    competitor_advantages: CompetitorAdvantage[];
    pricing_analysis: PricingAnalysis | null;
    sales_trend: SalesTrendInsight | null;
    recommendations: StrategicRecommendation[];
    confidence_score: ConfidenceLevel;
    cost: CostReport;
}

export interface ResearchResponse {
    session_id: string;
    mode: ResearchMode;
    query: string;
    sku: string | null;
    detected_goal?: string;
    analysis: StructuredAnalysis;
    clarifying_questions: ClarifyingQuestion[];
    data_gaps: string[];
    raw_response: string;
    timestamp: string;
}

export interface HealthResponse {
    status: string;
    openai_configured: boolean;
    qdrant_status: string;
    demo_mode: boolean;
    total_reviews_indexed: number;
    version: string;
}

export interface SKUListResponse {
    skus: Product[];
    brand: string;
}
