# 💼 TalentSphere – Intelligent Interview & Growth System  

> Empowering confident hiring and personal growth through autonomous agents powered by Google Gemini.  

---

## 🧠 Overview
**TalentSphere** is an autonomous multi-agent interviewer and personal skill coach that reads your resume, asks role-based technical questions, evaluates your performance, and generates a personalized 4-week improvement plan.  

It’s designed for **Kaggle AI Agent Hackathon 2025** and showcases how multiple AI agents can collaborate to assess, train, and upskill users intelligently.  

🌍 Live App URL: https://calligraphic-eufemia-unliberalised.ngrok-free.dev

---

## ✨ Key Features
- 🤖 **Recruiter Agent** — Reads résumé, analyzes skills, and asks relevant technical questions.  
- 🧠 **Trainer Agent** — Evaluates each answer’s clarity, confidence, and structure with JSON-based scoring.  
- 📊 **Evaluator Agent** — Generates a final report with technical, communication, and confidence scores.  
- 🚀 **Improvement Planner Agent** — Builds a 4-week personalized skill growth plan.  
- 🔊 **Text-to-Speech Support** — Converts feedback to professional voice using Google TTS.  
- 🧩 **Simple Streamlit Interface** — Clean and responsive interview dashboard.  

---

## 🧩 Tech Stack
- **Frontend:** Streamlit  
- **Core Intelligence:** Google Gemini (Generative AI API)  
- **Agents:** Custom-built Recruiter, Trainer, Evaluator & Improvement Planner  
- **Utilities:** PyPDF2 for résumé parsing, gTTS for audio feedback  
- **Deployment:** Ngrok (for temporary hosting)  

---
## ⚙️ Installation  

``bash
# Clone the repository
git clone https://github.com/shamiadnan/TalentSphere.git
cd TalentSphere

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

---
## 🧭 How It Works
---

Upload your résumé (PDF)

Recruiter Agent extracts key skills and experience

Trainer Agent conducts a role-based interview

Evaluator Agent scores your answers (clarity, confidence, accuracy)

Improvement Planner Agent builds your 4-week learning roadmap

## 🧠 Future Enhancements

Persistent dashboard for performance tracking

Emotion and speech tone recognition

Multi-language interview support

Personalized upskilling recommendations

## 👤 Author

Adnan Shami

## 🧡 Acknowledgements

Special thanks to Google AI Studio, Kaggle, and the Gemini API community for enabling next-gen agentic systems.
