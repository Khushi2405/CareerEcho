import streamlit as st
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

st.set_page_config(page_title="Resume PDF Upload", layout="centered")

st.title("Review your Resume")

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
uploaded_file = st.file_uploader("Upload your Resume in PDF format (we promise not to store it anywhere!)", type=["pdf"])

# Add input field for role
role = st.text_input("Enter the role you are targeting for (e.g., Data Scientist, Software Engineer)")

review_button = st.button(
    "Review Resume",
    disabled=not (uploaded_file)
)

if review_button:
    if not role:
        st.error("Please enter a role to review your resume.")
        st.stop()
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    prompt = (
        f"You are an expert resume reviewer and interviewer for the position of '{role}'.\n"
        "First, determine if the provided content is a resume. If not, reply: \"This PDF does not appear to be a resume.\" and briefly explain why.\n"
        f"Next, check if the role '{role}' matches the resume content. If not, reply: \"The role '{role}' does not seem to match the content of the resume. Please check the role and try again.\"\n"
        "If it is a resume and the role matches, provide concise, actionable suggestions to improve the resume for the '{role}' role. Only use information from the resume; do not fabricate details.\n"
        "Add suggestions to include important keywords relevant to the role.\n"
        "Add suggestions to remove buzzwords and make it more impactful.\n"
        "Focus your feedback on:\n"
        "- Education\n"
        "- Experience\n"
        "- Skills\n"
        "- Projects\n"
        "Here is the resume content:\n"
        "<resume>\n"
        f"{text}\n"
        "</resume>\n"
        "Return only the suggestions, using \\n for new lines. Do not include any text other than the suggestions or the message about the PDF not being a resume."
    )
    with st.spinner("Generating feedback..."):
        try:
            result = llm.invoke(prompt)
            st.write(f"Suggestions for improving your resume for the '{role}' role:")
            st.write(result.content.strip())
        except Exception as e:
            print(f"Error invoking upload pdf LLM: {e}")
            if "429" in str(e): 
                st.error("Rate limit exceeded. Please try again later.")
            else:
                st.error("An error occurred while generating feedback. Please try again later.")

    
