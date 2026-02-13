from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from langchain_core.messages import HumanMessage
import uvicorn
from src.utils.vector_store import ingest_docs
import shutil
import os
import traceback
from src.core.graph import get_app
from contextlib import asynccontextmanager
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from src.core.graph import workflow
from fastapi.responses import StreamingResponse


# Global variables to hold the app and the context manager
agent_app = None
_saver_context = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent_app, _saver_context
    # 1. Start the connection when the server starts
    _saver_context = AsyncSqliteSaver.from_conn_string("data/checkpoints.sqlite")
    memory = await _saver_context.__aenter__() 
    
    # 2. Compile the graph with the active memory instance
    agent_app = workflow.compile(checkpointer=memory)
    yield
    # 3. Close the connection when the server stops
    await _saver_context.__aexit__(None, None, None)

app = FastAPI(lifespan=lifespan)

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
    # agent_app = await get_app()
    
    try:
        print(f"DEBUG: Starting request for {request.query}")
        
        inputs = {"messages": [HumanMessage(content=request.query)]}
        config = {"configurable": {"thread_id": request.thread_id}}
        
        result = None
        async for chunk in agent_app.astream(inputs, config=config, stream_mode="values"):
            result = chunk
            print("DEBUG: Processing graph step...")

        if not result:
            raise HTTPException(status_code=500, detail="Graph failed to produce a result")

        last_message = result["messages"][-1]
        
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
        