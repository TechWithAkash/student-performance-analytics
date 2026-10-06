-- ==========================================================
-- Big Data Analytics Project: Student Performance Analytics
-- Script 04: Basic Analysis Queries (Q1 to Q4)
-- ==========================================================

USE student_performance_bda;

-- Query 1: Total Number of Students in Dataset
SELECT 
    COUNT(*) AS total_students
FROM student_por;

-- Query 2: Final Grade (G3) Summary Statistics
SELECT 
    ROUND(AVG(G3), 2) AS avg_final_grade,
    MIN(G3) AS min_final_grade,
    MAX(G3) AS max_final_grade,
    ROUND(STDDEV(G3), 2) AS stddev_final_grade
FROM student_por;

-- Query 3: Academic Progression Across Periods (G1, G2, G3)
SELECT 
    ROUND(AVG(G1), 2) AS avg_period1_grade,
    ROUND(AVG(G2), 2) AS avg_period2_grade,
    ROUND(AVG(G3), 2) AS avg_final_grade
FROM student_por;

-- Query 4: School Absence Summary Statistics
SELECT 
    ROUND(AVG(absences), 2) AS avg_absences,
    MIN(absences) AS min_absences,
    MAX(absences) AS max_absences,
    ROUND(STDDEV(absences), 2) AS stddev_absences
FROM student_por;
