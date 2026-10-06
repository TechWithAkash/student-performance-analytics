# Design Specification: Student Performance Big Data Analytics (BDA) System

- **Date:** 2026-10-06
- **Status:** Approved
- **Topic:** Student Performance Analytics Using Hadoop HDFS, Apache Hive, and Streamlit
- **Reference Document:** `Student_Performance_BDA_Technical_Lecture (1).md`

---

## 1. Executive Summary & Problem Statement

Educational institutions handle complex student records containing demographic data, academic history, socioeconomic conditions, and personal habits. Analyzing these factors using modern Big Data paradigms allows educators to discover key patterns influencing academic outcomes and identify at-risk students before final evaluations.

This project implements an end-to-end Big Data Analytics (BDA) pipeline that utilizes:
1. **Distributed Storage Layer:** Apache Hadoop HDFS for reliable, fault-tolerant dataset storage.
2. **Analytical Query Layer:** Apache Hive & HiveQL for SQL-based distributed data warehouse querying, aggregation, and segmentation.
3. **Interactive Presentation Layer:** Streamlit with Plotly for dynamic KPI monitoring, student risk factor drill-downs, and architectural visualization.
4. **Resilience & Demo Layer:** A containerized Docker Compose cluster (Hadoop + Hive) paired with a dual-execution local Python runner for 100% offline demo safety.

---

## 2. Dataset Specifications

- **Source:** UCI Machine Learning Repository (Student Performance Dataset).
- **Target File:** `student-por.csv` (Portuguese language course).
- **Format:** Semicolon-delimited (`;`), 649 records, 33 attributes, no missing values.
- **Attributes:**
  - **Demographics:** `school`, `sex`, `age`, `address`, `famsize`, `Pstatus`.
  - **Family & Socioeconomic:** `Medu`, `Fedu`, `Mjob`, `Fjob`, `reason`, `guardian`.
  - **Academic Habits:** `traveltime`, `studytime`, `failures`, `schoolsup`, `famsup`, `paid`, `activities`.
  - **Lifestyle & Health:** `nursery`, `higher`, `internet`, `romantic`, `famrel`, `freetime`, `goout`, `Dalc`, `Walc`, `health`, `absences`.
  - **Performance Benchmarks:** `G1` (1st period grade, 0–20), `G2` (2nd period grade, 0–20), `G3` (final grade, 0–20).

---

## 3. System Architecture & Component Interactions

```text
┌────────────────────────────────────────────────────────┐
│                   UCI Repository                       │
│                  (student-por.csv)                     │
└──────────────────────────┬─────────────────────────────┘
                           │ 1. Download & Validate
                           ▼
┌────────────────────────────────────────────────────────┐
│             Data Preparation & Validation              │
│            (scripts/download_data.py)                  │
└────────────┬─────────────────────────────┬─────────────┘
             │ 2. hdfs dfs -put            │
             ▼                             │
┌───────────────────────────────┐          │
│       Hadoop HDFS Storage     │          │
│  /user/hadoop/student-perf/   │          │
└────────────┬──────────────────┘          │
             │ 3. Schema-on-read           │
             ▼                             │ (Offline Fallback)
┌───────────────────────────────┐          │
│          Apache Hive          │          │
│    (Database & HiveQL 01-07)  │          │
└────────────┬──────────────────┘          │
             │ 4. Query Execution          │
             ▼                             ▼
┌────────────────────────────────────────────────────────┐
│            output/query-results/ (CSVs & Logs)         │
└──────────────────────────┬─────────────────────────────┘
                           │ 5. Read analytical summaries
                           ▼
┌────────────────────────────────────────────────────────┐
│                   Streamlit App                        │
│            KPIs, Plots, Risk Engine, Docs              │
└────────────────────────────────────────────────────────┘
```

---

## 4. Repository & Directory Structure

```text
/Users/akashvishwakarma/bda-project/
├── data/
│   ├── raw/
│   │   ├── student-por.csv
│   │   └── student-performance.zip
│   └── processed/
│       └── student_por_clean.csv
├── docker/
│   └── docker-compose.yml
├── hive/
│   ├── 01_create_database.sql
│   ├── 02_create_table.sql
│   ├── 03_load_data.sql
│   ├── 04_basic_analysis.sql
│   ├── 05_performance_analysis.sql
│   ├── 06_factor_analysis.sql
│   └── 07_advanced_analysis.sql
├── output/
│   └── query-results/
├── scripts/
│   ├── download_data.py
│   ├── run_pipeline.sh
│   └── local_query_runner.py
├── docs/
│   ├── project-report.md
│   └── viva-prep-guide.md
├── app.py
├── requirements.txt
└── README.md
```

