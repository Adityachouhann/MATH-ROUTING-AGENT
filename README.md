# Math Routing Agent - AI-Powered Mathematical Professor

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

An intelligent Agentic-RAG system that replicates a mathematical professor, providing step-by-step solutions with intelligent routing between knowledge base and web search.

## 🎯 Features

- **🤖 Agentic-RAG Architecture** - Intelligent routing between knowledge base and web search
- **🔒 AI Gateway Guardrails** - Input/output validation with privacy protection
- **📚 Vector Database** - Qdrant-based knowledge base with semantic search
- **🌐 MCP Web Search** - Model Context Protocol for enhanced web retrieval
- **🔄 Human-in-the-Loop** - DSPy-powered feedback system for continuous learning
- **🧮 Educational Focus** - Step-by-step mathematical solutions
- **⚡ FastAPI Backend** - High-performance REST API

## 🏗️ System Architecture


## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API Key
- Tavily API Key (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/math-routing-agent.git
cd math-routing-agent

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

# Create .env file
echo OPENAI_API_KEY=your_openai_key_here > .env
echo TAVILY_API_KEY=your_tavily_key_here >> .env

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

python test_complete.py


math-routing-agent/
├── app/                          # FastAPI Backend
│   ├── agents/                   # AI Agents
│   │   ├── math_solver.py        # Math solution generator
│   │   ├── routing_agent.py      # Intelligent routing (DSPy)
│   │   └── feedback_agent.py     # Human-in-the-loop system
│   ├── guardrails/               # AI Safety
│   │   └── ai_gateway.py         # Input/output validation
│   ├── knowledge_base/           # Vector Database
│   │   └── vector_db.py          # Qdrant vector store
│   ├── mcp/                      # Model Context Protocol
│   │   └── web_search.py         # Web search with MCP
│   ├── models/                   # Pydantic models
│   │   └── schemas.py            # API schemas
│   └── main.py                   # FastAPI application
├── benchmarks/                   # Testing & Evaluation
│   └── jee_bench.py              # JEE benchmark tests
├── storage/                      # Data storage
│   └── feedback_data.json        # Feedback storage
├── requirements.txt              # Dependencies
├── test_complete.py              # Comprehensive tests
└── README.md                     # This file

python test_complete.py

python benchmarks/jee_bench.py

python -m uvicorn app.main:app --reload

# Using Uvicorn with workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Using Gunicorn (Linux/Mac)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
