import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Props {
    text: string;
    speed?: number; // Speed in ms per word
    onComplete?: () => void;
}

export function Typewriter({ text, speed = 50, onComplete }: Props) {
    const [displayedText, setDisplayedText] = useState('');
    const [currentIndex, setCurrentIndex] = useState(0);
    const chunks = useRef<string[]>([]);
    const timerRef = useRef<any>(null);
    const hasCalledComplete = useRef(false);

    useEffect(() => {
        // Use capturing group to preserve whitespace and newlines
        chunks.current = text.split(/(\s+)/).filter(Boolean);
        setDisplayedText('');
        setCurrentIndex(0);
        hasCalledComplete.current = false;
    }, [text]);

    useEffect(() => {
        if (chunks.current.length === 0 && text.length > 0) {
            setDisplayedText(text);
            if (onComplete && !hasCalledComplete.current) {
                hasCalledComplete.current = true;
                onComplete();
            }
            return;
        }

        if (currentIndex < chunks.current.length) {
            timerRef.current = setTimeout(() => {
                setDisplayedText((prev) => prev + chunks.current[currentIndex]);
                setCurrentIndex((prev) => prev + 1);
            }, speed);
        } else if (chunks.current.length > 0 && !hasCalledComplete.current) {
            hasCalledComplete.current = true;
            if (onComplete) onComplete();
        }

        return () => {
            if (timerRef.current) clearTimeout(timerRef.current);
        };
    }, [currentIndex, speed, onComplete]);

    return (
        <div className="typewriter-content">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {displayedText}
            </ReactMarkdown>
            {currentIndex < chunks.current.length && (
                <span className="typewriter-cursor">|</span>
            )}
        </div>
    );
}
