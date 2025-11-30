import google.generativeai as genai
import json

# ----- model state -----
_MODEL_ID = None

def set_model_id(mid: str):
    """Called by the UI after you pick a model from the dropdown."""
    global _MODEL_ID
    _MODEL_ID = mid

def list_supported_models():
    """Return (id, label) for models that support generateContent."""
    out = []
    for m in genai.list_models():
        methods = getattr(m, "supported_generation_methods", []) or []
        if "generateContent" in methods:
            # Prefer the full resource name if present
            out.append(m.name)
    # Keep unique and sorted, most human-friendly last part
    out = sorted(set(out), key=lambda s: s.split("/")[-1])
    return out

def get_model():
    if not _MODEL_ID:
        raise RuntimeError("Model not selected. Call set_model_id() first.")
    return genai.GenerativeModel(_MODEL_ID)

# ---------- Recruiter (text only) ----------
def recruiter_agent(role, resume_text="", candidate_intro=""):
    model = get_model()
    ctx = resume_text or candidate_intro or "No context provided."
    sys = (f"You are a recruiter for {role}. "
           "Greet the candidate by name if available from the résumé and ask the FIRST technical question "
           "tailored to their skills. Keep it concise and specific.")
    prompt = f"{sys}\n\nRésumé/Context:\n{ctx}"
    return model.generate_content(prompt).text

def recruiter_followup(role, candidate_answer, step):
    model = get_model()
    prompt = (
        f"Candidate answered: {candidate_answer}\n"
        f"Current Step: {step}/4.\n"
        "If step < 4: acknowledge, then ask the next deeper technical question based on their résumé.\n"
        "If step == 4: thank them and say 'Interview Complete'. Keep it concise."
    )
    return model.generate_content(prompt).text

# ---------- Trainer (communication JSON) ----------
def trainer_agent(role, candidate_answer):
    model = get_model()
    prompt = (
      f"You are a personal interview trainer for the role {role}. "
      "Evaluate the candidate's answer for clarity, confidence, structure (STAR) and tone. "
      "Return ONLY valid minified JSON with this schema:\n"
      '{"clarity":0,"confidence":0,"structure":0,"tone":0,'
      '"praise":[],"improvements":[],"drill":""}\n'
      f"Answer: {candidate_answer}"
    )
    out = model.generate_content(prompt).text
    try:
        return json.loads(out)
    except:
        return {"raw_output": out}

# ---------- Evaluator (final report JSON) ----------
def evaluator_agent(chat_history):
    model = get_model()
    conversation = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history][-12000:])
    prompt = (
      "Evaluate the candidate based on the conversation.\n"
      "Return ONLY valid minified JSON exactly matching:\n"
      '{"candidate_name":"",'
      '"technical_score":0,"communication_score":0,"confidence_score":0,'
      '"overall":0,"strengths":[],"improvements":[],"verdict":""}\n'
      f"Conversation:\n{conversation}"
    )
    out = model.generate_content(prompt).text
    try:
        return json.loads(out)
    except:
        return {"raw_output": out}

# ---------- Improvement Plan (skills gap + 4-week plan JSON) ----------
def improvement_plan_agent(role, chat_history, resume_text_snippet=""):
    model = get_model()
    convo = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history][-6000:])
    prompt = (
      f"You are a senior mentor creating a skills-gap report and a 4-week plan for a {role} candidate.\n"
      "Use the resume/context and conversation to infer strengths and gaps.\n"
      "Return ONLY valid minified JSON with this schema:\n"
      '{"skills_gaps":[],'
      '"recommended_courses":[],'
      '"practice_projects":[],'
      '"daily_drills":[],'
      '"week_by_week_plan":[{"week":1,"focus":"","tasks":[]},{"week":2,"focus":"","tasks":[]},{"week":3,"focus":"","tasks":[]},{"week":4,"focus":"","tasks":[]}]}'
      f"\nResume/context:\n{resume_text_snippet}\n\nConversation:\n{convo}"
    )
    out = model.generate_content(prompt).text
    try:
        return json.loads(out)
    except:
        return {"raw_output": out}
