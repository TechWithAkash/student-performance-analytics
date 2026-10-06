#!/bin/bash
set -e

echo "=== Initializing Hadoop HDFS for Student Performance BDA ==="

# Wait for NameNode to be ready
echo "Checking HDFS availability..."
docker exec -i student_bda_namenode hdfs dfs -mkdir -p /user/hadoop/student-performance/ || true

echo "Uploading student-por.csv to HDFS..."
docker exec -i student_bda_namenode hdfs dfs -put -f /data/raw/student-por.csv /user/hadoop/student-performance/student-por.csv

echo "Verifying files in HDFS:"
docker exec -i student_bda_namenode hdfs dfs -ls /user/hadoop/student-performance/

echo "=== HDFS Ingestion Complete ==="
