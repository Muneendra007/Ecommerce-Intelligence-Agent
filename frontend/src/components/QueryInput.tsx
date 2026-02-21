import { useState } from 'react';
import type { Product, ResearchMode, BusinessGoal } from '../types';

interface Props {
    onSubmit: (query: string, mode: ResearchMode, goal: BusinessGoal, sku: string | null) => void;
    loading: boolean;
    skus: Product[];
}

const EXAMPLE_QUERIES = [
    'Why is Vitamin C Serum underperforming?',
    'Top complaints for SKU VITC30',
    'What features do competitors offer that we don\'t?',
    'Based on margin optimization, what should we improve?',
];

export function QueryInput({ onSubmit, loading, skus }: Props) {
    const [query, setQuery] = useState('');
    const [mode, setMode] = useState<ResearchMode>('quick');
    const [goal, setGoal] = useState<BusinessGoal>('growth');
    const [sku, setSku] = useState<string>('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;
        onSubmit(query.trim(), mode, goal, sku || null);
    };

    return (
        <div className="query-panel glass-card">
            <h2 className="panel-title">🔍 Research Query</h2>

            <form onSubmit={handleSubmit}>
                {/* Controls Row */}
                <div className="controls-row">
                    <div className="control-group">
                        <label>Mode</label>
                        <div className="mode-toggle">
                            <button
                                type="button"
                                className={`toggle-btn ${mode === 'quick' ? 'active' : ''}`}
                                onClick={() => setMode('quick')}
                            >
                                ⚡ Quick
                            </button>
                            <button
                                type="button"
                                className={`toggle-btn ${mode === 'deep' ? 'active' : ''}`}
                                onClick={() => setMode('deep')}
                            >
                                🔬 Deep
                            </button>
                        </div>
                    </div>

                    <div className="control-group">
                        <label>SKU</label>
                        <select value={sku} onChange={e => setSku(e.target.value)} className="select-input">
                            <option value="">All SKUs</option>
                            {skus.map(s => (
                                <option key={s.sku} value={s.sku}>
                                    {s.sku} — {s.name.replace('GlowSkin ', '')} (₹{s.price})
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="control-group">
                        <label>Goal</label>
                        <select value={goal} onChange={e => setGoal(e.target.value as BusinessGoal)} className="select-input">
                            <option value="growth">📈 Growth</option>
                            <option value="margin">💰 Margin</option>
                            <option value="revenue">💵 Revenue</option>
                            <option value="retention">🔄 Retention</option>
                            <option value="profitability">📊 Profitability</option>
                        </select>
                    </div>
                </div>

                {/* Query Input */}
                <div className="query-input-row">
                    <input
                        type="text"
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        placeholder="Ask a business question about GlowSkin products..."
                        className="query-input"
                        disabled={loading}
                    />
                    <button type="submit" disabled={loading || !query.trim()} className="submit-btn">
                        {loading ? '⏳' : '🚀'} Research
                    </button>
                </div>
            </form>

            {/* Example Queries */}
            <div className="example-queries">
                <span className="example-label">Try:</span>
                {EXAMPLE_QUERIES.map(eq => (
                    <button
                        key={eq}
                        className="example-chip"
                        onClick={() => setQuery(eq)}
                    >
                        {eq}
                    </button>
                ))}
            </div>
        </div>
    );
}
