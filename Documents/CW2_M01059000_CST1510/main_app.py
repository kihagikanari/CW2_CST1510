import streamlit as st

#page structure
st.set_page_config(page_title="Multi Intelligence platform", layout="centered")

#session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("Multi Intelligence platform")

#redirection if not logged in
if not st.session_state.logged_in:
    st.info("use the sidebar on the left to log in")
else:
    st.success(f"Welcome back, {st.session_state.username}!")
    st.switch_page("pages/Dashboard.py")