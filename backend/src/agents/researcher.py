from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from src.utils.vector_store import ingest_docs
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
load_dotenv()

def research_agent(state):
    """Executes the research step of the plan, checking local PDFs first to save costs."""

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="data/chroma_db", embedding_function=embeddings)

    query = state["plan"].steps[state["current_step"]].task_description
    local_docs = vectorstore.similarity_search(query, k=2)

    # Append the findings to the message history
    if local_docs:
        results_source = "Local PDF Documents"
        search_results = "\n".join([doc.page_content for doc in local_docs])
    
    else:
        results_source = "Web Search (Tavily)"
        search_tool= TavilySearchResults(max_results=3)
        search_results = search_tool.invoke({"query": query})

    content = f"Source: {results_source}\nResearch Findings for '{query}':\n\n{search_results}"
    return {
        "messages": [{"role": "assistant", "content": content}],
        "current_step": state["current_step"] + 1
    }