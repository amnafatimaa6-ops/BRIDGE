
import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile

from pathlib import Path
from io import BytesIO


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="PROJECT BRIDGE | AI Business Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 2. PROJECT HEADER
# ==================================================

st.title("PROJECT BRIDGE")
st.subheader("AI Adoption and Operational Value")

st.caption(
    "A simulated business analytics research project | 2026"
)


# ==================================================
# 3. ZIP DATA LOADER
# ==================================================

ZIP_PATH = Path(__file__).parent / "PROJECT_BRIDGE_backup.zip"


@st.cache_data
def load_csv_from_zip(filename):

    if not ZIP_PATH.exists():
        raise FileNotFoundError(
            "PROJECT_BRIDGE_backup.zip was not found. "
            "Ensure it is uploaded to the GitHub repository."
        )

    with zipfile.ZipFile(ZIP_PATH, "r") as archive:

        matches = [
            name for name in archive.namelist()
            if name.endswith("/" + filename)
            or name == filename
        ]

        if not matches:
            raise FileNotFoundError(
                f"{filename} was not found inside the project ZIP."
            )

        return pd.read_csv(
            BytesIO(archive.read(matches[0]))
        )


# ==================================================
# 4. LOAD EXPERIMENT DATA
# ==================================================

try:

    A = load_csv_from_zip(
        "experiment_A_human_ai_comparison.csv"
    )

    A_quality = load_csv_from_zip(
        "experiment_A_quality_comparison.csv"
    )

    B = load_csv_from_zip(
        "experiment_B_model_comparison.csv"
    )

    C = load_csv_from_zip(
        "experiment_C_prompt_comparison.csv"
    )

    BE = load_csv_from_zip(
        "experiment_A_break_even_scenarios.csv"
    )

    risks = load_csv_from_zip(
        "responsible_AI_risk_register.csv"
    )

    framework = load_csv_from_zip(
        "AI_adoption_decision_framework.csv"
    )

except Exception as error:

    st.error("Unable to load project data.")
    st.exception(error)
    st.stop()


# ==================================================
# 5. DATA VALIDATION
# ==================================================

required_columns = {

    "Experiment A": [
        "task_id",
        "human_time_seconds",
        "human_quality_score",
        "ai_quality_score"
    ],

    "Experiment A Quality": [
        "Criterion",
        "Human_Average",
        "AI_Average"
    ],

    "Experiment B": [
        "task",
        "model",
        "accuracy",
        "macro_f1"
    ],

    "Experiment C": [
        "criterion",
        "prompt_A_average",
        "prompt_B_average"
    ],

    "Financial Analysis": [
        "assumed_hourly_wage_pkr",
        "assumed_ai_cost_per_task_pkr",
        "human_only_cost_per_task_pkr",
        "maximum_break_even_review_seconds"
    ]
}


datasets = {
    "Experiment A": A,
    "Experiment A Quality": A_quality,
    "Experiment B": B,
    "Experiment C": C,
    "Financial Analysis": BE
}


for dataset_name, columns in required_columns.items():

    missing = [
        column for column in columns
        if column not in datasets[dataset_name].columns
    ]

    if missing:

        st.error(
            f"{dataset_name} is missing these columns: {missing}"
        )

        st.stop()


# ==================================================
# 6. SIDEBAR NAVIGATION
# ==================================================

st.sidebar.title("PROJECT BRIDGE")

st.sidebar.caption(
    "AI Adoption Research Dashboard"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Experiment A — Enquiries",
        "Experiment B — Feedback",
        "Experiment C — Products",
        "Financial Analysis",
        "Responsible AI"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Research subject: AI-assisted business operations"
)


# ==================================================
# 7. SHARED METRICS
# ==================================================

human_time = A["human_time_seconds"].mean()

human_quality = A["human_quality_score"].mean()

ai_quality = A["ai_quality_score"].mean()

quality_difference = ai_quality - human_quality


# ==================================================
# 8. OVERVIEW
# ==================================================

