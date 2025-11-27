import streamlit as st

#session state
if "registered" not in st.session_state:
    st.session_state.registered = True
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "admin123",
        "user": "user123",
        "jon": "jon123",
    }
#title
st.title("Multi Intelligence platform")
st.markdown("\n" + "=" * 70)

#creating login and register tabs with respective inputs and messages
tab_login, tab_register = st.tabs(["login", "register"])

with tab_login:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("You have successfully logged in!")
            st.switch_page("pages/Dashboard.py")
        else:
            st.session_state.logged_in = False
            st.error("Invalid username or password!, try again.")

with tab_register:
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not new_username or not new_password:
            st.error("Please enter both the username and password!")
        elif new_password != confirm_password:
            st.error("Entered passwords don't match!")
        elif new_username in st.session_state.users:
            st.error("That username already exists!")
        else:
            st.session_state.users[new_username] = new_password
            st.success("You have successfully registered!")
            st.info("You can now log in with your new account.")

