-- ==========================================================
-- Big Data Analytics Project: Student Performance Analytics
-- Script 06: Academic & Socioeconomic Factor Analysis (Q9 to Q14)
-- ==========================================================

USE student_performance_bda;

-- Query 9: Weekly Study Time vs Final Grade
-- Studytime: 1 = <2h, 2 = 2-5h, 3 = 5-10h, 4 = >10h
SELECT 
    studytime,
    CASE 
        WHEN studytime = 1 THEN '< 2 hours'
        WHEN studytime = 2 THEN '2 to 5 hours'
        WHEN studytime = 3 THEN '5 to 10 hours'
        ELSE '> 10 hours'
    END AS study_time_desc,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade,
    ROUND(AVG(failures), 2) AS avg_failures
FROM student_por
GROUP BY studytime
ORDER BY studytime ASC;

-- Query 10: Previous Class Failures vs Final Grade
SELECT 
    failures,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade,
    ROUND(AVG(absences), 2) AS avg_absences
FROM student_por
GROUP BY failures
ORDER BY failures ASC;

-- Query 11: School Absences Quartile Grouping vs Final Grade
SELECT 
    CASE 
        WHEN absences = 0 THEN '00. Zero Absences'
        WHEN absences BETWEEN 1 AND 4 THEN '01. Low (1-4)'
        WHEN absences BETWEEN 5 AND 9 THEN '02. Moderate (5-9)'
        ELSE '03. High (10+)'
    END AS absence_tier,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade,
    ROUND(AVG(studytime), 2) AS avg_study_time
FROM student_por
GROUP BY CASE 
        WHEN absences = 0 THEN '00. Zero Absences'
        WHEN absences BETWEEN 1 AND 4 THEN '01. Low (1-4)'
        WHEN absences BETWEEN 5 AND 9 THEN '02. Moderate (5-9)'
        ELSE '03. High (10+)'
    END
ORDER BY absence_tier ASC;

-- Query 12: Parental Education Levels vs Student Outcomes
-- 0 = None, 1 = Primary (4th grade), 2 = 5th-9th, 3 = Secondary, 4 = Higher
SELECT 
    Medu AS mother_education,
    Fedu AS father_education,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade
FROM student_por
GROUP BY Medu, Fedu
ORDER BY mother_education DESC, father_education DESC;

-- Query 13: Educational Support (School Support & Family Support)
SELECT 
    schoolsup,
    famsup,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade
FROM student_por
GROUP BY schoolsup, famsup
ORDER BY avg_final_grade DESC;

-- Query 14: Desire for Higher Education & Home Internet Access
SELECT 
    higher AS wants_higher_education,
    internet AS has_home_internet,
    COUNT(*) AS student_count,
    ROUND(AVG(G3), 2) AS avg_final_grade
FROM student_por
GROUP BY higher, internet
ORDER BY avg_final_grade DESC;
