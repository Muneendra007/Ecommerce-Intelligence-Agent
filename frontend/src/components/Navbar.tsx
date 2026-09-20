import React from 'react';
import type { HealthResponse } from '../types';

export type ActiveTab = 'research' | 'radar' | 'catalog' | 'telemetry';

interface Props {
    activeTab: ActiveTab;
    setActiveTab: (tab: ActiveTab) => void;
    health: HealthResponse | null;
    totalTokens?: number;
    costUsd?: number;
}

export function Navbar({ activeTab, setActiveTab, health, totalTokens = 0, costUsd = 0 }: Props) {
    return (
        <header className="app-header">
            <div className="header-inner">
                {/* Brand */}
                <div className="brand-section">
                    <div className="brand-logo-icon">
                        <span>⚡</span>
                    </div>
                    <div>
                        <div className="brand-title">
                            GlowSkin AI <span className="brand-tag">v2.1 Command</span>
                        </div>
                    </div>
                </div>

                {/* Live Telemetry Pills */}
                <div className="telemetry-row">
                    <div className="telemetry-badge" title="Vector Database Status">
                        <span className={`status-indicator ${health?.qdrant_status === 'connected' ? 'active' : 'warning'}`} />
                        <span>
                            Qdrant: {health?.qdrant_status === 'connected' ? 'Cloud Connected' : 'In-Memory Fallback'}
                        </span>
                        {health?.total_reviews_indexed ? (
                            <span style={{ color: 'var(--cyan)' }}>({health.total_reviews_indexed.toLocaleString()} vectors)</span>
                        ) : null}
                    </div>

                    <div className="telemetry-badge" title="LLM Provider">
                        <span className="status-indicator active" />
                        <span>Groq AI (Qwen-27B)</span>
                    </div>

                    {totalTokens > 0 && (
                        <div className="telemetry-badge" style={{ borderColor: 'rgba(16, 185, 129, 0.3)' }}>
                            <span style={{ color: 'var(--emerald)' }}>
                                📊 {totalTokens.toLocaleString()} tokens (${costUsd.toFixed(4)})
                            </span>
                        </div>
                    )}
                </div>
            </div>

            {/* Navigation Tabs */}
            <div className="nav-tabs-wrapper" style={{ marginTop: '1.25rem', marginBottom: '0' }}>
                <nav className="nav-tabs">
                    <button
                        type="button"
                        className={`nav-tab-btn ${activeTab === 'research' ? 'active' : ''}`}
                        onClick={() => setActiveTab('research')}
                    >
                        <span>⚡</span> Research Studio
                    </button>

                    <button
                        type="button"
                        className={`nav-tab-btn ${activeTab === 'radar' ? 'active' : ''}`}
                        onClick={() => setActiveTab('radar')}
                    >
                        <span>📡</span> Competitor Radar
                    </button>

                    <button
                        type="button"
                        className={`nav-tab-btn ${activeTab === 'catalog' ? 'active' : ''}`}
                        onClick={() => setActiveTab('catalog')}
                    >
                        <span>📦</span> SKU Catalog & Sales
                    </button>

                    <button
                        type="button"
                        className={`nav-tab-btn ${activeTab === 'telemetry' ? 'active' : ''}`}
                        onClick={() => setActiveTab('telemetry')}
                    >
                        <span>🧠</span> System Telemetry
                    </button>
                </nav>
            </div>
        </header>
    );
}
