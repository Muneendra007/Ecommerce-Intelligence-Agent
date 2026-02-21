import { useState } from 'react';

interface Props {
    sessionId: string;
    onFollowUp: (message: string) => void;
    loading: boolean;
}

const SUGGESTIONS = [
    'Focus on negative reviews only',
    'Optimize for margins instead',
    'Compare with DermaCare specifically',
    'Show me the competitive feature gaps',
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
        <div className="followup-panel glass-card">
            <h3>💬 Follow-Up</h3>
            <p className="session-id">Session: {sessionId}</p>

            <div className="suggestion-chips">
                {SUGGESTIONS.map(s => (
                    <button
                        key={s}
                        className="suggestion-chip"
                        onClick={() => onFollowUp(s)}
                        disabled={loading}
                    >
                        {s}
                    </button>
                ))}
            </div>

            <form onSubmit={handleSubmit} className="followup-form">
                <input
                    type="text"
                    value={message}
                    onChange={e => setMessage(e.target.value)}
                    placeholder="Ask a follow-up question..."
                    className="followup-input"
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !message.trim()} className="followup-btn">
                    Send
                </button>
            </form>
        </div>
    );
}
