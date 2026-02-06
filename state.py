from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    message: Annotated[List[BaseMessage],operator.add]
    # for tracking the current working agent
    sender:str
    # plan made by planner
    plan:str
    eval_score:float
    # for specific things
    constraints: List[str]