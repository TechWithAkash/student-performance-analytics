import os
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Student Performance Analytics | BDA Big Data Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling (Dark/Slate Academic BDA Theme)
st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 24px;
        border-radius: 12px;
        border-left: 6px solid #38bdf8;
        color: #f8fafc;
        margin-bottom: 24px;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.025em;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 6px;
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #38bdf8;
        margin: 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-hadoop { background-color: #fef08a; color: #854d0e; }
    .badge-hive { background-color: #bae6fd; color: #0369a1; }
    .badge-spark { background-color: #fed7aa; color: #9a3412; }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data(csv_path="data/raw/student-por.csv"):
    path = Path(csv_path)
    if not path.exists():
        # Fallback to current directory or processed path
        if Path("data/processed/student_por_clean.csv").exists():
            path = Path("data/processed/student_por_clean.csv")
        else:
            raise FileNotFoundError(f"Cannot find dataset at {csv_path}")
    df = pd.read_csv(path, sep=";")
    return df

def calculate_kpis(df):
    total = len(df)
    if total == 0:
        return {
            "total_students": 0,
            "avg_g3": 0.0,
            "max_g3": 0,
            "min_g3": 0,
            "avg_absences": 0.0,
            "pass_rate": 0.0,
        }
    passed = len(df[df["G3"] >= 10])
    return {
        "total_students": total,
        "avg_g3": round(float(df["G3"].mean()), 2),
        "max_g3": int(df["G3"].max()),
        "min_g3": int(df["G3"].min()),
        "avg_absences": round(float(df["absences"].mean()), 1),
        "pass_rate": round((passed / total) * 100.0, 1),
    }

def main():
    # Load dataset
    try:
        df_raw = load_data()
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return

    # Sidebar Filter Controls
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/0e/Apache_Hadoop_logo.svg", width=160)
    st.sidebar.title("🎛️ Analysis Filters")
    st.sidebar.markdown("Filter cohort data across school, demographics, and study factors.")

    # Filter: School
    school_map = {"All": "All", "GP": "GP - Gabriel Pereira", "MS": "MS - Mousinho da Silveira"}
    selected_school = st.sidebar.selectbox("School Location", options=["All", "GP", "MS"], format_func=lambda x: school_map.get(x, x))

    # Filter: Gender
    selected_sex = st.sidebar.radio("Student Gender", options=["All", "F", "M"], format_func=lambda x: "All Genders" if x == "All" else ("Female" if x == "F" else "Male"), horizontal=True)

    # Filter: Study Time
    study_time_opts = st.sidebar.multiselect(
        "Weekly Study Time",
        options=[1, 2, 3, 4],
        default=[1, 2, 3, 4],
        format_func=lambda x: {1: "< 2 hours", 2: "2-5 hours", 3: "5-10 hours", 4: "> 10 hours"}[x]
    )

    # Filter: Final Grade Range
    grade_range = st.sidebar.slider("Final Grade Range (G3: 0–20)", min_value=0, max_value=20, value=(0, 20))

    # Filter: Support & Socioeconomic
    higher_ed_only = st.sidebar.checkbox("Desires Higher Education Only", value=False)
    internet_only = st.sidebar.checkbox("Has Home Internet Only", value=False)

    # Apply Filters
    df = df_raw.copy()
    if selected_school != "All":
        df = df[df["school"] == selected_school]
    if selected_sex != "All":
        df = df[df["sex"] == selected_sex]
    if study_time_opts:
        df = df[df["studytime"].isin(study_time_opts)]
    df = df[(df["G3"] >= grade_range[0]) & (df["G3"] <= grade_range[1])]
    if higher_ed_only:
        df = df[df["higher"] == "yes"]
    if internet_only:
        df = df[df["internet"] == "yes"]

    # Header Banner
    st.markdown(
        """
        <div class="main-header">
            <h1 class="main-title">🎓 Student Performance Big Data Analytics</h1>
            <p class="sub-title">Distributed Storage & Querying: <b>Hadoop HDFS</b> + <b>Apache Hive (HiveQL)</b> | Interactive Analytics Layer</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top KPI Metrics Row
    kpis = calculate_kpis(df)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f'<div class="metric-card"><p class="metric-value">{kpis["total_students"]}</p><p class="metric-label">Enrolled Students</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><p class="metric-value">{kpis["avg_g3"]}<span style="font-size:1rem;color:#94a3b8">/20</span></p><p class="metric-label">Avg Final Grade (G3)</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><p class="metric-value">{kpis["pass_rate"]}%</p><p class="metric-label">Cohort Pass Rate (≥10)</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><p class="metric-value">{kpis["avg_absences"]}</p><p class="metric-label">Avg Class Absences</p></div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="metric-card"><p class="metric-value">{kpis["max_g3"]}<span style="font-size:1rem;color:#94a3b8">/20</span></p><p class="metric-label">Peak Grade Achieved</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Overview",
        "📈 Grade Distributions & Comparison",
        "🔍 Factor & Correlation Analysis",
        "⚠️ Risk Students & High Achievers",
        "🏛️ BDA Architecture & Hive Hub"
    ])

    # ---------------- TAB 1: EXECUTIVE OVERVIEW ----------------
    with tab1:
        st.subheader("Cohort Academic Progression & Trajectory")
        col_t1, col_t2 = st.columns([3, 2])

        with col_t1:
            # Period score progression (G1 -> G2 -> G3)
            prog_df = pd.DataFrame({
                "Period": ["Period 1 (G1)", "Period 2 (G2)", "Final Exam (G3)"],
                "Average Grade": [df["G1"].mean(), df["G2"].mean(), df["G3"].mean()]
            })
            fig_prog = px.line(
                prog_df,
                x="Period",
                y="Average Grade",
                markers=True,
                title="Academic Progression Across Evaluation Periods",
                color_discrete_sequence=["#38bdf8"],
            )
            fig_prog.update_layout(yaxis_range=[0, 20], template="plotly_dark")
            st.plotly_chart(fig_prog, use_container_width=True)

        with col_t2:
            # Pass vs Fail Donut
            pass_status = df["G3"].apply(lambda g: "Passed (≥10)" if g >= 10 else "Failed (<10)")
            status_counts = pass_status.value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            fig_pie = px.pie(
                status_counts,
                names="Status",
                values="Count",
                hole=0.55,
                color="Status",
                color_discrete_map={"Passed (≥10)": "#10b981", "Failed (<10)": "#ef4444"},
                title="Pass / Fail Proportions",
            )
            fig_pie.update_layout(template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)

        st.info("💡 **Hive Insight:** The correlation between G1, G2, and final G3 indicates early academic evaluations strongly predict final student success, allowing early interventions by educators.")

    # ---------------- TAB 2: GRADE DISTRIBUTIONS ----------------
    with tab2:
        st.subheader("Portuguese Grade Distribution & Group Segments")
        c_d1, c_d2 = st.columns(2)

        with c_d1:
            # Grade category histogram
            def categorize_grade(g):
                if g < 10: return "01. Fail (0-9)"
                elif g <= 13: return "02. Sufficient (10-13)"
                elif g <= 15: return "03. Good (14-15)"
                else: return "04. Excellent (16-20)"
            
            df_cat = df.copy()
            df_cat["Category"] = df_cat["G3"].apply(categorize_grade)
            cat_summary = df_cat["Category"].value_counts().sort_index().reset_index()
            cat_summary.columns = ["Category", "Count"]

            fig_cat = px.bar(
                cat_summary,
                x="Category",
                y="Count",
                text="Count",
                color="Category",
                color_discrete_sequence=px.colors.sequential.Teal,
                title="Cohort Distribution Across Standard Grade Categories",
            )
            fig_cat.update_layout(template="plotly_dark", showlegend=False)
            st.plotly_chart(fig_cat, use_container_width=True)

        with c_d2:
            # School comparison (GP vs MS)
            fig_box = px.box(
                df,
                x="school",
                y="G3",
                color="sex",
                title="Final Grade Spread by School and Gender",
                color_discrete_map={"F": "#ec4899", "M": "#3b82f6"},
                labels={"G3": "Final Grade", "school": "School", "sex": "Gender"}
            )
            fig_box.update_layout(template="plotly_dark")
            st.plotly_chart(fig_box, use_container_width=True)

    # ---------------- TAB 3: FACTOR & CORRELATION ----------------
    with tab3:
        st.subheader("Academic, Lifestyle, and Family Background Factors")
        cf1, cf2 = st.columns(2)

        with cf1:
            # Study time vs G3
            study_labels = {1: "< 2 hours", 2: "2-5 hours", 3: "5-10 hours", 4: "> 10 hours"}
            df_study = df.copy()
            df_study["study_desc"] = df_study["studytime"].map(study_labels)
            study_grp = df_study.groupby("study_desc")[["G3"]].mean().reindex(study_labels.values()).reset_index()

            fig_study = px.bar(
                study_grp,
                x="study_desc",
                y="G3",
                text="G3",
                title="Weekly Study Time vs Average Final Grade (G3)",
                color="G3",
                color_continuous_scale="Viridis",
            )
            fig_study.update_layout(template="plotly_dark", yaxis_range=[0, 20])
            st.plotly_chart(fig_study, use_container_width=True)

        with cf2:
            # Absences vs G3 scatter
            fig_abs = px.scatter(
                df,
                x="absences",
                y="G3",
                color="failures",
                trendline="ols",
                title="School Absences vs Final Grade (Colored by Past Failures)",
                color_continuous_scale="Reds",
                labels={"absences": "Number of Absences", "G3": "Final Grade (0-20)"}
            )
            fig_abs.update_layout(template="plotly_dark")
            st.plotly_chart(fig_abs, use_container_width=True)

        cf3, cf4 = st.columns(2)
        with cf3:
            # Parental education heatmap/grouped bar
            parent_edu = df.groupby(["Medu", "Fedu"])[["G3"]].mean().reset_index()
            fig_parent = px.density_heatmap(
                parent_edu,
                x="Medu",
                y="Fedu",
                z="G3",
                title="Mother's (Medu) vs Father's (Fedu) Education Impact on G3",
                labels={"Medu": "Mother Education (0-4)", "Fedu": "Father Education (0-4)", "G3": "Avg G3"},
            )
            fig_parent.update_layout(template="plotly_dark")
            st.plotly_chart(fig_parent, use_container_width=True)

        with cf4:
            # Weekend Alcohol Consumption vs G3
            alc_grp = df.groupby("Walc")[["G3"]].mean().reset_index()
            fig_alc = px.line(
                alc_grp,
                x="Walc",
                y="G3",
                markers=True,
                title="Weekend Alcohol Consumption (Walc: 1=Low, 5=High) vs Avg G3",
                color_discrete_sequence=["#f43f5e"]
            )
            fig_alc.update_layout(template="plotly_dark", yaxis_range=[0, 20])
            st.plotly_chart(fig_alc, use_container_width=True)

    # ---------------- TAB 4: RISK & ACHIEVERS ----------------
    with tab4:
        st.subheader("Academic Risk Identification & Top Achievers Drill-Down")
        
        col_r1, col_r2 = st.columns([1, 1])
        with col_r1:
            st.markdown("### ⚠️ At-Risk Students Filter")
            st.markdown("Identifies students meeting warning conditions ($G3 < 10$, $Failures > 0$, or $Absences > 10$).")
            risk_df = df[(df["G3"] < 10) | (df["failures"] > 0) | (df["absences"] > 10)].copy()
            risk_df["Risk Category"] = risk_df.apply(
                lambda r: "CRITICAL RISK" if r["G3"] < 10 and r["failures"] > 0 and r["absences"] > 10
                else ("FAILING RISK" if r["G3"] < 10 else ("HISTORY RISK" if r["failures"] > 0 else "ATTENDANCE RISK")),
                axis=1
            )
            st.write(f"Identified **{len(risk_df)}** at-risk students in current selection.")
            st.dataframe(
                risk_df[["school", "sex", "age", "studytime", "failures", "absences", "G1", "G2", "G3", "Risk Category"]].sort_values(by="G3"),
                height=320,
                use_container_width=True
            )
            csv_risk = risk_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download At-Risk Students CSV", csv_risk, "at_risk_students.csv", "text/csv")

        with col_r2:
            st.markdown("### 🌟 Top Academic Achievers ($G3 \\ge 16$)")
            top_df = df[df["G3"] >= 16].copy()
            st.write(f"Cohort Top Performers: **{len(top_df)}** students ({round(len(top_df)*100/len(df), 1)}% of cohort).")
            st.dataframe(
                top_df[["school", "sex", "age", "studytime", "failures", "absences", "higher", "internet", "G1", "G2", "G3"]].sort_values(by="G3", ascending=False),
                height=320,
                use_container_width=True
            )
            csv_top = top_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Top Achievers CSV", csv_top, "top_achievers.csv", "text/csv")

    # ---------------- TAB 5: BDA ARCHITECTURE & HIVE HUB ----------------
    with tab5:
        st.subheader("Big Data Technical Architecture & HiveQL Execution Hub")
        st.markdown(
            """
            ```
            ┌──────────────────┐       ┌───────────────────────┐       ┌──────────────────────┐       ┌──────────────────┐
            │   UCI DATASET    │ ────> │      HADOOP HDFS      │ ────> │     APACHE HIVE      │ ────> │    STREAMLIT     │
            │ student-por.csv  │       │ /user/hadoop/student/ │       │  HiveQL (01 to 07)   │       │ Dynamic Reports  │
            └──────────────────┘       └───────────────────────┘       └──────────────────────┘       └──────────────────┘
                 (Raw CSV)                (Storage Layer)                 (Warehouse Query)             (Presentation)
            ```
            """
        )

        st.markdown("#### Inspect HiveQL Query Scripts & Execution Outputs")
        script_choice = st.selectbox(
            "Select HiveQL Script:",
            [
                "01_create_database.sql",
                "02_create_table.sql",
                "03_load_data.sql",
                "04_basic_analysis.sql",
                "05_performance_analysis.sql",
                "06_factor_analysis.sql",
                "07_advanced_analysis.sql",
            ]
        )

        sql_file_path = Path("hive") / script_choice
        if sql_file_path.exists():
            with open(sql_file_path, "r") as f:
                sql_content = f.read()
            st.code(sql_content, language="sql")
        
        # Display corresponding output CSV if available
        csv_mapping = {
            "04_basic_analysis.sql": "output/query-results/04_basic_analysis.csv",
            "05_performance_analysis.sql": "output/query-results/05_gender_analysis.csv",
            "06_factor_analysis.sql": "output/query-results/06_study_time.csv",
            "07_advanced_analysis.sql": "output/query-results/07_top_achievers.csv",
        }
        if script_choice in csv_mapping and Path(csv_mapping[script_choice]).exists():
            st.markdown("##### Query Execution Result Sample:")
            st.dataframe(pd.read_csv(csv_mapping[script_choice]), use_container_width=True)

if __name__ == "__main__":
    main()
