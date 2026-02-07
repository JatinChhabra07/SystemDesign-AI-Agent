import os
from langgraph.graph import StateGraph,END
from schema import AgentState
from planner import planner_agent
from researcher import research_agent
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from architect import architect_agent


load_dotenv()

workflow = StateGraph(AgentState)

workflow.add_node("planner_node", planner_agent)
workflow.add_node("research_node", research_agent)

# the graph flow
workflow.set_entry_point("planner_node")
workflow.add_edge("planner_node", "research_node")
workflow.add_edge("research_node", END)


app = workflow.compile()

if __name__ == "__main__":
    # Wrap your input in a HumanMessage object
    inputs = {
        "messages": [HumanMessage(content="Design a high-scale chat app like WhatsApp")]
    }
    
    config = {"configurable": {"thread_id": "1"}}
    
    for output in app.stream(inputs, config):
        for key, value in output.items():
            print(f"\n--- Node: {key} ---")
            print(value)