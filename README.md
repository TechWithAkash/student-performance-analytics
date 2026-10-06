# Student Performance Analytics Using Hadoop HDFS & Apache Hive

An end-to-end Big Data Analytics (BDA) platform that ingests, stores, queries, and visualizes student academic performance data from the UCI Machine Learning Repository.

---

## 🏛️ Project Architecture

```
┌──────────────────┐       ┌───────────────────────┐       ┌──────────────────────┐       ┌──────────────────┐
│   UCI DATASET    │ ────> │      HADOOP HDFS      │ ────> │     APACHE HIVE      │ ────> │    STREAMLIT     │
│ student-por.csv  │       │ /user/hadoop/student/ │       │  HiveQL (01 to 07)   │       │ Dynamic Reports  │
└──────────────────┘       └───────────────────────┘       └──────────────────────┘       └──────────────────┘
     (Raw CSV)                (Storage Layer)                 (Warehouse Query)             (Presentation)
```

- **Distributed Storage:** Apache Hadoop HDFS provides scalable, fault-tolerant block storage.
- **Data Warehousing & Querying:** Apache Hive enables schema-on-read querying via HiveQL (17 analytical queries across 7 modular scripts).
- **Dual Execution Engine:** Dual-mode runner enables execution inside a Docker cluster or locally via an in-memory SQL engine for guaranteed demo reproducibility.
- **Interactive Visualization:** Streamlit dashboard featuring cohort KPIs, progression charts, risk identification, and an interactive architecture inspector.

---

## 📁 Repository Structure

```text
bda-project/
├── data/
│   ├── raw/
│   │   └── student-por.csv            # Official UCI Portuguese dataset (649 rows, 33 attributes)
│   └── processed/
│       └── student_por_clean.csv      # Cleaned and validated dataset
├── docker/
│   ├── docker-compose.yml             # Multi-container Hadoop (NameNode, DataNode) & Hive
│   └── hadoop.env                     # Hadoop environment variables
├── hive/
│   ├── 01_create_database.sql         # CREATE DATABASE IF NOT EXISTS
│   ├── 02_create_table.sql            # CREATE EXTERNAL TABLE with 33 attributes
│   ├── 03_load_data.sql               # Data loading statements
│   ├── 04_basic_analysis.sql          # Basic statistics (Q1 to Q4)
│   ├── 05_performance_analysis.sql    # Gender & school comparison (Q5 to Q8)
│   ├── 06_factor_analysis.sql         # Study time, absences, parental edu (Q9 to Q14)
│   └── 07_advanced_analysis.sql       # Risk student detection & top achievers (Q15 to Q17)
├── output/
│   └── query-results/                 # Generated analytical CSVs and text summary reports
├── scripts/
│   ├── download_data.py               # Ingestion and schema validator
│   ├── run_pipeline.sh                # Automated end-to-end pipeline runner
│   └── local_query_runner.py          # Dual execution SQL engine
├── docs/
│   ├── project-report.md              # Academic submission report
│   └── viva-prep-guide.md             # Viva Q&A and demo checklist
├── app.py                             # Interactive Streamlit dashboard
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+
- (Optional for cluster demo) Docker & Docker Compose

### 2. Setup Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the End-to-End Pipeline
To download the dataset, validate schemas, and run all 17 analytical queries:
```bash
./scripts/run_pipeline.sh
```
This executes the queries and populates `output/query-results/`.

### 4. Launch the Interactive Streamlit Dashboard
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🐳 Running with Docker (Hadoop + Hive Cluster)

To spin up the containerized Hadoop and Hive cluster:
```bash
# 1. Start the cluster
docker compose -f docker/docker-compose.yml up -d

# 2. Ingest data to HDFS
docker exec -i student_bda_namenode hdfs dfs -mkdir -p /user/hadoop/student-performance/
docker exec -i student_bda_namenode hdfs dfs -put -f /data/raw/student-por.csv /user/hadoop/student-performance/

# 3. View HDFS files
docker exec -i student_bda_namenode hdfs dfs -ls /user/hadoop/student-performance/

# 4. Stop the cluster when done
docker compose -f docker/docker-compose.yml down
```

---

## 📚 Academic Documentation
- **Submission Report:** [`docs/project-report.md`](docs/project-report.md)
- **Viva Preparation & Questions:** [`docs/viva-prep-guide.md`](docs/viva-prep-guide.md)
- **Technical Lecture Notes:** [`Student_Performance_BDA_Technical_Lecture (1).md`](Student_Performance_BDA_Technical_Lecture%20(1).md)
