from src.utils.model_config import get_model
from src.utils.utils import sanitize_mermaid
import re

def architect_agent(state:dict):
    """Drafts the technical architecture based on research."""
    llm = get_model()

    plan_title=state['plan'].title

    history = state.get("messages", [])[-2:]



    # Identify the latest research content
    last_message = history[-1] if history else ""
    research_data = last_message.content if hasattr(last_message, 'content') else str(last_message)
    # Truncate research data further to be safe
    truncated_research = str(research_data)[:1500]

    system_prompt = """
        You are a Principal System Architect with 15+ years of real-world experience 
        in designing scalable, reliable, and cost-efficient software systems.

        Your task is to analyze the user's requirements and design a PRACTICAL,
        REALISTIC, and WELL-JUSTIFIED system architecture.

        Your goal is NOT to impress with complexity.
        Your goal is to build the RIGHT system for the given use case.

        --------------------------------------------------
        CORE PRINCIPLES (MANDATORY):

        1. Avoid generic templates and boilerplate designs.
        2. Include ONLY components that are technically justified.
        3. Prefer simple architectures when scale is small or medium.
        4. Introduce advanced components (CDN, Load Balancer, Cache, Queue, Microservices)
        ONLY when they solve a clear, stated problem.
        5. For every major component:
        - Explain WHY it is included
        - Explain WHY alternatives were rejected
        6. If a common component is NOT used, explicitly justify its omission.
        7. Optimize for:
        - Performance
        - Cost
        - Maintainability
        - Scalability
        - Reliability

        --------------------------------------------------
        ANALYSIS REQUIREMENTS:

        Before proposing the architecture, reason about:
        - Expected traffic
        - Data volume
        - Read/write patterns
        - Latency needs
        - Availability requirements
        - Budget sensitivity

        Use these factors to guide all decisions.

        --------------------------------------------------
        OUTPUT FORMAT (STRICTLY FOLLOW):

        1. Title
        2. System Overview
        - Use Case Summary
        - Expected Scale (Small / Medium / Large)
        - Target Users
        - Key Constraints

        3. Architecture Design (With Justification)
        - Frontend Layer
        - Backend Layer
        - Database Layer
        - Caching / Messaging (if applicable)
        - Infrastructure Layer
        For each component:
        - Purpose
        - Reason for Selection

        4. Data Management Strategy
        - SQL vs NoSQL decision
        - Schema design approach
        - Indexing strategy
        - Backup & recovery plan

        5. Mermaid Architecture Diagram
        - Provide a clean, readable diagram
        - Wrap inside ```mermaid ``` blocks

        6. Trade-offs & Limitations
        - Performance trade-offs
        - Cost trade-offs
        - Technical risks
        - Future scaling challenges

        7. Growth & Evolution Plan
        - How the system evolves at 10x scale
        - When to migrate to microservices
        - Future optimization points

        CRITICAL FORMATTING RULE:
        You MUST provide exactly ONE Mermaid diagram wrapped in ```mermaid and ``` blocks.
        Do not add text, explanations, or comments inside the backticks.
        If you do not include the diagram, the system will fail.
        
        Ensure the first line inside the block is 'graph TD' or 'graph LR'.

        --------------------------------------------------
        QUALITY RULES:

        - Be concise but technically precise
        - No vague statements
        - No marketing language
        - No unnecessary buzzwords
        - Prefer concrete examples
        - Assume the reader is a technical interviewer

        Always prioritize clarity, realism, and engineering correctness.
"""

    messages_to_send = [{"role": "system", "content": system_prompt}]
    messages_to_send.extend(history)
    messages_to_send.append({
        "role": "user", 
        "content": f"Update the architecture for Project: {plan_title} using this new research: {truncated_research}"
    })

    response = llm.invoke(messages_to_send)
    raw_content = response.content

    if "graph TD" not in raw_content and "graph LR" not in raw_content:
        #   Ask the LLM to just generate the missing diagram
        fix_prompt = "Your previous response was missing the Mermaid diagram. Please provide ONLY the Mermaid code block starting with 'graph TD' or 'graph LR' wrapped in ```mermaid blocks."
        retry_response = llm.invoke(raw_content + "\n\n" + fix_prompt)
        
        # Append the fix to the original report
        raw_content += "\n\n### Architecture Visual Update\n" + retry_response.content

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