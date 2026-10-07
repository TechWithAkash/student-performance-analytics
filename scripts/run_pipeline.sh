#!/usr/bin/env bash
# ==============================================================================
# scripts/run_pipeline.sh
# End-to-end Big Data Analytics execution pipeline:
# 1. Downloads & validates UCI dataset
# 2. Uploads to Hadoop HDFS (if Docker cluster is active)
# 3. Executes HiveQL scripts (if Docker cluster is active)
# 4. Executes dual query runner to guarantee output generation
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT_DIR"

echo "=================================================================="
echo " Starting Student Performance Big Data Analytics Pipeline"
echo "=================================================================="

# 1. Data Ingestion & Validation
echo -e "\n[Step 1/4] Downloading and validating UCI student-por dataset..."
python3 scripts/download_data.py

# 2. Check Docker HDFS Status
echo -e "\n[Step 2/4] Checking Hadoop HDFS and Hive Docker Cluster..."
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "student_bda_namenode"; then
    echo "Hadoop NameNode container detected."
    echo "Ingesting data into HDFS /user/hadoop/student-performance/..."
    docker exec -i student_bda_namenode hdfs dfs -mkdir -p /user/hadoop/student-performance/ || true
    docker exec -i student_bda_namenode hdfs dfs -put -f /data/raw/student-por.csv /user/hadoop/student-performance/student-por.csv
    echo "HDFS directory contents:"
    docker exec -i student_bda_namenode hdfs dfs -ls /user/hadoop/student-performance/
else
    echo "Notice: Docker is not active (which is completely normal)."
    echo "Falling back to local execution engine for 17 HiveQL queries..."
fi

# 3. Execute Dual Query Runner
echo -e "\n[Step 3/4] Executing 17 HiveQL analytical queries..."
python3 scripts/local_query_runner.py

# 4. Show Summary
echo -e "\n[Step 4/4] Pipeline Complete! Results generated in output/query-results/:"
ls -lh output/query-results/

echo -e "\n=================================================================="
echo " Pipeline Finished Successfully!"
echo " To launch the interactive dashboard, run:"
echo "   streamlit run app.py"
echo "=================================================================="
