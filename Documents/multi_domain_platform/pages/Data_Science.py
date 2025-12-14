import streamlit as st
import plotly.express as px
from app.data.datasets import get_all_datasets
from database.db import connect_database
from services.ai_assistant import ai_assistant

#checking session state
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first")
    st.stop()

#role check for IT Operations
user_role = st.session_state.get("user_role", "").lower()
allowed_roles = ["admin", "data_analyst"]

if user_role not in allowed_roles:
    st.error("Access restricted to Data Science personnel")
    if st.button("Return to Dashboard Selector"):
        st.switch_page("pages/2_dashboard.py")
    st.stop()

#page setup
st.set_page_config(layout="wide")
st.title(f"Welcome {st.session_state.username}, to Data Science")
st.header("Dashboard")

#sidebar navigation
st.sidebar.title("Navigation")

#show current role
role = st.session_state.get("user_role", "user")
st.sidebar.write(f"**Role:** {role.upper()}")
st.sidebar.write(f"**Current:** Data science")

#log out button
if st.sidebar.button("Log out"):
    st.session_state.logged_in = False
    st.stop()

#retrieving data
try:
    conn = connect_database("intelligence_platform.db")
    datasets_df = get_all_datasets(conn)
except Exception as e:
    st.error(f"data unavailable{e}")

#showing data table
if not datasets_df.empty:
    st.dataframe(datasets_df, use_container_width=True)

#INSIGHTS SECTION
st.subheader("Dataset Governance Analysis")

#providing dataset data for the AI to gain context
if not datasets_df.empty:
    #Analyzing dataset governance
    source_stats = datasets_df.groupby(['uploaded_by']).agg({
        'dataset_id': 'count',
        'rows': 'sum',
        'columns': 'mean'
    }).rename(columns={'dataset_id': 'dataset_count', 'columns': 'avg_columns'})

    #Calculating estimated size
    datasets_df['estimated_size_mb'] = (datasets_df['rows'] * datasets_df['columns'] * 8) / (1024 * 1024)
    size_by_source = datasets_df.groupby('uploaded_by')['estimated_size_mb'].sum().to_dict()

    #Finding largest datasets
    largest_datasets = datasets_df.nlargest(3, 'rows')[['name', 'rows', 'uploaded_by']].to_dict('records')

    datasets_summary_data = f"""
    Total datasets: {len(datasets_df)}
    Total rows across all datasets: {datasets_df['rows'].sum():,}
    Average rows per dataset: {datasets_df['rows'].mean():.0f}
    Upload distribution by user: {source_stats.to_dict()}
    Estimated storage by user (MB): {size_by_source}
    Largest datasets (by rows): {largest_datasets}
    """
else:
    datasets_summary_data = "No dataset data available"

#visuals
if not datasets_df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Datasets", len(datasets_df))
    with col2:
        st.metric("Total Rows", f"{datasets_df['rows'].sum():,}")
    with col3:
        total_mb = datasets_df['estimated_size_mb'].sum()
        st.metric("Estimated Storage", f"{total_mb:.1f} MB")

    #displaying datasets by uploader
    uploader_counts = datasets_df['uploaded_by'].value_counts()
    fig1 = px.bar(
        x=uploader_counts.index,
        y=uploader_counts.values,
        title="Datasets by Uploader",
        labels={'x': 'Uploader', 'y': 'Number of Datasets'},
        color=uploader_counts.values,
        color_continuous_scale='Purples')
    st.plotly_chart(fig1, use_container_width=True)

    #displaying rows by uploader
    rows_by_uploader = datasets_df.groupby('uploaded_by')['rows'].sum()
    fig2 = px.pie (values=rows_by_uploader.values, names=rows_by_uploader.index, title="Total Rows by Uploader",)
    st.plotly_chart(fig2, use_container_width=True)

#AI ASSISTANT SECTION
st.subheader("AI Assistant")

#crafting user input and ai answer generation
user_question = st.text_input("Ask about anythng data science related")
if user_question and st.button("Get answer"):
    with st.spinner("Gemini is thinking..."):
        try:
            prompt = f"Dataset governance data: {datasets_summary_data}\nUser question: {user_question}"
            response = ai_assistant.get_ai_insight(prompt)
            st.write(response)
        except Exception as e:
            st.error(f"AI service error: {str(e)}")