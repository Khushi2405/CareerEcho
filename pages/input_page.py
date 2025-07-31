import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json
import re

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

if "selected_post" not in st.session_state:
    st.session_state.selected_post = None


st.title("💼 LinkedIn Post Assistant")
# Initialize session state with defaults if missing
st.session_state._topic_input = st.session_state.get("topic_input", "")
st.session_state._type_input = st.session_state.get("type_input", "")
st.session_state._tone_input = st.session_state.get("tone_input", "")
st.session_state._audience_input = st.session_state.get("audience_input", "")  
st.session_state._include_hashtags = st.session_state.get("include_hashtags", False)
st.session_state._hashtags_input = st.session_state.get("hashtags_input", "")
st.session_state._include_emojis = st.session_state.get("include_emojis", False)
st.session_state._version_input = st.session_state.get("version_input", "3")



def store_value(key):
    st.session_state[key] = st.session_state["_"+key]


# Free-form input fields
topic_input = st.text_input(
    "🧠 What is your post about?",
    key="_topic_input",
    placeholder="e.g. Building my first AI agent project",
    on_change=lambda: store_value("topic_input")
)

type_input = st.text_input(
    "🗂️ What type of post are you making?",
    key="_type_input",
    placeholder="e.g. Project announcement, personal story, career tip",
    on_change=lambda: store_value("type_input")
)

tone_input = st.text_input(
    "🎭 What tone do you want?",
    key="_tone_input",
    placeholder="e.g. Excited, humble, informative, inspirational, formal, casual",
    on_change=lambda: store_value("tone_input")
)

audience_input = st.text_input(
    "🎯 Who is your target audience?",
    key="_audience_input",
    placeholder="e.g. Recruiters, students, hiring managers, general public",
    on_change=lambda: store_value("audience_input")
)

include_hashtags = st.checkbox(
    "Add relevant hashtags to the post?", 
    key="_include_hashtags",
    on_change=lambda: store_value("include_hashtags")
)
if include_hashtags:
    hashtags_input = st.text_input(
        "🔖 Any specific hashtags to include?",
        key="_hashtags_input",
        placeholder="e.g. #AI #MachineLearning #CareerGrowth",
        on_change=lambda: store_value("hashtags_input")
    )
    
include_emojis = st.checkbox(
    "Add emojis to make the post more expressive?", 
    key="_include_emojis",
    on_change=lambda: store_value("include_emojis")
)

version_input = st.text_input(
    "Enter number of post variations to generate(1-10):",
    key="_version_input",
    on_change=lambda: store_value("version_input")
)

def extract_structured(fields_dict):
    user_combined = (
        f"Topic: {fields_dict['topic']}. "
        f"Post type: {fields_dict['post_type']}. "
        f"Tone: {fields_dict['tone']}. "
        f"Audience: {fields_dict['audience']}."
    )
    prompt = (
        "You are an expert in extracting only relevant information from any text",
        "Extract structured information from the following user input:\n"
        f"{user_combined}\n\n"
        "Return a JSON object with the following keys:\n"
        "- topic: The main topic of the post\n"
        "- post_type: The type of post (e.g. announcement, story, tip)\n"
        "- tone: The desired tone of the post (e.g. excited, humble)\n"
        "- audience: The target audience for the post (e.g. recruiters, students)\n"
        "Ensure the output is a valid JSON object with no additional text."
    )
    response = llm.invoke(prompt)
    
    extracted_response = re.sub(r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", response.content).strip()
    print(f"Structured extraction response: {extracted_response}")
    try:
        structured = json.loads(extracted_response)
        if isinstance(structured, dict) and all(key in structured for key in ["topic", "post_type", "tone", "audience"]):
            return structured
        else:
            print("Invalid structured output:", structured)
            return None
    except json.JSONDecodeError:
        print("JSON decoding error:", extracted_response)
        return None

def parse_multiple_posts(response_text):
    response_text = re.sub(r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", response_text).strip()
    print(f"Raw response: {response_text}")
    
    try:
        # Expecting JSON array: ["post 1 text", "post 2 text", "post 3 text"]
        posts = json.loads(response_text)
        if isinstance(posts, list):
            return posts
        return [response_text]
    except json.JSONDecodeError:
        # If not JSON, fallback to single post
        return [response_text]

if st.button("Generate Post"):
    if not topic_input.strip():
        st.warning("Topic is required.")
    else:
        with st.spinner("Extracting inputs..."):
            structured = extract_structured({
                "topic": topic_input,
                "post_type": type_input,
                "tone": tone_input,
                "audience": audience_input
            })
            print(structured)
        if not structured:
            st.error("Couldn't parse inputs—please simplify and try again.")
        else:
            hashtag_text = ""
            if include_hashtags:
                if hashtags_input.strip():
                    hashtag_text = (
                        f"Include these hashtags at the end of the post: {hashtags_input.strip()}. "
                        "Also, suggest 2-3 more relevant hashtags to add."
                    )
                else:
                    hashtag_text = "Include relevant hashtags at the end of the post."
            else:
                hashtag_text = "Do not add any hashtags."

            num_variations = version_input.strip()
            if not num_variations.isdigit() or not (1 <= int(num_variations) <= 10):
                st.warning("Please enter a valid number of variations (1-10). Defaulting to 3.")
                num_variations = "3"
            # Clean prompt for generating the post
            clean_prompt = (
                f"Write {num_variations} different versions of a {structured['tone']} LinkedIn {structured['post_type']} "
                f"targeted at {structured['audience']} about: {structured['topic']}. "
                f"{hashtag_text} "
                f"{'Include' if include_emojis else 'Do not include'} emojis. "
                f"Return only the posts as a JSON array of strings, with each post using \\n for new lines. Do not include any text outside the JSON block. Each post should be clearly formatted for LinkedIn."
            )
            with st.spinner("Generating post..."):
                result = llm.invoke(clean_prompt)
            posts = parse_multiple_posts(result.content)
            st.session_state.generated_posts = posts

if "generated_posts" in st.session_state and st.session_state.generated_posts:
    st.subheader("✍️ Choose a Version to Edit")
    posts = st.session_state.generated_posts
    for i, post in enumerate(posts):
        if st.button("Test print", key=f"Test_{i}"):
            st.success(f"Selected post {i+1}!")
            print("Button pressed!")

        if st.button(f"Select Post {i+1}", key=f"select_post_{i}"):
            st.session_state.selected_post = post
            st.session_state.page = "edit"
            # store_value()
            print("Session State in input:", st.session_state)
            st.switch_page("pages/edit_page.py")
        st.text_area(f"Post {i+1}", post, height=200)
        st.markdown("---")
