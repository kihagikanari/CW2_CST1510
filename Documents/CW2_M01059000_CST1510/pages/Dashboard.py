from app.data.db import connect_database
from app.data.incidents import get_all_incidents
import streamlit as st
import pandas as pd
import plotly.express as px

#connecting database
conn = connect_database("intelligence_platform.db")

#session state
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first")
    st.stop()

#Page setup
st.set_page_config(layout="wide")
st.title(f"Welcome, {st.session_state.username}!")

#retrieving data
try:
    conn = connect_database("intelligence_platform.db")
    incidents_df = get_all_incidents(conn)

except Exception as e:
    st.error(f"Database error: {e}")
    incidents_df = pd.DataFrame()

#Primary domain (cybersecurity) with metrics
if not incidents_df.empty:
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Total incidents", len(incidents_df))
    with col2: st.metric("Critical", len(incidents_df[incidents_df['severity'] == 'CRITICAL']))
    with col3: st.metric("Open", len(incidents_df[incidents_df['status'] == 'OPEN']))

    #bar chart visual
    fig_bar = px.bar(incidents_df['severity'].value_counts(), title="incidents by severity")
    st.plotly_chart(fig_bar, use_container_width=True)

    #scatter plot
    if 'timestamp' in incidents_df.columns and not incidents_df.empty:
        incidents_df['date_part'] = pd.to_datetime(incidents_df['timestamp']).dt.date
        incidents_by_date = incidents_df.groupby('date_part').size().reset_index(name='count')
        fig_time = px.scatter(incidents_by_date, x="date_part", y="count", title="incidents over time")
        st.plotly_chart(fig_time, use_container_width=True)

    #Data table
    st.dataframe(incidents_df, use_container_width=True)

#log out button
if st.sidebar.button("Log out"):
    st.session_state.logged_in = False
    st.switch_page("main_app.py")