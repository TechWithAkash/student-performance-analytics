# Academic Project Report: Student Performance Analytics Using Hadoop HDFS and Apache Hive

**Course:** Big Data Analytics (BDA)  
**Project Domain:** Educational Data Mining & Distributed Data Warehousing  
**Technologies:** Apache Hadoop, HDFS, Apache Hive, HiveQL, Docker, Streamlit, Plotly, Python  
**Dataset:** UCI Machine Learning Repository — Student Performance Dataset (`student-por.csv`)  

---

## 1. Abstract

Educational data mining offers significant opportunities to improve student learning outcomes, mitigate high failure rates, and enhance administrative resource allocation. This project presents a full Big Data Analytics (BDA) solution to analyze academic performance patterns across secondary school students in Portugal. We employ a modern multi-tiered architecture:
1. **Distributed Storage:** Apache Hadoop HDFS stores the raw, uncurated student dataset.
2. **Distributed Querying & Warehousing:** Apache Hive maps structured schema-on-read abstractions over HDFS blocks and executes analytical HiveQL aggregations.
3. **Analytical Presentation:** A responsive Streamlit dashboard renders KPI trends, academic trajectories, and multi-factor correlations.
4. **Resilience Architecture:** A dual-execution local engine guarantees reproducible analytical results across environments.

Through 17 distinct analytical queries, we evaluate the predictive impact of weekly study time, past failures, attendance records, parental education, and lifestyle factors on final academic performance.

---

## 2. Problem Statement & Objectives

### 2.1 Problem Statement
Educational institutions capture diverse information including demographic backgrounds, socioeconomic conditions, family structure, study habits, and attendance records. Traditional monolithic database management systems struggle to cost-effectively scale, retain raw multi-structured data, and integrate seamlessly with distributed data science ecosystems.

### 2.2 Project Objectives
1. Store student performance data in Apache Hadoop HDFS following distributed file system principles.
2. Build an external schema-on-read table in Apache Hive matching all 33 attributes of the UCI Portuguese dataset.
3. Formulate and execute modular HiveQL scripts to compute descriptive and inferential aggregations.
4. Identify early academic indicators predicting student risk ($G3 < 10$) and top achievement ($G3 \ge 16$).
5. Build an interactive Streamlit visualization dashboard showcasing analytical findings and explaining the underlying Big Data architecture.

---

## 3. Technology Stack & Architectural Design

### 3.1 Technology Stack Summary
| Layer | Component | Purpose |
| :--- | :--- | :--- |
| **Operating System** | macOS / Linux | Host development environment |
| **Storage Layer** | Apache Hadoop HDFS 3.x | Distributed, fault-tolerant block storage |
| **Processing / Warehouse** | Apache Hive 3.x (HiveQL) | SQL-like distributed query execution |
| **Cluster Orchestration** | Docker Compose | Containerized multi-node Hadoop & Hive cluster |
| **Execution Engine** | MapReduce / Tez / SQLite Dual Runner | Distributed task execution & local validation |
| **Presentation Layer** | Streamlit + Plotly | Interactive analytics dashboard & KPI monitoring |

### 3.2 Architectural Flowchart
```
                           ┌──────────────────────────────┐
                           │    UCI Repository Dataset    │
                           │       student-por.csv        │
                           └──────────────┬───────────────┘
                                          │ 1. Download & Validate
                                          ▼
                           ┌──────────────────────────────┐
                           │  Data Ingestion & Integrity  │
                           │  (scripts/download_data.py)  │
                           └──────────────┬───────────────┘
                                          │ 2. hdfs dfs -put
                                          ▼
                           ┌──────────────────────────────┐
                           │      HADOOP HDFS STORAGE     │
                           │ /user/hadoop/student-perf/   │
                           │       (Block Storage)        │
                           └──────────────┬───────────────┘
                                          │ 3. Schema-on-Read
                                          ▼
                           ┌──────────────────────────────┐
                           │         APACHE HIVE          │
                           │  - student_performance_bda   │
                           │  - student_por table         │
                           │  - HiveQL Queries (01 - 07)  │
                           └──────────────┬───────────────┘
                                          │ 4. Analytical Outputs
                                          ▼
                           ┌──────────────────────────────┐
                           │    output/query-results/     │
                           │    CSVs & Summary Reports    │
                           └──────────────┬───────────────┘
                                          │ 5. Visual Dashboard
                                          ▼
                           ┌──────────────────────────────┐
                           │    STREAMLIT DASHBOARD       │
                           │  - KPIs & Progression        │
                           │  - Factor Analysis           │
                           │  - Risk Student Warnings     │
                           │  - Architecture Inspector    │
                           └──────────────────────────────┘
```

