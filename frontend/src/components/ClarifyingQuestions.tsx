import type { ClarifyingQuestion } from '../types';

interface Props {
    questions: ClarifyingQuestion[];
    onAnswer: (question: string, answer: string) => void;
}

export function ClarifyingQuestions({ questions, onAnswer }: Props) {
    return (
        <div className="glass-card" style={{ padding: '1.75rem', marginBottom: '1.5rem', border: '1px solid rgba(245, 158, 11, 0.4)', background: 'rgba(245, 158, 11, 0.05)' }}>
            <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', fontWeight: 600, color: 'var(--amber)', marginBottom: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span>🤔</span> Clarification Needed for Precision
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {questions.map((q, i) => (
                    <div key={i} style={{ padding: '1rem', background: 'rgba(15, 23, 42, 0.6)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
                        <p style={{ fontWeight: 600, color: '#fff', fontSize: '0.98rem', marginBottom: '0.3rem' }}>{q.question}</p>
                        {q.context && <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '0.8rem' }}>{q.context}</p>}
                        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                            {q.options.map(opt => (
                                <button
                                    key={opt}
                                    type="button"
                                    className="prompt-chip"
                                    style={{ background: 'rgba(245, 158, 11, 0.15)', borderColor: 'rgba(245, 158, 11, 0.4)', color: '#fff', padding: '0.45rem 0.95rem' }}
                                    onClick={() => onAnswer(q.question, opt)}
                                >
                                    {opt}
                                </button>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
