import { useState, useEffect } from 'react';
import './App.css';
import { Navbar, ActiveTab } from './components/Navbar';
import { QueryInput } from './components/QueryInput';
import { ResultsPanel } from './components/ResultsPanel';
import { MemoryPanel } from './components/MemoryPanel';
import { CompetitorRadar } from './components/CompetitorRadar';
import { CatalogAnalytics } from './components/CatalogAnalytics';
import { FollowUp } from './components/FollowUp';
import { ClarifyingQuestions } from './components/ClarifyingQuestions';
import { fetchHealth, fetchSKUs, submitResearch, submitFollowUp } from './services/api';
import type { ResearchResponse, Product, HealthResponse, ResearchMode, BusinessGoal } from './types';

function App() {
    const [activeTab, setActiveTab] = useState<ActiveTab>('research');
    const [health, setHealth] = useState<HealthResponse | null>(null);
    const [skus, setSkus] = useState<Product[]>([]);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<ResearchResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Initial pre-filled values when clicking from other tabs
    const [initialQuery, setInitialQuery] = useState('');
    const [initialSku, setInitialSku] = useState('');

    // Load health and SKUs on mount
    useEffect(() => {
        fetchHealth().then(setHealth).catch(console.error);
        fetchSKUs().then(data => setSkus(data.skus || [])).catch(console.error);
    }, []);

    const handleResearch = async (query: string, mode: ResearchMode, goal: BusinessGoal, sku: string | null) => {
        setLoading(true);
        setError(null);
        setResult(null);
        try {
            const res = await submitResearch({ query, mode, goal, sku });
            setResult(res);
        } catch (e: unknown) {
            setError(e instanceof Error ? e.message : 'Research request failed. Check server connection.');
        } finally {
            setLoading(false);
        }
    };

    const handleFollowUp = async (message: string) => {
        if (!result?.session_id) return;
        setLoading(true);
        try {
            const res = await submitFollowUp({ session_id: result.session_id, message });
            setResult(res);
        } catch (e: unknown) {
            setError(e instanceof Error ? e.message : 'Follow-up failed');
        } finally {
            setLoading(false);
        }
    };

    const handleClarificationAnswer = (question: string, answer: string) => {
        if (result) {
            const enrichedQuery = `${result.query} (${answer})`;
            handleResearch(enrichedQuery, result.mode, (result.detected_goal as BusinessGoal) || 'growth', result.sku);
        }
    };

    // Triggered from SKU Catalog tab
    const handleDiagnoseSku = (sku: string, productName: string) => {
        const queryText = `Perform full deep diagnostic on ${sku} (${productName}): investigate customer returns, complaints, and pricing vs competitors.`;
        setInitialQuery(queryText);
        setInitialSku(sku);
        setActiveTab('research');
        handleResearch(queryText, 'deep', 'retention', sku);
    };

    // Triggered from Competitor Radar tab
    const handleAnalyzeCompetitor = (queryText: string) => {
        setInitialQuery(queryText);
        setActiveTab('research');
        handleResearch(queryText, 'quick', 'growth', null);
    };

    const totalTokens = result?.analysis?.cost?.total_tokens || 0;
    const costUsd = result?.analysis?.cost?.estimated_cost_usd || 0;

    return (
        <div className="app-container">
            {/* Command Header with Telemetry & Navigation */}
            <Navbar
                activeTab={activeTab}
                setActiveTab={setActiveTab}
                health={health}
                totalTokens={totalTokens}
                costUsd={costUsd}
            />

            <main>
                {/* ── Tab 1: Research Studio ── */}
                {activeTab === 'research' && (
                    <div className="tab-pane">
                        <QueryInput
                            onSubmit={handleResearch}
                            loading={loading}
                            skus={skus}
                            initialQuery={initialQuery}
                            initialSku={initialSku}
                        />

                        {/* Loading Radar Animation */}
                        {loading && (
                            <div className="glass-card loading-card">
                                <div className="radar-spinner">
                                    <div className="radar-spinner-ring" />
                                    <div className="radar-spinner-ring" />
                                    <div className="radar-spinner-ring" />
                                </div>
                                <div className="loading-headline">AI Intelligence Agent at Work</div>
                                <div className="loading-steps-pills">
                                    <span>● Query Vectorization (384-dim)</span>
                                    <span>● Qdrant Cloud Semantic Search</span>
                                    <span>● Multi-Marketplace Synthesis</span>
                                    <span>● Groq AI Strategic Reasoning</span>
                                </div>
                            </div>
                        )}

                        {/* Error Notification */}
                        {error && (
                            <div className="glass-card" style={{ padding: '1.25rem 1.75rem', marginBottom: '1.5rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--rose)' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: 'var(--rose)', fontWeight: 600 }}>
                                    <span>⚠️</span> {error}
                                </div>
                            </div>
                        )}

                        {/* Clarifying Questions Prompt */}
                        {result?.clarifying_questions && result.clarifying_questions.length > 0 && (
                            <ClarifyingQuestions
                                questions={result.clarifying_questions}
                                onAnswer={handleClarificationAnswer}
                            />
                        )}

                        {/* Results Display */}
                        {result?.analysis?.executive_summary && (
                            <>
                                <ResultsPanel result={result} />
                                <FollowUp
                                    sessionId={result.session_id}
                                    onFollowUp={handleFollowUp}
                                    loading={loading}
                                />
                            </>
                        )}
                    </div>
                )}

                {/* ── Tab 2: Competitor Radar ── */}
                {activeTab === 'radar' && (
                    <CompetitorRadar onAnalyzeCompetitor={handleAnalyzeCompetitor} />
                )}

                {/* ── Tab 3: SKU Catalog & Sales Diagnostics ── */}
                {activeTab === 'catalog' && (
                    <CatalogAnalytics skus={skus} onDiagnoseSku={handleDiagnoseSku} />
                )}

                {/* ── Tab 4: System Telemetry & Memory ── */}
                {activeTab === 'telemetry' && (
                    <MemoryPanel skus={skus} health={health} />
                )}
            </main>
        </div>
    );
}

export default App;
