import os
from google import genai
from backend.templates import build_legal_prompt

GEMINI_API_KEY = "AQ.Ab8RN6LSYYX04jKnVaBNhMfrRy5N_q7IRaSsoiPQAj0K3iz-pg"
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_document_from_gemini(doc_type: str, parties: dict, terms: str, effective_date: str) -> str:
    prompt = build_legal_prompt(doc_type, parties, terms, effective_date)
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text
