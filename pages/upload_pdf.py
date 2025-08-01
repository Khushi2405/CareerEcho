import streamlit as st
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

st.set_page_config(page_title="Resume PDF Upload", layout="centered")

st.title("Upload Your Resume in PDF format (we promise not to store it anywhere!)")

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
uploaded_file = st.file_uploader("Upload your Resume", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully!")
    
    # Optionally display the PDF content
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    prompt = (f"""
        You are an expert resume reviewer. You will assume the role based on resume content and
        suggest improvements to the resume to better match the role. Use only the content
        provided in the resume to generate your suggestions. Don't make up any information.
        Make sure to keep the suggestions concise and relevant. More importantly focus on
        -Education
        -Experience
        -Skills
        -Projects
        -No buzzwords
        -includes important keywords
        Here is the resume content:
        <resume>
                    {text}
        </resume>
        Return only the suggestions using \\n for new lines. Do not include any text other than the actual suggestions.
    """)
    with st.spinner("Generating feedback..."):
        result = llm.invoke(prompt)
        st.write("Suggestions for improving your resume:")
        st.write(result.content.strip())

    
