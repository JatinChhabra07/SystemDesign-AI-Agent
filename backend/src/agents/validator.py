from src.utils.model_config import get_model
import re


def validator_agent(state: dict):
    """
    Reviews the system design using LLM + rule-based validation.
    Provides score, feedback, and updates workflow state.
    """

    llm = get_model()


    last_message = state["messages"][-1]

    if isinstance(last_message, dict):
        architecture_design = last_message.get("content", "")
    else:
        architecture_design = getattr(
            last_message,
            "content",
            str(last_message)
        )

    if not architecture_design.strip():

        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": "Validation failed: Empty architecture design."
                }
            ],
            "eval_score": 0,
            "current_step": state["current_step"] + 1
        }


    system_prompt = """
You are a Principal Systems Reviewer with extensive experience evaluating
large-scale distributed systems in production environments.

Your task is to critically review the proposed system architecture and identify
technical risks, weaknesses, and hidden failure points.

Follow these rules strictly:

1. Analyze the design across the following dimensions:
- Scalability (horizontal/vertical scaling, bottlenecks, load handling)
- Security (authentication, authorization, data protection, attack surfaces)
- Fault Tolerance (redundancy, failover, disaster recovery, resilience)

2. For each dimension:
- Identify concrete weaknesses
- Explain why they are risky
- Provide actionable improvement suggestions

3. Highlight any missing components, unrealistic assumptions, or cost risks.

4. Evaluate the design as if it will be deployed to millions of users.

5. Be objective, skeptical, and technically rigorous.
Do not provide generic praise.

6. Use clear headings and bullet points for readability.

7. Avoid vague language. Every claim must be justified.

8. After completing the review, assign a final numerical score.

IMPORTANT:
You MUST end your response in exactly this format:

SCORE: X/10

(where X is an integer from 1 to 10)
"""

    response = llm.invoke(
        [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Review This Architecture:\n\n{architecture_design}"
            }
        ]
    )

    content = response.content


    try:
        match = re.search(r"SCORE:\s*(\d+)/10", content)
        eval_score = int(match.group(1)) if match else 7
    except Exception:
        eval_score = 7 


    # Penalize if Mermaid diagram missing
    if "```mermaid" not in architecture_design.lower():
        eval_score = 6 
    else:
        eval_score = 8

    print(f"--- VALIDATOR: Design Scored {eval_score} ---")


    return {
        "messages": [
            {
                "role": "assistant",
                "content": f"Validation Feedback:\n\n{content}"
            }
        ],
        "eval_score": eval_score,
        "current_step": state["current_step"] + 1
    }
