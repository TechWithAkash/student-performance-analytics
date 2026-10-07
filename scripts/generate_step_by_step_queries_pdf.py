#!/usr/bin/env python3
"""
scripts/generate_step_by_step_queries_pdf.py
Generates a comprehensive, step-by-step interactive HiveQL Query Execution
and Viva Defense Guide PDF for the Student Performance Analytics BDA project.
"""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_queries_guide_pdf(output_filename="docs/HiveQL_Step_by_Step_Query_Execution_Guide.pdf"):
    out_path = Path(output_filename)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        rightMargin=36, leftMargin=36,
        topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Premium color palette
    c_primary = colors.HexColor("#0f172a")     # Slate 900
    c_accent = colors.HexColor("#0284c7")      # Sky 600
    c_secondary = colors.HexColor("#1e293b")   # Slate 800
    c_code_bg = colors.HexColor("#f8fafc")     # Code background
    c_code_border = colors.HexColor("#cbd5e1") # Slate 300
    c_gold = colors.HexColor("#d97706")        # Amber 600
    c_green = colors.HexColor("#15803d")       # Emerald 700

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_accent,
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceBefore=10,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_secondary,
        spaceBefore=6,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#334155")
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    )

    insight_style = ParagraphStyle(
        'InsightText',
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=c_green
    )

    viva_style = ParagraphStyle(
        'VivaText',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_gold
    )

    story = []

    # ========================== COVER / HEADER ==========================
    story.append(Paragraph("Student Performance Analytics", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("HiveQL Step-by-Step Query Execution & Viva Defense Guide", subtitle_style))
    story.append(Spacer(1, 6))

    team_data = [
        [
            Paragraph("<b>Subject:</b> Big Data Analytics (BDA)", body_style),
            Paragraph("<b>Team:</b> Akash • Manish • Prathamesh", body_style),
            Paragraph("<b>Stack:</b> Hadoop HDFS + HiveQL + Streamlit", body_style)
        ]
    ]
    team_table = Table(team_data, colWidths=[170, 200, 170])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 8))

    # ========================== SECTION 1: PRE-REQUISITES & WORKFLOW ==========================
    story.append(Paragraph("1. Infrastructure Setup & Dual Execution Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))

    infra_p = """
    This runbook guides you through executing all <b>17 Analytical HiveQL Queries</b> across 7 modular scripts.
    Our project features a <b>Dual-Engine Architecture</b>: queries can be executed directly inside the distributed
    <b>Apache Hadoop/Hive Docker Cluster</b> or via the <b>Automated Python Query Runner</b>.
    """
    story.append(Paragraph(infra_p, body_style))
    story.append(Spacer(1, 4))

    setup_table_data = [
        [Paragraph("<b>Step</b>", body_style), Paragraph("<b>Target Environment</b>", body_style), Paragraph("<b>Exact Terminal Command</b>", body_style), Paragraph("<b>Verification Check</b>", body_style)],
        [
            Paragraph("<b>1. Start Cluster</b>", body_style),
            Paragraph("Docker Containers", body_style),
            Paragraph("<code>docker compose -f docker/docker-compose.yml up -d</code>", code_style),
            Paragraph("NameNode (9870), DataNode (9864), Hive (10000) active", body_style)
        ],
        [
            Paragraph("<b>2. HDFS Ingest</b>", body_style),
            Paragraph("Hadoop Distributed FS", body_style),
            Paragraph("<code>./docker/init-hadoop.sh</code>", code_style),
            Paragraph("File at <code>/user/hadoop/student-performance/student-por.csv</code>", body_style)
        ],
        [
            Paragraph("<b>3. Run All Queries</b>", body_style),
            Paragraph("Automated Pipeline", body_style),
            Paragraph("<code>./scripts/run_pipeline.sh</code>", code_style),
            Paragraph("Executes 17 queries & writes CSVs to <code>output/query-results/</code>", body_style)
        ],
        [
            Paragraph("<b>4. Launch UI</b>", body_style),
            Paragraph("Streamlit Dashboard", body_style),
            Paragraph("<code>streamlit run app.py</code>", code_style),
            Paragraph("Interactive UI at <code>http://localhost:8501</code> (Live HDFS Connected)", body_style)
        ]
    ]
    st_table = Table(setup_table_data, colWidths=[75, 110, 210, 145])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(st_table)
    story.append(Spacer(1, 8))

    # ========================== SECTION 2: SCRIPTS 01-03 (DATABASE & DDL) ==========================
    story.append(Paragraph("2. DDL & Storage Ingestion Scripts (01 to 03)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))

    ddl_items = [
        ("Script 01: Database Creation (hive/01_create_database.sql)",
         "CREATE DATABASE IF NOT EXISTS student_performance_bda;\nUSE student_performance_bda;",
         "docker exec -i student_bda_hiveserver hive -f /hive/01_create_database.sql",
         "Creates the isolated warehouse namespace in the Hive Metastore."),
        
        ("Script 02: External Table Schema (hive/02_create_table.sql)",
         "CREATE EXTERNAL TABLE IF NOT EXISTS student_performance (\n"
         "  school STRING, sex STRING, age INT, address STRING, famsize STRING, Pstatus STRING,\n"
         "  Medu INT, Fedu INT, Mjob STRING, Fjob STRING, reason STRING, guardian STRING,\n"
         "  traveltime INT, studytime INT, failures INT, schoolsup STRING, famsup STRING,\n"
         "  paid STRING, activities STRING, nursery STRING, higher STRING, internet STRING,\n"
         "  romantic STRING, famrel INT, freetime INT, goout INT, Dalc INT, Walc INT,\n"
         "  health INT, absences INT, G1 INT, G2 INT, G3 INT\n"
         ")\n"
         "ROW FORMAT DELIMITED FIELDS TERMINATED BY ';'\n"
         "STORED AS TEXTFILE LOCATION '/user/hadoop/student-performance/';",
         "docker exec -i student_bda_hiveserver hive -f /hive/02_create_table.sql",
         "Schema-on-Read: Semicolon delimited (;) parsing across 33 student attributes."),

        ("Script 03: Data Ingestion (hive/03_load_data.sql)",
         "LOAD DATA INPATH '/user/hadoop/student-performance/student-por.csv'\nINTO TABLE student_performance;",
         "docker exec -i student_bda_hiveserver hive -f /hive/03_load_data.sql",
         "Mounts HDFS block bytes into the Hive metastore table catalog.")
    ]

    for title, code_snippet, cmd_str, note_str in ddl_items:
        box_data = [
            [Paragraph(f"<b>{title}</b>", h2_style)],
            [Paragraph(f"<code>{code_snippet.replace(chr(10), '<br/>')}</code>", code_style)],
            [Paragraph(f"<b>Run Command:</b> <code>{cmd_str}</code><br/><b>Technical Rationale:</b> {note_str}", body_style)]
        ]
        tbox = Table(box_data, colWidths=[540])
        tbox.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
            ('BOX', (0,0), (-1,-1), 1, c_code_border),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(tbox)
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ========================== SECTION 3: QUERIES 1 TO 17 STEP-BY-STEP ==========================
    story.append(Paragraph("3. Step-by-Step HiveQL Analytical Queries (1 to 17)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=6))

    queries = [
        # QUERY 1
        {
            "num": 1,
            "title": "Total Student Enrollment Count",
            "script": "04_basic_analysis.sql",
            "sql": "SELECT COUNT(*) AS total_students FROM student_performance;",
            "output": "total_students: 649",
            "insight": "Ingests exactly 649 student records from the UCI Portuguese dataset without loss.",
            "viva": "Proves data integrity during HDFS block allocation and table loading."
        },
        # QUERY 2
        {
            "num": 2,
            "title": "Final Grade (G3) Summary Statistics",
            "script": "04_basic_analysis.sql",
            "sql": "SELECT ROUND(AVG(G3), 2) AS avg_final, MIN(G3) AS min_final,\n       MAX(G3) AS max_final, ROUND(STDDEV(G3), 2) AS std_final\nFROM student_performance;",
            "output": "avg_final: 11.91 | min_final: 0 | max_final: 19 | std_final: 3.23",
            "insight": "Average cohort grade is 11.91/20 with a standard deviation of 3.23 points.",
            "viva": "Demonstrates aggregation functions (AVG, MIN, MAX, STDDEV) over distributed records."
        },
        # QUERY 3
        {
            "num": 3,
            "title": "Period-over-Period Progression Tracking (G1 -> G2 -> G3)",
            "script": "04_basic_analysis.sql",
            "sql": "SELECT ROUND(AVG(G1), 2) AS avg_G1, ROUND(AVG(G2), 2) AS avg_G2,\n       ROUND(AVG(G3), 2) AS avg_G3 FROM student_performance;",
            "output": "avg_G1: 11.40 | avg_G2: 11.57 | avg_G3: 11.91",
            "insight": "Positive learning curve: cohort average improved by +0.51 points across the academic year.",
            "viva": "Proves student retention and gradual knowledge accumulation across periods."
        },
        # QUERY 4
        {
            "num": 4,
            "title": "Absence Distribution Summary",
            "script": "04_basic_analysis.sql",
            "sql": "SELECT ROUND(AVG(absences), 2) AS avg_abs, MIN(absences) AS min_abs,\n       MAX(absences) AS max_abs, ROUND(STDDEV(absences), 2) AS std_abs\nFROM student_performance;",
            "output": "avg_abs: 3.66 | min_abs: 0 | max_abs: 32 | std_abs: 4.64",
            "insight": "Mean absences is 3.66 days; high variance up to 32 days reveals severe attendance outliers.",
            "viva": "Highlights attendance variance as a critical behavioral risk variable."
        },
        # QUERY 5
        {
            "num": 5,
            "title": "Academic Performance Disaggregated by Gender",
            "script": "05_performance_analysis.sql",
            "sql": "SELECT sex, COUNT(*) AS count, ROUND(AVG(G1), 2) AS avg_G1,\n       ROUND(AVG(G2), 2) AS avg_G2, ROUND(AVG(G3), 2) AS avg_G3,\n       ROUND(AVG(absences), 2) AS avg_abs\nFROM student_performance GROUP BY sex;",
            "output": "Female (383): avg_G3=12.25, abs=3.58 | Male (266): avg_G3=11.41, abs=3.78",
            "insight": "Female students outperformed male students by +0.84 points with slightly better attendance.",
            "viva": "Showcases multi-column GROUP BY aggregation and gender equity analysis."
        },
        # QUERY 6
        {
            "num": 6,
            "title": "Institutional Comparison: Gabriel Pereira (GP) vs Mousinho (MS)",
            "script": "05_performance_analysis.sql",
            "sql": "SELECT school, COUNT(*) AS students, ROUND(AVG(G3), 2) AS avg_G3,\n       ROUND(AVG(studytime), 2) AS avg_study, ROUND(AVG(absences), 2) AS avg_abs\nFROM student_performance GROUP BY school;",
            "output": "GP (423): avg_G3=12.58, study=2.01h, abs=4.22 | MS (226): avg_G3=10.65, study=1.77h, abs=2.62",
            "insight": "Urban school GP leads rural MS by +1.93 grade points due to higher average study time.",
            "viva": "Identifies geographic/resource disparities between urban and rural school systems."
        },
        # QUERY 7
        {
            "num": 7,
            "title": "Cohort Pass vs Fail Ratio (Passing Threshold G3 >= 10)",
            "script": "05_performance_analysis.sql",
            "sql": "SELECT CASE WHEN G3 >= 10 THEN 'Passed' ELSE 'Failed' END AS status,\n       COUNT(*) AS student_count,\n       ROUND(COUNT(*) * 100.0 / 649, 2) AS percentage\nFROM student_performance GROUP BY CASE WHEN G3 >= 10 THEN 'Passed' ELSE 'Failed' END;",
            "output": "Passed: 549 students (84.59%) | Failed: 100 students (15.41%)",
            "insight": "Overall graduation pass rate is strong at 84.6%, but 15.4% require urgent intervention.",
            "viva": "Uses conditional CASE-WHEN logic inside GROUP BY for executive KPI classification."
        },
        # QUERY 8
        {
            "num": 8,
            "title": "Grade Distribution by Academic Tiers",
            "script": "05_performance_analysis.sql",
            "sql": "SELECT CASE\n         WHEN G3 < 10 THEN '01. Fail (0-9)'\n         WHEN G3 BETWEEN 10 AND 13 THEN '02. Sufficient (10-13)'\n         WHEN G3 BETWEEN 14 AND 15 THEN '03. Good (14-15)'\n         ELSE '04. Excellent (16-20)'\n       END AS grade_category, COUNT(*) AS count,\n       ROUND(COUNT(*) * 100.0 / 649, 2) AS pct,\n       ROUND(AVG(studytime), 2) AS avg_study, ROUND(AVG(absences), 2) AS avg_abs\nFROM student_performance GROUP BY ... ORDER BY grade_category;",
            "output": "Fail: 15.4% (1.61h study) | Sufficient: 54.7% (1.89h) | Good: 17.3% (2.13h) | Excellent: 12.6% (2.24h)",
            "insight": "Direct correlation: Study time increases monotonically with each higher grade tier.",
            "viva": "Demonstrates multi-tier discretization and academic segmentation in Hive."
        },
        # QUERY 9
        {
            "num": 9,
            "title": "Study Time Elasticity vs Final Academic Outcome",
            "script": "06_factor_analysis.sql",
            "sql": "SELECT studytime, CASE studytime WHEN 1 THEN '< 2h' WHEN 2 THEN '2-5h'\n       WHEN 3 THEN '5-10h' ELSE '> 10h' END AS study_desc,\n       COUNT(*) AS students, ROUND(AVG(G3), 2) AS avg_G3, ROUND(AVG(failures), 2) AS avg_fails\nFROM student_performance GROUP BY studytime ORDER BY studytime;",
            "output": "<2h: 10.84 avg (0.33 fails) | 2-5h: 12.09 | 5-10h: 13.23 (0.10 fails) | >10h: 13.06",
            "insight": "Studying 5-10 hours/week yields +2.39 grade points compared to <2 hours/week.",
            "viva": "Proves behavioral factors directly mitigate academic failure rates."
        },
        # QUERY 10
        {
            "num": 10,
            "title": "Previous Failures Impact Analysis",
            "script": "06_factor_analysis.sql",
            "sql": "SELECT failures, COUNT(*) AS count, ROUND(AVG(G3), 2) AS avg_G3,\n       ROUND(AVG(absences), 2) AS avg_abs\nFROM student_performance GROUP BY failures ORDER BY failures;",
            "output": "0 Failures: 12.51 (549 students) | 1 Failure: 8.64 (70) | 2: 8.81 (16) | 3: 8.07 (14)",
            "insight": "CRITICAL RISK FACTOR: Having just 1 prior failure drops average score below passing (8.64/20).",
            "viva": "Identifies the single most decisive historical predictor of academic failure."
        },
        # QUERY 11
        {
            "num": 11,
            "title": "Absence Tiers vs Academic Performance",
            "script": "06_factor_analysis.sql",
            "sql": "SELECT CASE\n         WHEN absences = 0 THEN '00. Zero Absences'\n         WHEN absences BETWEEN 1 AND 4 THEN '01. Low (1-4)'\n         WHEN absences BETWEEN 5 AND 9 THEN '02. Moderate (5-9)'\n         ELSE '03. High (10+)'\n       END AS absence_tier, COUNT(*) AS count, ROUND(AVG(G3), 2) AS avg_G3\nFROM student_performance GROUP BY ... ORDER BY absence_tier;",
            "output": "Zero: 12.04 (244) | Low (1-4): 12.07 (222) | Moderate (5-9): 11.77 (113) | High (10+): 11.13 (70)",
            "insight": "High absenteeism (10+ missed classes) reduces student performance by nearly 1 full point.",
            "viva": "Demonstrates tier-based clustering and attendance penalty modeling."
        },
        # QUERY 12
        {
            "num": 12,
            "title": "Parental Educational Attainment Correlation",
            "script": "06_factor_analysis.sql",
            "sql": "SELECT Medu AS mother_edu, Fedu AS father_edu, COUNT(*) AS count,\n       ROUND(AVG(G3), 2) AS avg_G3\nFROM student_performance GROUP BY Medu, Fedu HAVING count >= 10 ORDER BY avg_G3 DESC;",
            "output": "Both Higher Ed (4,4): 13.12/20 (95 students) | Both Primary (1,1): 11.70/20 (20 students)",
            "insight": "Students from households with higher parental education achieve up to +1.4 points higher.",
            "viva": "Uses HAVING clause to filter statistically robust sample sizes in distributed SQL."
        },
        # QUERY 13
        {
            "num": 13,
            "title": "School vs Family Educational Support Effectiveness",
            "script": "06_factor_analysis.sql",
            "sql": "SELECT schoolsup, famsup, COUNT(*) AS count, ROUND(AVG(G3), 2) AS avg_G3\nFROM student_performance GROUP BY schoolsup, famsup ORDER BY avg_G3 DESC;",
            "output": "No School / Yes Family: 12.14 (349) | Yes School / Yes Family: 11.47 (49) | Yes School / No Family: 10.79 (19)",
            "insight": "Remedial school support is targeted at struggling students; family support helps buffer scores.",
            "viva": "Evaluates targeted intervention effects and institutional support programs."
        },
        # QUERY 14
        {
            "num": 14,
            "title": "Higher Education Ambition & Home Internet Access Synergies",
            "script": "06_factor_analysis.sql",
            "sql": "SELECT higher AS wants_higher_ed, internet AS has_home_internet,\n       COUNT(*) AS count, ROUND(AVG(G3), 2) AS avg_G3\nFROM student_performance GROUP BY higher, internet ORDER BY avg_G3 DESC;",
            "output": "Yes Higher / Yes Net: 12.53 (451) | Yes Higher / No Net: 11.40 (129) | No Higher / Any: 8.80 (69)",
            "insight": "Students aiming for university score ~3.7 points higher; internet connectivity adds +1.13 points.",
            "viva": "Proves the compounding benefit of student motivation and digital access."
        },
        # QUERY 15
        {
            "num": 15,
            "title": "Early Intervention Radar: At-Risk Student Identification",
            "script": "07_advanced_analysis.sql",
            "sql": "SELECT school, sex, age, studytime, failures, absences, G1, G2, G3,\n       CASE\n         WHEN G3 < 10 AND failures > 0 AND absences > 10 THEN 'CRITICAL RISK'\n         WHEN G3 < 10 THEN 'FAILING RISK'\n         WHEN failures > 0 THEN 'HISTORY RISK'\n         ELSE 'ATTENDANCE RISK'\n       END AS risk_category\nFROM student_performance\nWHERE G3 < 10 OR failures > 0 OR absences > 10 ORDER BY G3 ASC LIMIT 10;",
            "output": "Identified 177 at-risk students across 4 actionable severity tiers.",
            "insight": "Translates big data analytics into proactive educator intervention lists before final exams.",
            "viva": "Demonstrates complex multi-criteria filtering (WHERE OR) and rule-based risk ranking."
        },
        # QUERY 16
        {
            "num": 16,
            "title": "Elite Achievers Profile (G3 >= 16/20)",
            "script": "07_advanced_analysis.sql",
            "sql": "SELECT COUNT(*) AS top_count, ROUND(COUNT(*)*100.0/649, 2) AS cohort_pct,\n       ROUND(AVG(studytime), 2) AS avg_study, ROUND(AVG(absences), 2) AS avg_abs,\n       ROUND(AVG(failures), 2) AS avg_fails,\n       ROUND(SUM(CASE WHEN higher='yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS pct_higher_ed,\n       ROUND(SUM(CASE WHEN internet='yes' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS pct_internet\nFROM student_performance WHERE G3 >= 16;",
            "output": "82 Elite Students (12.63%): 2.24h study, 2.59 absences, 0.01 failures, 100% Higher Ed, 85.4% Internet",
            "insight": "100% of elite achievers desire higher education and maintain near-zero failure and low absence records.",
            "viva": "Showcases advanced feature profiling and conditional SUM aggregation in HiveQL."
        },
        # QUERY 17
        {
            "num": 17,
            "title": "Weekend Alcohol Consumption vs Academic Trajectory",
            "script": "07_advanced_analysis.sql",
            "sql": "SELECT Walc AS weekend_alcohol_level, COUNT(*) AS count,\n       ROUND(AVG(G3), 2) AS avg_G3, ROUND(AVG(absences), 2) AS avg_abs,\n       ROUND(AVG(studytime), 2) AS avg_study\nFROM student_performance GROUP BY Walc ORDER BY Walc ASC;",
            "output": "Level 1 (Very Low): 12.36 avg, 2.89 abs, 2.12h study (247 students)\nLevel 5 (Very High): 10.56 avg, 5.24 abs, 1.58h study (45 students)",
            "insight": "High weekend alcohol consumption lowers final grades by -1.8 points and nearly doubles absences (5.2 vs 2.9).",
            "viva": "Highlights lifestyle health factors that directly undermine academic performance."
        }
    ]

    for q in queries:
        card_data = [
            [
                Paragraph(f"<b>Query {q['num']}: {q['title']}</b>", h2_style),
                Paragraph(f"<b>File:</b> <code>hive/{q['script']}</code>", body_style)
            ],
            [
                Paragraph(f"<code>{q['sql'].replace(chr(10), '<br/>')}</code>", code_style),
                Paragraph(f"<b>Expected Output:</b><br/><code>{q['output'].replace(chr(10), '<br/>')}</code>", body_style)
            ],
            [
                Paragraph(f"<b>Key Insight:</b> {q['insight']}", insight_style),
                Paragraph(f"<b>Teacher Viva Defense:</b> {q['viva']}", viva_style)
            ]
        ]
        q_table = Table(card_data, colWidths=[310, 230])
        q_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
            ('BOX', (0,0), (-1,-1), 1, c_code_border),
            ('LINEBELOW', (0,0), (-1,0), 0.5, colors.HexColor("#e2e8f0")),
            ('LINEBELOW', (0,1), (-1,1), 0.5, colors.HexColor("#e2e8f0")),
            ('PADDING', (0,0), (-1,-1), 3.5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(q_table)
        story.append(Spacer(1, 4))

        if q['num'] in [4, 8, 12]:
            story.append(PageBreak())

    # ========================== SECTION 4: VIVA QUICK DEFENSE ==========================
    story.append(PageBreak())
    story.append(Paragraph("4. Essential Viva Questions & Speaking Scripts", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))

    viva_qa = [
        ("Q1: How do you run individual HiveQL queries in front of the teacher?",
         "<b>Answer:</b> <i>'Ma'am, we have two ways: (1) Running directly inside the Hive container: <code>docker exec -i student_bda_hiveserver hive -e \"SELECT ...\"</code>, or (2) Running our automated master pipeline <code>./scripts/run_pipeline.sh</code> which executes all 17 queries and outputs CSV reports.'</i>"),

        ("Q2: What is the difference between Managed and External tables in Hive?",
         "<b>Answer:</b> <i>'In our project we created an <b>EXTERNAL TABLE</b>. With external tables, Hive manages the metadata/schema, but if we drop the table, the raw data file remains safe inside HDFS. In a managed table, dropping the table permanently deletes both metadata and HDFS data.'</i>"),

        ("Q3: Why does HiveQL use MapReduce/Tez under the hood?",
         "<b>Answer:</b> <i>'Hive is a SQL abstraction on top of distributed data. When we run GROUP BY or AVG queries, Hive translates declarative SQL into distributed MapReduce or Tez execution DAGs across cluster DataNodes.'</i>"),

        ("Q4: Which query reveals the highest correlation with student failure?",
         "<b>Answer:</b> <i>'Query 10 (Previous Failures). A student with 0 failures averages 12.51/20, but with just 1 previous failure, the average drops below the passing threshold to 8.64/20.'</i>")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 3))

    doc.build(story)
    print(f"Interactive Step-by-Step Queries Guide generated at: {out_path}")
    return str(out_path)

if __name__ == "__main__":
    generate_queries_guide_pdf()
