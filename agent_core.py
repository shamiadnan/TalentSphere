import google.generativeai as genai
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

# --- 1. Define State ---
class AgentState(TypedDict):
    resume_text: str
    role: str
    history: List[dict]
    step_count: int
    latest_response: str
    analysis: str

# --- 2. Define Tools & Nodes ---
def get_model():
    return genai.GenerativeModel('gemini-1.5-flash')

def analyzer_node(state: AgentState):
    model = get_model()
    
    # Analyze Resume
    analysis_prompt = f"""
    Role: {state['role']}
    Resume: {state['resume_text']}
    
    Task: Identify 3 missing skills and 1 main strength. Output a concise summary.
    """
    try:
        analysis = model.generate_content(analysis_prompt).text
    except:
        analysis = "Analysis complete."

    # Generate First Greeting
    greeting_prompt = f"""
    Context: Interview for {state['role']}.
    Resume Analysis: {analysis}
    
    Task: Greet the candidate professionally by name. Mention their strength. Ask the first technical question.
    """
    greeting = model.generate_content(greeting_prompt).text
    
    return {
        "history": [{"role": "user", "parts": [greeting_prompt]}, {"role": "model", "parts": [greeting]}],
        "step_count": 1,
        "latest_response": greeting,
        "analysis": analysis
    }

def interviewer_node(state: AgentState):
    model = get_model()
    chat = model.start_chat(history=state['history'])
    
    prompt = f"""
    Step: {state['step_count']}/4.
    Instructions:
    1. Acknowledge the user's answer.
    2. Ask the next technical question.
    3. If Step 4, say "Interview Complete".
    """
    response = chat.send_message(prompt)
    
    return {
        "history": chat.history,
        "step_count": state['step_count'] + 1,
        "latest_response": response.text
    }

def reporting_node(state: AgentState):
    model = get_model()
    chat = model.start_chat(history=state['history'])
    prompt = "Generate a JSON report: {score_0_to_10, verdict, feedback}"
    response = chat.send_message(prompt)
    return {"latest_response": response.text}

# --- 3. Build Graph ---
def build_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("interviewer", interviewer_node)
    workflow.add_node("reporter", reporting_node)
    workflow.set_entry_point("analyzer")
    return workflow.compile()
