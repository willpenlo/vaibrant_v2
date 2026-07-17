# vAIbrant — AI Security Analyzer

AI-powered code security scanner with RAG, agents, evals, and CI/CD.
Live API: https://vaibrantv2-production.up.railway.app/docs

## What it does
Scans Python, JavaScript, and TypeScript files for security vulnerabilities
using LLM analysis, AST parsing, and structured risk reporting.

## Architecture
- FastAPI REST API with API key auth
- OpenAI GPT-4o-mini for analysis
- AST parsing for deterministic pre-analysis
- SQLite for scan history persistence
- ChromaDB RAG pipeline for document Q&A
- Agent loop with tool use (file listing, scanning, summarization)
- Retrieval + generation evals with LLM-as-judge scoring
- Docker containerization
- CI/CD via GitHub Actions (auto-runs evals on every push)
- Cost and latency monitoring via /monitor endpoint
- Streamlit dashboard for scan history visualization

## Stack
Python 3.12, FastAPI, OpenAI, ChromaDB, SQLite, Docker, GitHub Actions

## Run locally
pip install -r requirements.txt
uvicorn api:app --reload

## API Endpoints
POST /analyze — analyze code text
POST /analyze/upload — upload a file
GET /history — scan history
GET /stats — risk level breakdown
GET /monitor — cost and latency stats
GET /docs — interactive API docs
