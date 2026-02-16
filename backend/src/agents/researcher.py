import re
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from src.utils.vector_store import ingest_docs
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.utils.model_config import get_model

load_dotenv()


def research_agent(state):
    """
    Executes research phase.
    Uses Local RAG first → Tavily fallback.
    Forces graph progression after each step.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="data/chroma_db",
        embedding_function=embeddings
    )


    current_step_idx = state.get("current_step", 0)
    plan = state.get("plan")

    if not plan or current_step_idx >= len(plan.steps):
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": "✅ Research phase complete. Moving to design phase."
                }
            ],
            "current_step": current_step_idx
        }

    step = plan.steps[current_step_idx]
    task = step.task_description
    agent_role = step.agent_role

    # Get recent chat history (for context)
    history = state.get("messages", [])[-5:]

    llm = get_model()


    refinement_prompt = f"""
Rewrite the following task into ONE concise technical search query.

CRITICAL RULES:
- Max 10–15 words
- No alternatives
- No filler text
- No explanations
- No quotes
- Focus on system design / architecture keywords

Task:
{task}
"""

    refined_query_response = llm.invoke(
        history + [{"role": "user", "content": refinement_prompt}]
    )

    refined_query = refined_query_response.content.strip()


    # Take only first line
    cleaned_query = refined_query.split("\n")[0].strip()

    # Remove quotes
    cleaned_query = re.sub(r'["\']', '', cleaned_query)

    # Truncate for Tavily safety
    final_search_query = cleaned_query[:150]

    local_docs = vectorstore.similarity_search(
        final_search_query,
        k=2
    )

    if local_docs:

        results_source = "Local PDF Documents"

        search_results = "\n\n".join(
            [doc.page_content[:500] for doc in local_docs]
        )

    else:


        results_source = "Web Search (Tavily)"

        search_tool = TavilySearchResults(
            max_results=2
        )

        try:

            raw_results = search_tool.invoke(
                {"query": final_search_query}
            )

            search_results = str(raw_results)[:1000]

        except Exception as e:

            print(
                f"DEBUG: Tavily Error with query '{final_search_query}': {e}"
            )

            search_results = (
                "Web search failed. "
                "Proceeding with internal architectural knowledge."
            )

    content = f"""
### 🔍 Step {current_step_idx + 1}: Researching {agent_role}

**Task:** {task}

**Query Used:** {final_search_query}

**Source:** {results_source}

---

{search_results}
""".strip()


    return {
        "messages": [
            {
                "role": "assistant",
                "content": content
            }
        ],
        "current_step": current_step_idx + 1
    }
