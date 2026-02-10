from src.utils.model_config import get_model
from src.utils.utils import sanitize_mermaid
import re

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

        CRITICAL INSTRUCTION: You must include a Mermaid.js diagram and follow these rules strictly:

        1. Start the code block with 'graph LR' or 'graph TD'.
        2. ALL node labels with special characters (spaces, (), &, /) MUST be double-quoted.
        Example: A["Database (Postgres)"]
        3. Avoid using illegal characters like <, >, or & unless escaped.
        4. Use standard arrows only:
        --> for solid arrows
        -.-> for dotted arrows
        5. Keep the diagram simple and clean.

        Wrap the final Mermaid code EXACTLY like this:

        ```mermaid
        graph LR
        A["Client"] --> B["API Gateway"]
        B --> C["Microservices"]



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

    raw_content = response.content

    # Extract just the mermaid block
    mermaid_match = re.search(r"```mermaid\s+(.*?)\s+```", raw_content, re.DOTALL)

    if mermaid_match:
        clean_mermaid = sanitize_mermaid(mermaid_match.group(1))

        final_content = raw_content.replace(mermaid_match.group(1), clean_mermaid)
    else:
        final_content = raw_content

    return{
        "messages": [{"role":"assistant", "content":final_content}],
        "current_step": state["current_step"] +1
    }
