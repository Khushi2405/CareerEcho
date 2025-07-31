import streamlit as st

st.set_page_config(page_title="Edit Selected Post")

st.title("📝 Edit Your Selected Post")
print("Session State in edit_page:", st.session_state)
if "selected_post" not in st.session_state:
    st.warning("No post selected. Please go back to the input page and choose one.")
    st.stop()

# Editable text area with pre-filled selected post
edited_text = st.text_area(
    "✍️ You can edit your post below:",
    value=st.session_state["selected_post"],
    height=300
)

# Save button
if st.button("✅ Save Final Version"):
    st.session_state["final_post"] = edited_text
    st.success("Your final post has been saved!")

# Navigation button to go back to input page
if st.button("🔙 Back to Input Page"):
    st.session_state.page = "input"
    st.switch_page("pages/input_page.py")
