import streamlit as st

st.set_page_config(
    page_title="WaterWatch AI",
    page_icon="💧",
    layout="wide"
)

st.title("💧 WaterWatch AI")

st.subheader(
    "Environmental Water Quality Monitoring"
)

st.write(
    """
    Welcome to WaterWatch AI!

    Our goal is to make environmental water
    quality measurements easier to understand.
    """
)

st.success("Your application is running!")

st.header("Project Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Locations Monitored", "3")

with col2:
    st.metric("Measurements", "15")

with col3:
    st.metric("Alerts", "1")

st.info(
    "Upload environmental data to begin analysis."
)