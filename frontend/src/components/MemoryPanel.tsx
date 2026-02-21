import type { Product, HealthResponse } from '../types';

interface Props {
    skus: Product[];
    health: HealthResponse | null;
}

export function MemoryPanel({ skus, health }: Props) {
    return (
        <div className="memory-panel">
            {/* Brand Info */}
            <div className="sidebar-section glass-card">
                <h3>🧴 GlowSkin</h3>
                <p className="brand-desc">D2C Skincare Brand • Amazon Marketplace</p>
            </div>

            {/* Product Catalog */}
            <div className="sidebar-section glass-card">
                <h3>📦 Product Catalog</h3>
                <div className="sku-list">
                    {skus.map(p => (
                        <div key={p.sku} className="sku-card">
                            <div className="sku-header">
                                <span className="sku-code">{p.sku}</span>
                                <span className="sku-rating">{p.rating}★</span>
                            </div>
                            <p className="sku-name">{p.name.replace('GlowSkin ', '')}</p>
                            <span className="sku-price">₹{p.price}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* System Status */}
            <div className="sidebar-section glass-card">
                <h3>⚙️ System</h3>
                {health && (
                    <div className="status-list">
                        <div className="status-row">
                            <span>Vector Store</span>
                            <span className={`status-val ${health.qdrant_status === 'connected' ? 'ok' : 'fallback'}`}>
                                {health.qdrant_status}
                            </span>
                        </div>
                        <div className="status-row">
                            <span>Reviews Indexed</span>
                            <span className="status-val ok">{health.total_reviews_indexed}</span>
                        </div>
                        <div className="status-row">
                            <span>LLM</span>
                            <span className={`status-val ${health.demo_mode ? 'fallback' : 'ok'}`}>
                                {health.demo_mode ? 'Demo Mode' : 'Live'}
                            </span>
                        </div>
                        <div className="status-row">
                            <span>Version</span>
                            <span className="status-val">{health.version}</span>
                        </div>
                    </div>
                )}
            </div>

            {/* Capabilities */}
            <div className="sidebar-section glass-card">
                <h3>🧠 Capabilities</h3>
                <ul className="cap-list">
                    <li>Sentiment cluster detection</li>
                    <li>Competitor feature gap analysis</li>
                    <li>Pricing intelligence</li>
                    <li>Sales trend reasoning</li>
                    <li>Strategic recommendations</li>
                    <li>Memory & preference learning</li>
                </ul>
            </div>
        </div>
    );
}
