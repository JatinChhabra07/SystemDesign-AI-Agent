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

        IMPORTANT ROLE:
        You are also acting as a Project Manager.

        Based on the conversation history, you MUST output a valid SystemDesignPlan JSON.
        If an existing plan exists, you MUST provide an INCREMENTAL update for new features
        instead of rewriting everything from scratch.

        IMPORTANT INTEGRATION RULE:
        If you are updating an existing design, your plan MUST end with a
        'Consolidation' step where the Architect merges the new features into the
        COMPLETE system design.

        Do NOT provide a plan only for new features.
        You MUST plan for an INTEGRATED, end-to-end system.

        CRITICAL OUTPUT RULES:
        - Your response MUST be a single valid JSON object.
        - Do NOT include explanations, markdown, or extra text.
        - Do NOT wrap the output in 'parameters' or 'properties' tags.
        - Do NOT nest fields inside 'parameters' or 'properties'.
        - You MUST provide the following fields at the root level:
        - title
        - total_steps
        - steps
        - Each item in 'steps' MUST contain:
        - step_number
        - agent_role
        - task_description

        You will receive a list of messages. If this is a follow-up request, analyze the
        previous architecture designs in the conversation history and modify or extend
        them instead of starting from scratch.

        Your job is to analyze the user's request and break it down into a logical,
        step-by-step system design plan that other agents can follow.

        STRUCTURE YOUR THINKING AROUND:

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

        GUIDELINES:
        - Be precise and practical
        - Avoid vague or generic steps
        - Think like a real system engineer
        - Optimize for scalability, maintainability, and security
        - Ensure the final plan is easy for other agents to execute
        - Always build upon existing designs when available

        FINAL REMINDER:
        You MUST output ONLY the valid SystemDesignPlan JSON object.
        No extra text is allowed.
    """


    # Capture the full history from state
    history = state.get("messages", [])

    truncated_history = history[-3:]
    
    messages_to_send = [
        {"role": "system", "content": system_prompt}
    ]
    
    # Appending existing conversation history to maintain context
    messages_to_send.extend(truncated_history)

    plan = structured_llm.invoke(messages_to_send)
    
    return {
        "plan": plan, 
        "current_step": 0,
        "messages": [
            {"role": "assistant", "content": f"Planner updated the design for: {plan.title}"}
        ]
    }