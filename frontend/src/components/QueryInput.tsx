import { useState } from 'react';
import type { Product, ResearchMode, BusinessGoal } from '../types';

interface Props {
    onSubmit: (query: string, mode: ResearchMode, goal: BusinessGoal, sku: string | null) => void;
    loading: boolean;
    skus: Product[];
    initialQuery?: string;
    initialSku?: string;
}

const STARTER_QUERIES = [
    { label: '🔥 Retinol Returns', text: 'Why are customers returning the Retinol Night Cream (RET50)?' },
    { label: '💰 Vit-C vs DermaCare', text: 'Compare our Vitamin C serum pricing and formula against DermaCare.' },
    { label: '📈 Sunscreen Expansion', text: 'How can we scale Matte Sunscreen (SUN50) sales on Blinkit and Amazon?' },
    { label: '🧪 Salicylic Complaints', text: 'What are the top complaint themes for Salicylic Cleanser (SALI100)?' },
    { label: '💎 Margin Strategy', text: 'How can we increase profitability across our top 3 skincare SKUs?' },
];

export function QueryInput({ onSubmit, loading, skus, initialQuery = '', initialSku = '' }: Props) {
    const [query, setQuery] = useState(initialQuery);
    const [mode, setMode] = useState<ResearchMode>('quick');
    const [goal, setGoal] = useState<BusinessGoal>('growth');
    const [sku, setSku] = useState<string>(initialSku);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;
        onSubmit(query.trim(), mode, goal, sku || null);
    };

    return (
        <div className="query-panel glass-card">
            <form onSubmit={handleSubmit}>
                {/* Control Ribbon */}
                <div className="controls-row">
                    {/* Mode Segmented Switch */}
                    <div className="control-item">
                        <label>Analysis Depth</label>
                        <div className="mode-segmented">
                            <button
                                type="button"
                                className={`mode-btn ${mode === 'quick' ? 'active' : ''}`}
                                onClick={() => setMode('quick')}
                            >
                                <span>⚡ Quick</span>
                                <span className="mode-badge-meta">&lt;3s</span>
                            </button>
                            <button
                                type="button"
                                className={`mode-btn ${mode === 'deep' ? 'active' : ''}`}
                                onClick={() => setMode('deep')}
                            >
                                <span>🔬 Deep</span>
                                <span className="mode-badge-meta">Full</span>
                            </button>
                        </div>
                    </div>

                    {/* SKU Selector */}
                    <div className="control-item">
                        <label>Focus Product (Optional)</label>
                        <select
                            value={sku}
                            onChange={e => setSku(e.target.value)}
                            className="modern-select"
                        >
                            <option value="">🌐 All Products (Brand Overview)</option>
                            {skus.map(s => (
                                <option key={s.sku} value={s.sku}>
                                    {s.sku} — {s.name.replace('GlowSkin ', '')} (₹{s.price})
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Goal Selector */}
                    <div className="control-item">
                        <label>Strategic Objective</label>
                        <select
                            value={goal}
                            onChange={e => setGoal(e.target.value as BusinessGoal)}
                            className="modern-select"
                        >
                            <option value="growth">📈 Market Growth & Acquisition</option>
                            <option value="retention">🔄 Customer Retention & Satisfaction</option>
                            <option value="margin">💰 Margin Optimization</option>
                            <option value="revenue">💵 Gross Revenue Expansion</option>
                            <option value="profitability">📊 Unit Economics & Profitability</option>
                        </select>
                    </div>
                </div>

                {/* Main Command Bar */}
                <div className="query-search-bar">
                    <input
                        type="text"
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        placeholder="Ask anything (e.g. 'Why is Vitamin C underperforming vs DermaCare?', 'Analyze customer complaints for SUN50')..."
                        className="query-search-input"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading || !query.trim()}
                        className="query-action-btn"
                    >
                        {loading ? (
                            <><span>⏳</span> Analyzing...</>
                        ) : (
                            <><span>🚀</span> Execute AI Query</>
                        )}
                    </button>
                </div>
            </form>

            {/* Quick Starter Chips */}
            <div className="prompt-chips-wrapper">
                <span className="prompt-chips-label">Quick Prompts:</span>
                {STARTER_QUERIES.map(item => (
                    <button
                        key={item.label}
                        type="button"
                        className="prompt-chip"
                        onClick={() => setQuery(item.text)}
                    >
                        {item.label}
                    </button>
                ))}
            </div>
        </div>
    );
}
