# E-Commerce Deep Research Agent

A production-ready **dual-mode AI research agent** for e-commerce teams. Transforms raw catalog, pricing, review, and competitor data into actionable business decisions.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Dashboard (Vite)                     │
│  ┌──────────┐ ┌──────────────┐ ┌────────────┐ ┌──────────┐ │
│  │ QueryInput│ │ ResultsPanel │ │ MemoryPanel│ │ReportView│ │
│  └─────┬────┘ └──────┬───────┘ └─────┬──────┘ └────┬─────┘ │
│        └──────────────┼───────────────┼─────────────┘       │
│                       │  REST API     │                      │
├───────────────────────┼───────────────┼──────────────────────┤
│               FastAPI Backend (Python)                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Orchestrator                          │  │
│  │   ┌────────────┐  ┌────────────┐  ┌────────────────┐  │  │
│  │   │ Quick Mode │  │ Deep Mode  │  │ Session Mgr    │  │  │
│  │   │ <2 min     │  │ <10 min    │  │ (Follow-ups)   │  │  │
│  │   └────────────┘  └────────────┘  └────────────────┘  │  │
│  └──────────┬────────────┬───────────────┬───────────────┘  │
│             │            │               │                   │
│  ┌──────────┴──┐  ┌──────┴───────┐  ┌───┴──────────────┐   │
│  │  LLM Core   │  │ Tool Registry│  │  Vector Memory   │   │
│  │  (OpenAI)   │  │              │  │  (Qdrant)        │   │
│  └─────────────┘  │ • Pricing    │  └──────────────────┘   │
│                   │ • Reviews    │                           │
│  ┌────────────┐   │ • Competitor │   ┌──────────────────┐   │
│  │ Safeguards │   └──────────────┘   │ Report Generator │   │
│  │ • Validator│                      │ • Exec Reports   │   │
│  │ • CostCtrl │                      │ • Markdown Export │   │
│  └────────────┘                      └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Clone & Setup Backend

```bash
cd backend
cp .env.example .env           # Edit with your API keys
pip install -r requirements.txt
python run.py                  # Starts on http://localhost:8000
```

### 2. Setup Frontend

```bash
cd frontend
npm install
npm run dev                    # Starts on http://localhost:5173
```

### 3. Open Dashboard

Visit **http://localhost:5173** — the dashboard works in demo mode out of the box.

## Configuration

Edit `backend/.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | _(demo mode)_ |
| `OPENAI_MODEL` | Model to use | `gpt-4o` |
| `QDRANT_URL` | Qdrant server URL | `http://localhost:6333` |
| `QDRANT_API_KEY` | Qdrant auth key | _(in-memory fallback)_ |
| `DEMO_MODE` | Enable simulated data | `true` |

## Dual Research Modes

| Feature | ⚡ Quick Mode | 🔬 Deep Mode |
|---------|--------------|-------------|
| Target Time | < 2 minutes | < 10 minutes |
| Tool Calls | 1-2 max | 3-5 max |
| Token Budget | 2,000 | 8,000 |
| Output | Concise insights | Full analysis + citations |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | System health check |
| `POST` | `/api/research` | Execute research query |
| `POST` | `/api/followup` | Follow-up in session |
| `POST` | `/api/report` | Generate executive report |
| `GET` | `/api/memory` | View stored memory |
| `POST` | `/api/memory` | Store business context |

## Example Queries

- _"Top complaints for wireless earbuds under ₹2000 on Amazon"_
- _"Price comparison for running shoes: Amazon vs Flipkart"_
- _"Competitor analysis for skincare products in D2C"_
- _"What's the demand trend for laptop bags this quarter?"_

## Project Structure

```
Ecommerce_ai_agent/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Environment settings
│   │   ├── core/
│   │   │   ├── llm.py           # OpenAI integration
│   │   │   ├── memory.py        # Qdrant vector store
│   │   │   └── orchestrator.py  # Dual-mode engine
│   │   ├── tools/
│   │   │   ├── registry.py      # Tool dispatcher
│   │   │   ├── pricing.py       # Price analysis
│   │   │   ├── reviews.py       # Review sentiment
│   │   │   └── competitor.py    # Competitive intel
│   │   ├── models/schemas.py    # Pydantic models
│   │   ├── services/
│   │   │   ├── research.py      # Research service
│   │   │   └── report.py        # Report generator
│   │   └── safeguards/
│   │       ├── validator.py     # Hallucination guard
│   │       └── cost_control.py  # Token budgets
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # React UI components
│   │   ├── services/api.ts      # Backend API client
│   │   └── types/index.ts       # TypeScript interfaces
│   └── package.json
└── README.md
```

## Evaluation Criteria (Hackathon)

| Criterion | Weight | What We Demonstrate |
|-----------|--------|---------------------|
| **Architecture Design** | 25% | Modular Python backend, clean separation of concerns |
| **AI Agent Quality** | 25% | Dual-mode orchestration, tool-augmented reasoning |
| **Production Readiness** | 20% | Safeguards, cost control, graceful fallbacks |
| **User Experience** | 15% | Dark-themed dashboard, follow-up support, executive reports |
| **Innovation** | 15% | Vector memory for context, confidence scoring, structured output |