if page == "Overview":

    st.header("Research Overview")

    st.write(
        """
        PROJECT BRIDGE investigates the operational and financial
        conditions under which artificial intelligence may create
        measurable value for small businesses.

        The initial case study uses a simulated online retailer,
        NOVA Retail, to compare AI-assisted and traditional workflows.
        """
    )

    st.divider()

    st.subheader("Research Question")

    st.info(
        "Under what operational and financial conditions does "
        "artificial intelligence create measurable value for "
        "small businesses, and when is traditional human-led "
        "work more economically viable?"
    )

    st.subheader("Key Experiment A Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Enquiries evaluated",
        f"{len(A)}"
    )

    col2.metric(
        "Average human time",
        f"{human_time:.2f} sec"
    )

    col3.metric(
        "Human quality",
        f"{human_quality:.2f}/10"
    )

    col4.metric(
        "AI quality",
        f"{ai_quality:.2f}/10",
        delta=f"{quality_difference:+.2f}"
    )

    st.caption(
        "Quality scores are preliminary evaluation results, "
        "not independently validated evidence of AI superiority."
    )

    st.divider()

    st.subheader("Three Experimental Workflows")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown("### A. Customer Enquiries")

        st.write(
            "Comparison of human-written and AI-generated "
            "customer service responses."
        )

        st.caption("100 synthetic enquiries")

    with c2:

        st.markdown("### B. Customer Feedback")

        st.write(
            "Sentiment and topic classification using "
            "traditional machine-learning models."
        )

        st.caption("120 synthetic reviews")

    with c3:

        st.markdown("### C. Product Descriptions")

        st.write(
            "Exploratory comparison of two AI prompting "
            "approaches for product descriptions."
        )

        st.caption("30 synthetic products")

    st.divider()

    st.subheader("Research Methodology")

    st.write(
        """
        The project uses controlled workflow comparisons,
        quantitative evaluation, machine-learning classification,
        illustrative financial scenarios and responsible AI
        risk assessment.
        """
    )

    st.divider()

    st.subheader("Research Limitations")

    st.warning(
        """
        All three datasets contain synthetic data.

        Experiment A did not measure AI processing time or
        human review time. Its quality evaluation was not
        independently validated by an external evaluator.

        Experiment B uses a small test set and requires
        real-world validation.

        Experiment C contains uniformly prefilled provisional
        scores, so no reliable prompt-quality comparison can
        be established.

        Financial scenarios use assumptions rather than
        verified costs. Actual ROI was not measured.
        """
    )


# ==================================================
# 9. EXPERIMENT A — CUSTOMER ENQUIRIES
# ==================================================

