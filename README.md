🤖 SystemDesign-AI-Agent
An Autonomous Multi-Agent Orchestration Framework for Professional System Architecture Design.

Built with LangGraph, this system automates technical research, architectural planning, and Mermaid.js visualization using a stateful, persistent multi-agent workflow.

🌟 Key Technical Highlights
Stateful Intelligence: Leverages SQLite-backed checkpointers to maintain session persistence. You can refine a design incrementally across multiple turns without losing context.

Autonomous Routing: Implemented custom routing_logic that dynamically navigates between Research, Architecture, and Validation nodes based on task completion and scoring.

Optimized for Real-Time Stacks: Specialized in generating designs for high-throughput systems involving Apache Kafka, Apache Flink, and PostgreSQL/PostGIS.

Self-Healing Design: A dedicated Validator Agent scores outputs and triggers automatic re-planning if technical constraints (like scalability or security) are not met.

🛠️ Tech Stack
Orchestration: LangGraph, LangChain

Compute Engine: Groq (Llama 3.1/3.3)

Research & RAG: Tavily Search API & ChromaDB

Storage: SQLite (Agent State) & PostgreSQL (System Design Target)

Infrastructure: FastAPI, Docker, Docker-Compose

🚀 Execution Guide (How to Run)
1. Prerequisites
Ensure you have Docker and Docker-Compose installed on your system.

2. Environment Configuration
Create a .env file in the backend/ directory:

Code snippet
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
3. Launching the System
Use Docker to orchestrate the backend and frontend services simultaneously:

Bash
# Clone the repository
git clone https://github.com/your-username/SystemDesign-AI-Agent.git
cd SystemDesign-AI-Agent

# Build and Start
docker-compose up --build
Backend API: Running at http://localhost:8000

Frontend UI: Accessible at http://localhost:8501

🧠 Agent Workflow Detail
Planner: Receives the prompt and generates a multi-step execution plan.

Researcher: Performs deep-dives into specific technologies (e.g., Kafka vs RabbitMQ).

Architect: Generates technical specs and a Mermaid.js diagram.

Validator: Performs a "Critical Review" (Security, Scalability, Cost) and provides a score.

📊 Deployment & CI/CD
This project is configured for automated deployment via GitHub Actions. Every push to main triggers:

Automated Unit Testing.

Docker Image Build.

Deployment to Render/AWS.