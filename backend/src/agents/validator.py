from backend.src.utils.model_config import get_model


def validator_agent(state:dict):
    """Reviews the design and provides a score + feedback."""
    llm = get_model()

    architecture_design = state["messages"][-1].content

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
            {"role":"system", "content": system_prompt},
            {"role": "user", "content": f"Review This Architecture: {architecture_design}"}
        ]
    )

    content = response.content
    try:
        import re
        match = re.search(r"SCORE: (\d+)/10", content)
        eval_score = int(match.group(1) if match else 7)
    except:
        eval_score=7 # Default if parsing fails

    return{
        "message": [
            {"role": "assistant", "content": f"Validation Feedback: {content}"}
        ],
        "eval_score": eval_score,
        "current_step": state["current_step"] +1
    }
