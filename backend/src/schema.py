from typing import Annotated, List, TypedDict, Optional
from pydantic import BaseModel, Field
import operator

# The output structure must be provided by planner
class DesignStep(BaseModel):
    step_number: int = Field(description="The unique integer ID for this step (1, 2, 3...)")
    agent_role: str = Field(description="Agent responsible: Research, Architect, or Validator")
    task_description: str = Field(description="Clear instructions on what needs to be done in this step")
    dependencies: List[int] = Field(
        default_factory=list, 
        description="List of step_number integers that must be completed before this one"
    )

class SystemDesignPlan(BaseModel):
    """
    Plan for designing a system. 
    IMPORTANT: Provide 'title', 'total_steps', and 'steps' at the ROOT level of your JSON.
    """
    title: str = Field(description="A concise title for the system design project")
    total_steps: int = Field(description="Total number of steps in this plan")
    steps: List[DesignStep] = Field(description="The sequential list of design steps")

# Shared state that lives in LangGraph
class AgentState(TypedDict):
    # 'operator.add' ensures messages are appended, which is key for persistence
    messages: Annotated[list, operator.add] 
    plan: Optional[SystemDesignPlan]
    current_step: int
    eval_score: float