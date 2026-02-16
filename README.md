# 🤖 SystemDesign-AI-Agent

**An Autonomous Multi-Agent Framework for Professional System Architecture & Research**

---

## 🚀 Overview

**SystemDesign-AI-Agent** is a state-of-the-art multi-agent system designed to automate the end-to-end process of system design.

It doesn't just chat — it **researches, plans, architects, and validates** complex technical requirements into **production-ready designs**.

---

## 🌟 Key Features

### 🔁 Stateful Orchestration
- Built on **LangGraph**
- Uses a Directed Cyclic Graph (DCG) for multi-agent coordination
- Maintains workflow state across iterations

### 💾 Persistent Memory
- SQLite-backed checkpointers
- Enables long-term context retention
- Supports iterative refinements  
  _(e.g., adding a booking module to an existing system)_

### 🤝 Specialized Agent Roles

- **Planner**
  - Breaks complex prompts into structured steps

- **Researcher**
  - Performs deep technical research using Tavily
  - Analyzes tools like Kafka, Flink, Redis, etc.

- **Architect**
  - Generates detailed technical specifications
  - Produces Mermaid.js architecture diagrams

- **Validator**
  - Evaluates scalability, security, and cost
  - Assigns quality scores

### 📊 Automated Visualization
- Native Mermaid.js support
- Renders system architecture directly in UI

---

## 🛠️ Tech Stack

| Component        | Technology                                |
|------------------|--------------------------------------------|
| Orchestration    | LangGraph & LangChain                     |
| LLM Inference    | Groq (Llama 3.1 / 3.3)                     |
| Vector DB / RAG  | ChromaDB (Local PDF Analysis)             |
| Persistence      | SQLite (Async Checkpoints)                |
| API / UI         | FastAPI & Streamlit                       |
| Infrastructure   | Docker & Docker Compose                   |

---

## 🧠 Workflow Architecture

The system operates in a continuous feedback loop:

1️⃣ **Input**  
User submits a system request  
_(e.g., "Build a WhatsApp-like app")_

2️⃣ **Research & Design**  
Agents collaborate and iterate until quality standards are met

3️⃣ **Validation**  
Design is reviewed and scored

4️⃣ **Output**  
A complete technical report with integrated diagrams

---

## 📦 How to Run

### 1️⃣ Prerequisites

Make sure you have:

- ✅ Docker & Docker Compose
- ✅ Groq API Key (Free tier supported)
- ✅ Tavily API Key (For web search)

---

### 2️⃣ Environment Setup

Create a `.env` file inside the `backend/` directory:

```env
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
