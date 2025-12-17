import streamlit as st
import re
from io import BytesIO
from PyPDF2 import PdfReader
import markdown2
from xhtml2pdf import pisa
from helpers.ai_models import get_summary
from tempfile import NamedTemporaryFile


def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Configure page
st.set_page_config(page_title="Home - AI Study Assistant", page_icon="🏠")

# Main content
st.title("🏠 Upload PDF/PPTX")
st.subheader("Upload your study materials to get started")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
file_name = uploaded_file.name if uploaded_file else "No file uploaded"

if uploaded_file is None:
    st.warning("Please upload a PDF file to proceed.")
else:
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
        else:
            with st.spinner("Generating summary..."):
                summary = get_summary(text_to_summarize)
                if not summary: 
                    summary = "Summary not available."
            
            st.success("Summary generated!")
            
            code_block_match = re.search(
            r'```(?:markdown|readme)?\s*(.*?)\s*```',
            summary,
            re.DOTALL | re.IGNORECASE
            )
            if code_block_match:
                cleaned_summary = code_block_match.group(1).strip()
            else:
                cleaned_summary = summary
                
            st.session_state["summary"] = cleaned_summary
            st.markdown(cleaned_summary)

if "summary" in st.session_state:
    st.markdown("---")
    st.markdown("### Current Summary")
    st.markdown(st.session_state["summary"])
    
    # Generate PDF for download
    html_content = markdown2.markdown(st.session_state["summary"])
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        pisa.CreatePDF(html_content, dest=temp_pdf)
        temp_pdf.seek(0)
        pdf_data = temp_pdf.read()
    st.download_button(
        label="📄 Download Summary as PDF",
        data=pdf_data,
        file_name=f"{file_name}_Summary.pdf",
        mime="application/pdf"
    )