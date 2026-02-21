import os 
from google import genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "models/gemini-2.0-flash"

@st.cache_data
def generate_topic_title(keywords): 
    prompt = f"""
Convert the following topic keywords into a short , professional dashboard title. 
Rules :
Create a SHORT (3–5 word) neutral topic label based ONLY on the keywords. Do not infer additional context.
KEYWORDS:{keywords}

Return ONLY the title.

"""

    response = client.models.generate_content(model=MODEL , contents=prompt , config={'temperature': 0.2 , "max_output_tokens":20})
    return response.text.strip()





def generate_topic_name(keywords: list[str], max_words: int = 4) -> str:
    return " / ".join(keywords[:max_words]).title()

