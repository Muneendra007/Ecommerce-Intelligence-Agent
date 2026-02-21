const API_BASE = 'http://localhost:8000/api';

export async function fetchHealth() {
    const res = await fetch(`${API_BASE}/health`);
    return res.json();
}

export async function fetchSKUs() {
    const res = await fetch(`${API_BASE}/skus`);
    return res.json();
}

export async function submitResearch(payload: {
    query: string;
    mode: string;
    goal: string;
    sku?: string | null;
}) {
    const res = await fetch(`${API_BASE}/research`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });
    return res.json();
}

export async function submitFollowUp(payload: {
    session_id: string;
    message: string;
}) {
    const res = await fetch(`${API_BASE}/followup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });
    return res.json();
}

export async function fetchMemory() {
    const res = await fetch(`${API_BASE}/memory`);
    return res.json();
}

export async function storeMemory(key: string, value: string) {
    const res = await fetch(`${API_BASE}/memory`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key, value, category: 'preference' }),
    });
    return res.json();
}
