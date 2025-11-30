import google.generativeai as genai
from gtts import gTTS
import tempfile, io
from PyPDF2 import PdfReader

def configure_gemini(api_key: str):
    genai.configure(api_key=api_key)

def extract_pdf_text(uploaded_file) -> str:
    """Extracts text locally so we only send TEXT to the model (no file API)."""
    try:
        data = uploaded_file.getvalue()
        reader = PdfReader(io.BytesIO(data))
        text = "\n".join([(p.extract_text() or "") for p in reader.pages]).strip()
        # compact for context
        if len(text) > 12000:
            text = text[:6000] + "\n...\n" + text[-5800:]
        return text
    except Exception as e:
        print("Text Extraction Error:", e)
        return ""

def google_text_to_speech(text: str):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        return tmp.name
    except Exception as e:
        print("TTS Error:", e)
        return None
