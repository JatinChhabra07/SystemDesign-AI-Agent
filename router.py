
def routing_logic(state):
    """
    Decides: 
    1. Do we need more research? 
    2. Is the design ready for validation?
    3. Did the validator fail the design (Self-Healing)?
    """
    
    # Self-Healing Logic: If the Validator gave a low score
    if state.get("eval_score", 10) < 7:
        print("--- ROUTING: RE-EXECUTING DUE TO LOW SCORE ---")
        return "execution_agent" # Send back to fix it
        
    # Flow Logic: Check if there are more steps in the plan
    if state["current_step"] < state["plan"].total_steps:
        return "research_agent"
        
    return "reporter_agent"