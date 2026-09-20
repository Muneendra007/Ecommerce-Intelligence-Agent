import { useState } from 'react';

interface CompetitorProduct {
    brand: string;
    sku: string;
    name: string;
    price: number;
    rating: number;
    marketplace: string;
    category: string;
    keyAdvantage: string;
    packaging: string;
}

const COMPETITOR_BENCHMARKS: CompetitorProduct[] = [
    {
        brand: 'GlowSkin (Us)',
        sku: 'VITC30',
        name: 'GlowSkin Vitamin C Serum 30ml',
        price: 899,
        rating: 4.2,
        marketplace: 'Amazon, Nykaa, Flipkart',
        category: 'Vitamin C Serum',
        keyAdvantage: '20% High-strength L-Ascorbic Acid + HA',
        packaging: 'Glass Dropper Bottle',
    },
    {
        brand: 'DermaCare',
        sku: 'DC-VITC',
        name: 'DermaCare 15% Vitamin C + Ferulic Acid',
        price: 749,
        rating: 4.4,
        marketplace: 'Amazon, Nykaa, Quick Commerce',
        category: 'Vitamin C Serum',
        keyAdvantage: 'Ferulic Acid stabilization, darker amber bottle prevents oxidation',
        packaging: 'Amber UV-Protected Glass',
    },
    {
        brand: 'PureSkin',
        sku: 'PS-VITC',
        name: 'PureSkin Gentle Glow 10% Vitamin C',
        price: 699,
        rating: 4.1,
        marketplace: 'Amazon, Flipkart',
        category: 'Vitamin C Serum',
        keyAdvantage: 'Budget entry-level, non-irritating for sensitive skin',
        packaging: 'Plastic Pump Bottle',
    },
    {
        brand: 'GlowSkin (Us)',
        sku: 'HYALU50',
        name: 'GlowSkin Hyaluronic Acid Moisturizer 50ml',
        price: 1299,
        rating: 4.5,
        marketplace: 'Amazon, Nykaa',
        category: 'Moisturizer',
        keyAdvantage: 'Multi-molecular weight HA + Ceramide complex',
        packaging: 'Airless Pump Jar',
    },
    {
        brand: 'DermaCare',
        sku: 'DC-HYALU',
        name: 'DermaCare Ceramide Hydrating Cream 60g',
        price: 899,
        rating: 4.3,
        marketplace: 'Amazon, Quick Commerce',
        category: 'Moisturizer',
        keyAdvantage: '35% lower price point, generous 60g volume',
        packaging: 'Squeeze Tube',
    },
    {
        brand: 'GlowSkin (Us)',
        sku: 'SUN50',
        name: 'GlowSkin Matte Sunscreen SPF 50 PA++++',
        price: 699,
        rating: 4.4,
        marketplace: 'Amazon, Blinkit, D2C',
        category: 'Sunscreen',
        keyAdvantage: 'Zero white cast, ultra-light silicone-free matte finish',
        packaging: 'Travel Squeeze Tube',
    },
    {
        brand: 'DermaCare',
        sku: 'DC-SUN',
        name: 'DermaCare Ultra-Light Water-Gel SPF 50',
        price: 649,
        rating: 4.6,
        marketplace: 'Amazon, Nykaa, Blinkit',
        category: 'Sunscreen',
        keyAdvantage: 'Top-rated watery texture, high Blinkit quick-commerce volume',
        packaging: 'Pump Dispenser',
    },
    {
        brand: 'GlowSkin (Us)',
        sku: 'SALI100',
        name: 'GlowSkin Salicylic Acid Cleanser 100ml',
        price: 599,
        rating: 4.1,
        marketplace: 'Amazon, Flipkart',
        category: 'Cleanser',
        keyAdvantage: '2% BHA with soothing Aloe extract',
        packaging: 'Flip-top Bottle',
    },
    {
        brand: 'DermaCare',
        sku: 'DC-SALI',
        name: 'DermaCare 2% BHA Pore Cleanser 120ml',
        price: 549,
        rating: 4.4,
        marketplace: 'Amazon, Nykaa',
        category: 'Cleanser',
        keyAdvantage: 'Gentle surfactants, lower return rate on Flipkart',
        packaging: 'Pump Dispenser',
    },
];

interface Props {
    onAnalyzeCompetitor: (query: string) => void;
}

