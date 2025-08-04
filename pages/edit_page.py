import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
st.set_page_config(page_title="Edit Selected Post")
st.title("📝 Edit Your Selected Post")

if "selected_post" not in st.session_state:
    st.warning("No post selected. Please go back to the input page and choose one.")
    st.stop()

if "edited_text" not in st.session_state:
    st.session_state.edited_text = st.session_state["selected_post"]

def refine_post_on_click():
    with st.spinner("Refining your post with AI..."):

        system_prompt = f"""
        You are a helpful assistant that helps refines LinkedIn posts created by AI.
        This was the prompt used to generate the post:
        Topic: {st.session_state.get("prompt", "")}
        Use this prompt to refine the post.
        Your task is to improve the post while keeping the original intent and content.
        If the user has provided any [PERSON] names, keep them as is.
        Return only the posts using \\n for new lines. Do not include any text other than the actual post and it should be clearly formatted for LinkedIn."
        """
        if user_prompt:
            system_prompt += f"\nUser wants to refine the post with the following instruction: {user_prompt}\n"

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Here's the post to refine:\n{edited_text}")
        ]

        try:
            response = llm.invoke(messages)
            refined_post = response.content.strip()
            st.session_state.edited_text = refined_post
        except Exception as e:
            print(f"Error invoking refining linkedin post LLM: {e}")
            if "429" in str(e): 
                st.error("Rate limit exceeded. Please try again later.")
            else:
                st.error("An error occurred while generating feedback. Please try again later.")

# Editable text area with pre-filled selected post
edited_text = st.text_area(
    "✍️ You can edit your post below:",
    value=st.session_state.edited_text,
    height=300
)

# Optional refinement prompt
user_prompt = st.text_input(
    "💬 Optional instruction to refine the post (e.g. 'make it shorter', 'add excitement')",
    placeholder="Leave blank to simply improve the current version."
)

# Refine with AI button
st.button("🤖 Refine with AI", on_click=refine_post_on_click)
# Save button
if st.button("✅ Save Final Version"):
    st.session_state["final_post"] = edited_text
    st.success("Your final post has been saved!")

# Navigation button to go back to input page
if st.button("🔙 Back to Input Page"):
    st.session_state.page = "input"
    if "edited_text" in st.session_state:
        del st.session_state["edited_text"]
    st.switch_page("pages/input_page.py")
