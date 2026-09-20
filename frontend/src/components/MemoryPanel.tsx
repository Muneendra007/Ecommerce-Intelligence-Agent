import { useState, useEffect } from 'react';
import type { HealthResponse, Product } from '../types';
import { fetchMemory, storeMemory } from '../services/api';

interface Props {
    skus: Product[];
    health: HealthResponse | null;
}

export function MemoryPanel({ skus, health }: Props) {
    const [memory, setMemory] = useState<Record<string, string>>({});
    const [newKey, setNewKey] = useState('');
    const [newVal, setNewVal] = useState('');
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        fetchMemory().then(res => setMemory(res.preferences || {})).catch(console.error);
    }, []);

    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newKey.trim() || !newVal.trim()) return;
        setSaving(true);
        try {
            await storeMemory(newKey.trim(), newVal.trim());
            setMemory(prev => ({ ...prev, [newKey.trim()]: newVal.trim() }));
            setNewKey('');
            setNewVal('');
        } catch (err) {
            console.error(err);
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="tab-pane">
            <div className="telemetry-dashboard">
                {/* 1. Vector Database Telemetry */}
                <div className="glass-card telemetry-card">
                    <h3><span>⚡</span> Vector Engine (Qdrant Cloud)</h3>
                    <div className="telemetry-list">
                        <div className="telemetry-item">
                            <span className="telemetry-key">Cluster Status</span>
                            <span className="telemetry-val" style={{ color: 'var(--emerald)' }}>
                                {health?.qdrant_status === 'connected' ? '● Live Connected' : '○ In-Memory Fallback'}
                            </span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">Collections</span>
                            <span className="telemetry-val">reviews, competitor_features, user_memory</span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">Total Indexed Vectors</span>
                            <span className="telemetry-val" style={{ color: 'var(--cyan)' }}>
                                {health?.total_reviews_indexed ? health.total_reviews_indexed.toLocaleString() : '2,867'}
                            </span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">Embedding Model</span>
                            <span className="telemetry-val">all-MiniLM-L6-v2 (384-dim)</span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">Distance Metric</span>
                            <span className="telemetry-val">Cosine Similarity</span>
                        </div>
                    </div>
                </div>

                {/* 2. LLM Engine Telemetry */}
                <div className="glass-card telemetry-card">
                    <h3><span>🧠</span> Inference Engine (Groq AI)</h3>
                    <div className="telemetry-list">
                        <div className="telemetry-item">
                            <span className="telemetry-key">Active Provider</span>
                            <span className="telemetry-val" style={{ color: 'var(--accent-primary)' }}>Groq LPU Cloud</span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">Production Model</span>
                            <span className="telemetry-val">qwen/qwen3.8-27b</span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">Inference Latency</span>
                            <span className="telemetry-val" style={{ color: 'var(--emerald)' }}>~350 - 650 ms</span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">Token Budget (Quick / Deep)</span>
                            <span className="telemetry-val">1,800 / 3,500 tokens</span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">JSON Enforcement</span>
                            <span className="telemetry-val" style={{ color: 'var(--emerald)' }}>Enabled (response_format)</span>
                        </div>
                    </div>
                </div>

                {/* 3. Catalog & Dataset Scope */}
                <div className="glass-card telemetry-card">
                    <h3><span>📊</span> Dataset & Marketplace Scope</h3>
                    <div className="telemetry-list">
                        <div className="telemetry-item">
                            <span className="telemetry-key">GlowSkin Products</span>
                            <span className="telemetry-val">{skus.length} Core SKUs</span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">Benchmark Competitors</span>
                            <span className="telemetry-val">DermaCare (6 SKUs) + PureSkin (6 SKUs)</span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">Indexed Marketplaces</span>
                            <span className="telemetry-val">Amazon, Nykaa, Flipkart, Blinkit, D2C</span>
                        </div>
                        <div className="telemetry-item">
                            <span className="telemetry-key">Time Horizons</span>
                            <span className="telemetry-val">Nov 2025 – Feb 2026 (4-Month Trends)</span>
                        </div>
                    </div>
                </div>

                {/* 4. Preference & Memory Store */}
                <div className="glass-card telemetry-card">
                    <h3><span>💾</span> Persistent Session Memory</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                        User preferences stored in Qdrant's <code>user_memory</code> vector collection for context personalization across sessions.
                    </p>

                    <div className="telemetry-list" style={{ marginBottom: '1.25rem' }}>
                        {Object.entries(memory).length > 0 ? (
                            Object.entries(memory).map(([k, v]) => (
                                <div key={k} className="telemetry-item">
                                    <span className="telemetry-key" style={{ fontFamily: 'var(--font-mono)' }}>{k}</span>
                                    <span className="telemetry-val">{v}</span>
                                </div>
                            ))
                        ) : (
                            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No active preferences recorded.</div>
                        )}
                    </div>

                    <form onSubmit={handleSave} style={{ display: 'flex', gap: '0.6rem' }}>
                        <input
                            type="text"
                            placeholder="Key (e.g. market_focus)"
                            value={newKey}
                            onChange={e => setNewKey(e.target.value)}
                            className="followup-input"
                            style={{ fontSize: '0.82rem', padding: '0.5rem 0.9rem' }}
                        />
                        <input
                            type="text"
                            placeholder="Value (e.g. quick_commerce)"
                            value={newVal}
                            onChange={e => setNewVal(e.target.value)}
                            className="followup-input"
                            style={{ fontSize: '0.82rem', padding: '0.5rem 0.9rem' }}
                        />
                        <button
                            type="submit"
                            disabled={saving || !newKey.trim() || !newVal.trim()}
                            className="followup-btn"
                            style={{ fontSize: '0.82rem', padding: '0.5rem 1rem' }}
                        >
                            {saving ? 'Saving...' : 'Add'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
