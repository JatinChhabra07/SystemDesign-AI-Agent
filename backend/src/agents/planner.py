import os
from src.utils.model_config import get_model
from src.schema import SystemDesignPlan
from dotenv import load_dotenv

load_dotenv()

def planner_agent(state):
    llm=get_model()


    structured_llm=llm.with_structured_output(SystemDesignPlan)
    
    system_prompt = """
        You are a Lead System Architect and System Design Planner responsible for creating
        clear, actionable, and high-quality plans for multi-agent execution.

        You will receive a list of messages. If this is a follow-up request, analyze the
        previous architecture designs in the conversation history and modify or extend
        them instead of starting from scratch.

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
        - Always build upon existing designs when available
    """


    # 1. Capture the full history from state
    history = state.get("messages", [])

    truncated_history = history[-5:]
    
    # 2. Build the message list for the LLM
    # We include the system prompt first, followed by the entire history
    messages_to_send = [
        {"role": "system", "content": system_prompt}
    ]
    
    # Append existing conversation history to maintain context
    messages_to_send.extend(truncated_history)

    # 3. Invoke LLM with the full history context
    plan = structured_llm.invoke(messages_to_send)
    
    return {
        "plan": plan, 
        "current_step": 0,
        "messages": [
            {"role": "assistant", "content": f"Planner updated the design for: {plan.title}"}
        ]
    }
