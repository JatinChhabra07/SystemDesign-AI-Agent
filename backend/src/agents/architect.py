from src.utils.model_config import get_model
from src.utils.utils import sanitize_mermaid
import re


def architect_agent(state: dict):
    """
    Drafts and evolves the technical architecture based on research
    and previous system designs.
    """

    llm = get_model()

    plan_title = state["plan"].title if "plan" in state else "System Architecture"

    messages = state.get("messages", [])


    full_history_text = ""
    for m in messages:
        m_content = m.get("content", "") if isinstance(m, dict) else getattr(m, "content", "")
        if "```mermaid" in m_content:
            full_history_text = m_content


    history = messages[-2:] if len(messages) >= 2 else messages

    last_message = history[-1] if history else ""

    if isinstance(last_message, dict):
        research_data = last_message.get("content", "")
    else:
        research_data = getattr(last_message, "content", str(last_message))

    truncated_research = str(research_data)[:1500]

    truncated_previous = str(full_history_text)[:1000]


    system_prompt = f"""
        You are a Principal System Architect with 15+ years of real-world experience
        in designing scalable, reliable, and cost-efficient software systems.

        PREVIOUS DESIGN (if any):
        {truncated_previous}

        NEW RESEARCH:
        {truncated_research}

        TASK:
        You MUST provide the COMPLETE, UPDATED system architecture.

        If a previous design exists:
        - Preserve all valid components
        - Integrate new features cleanly
        - Refactor when needed
        - Do NOT remove working parts without justification

        Your goal is NOT to impress with complexity.
        Your goal is to build the RIGHT system for the use case.

        --------------------------------------------------
        CORE PRINCIPLES (MANDATORY):

        1. Avoid generic templates.
        2. Include ONLY justified components.
        3. Prefer simplicity when possible.
        4. Introduce advanced infra ONLY if needed.
        5. For every major component:
        - Explain WHY chosen
        - Explain WHY alternatives rejected
        6. Justify omitted components.
        7. Optimize for:
        - Performance
        - Cost
        - Maintainability
        - Scalability
        - Reliability

        --------------------------------------------------
        ANALYSIS REQUIREMENTS:

        Before proposing the architecture, analyze:
        - Expected traffic
        - Data volume
        - Read/write patterns
        - Latency
        - Availability
        - Budget

        --------------------------------------------------
        OUTPUT FORMAT (STRICT):

        1. Title
        2. System Overview
        3. Architecture Design (With Justification)
        4. Data Management Strategy
        5. Mermaid Architecture Diagram (REQUIRED)
        6. Trade-offs & Limitations
        7. Growth & Evolution Plan

        --------------------------------------------------
        MERMAID RULES (CRITICAL):

        - Provide EXACTLY ONE Mermaid diagram
        - Wrap inside ```mermaid ``` blocks
        - First line MUST be: graph TD or graph LR
        - Must represent the FULL integrated system
        - No comments inside diagram
        - No extra diagrams

        If diagram is missing → system fails.

        --------------------------------------------------

        STRICT TECHNICAL CONSTRAINTS:
        1. If the user specifies a technology (e.g., PostgreSQL, Flink), you MUST use it.
        2. Do NOT use generic alternatives like Neptune or Glue if specific tools are requested.
        3. Architecture MUST be integrated. Show how User Profiles and Tracking data flow into the SAME database.
        4. Mermaid diagrams must be CONNECTED (Graph TD). No isolated blocks.


        QUALITY RULES:

        - No vague language
        - No buzzwords
        - No marketing tone
        - Interview-level clarity
        - Engineering-first thinking

        Always prioritize realism and correctness.
    """
    messages_to_send = [{"role": "system", "content": system_prompt}]
    messages_to_send.extend(history)

    feedback = ""
    if "Validation Feedback" in str(history):
        feedback = f"\n\nPREVIOUS FEEDBACK: Your last design was rejected. Fix the following: {research_data}"

    messages_to_send.append({
    "role": "user", 
    "content": f"Update the architecture for Project: {plan_title}. {feedback} Research: {truncated_research}"
})

    response = llm.invoke(messages_to_send)
    raw_content = response.content

    if "graph TD" not in raw_content and "graph LR" not in raw_content:
        #   Ask the LLM to just generate the missing diagram
        fix_prompt = "Your previous response was missing the Mermaid diagram. Please provide ONLY the Mermaid code block starting with 'graph TD' or 'graph LR' wrapped in ```mermaid blocks."
        retry_response = llm.invoke(raw_content + "\n\n" + fix_prompt)
        
        raw_content += "\n\n### Architecture Visual Update\n" + retry_response.content

    # Extract and sanitize the mermaid block
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