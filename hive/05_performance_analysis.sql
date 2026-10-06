-- ==========================================================
-- Big Data Analytics Project: Student Performance Analytics
-- Script 05: Performance & Comparative Analysis (Q5 to Q8)
-- ==========================================================

USE student_performance_bda;

-- Query 5: Grade & Attendance Comparison by Gender
SELECT 
    sex AS gender,
    COUNT(*) AS student_count,
    ROUND(AVG(G1), 2) AS avg_G1,
    ROUND(AVG(G2), 2) AS avg_G2,
    ROUND(AVG(G3), 2) AS avg_final_grade,
    ROUND(AVG(absences), 2) AS avg_absences
FROM student_por
GROUP BY sex
ORDER BY avg_final_grade DESC;

-- Query 6: Performance Comparison by School (GP vs MS)
SELECT 
    school,
    COUNT(*) AS total_students,
    ROUND(AVG(G3), 2) AS avg_final_grade,
    ROUND(AVG(studytime), 2) AS avg_study_time,
    ROUND(AVG(absences), 2) AS avg_absences
FROM student_por
GROUP BY school
ORDER BY avg_final_grade DESC;

-- Query 7: Overall Pass vs Fail Rate (Pass mark >= 10 on 0-20 scale)
SELECT 
    CASE WHEN G3 >= 10 THEN 'Passed' ELSE 'Failed' END AS status,
    COUNT(*) AS student_count,
    ROUND(COUNT(*) * 100.0 / 649, 2) AS percentage
FROM student_por
GROUP BY CASE WHEN G3 >= 10 THEN 'Passed' ELSE 'Failed' END;

-- Query 8: Portuguese Grade Distribution Categories
SELECT 
    CASE 
        WHEN G3 < 10 THEN '01. Fail (0-9)'
        WHEN G3 BETWEEN 10 AND 13 THEN '02. Sufficient (10-13)'
        WHEN G3 BETWEEN 14 AND 15 THEN '03. Good (14-15)'
        ELSE '04. Excellent (16-20)'
    END AS grade_category,
    COUNT(*) AS student_count,
    ROUND(COUNT(*) * 100.0 / 649, 2) AS percentage,
    ROUND(AVG(studytime), 2) AS avg_study_time,
    ROUND(AVG(absences), 2) AS avg_absences
FROM student_por
GROUP BY CASE 
        WHEN G3 < 10 THEN '01. Fail (0-9)'
        WHEN G3 BETWEEN 10 AND 13 THEN '02. Sufficient (10-13)'
        WHEN G3 BETWEEN 14 AND 15 THEN '03. Good (14-15)'
        ELSE '04. Excellent (16-20)'
    END
ORDER BY grade_category;
