import streamlit as st

from ui.upload_section import render_upload_section
from ui.report_section import render_report_section
from utils.text_extractor import extract_text_from_file
from engine.clause_extractor import extract_clauses
from engine.scorer import calculate_results

st.set_page_config(page_title="Tenderly", page_icon="📄", layout="wide")

st.title("📄 Tenderly")
st.subheader("AI-Based Government Tender Eligibility & Evidence Matching System")

st.markdown("""
Upload a tender document and bidder evidence documents.
Tenderly will extract eligibility clauses, match evidence,
calculate an eligibility score, and generate a gap report.
""")

tender_file, evidence_files = render_upload_section()

if st.button("Run Eligibility Check", type="primary"):
    if not tender_file:
        st.error("Please upload a tender document.")
        st.stop()

    if not evidence_files:
        st.error("Please upload at least one evidence document.")
        st.stop()

    try:
        with st.spinner("Extracting tender text..."):
            tender_text = extract_text_from_file(tender_file)
            clauses = extract_clauses(tender_text)
    except Exception as error:
        st.error(f"Could not process tender: {error}")
        st.stop()

    with st.spinner("Extracting evidence text..."):
        evidence_documents = []

        for evidence_file in evidence_files:
            try:
                evidence_text = extract_text_from_file(evidence_file)
                if evidence_text.strip():
                    evidence_documents.append({
                        "name": evidence_file.name,
                        "text": evidence_text
                    })
            except Exception:
                st.warning(f"Could not read file: {evidence_file.name}")

    if not evidence_documents:
        st.error("No readable text found in evidence documents.")
        st.stop()

    with st.spinner("Matching clauses with evidence..."):
        results_df, eligibility_score, verdict = calculate_results(
            clauses, evidence_documents
        )

    st.success("Eligibility check completed.")
    render_report_section(results_df, eligibility_score, verdict)
