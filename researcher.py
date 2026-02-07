from langchain_community.tools.tavily_search import TavilySearchResults
from model_config import get_model

search_tool= TavilySearchResults(max_results=3)

def research_agent(state):
    """Fetches technical documentation and system design patterns."""

    query = state["plan"].steps[state["current_step"]].task_description

    search_results = search_tool.invoke({"query": query})

    # Append the findings to the message history
    content = f"Research Findings for '{query}':\n\n{search_results}"
    return {
        "messages": [{"role": "assistant", "content": content}],
        "current_step": state["current_step"] + 1
    }