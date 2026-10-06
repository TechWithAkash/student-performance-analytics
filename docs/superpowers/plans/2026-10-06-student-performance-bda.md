# Student Performance BDA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and execute an end-to-end Big Data Analytics (BDA) project analyzing student performance using Hadoop HDFS, Apache Hive (HiveQL), dual query execution, and an interactive Streamlit dashboard.

**Architecture:** A multi-layered BDA pipeline with distributed storage (Hadoop HDFS) and warehouse analytics (Apache Hive), supplemented by an offline DuckDB query runner for 100% demo safety, feeding an interactive Streamlit analytics dashboard.

**Tech Stack:** Python 3.11+, Hadoop HDFS 3.x, Apache Hive 3.x, Docker Compose, DuckDB, Streamlit, Plotly, Pandas.

**Spec:** [`docs/superpowers/specs/2026-10-06-student-performance-bda-design.md`](file:///Users/akashvishwakarma/bda-project/docs/superpowers/specs/2026-10-06-student-performance-bda-design.md)

## Global Constraints

- Primary dataset: Official UCI Student Performance Portuguese dataset (`student-por.csv`), 649 records, 33 columns.
- File delimiter: Semicolon (`;`).
- Output format: SQL scripts must output reproducible results to `output/query-results/`.
- Dual execution: All HiveQL queries must run either in the Docker Hive cluster or via the local fallback runner.
- Web UI: Streamlit must run locally at `http://localhost:8501` without errors.

---

### Task 1: Project Scaffolding & Environment Setup

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `scripts/__init__.py`
- Test: `tests/test_scaffolding.py`

**Interfaces:**
- Produces: Base directory structure (`data/raw`, `data/processed`, `docker`, `hive`, `output/query-results`, `scripts`, `docs`, `tests`), Python virtual environment.

- [ ] **Step 1: Write the failing test for project scaffolding**

```python
# tests/test_scaffolding.py
import os
from pathlib import Path

def test_directory_structure_exists():
    required_dirs = [
        "data/raw",
        "data/processed",
        "docker",
        "hive",
        "output/query-results",
        "scripts",
        "docs",
        "tests",
    ]
    for d in required_dirs:
        assert Path(d).is_dir(), f"Missing directory: {d}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_scaffolding.py`
Expected: FAIL (directories do not exist yet)

- [ ] **Step 3: Create directory structure, requirements.txt, and .gitignore**

Create directories:
```bash
mkdir -p data/raw data/processed docker hive output/query-results scripts docs tests
touch scripts/__init__.py
```

Create `requirements.txt`:
```text
streamlit>=1.35.0
pandas>=2.2.0
plotly>=5.22.0
duckdb>=0.10.0
pytest>=8.0.0
requests>=2.31.0
```

Create `.gitignore`:
```text
.venv/
__pycache__/
*.pyc
.pytest_cache/
.DS_Store
data/raw/*.zip
*.log
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_scaffolding.py`
Expected: PASS

- [ ] **Step 5: Commit scaffolding**

```bash
git add .gitignore requirements.txt scripts/__init__.py tests/test_scaffolding.py
git commit -m "chore: scaffold project directories and requirements"
```

---

### Task 2: Data Ingestion & Validation Pipeline

**Files:**
- Create: `scripts/download_data.py`
- Test: `tests/test_data_validation.py`
- Output: `data/raw/student-por.csv`, `data/processed/student_por_clean.csv`

**Interfaces:**
- Produces: `fetch_and_prepare_dataset(dest_dir: str) -> dict` returning record count and column list.

- [ ] **Step 1: Write failing test for data validation**

```python
# tests/test_data_validation.py
import os
import pandas as pd
from pathlib import Path
from scripts.download_data import validate_dataset

def test_validate_dataset_schema():
    csv_path = Path("data/raw/student-por.csv")
    assert csv_path.exists(), "student-por.csv does not exist"
    
    df = pd.read_csv(csv_path, sep=";")
    assert len(df) == 649, f"Expected 649 rows, got {len(df)}"
    assert len(df.columns) == 33, f"Expected 33 columns, got {len(df.columns)}"
    assert "G1" in df.columns and "G2" in df.columns and "G3" in df.columns
    assert df["G3"].min() >= 0 and df["G3"].max() <= 20
    assert not df.isnull().values.any(), "Dataset contains unexpected NULL values"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_validation.py`
Expected: FAIL (missing `scripts/download_data.py` and `data/raw/student-por.csv`)

- [ ] **Step 3: Implement `scripts/download_data.py`**

```python
# scripts/download_data.py
import io
import os
import zipfile
import requests
import pandas as pd
from pathlib import Path

UCI_URL = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"

def download_and_extract_data(target_raw_dir="data/raw", target_processed_dir="data/processed"):
    raw_path = Path(target_raw_dir)
    processed_path = Path(target_processed_dir)
    raw_path.mkdir(parents=True, exist_ok=True)
    processed_path.mkdir(parents=True, exist_ok=True)

    dest_csv = raw_path / "student-por.csv"
    if not dest_csv.exists():
        print(f"Fetching dataset from {UCI_URL}...")
        resp = requests.get(UCI_URL, timeout=30)
        resp.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            z.extractall(raw_path)
            
        # The zip contains inner student.zip or direct csvs
        inner_zip = raw_path / "student.zip"
        if inner_zip.exists():
            with zipfile.ZipFile(inner_zip) as iz:
                iz.extractall(raw_path)
                
    if not dest_csv.exists():
        raise FileNotFoundError(f"Failed to find student-por.csv after extraction at {dest_csv}")

    df = pd.read_csv(dest_csv, sep=";")
    print(f"Validated student-por.csv: {df.shape[0]} rows, {df.shape[1]} columns.")
    
    clean_csv = processed_path / "student_por_clean.csv"
    df.to_csv(clean_csv, sep=";", index=False)
    print(f"Saved processed dataset to {clean_csv}")
    return df

def validate_dataset(csv_path="data/raw/student-por.csv"):
    df = pd.read_csv(csv_path, sep=";")
    assert len(df) == 649, f"Expected 649 rows, got {len(df)}"
    assert len(df.columns) == 33, f"Expected 33 columns, got {len(df.columns)}"
    return True

if __name__ == "__main__":
    download_and_extract_data()
    validate_dataset()
```

- [ ] **Step 4: Execute download script and run tests**

Run:
```bash
python scripts/download_data.py
pytest tests/test_data_validation.py
```
Expected: PASS with 649 records and 33 columns.

- [ ] **Step 5: Commit data ingestion pipeline**

```bash
git add scripts/download_data.py tests/test_data_validation.py data/raw/student-por.csv data/processed/student_por_clean.csv
git commit -m "feat: implement data ingestion and validation for UCI student-por dataset"
```

---

### Task 3: Dockerized Hadoop HDFS & Hive Cluster Setup

**Files:**
- Create: `docker/docker-compose.yml`
- Create: `docker/init-hadoop.sh`
- Test: `tests/test_docker_config.py`

**Interfaces:**
- Produces: Multi-container setup containing NameNode (`9870`, `9000`), DataNode (`9864`), HiveServer2 (`10000`), Hive Metastore (`9083`).

- [ ] **Step 1: Write test for docker compose configuration syntax**

```python
# tests/test_docker_config.py
from pathlib import Path
import yaml

def test_docker_compose_syntax():
    compose_path = Path("docker/docker-compose.yml")
    assert compose_path.exists(), "docker-compose.yml does not exist"
    with open(compose_path, "r") as f:
        config = yaml.safe_load(f)
    services = config.get("services", {})
    assert "namenode" in services
    assert "datanode" in services
    assert "hive-server" in services
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_docker_config.py`
Expected: FAIL

- [ ] **Step 3: Implement `docker/docker-compose.yml` & `docker/init-hadoop.sh`**

```yaml
# docker/docker-compose.yml
version: "3.8"

services:
  namenode:
    image: bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
    container_name: namenode
    restart: always
    ports:
      - "9870:9870"
      - "9000:9000"
    environment:
      - CLUSTER_NAME=student_bda_cluster
    env_file:
      - ./hadoop.env
    volumes:
      - hadoop_namenode:/hadoop/dfs/name
      - ../data:/data

  datanode:
    image: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
    container_name: datanode
    restart: always
    ports:
      - "9864:9864"
    env_file:
      - ./hadoop.env
    volumes:
      - hadoop_datanode:/hadoop/dfs/data
    depends_on:
      - namenode

  hive-server:
    image: bde2020/hive:2.3.2-postgresql-metastore
    container_name: hive-server
    restart: always
    ports:
      - "10000:10000"
      - "10002:10002"
    env_file:
      - ./hadoop.env
    environment:
      - HIVE_CORE_CONF_javax_jdo_option_ConnectionURL=jdbc:postgresql://hive-metastore-postgresql:5432/metastore
    depends_on:
      - namenode
      - datanode
    volumes:
      - ../hive:/hive
      - ../data:/data

volumes:
  hadoop_namenode:
  hadoop_datanode:
```

Create `docker/hadoop.env`:
```text
CORE_CONF_fs_defaultFS=hdfs://namenode:9000
CORE_CONF_hadoop_http_staticuser_user=root
HDFS_CONF_dfs_replication=1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_docker_config.py`
Expected: PASS

- [ ] **Step 5: Commit docker configuration**

```bash
git add docker/ tests/test_docker_config.py
git commit -m "feat: add Docker Compose cluster definition for Hadoop and Hive"
```

---

### Task 4: Modular HiveQL Scripts (01 to 07)

**Files:**
- Create: `hive/01_create_database.sql`
- Create: `hive/02_create_table.sql`
- Create: `hive/03_load_data.sql`
- Create: `hive/04_basic_analysis.sql`
- Create: `hive/05_performance_analysis.sql`
- Create: `hive/06_factor_analysis.sql`
- Create: `hive/07_advanced_analysis.sql`
- Test: `tests/test_hive_scripts.py`

**Interfaces:**
- Produces: 7 production-grade HiveQL scripts containing all 17 lecture queries.

- [ ] **Step 1: Write test verifying presence and key statements in all 7 scripts**

```python
# tests/test_hive_scripts.py
from pathlib import Path

def test_all_seven_scripts_exist():
    scripts = [
        "01_create_database.sql",
        "02_create_table.sql",
        "03_load_data.sql",
        "04_basic_analysis.sql",
        "05_performance_analysis.sql",
        "06_factor_analysis.sql",
        "07_advanced_analysis.sql",
    ]
    for s in scripts:
        p = Path("hive") / s
        assert p.exists(), f"Missing HiveQL script {s}"
        assert p.stat().st_size > 0, f"Script {s} is empty"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_hive_scripts.py`
Expected: FAIL

- [ ] **Step 3: Implement all 7 HiveQL scripts**

`hive/01_create_database.sql`:
```sql
CREATE DATABASE IF NOT EXISTS student_performance_bda;
USE student_performance_bda;
```

`hive/02_create_table.sql`:
```sql
USE student_performance_bda;

DROP TABLE IF EXISTS student_por;

CREATE EXTERNAL TABLE IF NOT EXISTS student_por (
    school STRING,
    sex STRING,
    age INT,
    address STRING,
    famsize STRING,
    Pstatus STRING,
    Medu INT,
    Fedu INT,
    Mjob STRING,
    Fjob STRING,
    reason STRING,
    guardian STRING,
    traveltime INT,
    studytime INT,
    failures INT,
    schoolsup STRING,
    famsup STRING,
    paid STRING,
    activities STRING,
    nursery STRING,
    higher STRING,
    internet STRING,
    romantic STRING,
    famrel INT,
    freetime INT,
    goout INT,
    Dalc INT,
    Walc INT,
    health INT,
    absences INT,
    G1 INT,
    G2 INT,
    G3 INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
STORED AS TEXTFILE
LOCATION '/user/hadoop/student-performance/'
TBLPROPERTIES ("skip.header.line.count"="1");
```

`hive/03_load_data.sql`:
```sql
USE student_performance_bda;
-- For local/container testing:
LOAD DATA LOCAL INPATH '/data/raw/student-por.csv' OVERWRITE INTO TABLE student_por;
```

`hive/04_basic_analysis.sql`:
```sql
USE student_performance_bda;

-- Query 1: Total Number of Students
SELECT COUNT(*) AS total_students FROM student_por;

-- Query 2: Final Grade Statistics
SELECT 
    ROUND(AVG(G3), 2) AS avg_final_grade,
    MIN(G3) AS min_final_grade,
    MAX(G3) AS max_final_grade,
    ROUND(STDDEV(G3), 2) AS stddev_final_grade
FROM student_por;

-- Query 3: Progression of Period Grades
SELECT 
    ROUND(AVG(G1), 2) AS avg_G1,
    ROUND(AVG(G2), 2) AS avg_G2,
    ROUND(AVG(G3), 2) AS avg_G3
FROM student_por;

-- Query 4: School Absence Statistics
SELECT 
    ROUND(AVG(absences), 2) AS avg_absences,
    MIN(absences) AS min_absences,
    MAX(absences) AS max_absences
FROM student_por;
```

`hive/05_performance_analysis.sql`:
```sql
USE student_performance_bda;

-- Query 5: Grade Comparison by Gender
SELECT 
    sex,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade,
    ROUND(AVG(absences), 2) AS avg_absences
FROM student_por
GROUP BY sex;

-- Query 6: Performance by School
SELECT 
    school,
    COUNT(*) AS total_students,
    ROUND(AVG(G3), 2) AS avg_final_grade,
    ROUND(AVG(studytime), 2) AS avg_study_time
FROM student_por
GROUP BY school;

-- Query 7: Pass vs Fail Ratio (Passing grade >= 10 out of 20)
SELECT 
    CASE WHEN G3 >= 10 THEN 'Passed' ELSE 'Failed' END AS status,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM student_por), 2) AS percentage
FROM student_por
GROUP BY CASE WHEN G3 >= 10 THEN 'Passed' ELSE 'Failed' END;

-- Query 8: Portuguese Grade Categories
SELECT 
    CASE 
        WHEN G3 < 10 THEN '01. Fail (0-9)'
        WHEN G3 BETWEEN 10 AND 13 THEN '02. Sufficient (10-13)'
        WHEN G3 BETWEEN 14 AND 15 THEN '03. Good (14-15)'
        ELSE '04. Excellent (16-20)'
    END AS grade_category,
    COUNT(*) AS student_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM student_por), 2) AS percentage
FROM student_por
GROUP BY CASE 
        WHEN G3 < 10 THEN '01. Fail (0-9)'
        WHEN G3 BETWEEN 10 AND 13 THEN '02. Sufficient (10-13)'
        WHEN G3 BETWEEN 14 AND 15 THEN '03. Good (14-15)'
        ELSE '04. Excellent (16-20)'
    END
ORDER BY grade_category;
```

`hive/06_factor_analysis.sql`:
```sql
USE student_performance_bda;

-- Query 9: Weekly Study Time vs Final Grade
SELECT 
    studytime,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade,
    ROUND(AVG(failures), 2) AS avg_failures
FROM student_por
GROUP BY studytime
ORDER BY studytime;

-- Query 10: Previous Failures vs Final Grade
SELECT 
    failures,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade
FROM student_por
GROUP BY failures
ORDER BY failures;

-- Query 11: Absences Quartiles vs Final Grade
SELECT 
    CASE 
        WHEN absences = 0 THEN '00. Zero Absences'
        WHEN absences BETWEEN 1 AND 4 THEN '01. Low (1-4)'
        WHEN absences BETWEEN 5 AND 9 THEN '02. Moderate (5-9)'
        ELSE '03. High (10+)'
    END AS absence_group,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade
FROM student_por
GROUP BY CASE 
        WHEN absences = 0 THEN '00. Zero Absences'
        WHEN absences BETWEEN 1 AND 4 THEN '01. Low (1-4)'
        WHEN absences BETWEEN 5 AND 9 THEN '02. Moderate (5-9)'
        ELSE '03. High (10+)'
    END
ORDER BY absence_group;

-- Query 12: Parental Education Impact
SELECT 
    Medu AS mother_education,
    Fedu AS father_education,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade
FROM student_por
GROUP BY Medu, Fedu
ORDER BY Medu DESC, Fedu DESC;

-- Query 13: Educational Support Impact
SELECT 
    schoolsup,
    famsup,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade
FROM student_por
GROUP BY schoolsup, famsup;

-- Query 14: Desire for Higher Education & Internet Access
SELECT 
    higher,
    internet,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade
FROM student_por
GROUP BY higher, internet;
```

`hive/07_advanced_analysis.sql`:
```sql
USE student_performance_bda;

-- Query 15: Academic Risk Identification (Failures > 0 or G3 < 10 or Absences > 10)
SELECT 
    school,
    sex,
    age,
    studytime,
    failures,
    absences,
    G1,
    G2,
    G3
FROM student_por
WHERE G3 < 10 OR failures > 0 OR absences > 10
ORDER BY G3 ASC, absences DESC
LIMIT 20;

-- Query 16: Top Academic Achievers (G3 >= 16) Profile
SELECT 
    COUNT(*) AS top_student_count,
    ROUND(AVG(studytime), 2) AS avg_study_time,
    ROUND(AVG(absences), 2) AS avg_absences,
    ROUND(AVG(failures), 2) AS avg_failures,
    ROUND(SUM(CASE WHEN higher = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_wanting_higher_ed
FROM student_por
WHERE G3 >= 16;

-- Query 17: Alcohol Consumption vs Final Grades
SELECT 
    Walc AS weekend_alcohol,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade,
    ROUND(AVG(absences), 2) AS avg_absences
FROM student_por
GROUP BY Walc
ORDER BY Walc;
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_hive_scripts.py`
Expected: PASS

- [ ] **Step 5: Commit HiveQL scripts**

```bash
git add hive/ tests/test_hive_scripts.py
git commit -m "feat: implement all 7 modular HiveQL scripts for BDA analytics"
```

---

### Task 5: Dual Query Runner & Pipeline Automation

**Files:**
- Create: `scripts/local_query_runner.py`
- Create: `scripts/run_pipeline.sh`
- Test: `tests/test_query_runner.py`
- Output: `output/query-results/*.csv`

**Interfaces:**
- Produces: `run_all_queries(csv_path: str, output_dir: str) -> dict` returning dictionary of query results and writing CSV summaries.

- [ ] **Step 1: Write test for local query runner**

```python
# tests/test_query_runner.py
from pathlib import Path
from scripts.local_query_runner import run_all_queries

def test_local_query_runner_generates_outputs():
    results = run_all_queries("data/raw/student-por.csv", "output/query-results")
    assert "total_students" in results
    assert results["total_students"] == 649
    
    assert Path("output/query-results/04_basic_analysis.csv").exists()
    assert Path("output/query-results/05_performance_analysis.csv").exists()
    assert Path("output/query-results/06_factor_analysis.csv").exists()
    assert Path("output/query-results/07_advanced_analysis.csv").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_query_runner.py`
Expected: FAIL

- [ ] **Step 3: Implement `scripts/local_query_runner.py` and `scripts/run_pipeline.sh`**

Implement `scripts/local_query_runner.py` using DuckDB to parse and execute queries against `student-por.csv` with identical semantics and dump results to `output/query-results/`.

Implement executable `scripts/run_pipeline.sh`:
- Checks Docker status
- Copies dataset to HDFS if container active
- Runs Hive scripts if container active
- Runs local Python query runner to guarantee output generation

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_query_runner.py`
Expected: PASS and all output CSVs populated.

- [ ] **Step 5: Commit query runner & pipeline**

```bash
git add scripts/ tests/test_query_runner.py output/query-results/
git commit -m "feat: implement dual execution runner and pipeline automation"
```

---

### Task 6: Interactive Streamlit Dashboard

**Files:**
- Create: `app.py`
- Test: `tests/test_app.py`

**Interfaces:**
- Produces: High-grade Streamlit application with custom styling, 5 interactive tabs, Plotly charts, risk tables, and architecture visualizer.

- [ ] **Step 1: Write test verifying Streamlit app structure and helper functions**

```python
# tests/test_app.py
import pytest
import pandas as pd
from app import load_data, calculate_kpis

def test_load_data():
    df = load_data("data/raw/student-por.csv")
    assert df is not None
    assert len(df) == 649

def test_calculate_kpis():
    df = load_data("data/raw/student-por.csv")
    kpis = calculate_kpis(df)
    assert kpis["total_students"] == 649
    assert kpis["pass_rate"] > 0
    assert 0 <= kpis["avg_g3"] <= 20
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_app.py`
Expected: FAIL (missing `app.py`)

- [ ] **Step 3: Implement `app.py`**

Build `app.py` featuring:
- Custom CSS with styled metric cards, gradient banners, and responsive cards
- 5 comprehensive tabs:
  1. Executive KPI Overview (Pass Rate, Total Students, Average G3, Attendance)
  2. Academic Performance Breakdown (Distribution, Gender comparison, School comparison)
  3. Factor & Lifestyle Analysis (Study time, Absences, Alcohol consumption, Parental education)
  4. Student Risk & Achiever Drill-Down (Interactive table with export)
  5. BDA Technical Architecture & Hive Hub (Interactive pipeline diagram and code inspector)

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_app.py`
Expected: PASS

- [ ] **Step 5: Commit Streamlit application**

```bash
git add app.py tests/test_app.py
git commit -m "feat: implement interactive Streamlit analytics dashboard"
```

---

### Task 7: Comprehensive Academic Documentation & Viva Preparation Guide

**Files:**
- Create: `docs/project-report.md`
- Create: `docs/viva-prep-guide.md`
- Create: `README.md`
- Test: `tests/test_docs.py`

**Interfaces:**
- Produces: Submission-ready academic project report, comprehensive viva Q&A guide, and quickstart documentation.

- [ ] **Step 1: Write test verifying completeness of documentation**

```python
# tests/test_docs.py
from pathlib import Path

def test_documentation_files_exist_and_populated():
    docs = ["docs/project-report.md", "docs/viva-prep-guide.md", "README.md"]
    for d in docs:
        p = Path(d)
        assert p.exists(), f"Missing doc file: {d}"
        assert p.stat().st_size > 500, f"Doc file {d} too short"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_docs.py`
Expected: FAIL

- [ ] **Step 3: Create `docs/project-report.md`, `docs/viva-prep-guide.md`, and `README.md`**

Write:
- `docs/project-report.md`: Complete academic project report containing Abstract, Problem Statement, BDA Architecture, Data Dictionary, Analysis Results, and Conclusion.
- `docs/viva-prep-guide.md`: Detailed viva questions and answers covering HDFS, Hive internals, HiveQL vs SQL, and live demonstration checklist.
- `README.md`: Clear setup and execution guide with screenshots/command snippets.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_docs.py`
Expected: PASS

- [ ] **Step 5: Commit documentation**

```bash
git add docs/ README.md tests/test_docs.py
git commit -m "docs: add formal academic project report, viva guide, and README"
```

---

### Task 8: End-to-End Verification & Verification Gate

**Files:**
- Test: `tests/test_full_suite.py`

- [ ] **Step 1: Run complete test suite**

Run: `pytest tests/ -v`
Expected: All tests PASS across data validation, docker config, hive scripts, query runner, dashboard, and documentation.

- [ ] **Step 2: Run data pipeline end-to-end**

Run: `python scripts/download_data.py && python scripts/local_query_runner.py`
Expected: Clean execution, 17 queries processed, output CSVs generated.

- [ ] **Step 3: Smoke test Streamlit server launch**

Run headless test:
`streamlit run app.py --server.headless=true --server.port=8501 & sleep 3; curl -I http://localhost:8501; pkill -f streamlit`
Expected: HTTP 200 OK.

- [ ] **Step 4: Final Git commit & status check**

```bash
git status
git commit -am "chore: complete BDA student performance project end-to-end"
```
