# main.py
import streamlit as st

st.set_page_config(page_title="CareerEcho", layout="centered", initial_sidebar_state="collapsed")

st.title("🔗 CareerEcho")
st.subheader("Your career, reflected and amplified")

st.write("Choose what you'd like to do:")

# Create three columns for the three main features
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Upload & Review Resume", use_container_width=True):
        st.session_state.page = "review"
        st.switch_page("pages/upload_pdf.py")

with col2:
    if st.button("✍️ Generate LinkedIn Post", use_container_width=True):
        st.session_state.page = "post"
        st.switch_page("pages/input_page.py")

with col3:
    if st.button("📚 Create Study Cheatsheet", use_container_width=True):
        st.session_state.page = "cheatsheet"
        st.switch_page("pages/cheatsheet_page.py")

# Add feature descriptions
# st.markdown("---")
# st.markdown("### Features:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    - Upload your PDF resume
    - Get targeted feedback
    - Role-specific suggestions
    - Keyword optimization
    """)

with col2:
    st.markdown("""
    - Generate engaging posts
    - Multiple variations
    - AI-powered editing
    - Customizable tone & style
    """)

with col3:
    st.markdown("""
    - Create comprehensive guides
    - Any subject or topic
    - Downloadable PDF format
    - Multiple difficulty levels
    """)