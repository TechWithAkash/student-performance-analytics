#!/usr/bin/env python3
"""
scripts/local_query_runner.py
Dual-execution engine that runs the exact HiveQL queries locally using standard
SQL engine (sqlite3 + pandas), guaranteeing reproducible outputs in output/query-results/
even if Docker is offline.
"""

import sys
import sqlite3
from pathlib import Path
import pandas as pd

def get_connection(csv_path="data/raw/student-por.csv"):
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"Source dataset not found at {csv_file}")
    
    df = pd.read_csv(csv_file, sep=";")
    con = sqlite3.connect(":memory:")
    # Register custom STDDEV function in sqlite
    class StdDev:
        def __init__(self):
            self.values = []
        def step(self, value):
            if value is not None:
                self.values.append(float(value))
        def finalize(self):
            if len(self.values) < 2:
                return 0.0
            mean = sum(self.values) / len(self.values)
            variance = sum((x - mean) ** 2 for x in self.values) / (len(self.values) - 1)
            return round(variance ** 0.5, 2)
            
    con.create_aggregate("STDDEV", 1, StdDev)
    df.to_sql("student_por", con, index=False, if_exists="replace")
    return con

def run_all_queries(csv_path="data/raw/student-por.csv", output_dir="output/query-results"):
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    con = get_connection(csv_path)

    summary_lines = []
    summary_lines.append("=" * 70)
    summary_lines.append("STUDENT PERFORMANCE BDA - HIVEQL QUERY EXECUTION SUMMARY")
    summary_lines.append("=" * 70)

    # 1. Total Students
    df_q1 = pd.read_sql_query("SELECT COUNT(*) AS total_students FROM student_por;", con)
    total_students = int(df_q1["total_students"].iloc[0])
    summary_lines.append(f"\n[QUERY 1] Total Students: {total_students}")

    # 2. Final Grade Stats
    q2_sql = """
    SELECT 
        ROUND(AVG(G3), 2) AS avg_final_grade,
        MIN(G3) AS min_final_grade,
        MAX(G3) AS max_final_grade,
        ROUND(STDDEV(G3), 2) AS stddev_final_grade
    FROM student_por;
    """
    df_q2 = pd.read_sql_query(q2_sql, con)
    df_q2.to_csv(out_path / "04_basic_analysis.csv", index=False)
    summary_lines.append("\n[QUERY 2] Final Grade Statistics:")
    summary_lines.append(df_q2.to_string(index=False))

    # 3. Progression of Period Grades
    q3_sql = """
    SELECT 
        ROUND(AVG(G1), 2) AS avg_period1_grade,
        ROUND(AVG(G2), 2) AS avg_period2_grade,
        ROUND(AVG(G3), 2) AS avg_final_grade
    FROM student_por;
    """
    df_q3 = pd.read_sql_query(q3_sql, con)
    summary_lines.append("\n[QUERY 3] Period Progression:")
    summary_lines.append(df_q3.to_string(index=False))

    # 4. Absence Statistics
    q4_sql = """
    SELECT 
        ROUND(AVG(absences), 2) AS avg_absences,
        MIN(absences) AS min_absences,
        MAX(absences) AS max_absences,
        ROUND(STDDEV(absences), 2) AS stddev_absences
    FROM student_por;
    """
    df_q4 = pd.read_sql_query(q4_sql, con)
    summary_lines.append("\n[QUERY 4] Absence Summary:")
    summary_lines.append(df_q4.to_string(index=False))

    # 5. Gender Comparison
    q5_sql = """
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
    """
    df_q5 = pd.read_sql_query(q5_sql, con)
    df_q5.to_csv(out_path / "05_gender_analysis.csv", index=False)
    summary_lines.append("\n[QUERY 5] Performance by Gender:")
    summary_lines.append(df_q5.to_string(index=False))

    # 6. Performance by School
    q6_sql = """
    SELECT 
        school,
        COUNT(*) AS total_students,
        ROUND(AVG(G3), 2) AS avg_final_grade,
        ROUND(AVG(studytime), 2) AS avg_study_time,
        ROUND(AVG(absences), 2) AS avg_absences
    FROM student_por
    GROUP BY school
    ORDER BY avg_final_grade DESC;
    """
    df_q6 = pd.read_sql_query(q6_sql, con)
    summary_lines.append("\n[QUERY 6] Performance by School:")
    summary_lines.append(df_q6.to_string(index=False))

    # 7. Pass vs Fail Ratio
    q7_sql = """
    SELECT 
        CASE WHEN G3 >= 10 THEN 'Passed' ELSE 'Failed' END AS status,
        COUNT(*) AS student_count,
        ROUND(COUNT(*) * 100.0 / 649, 2) AS percentage
    FROM student_por
    GROUP BY CASE WHEN G3 >= 10 THEN 'Passed' ELSE 'Failed' END;
    """
    df_q7 = pd.read_sql_query(q7_sql, con)
    summary_lines.append("\n[QUERY 7] Pass vs Fail Ratio:")
    summary_lines.append(df_q7.to_string(index=False))

    # 8. Grade Categories
    q8_sql = """
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
    """
    df_q8 = pd.read_sql_query(q8_sql, con)
    df_q8.to_csv(out_path / "05_grade_categories.csv", index=False)
    summary_lines.append("\n[QUERY 8] Grade Distribution Categories:")
    summary_lines.append(df_q8.to_string(index=False))

    # 9. Study Time
    q9_sql = """
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
    """
    df_q9 = pd.read_sql_query(q9_sql, con)
    df_q9.to_csv(out_path / "06_study_time.csv", index=False)
    summary_lines.append("\n[QUERY 9] Study Time vs Final Grade:")
    summary_lines.append(df_q9.to_string(index=False))

    # 10. Failures
    q10_sql = """
    SELECT 
        failures,
        COUNT(*) AS student_count,
        ROUND(AVG(G3), 2) AS avg_final_grade,
        ROUND(AVG(absences), 2) AS avg_absences
    FROM student_por
    GROUP BY failures
    ORDER BY failures ASC;
    """
    df_q10 = pd.read_sql_query(q10_sql, con)
    summary_lines.append("\n[QUERY 10] Previous Failures Impact:")
    summary_lines.append(df_q10.to_string(index=False))

    # 11. Absences Grouping
    q11_sql = """
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
    """
    df_q11 = pd.read_sql_query(q11_sql, con)
    summary_lines.append("\n[QUERY 11] Absences Impact:")
    summary_lines.append(df_q11.to_string(index=False))

    # 12. Parental Education
    q12_sql = """
    SELECT 
        Medu AS mother_education,
        Fedu AS father_education,
        COUNT(*) AS student_count,
        ROUND(AVG(G3), 2) AS avg_final_grade
    FROM student_por
    GROUP BY Medu, Fedu
    ORDER BY mother_education DESC, father_education DESC;
    """
    df_q12 = pd.read_sql_query(q12_sql, con)
    df_q12.to_csv(out_path / "06_factor_analysis.csv", index=False)
    summary_lines.append("\n[QUERY 12] Parental Education vs Grade:")
    summary_lines.append(df_q12.head(10).to_string(index=False))

    # 13. Educational Support
    q13_sql = """
    SELECT 
        schoolsup,
        famsup,
        COUNT(*) AS student_count,
        ROUND(AVG(G3), 2) AS avg_final_grade
    FROM student_por
    GROUP BY schoolsup, famsup
    ORDER BY avg_final_grade DESC;
    """
    df_q13 = pd.read_sql_query(q13_sql, con)
    summary_lines.append("\n[QUERY 13] Educational Support:")
    summary_lines.append(df_q13.to_string(index=False))

    # 14. Higher Ed & Internet
    q14_sql = """
    SELECT 
        higher AS wants_higher_education,
        internet AS has_home_internet,
        COUNT(*) AS student_count,
        ROUND(AVG(G3), 2) AS avg_final_grade
    FROM student_por
    GROUP BY higher, internet
    ORDER BY avg_final_grade DESC;
    """
    df_q14 = pd.read_sql_query(q14_sql, con)
    summary_lines.append("\n[QUERY 14] Higher Ed & Internet Access:")
    summary_lines.append(df_q14.to_string(index=False))

    # 15. Risk Identification
    q15_sql = """
    SELECT 
        school, sex, age, studytime, failures, absences, higher, G1, G2, G3,
        CASE 
            WHEN G3 < 10 AND failures > 0 AND absences > 10 THEN 'CRITICAL RISK'
            WHEN G3 < 10 THEN 'FAILING RISK'
            WHEN failures > 0 THEN 'HISTORY RISK'
            ELSE 'ATTENDANCE RISK'
        END AS risk_category
    FROM student_por
    WHERE G3 < 10 OR failures > 0 OR absences > 10
    ORDER BY G3 ASC, absences DESC;
    """
    df_q15 = pd.read_sql_query(q15_sql, con)
    df_q15.to_csv(out_path / "07_advanced_analysis.csv", index=False)
    summary_lines.append(f"\n[QUERY 15] Academic Risk Students Identified: {len(df_q15)} students")
    summary_lines.append(df_q15.head(10).to_string(index=False))

    # 16. Top Achievers
    q16_sql = """
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
    """
    df_q16 = pd.read_sql_query(q16_sql, con)
    df_q16.to_csv(out_path / "07_top_achievers.csv", index=False)
    summary_lines.append("\n[QUERY 16] Top Academic Achievers (G3 >= 16):")
    summary_lines.append(df_q16.to_string(index=False))

    # 17. Alcohol vs Final Grade
    q17_sql = """
    SELECT 
        Walc AS weekend_alcohol_level,
        COUNT(*) AS student_count,
        ROUND(AVG(G3), 2) AS avg_final_grade,
        ROUND(AVG(absences), 2) AS avg_absences,
        ROUND(AVG(studytime), 2) AS avg_study_time
    FROM student_por
    GROUP BY Walc
    ORDER BY Walc ASC;
    """
    df_q17 = pd.read_sql_query(q17_sql, con)
    summary_lines.append("\n[QUERY 17] Weekend Alcohol Consumption vs Final Grades:")
    summary_lines.append(df_q17.to_string(index=False))

    summary_text = "\n".join(summary_lines)
    with open(out_path / "all_queries_summary.txt", "w") as f:
        f.write(summary_text)

    print(f"Successfully executed 17 queries and generated reports in {out_path}")
    return {
        "total_students": total_students,
        "avg_final_grade": float(df_q2["avg_final_grade"].iloc[0]),
        "pass_count": int(df_q7[df_q7["status"] == "Passed"]["student_count"].iloc[0]),
        "risk_count": len(df_q15),
        "top_achievers_count": int(df_q16["top_student_count"].iloc[0]),
    }

if __name__ == "__main__":
    run_all_queries()
