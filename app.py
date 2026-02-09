from langgraph.graph import StateGraph,END
from schema import AgentState
from planner import planner_agent
from researcher import research_agent
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from architect import architect_agent
from router import routing_logic
from validator import validator_agent


load_dotenv()

workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_agent)
workflow.add_node("researcher", research_agent)
workflow.add_node("architect", architect_agent)
workflow.add_node("validator", validator_agent)

# the graph flow
workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")

node_list = ["researcher", "architect", "validator"]

for node in node_list:
    workflow.add_conditional_edges(
        node,
        routing_logic,
        {
            "researcher": "researcher",
            "architect": "architect",
            "validator": "validator",
            "__end__": END
        }
    )

app = workflow.compile()

if __name__ == "__main__":
    inputs = {"messages": [HumanMessage(content="Design a high-scale chat app like WhatsApp")]}
    config = {"configurable": {"thread_id": "1"}}
    
    print("--- STARTING MULTI-AGENT SYSTEM ---")
    for output in app.stream(inputs, config):
        print(output)