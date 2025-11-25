from google import genai
from dotenv import load_dotenv
import os


load_dotenv()


api_key = os.getenv("SECRET_SECRET_KEY")
client = genai.Client(api_key=api_key)

promp_2 = "What is your name"
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
        contents=f"""Generate a multiple-choice quiz based on the following text {extracted_text}. Each question should have 4 options (A, B, C, D), and you should include the correct answer with an explanation. The format of the response should be in JSON, and the structure should contain the following fields for each question:

- `QUESTION`: The quiz question based on the text.
- `ANSWER (EXPLANATION)`: The correct answer, along with an explanation of why it's correct.
- `CORRECT OPTION`: The letter corresponding to the correct answer (A, B, C, or D).
- `USER_OPTION`: This field should be left empty initially (for user to fill in later with their choice, e.g., "A", "B", etc.).

Ensure the questions cover the main concepts and important details from the provided text. The output should be a valid JSON array of objects with these fields:

```json
[
    {
        "QUESTION": "What is the main idea of the passage?",
        "ANSWER": "The passage discusses the importance of environmental sustainability.",
        "CORRECT OPTION": "A",
        "USER_OPTION": ""
    },
    {
        "QUESTION": "What is the primary cause of deforestation according to the text?",
        "ANSWER": "The text attributes deforestation to industrial expansion and urbanization.",
        "CORRECT OPTION": "C",
        "USER_OPTION": ""
    },
    ...
]
"""
    )
    print(response.text)
    return response.text