elif page == "Experiment A — Enquiries":

    st.header("Experiment A — Customer Enquiry Management")

    st.write(
        """
        This experiment compares human-written and AI-generated
        responses across 100 synthetic customer enquiries using
        the fictional NOVA Retail policy framework.
        """
    )

    st.divider()

    # KEY METRICS

    st.subheader("Key Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Tasks evaluated",
        len(A)
    )

    col2.metric(
        "Human response quality",
        f"{human_quality:.2f}/10"
    )

    col3.metric(
        "AI response quality",
        f"{ai_quality:.2f}/10"
    )

    col4.metric(
        "Quality difference",
        f"{quality_difference:+.2f}"
    )

    st.metric(
        "Average measured human completion time",
        f"{human_time:.2f} seconds"
    )

    st.divider()

    # QUALITY COMPARISON

    st.subheader("Human vs AI Quality by Criterion")

    st.write(
        """
        Responses were evaluated across five criteria:
        policy accuracy, completeness, unsupported claims,
        escalation correctness and clarity.
        """
    )

    quality_plot = A_quality.melt(
        id_vars=["Criterion"],
        value_vars=["Human_Average", "AI_Average"],
        var_name="Workflow",
        value_name="Average Score"
    )

    quality_plot["Workflow"] = quality_plot["Workflow"].replace(
        {
            "Human_Average": "Human",
            "AI_Average": "AI"
        }
    )

    fig_quality = px.bar(
        quality_plot,
        x="Criterion",
        y="Average Score",
        color="Workflow",
        barmode="group",
        title="Quality Comparison Across Evaluation Criteria",
        text_auto=".2f",
        labels={
            "Criterion": "Evaluation Criterion",
            "Average Score": "Average Score",
            "Workflow": "Response Type"
        }
    )

    fig_quality.update_layout(
        yaxis_range=[0, 2.2],
        xaxis_tickangle=-20,
        legend_title="Workflow"
    )

    st.plotly_chart(
        fig_quality,
        use_container_width=True
    )

    st.divider()

    # QUALITY DISTRIBUTION

    st.subheader("Response Quality Distribution")

    distribution = A.melt(
        value_vars=[
            "human_quality_score",
            "ai_quality_score"
        ],
        var_name="Workflow",
        value_name="Quality Score"
    )

    distribution["Workflow"] = distribution["Workflow"].replace(
        {
            "human_quality_score": "Human",
            "ai_quality_score": "AI"
        }
    )

    fig_distribution = px.histogram(
        distribution,
        x="Quality Score",
        color="Workflow",
        barmode="overlay",
        opacity=0.65,
        nbins=10,
        title="Distribution of Human and AI Quality Scores"
    )

    st.plotly_chart(
        fig_distribution,
        use_container_width=True
    )

    st.divider()

    # TIME ANALYSIS

    st.subheader("Human Completion Time")

    col1, col2 = st.columns(2)

    col1.metric(
        "Mean completion time",
        f"{A['human_time_seconds'].mean():.2f} sec"
    )

    col2.metric(
        "Median completion time",
        f"{A['human_time_seconds'].median():.2f} sec"
    )

    st.caption(
        "Only human completion time was measured. "
        "AI inference time and human review time were not recorded."
    )

    st.divider()

    # METHODOLOGICAL LIMITATIONS

    st.subheader("Methodological Limitations")

    st.warning(
        """
        **Evaluation independence**

        Human and AI responses were assessed using the same
        AI-assisted evaluation workflow. The scoring was not
        independently validated by an external evaluator.

        Therefore, the observed quality difference should be
        interpreted as a preliminary result, not proof of
        independently verified AI superiority.
        """
    )

    st.info(
        """
        **Operational efficiency**

        Human completion time was measured directly.

        AI processing time and human review time were not
        measured. Consequently, actual AI time savings,
        productivity gains and operational ROI cannot
        be calculated from this experiment.
        """
    )

    st.info(
        """
        **Synthetic dataset**

        The 100 enquiries were created using fictional
        NOVA Retail policies. They do not represent a
        verified sample of real customer interactions.
        """
    )

    # DATA TABLE

    with st.expander("View complete Experiment A dataset"):

        st.dataframe(
            A,
            use_container_width=True,
            hide_index=True
        )

    with st.expander("View quality evaluation data"):

        st.dataframe(
            A_quality,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# 10. EXPERIMENT B — CUSTOMER FEEDBACK
# ==================================================

elif page == "Experiment B — Feedback":

    st.header("Experiment B — Customer Feedback Analysis")

    st.write(
        """
        This experiment evaluates machine-learning models
        for classifying synthetic customer reviews into
        sentiment categories and feedback topics.
        """
    )

    st.divider()

    st.subheader("Model Performance")

    st.dataframe(
        B,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ACCURACY

    st.subheader("Classification Accuracy")

    fig_accuracy = px.bar(
        B,
        x="task",
        y="accuracy",
        color="model",
        barmode="group",
        title="Model Accuracy Comparison",
        text_auto=".1f"
    )

    fig_accuracy.update_layout(
        yaxis_range=[0, 1.05],
        yaxis_tickformat=".0%",
        xaxis_title="Classification Task",
        yaxis_title="Accuracy"
    )

    st.plotly_chart(
        fig_accuracy,
        use_container_width=True
    )

    # MACRO F1

    st.subheader("Macro F1 Score")

    fig_f1 = px.bar(
        B,
        x="task",
        y="macro_f1",
        color="model",
        barmode="group",
        title="Macro F1 Model Comparison",
        text_auto=".3f"
    )

    fig_f1.update_layout(
        yaxis_range=[0, 1.05],
        xaxis_title="Classification Task",
        yaxis_title="Macro F1 Score"
    )

    st.plotly_chart(
        fig_f1,
        use_container_width=True
    )

    st.divider()

    # RESULTS INTERPRETATION

    st.subheader("Interpretation")

    st.write(
        """
        Logistic Regression achieved 83.3% sentiment
        classification accuracy and 91.7% topic classification
        accuracy on the respective 24-record test sets.

        Its main sentiment weakness was confusing neutral
        reviews with negative reviews.

        Topic classification also showed confusion between
        Customer Support and Returns and Refunds.
        """
    )

    st.info(
        """
        Linear SVM achieved the same topic accuracy as
        Logistic Regression but lower sentiment accuracy.
        Logistic Regression was therefore retained as the
        preferred baseline model.
        """
    )

    st.divider()

    st.subheader("Research Limitations")

    st.warning(
        """
        The dataset contains only 120 synthetic reviews.

        Each classification test set contains 24 records.
        The results use a single stratified train-test split.

        The dataset is not representative of real customer
        populations. External validation and larger datasets
        are necessary before operational deployment.
        """
    )


# ==================================================
# 11. EXPERIMENT C — PRODUCT DESCRIPTIONS
# ==================================================

elif page == "Experiment C — Products":

    st.header("Experiment C — Product Description Generation")

    st.write(
        """
        This exploratory experiment examines two AI-generated
        product description sets using a synthetic catalogue
        of 30 fictional products.
        """
    )

    st.divider()

    st.subheader("Prompt Comparison")

    C_plot = C.melt(
        id_vars=["criterion"],
        value_vars=[
            "prompt_A_average",
            "prompt_B_average"
        ],
        var_name="Prompt",
        value_name="Provisional Score"
    )

    C_plot["Prompt"] = C_plot["Prompt"].replace(
        {
            "prompt_A_average": "Prompt A",
            "prompt_B_average": "Prompt B"
        }
    )

    fig = px.bar(
        C_plot,
        x="criterion",
        y="Provisional Score",
        color="Prompt",
        barmode="group",
        title="Provisional Prompt Evaluation Scores"
    )

    fig.update_layout(
        yaxis_range=[0, 2.2],
        xaxis_tickangle=-20
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Evaluation Data")

    st.dataframe(
        C,
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        """
        **Critical evaluation limitation**

        Both description sets were AI-generated.

        Prompt B scores were uniformly prefilled with 2/2
        across all evaluation criteria and records.

        These are provisional administrative values,
        not independent item-by-item quality measurements.

        Therefore, the available results cannot establish
        that Prompt A and Prompt B have equivalent quality
        or identify a superior prompting strategy.
        """
    )

    st.info(
        """
        A future evaluation should use independently scored
        descriptions, predefined factual accuracy criteria,
        and human reviewers who do not know which prompt
        generated each description.
        """
    )


# ==================================================
# 12. FINANCIAL ANALYSIS
# ==================================================

elif page == "Financial Analysis":

    st.header("Financial Analysis — Break-even Scenarios")

    st.write(
        """
        This section models illustrative AI adoption costs
        using measured human completion time and assumed
        labour and AI costs.
        """
    )

    st.divider()

    st.subheader("Scenario Selection")

    wage_options = sorted(
        BE["assumed_hourly_wage_pkr"].unique()
    )

    wage = st.selectbox(
        "Assumed hourly labour cost (PKR)",
        wage_options
    )

    filtered = BE[
        BE["assumed_hourly_wage_pkr"] == wage
    ].copy()

    filtered = filtered.sort_values(
        "assumed_ai_cost_per_task_pkr"
    )

    human_cost = (
        filtered["human_only_cost_per_task_pkr"].iloc[0]
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Human-only cost per enquiry",
        f"PKR {human_cost:.3f}"
    )

    col2.metric(
        "Measured human time",
        f"{human_time:.2f} sec"
    )

    st.divider()

    # BREAK-EVEN CHART

    st.subheader("Maximum Break-even Review Time")

    st.write(
        """
        The chart shows the maximum human review time
        permitted under each assumed AI cost before the
        AI-assisted workflow becomes more expensive than
        the human-only baseline.
        """
    )

    fig = px.bar(
        filtered,
        x="assumed_ai_cost_per_task_pkr",
        y="maximum_break_even_review_seconds",
        title="Break-even Human Review Time by AI Cost",
        labels={
            "assumed_ai_cost_per_task_pkr":
                "Assumed AI Cost per Enquiry (PKR)",

            "maximum_break_even_review_seconds":
                "Maximum Review Time (Seconds)"
        },
        text_auto=".1f"
    )

    fig.update_layout(
        xaxis_title="AI Cost per Enquiry (PKR)",
        yaxis_title="Break-even Review Time (Seconds)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # SCENARIO TABLE

    st.subheader("Scenario Data")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    # SELECTED SCENARIO INTERPRETATION

    st.subheader("Financial Interpretation")

    st.write(
        """
        AI adoption is economically attractive only if
        its cost and associated human review time remain
        below the human-only cost baseline.
        """
    )

    st.info(
        """
        A break-even threshold is not evidence of actual
        savings. It is a conditional financial scenario
        based on the selected wage and assumed AI cost.
        """
    )

    st.warning(
        """
        Hourly wages and AI costs are illustrative assumptions,
        not verified market prices.

        Actual AI processing costs, human review time,
        implementation expenses and ROI were not measured.
        """
    )


# ==================================================
# 13. RESPONSIBLE AI
# ==================================================

elif page == "Responsible AI":

    st.header("Responsible AI Risk Assessment")

    st.write(
        """
        AI adoption requires operational safeguards,
        accountability and human oversight.
        """
    )

    st.divider()

    st.subheader("Identified Risks")

    st.dataframe(
        risks,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("AI Adoption Decision Framework")

    st.write(
        """
        The framework translates the experimental findings
        into conditional adoption recommendations for
        the three business workflows.
        """
    )

    st.dataframe(
        framework,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Responsible Adoption Principles")

    st.markdown(
        """
        - Maintain human oversight for sensitive decisions.
        - Verify AI-generated factual claims.
        - Escalate uncertain or policy-sensitive enquiries.
        - Protect customer information.
        - Monitor classification errors.
        - Validate financial benefits before investment.
        - Keep accountability with the business.
        """
    )

    st.info(
        """
        PROJECT BRIDGE does not recommend unrestricted
        automation. Its findings support conditional adoption
        and human-assisted AI workflows.
        """
    )


# ==================================================
# 14. FOOTER
# ==================================================

st.divider()

st.caption(
    "PROJECT BRIDGE | Research Portfolio | 2026 | "
    "Synthetic-data pilot study"
)

st.caption(
    "All findings are exploratory and should be interpreted "
    "within the stated experimental limitations."
)

