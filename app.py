
import streamlit as st
import pandas as pd
import plotly.express as px

from analyzer import analyze_water_data


# Page configuration
st.set_page_config(
    page_title="WaterWatch AI",
    page_icon="💧",
    layout="wide"
)


# Application title
st.title("💧 WaterWatch AI")

st.write(
    "AI-powered environmental water quality monitoring."
)

st.divider()


# Sidebar
st.sidebar.title("WaterWatch AI")

st.sidebar.write(
    "Environmental monitoring dashboard"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Data Analysis",
        "AI Insights"
    ]
)


# Dataset upload
st.sidebar.subheader("Upload Water Data")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)


# Load data
df = None

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

    except Exception as error:
        st.error(f"Unable to read CSV: {error}")

else:
    st.info(
        "Upload a CSV file using the sidebar to begin."
    )


# Analyze uploaded data
if df is not None:

    try:

        results = analyze_water_data(df)

        st.success("Data successfully analyzed!")

        if page == "Overview":

            st.header("Environmental Overview")

            total_locations = (
                results["location"].nunique()
            )

            total_measurements = len(results)

            total_alerts = sum(
                bool(alerts)
                for alerts in results["alerts"]
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Locations Monitored",
                total_locations
            )

            col2.metric(
                "Measurements",
                total_measurements
            )

            col3.metric(
                "Measurements Flagged",
                total_alerts
            )

            st.subheader("Measurement Summary")

            st.dataframe(
                results,
                use_container_width=True
            )

            st.subheader("Locations Requiring Review")

            flagged = results[
                results["alerts"].map(bool)
            ]

            if len(flagged) > 0:
                st.warning(
                    f"{len(flagged)} measurements "
                    "require further review."
                )
            else:
                st.success(
                    "No screening alerts detected."
                )

        elif page == "Data Analysis":

            st.header("Water Quality Analysis")

            st.subheader("Uploaded Measurements")

            st.dataframe(
                results,
                use_container_width=True
            )

            st.subheader("pH Measurements")

            fig = px.bar(
                results,
                x="location",
                y="ph",
                color="location",
                title="pH by Location"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader("Dissolved Oxygen")

            fig = px.bar(
                results,
                x="location",
                y="dissolved_oxygen",
                color="location",
                title="Dissolved Oxygen by Location"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader("Turbidity")

            fig = px.bar(
                results,
                x="location",
                y="turbidity",
                color="location",
                title="Turbidity by Location"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        elif page == "AI Insights":

            st.header("Environmental Findings")

            st.info(
                "AI explanations will be added in Stage 4."
            )

            for _, row in results.iterrows():

                with st.expander(
                    f"{row['location']} - {row['date']}"
                ):

                    if row["alerts"]:

                        for alert in row["alerts"]:
                            st.warning(alert)

                    else:
                        st.success(
                            "No screening alerts detected."
                        )

                    st.write(
                        "These findings are preliminary "
                        "and do not establish water safety."
                    )

    except ValueError as error:

        st.error(f"Data validation error: {error}")

    except Exception as error:

        st.error(f"Analysis failed: {error}")


st.divider()

st.caption(
    "WaterWatch AI | Environmental data screening "
    "and analysis. Not a substitute for laboratory testing."
)
