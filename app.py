
import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile
from pathlib import Path
from io import BytesIO

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="PROJECT BRIDGE | AI Business Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("PROJECT BRIDGE")
st.subheader("AI Adoption and Operational Value")
st.caption("A simulated business analytics research project")

# --------------------------------------------------
# LOAD PROJECT ZIP
# --------------------------------------------------

ZIP_PATH = Path(__file__).parent / "PROJECT_BRIDGE_backup.zip"

@st.cache_data
def load_csv_from_zip(filename):
    if not ZIP_PATH.exists():
        raise FileNotFoundError(
            "PROJECT_BRIDGE_backup.zip was not found in the repository."
        )

    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        matches = [
            name for name in archive.namelist()
            if name.endswith("/" + filename)
            or name == filename
        ]

        if not matches:
            raise FileNotFoundError(f"{filename} was not found in the ZIP.")

        return pd.read_csv(BytesIO(archive.read(matches[0])))


# --------------------------------------------------
# LOAD EXPERIMENT DATA
# --------------------------------------------------

try:
    A = load_csv_from_zip("experiment_A_human_ai_comparison.csv")
    A_quality = load_csv_from_zip("experiment_A_quality_comparison.csv")
    B = load_csv_from_zip("experiment_B_model_comparison.csv")
    C = load_csv_from_zip("experiment_C_prompt_comparison.csv")
    BE = load_csv_from_zip("experiment_A_break_even_scenarios.csv")
    risks = load_csv_from_zip("responsible_AI_risk_register.csv")
    framework = load_csv_from_zip("AI_adoption_decision_framework.csv")

except Exception as error:
    st.error(f"Unable to load project data: {error}")
    st.stop()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("PROJECT BRIDGE")
