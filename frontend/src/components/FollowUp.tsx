import { useState } from 'react';

interface Props {
    sessionId: string;
    onFollowUp: (message: string) => void;
    loading: boolean;
}

const SUGGESTIONS = [
    'Focus on negative reviews and complaints',
    'What price adjustment maximizes gross margin?',
    'Compare formula and packaging with DermaCare',
    'Draft an immediate 30-day action plan',
];

export function FollowUp({ sessionId, onFollowUp, loading }: Props) {
    const [message, setMessage] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!message.trim()) return;
        onFollowUp(message.trim());
        setMessage('');
    };

    return (
        <div className="glass-card followup-panel" style={{ marginTop: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.8rem' }}>
                <h4 style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span>💬</span> Intelligent Follow-Up Refinement
                </h4>
                <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                    Session: {sessionId.slice(0, 8)}...
                </span>
            </div>

            {/* Suggestions */}
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
                {SUGGESTIONS.map(s => (
                    <button
                        key={s}
                        type="button"
                        className="prompt-chip"
                        onClick={() => onFollowUp(s)}
                        disabled={loading}
                    >
                        {s}
                    </button>
                ))}
            </div>

            {/* Input Bar */}
            <form onSubmit={handleSubmit} className="followup-form">
                <input
                    type="text"
                    value={message}
                    onChange={e => setMessage(e.target.value)}
                    placeholder="Ask a clarifying follow-up question..."
                    className="followup-input"
                    disabled={loading}
                />
                <button
                    type="submit"
                    disabled={loading || !message.trim()}
                    className="followup-btn"
                >
                    {loading ? 'Thinking...' : 'Refine Analysis ↵'}
                </button>
            </form>
        </div>
    );
}
