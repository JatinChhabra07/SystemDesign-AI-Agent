# 🤖 SystemDesign-AI-Agent
A professional multi-agent AI system that researches, plans, and visualizes complex system architectures using **LangGraph**, **Groq**, and **Streamlit**.

## 🚀 Key Features
- **Multi-Agent Orchestration**: Specialized agents for Planning, Research, Architecture, and Validation.
- **Iterative Design**: Persistent memory allows you to refine designs over multiple turns.
- **RAG Integration**: Analyzes local technical PDFs using ChromaDB for grounded recommendations.
- **Dynamic Visuals**: Automatically generates and renders Mermaid.js diagrams.
- **Token Efficient**: Optimized for Groq's 6000 TPM limit using a sliding-window context.

## 🛠️ Tech Stack
- **AI/ML**: LangChain, LangGraph, Groq (Llama 3.1), HuggingFace Embeddings.
- **Backend**: FastAPI, SQLite (Persistence), ChromaDB (Vector Store).
- **Frontend**: Streamlit, Mermaid.js.
- **DevOps**: Docker, Docker-Compose.

## 📦 How to Run
1. **Clone the repo**
2. **Add API Keys**: Place your `GROQ_API_KEY` and `TAVILY_API_KEY` in `./backend/.env`.
3. **Launch with Docker**:
   ```bash
   docker-compose up --build