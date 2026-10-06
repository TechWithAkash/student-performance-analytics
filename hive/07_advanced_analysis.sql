-- ==========================================================
-- Big Data Analytics Project: Student Performance Analytics
-- Script 07: Advanced Risk & Profile Analysis (Q15 to Q17)
-- ==========================================================

USE student_performance_bda;

-- Query 15: Academic Risk Identification
-- Identifies students failing (G3 < 10) OR with past failures > 0 OR excessive absences (> 10)
SELECT 
    school,
    sex,
    age,
    studytime,
    failures,
    absences,
    higher,
    G1,
    G2,
    G3,
    CASE 
        WHEN G3 < 10 AND failures > 0 AND absences > 10 THEN 'CRITICAL RISK'
        WHEN G3 < 10 THEN 'FAILING RISK'
        WHEN failures > 0 THEN 'HISTORY RISK'
        ELSE 'ATTENDANCE RISK'
    END AS risk_category
FROM student_por
WHERE G3 < 10 OR failures > 0 OR absences > 10
ORDER BY G3 ASC, absences DESC
LIMIT 25;

-- Query 16: Top Academic Achievers Profile (G3 >= 16 / 20)
SELECT 
    COUNT(*) AS top_student_count,
    ROUND(COUNT(*) * 100.0 / 649, 2) AS percentage_of_cohort,
    ROUND(AVG(studytime), 2) AS avg_study_time,
    ROUND(AVG(absences), 2) AS avg_absences,
    ROUND(AVG(failures), 2) AS avg_failures,
    ROUND(SUM(CASE WHEN higher = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_desiring_higher_ed,
    ROUND(SUM(CASE WHEN internet = 'yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_with_internet
FROM student_por
WHERE G3 >= 16;

-- Query 17: Alcohol Consumption (Weekend & Workday) vs Final Grades
SELECT 
    Walc AS weekend_alcohol_level,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade,
    ROUND(AVG(absences), 2) AS avg_absences,
    ROUND(AVG(studytime), 2) AS avg_study_time
FROM student_por
GROUP BY Walc
ORDER BY Walc ASC;