---

## 5. Detailed HiveQL Query Specifications

### Script `01_create_database.sql`
- Creates database `student_performance_bda` if not exists.
- Sets database active.

### Script `02_create_table.sql`
- Defines table `student_por` with 33 columns matching UCI exact types (`INT` and `STRING`).
- Specifies delimiter: `ROW FORMAT DELIMITED FIELDS TERMINATED BY ';'`.
- Specifies `STORED AS TEXTFILE` and skips header row.

### Script `03_load_data.sql`
- Loads data from HDFS `/user/hadoop/student-performance/student-por.csv` into `student_por`.

### Script `04_basic_analysis.sql`
- **Q1:** Total student count (`COUNT(*)`).
- **Q2:** Aggregate metrics for final score: Average, Min, Max, and Standard Deviation of `G3`.
- **Q3:** Progression of period scores: `AVG(G1)`, `AVG(G2)`, `AVG(G3)`.
- **Q4:** Absence statistics: Average, Min, and Max absences.

### Script `05_performance_analysis.sql`
- **Q5:** Grade comparison by Gender (`sex`).
- **Q6:** Grade comparison by School (`GP` vs `MS`).
- **Q7:** Overall Pass Rate ($G3 \ge 10$ count and percentage).
- **Q8:** Portuguese grade distribution buckets: Fail ($<10$), Sufficient ($10-13$), Good ($14-15$), Excellent ($16-20$).

### Script `06_factor_analysis.sql`
- **Q9:** Weekly study time impact (`studytime` 1 through 4 vs `AVG(G3)`).
- **Q10:** Previous failures impact (`failures` vs `AVG(G3)`).
- **Q11:** Attendance/absence quartiles vs academic outcome.
- **Q12:** Mother's and Father's education levels (`Medu`, `Fedu`) vs `AVG(G3)`.
- **Q13:** Educational support (`schoolsup`, `famsup`) vs `AVG(G3)`.
- **Q14:** Socioeconomic factors: Internet access and desire for higher education (`higher`, `internet`).

### Script `07_advanced_analysis.sql`
- **Q15:** Academic At-Risk identification: Students with $G3 < 10$, failures $>0$, or absences $>10$.
- **Q16:** Top Academic Achievers ($G3 \ge 16$) and correlation with lifestyle factors.
- **Q17:** Alcohol consumption (`Dalc`, `Walc`) and leisure time (`freetime`, `goout`) impact on performance.

---

## 6. Streamlit Dashboard Design

### UI Layout
- **Custom Theme:** Navy/Slate modern analytical theme with CSS metric cards.
- **Sidebar:** School selector, Gender filter, Study Time slider, Grade Range slider, Socioeconomic toggles.
- **Tabs:**
  1. **Overview & KPIs:** Summary badges, progression timeline ($G1 \rightarrow G2 \rightarrow G3$).
  2. **Performance Analysis:** Grade histograms, Pass/Fail ratios, school and gender comparisons.
  3. **Factor & Correlation:** Study time vs grade, absence impact, parental education heatmaps.
  4. **At-Risk & Top Achievers:** Interactive data tables with CSV download capability.
  5. **BDA Architecture & Hive Hub:** Full interactive architecture diagram and embedded SQL viewer with query results.

---

## 7. Dual Execution Pipeline & Verification Strategy

- **Primary Pipeline (Docker):**
  - Spin up Hadoop HDFS and Hive with `docker compose up -d`.
  - Run `scripts/run_pipeline.sh` inside or against the cluster.
  - Automatically pipe output tables to `output/query-results/`.
- **Dual Offline Runner (Python):**
  - `scripts/local_query_runner.py` uses DuckDB to parse and execute the exact HiveQL queries locally on `data/raw/student-por.csv`.
  - Ensures outputs in `output/query-results/` are always reproducible and consistent even when demonstrating without Docker active.
- **Verification Criteria:**
  - Total records = 649.
  - Grade range = [0, 20].
  - All 17 analytical queries produce valid formatted tables in `output/query-results/`.
  - Streamlit dashboard runs cleanly on `localhost:8501`.

---

## 8. Academic Deliverables

1. `docs/project-report.md`: Formal academic project report formatted for submission.
2. `docs/viva-prep-guide.md`: Evaluator questions, answers, architecture justifications, and demo flow.
3. `README.md`: Complete step-by-step instructions.
