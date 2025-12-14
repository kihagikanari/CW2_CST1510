import streamlit as st
from services.auth_manager import AuthManager

#STORE AuthManager in session state (persists across pages)
if "auth_manager" not in st.session_state:
    st.session_state.auth_manager = AuthManager()

auth_manager = st.session_state.auth_manager

#Also store registered users count to detect changes
if "user_count" not in st.session_state:
    st.session_state.user_count = len(auth_manager.users) if auth_manager.users else 0

#session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None

#title
st.title("Multi Intelligence platform")
st.markdown("\n" + "=" * 70)

#creating login and register tabs with respective inputs and messages
tab_login, tab_register = st.tabs(["login", "register"])

with tab_login:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Please enter username and password!")
        else:
            #authmanager use for login
            user = auth_manager.login(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.username = user.get_username()
                st.session_state.user_role = user._role
                st.success(f"Welcome, {user.get_username()}, ({user._role})!")
                st.switch_page("pages/2_dashboard.py")
            else:
                st.error("Invalid username or password!")

with tab_register:
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    #role selection
    role = st.selectbox("Select Role", ["cyber_analyst", "it_admin", "data_analyst", "admin"])

    if st.button("Register"):
        if not new_username or not new_password:
            st.error("Please enter both the username and password!")
        elif new_password != confirm_password:
            st.error("Entered passwords don't match!")
        else:
            #authmanager use for registering
            success = auth_manager.register(new_username, new_password, role)
            if success:
                #Update user count in session state
                st.session_state.user_count = len(auth_manager.users)

                #Auto-login after registration
                st.session_state.logged_in = True
                st.session_state.username = new_username
                st.session_state.user_role = role

                st.success(f"Registered as {role}! Logging you in...")
                st.switch_page("pages/2_dashboard.py")
            else:
                st.error("Username already exists!")

