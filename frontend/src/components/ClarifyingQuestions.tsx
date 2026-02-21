import type { ClarifyingQuestion } from '../types';

interface Props {
    questions: ClarifyingQuestion[];
    onAnswer: (question: string, answer: string) => void;
}

export function ClarifyingQuestions({ questions, onAnswer }: Props) {
    return (
        <div className="clarifying-panel glass-card">
            <h3>🤔 I need a bit more context...</h3>
            <div className="questions-list">
                {questions.map((q, i) => (
                    <div key={i} className="question-block">
                        <p className="question-text">{q.question}</p>
                        {q.context && <p className="question-context">{q.context}</p>}
                        <div className="question-options">
                            {q.options.map(opt => (
                                <button
                                    key={opt}
                                    className="option-btn"
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
