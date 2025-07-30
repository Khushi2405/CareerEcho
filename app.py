import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os, json
import re

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

st.set_page_config(page_title="LinkedIn Post Generator")
st.title("💼 LinkedIn Post Assistant")

# Free-form input fields
topic_input = st.text_input(
    "🧠 What is your post about?",
    placeholder="e.g. Building my first AI agent project"
)

type_input = st.text_input(
    "🗂️ What type of post are you making?",
    placeholder="e.g. Project announcement, personal story, career tip"
)

tone_input = st.text_input(
    "🎭 What tone do you want?",
    placeholder="e.g. Excited, humble, informative, inspirational, formal, casual"
)

audience_input = st.text_input(
    "🎯 Who is your target audience?",
    placeholder="e.g. Recruiters, students, hiring managers, general public"
)

include_hashtags = st.checkbox("Add relevant hashtags to the post?", value=False)
if include_hashtags:
    hashtags_input = st.text_input(
        "🔖 Any specific hashtags to include?",
        placeholder="e.g. #AI #MachineLearning #CareerGrowth")
include_emojis = st.checkbox("Add emojis to make the post more expressive?", value=False)


def extract_structured(fields_dict):
    user_combined = (
        f"Topic: {fields_dict['topic']}. "
        f"Post type: {fields_dict['post_type']}. "
        f"Tone: {fields_dict['tone']}. "
        f"Audience: {fields_dict['audience']}."
    )
    # # Extraction prompt
    # extraction_prompt = f"""
    #     You are an assistant that normalizes user‑provided text into clean structured fields.
    #     Input: "{user_combined}"
    #     Produce JSON:
    #     {{"topic":"...", "post_type":"...", "tone":"...", "audience":"..."}}
    # """
    # resp = llm.invoke(extraction_prompt)
    # try:
    #     print(json.loads(resp.content))
    #     return json.loads(resp.content)
    # except json.JSONDecodeError:
    #     return None
    return {
        "topic": fields_dict["topic"],
        "post_type": fields_dict["post_type"],
        "tone": fields_dict["tone"],
        "audience": fields_dict["audience"]
    }

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
            # Clean prompt for generating the post
            clean_prompt = (
                f"Write 3 different versions of a {structured['tone']} LinkedIn {structured['post_type']} "
                f"targeted at {structured['audience']} about: {structured['topic']}. "
                f"{hashtag_text} "
                f"{'Include' if include_emojis else 'Do not include'} emojis. "
                f"Return only the posts as a JSON array of strings, with each post using \\n for new lines. Do not include any text outside the JSON block. Each post should be clearly formatted for LinkedIn."
            )
            with st.spinner("Generating post..."):
                result = llm.invoke(clean_prompt)
            posts = parse_multiple_posts(result.content)
            print(f"Generated posts: {posts}")
            st.subheader("✍️ Generated Post Variations")
            for i, post in enumerate(posts, 1):
                st.markdown(f"### Post {i}")
                st.write(post)
                st.markdown("---")
            st.caption("🔁 Edit inputs or refine prompt above to regenerate.")
