from typing import Annotated, List, TypedDict, Optional
from pydantic import BaseModel, Field
import operator

# the output structure must provide by planner
class DesignStep(BaseModel):
    step_number:int
    agent_role: str =Field(description="Which agent should do this? (Research, Execution, etc.)")
    task_description:str
    dependencies: List[int] = Field(default_factory=list, description="Step numbers that must be done first")

class SystemDesignPlan(BaseModel):
    title:str
    total_steps:int
    steps: List[DesignStep]

# shared state that lives in langgraph
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    plan: Optional[SystemDesignPlan]
    current_step: int
    eval_score: float
