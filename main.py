# main.py
import streamlit as st

st.set_page_config(page_title="LinkedIn Post Assistant", layout="centered", initial_sidebar_state="collapsed")
print("Session State in main:", st.session_state)

if "page" not in st.session_state:
    st.session_state.page = "input"

if st.session_state.page == "input":
    st.switch_page("pages/input_page.py")
elif st.session_state.page == "edit":
    st.switch_page("pages/edit_page.py")


# if "selected_post" in st.session_state and st.session_state.selected_post:
#     with st.spinner("Loading editor..."):
#         st.switch_page("pages/edit_page.py")
# else:
#     with st.spinner("Loading..."):
#         st.switch_page("pages/input_page.py")