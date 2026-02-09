from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from langchain_core.messages import HumanMessage
from app import app as agent_graph
import uvicorn

app = FastAPI(title="System Design AI Agent Service")

class QueryRequest(BaseModel):
    query: str
    thread_id: str = "default_user"

@app.post("/design")
async def generate_design(request: QueryRequest):
    try:
        inputs = {"messages": [HumanMessage(content=request.query)]}
        config = {"configurable": {"thread_id": request.thread_id}}
        
        #using ainvoke for FastAPI (asynchronous)
        result = await agent_graph.ainvoke(inputs, config)
        
        # 2. Extract final message safely
        last_message = result["messages"][-1]
        
        # Check if it's a message object or a dict/string
        if hasattr(last_message, 'content'):
            final_report = last_message.content
        elif isinstance(last_message, dict):
            final_report = last_message.get('content', str(last_message))
        else:
            final_report = str(last_message)
        
        plan_title = "System Design Report"
        if result.get("plan"):
            plan_title = result["plan"].title

        return {
            "status": "success",
            "title": plan_title,
            "report": final_report,
            "steps_completed": result.get("current_step", 0)
        }
    except Exception as e:
        if "rate_limit_exceeded" in str(e).lower():
            return {
                "status": "error",
                "report": "🚨 Rate limit reached! Please wait a minute or switch to fallback model.",
                "title": "Rate Limit Hit"
            }
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
        