import streamlit as st

#checking session state
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first")
    st.stop()

st.title("🏠 Dashboard Selector")
st.write(f"Welcome, **{st.session_state.get('username', 'User')}**")
st.write(f"**Role:** {st.session_state.get('user_role', 'user').upper()}")

#getting user role
user_role = st.session_state.get("user_role", "user")

st.markdown("---")

#admin privileges
if user_role == "admin":
    st.success("👑 **Administrator Access**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔒 Cybersecurity", use_container_width=True):
            st.switch_page("pages/Cybersecurity.py")
    with col2:
        if st.button("📊 Data Science", use_container_width=True):
            st.switch_page("pages/Data_Science.py")
    with col3:
        if st.button("🖥️ IT Operations", use_container_width=True):
            st.switch_page("pages/IT_Operations.py")

#cybersecurity user
elif user_role == "cyber_analyst":
    st.info("🔒 **Cybersecurity Analyst**")
    if st.button("Go to Cybersecurity Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/Cybersecurity.py")

#IT operations user
elif user_role == "it_admin":
    st.info("🖥️ **IT Administrator**")
    if st.button("Go to IT Operations Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/IT_Operations.py")

#Data science user
elif user_role == "data_analyst":
    st.info("📊 **Data Scientist**")
    if st.button("Go to Data Science Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/Data_Science.py")


#logout button
st.markdown("---")
if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.stop()