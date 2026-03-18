import streamlit as st
from main import run

st.set_page_config(page_title="Email Automation", layout="centered")

st.title("📧 Email Automation Dashboard")

st.write("Fetch and process latest emails using AI")

if st.button("Fetch Emails"):
    st.write("Processing emails... please wait ⏳")

    run()

    st.success("✅ Emails processed and stored in Google Sheets!")