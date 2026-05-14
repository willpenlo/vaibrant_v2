# vAIbrant

AI-powered code security analyzer. Scans Python files for vulnerabilities,
hardcoded secrets, and dangerous function calls using LLM analysis.

## Features
- Analyze raw code via REST API
- Upload .py files for instant security reports
- Risk levels: LOW / MEDIUM / HIGH / CRITICAL
- JSON output for integration with other tools
- Auto-generated API docs at /docs

## Setup
```bash
git clone https://github.com/yourusername/vaibrant
cd vaibrant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your OpenAI key
```

## Run
```bash
uvicorn api:app --reload
```

## API Endpoints
- POST /analyze — send code as JSON
- POST /analyze/upload — upload a .py file
- GET /docs — interactive API documentation

## Built with
- FastAPI, Python, OpenAI GPT-4o-mini