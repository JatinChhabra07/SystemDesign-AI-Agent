import os
from src.utils.model_config import get_model
from src.schema import SystemDesignPlan
from dotenv import load_dotenv

load_dotenv()

def planner_agent(state):
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

    last_message=state["messages"][-1].content

    if hasattr(last_message, 'content'):
        user_query = last_message.content
    # Check if it's a dictionary (has .get)
    elif isinstance(last_message, dict):
        user_query = last_message.get('content', str(last_message))
    # Otherwise, treat it as a string
    else:
        user_query = str(last_message)


    plan = structured_llm.invoke(
        [
            {"role":"system", "content":system_prompt},
            {"role":"user","content":user_query}
        ]
    )
    
    return {
        "plan": plan, 
        "current_step": 0,
        "messages": [{"role": "assistant", "content": f"Planner has outlined: {plan.title}"}]
    }
