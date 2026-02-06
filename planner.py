import os
from model_config import get_model
from schema import SystemDesignPlan

def get_planner_grade(state):
    llm=get_model()

    structured_llm=llm.with_structured_output(SystemDesignPlan)
    
    system_prompt = """
    You are a Lead System Architect responsible for creating clear, actionable,
    and high-quality plans for multi-agent execution.

    Your job is to analyze the user's request and break it down into a logical,
    step-by-step system design plan that other agents can follow.

    Follow this structure:

    1. Research Phase
    - Identify required technologies, tools, and frameworks
    - Analyze similar real-world systems
    - Highlight technical risks and constraints

    2. Design Phase
    - Define system architecture (frontend, backend, database, APIs, AI, etc.)
    - Explain data flow and component interactions
    - Select appropriate design patterns and scalability strategies

    3. Validation Phase
    - Review the design for performance, security, and reliability
    - Check for bottlenecks and failure points
    - Suggest improvements and optimizations

    Guidelines:
    - Be precise and practical
    - Avoid vague or generic steps
    - Think like a real system engineer
    - Optimize for scalability, maintainability, and security
    - Ensure the final plan is easy for other agents to execute
    """

    user_query=state["messages"][-1].content
    plan = structured_llm.invoke(
        [
            {"role":"system", "content":system_prompt},
            {"role":"user","content":user_query}
        ]
    )
    
    return {"plan":plan, "message":[{"role":"assistant", "content": f"Plan created: {plan.title}"}]}