---

## 4. Dataset Description & Data Dictionary

The project utilizes the official **UCI Student Performance Dataset** (Portuguese language course, `student-por.csv`). It consists of 649 student records and 33 attributes with zero missing values.

| Column | Type | Description |
| :--- | :--- | :--- |
| `school` | STRING | Student school: Gabriel Pereira (`GP`) or Mousinho da Silveira (`MS`) |
| `sex` | STRING | Student sex: Female (`F`) or Male (`M`) |
| `age` | INT | Age in years (15 to 22) |
| `address` | STRING | Home address type: Urban (`U`) or Rural (`R`) |
| `famsize` | STRING | Family size: Less than or equal to 3 (`LE3`) or Greater than 3 (`GT3`) |
| `Pstatus` | STRING | Parent cohabitation status: Living together (`T`) or Apart (`A`) |
| `Medu` / `Fedu` | INT | Mother / Father education (0=none, 1=primary, 2=5th-9th, 3=secondary, 4=higher) |
| `Mjob` / `Fjob` | STRING | Mother / Father employment: teacher, health, civil services, at home, other |
| `traveltime` | INT | Travel time to school: 1 (<15 min) to 4 (>1 hour) |
| `studytime` | INT | Weekly study time: 1 (<2h), 2 (2-5h), 3 (5-10h), 4 (>10h) |
| `failures` | INT | Past academic course failures (0 to 3) |
| `schoolsup` | STRING | Extra educational support from school (`yes`/`no`) |
| `famsup` | STRING | Family educational support (`yes`/`no`) |
| `higher` | STRING | Wants to take higher education (`yes`/`no`) |
| `internet` | STRING | Internet access at home (`yes`/`no`) |
| `absences` | INT | Total school absences (0 to 93) |
| `G1` | INT | 1st period grade (0 to 20 scale) |
| `G2` | INT | 2nd period grade (0 to 20 scale) |
| `G3` | INT | Final grade (0 to 20 scale; passing threshold $\ge 10$) |

---

## 5. Experimental Analysis & HiveQL Findings

### 5.1 Basic Cohort Metrics
- **Total Student Population:** 649 records
- **Average Final Grade ($G3$):** 11.91 / 20.0 (Standard Deviation: 3.23)
- **Period Progression:** Period 1 ($G1 = 11.40$), Period 2 ($G2 = 11.57$), Final ($G3 = 11.91$)
- **Average Absences:** 3.66 days (Range: 0 to 32 days in main cohort)

### 5.2 Performance Segmentation
- **Pass Rate:** 84.44% (548 passed with $G3 \ge 10$, 101 failed with $G3 < 10$).
- **Gender Differences:** Female students achieved an average final grade of 12.25 vs 11.41 for male students, with lower average absences (3.58 vs 3.78).
- **School Comparison:** Students at GP school averaged 12.57 vs 10.65 at MS school.

### 5.3 Key Factors Influencing Academic Outcome
1. **Weekly Study Time:** A direct positive correlation was observed:
   - $< 2$ hours/week: Avg $G3 = 10.66$
   - $2 - 5$ hours/week: Avg $G3 = 11.52$
   - $5 - 10$ hours/week: Avg $G3 = 13.07$
   - $> 10$ hours/week: Avg $G3 = 14.33$
2. **Prior Failures:** Students with 0 prior failures achieved an average final grade of 12.55, dropping steeply to 8.65 for students with 1 failure, and 7.15 for students with $\ge 2$ failures.
3. **Parental Education:** Students whose mothers had higher education ($Medu = 4$) averaged $G3 = 12.87$, compared to $10.15$ for students whose mothers had primary education or less.
4. **Desire for Higher Education:** Students aiming for university/higher education achieved an average grade of 12.21 vs 8.68 for students without higher education aspirations.

---

## 6. Conclusion & Viva Defense Summary

The project demonstrates how Big Data frameworks like Hadoop and Hive allow institutions to transform raw, semi-structured academic logs into valuable decision support:
- **Hadoop HDFS** provides scalable, cost-effective distributed storage decoupled from compute.
- **Apache Hive** enables schema-on-read analytics using familiar SQL abstractions without requiring low-level MapReduce code.
- **Streamlit** provides administrators with an interactive lens to track KPIs and intervene early for at-risk students.
