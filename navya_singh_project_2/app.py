import os
import streamlit as st

from crew import create_analytics_crew

st.set_page_config(
    page_title="AI Delegation Analytics Assistant",
    layout="wide"
)

st.title(" AI Delegation Analytics Assistant")

st.write(
    "Upload a CSV dataset and ask an analytics or machine learning question."
)

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

user_request = st.text_area(
    "Ask your question",
    placeholder="Example: Analyze my sales dataset and recommend KPIs."
)

if st.button("Analyze"):

    if uploaded_file is None:
        st.error("Please upload a CSV file.")
        st.stop()

    if user_request.strip() == "":
        st.error("Please enter a question.")
        st.stop()

    os.makedirs("temp", exist_ok=True)

    file_path = os.path.join("temp", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Running CrewAI..."):

        crew = create_analytics_crew()
        result = crew.kickoff(
            inputs={
                "user_request": user_request,
                "dataset_path": file_path
            }
        )

    st.success("Analysis Complete")

    st.markdown(result)