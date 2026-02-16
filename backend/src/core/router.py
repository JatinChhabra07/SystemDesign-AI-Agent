from langgraph.graph import END

def routing_logic(state):
    """
    Final Robust Router:
    - Case-insensitive role mapping.
    - Strict Loop Prevention (Max 2 retries).
    - Intelligent State Progression.
    """
    plan = state.get("plan")
    step_idx = state.get("current_step", 0)
    eval_score = state.get("eval_score", 10)
    messages = state.get("messages", [])

    # Check specifically for validation feedback keywords in assistant messages
    retry_count = 0
    for m in messages:
        content = m.get("content", "") if isinstance(m, dict) else getattr(m, "content", "")
        if "Validation Feedback" in content or "Validation Report" in content:
            retry_count += 1

    if not plan:
        print("--- ROUTING: NO PLAN FOUND ---")
        return END

    if eval_score < 7:
        if retry_count < 2: 
            print(f"--- SELF-HEALING: Score {eval_score}/10. Attempt {retry_count + 1}. Routing to Architect... ---")
            return "architect"
        else:
            print(f"--- LOOP PREVENTION: Max retries ({retry_count}) hit. Forcing Exit. ---")
            return END

    if step_idx >= len(plan.steps):
        print("--- ROUTING: ALL STEPS EXECUTED ---")
        return END

    # 5. DYNAMIC ROLE ROUTING
    next_step = plan.steps[step_idx]
    role = next_step.agent_role.lower()

    print(f"--- ROUTING: Current Step {step_idx + 1}/{len(plan.steps)}, Role: {role} ---")

    if "research" in role:
        return "researcher"
    
    if any(r in role for r in ["architect", "design", "execution", "structure"]):
        return "architect"
    
    if "validation" in role or "validator" in role:
        return "validator"
    
    # Fallback to END if role is unknown to prevent infinite hanging
    print(f"--- ROUTING: Unknown role '{role}', terminating gracefully. ---")
    return END