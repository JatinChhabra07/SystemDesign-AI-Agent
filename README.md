# 🤖 SystemDesign-AI-Agent

**An Autonomous Multi-Agent Framework for Professional System Architecture & Research**

---

## 🚀 Overview

SystemDesign-AI-Agent is a state-of-the-art multi-agent system designed to automate
the end-to-end process of system design.

It doesn't just chat; it researches, plans, architects, and validates complex
technical requirements into production-ready designs.

---

## 🌟 Key Features

### 🔁 Stateful Orchestration
- Built on LangGraph
- Uses a Directed Cyclic Graph (DCG) for managing multi-agent state

### 💾 Persistent Memory
- SQLite-backed checkpointers
- Remembers previous design turns
- Enables iterative refinements  
  (e.g., adding a booking module to a tracking app)

### 🤝 Specialized Agent Roles

- **Planner**  
  Breaks complex prompts into structured execution steps

- **Researcher**  
  Performs deep-dives into technologies (Kafka, Flink, etc.) using Tavily

- **Architect**  
  Synthesizes data into technical specs and Mermaid.js diagrams

- **Validator**  
  Scores designs on scalability, security, and cost

### 📊 Automated Visualization
- Direct rendering using Mermaid.js syntax

---

## 🛠️ Tech Stack

| Component        | Technology                          |
|------------------|--------------------------------------|
| Orchestration    | LangGraph & LangChain                |
| LLM Inference    | Groq (Llama 3.1 / 3.3)               |
| Vector DB / RAG  | ChromaDB                             |
| Persistence      | SQLite                               |
| API / UI         | FastAPI & Streamlit                 |
| Infrastructure   | Docker & Docker Compose             |

---

## 🧠 Workflow Architecture

The system operates in a continuous feedback loop:

1. **Input**  
   User requests a high-scale system  
   (e.g., "WhatsApp-like app")

2. **Research & Design**  
   Agents iterate until minimum validation score is achieved

3. **Output**  
   A comprehensive technical report with an integrated diagram

---

## 📦 How to Run

### 1️⃣ Prerequisites

- Docker & Docker Compose  
- Groq API Key (Free tier works)  
- Tavily API Key (For web search)

---

### 2️⃣ Environment Setup

Create a `.env` file in the `backend/` directory:

```env
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here


3️⃣ Launch
Run the entire stack:

docker-compose up --build


🌐 Access
Frontend: http://localhost:8501

Backend API: http://localhost:8000