page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Experiment A — Enquiries",
        "Experiment B — Feedback",
        "Experiment C — Products",
        "Financial Analysis",
        "Responsible AI"
    ]
)

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "Overview":

    st.header("Research Overview")

    st.write(
        "PROJECT BRIDGE investigates the operational and financial "
        "conditions under which AI-assisted workflows may create value "
        "for a simulated small online retailer, NOVA Retail."
    )

    human_time = A["human_time_seconds"].mean()
    human_quality = A["human_quality_score"].mean()
    ai_quality = A["ai_quality_score"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Enquiries tested", len(A))
    col2.metric("Average human time", f"{human_time:.1f} sec")
    col3.metric("Human quality", f"{human_quality:.2f}/10")
    col4.metric("AI quality", f"{ai_quality:.2f}/10")

    st.divider()

    st.header("Three Experimental Workflows")

    c1, c2, c3 = st.columns(3)

    c1.subheader("A. Customer Enquiries")
    c1.write("Human and AI response quality comparison.")

    c2.subheader("B. Customer Feedback")
    c2.write("Sentiment and topic classification using machine learning.")

    c3.subheader("C. Product Descriptions")
    c3.write("Comparison of two AI prompting approaches.")

    st.divider()

    st.header("Research Limitations")

    st.warning(
        "All datasets are synthetic. Experiment A did not measure "
        "AI processing or human review time. Experiment C used "
        "uniform provisional scores rather than independent "
        "item-by-item evaluation. Financial results are scenarios, "
        "not measured ROI."
    )


# --------------------------------------------------
# EXPERIMENT A
# --------------------------------------------------

elif page == "Experiment A — Enquiries":

    st.header("Experiment A — Customer Enquiry Management")

    st.write(
        "Comparison of human-written and AI-generated responses "
        "across 100 synthetic customer enquiries."
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Human quality",
        f"{A['human_quality_score'].mean():.2f}/10"
    )

    col2.metric(
        "AI quality",
        f"{A['ai_quality_score'].mean():.2f}/10"
    )

    st.subheader("Quality by Evaluation Criterion")

    fig = px.bar(
        A_quality,
        x="Criterion",
        y=["Human_Average", "AI_Average"],
        barmode="group",
        title="Human vs AI quality"
    )

    fig.update_layout(yaxis_range=[0, 2.2])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Response Quality Distribution")

    fig2 = px.histogram(
        A,
        x=["human_quality_score", "ai_quality_score"],
        barmode="overlay",
        opacity=0.7,
        labels={"value": "Quality score", "variable": "Workflow"}
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Human Completion Time")

    st.metric(
        "Average human completion time",
        f"{A['human_time_seconds'].mean():.2f} seconds"
    )

    st.dataframe(A, use_container_width=True)

    st.info(
        "AI processing time and human review time were not measured. "
        "Quality differences cannot establish actual time savings."
    )


# --------------------------------------------------
# EXPERIMENT B
# --------------------------------------------------

elif page == "Experiment B — Feedback":

    st.header("Experiment B — Customer Feedback Analysis")

    st.write(
        "Machine-learning classification of synthetic customer "
        "reviews into sentiment and feedback topics."
    )

    st.subheader("Model Performance")

    st.dataframe(B, use_container_width=True)

    fig = px.bar(
        B,
        x="task",
        y="accuracy",
        color="model",
        barmode="group",
        title="Model Accuracy Comparison",
        text_auto=".1%"
    )

    fig.update_layout(yaxis_range=[0, 1.05])
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        B,
        x="task",
        y="macro_f1",
        color="model",
        barmode="group",
        title="Macro F1 Comparison",
        text_auto=".3f"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.warning(
        "The dataset contains 120 synthetic reviews. Each test set "
        "contains only 24 records. Results are exploratory and "
        "require validation on larger real-world datasets."
    )


# --------------------------------------------------
# EXPERIMENT C
# --------------------------------------------------

elif page == "Experiment C — Products":

    st.header("Experiment C — Product Description Generation")

    st.write(
        "Exploratory comparison of two AI-generated product "
        "description sets using a catalogue of 30 synthetic products."
    )

    st.subheader("Prompt Comparison")

    fig = px.bar(
        C,
        x="criterion",
        y=["prompt_A_average", "prompt_B_average"],
        barmode="group",
        title="Provisional Prompt Quality Scores"
    )

    fig.update_layout(yaxis_range=[0, 2.2])
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(C, use_container_width=True)

    st.warning(
        "Both description sets were AI-generated. Scores were "
        "uniformly prefilled at 2/2 for every criterion. They are "
        "provisional administrative values, not independent "
        "quality measurements."
    )


# --------------------------------------------------
# FINANCIAL ANALYSIS
# --------------------------------------------------

elif page == "Financial Analysis":

    st.header("Financial Analysis — Break-even Scenarios")

    st.write(
        "Illustrative cost scenarios based on the measured human "
        "completion time and assumed labour and AI costs."
    )

    wage = st.selectbox(
        "Assumed hourly labour cost (PKR)",
        sorted(BE["assumed_hourly_wage_pkr"].unique())
    )

    filtered = BE[BE["assumed_hourly_wage_pkr"] == wage]

    st.metric(
        "Human-only cost per enquiry",
        f"PKR {filtered['human_only_cost_per_task_pkr'].iloc[0]:.3f}"
    )

    fig = px.bar(
        filtered,
        x="assumed_ai_cost_per_task_pkr",
        y="maximum_break_even_review_seconds",
        title="Maximum break-even human review time",
        labels={
            "assumed_ai_cost_per_task_pkr": "AI cost per enquiry (PKR)",
            "maximum_break_even_review_seconds": "Review time (seconds)"
        },
        text_auto=".1f"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(filtered, use_container_width=True)

    st.info(
        "Wages and AI costs are illustrative assumptions, not "
        "verified market prices. Actual AI review time and ROI "
        "were not measured."
    )


# --------------------------------------------------
# RESPONSIBLE AI
# --------------------------------------------------

elif page == "Responsible AI":

    st.header("Responsible AI Risk Assessment")

    st.write("Identified risks and recommended operational safeguards.")

    st.dataframe(risks, use_container_width=True)

    st.divider()

    st.header("AI Adoption Decision Framework")

    st.dataframe(framework, use_container_width=True)

    st.success(
        "The framework recommends conditional adoption or "
        "assisted use, with human oversight and validation."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "PROJECT BRIDGE | Research Portfolio | 2026 | "
    "Synthetic-data pilot study"
)
