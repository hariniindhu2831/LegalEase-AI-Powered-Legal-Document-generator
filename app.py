import streamlit as st
import requests
import os
import sys

# Append parent directory to sys.path to import modules from utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.exporter import create_docx, create_pdf, create_txt

# Use explicit 127.0.0.1 IP address instead of localhost
BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="LegalEase - AI Legal Document Platform",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase AI")
st.caption("Generative AI Legal Document Drafting Platform")

# Sidebar configurations
st.sidebar.header("Document Configurations")
doc_type = st.sidebar.selectbox(
    "Select Agreement Type",
    [
        "Employment Contract",
        "Non-Disclosure Agreement (NDA)",
        "Lease Agreement",
        "Service Agreement",
        "Custom Legal Agreement"
    ]
)
effective_date = st.sidebar.date_input("Effective Date")

# Party Details Input Section
st.subheader("Party Details & Specific Provisions")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Party 1 (First Party)")
    p1_name = st.text_input("Name / Company Name", "TechCorp Inc.")
    p1_role = st.text_input("Role", "Employer")
    p1_addr = st.text_area("Address", "100 Innovation Way, CA")

with col2:
    st.markdown("### Party 2 (Second Party)")
    p2_name = st.text_input("Name / Individual", "Jane Smith")
    p2_role = st.text_input("Role", "Employee")
    p2_addr = st.text_area("Address", "45 Residence Ave, CA")

terms = st.text_area(
    "Key Terms & Conditions",
    height=150,
    value="Salary: $130,000 annually. Probation period: 90 days."
)

# Document Generation Trigger
if st.button("Generate Legal Document", type="primary", use_container_width=True):
    payload = {
        "doc_type": doc_type,
        "effective_date": str(effective_date),
        "parties": {
            "party1_name": p1_name,
            "party1_role": p1_role,
            "party1_address": p1_addr,
            "party2_name": p2_name,
            "party2_role": p2_role,
            "party2_address": p2_addr
        },
        "terms": terms
    }
    
    with st.spinner("Gemini is generating the document..."):
        try:
            res = requests.post(f"{BACKEND_URL}/api/v1/generate-document", json=payload)
            if res.status_code == 200:
                st.session_state["generated_doc"] = res.json()["generated_content"]
                st.success("Document Generated Successfully!")
            else:
                st.error(f"Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"Failed to connect to backend server: {str(e)}")

# Preview and Download Options
if "generated_doc" in st.session_state:
    st.markdown("---")
    st.subheader("Editable Document Preview")
    
    edited_doc = st.text_area(
        "Edit document text:",
        value=st.session_state["generated_doc"],
        height=400
    )
    
    st.markdown("### Download Options")
    col_pdf, col_docx, col_txt = st.columns(3)
    
    pdf_bytes = create_pdf(edited_doc)
    docx_bytes = create_docx(edited_doc)
    txt_bytes = create_txt(edited_doc)
    
    with col_pdf:
        st.download_button("📄 Download PDF", pdf_bytes, "document.pdf", "application/pdf")
    with col_docx:
        st.download_button("📝 Download DOCX", docx_bytes, "document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    with col_txt:
        st.download_button("📄 Download TXT", txt_bytes, "document.txt", "text/plain")

