-- ==========================================================
-- Big Data Analytics Project: Student Performance Analytics
-- Script 02: Create Student Table
-- ==========================================================

USE student_performance_bda;

DROP TABLE IF EXISTS student_por;

CREATE EXTERNAL TABLE IF NOT EXISTS student_por (
    school STRING COMMENT 'Student school (GP or MS)',
    sex STRING COMMENT 'Student sex (F or M)',
    age INT COMMENT 'Student age (15 to 22)',
    address STRING COMMENT 'Home address type (U=urban, R=rural)',
    famsize STRING COMMENT 'Family size (LE3 or GT3)',
    Pstatus STRING COMMENT 'Parent cohabitation status (T=together, A=apart)',
    Medu INT COMMENT 'Mother education (0=none to 4=higher)',
    Fedu INT COMMENT 'Father education (0=none to 4=higher)',
    Mjob STRING COMMENT 'Mother job',
    Fjob STRING COMMENT 'Father job',
    reason STRING COMMENT 'Reason for choosing school',
    guardian STRING COMMENT 'Guardian (mother, father, other)',
    traveltime INT COMMENT 'Home to school travel time (1=<15min to 4=>1hour)',
    studytime INT COMMENT 'Weekly study time (1=<2h, 2=2-5h, 3=5-10h, 4=>10h)',
    failures INT COMMENT 'Number of past class failures',
    schoolsup STRING COMMENT 'Extra educational school support (yes/no)',
    famsup STRING COMMENT 'Family educational support (yes/no)',
    paid STRING COMMENT 'Extra paid classes (yes/no)',
    activities STRING COMMENT 'Extra-curricular activities (yes/no)',
    nursery STRING COMMENT 'Attended nursery school (yes/no)',
    higher STRING COMMENT 'Wants to take higher education (yes/no)',
    internet STRING COMMENT 'Internet access at home (yes/no)',
    romantic STRING COMMENT 'In a romantic relationship (yes/no)',
    famrel INT COMMENT 'Family relationship quality (1=very bad to 5=excellent)',
    freetime INT COMMENT 'Free time after school (1=very low to 5=very high)',
    goout INT COMMENT 'Going out with friends (1=very low to 5=very high)',
    Dalc INT COMMENT 'Workday alcohol consumption (1=very low to 5=very high)',
    Walc INT COMMENT 'Weekend alcohol consumption (1=very low to 5=very high)',
    health INT COMMENT 'Current health status (1=very bad to 5=very good)',
    absences INT COMMENT 'Number of school absences (0 to 93)',
    G1 INT COMMENT 'First period grade (0 to 20)',
    G2 INT COMMENT 'Second period grade (0 to 20)',
    G3 INT COMMENT 'Final grade (0 to 20)'
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
STORED AS TEXTFILE
LOCATION '/user/hadoop/student-performance/'
TBLPROPERTIES ("skip.header.line.count"="1");

DESCRIBE FORMATTED student_por;
