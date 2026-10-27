import streamlit as st


def render_upload_section():
    st.header("1. Upload Tender Document")

    tender_file = st.file_uploader(
        "Upload tender PDF, DOCX, or TXT",
        type=["pdf", "docx", "txt"]
    )

    st.header("2. Upload Bidder Evidence Documents")

    evidence_files = st.file_uploader(
        "Upload supporting documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    return tender_file, evidence_files
