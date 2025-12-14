import streamlit as st

#page structure
st.set_page_config(page_title="Multi Intelligence platform", layout="wide")

#session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title(" --- Welcome to the Multi Intelligence platform --- ")
st.markdown("\n" + "=" * 198)

#redirection if not logged in
if not st.session_state.logged_in:
    st.info("kindly use the sidebar on the left to log in, see you in there!🫵")
    st.markdown("\n" + "=" * 198)
else:
    st.switch_page("pages/2_dashboard.py")