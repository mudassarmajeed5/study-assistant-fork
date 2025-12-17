from google import genai
from dotenv import load_dotenv
import os
from streamlit_javascript import st_javascript

load_dotenv()


api_key = os.getenv("SECRET_SECRET_KEY")
client = genai.Client(api_key=api_key)

def get_summary(text_extracted):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""Summarize the following text as structured notes, similar to a README.md file. 
        The summary should cover every concept and key point from the content, and be organized 
        with sections, headers, and bullet points where applicable. Make sure the explanation is clear 
        and concise, and use a simple format for easy readability. For each concept, include:
        
        1. A brief title or heading
        2. A short description or summary
        3. Any important points, facts, or examples in bullet points (if applicable)
        
        Format the output in Markdown style so that it can be rendered easily in a UI like Streamlit.
        
        Text to summarize:

{text_extracted}""",
    )


    print(response.text)
    return response.text



def generate_quiz(extracted_text):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Generate a multiple-choice quiz from the following:
        {extracted_text}
        Output rules (follow strictly):
        - Output ONLY a valid JSON array.
        - NO markdown.
        - NO backticks.
        - NO commentary.
        - NO explanation before or after the JSON.
        - Do NOT wrap JSON in ```json``` or any code fences.
        - The output **must be directly parsable JSON**.
        Each quiz item must follow this exact structure:
        [
        {{
            "question": "string",
            "options": {{
            "A": "string",
            "B": "string",
            "C": "string",
            "D": "string"
            }},
            "correct_option": "A" | "B" | "C" | "D",
            "answer_explanation": "string"
        }}
        ]
        Constraints:
        - Exactly 4 options: A, B, C, D.
        - The array may contain multiple quiz items upto 10.
        """
    )

    if not response.text:
        return "Gemini Model returned None/Null"

    return response.text.strip()

def generate_flashcards(extracted_text):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Generate a flashcards from the following:
        {extracted_text}
        Output rules (follow strictly):
        - Output ONLY a valid JSON array.
        - NO markdown.
        - NO backticks.
        - NO commentary.
        - NO explanation before or after the JSON.
        - Do NOT wrap JSON in ```json``` or any code fences.
        - The output **must be directly parsable JSON**.
        Each quiz item must follow this exact structure:
        [
        {{
            "question": "string",
            "answer": "string"
        }}
        ]
        """
    )
    if not response.text:
        return "Gemini Model returned None/Null"

    return response.text.strip()
