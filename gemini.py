from google import genai

client = genai.Client(api_key="AIzaSyBnHXZMP6scAPQ3eReL5qd4vhS5ZeJK_6E")

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