from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from src.utils.vector_store import ingest_docs
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.utils.model_config import get_model

load_dotenv()

def research_agent(state):
    """Executes the research step of the plan, checking local PDFs first to save costs."""

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="data/chroma_db", embedding_function=embeddings)

    current_step_idx = state["current_step"]
    task = state["plan"].steps[current_step_idx].task_description

    history = state.get("messages", [])[-5:]
    
    llm = get_model()

    refinement_prompt = f"""
    Based on the following conversation history, rewrite this task description into a 
    standalone search query that captures the full context of the system design.
    
    Task: {task}
    """

    refined_query_response = llm.invoke(history + [{"role": "user", "content": refinement_prompt}])
    refined_query = refined_query_response.content

    local_docs = vectorstore.similarity_search(refined_query, k=2)

    # Append the findings to the message history
    if local_docs:
        results_source = "Local PDF Documents"
        search_results = "\n".join([doc.page_content[:500] for doc in local_docs])
    
    else:
        results_source = "Web Search (Tavily)"
        search_tool= TavilySearchResults(max_results=2)
        search_results = search_tool.invoke({"query": refined_query})[:1000]
        search_results = search_results[:1000]

    content = f"Source: {results_source}\nResearch Findings for '{refined_query}':\n\n{search_results}"
    return {
        "messages": [{"role": "assistant", "content": content}],
        "current_step": current_step_idx + 1
    }