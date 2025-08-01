# main.py
import streamlit as st

st.set_page_config(page_title="LinkCraft", layout="centered", initial_sidebar_state="collapsed")

st.title("🔗 CareerEcho")
st.subheader("Your career, reflected and amplified")

st.write("Choose what you'd like to do:")

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Upload & Review Resume"):
        st.session_state.page = "review"
        st.switch_page("pages/upload_pdf.py")

with col2:
    if st.button("✍️ Generate LinkedIn Post"):
        st.session_state.page = "post"
        st.switch_page("pages/input_page.py")
