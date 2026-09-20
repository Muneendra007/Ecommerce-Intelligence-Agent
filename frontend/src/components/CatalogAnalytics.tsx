import React from 'react';
import type { Product } from '../types';

interface Props {
    skus: Product[];
    onDiagnoseSku: (sku: string, productName: string) => void;
}

export function CatalogAnalytics({ skus, onDiagnoseSku }: Props) {
    return (
        <div className="tab-pane">
            <div className="glass-card" style={{ padding: '2rem', marginBottom: '2rem' }}>
                <div style={{ marginBottom: '1.5rem' }}>
                    <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.5rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                        <span>📦</span> GlowSkin SKU Catalog & Sales Diagnostics
                    </h2>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', marginTop: '0.3rem' }}>
                        Multi-marketplace telemetry across Amazon, Nykaa, and Flipkart with 4-month sales performance, return rates, and 1-click AI deep dives.
                    </p>
                </div>

                <div className="catalog-grid">
                    {skus.map(p => {
                        const totalUnits = p.sales_data.reduce((acc, s) => acc + s.units_sold, 0);
                        const totalRevenue = p.sales_data.reduce((acc, s) => acc + s.revenue, 0);
                        const totalReturns = p.sales_data.reduce((acc, s) => acc + s.returns, 0);
                        const returnRate = totalUnits > 0 ? ((totalReturns / totalUnits) * 100).toFixed(1) : '0';
                        const returnWarning = parseFloat(returnRate) > 6.0;

                        return (
                            <div key={p.sku} className="sku-product-card">
                                <div className="sku-card-top">
                                    <div className="sku-header-row">
                                        <span className="sku-code-badge">{p.sku}</span>
                                        <span className="sku-rating-star">★ {p.rating}</span>
                                    </div>

                                    <h3 className="sku-name">{p.name}</h3>

                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', margin: '0.6rem 0' }}>
                                        <span className="sku-price-tag">₹{p.price}</span>
                                        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                                            {p.marketplace}
                                        </span>
                                    </div>

                                    {/* Feature Pills */}
                                    <div className="sku-features-pills">
                                        {p.features.slice(0, 3).map((f, i) => (
                                            <span key={i} className="feature-pill">{f}</span>
                                        ))}
                                    </div>

                                    {/* 4-Month Performance Mini-Table */}
                                    <div className="sku-sales-stats">
                                        <div className="stat-metric-cell">
                                            <span>4M Units</span>
                                            <span>{totalUnits.toLocaleString()}</span>
                                        </div>
                                        <div className="stat-metric-cell">
                                            <span>4M Revenue</span>
                                            <span style={{ color: 'var(--emerald)' }}>₹{(totalRevenue / 100000).toFixed(1)}L</span>
                                        </div>
                                        <div className="stat-metric-cell">
                                            <span>Returns</span>
                                            <span style={{ color: returnWarning ? 'var(--rose)' : 'var(--emerald)' }}>
                                                {returnRate}%
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                <button
                                    type="button"
                                    className="sku-diagnose-btn"
                                    onClick={() => onDiagnoseSku(p.sku, p.name)}
                                >
                                    <span>🧠</span> Run Deep Diagnosis on {p.sku}
                                </button>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
