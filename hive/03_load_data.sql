-- ==========================================================
-- Big Data Analytics Project: Student Performance Analytics
-- Script 03: Load Data into Hive
-- ==========================================================

USE student_performance_bda;

-- Note: When using EXTERNAL TABLE pointing to LOCATION '/user/hadoop/student-performance/',
-- data placed in HDFS is automatically accessible.
-- For managed tables or local container tests, LOAD DATA LOCAL can also be executed:

LOAD DATA LOCAL INPATH '/data/raw/student-por.csv' OVERWRITE INTO TABLE student_por;

-- Validate loaded rows
SELECT COUNT(*) AS initial_record_count FROM student_por;
SELECT * FROM student_por LIMIT 5;
