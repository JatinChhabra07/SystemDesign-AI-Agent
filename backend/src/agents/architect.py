from src.utils.model_config import get_model
from src.utils.utils import sanitize_mermaid
import re

def architect_agent(state:dict):
    """Drafts the technical architecture based on research."""
    llm = get_model()

    plan_title=state['plan'].title

    history = state.get("messages", [])[-4:]



    # Identify the latest research content
    last_message = history[-1] if history else ""
    research_data = last_message.content if hasattr(last_message, 'content') else str(last_message)
    # Truncate research data further to be safe
    research_data = research_data[:1500]

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

        1. Start the code block STRICTLY with 'graph TD'. 
        2. ALL node labels MUST be wrapped in double quotes to prevent syntax errors. 
        Example: A["Load Balancer"]
        3. NEVER use nested double quotes like ""Label"". Use exactly one set of quotes.
        4. Avoid special characters like (), &, or / inside labels. If necessary, use hyphens instead.
        Example: D["Market Data Service - Kafka"]
        5. Use standard arrows only:
        --> for solid arrows
        -.-> for dotted arrows
        6. Each connection MUST be on its own new line.

        Wrap the final Mermaid code EXACTLY like this:

        ```mermaid
        graph TD
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
    messages_to_send = [{"role": "system", "content": system_prompt}]
    messages_to_send.extend(history)
    messages_to_send.append({
        "role": "user", 
        "content": f"Update the architecture for Project: {plan_title} using this new research: {research_data}"
    })

    response = llm.invoke(messages_to_send)
    raw_content = response.content

    # 3. Extract and sanitize the mermaid block
    mermaid_match = re.search(r"```mermaid\s*(.*?)\s*```", raw_content, re.DOTALL | re.IGNORECASE)

    if mermaid_match:
        clean_mermaid = sanitize_mermaid(mermaid_match.group(1))
        
        final_content = raw_content.replace(mermaid_match.group(1), clean_mermaid)
    else:
        final_content = raw_content

    return {
        "messages": [{"role": "assistant", "content": final_content}],
        "current_step": state["current_step"] + 1
    }