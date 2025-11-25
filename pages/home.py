import streamlit as st
import re
from io import BytesIO
from PyPDF2 import PdfReader
import markdown2
from weasyprint import HTML
from gemini import get_summary


def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


def render_home():
    """Render the Home page content."""
    st.title("Upload PDF/PPTX")
    st.subheader("Upload your study materials to get started")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    file_name = uploaded_file.name if uploaded_file else "No file uploaded"
    if uploaded_file is None:
        st.warning("Please upload a PDF file to proceed.")
        return

    uploaded_name = getattr(uploaded_file, "name", None)
    if (
        "extracted_text" not in st.session_state
        or st.session_state.get("last_uploaded_name") != uploaded_name
    ):
        with st.spinner("Extracting text from PDF..."):
            st.session_state["extracted_text"] = extract_text_from_pdf(uploaded_file)
            st.session_state["last_uploaded_name"] = uploaded_name
        st.success("Text extraction complete!")

    st.markdown("---")
    st.info("PDF uploaded and text extracted. Click the button below to generate a summary.")

    if st.button("Generate Summary"):
        text_to_summarize = st.session_state.get("extracted_text", "")
        if not text_to_summarize:
            st.warning("No extracted text available to summarize.")
            return
        with st.spinner("Generating summary..."):
            summary = get_summary(text_to_summarize)
        
        st.success("Summary generated!")
        st.markdown("### Summary")
        
        # Extract and store summary
        code_block_match = re.search(r'```(?:markdown|readme)?\s*(.*?)\s*```', summary, re.DOTALL | re.IGNORECASE)
        if code_block_match:
            cleaned_summary = code_block_match.group(1).strip()
        else:
            cleaned_summary = summary
            
        st.session_state["summary"] = cleaned_summary
        st.markdown(cleaned_summary)
        
    if "summary" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state["summary"])
        
        # Generate PDF for download
        html_content = markdown2.markdown(st.session_state["summary"])
        pdf_buffer = BytesIO()
        HTML(string=html_content).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)
        
        st.download_button(
            label="📄 Download Summary as PDF",
            data=pdf_buffer,
            file_name=f"{file_name}_Summary.pdf",
            mime="application/pdf"
        )
