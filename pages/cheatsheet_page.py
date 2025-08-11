# pages/cheatsheet_page.py
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import re

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

st.title("📚 Study Cheatsheet Generator")

# Initialize session state
if "generated_cheatsheet" not in st.session_state:
    st.session_state.generated_cheatsheet = None

# Main input fields
topic = st.text_input(
    "📖 What topic do you want to create a cheatsheet for?",
    placeholder="e.g., Python Data Structures, Linear Algebra, Machine Learning"
)

difficulty_level = st.selectbox(
    "📊 Difficulty Level",
    ["Beginner", "Intermediate", "Advanced"]
)

cheatsheet_type = st.selectbox(
    "📋 Cheatsheet Type",
    ["Quick Reference", "Formula Sheet", "Concept Overview", "Step-by-Step Guide", "Comprehensive Review"]
)

length = st.selectbox(
    "📏 Content Length",
    ["Short (1-2 pages)", "Medium (2-4 pages)", "Long (4-6 pages)"]
)

# Additional requirements
custom_requirements = st.text_area(
    "💬 Additional requirements (optional)",
    placeholder="e.g., Focus on interview questions, Include common pitfalls, Emphasize practical applications",
    height=80
)

def create_cheatsheet_requirements(inputs):
    """Structure the cheatsheet requirements"""
    return {
        'topic': inputs['topic'].strip(),
        'difficulty_level': inputs['difficulty_level'],
        'cheatsheet_type': inputs['cheatsheet_type'],
        'length': inputs['length'],
        'custom_requirements': inputs['custom_requirements'].strip() if inputs['custom_requirements'] else ""
    }

def generate_cheatsheet_content(requirements):
    """Generate the cheatsheet content using AI"""
    
    # Create the prompt
    prompt = f"""You are an expert in creating study cheatsheets.
    Create a {requirements['difficulty_level'].lower()} level cheatsheet for '{requirements['topic']}'. 
This should be a {requirements['cheatsheet_type'].lower()} with {requirements['length'].lower()} content.

Content requirements:
- Include: core concepts only
- Well-organized with clear sections and headings
- Use bullet points and numbered lists for easy scanning
- Make it comprehensive but concise for quick reference
- Format using markdown with clear structure"""

    if requirements['custom_requirements']:
        prompt += f"\n- Special focus: {requirements['custom_requirements']}"
    
    prompt += "\n\nReturn only the cheatsheet content formatted in clean markdown."
    
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        if "429" in str(e):
            st.error("Rate limit exceeded. Please try again later.")
        else:
            st.error("An error occurred while generating the cheatsheet. Please try again later.")
        return None

def create_pdf(markdown_content, filename="cheatsheet.pdf"):
    """Convert markdown content to PDF with proper formatting"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        textColor=colors.darkblue,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=12,
        textColor=colors.darkgreen
    )
    
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=8,
        textColor=colors.darkred
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=10,
        leftIndent=20,
        backgroundColor=colors.lightgrey,
        spaceAfter=6,
        spaceBefore=6
    )
    
    def clean_text(text):
        """Clean and format markdown text for PDF"""
        # Handle bold text **text** -> <b>text</b>
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        # Handle italic text *text* -> <i>text</i>
        text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
        
        # Handle inline code `code` -> <font name="Courier">code</font>
        text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)
        
        # Clean up any remaining markdown artifacts
        text = text.replace('```', '')
        
        return text
    
    # Parse markdown content
    lines = markdown_content.split('\n')
    in_code_block = False
    
    for line in lines:
        original_line = line
        line = line.strip()
        
        # Handle empty lines
        if not line:
            story.append(Spacer(1, 6))
            continue
        
        # Handle section dividers
        if line.startswith('---'):
            story.append(Spacer(1, 12))
            continue
            
        # Handle code blocks
        if line.startswith('```'):
            in_code_block = not in_code_block
            continue
            
        if in_code_block:
            story.append(Paragraph(clean_text(original_line), code_style))
            continue
        
        # Handle headers
        if line.startswith('# '):
            story.append(Paragraph(clean_text(line[2:]), title_style))
        elif line.startswith('## '):
            story.append(Paragraph(clean_text(line[3:]), heading_style))
        elif line.startswith('### '):
            story.append(Paragraph(clean_text(line[4:]), subheading_style))
        elif line.startswith('#### '):
            story.append(Paragraph(clean_text(line[5:]), subheading_style))
        
        # Handle bullet points with proper indentation
        elif line.startswith('• ') or line.startswith('- ') or line.startswith('* '):
            bullet_text = clean_text(line[2:])
            story.append(Paragraph(f"• {bullet_text}", bullet_style))
        
        # Handle numbered lists
        elif re.match(r'^\d+\.', line):
            story.append(Paragraph(clean_text(line), styles['Normal']))
        
        # Handle regular text
        else:
            cleaned_line = clean_text(line)
            if cleaned_line:
                story.append(Paragraph(cleaned_line, styles['Normal']))
    
    try:
        doc.build(story)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"Error creating PDF: {e}")
        return None

# Generate button
if st.button("📝 Generate Cheatsheet", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic for your cheatsheet.")
    else:
        requirements = create_cheatsheet_requirements({
            'topic': topic,
            'difficulty_level': difficulty_level,
            'cheatsheet_type': cheatsheet_type,
            'length': length,
            'custom_requirements': custom_requirements
        })
        
        with st.spinner("Generating your cheatsheet..."):
            cheatsheet_content = generate_cheatsheet_content(requirements)
            
            if cheatsheet_content:
                st.session_state.generated_cheatsheet = cheatsheet_content
                st.session_state.cheatsheet_topic = topic

# Display generated cheatsheet
if st.session_state.generated_cheatsheet:
    st.success("✅ Cheatsheet generated successfully!")
    
    st.markdown(st.session_state.generated_cheatsheet)
    
    # Action buttons section
    st.markdown("---")
    pdf_buffer = create_pdf(
        st.session_state.generated_cheatsheet,
        f"{st.session_state.get('cheatsheet_topic', 'cheatsheet').replace(' ', '_')}.pdf"
    )
    
    if pdf_buffer:
        st.download_button(
            label="📄 Download PDF",
            data=pdf_buffer.getvalue(),
            file_name=f"{st.session_state.get('cheatsheet_topic', 'cheatsheet').replace(' ', '_')}.pdf",
            mime="application/pdf",
            type="primary"
        )

# Back button
st.markdown("---")
if st.button("🔙 Back to Home"):
    st.switch_page("main.py")