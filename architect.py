from model_config import get_model

def architect_agent(state:dict):
    """Drafts the technical architecture based on research."""
    llm = get_model()

    plan_title=state['plan'].title
    last_message=state['messages'][-1]

    if hasattr(last_message, 'content'):
        research_data = last_message.content
    elif isinstance(last_message, dict):
        research_data = last_message.get('content', str(last_message))
    else:
        research_data = str(last_message)

    system_prompt = """
        You are a Principal System Architect with 15+ years of experience designing
        large-scale, fault-tolerant, cloud-native systems.

        Your task is to design a high-level system architecture using the provided research.

        Follow these rules strictly:

        1. Clearly describe all major components, including:
        - Load Balancer
        - API Gateway
        - Authentication Service
        - Core Microservices
        - Message Queue / Event Bus
        - Caching Layer
        - Databases
        - Monitoring & Logging

        2. Justify every major design decision.
        Explain WHY each component is chosen.

        3. Choose appropriate databases (SQL / NoSQL / Hybrid) and explain trade-offs.

        4. Address:
        - Scalability
        - High Availability
        - Fault Tolerance
        - Security
        - Performance
        - Cost Optimization

        5. Provide a Mermaid.js diagram that visualizes:
        - Client → Backend → Data Flow
        - Internal service communication
        - External dependencies

        6. Use clear headings and bullet points.
        Keep the explanation concise but technically rigorous.

        7. Write as if presenting to senior engineers in a design interview.

        Output Format:

        - Title
        - System Overview
        - Architecture Components
        - Data Storage Strategy
        - Scalability & Reliability
        - Security Considerations
        - Mermaid Diagram
        - Final Recommendations
    """
    response = llm.invoke(
        [
            {"role":"system", "content": system_prompt},
            {"role": "user", "content":f"Project: {plan_title}\nResearch: {research_data}"}
        ]
    )

    return{
        "message": [{"role":"assistant", "content":response.content}],
        "current_step": state["current_step"] +1
    }
