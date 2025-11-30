import os
import json
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import PyPDF2
from openai import OpenAI

# Initialize Models
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
client = OpenAI()

# --- TOOL: Resume Parser ---
def extract_text_from_pdf(pdf_path):
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return "Error reading PDF."

# --- TOOL: Text-to-Speech (The "Voice") ---
def text_to_speech(text):
    """Generates audio from text using OpenAI"""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        output_path = "output_audio.mp3"
        response.stream_to_file(output_path)
        return output_path
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

# --- STATE DEFINITION ---
class InterviewState(TypedDict):
    resume_text: str
    role: str
    messages: List[Annotated[str, "messages"]] # Chat History
    step_count: int
    feedback: str

# --- NODE 1: INITIALIZE INTERVIEW ---
def init_node(state: InterviewState):
    print("--- PARSING RESUME ---")
    # 1. Analyze Resume
    prompt = f"""
    You are an expert Tech Recruiter.
    Role: {state['role']}
    Resume: {state['resume_text'][:2000]}
    
    Start the interview. Greet the candidate by name (if found) and ask the FIRST technical question based on their skills.
    Keep it conversational and short.
    """
    response = llm.invoke([SystemMessage(content=prompt)])
    return {
        "messages": [response],
        "step_count": 1
    }

# --- NODE 2: INTERVIEW LOOP ---
def interview_node(state: InterviewState):
    print("--- CONDUCTING INTERVIEW ---")
    
    # Get the last user answer
    last_user_msg = state['messages'][-1]
    
    prompt = f"""
    Role: {state['role']}
    Resume Context: {state['resume_text'][:1000]}
    Current Step: {state['step_count']}/3
    
    The user just answered: "{last_user_msg.content}"
    
    If step_count < 3:
        Acknowledge their answer briefly and ask the NEXT technical question.
    If step_count >= 3:
        Thank them and say "That concludes our interview. I will generate your report now."
    """
    
    response = llm.invoke(state['messages'] + [SystemMessage(content=prompt)])
    return {
        "messages": [response],
        "step_count": state['step_count'] + 1
    }

# --- NODE 3: SCORING ---
def scoring_node(state: InterviewState):
    print("--- SCORING CANDIDATE ---")
    
    # Analyze the whole conversation
    conversation_text = "\n".join([m.content for m in state['messages']])
    
    prompt = f"""
    Analyze this interview transcript for the role of {state['role']}.
    Transcript: {conversation_text}
    
    Output a JSON with:
    1. Score (0-10)
    2. Verdict (Hire/No Hire)
    3. Key Strengths
    4. Weaknesses
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"feedback": response.content}

# --- GRAPH CONSTRUCTION ---
def build_graph():
    workflow = StateGraph(InterviewState)
    
    workflow.add_node("init", init_node)
    workflow.add_node("interview_loop", interview_node)
    workflow.add_node("score", scoring_node)
    
    workflow.set_entry_point("init")
    
    # Logic: If user replies, go back to loop. If step > 3, score.
    # Note: In Streamlit, we handle the 'User Reply' interruption manually in the UI code.
    # This graph defines the logic for *generating the AI response*.
    
    return workflow.compile()