export function CompetitorRadar({ onAnalyzeCompetitor }: Props) {
    const [selectedCategory, setSelectedCategory] = useState<string>('All');

    const categories = ['All', 'Vitamin C Serum', 'Moisturizer', 'Sunscreen', 'Cleanser'];

    const filtered = selectedCategory === 'All'
        ? COMPETITOR_BENCHMARKS
        : COMPETITOR_BENCHMARKS.filter(p => p.category === selectedCategory);

    return (
        <div className="tab-pane">
            <div className="glass-card" style={{ padding: '2rem', marginBottom: '2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
                    <div>
                        <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.5rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                            <span>📡</span> Competitor Intelligence Radar
                        </h2>
                        <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', marginTop: '0.3rem' }}>
                            Continuous price, rating, and formula battlecard monitoring against DermaCare and PureSkin across Amazon, Nykaa, and Quick-Commerce.
                        </p>
                    </div>

                    {/* Category Filter Pills */}
                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                        {categories.map(cat => (
                            <button
                                key={cat}
                                type="button"
                                className={`prompt-chip ${selectedCategory === cat ? 'active' : ''}`}
                                style={{
                                    background: selectedCategory === cat ? 'var(--accent-secondary)' : 'rgba(255, 255, 255, 0.05)',
                                    color: selectedCategory === cat ? '#fff' : 'var(--text-secondary)',
                                    borderColor: selectedCategory === cat ? 'var(--accent-primary)' : 'var(--border-subtle)',
                                    padding: '0.45rem 1rem',
                                }}
                                onClick={() => setSelectedCategory(cat)}
                            >
                                {cat}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Battlecard Grid */}
                <div className="competitor-battle-grid">
                    {filtered.map((item, idx) => {
                        const isUs = item.brand.includes('GlowSkin');
                        return (
                            <div
                                key={idx}
                                className="competitor-card"
                                style={{
                                    border: isUs ? '1px solid rgba(139, 92, 246, 0.45)' : '1px solid var(--border-subtle)',
                                    background: isUs ? 'rgba(20, 26, 56, 0.75)' : 'rgba(11, 16, 36, 0.65)',
                                    boxShadow: isUs ? '0 0 20px rgba(139, 92, 246, 0.15)' : 'none',
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                                    <span style={{
                                        fontFamily: 'var(--font-mono)',
                                        fontSize: '0.72rem',
                                        fontWeight: 700,
                                        padding: '0.2rem 0.5rem',
                                        borderRadius: 'var(--radius-sm)',
                                        background: isUs ? 'var(--accent-secondary)' : 'rgba(255, 255, 255, 0.08)',
                                        color: '#fff',
                                    }}>
                                        {item.brand}
                                    </span>

                                    <span style={{ color: '#facc15', fontSize: '0.88rem', fontWeight: 600 }}>
                                        ★ {item.rating}
                                    </span>
                                </div>

                                <div className="competitor-card-title">{item.name}</div>

                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem', margin: '0.8rem 0' }}>
                                    <div className="competitor-kv">
                                        <span>Price</span>
                                        <span style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--emerald)', fontFamily: 'var(--font-mono)' }}>
                                            ₹{item.price}
                                        </span>
                                    </div>
                                    <div className="competitor-kv">
                                        <span>Packaging</span>
                                        <span style={{ color: 'var(--text-secondary)' }}>{item.packaging}</span>
                                    </div>
                                </div>

                                <div className="competitor-gap-highlight" style={{
                                    background: isUs ? 'rgba(16, 185, 129, 0.08)' : 'rgba(244, 63, 94, 0.08)',
                                    borderLeftColor: isUs ? 'var(--emerald)' : 'var(--rose)',
                                }}>
                                    <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
                                        {isUs ? 'Core GlowSkin Claim' : 'Competitor Advantage'}
                                    </div>
                                    <div style={{ fontSize: '0.86rem', color: '#fff', marginTop: '0.2rem' }}>
                                        {item.keyAdvantage}
                                    </div>
                                </div>

                                <button
                                    type="button"
                                    className="sku-diagnose-btn"
                                    style={{ marginTop: '1rem', fontSize: '0.8rem', padding: '0.5rem 0.8rem' }}
                                    onClick={() => onAnalyzeCompetitor(`Compare GlowSkin vs ${item.brand} for ${item.category}. What is their advantage and how should we compete?`)}
                                >
                                    🔍 Run Head-to-Head AI Diagnosis
                                </button>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
