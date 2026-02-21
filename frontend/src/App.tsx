import { useState, useEffect } from 'react';
import './App.css';
import { QueryInput } from './components/QueryInput';
import { ResultsPanel } from './components/ResultsPanel';
import { MemoryPanel } from './components/MemoryPanel';
import { FollowUp } from './components/FollowUp';
import { ClarifyingQuestions } from './components/ClarifyingQuestions';
import { fetchHealth, fetchSKUs, submitResearch, submitFollowUp } from './services/api';
import type { ResearchResponse, Product, HealthResponse, ResearchMode, BusinessGoal } from './types';

function App() {
    const [health, setHealth] = useState<HealthResponse | null>(null);
    const [skus, setSkus] = useState<Product[]>([]);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<ResearchResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

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
            setError(e instanceof Error ? e.message : 'Research request failed');
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
        // Re-submit with more context
        if (result) {
            const enrichedQuery = `${result.query} (${answer})`;
            handleResearch(enrichedQuery, result.mode, 'growth', result.sku);
        }
    };

    return (
        <div className="app">
            {/* Header */}
            <header className="app-header">
                <div className="header-content">
                    <div className="brand">
                        <span className="brand-icon">🧪</span>
                        <h1>GlowSkin Intelligence</h1>
                        <span className="version-badge">v2.0</span>
                    </div>
                    <div className="header-status">
                        {health && (
                            <>
                                <span className={`status-dot ${health.status === 'ok' ? 'active' : 'inactive'}`} />
                                <span className="status-text">
                                    {health.demo_mode ? 'Demo Mode' : 'Live'} • {health.total_reviews_indexed} reviews indexed
                                </span>
                            </>
                        )}
                    </div>
                </div>
            </header>

            <main className="app-main">
                {/* Sidebar */}
                <aside className="sidebar">
                    <MemoryPanel skus={skus} health={health} />
                </aside>

                {/* Main Content */}
                <section className="content">
                    <QueryInput
                        onSubmit={handleResearch}
                        loading={loading}
                        skus={skus}
                    />

                    {/* Loading State */}
                    {loading && (
                        <div className="loading-panel">
                            <div className="loading-spinner" />
                            <p className="loading-text">Analyzing marketplace data...</p>
                            <p className="loading-sub">Retrieving reviews • Computing sentiment • Mapping competitors</p>
                        </div>
                    )}

                    {/* Error */}
                    {error && (
                        <div className="error-panel">
                            <span className="error-icon">⚠️</span>
                            <p>{error}</p>
                        </div>
                    )}

                    {/* Clarifying Questions */}
                    {result?.clarifying_questions && result.clarifying_questions.length > 0 && (
                        <ClarifyingQuestions
                            questions={result.clarifying_questions}
                            onAnswer={handleClarificationAnswer}
                        />
                    )}

                    {/* Results */}
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
                </section>
            </main>
        </div>
    );
}

export default App;
