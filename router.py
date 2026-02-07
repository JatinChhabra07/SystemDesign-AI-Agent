from langgraph.graph import END

def routing_logic(state):
    """
    1. Handles Self-Healing (if score is low)
    2. Routes to the correct Agent based on the Plan
    3. Ends the process when steps are done
    """
    plan = state["plan"]
    step_idx = state["current_step"]

    # 1. Self-Healing: If the Validator (we'll add this next) fails the design
    if state.get("eval_score", 10) < 7:
        print("--- ROUTING: RE-EXECUTING DUE TO LOW SCORE ---")
        return "architect" # Send back to fix it

    # 2. End of Plan: If no more steps, go to the Reporter or End
    if step_idx >= len(plan.steps):
        print("--- ROUTING: PLAN COMPLETE ---")
        return END

    # 3. Dynamic Routing: Look at the next step's role in the plan
    next_step = plan.steps[step_idx]
    role = next_step.agent_role

    if role == "Research":
        return "researcher"
    elif role in ["Design", "Execution", "Validation"]:
        return "architect"
    
    return END