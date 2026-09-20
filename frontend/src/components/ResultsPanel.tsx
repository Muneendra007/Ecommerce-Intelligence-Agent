import { Typewriter } from './Typewriter';
import type { ResearchResponse } from '../types';

interface Props {
    result: ResearchResponse;
}

export function ResultsPanel({ result }: Props) {
    const { analysis, mode } = result;

    const confidenceStyle = {
        high: { color: 'var(--emerald)', bg: 'var(--emerald-bg)', border: 'rgba(16, 185, 129, 0.4)' },
        medium: { color: 'var(--amber)', bg: 'var(--amber-bg)', border: 'rgba(245, 158, 11, 0.4)' },
        low: { color: 'var(--rose)', bg: 'var(--rose-bg)', border: 'rgba(244, 63, 94, 0.4)' },
    }[analysis.confidence_score] || { color: 'var(--text-secondary)', bg: 'rgba(255,255,255,0.05)', border: 'var(--border-subtle)' };

    return (
        <div className="results-grid tab-pane">
            {/* Meta Control Strip */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                    <span style={{
                        padding: '0.35rem 0.85rem',
                        background: 'rgba(99, 102, 241, 0.15)',
                        border: '1px solid rgba(99, 102, 241, 0.4)',
                        borderRadius: 'var(--radius-pill)',
                        fontSize: '0.82rem',
                        fontWeight: 600,
                        color: 'var(--text-accent)',
                        fontFamily: 'var(--font-mono)',
                    }}>
                        {mode === 'quick' ? '⚡ Quick Intelligence' : '🔬 Deep Multi-Dimensional Diagnosis'}
                    </span>

                    <span style={{
                        padding: '0.35rem 0.85rem',
                        background: confidenceStyle.bg,
                        border: `1px solid ${confidenceStyle.border}`,
                        borderRadius: 'var(--radius-pill)',
                        fontSize: '0.82rem',
                        fontWeight: 600,
                        color: confidenceStyle.color,
                        fontFamily: 'var(--font-mono)',
                    }}>
                        Confidence: {analysis.confidence_score.toUpperCase()}
                    </span>
                </div>

                {analysis.cost && (
                    <div style={{
                        padding: '0.35rem 0.85rem',
                        background: 'rgba(16, 185, 129, 0.08)',
                        border: '1px solid rgba(16, 185, 129, 0.25)',
                        borderRadius: 'var(--radius-pill)',
                        fontSize: '0.8rem',
                        fontFamily: 'var(--font-mono)',
                        color: 'var(--emerald)',
                    }}>
                        💰 {analysis.cost.total_tokens.toLocaleString()} tokens • ${analysis.cost.estimated_cost_usd.toFixed(5)}
                    </div>
                )}
            </div>

            {/* 1. Executive Summary Hero Card */}
            <div className="glass-card summary-hero-card">
                <div className="summary-meta-header">
                    <div className="summary-title-badge">
                        <span>📋</span> Executive Intelligence Summary
                    </div>
                    {result.detected_goal && (
                        <span style={{
                            fontSize: '0.75rem',
                            fontFamily: 'var(--font-mono)',
                            textTransform: 'uppercase',
                            color: 'var(--text-muted)',
                            background: 'rgba(255, 255, 255, 0.05)',
                            padding: '0.2rem 0.6rem',
                            borderRadius: 'var(--radius-sm)',
                        }}>
                            Goal: {result.detected_goal}
                        </span>
                    )}
                </div>
                <div className="summary-text-body">
                    <Typewriter text={analysis.executive_summary} speed={25} />
                </div>
            </div>

            {/* 2. Sentiment Breakdown */}
            {analysis.sentiment_breakdown.length > 0 && (
                <div className="glass-card" style={{ padding: '1.75rem' }}>
                    <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                        <span>💬</span> Customer Sentiment Clusters & Voice of Customer
                    </h3>
                    <div className="sentiment-matrix">
                        {analysis.sentiment_breakdown.map((cluster, i) => {
                            const isPositive = cluster.label.toLowerCase().includes('positive') || cluster.label.toLowerCase().includes('5');
                            const isNegative = cluster.label.toLowerCase().includes('negative') || cluster.label.toLowerCase().includes('1') || cluster.label.toLowerCase().includes('2');
                            const clusterType = isPositive ? 'positive' : isNegative ? 'negative' : 'insight';

                            return (
                                <div key={i} className="sentiment-cluster-card">
                                    <div className="cluster-header">
                                        <span className={`cluster-tag ${clusterType}`}>
                                            {cluster.label}
                                        </span>
                                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.95rem', fontWeight: 700, color: '#fff' }}>
                                            {cluster.percentage > 0 ? `${cluster.percentage.toFixed(1)}%` : `${cluster.review_count} revs`}
                                        </span>
                                    </div>

                                    {cluster.percentage > 0 && (
                                        <div className="cluster-bar-bg">
                                            <div
                                                className={`cluster-bar-fill ${clusterType}`}
                                                style={{ width: `${Math.min(cluster.percentage, 100)}%` }}
                                            />
                                        </div>
                                    )}

                                    {cluster.sample_reviews && cluster.sample_reviews.length > 0 && (
                                        <div style={{ marginTop: '0.6rem' }}>
                                            {cluster.sample_reviews.slice(0, 2).map((rev, rIdx) => (
                                                <p key={rIdx} className="cluster-quote">
                                                    "{rev.length > 130 ? `${rev.slice(0, 130)}...` : rev}"
                                                </p>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* 3. Strategic Recommendations */}
            {analysis.recommendations.length > 0 && (
                <div className="glass-card" style={{ padding: '1.75rem' }}>
                    <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                        <span>🎯</span> Prioritized Strategic Action Plan
                    </h3>
                    <div className="recommendations-list">
                        {analysis.recommendations.map((rec, i) => (
                            <div key={i} className="recommendation-card">
                                <span className={`priority-chip ${rec.priority.toLowerCase()}`}>
                                    {rec.priority} Priority
                                </span>
                                <div className="rec-content-box">
                                    <div className="rec-action-text">{rec.action}</div>
                                    {rec.expected_impact && (
                                        <div className="rec-impact-text">
                                            <span style={{ color: 'var(--cyan)' }}>Impact: </span>
                                            {rec.expected_impact}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* 4. Competitor Advantages Mapping */}
            {analysis.competitor_advantages.length > 0 && (
                <div className="glass-card" style={{ padding: '1.75rem' }}>
                    <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                        <span>🏆</span> Competitor Advantage & Vulnerability Mapping
                    </h3>
                    <div className="competitor-battle-grid">
                        {analysis.competitor_advantages.map((comp, i) => (
                            <div key={i} className="competitor-card">
                                <div className="competitor-card-title">{comp.competitor}</div>
                                <div className="competitor-kv">
                                    <span>Advantage</span>
                                    <span style={{ color: '#fff' }}>{comp.advantage}</span>
                                </div>
                                <div className="competitor-kv">
                                    <span>Market Impact</span>
                                    <span style={{ color: 'var(--text-secondary)' }}>{comp.impact}</span>
                                </div>
                                <div className="competitor-gap-highlight">
                                    <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
                                        Our Gap & Required Action
                                    </div>
                                    <div style={{ fontSize: '0.88rem', color: '#fff', marginTop: '0.2rem' }}>
                                        {comp.our_gap}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* 5. Pricing Analysis */}
            {analysis.pricing_analysis && (
                <div className="glass-card" style={{ padding: '1.75rem' }}>
                    <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', fontWeight: 600, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                        <span>💲</span> Price Elasticity & Positioning Analysis
                    </h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', alignItems: 'center' }}>
                        <div style={{ padding: '1.25rem', background: 'rgba(8, 12, 26, 0.6)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
                            <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', textTransform: 'uppercase', color: 'var(--text-muted)' }}>GlowSkin Price</div>
                            <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--emerald)', fontFamily: 'var(--font-mono)', margin: '0.3rem 0' }}>
                                ₹{analysis.pricing_analysis.our_price}
                            </div>
                            <div style={{ fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
                                {analysis.pricing_analysis.price_position}
                            </div>
                            {analysis.pricing_analysis.recommendation && (
                                <div style={{ marginTop: '0.8rem', padding: '0.6rem', background: 'rgba(139, 92, 246, 0.1)', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(139, 92, 246, 0.25)', fontSize: '0.85rem', color: '#fff' }}>
                                    💡 {analysis.pricing_analysis.recommendation}
                                </div>
                            )}
                        </div>

                        {Object.keys(analysis.pricing_analysis.competitor_prices).length > 0 && (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                                <div style={{ fontSize: '0.78rem', fontFamily: 'var(--font-mono)', textTransform: 'uppercase', color: 'var(--text-muted)' }}>Market Competitor Comparison</div>
                                {Object.entries(analysis.pricing_analysis.competitor_prices).map(([comp, price]) => (
                                    <div key={comp} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.6rem 0.9rem', background: 'rgba(15, 23, 42, 0.5)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
                                        <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>{comp}</span>
                                        <span style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff', fontFamily: 'var(--font-mono)' }}>₹{price}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* 6. Sales Trend Insights */}
            {analysis.sales_trend && (
                <div className="glass-card" style={{ padding: '1.75rem' }}>
                    <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', fontWeight: 600, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                        <span>📈</span> 4-Month Multi-Marketplace Sales Trend
                    </h3>
                    <div style={{ display: 'inline-block', padding: '0.35rem 0.85rem', background: 'rgba(99, 102, 241, 0.15)', borderRadius: 'var(--radius-pill)', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-accent)', marginBottom: '0.8rem' }}>
                        Trend: {analysis.sales_trend.trend}
                    </div>
                    <p style={{ color: '#cbd5e1', lineHeight: 1.6, fontSize: '0.95rem', marginBottom: '1.2rem' }}>
                        {analysis.sales_trend.analysis}
                    </p>

                    {analysis.sales_trend.data_points.length > 0 && (
                        <div style={{ overflowX: 'auto' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem' }}>
                                <thead>
                                    <tr style={{ borderBottom: '1px solid var(--border-subtle)', textAlign: 'left', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                                        <th style={{ padding: '0.6rem' }}>Month</th>
                                        <th style={{ padding: '0.6rem' }}>Units Sold</th>
                                        <th style={{ padding: '0.6rem' }}>Revenue (₹)</th>
                                        <th style={{ padding: '0.6rem' }}>Returns</th>
                                        <th style={{ padding: '0.6rem' }}>Return Rate</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {analysis.sales_trend.data_points.map((dp, idx) => {
                                        const units = dp.units_sold ?? dp.units ?? 0;
                                        const returnRate = units > 0 ? ((dp.returns / units) * 100).toFixed(1) : '0.0';
                                        return (
                                            <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                                                <td style={{ padding: '0.6rem', fontFamily: 'var(--font-mono)', color: 'var(--text-primary)' }}>{dp.month}</td>
                                                <td style={{ padding: '0.6rem', fontFamily: 'var(--font-mono)' }}>{units.toLocaleString()}</td>
                                                <td style={{ padding: '0.6rem', fontFamily: 'var(--font-mono)', color: 'var(--emerald)' }}>₹{dp.revenue.toLocaleString()}</td>
                                                <td style={{ padding: '0.6rem', fontFamily: 'var(--font-mono)', color: 'var(--rose)' }}>{dp.returns}</td>
                                                <td style={{ padding: '0.6rem', fontFamily: 'var(--font-mono)', color: parseFloat(returnRate) > 6 ? 'var(--rose)' : 'var(--emerald)' }}>
                                                    {returnRate}%
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
