# Viva & Presentation Preparation Guide: Student Performance BDA

This guide equips you with concise, authoritative answers to anticipated viva/evaluation questions, architectural justifications, and a step-by-step demonstration checklist for professors.

---

## 1. Top Viva Questions & Authoritative Answers

### Q1: What is the core problem this Big Data project addresses?
> **Answer:**  
> Educational institutions generate multi-dimensional student datasets (demographics, habits, grades, socioeconomic factors). This project builds an end-to-end Big Data Analytics pipeline using **Hadoop HDFS** for distributed storage and **Apache Hive (HiveQL)** for SQL-based analytical querying to discover actionable academic patterns, identify high-risk students, and present findings via an interactive **Streamlit** dashboard.

---

### Q2: Why use Hadoop HDFS instead of a traditional RDBMS like MySQL or PostgreSQL?
> **Answer:**  
> 1. **Decoupled Architecture:** In HDFS, storage scales independently of compute.
> 2. **Schema-on-Read:** Unlike RDBMS (which enforces schema on write), HDFS stores the raw, untouched dataset. Apache Hive applies schemas dynamically during query execution.
> 3. **Fault Tolerance & Horizontal Scalability:** HDFS splits files into distributed blocks across commodity hardware with automatic replication.
> 4. **Ecosystem Integration:** Once stored in HDFS, the data can be consumed by Hive, Spark, Presto, and ML pipelines simultaneously.

---

### Q3: What is the architectural difference between Managed and External tables in Hive?
> **Answer:**  
> - **Managed Table (`INTERNAL`):** Hive manages both metadata in the Metastore AND the underlying data in `/user/hive/warehouse/`. Dropping the table deletes both metadata and raw data files.
> - **External Table (`EXTERNAL`):** Hive manages only the metadata. The data resides at an explicit HDFS path (`LOCATION '/user/hadoop/student-performance/'`). Dropping an external table drops only the schema definition; the raw data in HDFS remains completely safe.
> - *In this project, we defined `student_por` as an EXTERNAL table to preserve data lake integrity.*

---

### Q4: How does Apache Hive execute a query written in HiveQL?
> **Answer:**  
> 1. **Parser & Semantic Analyzer:** Converts the HiveQL statement into an Abstract Syntax Tree (AST) and validates table schemas against the Hive Metastore.
> 2. **Logical & Physical Planner:** Transforms the AST into an execution plan and optimizes it (partition pruning, pushdown predicates).
> 3. **Execution Engine:** Converts the plan into distributed execution jobs (MapReduce, Tez, or Spark tasks) that execute across DataNodes in the cluster.
> 4. **Result Fetch:** Aggregated outputs are written to HDFS temporary sinks and returned to the client.

---

### Q5: Does Streamlit replace Hadoop or Hive?
> **Answer:**  
> **No.** Streamlit is strictly the **Presentation / Visualization Layer**.  
> The architectural separation is:
> - **Hadoop HDFS** = Distributed Storage Layer
> - **Apache Hive** = Distributed Warehouse & Query Processing Layer
> - **Streamlit** = Interactive User Interface & Decision Support Layer  
> Streamlit visualizes the aggregated data and queries produced by the Big Data warehouse.

---

### Q6: What were the most significant analytical findings from your 17 queries?
> **Answer:**  
> 1. **Study Time Direct Impact:** Increasing weekly study time from $<2$ hours to $>10$ hours improved average grades from $10.66$ to $14.33$ points (out of 20).
> 2. **Prior Failures as Risk Indicator:** Students with zero failures averaged $12.55$, while even a single past failure dropped average performance below passing ($8.65$).
> 3. **Parental Education Correlation:** Higher maternal education ($Medu=4$) corresponded to an average grade of $12.87$ vs $10.15$ for primary education.
> 4. **Aspiration for Higher Education:** Wanting higher education was associated with a $+3.5$ point increase in final grades.

---

## 2. Step-by-Step Live Demonstration Checklist

Follow this exact sequence when presenting to the evaluator:

```text
Step 1: Introduce Problem Statement & Architecture Diagram
        (Show Slide/Tab 5 in Streamlit or Architecture in report)
        ↓
Step 2: Show Raw Dataset Integrity
        terminal: head -n 5 data/raw/student-por.csv
        ↓
Step 3: Show Hadoop HDFS Status (if running Docker)
        terminal: docker exec -it student_bda_namenode hdfs dfs -ls /user/hadoop/student-performance/
        ↓
Step 4: Demonstrate HiveQL Script Structure
        Show files: hive/01_create_database.sql through hive/07_advanced_analysis.sql
        ↓
Step 5: Execute Queries & Show Generated Outputs
        terminal: ./scripts/run_pipeline.sh
        Show outputs: cat output/query-results/04_basic_analysis.csv
        ↓
Step 6: Launch Streamlit Dashboard
        terminal: streamlit run app.py
        ↓
Step 7: Demonstrate Interactive Filtering & Risk Detection
        - Adjust study time slider & observe grade chart update
        - Show "At-Risk Students" tab and download CSV
        - Open "BDA Architecture & Hive Hub" tab to show SQL query inspector
```

---

## 3. Useful Big Data Terminal Commands Cheatsheet

| Task | Command |
| :--- | :--- |
| **Start Docker Cluster** | `docker compose -f docker/docker-compose.yml up -d` |
| **Stop Docker Cluster** | `docker compose -f docker/docker-compose.yml down` |
| **Check HDFS Directory** | `docker exec -it student_bda_namenode hdfs dfs -ls /user/hadoop/` |
| **Upload to HDFS** | `docker exec -it student_bda_namenode hdfs dfs -put /data/raw/student-por.csv /user/hadoop/` |
| **Read from HDFS** | `docker exec -it student_bda_namenode hdfs dfs -cat /user/hadoop/student-performance/student-por.csv \| head -n 5` |
| **Execute Full Pipeline** | `./scripts/run_pipeline.sh` |
| **Launch Dashboard** | `streamlit run app.py` |
