from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket
from services.ai_assistant import ai_assistant
import streamlit as st
import pandas as pd
import plotly.express as px

#session state
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first")
    st.stop()

#role check for IT Operations
user_role = st.session_state.get("user_role", "").lower()
allowed_roles = ["admin", "it_admin"]

if user_role not in allowed_roles:
    st.error("Access restricted to IT Operations personnel")
    if st.button("Return to Dashboard Selector"):
        st.switch_page("pages/2_dashboard.py")
    st.stop()

#Page setup
st.set_page_config(layout="wide")
st.title(f"Welcome {st.session_state.username}, to IT_Operations")
st.header("Dashboard")

#sidebar navigation
st.sidebar.title("Navigation")

#displaying current role
role = st.session_state.get("user_role", "user")
st.sidebar.write(f"**Role:** {role.upper()}")
st.sidebar.write(f"**Current:** IT_Operations")

#log out button
if st.sidebar.button("Log out"):
    st.session_state.logged_in = False
    st.stop()

#retrieving data from tickets csv
try:
    db = DatabaseManager("intelligence_platform.db")

    # Retrieve data from DB
    rows = db.retrieve_all("SELECT * FROM it_tickets")

    # Convert rows to ITTicket objects
    tickets = []
    for row in rows:
        ticket = ITTicket(
            ticket_id=row['ticket_id'],
            priority=row['priority'],
            description=row['description'],
            status=row['status'],
            assigned_to=row['assigned_to'],
            created_at=row['created_at'],
            resolution_time_hours=row['resolution_time_hours'],
        )
        tickets.append(ticket)

    # Convert to DataFrame for visualizations
    tickets_df = pd.DataFrame([{
        'ticket_id': t.get_id(),
        'priority': t.get_priority(),
        'status': t.get_status(),
        'assigned_to': t.get_assigned_to(),
        'resolution_time_hours': t.get_resolution_time_hours()
    } for t in tickets])

except Exception as e:
    st.error(f"Database error: {e}")
    tickets = []
    tickets_df = pd.DataFrame()

#metrics
col1, col2, col3 = st.columns(3)
with col1: st.metric("Total tickets", len(tickets_df))
with col2: st.metric("Open tickets", len(tickets_df[tickets_df["status"] == "Open"]))
with col3:
    if 'resolution_time_hours' in tickets_df.columns:
        avg_res_time = tickets_df['resolution_time_hours'].mean()
        st.metric("Average resolution time", f"{avg_res_time:.1f} hours")
    else:
        st.metric("Average resolution time", 0)


#bar chart visual
st.subheader("Performance analytics")

#displaying ticket status distribution
status_counts = tickets_df['status'].value_counts()
diagram_1 = px.pie (values=status_counts.values, names=status_counts.index, title="Ticket Status Distribution")
st.plotly_chart(diagram_1)

#displaying active tickets
active_tickets = tickets_df[tickets_df['status'].isin(['Open', 'In Progress', 'Waiting for User'])]

if not active_tickets.empty:
    staff_counts = active_tickets['assigned_to'].value_counts()
    #ensuring IT_Support_C appears first if it has most
    staff_counts = staff_counts.sort_values(ascending=False)
    fig_staff = px.bar (x=staff_counts.index, y=staff_counts.values, title="Active Tickets by Staff", labels={'x': 'Staff Member', 'y': 'Active Tickets'}, color=staff_counts.values, color_continuous_scale='Reds')
    st.plotly_chart(fig_staff, use_container_width=True)

#displaying process Bottleneck Analysis
status_times = tickets_df.groupby('status')['resolution_time_hours'].mean().sort_values(ascending=False)
diagram_3 = px.bar (x=status_times.index, y=status_times.values, title="Average Time in Each Status", labels={'x': 'Status', 'y': 'Average Hours'}, color=status_times.values, color_continuous_scale='Greens')
st.plotly_chart(diagram_3)



#INSIGHTS SECTION
st.subheader("Staff Performance Analysis")

#providing tickets data for the AI to gain context
if not tickets_df.empty:
    #analysing staff performance
    staff_stats = tickets_df.groupby(['assigned_to']).agg({
        'ticket_id': 'count',
        'resolution_time_hours': 'mean'
    }).rename(columns={'ticket_id': 'ticket_count', 'resolution_time_hours': 'avg_resolution_hours'})

    status_times = tickets_df.groupby('status')['resolution_time_hours'].mean().sort_values(ascending=False)

    tickets_summary_data = f"""
    total tickets: {len(tickets_df)}
    open tickets: {len(tickets_df[tickets_df["status"] =="Open"])}
    average resolution time: {tickets_df['resolution_time_hours'].mean()}
    tickets waiting for user: {len(tickets_df[tickets_df["status"] =="Waiting for User"])}
    staff performance (slowest): {staff_stats.to_dict()}
    process bottlenecks: {status_times.to_dict()}
    """
else:
    tickets_summary_data = "No data available"

#crafting user input and ai answer generation
user_question = st.text_input("Ask anything IT related")
if user_question and st.button("Get answer"):
    with st.spinner("Gemini is thinking..."):
        try:
            #giving context data in AI response
            prompt = f"Real tickets data: {tickets_summary_data}\nUser question: {user_question}"
            response = ai_assistant.get_ai_insight(prompt)
            st.write(response)
        except Exception as e:
            st.error(str(e))

