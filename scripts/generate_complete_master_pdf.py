#!/usr/bin/env python3
"""
scripts/generate_complete_master_pdf.py
Generates a comprehensive, all-in-one Master Academic Guide & Viva Defense PDF
for the Student Performance Big Data Analytics (BDA) project.
"""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def build_master_pdf(output_filename="docs/Student_Performance_BDA_Complete_Project_Book.pdf"):
    out_path = Path(output_filename)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 40pt margins for a professional, book-like document
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Premium color palette
    c_primary = colors.HexColor("#0f172a")     # Slate 900
    c_accent = colors.HexColor("#0284c7")      # Sky 600
    c_secondary = colors.HexColor("#334155")   # Slate 700
    c_light = colors.HexColor("#f8fafc")       # Slate 50
    c_border = colors.HexColor("#cbd5e1")      # Slate 300
    c_highlight = colors.HexColor("#f0fdf4")   # Green 50

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_accent,
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_accent,
        spaceBefore=12,
        spaceAfter=5
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_secondary,
        spaceBefore=7,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b"),
        alignment=TA_LEFT
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#0369a1")
    )

    story = []

    # ========================== COVER / HEADER ==========================
    story.append(Paragraph("Student Performance Analytics", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Complete Technical Architecture, Technology Justification & Viva Presentation Guide", subtitle_style))
    story.append(Spacer(1, 8))

    team_data = [
        [
            Paragraph("<b>Subject:</b> Big Data Analytics (BDA)", body_style),
            Paragraph("<b>Dataset:</b> UCI Portuguese Cohort (N=649)", body_style),
            Paragraph("<b>Architecture:</b> HDFS + Hive + Streamlit", body_style)
        ],
        [
            Paragraph("<b>Group Member 1:</b> Akash (Storage & Ingestion)", body_style),
            Paragraph("<b>Group Member 2:</b> Manish (Hive & Query Warehouse)", body_style),
            Paragraph("<b>Group Member 3:</b> Prathamesh (Streamlit & Presentation)", body_style)
        ]
    ]
    team_table = Table(team_data, colWidths=[174, 174, 174])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 10))

    # ========================== SECTION 1: THE SIMPLE STORY ==========================
    story.append(Paragraph("1. The Simple Story — How to Explain this in 20 Seconds", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=6))
    
    p1 = """
    <b>In plain words:</b> Schools collect student data (attendance, study hours, parents' education, failures), 
    but teachers rarely know who is about to fail until it is too late. <br/>
    In this project, we built a <b>Big Data pipeline</b>: we put <b>649 real student records</b> into 
    <b>Hadoop HDFS</b> (distributed storage), ran <b>17 analytical SQL queries</b> using <b>Apache Hive</b>, 
    and built an interactive <b>Streamlit dashboard</b> that automatically warns teachers about at-risk students 
    and reveals what habits drive academic success.
    """
    story.append(Paragraph(p1, body_style))
    story.append(Spacer(1, 10))

    # ========================== SECTION 2: WHY THIS TECH STACK? ==========================
    story.append(Paragraph("2. Technology Justification — Why We Chose These Tools & NOT Others", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=6))

    tech_just_data = [
        ["Technology Chosen", "Alternative Considered", "Why We Chose It (The Killer Reason for Ma'am)"],
        [
            Paragraph("<b>Hadoop HDFS</b><br/>(Distributed Storage)", body_style),
            Paragraph("MySQL / PostgreSQL / Excel", body_style),
            Paragraph("<b>Decoupled Storage & Horizontal Scale:</b> RDBMS enforces rigid schemas on write and runs on a single expensive server. HDFS splits files into 128MB blocks across commodity hardware with automatic replication. We can grow from 600 records to 600 million records without redesigning the system.", body_style)
        ],
        [
            Paragraph("<b>Apache Hive</b><br/>(HiveQL Data Warehouse)", body_style),
            Paragraph("Writing Java MapReduce jobs", body_style),
            Paragraph("<b>SQL Abstraction over Big Data:</b> Writing raw Java MapReduce requires hundreds of lines of complex Mapper/Reducer code. Hive provides HiveQL (SQL-like) that automatically compiles high-level queries into distributed execution plans without writing low-level Java.", body_style)
        ],
        [
            Paragraph("<b>External Table</b><br/>(Hive Table Type)", body_style),
            Paragraph("Managed (Internal) Table", body_style),
            Paragraph("<b>Data Lake Safety:</b> In Managed tables, dropping the table permanently deletes the underlying HDFS files. In <b>External tables</b>, Hive manages only metadata. If we drop or modify the Hive schema, our raw data in HDFS remains 100% safe and accessible to Spark, Python, or Presto.", body_style)
        ],
        [
            Paragraph("<b>Streamlit (Python)</b><br/>(Interactive UI)", body_style),
            Paragraph("Tableau / Power BI / React", body_style),
            Paragraph("<b>Native Python Integration & Zero-License Cost:</b> Power BI/Tableau require expensive proprietary licenses and manual refresh exports. React requires complex frontend state management. Streamlit allows pure-Python interactive KPI cards, filters, and dynamic CSV exports natively.", body_style)
        ]
    ]

    t_just = Table(tech_just_data, colWidths=[100, 110, 312])
    t_just.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,1), (-1,-1), c_light),
    ]))
    story.append(t_just)
    story.append(Spacer(1, 10))

    # ========================== SECTION 3: ARCHITECTURE & DATA FLOW ==========================
    story.append(Paragraph("3. Technical Architecture & End-to-End Pipeline", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=6))

    arch_steps = """
    <b>The pipeline moves through 5 distinct stages:</b><br/>
    <b>1. Ingestion & Validation:</b> Automated Python script (<code>scripts/download_data.py</code>) fetches the official UCI archive, validates zero NULL values, and confirms 33 columns and 649 records.<br/>
    <b>2. Distributed Storage (HDFS):</b> Data is loaded into HDFS at <code>/user/hadoop/student-performance/student-por.csv</code>.<br/>
    <b>3. Warehouse Schema-on-Read (Hive):</b> Hive database <code>student_performance_bda</code> is created, with an EXTERNAL table pointing to the HDFS location with delimiter <code>FIELDS TERMINATED BY ';'</code>.<br/>
    <b>4. Analytical Query Execution:</b> 7 modular HiveQL scripts execute 17 analytical queries and output summaries to <code>output/query-results/</code>.<br/>
    <b>5. Interactive Presentation (Streamlit):</b> Responsive dashboard loads aggregated results, calculates live KPIs, renders Plotly charts, and filters at-risk students.
    """
    story.append(Paragraph(arch_steps, body_style))
    story.append(Spacer(1, 10))

    # ========================== SECTION 4: DATASET & PARSING ==========================
    story.append(Paragraph("4. Dataset Details, Delimiter Parsing & Data Dictionary", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=6))

    p_data = """
    • <b>Source:</b> UCI Machine Learning Repository (Student Performance Dataset).<br/>
    • <b>Primary Course File:</b> <code>student-por.csv</code> (Portuguese language course, 649 rows, 33 columns).<br/>
    • <b>Crucial Delimiter Detail:</b> The raw UCI file uses <b>semicolons (;)</b> as the delimiter, NOT standard commas. 
    In Hive, this requires exact configuration: <code>ROW FORMAT DELIMITED FIELDS TERMINATED BY ';'</code>. Failing to specify this delimiter causes Hive to read all 33 columns as one giant NULL-filled string!<br/>
    • <b>Evaluation Scale:</b> Grades G1, G2, and final G3 are graded on a <b>0 to 20 scale</b> (10 is the official pass mark in Portugal).
    """
    story.append(Paragraph(p_data, body_style))
    story.append(Spacer(1, 6))

    data_dict_table_data = [
        ["Category", "Columns", "Description & Values"],
        ["Demographics", "school, sex, age, address, famsize, Pstatus", "GP/MS schools, F/M, Age 15-22, Urban/Rural address, Family size, Parents Together/Apart"],
        ["Family & Social", "Medu, Fedu, Mjob, Fjob, guardian, famrel", "Parents' education (0=none to 4=higher), jobs, guardian (mother/father), family quality (1-5)"],
        ["Academic Habits", "traveltime, studytime, failures, schoolsup, famsup", "Travel time, Study time (1=<2h to 4=>10h), Past Failures (0-3), School/Family support (yes/no)"],
        ["Lifestyle & Health", "activities, higher, internet, Dalc, Walc, absences", "Activities, Wants Higher Ed (yes/no), Internet (yes/no), Alcohol usage (1-5), Absences (0-93)"],
        ["Grades (Target)", "G1, G2, G3", "Period 1 (0-20), Period 2 (0-20), Final Grade G3 (0-20, Passing threshold >= 10)"]
    ]
    t_dict = Table(data_dict_table_data, colWidths=[90, 160, 272])
    t_dict.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,1), (-1,-1), c_light),
    ]))
    story.append(t_dict)
    story.append(PageBreak())

    # ========================== SECTION 5: 17 QUERIES & INSIGHTS ==========================
    story.append(Paragraph("5. The 17 HiveQL Analytical Queries & Big Data Insights", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=6))

    queries_summary_data = [
        ["Script", "Queries Included", "Key Analytical Finding Discovered"],
        ["04_basic_analysis.sql", "Q1: Count, Q2: Avg/Min/Max/StdDev G3, Q3: G1/G2/G3 Progression, Q4: Absences", "Cohort has 649 students. Average G3 is 11.91/20 (StdDev 3.23). Scores steadily improve from G1 (11.4) to G3 (11.9)."],
        ["05_performance_analysis.sql", "Q5: Gender Comparison, Q6: School Comparison, Q7: Pass Rate, Q8: Grade Buckets", "Overall Pass Rate is 84.6% (548 passed). Females averaged 12.25 vs 11.41 for males. GP school averaged 12.57 vs 10.65 for MS."],
        ["06_factor_analysis.sql", "Q9: Study Time, Q10: Past Failures, Q11: Absence Quartiles, Q12: Parents, Q13-14: Support", "<b>Study Time Impact:</b> >10 hrs/wk yields 14.33 avg vs 10.66 for <2 hrs.<br/><b>Failures:</b> 1 prior failure crashes average grade to 8.65 (failing!)."],
        ["07_advanced_analysis.sql", "Q15: At-Risk Identification, Q16: Top Achievers Profile, Q17: Alcohol Impact", "Identified 101 failing students and 82 elite achievers (>=16/20). Weekend alcohol (Walc=5) correlates with 10.6 avg grade and higher absences."]
    ]
    t_queries = Table(queries_summary_data, colWidths=[120, 170, 232])
    t_queries.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,1), (-1,-1), c_light),
    ]))
    story.append(t_queries)
    story.append(Spacer(1, 10))

    # ========================== SECTION 6: 3-MEMBER PRESENTATION SCRIPT ==========================
    story.append(Paragraph("6. Presentation Division & Complete Speaking Script", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=6))

    # Speaker 1
    s1_box = [
        [Paragraph("<b>SPEAKER 1: AKASH — Introduction, Problem & Hadoop HDFS Layer</b>", ParagraphStyle('W1', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white))]
    ]
    t_s1 = Table(s1_box, colWidths=[522])
    t_s1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0284c7")), ('PADDING', (0,0), (-1,-1), 4)]))
    story.append(t_s1)
    
    akash_p = """
    <b>What Akash says to Ma'am:</b><br/>
    <i>'Good morning Ma'am. Today our group is presenting our Big Data Analytics project on Student Performance Analytics.'</i><br/>
    • <b>The Problem:</b> <i>'Schools collect vast amounts of demographic, attendance, and behavioral data, but rarely connect these data points in time to prevent student failure.'</i><br/>
    • <b>The Dataset:</b> <i>'We ingested the official UCI Portuguese language dataset consisting of 649 student records across 33 academic and demographic variables.'</i><br/>
    • <b>Storage in Hadoop HDFS:</b> <i>'Instead of an RDBMS table that limits horizontal scalability, we store the raw dataset directly in Hadoop HDFS. HDFS splits data across distributed blocks with fault tolerance. It separates storage from compute, meaning we can scale to millions of records seamlessly.'</i><br/>
    • <b>Transition:</b> <i>'Now Manish will explain how we query and aggregate this distributed data using Apache Hive.'</i>
    """
    story.append(Paragraph(akash_p, body_style))
    story.append(Spacer(1, 6))

    # Speaker 2
    s2_box = [
        [Paragraph("<b>SPEAKER 2: MANISH — Data Warehousing with Apache Hive & Key Findings</b>", ParagraphStyle('W2', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white))]
    ]
    t_s2 = Table(s2_box, colWidths=[522])
    t_s2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f766e")), ('PADDING', (0,0), (-1,-1), 4)]))
    story.append(t_s2)

    manish_p = """
    <b>What Manish says to Ma'am:</b><br/>
    <i>'Thank you Akash. Once the data is stored in HDFS, writing MapReduce in Java is slow and tedious. To solve this, we used <b>Apache Hive</b>.'</i><br/>
    • <b>Schema-on-Read:</b> <i>'We created an <b>EXTERNAL table</b> in Hive with semicolon delimiter parsing. In Hive, schema is applied on read, so our original HDFS data file remains untouched and safe.'</i><br/>
    • <b>17 HiveQL Queries:</b> <i>'We created 7 modular scripts executing 17 queries across basic statistics, gender benchmarks, study habits, and risk detection.'</i><br/>
    • <b>Top 3 Analytical Discoveries:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;1. <b>Study Hours:</b> Studying >10 hrs/wk yields an average grade of 14.33 vs 10.66 for <2 hrs.<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;2. <b>Past Failures:</b> A single past failure drops average grades to 8.65, making it the #1 indicator of academic risk.<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;3. <b>Maternal Education:</b> Students of mothers with higher education averaged 12.87 vs 10.15 for primary education.<br/>
    • <b>Transition:</b> <i>'Now Prathamesh will walk you through our interactive Streamlit application and live dashboard.'</i>
    """
    story.append(Paragraph(manish_p, body_style))
    story.append(Spacer(1, 6))

    # Speaker 3
    s3_box = [
        [Paragraph("<b>SPEAKER 3: PRATHAMESH — Interactive Streamlit Dashboard & Live Demo</b>", ParagraphStyle('W3', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white))]
    ]
    t_s3 = Table(s3_box, colWidths=[522])
    t_s3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#4338ca")), ('PADDING', (0,0), (-1,-1), 4)]))
    story.append(t_s3)

    prathamesh_p = """
    <b>What Prathamesh says to Ma'am (showing the live browser screen):</b><br/>
    <i>'Thank you Manish. To make these Hive query results intuitive for teachers, we built an interactive <b>Streamlit application</b>.'</i><br/>
    • <b>Dashboard Walkthrough:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>KPI Cards:</b> <i>'At the top, Ma'am can see our cohort metrics: 649 students, 84.6% pass rate, and average grade of 11.91/20.'</i><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>Tab 1 & 2:</b> <i>'Shows the steady progression from Period 1 to the final exam, alongside Portuguese grade category distributions.'</i><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>Tab 3 (Factor Matrix):</b> <i>'When we adjust the study time slider on the left, all graphs immediately recompute.'</i><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>Tab 4 (Early Warning Radar):</b> <i>'Our key innovation: teachers can instantly view and export a CSV of students failing or with high absences for early counseling.'</i><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>Tab 5 (Architecture Console):</b> <i>'Inspects our exact HiveQL scripts and real execution outputs.'</i><br/>
    • <b>Conclusion:</b> <i>'HDFS provides storage, Hive executes distributed queries, and Streamlit delivers visual intelligence. Thank you!'</i>
    """
    story.append(Paragraph(prathamesh_p, body_style))
    story.append(PageBreak())

    # ========================== SECTION 7: VIVA Q&A ==========================
    story.append(Paragraph("7. Evaluator Viva Questions & Simple Answers", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=6))

    viva_qa = [
        ("Q1: Why use Hadoop HDFS instead of a standard MySQL database?",
         "<b>Answer:</b> MySQL enforces 'Schema-on-Write' and is bound to a single server's disk and CPU. Hadoop HDFS is a distributed, fault-tolerant file system that splits data into blocks across commodity machines. Storage scales independently of compute, making it ready for massive enterprise data."),

        ("Q2: What is the difference between Managed and External tables in Hive?",
         "<b>Answer:</b> A Managed table owns both the metadata and the data; dropping the table permanently deletes the data from HDFS. An <b>External table</b> manages only the metadata. Dropping the table leaves the raw HDFS dataset completely intact and available to other tools like Spark."),

        ("Q3: Does Streamlit perform the Big Data processing?",
         "<b>Answer (Crucial):</b> <b>No, Ma'am.</b> Streamlit is strictly the <b>Presentation / Visualization Layer</b>. HDFS provides storage, and Apache Hive performs the SQL-based Big Data processing. Streamlit merely displays the analytical output interactively."),

        ("Q4: Why did we have to explicitly configure the semicolon delimiter in Hive?",
         "<b>Answer:</b> By default, Hive expects Ctrl-A or comma delimiters. The UCI Portuguese dataset uses semicolons (<code>;</code>). We explicitly set <code>FIELDS TERMINATED BY ';'</code> so Hive parses each of the 33 columns cleanly instead of merging them into one column."),

        ("Q5: What was the most critical student risk factor identified?",
         "<b>Answer:</b> <b>Past class failures.</b> Students with zero failures passed easily with an average of 12.55/20. Having just one past failure dropped the student's average grade below passing to 8.65/20, proving it is the single strongest warning flag for teachers.")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))

    # ========================== SECTION 8: DEMO CHEATSHEET ==========================
    story.append(Paragraph("8. Live Demonstration Quickstart Commands", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=6))

    cmd_text = """
    <b>1. Run the Full Big Data Pipeline in Terminal:</b><br/>
    <code>./scripts/run_pipeline.sh</code><br/>
    <i>(Downloads data, checks HDFS, executes all 17 queries, and generates reports in output/query-results/)</i><br/><br/>
    <b>2. Launch the Streamlit Dashboard:</b><br/>
    <code>streamlit run app.py</code><br/>
    <i>(Opens http://localhost:8501 in your browser for the live demonstration)</i><br/><br/>
    <b>3. Run Verification Tests:</b><br/>
    <code>pytest tests/ -v</code><br/>
    <i>(Verifies all 9 unit and integration tests pass with 100% success)</i>
    """
    story.append(Paragraph(cmd_text, body_style))

    doc.build(story)
    print(f"Master Project Book PDF generated successfully at: {out_path}")
    return str(out_path)

if __name__ == "__main__":
    build_master_pdf()
