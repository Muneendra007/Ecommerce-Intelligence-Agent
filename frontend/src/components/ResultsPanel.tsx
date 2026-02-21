import { Typewriter } from './Typewriter';
import type { ResearchResponse } from '../types';

interface Props {
    result: ResearchResponse;
}

export function ResultsPanel({ result }: Props) {
    const { analysis, mode, data_gaps } = result;

    const confidenceColor = {
        high: '#22c55e',
        medium: '#f59e0b',
        low: '#ef4444',
    }[analysis.confidence_score] || '#888';

    return (
        <div className="results-panel">
            {/* Header Bar */}
            <div className="results-header">
                <div className="results-meta">
                    <span className="mode-badge">{mode === 'quick' ? '⚡ Quick' : '🔬 Deep'} Analysis</span>
                    <span className="confidence-badge" style={{ borderColor: confidenceColor, color: confidenceColor }}>
                        Confidence: {analysis.confidence_score.toUpperCase()}
                    </span>
                </div>
                {analysis.cost && (
                    <span className="cost-badge">
                        💰 {analysis.cost.total_tokens} tokens • ${analysis.cost.estimated_cost_usd.toFixed(4)}
                    </span>
                )}
            </div>

            {/* Executive Summary */}
            <div className="section glass-card summary-card">
                <h3>📋 Executive Summary</h3>
                <Typewriter text={analysis.executive_summary} speed={30} />
            </div>

            {/* Sentiment Breakdown */}
            {analysis.sentiment_breakdown.length > 0 && (
                <div className="section glass-card">
                    <h3>💬 Sentiment Breakdown</h3>
                    <div className="sentiment-grid">
                        {analysis.sentiment_breakdown.slice(0, 3).map(cluster => (
                            <div key={cluster.label} className={`sentiment-card sentiment-${cluster.label.toLowerCase()}`}>
                                <div className="sentiment-header">
                                    <span className="sentiment-label">{cluster.label}</span>
                                    <span className="sentiment-pct">{cluster.percentage.toFixed(1)}%</span>
                                </div>
                                <div className="sentiment-bar">
                                    <div
                                        className="sentiment-fill"
                                        style={{ width: `${Math.min(cluster.percentage, 100)}%` }}
                                    />
                                </div>
                                <span className="sentiment-count">{cluster.review_count} reviews</span>
                                {cluster.sample_reviews.length > 0 && (
                                    <div className="sample-reviews">
                                        {cluster.sample_reviews.slice(0, 2).map((rev, i) => (
                                            <p key={i} className="sample-review">"{rev.slice(0, 100)}..."</p>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Competitor Advantages */}
            {analysis.competitor_advantages.length > 0 && (
                <div className="section glass-card">
                    <h3>🏆 Competitor Advantage Mapping</h3>
                    <div className="competitor-grid">
                        {analysis.competitor_advantages.map((comp, i) => (
                            <div key={i} className="competitor-card">
                                <div className="comp-header">{comp.competitor}</div>
                                <div className="comp-field">
                                    <span className="field-label">Advantage:</span>
                                    <span>{comp.advantage}</span>
                                </div>
                                <div className="comp-field">
                                    <span className="field-label">Impact:</span>
                                    <span>{comp.impact}</span>
                                </div>
                                <div className="comp-field gap-field">
                                    <span className="field-label">Our Gap:</span>
                                    <span>{comp.our_gap}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Pricing Analysis */}
            {analysis.pricing_analysis && (
                <div className="section glass-card">
                    <h3>💲 Pricing Analysis</h3>
                    <div className="pricing-content">
                        <div className="pricing-main">
                            <div className="price-tag">₹{analysis.pricing_analysis.our_price}</div>
                            <p className="price-position">{analysis.pricing_analysis.price_position}</p>
                            <p className="price-rec">💡 {analysis.pricing_analysis.recommendation}</p>
                        </div>
                        {Object.keys(analysis.pricing_analysis.competitor_prices).length > 0 && (
                            <div className="competitor-prices">
                                <h4>Competitor Prices</h4>
                                {Object.entries(analysis.pricing_analysis.competitor_prices).map(([name, price]) => (
                                    <div key={name} className="comp-price-row">
                                        <span>{name}</span>
                                        <span className="comp-price">₹{price}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Sales Trend */}
            {analysis.sales_trend && (
                <div className="section glass-card">
                    <h3>📈 Sales Trend Insight</h3>
                    <div className="trend-content">
                        <div className={`trend-badge ${analysis.sales_trend.trend.toLowerCase().includes('declining') ? 'trend-down' : analysis.sales_trend.trend.toLowerCase().includes('growing') ? 'trend-up' : 'trend-stable'}`}>
                            {analysis.sales_trend.trend}
                        </div>
                        <p className="trend-analysis">{analysis.sales_trend.analysis}</p>
                        {analysis.sales_trend.data_points.length > 0 && (
                            <div className="trend-table">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Month</th>
                                            <th>Units</th>
                                            <th>Revenue</th>
                                            <th>Returns</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {analysis.sales_trend.data_points.map(dp => (
                                            <tr key={dp.month}>
                                                <td>{dp.month}</td>
                                                <td>{dp.units.toLocaleString()}</td>
                                                <td>₹{dp.revenue.toLocaleString()}</td>
                                                <td>{dp.returns}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Strategic Recommendations */}
            {analysis.recommendations.length > 0 && (
                <div className="section glass-card">
                    <h3>🎯 Strategic Recommendations</h3>
                    <div className="rec-list">
                        {analysis.recommendations.map((rec, i) => (
                            <div key={i} className={`rec-card priority-${rec.priority}`}>
                                <div className="rec-header">
                                    <span className={`priority-badge priority-${rec.priority}`}>
                                        {rec.priority.toUpperCase()}
                                    </span>
                                    <span className="rec-confidence">Confidence: {rec.confidence}</span>
                                </div>
                                <p className="rec-action">{rec.action}</p>
                                {rec.expected_impact && (
                                    <p className="rec-impact">📊 Expected Impact: {rec.expected_impact}</p>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Data Gaps */}
            {data_gaps.length > 0 && (
                <div className="section glass-card data-gaps">
                    <h3>⚠️ Data Gaps & Caveats</h3>
                    <ul>
                        {data_gaps.map((gap, i) => (
                            <li key={i}>{gap}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}
