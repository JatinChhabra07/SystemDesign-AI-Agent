from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()


search_tool= TavilySearchResults(max_results=3)

def research_agent(state):
    """Executes the research step of the plan."""

    query = state["plan"].steps[state["current_step"]].task_description

    search_results = search_tool.invoke({"query": query})

    # Append the findings to the message history
    content = f"Research Findings for '{query}':\n\n{search_results}"
    return {
        "messages": [{"role": "assistant", "content": content}],
        "current_step": state["current_step"] + 1
    }