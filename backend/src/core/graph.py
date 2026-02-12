from langgraph.graph import StateGraph,END
from src.schema import AgentState
from src.agents.planner import planner_agent
from src.agents.researcher import research_agent
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from src.agents.architect import architect_agent
from src.core.router import routing_logic
from src.agents.validator import validator_agent
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from src.schema import AgentState
import os
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import asyncio


os.makedirs("data", exist_ok=True)


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

# ASYNC COMPATIBILITY: Wrap compilation in a helper function
async def get_app():
    """
    Properly handles the Async Context Manager for the checkpointer.
    """
    # 1. Initialize the async context manager
    checkpointer_context = AsyncSqliteSaver.from_conn_string("data/checkpoints.sqlite")
    
    memory = await checkpointer_context.__aenter__()
    
    # 3. Compile and return
    return workflow.compile(checkpointer=memory)

if __name__ == "__main__":

    async def main():
        app = await get_app()
        inputs = {"messages": [HumanMessage(content="Design a high-scale chat app like WhatsApp")]}
        config = {"configurable": {"thread_id": "1"}}
        
        print("--- STARTING MULTI-AGENT SYSTEM ---")
        async for output in app.astream(inputs, config): 
            print(output)

    asyncio.run(main())