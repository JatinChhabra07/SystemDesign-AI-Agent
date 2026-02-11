from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from langchain_core.messages import HumanMessage
from src.core.graph import app as agent_graph
import uvicorn
from src.utils.vector_store import ingest_docs
import shutil
import os
import traceback

app = FastAPI(title="System Design AI Agent Service")

os.makedirs("backend/data/", exist_ok=True)

@app.post("/ingest")
async def ingest_file(file: UploadFile=File(...)):
    temp_path = f"data/{file.filename}"
    with open(temp_path,"wb") as buffer:
        shutil.copyfileobj(file.file,   buffer)

    try:
        ingest_docs(temp_path)
        return {"status": "success", "message": f"Indexed {file.filename}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

class QueryRequest(BaseModel):
    query: str
    thread_id: str = "default_user"

@app.post("/design")
async def generate_design(request: QueryRequest):
    try:
        print(f"DEBUG: Received request for {request.query}")
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
        print("\n" + "="*50)
        print("CRITICAL ERROR IN BACKEND:")
        traceback.print_exc() 
        print("="*50 + "\n")
        
        raise HTTPException(status_code=500, detail=str(e))
    

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
        