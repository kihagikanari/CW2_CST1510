from services.database_manager import  DatabaseManager
from models.security_incident import SecurityIncident
from services.ai_assistant import ai_assistant
import streamlit as st
import pandas as pd
import plotly.express as px

#checking session state
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first")
    st.stop()

#role check for Cybersecurity
user_role = st.session_state.get("user_role", "").lower()
allowed_roles = ["admin", "cyber_analyst"]

if user_role not in allowed_roles:
    st.error("Access restricted to Cybersecurity personnel")
    if st.button("Return to Dashboard Selector"):
        st.switch_page("pages/2_dashboard.py")
    st.stop()

st.set_page_config(layout="wide")
st.title(f"Welcome, {st.session_state.username}!, to Cybersecurity")
st.header("Dashboard")

#sidebar navigation
st.sidebar.title("Navigation")

#displaying current role
role = st.session_state.get("user_role", "user")
st.sidebar.write(f"**Role:** {role.upper()}")
st.sidebar.write(f"**Current:** Cybersecurity")

#retreiving data from db
try:
    db = DatabaseManager("intelligence_platform.db")
    #retrieving data
    rows = db.retrieve_all("SELECT * FROM cyber_incidents")
    #converting all rows to objects
    incidents = []
    for row in rows:
        incident = SecurityIncident(
            incident_id=row['incident_id'],
            category=row['category'],
            severity=row['severity'],
            status=row['status'],
            description=row.get('description', ''),
            timestamp=row['timestamp']
        )
        incidents.append(incident)

    # Converting to Dataframe for visualizations
    incidents_df = pd.DataFrame([{
        'incident_id': inc.get_id(),
        'category': inc.get_category(),
        'severity': inc.get_severity(),
        'status': inc.get_status(),
        'timestamp': inc.get_timestamp(),
    } for inc in incidents])

except Exception as e:
    st.error(f"Database error: {e}")
    incidents = []
    incidents_df = pd.DataFrame()

#metrics
if incidents:
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Total incidents", len(incidents))
    with col2:
        critical_count = sum(1 for inc in incidents if inc.is_critical())
        st.metric("Critical/High", critical_count)

    with col3:
        open_count = sum(1 for inc in incidents if inc.get_status() == 'Open')
        st.metric("Open", open_count)

    #bar chart visual
    severity_counts = incidents_df['severity'].value_counts()
    fig_bar = px.bar (x=severity_counts.index, y=severity_counts.values, title="Incidents by Severity", labels={'x': 'Severity Level', 'y': 'Number of Incidents'}, color=severity_counts.values, color_continuous_scale='Purples')
    st.plotly_chart(fig_bar, use_container_width=True)

    #scatter plot
    if 'timestamp' in incidents_df.columns and not incidents_df.empty:
        incidents_df['date_part'] = pd.to_datetime(incidents_df['timestamp']).dt.date
        incidents_by_date = incidents_df.groupby('date_part').size().reset_index(name='count')
        fig_time = px.scatter(incidents_by_date, x="date_part", y="count", title="incidents over time")
        st.plotly_chart(fig_time, use_container_width=True)

    #data table
    st.dataframe(incidents_df, use_container_width=True)

#log out button
if st.sidebar.button("Log out"):
    st.session_state.logged_in = False
    st.stop()

#INSIGHTs and AI SECTION
st.subheader("Threat Trend Analysis")

#providing incident data for AI to gain context
if not incidents_df.empty:
    #summary of actual data
    incident_summary_data = f"""
    Total Incidents: {len(incidents_df)}
    Severity Distribution: {incidents_df['severity'].value_counts().to_dict()}
    Status Breakdown: {incidents_df['status'].value_counts().to_dict()}
    Threat Categories: {incidents_df['category'].value_counts().head(5).to_dict() if 'category' in incidents_df.columns else 'N/A'}
    """
else:
    incident_summary_data = "No incident data available"

#crafting user input and ai answer generation
user_question = st.text_input("Ask anything cybersecurity related")
if user_question and st.button("Get answer"):
    with st.spinner("Gemini is thinking..."):
        try:
            #ai assistant OOP refactored
            prompt = f"Real incident data: {incident_summary_data}\nUser question: {user_question}"
            response = ai_assistant.get_ai_insight(prompt)
            st.write(response)
        except Exception as e:
            st.error(f"Gemini Ai service error: {str(e)}")