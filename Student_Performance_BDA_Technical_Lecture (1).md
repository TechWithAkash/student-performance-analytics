# Big Data Analytics Project

## Student Performance Analytics Using Hadoop HDFS and Apache Hive

> **Project type:** Big Data Analytics (BDA)
> **Primary technologies:** Apache Hadoop, HDFS, Apache Hive, HiveQL
> **Dataset:** UCI Student Performance Dataset
> **Primary file:** `student-por.csv` (Portuguese language course)
> **Primary environment:** macOS / Linux
> **Goal:** Store student data in HDFS and perform SQL-based analytics
> using Hive.

---

# 1. Project Overview

## 1.1 Project Title

**Student Performance Analytics Using Hadoop and Hive**

## 1.2 Problem Statement

Educational institutions collect information about students' academic
performance, study habits, attendance, family background, school
support, and other factors.

The objective of this project is to use a Big Data technology stack to
store and analyze student-performance data. Hadoop HDFS will be used as
the distributed storage layer, while Apache Hive will provide a SQL-like
interface for querying and aggregating the data.

The project will answer questions such as:

- What is the overall student performance?
- How does study time relate to final grades?
- How do previous failures relate to performance?
- How does attendance/absence relate to final grades?
- How does parental education relate to performance?
- How do school and family support affect performance?
- What is the distribution of students across grade categories?
- Which student groups show stronger academic outcomes?

## 1.3 Technology Stack

  Layer                    Technology

---

  Operating System         macOS / Linux
  Storage                  Hadoop HDFS
  Query Engine             Apache Hive
  Query Language           HiveQL
  Dataset Format           CSV
  Dataset Source           UCI Machine Learning Repository
  Optional Visualization   Excel / Power BI / Python

---

# 2. Dataset

## 2.1 Official Source

The dataset is the **Student Performance** dataset from the UCI Machine
Learning Repository.

Official source:

https://archive.ics.uci.edu/dataset/320/student+performance

UCI describes the dataset as student achievement data from two
Portuguese schools, collected from school reports and questionnaires. It
contains academic, demographic, social, and school-related variables.

The UCI page reports 649 instances and 30 core attributes for the
Student Performance dataset and states that there are no missing values.
The downloadable archive contains separate Mathematics
(`student-mat.csv`) and Portuguese (`student-por.csv`) course files.

For this project, use:

```text
student-por.csv
```

This keeps the project simple and gives us a clean 649-record primary
dataset.

## 2.2 Dataset Variables

The original Portuguese dataset contains the following fields:

  Column         Description

---

  `school`       Student's school
  `sex`          Student's sex
  `age`          Student age
  `address`      Urban or rural address
  `famsize`      Family size
  `Pstatus`      Parent cohabitation status
  `Medu`         Mother's education
  `Fedu`         Father's education
  `Mjob`         Mother's job
  `Fjob`         Father's job
  `reason`       Reason for choosing school
  `guardian`     Student's guardian
  `traveltime`   Travel time to school
  `studytime`    Weekly study time
  `failures`     Previous class failures
  `schoolsup`    Extra educational support
  `famsup`       Family educational support
  `paid`         Extra paid classes
  `activities`   Extra-curricular activities
  `nursery`      Attended nursery school
  `higher`       Wants higher education
  `internet`     Internet access at home
  `romantic`     Romantic relationship
  `famrel`       Family relationship quality
  `freetime`     Free time after school
  `goout`        Going out with friends
  `Dalc`         Workday alcohol consumption
  `Walc`         Weekend alcohol consumption
  `health`       Current health status
  `absences`     Number of school absences
  `G1`           First-period grade
  `G2`           Second-period grade
  `G3`           Final grade

Grades are on a 0--20 scale.

> **Important:** `G3` is the final grade. UCI notes that `G1` and `G2`
> are strongly correlated with `G3` because they are earlier-period
> grades. For a descriptive BDA project, we can analyze them; we should
> not claim that our Hive queries prove causation.

---

# 3. Project Architecture

```text
                    UCI PUBLIC DATASET
                           |
                           v
                    student-por.csv
                           |
                           v
                    Data Inspection
                           |
                           v
                    Data Preparation
                           |
                           v
                 +-------------------+
                 |     Hadoop HDFS   |
                 |                   |
                 |  Distributed      |
                 |  Storage          |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 |      Apache Hive  |
                 |                   |
                 |      HiveQL       |
                 +---------+---------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        Grade Analysis  Student      Factor Analysis
                        Groups
             |             |             |
             +-------------+-------------+
                           |
                           v
                    Analytical Results
                           |
                           v
                  Charts / Dashboard
                           |
                           v
                    Final Conclusions
```

---

# 4. Project Directory Structure

Create the following project structure:

```text
student-performance-bda/
├── data/
│   ├── raw/
│   │   └── student-por.csv
│   └── processed/
│       └── student_por_clean.csv
├── hive/
│   ├── 01_create_database.sql
│   ├── 02_create_table.sql
│   ├── 03_load_data.sql
│   ├── 04_basic_analysis.sql
│   ├── 05_performance_analysis.sql
│   ├── 06_factor_analysis.sql
│   └── 07_advanced_analysis.sql
├── output/
│   └── query-results/
├── docs/
│   └── project-report.md
└── README.md
```

Create it with:

```bash
mkdir -p student-performance-bda/data/raw
mkdir -p student-performance-bda/data/processed
mkdir -p student-performance-bda/hive
mkdir -p student-performance-bda/output/query-results
mkdir -p student-performance-bda/docs
cd student-performance-bda
```

---

# 5. Prerequisites

You need:

- Java
- Hadoop
- HDFS
- Hive
- Terminal
- A browser
- The UCI dataset

Check Java:

```bash
java -version
```

Check SSH:

```bash
ssh -V
```

On macOS, install Homebrew if it is not already installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then:

```bash
brew update
```

Install Java:

```bash
brew install openjdk
```

Verify:

```bash
java -version
```

If macOS does not automatically expose Java, follow the path printed by
Homebrew. A typical command is:

```bash
sudo ln -sfn $(brew --prefix openjdk)/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
```

Then verify again:

```bash
java -version
```

---

# 6. Download the UCI Dataset

Create the raw-data directory:

```bash
mkdir -p data/raw
```

Download the official UCI archive:

```bash
curl -L "https://archive.ics.uci.edu/static/public/320/student+performance.zip" -o data/raw/student-performance.zip
```

Check the downloaded file:

```bash
ls -lh data/raw/
```

Extract it:

```bash
unzip data/raw/student-performance.zip -d data/raw/
```

List the files:

```bash
find data/raw -maxdepth 2 -type f
```

You should find files including:

```text
student-mat.csv
student-por.csv
```

For this project, use:

```text
student-por.csv
```

Copy it into the project location if necessary:

```bash
cp data/raw/student-por.csv data/raw/
```

Check the file:

```bash
head data/raw/student-por.csv
```

Check the number of lines:

```bash
wc -l data/raw/student-por.csv
```

The file should contain a header plus the student records.

---

# 7. Understand the Dataset Delimiter

The UCI files use semicolon-separated values.

Check the first line:

```bash
head -n 1 data/raw/student-por.csv
```

You will see fields separated by:

```text
;
```

This matters because Hive must be configured with:

```sql
FIELDS TERMINATED BY ';'
```

Do not change the delimiter unless you intentionally create a new
processed CSV.

---

# 8. Optional Data Validation

Check the first five records:

```bash
head -n 6 data/raw/student-por.csv
```

Check the last five records:

```bash
tail -n 5 data/raw/student-por.csv
```

Count records excluding the header:

```bash
tail -n +2 data/raw/student-por.csv | wc -l
```

Expected primary dataset size:

```text
649 records
```

Check the number of columns in the first record:

```bash
head -n 2 data/raw/student-por.csv | tail -n 1 | awk -F';' '{print NF}'
```

The expected number of fields is:

```text
33
```

This includes the 30 original explanatory attributes plus `G1`, `G2`,
and `G3`.

---

# 9. Install and Configure Hadoop

## 9.1 Download Hadoop

Download a compatible Apache Hadoop 3.x binary release from:

https://hadoop.apache.org/releases.html

After downloading the archive, extract it.

Example:

```bash
tar -xzf hadoop-3.x.x.tar.gz
```

Move it:

```bash
sudo mv hadoop-3.x.x /usr/local/hadoop
```

If your macOS permissions prevent writing to `/usr/local`, place Hadoop
somewhere in your home directory instead:

```bash
mkdir -p $HOME/hadoop
mv hadoop-3.x.x $HOME/hadoop/
```

The rest of this document assumes:

```text
$HOME/hadoop/hadoop-3.x.x
```

---

# 10. Set Hadoop Environment Variables

Open your shell configuration:

```bash
nano ~/.zshrc
```

Add:

```bash
export JAVA_HOME=$(/usr/libexec/java_home)
export HADOOP_HOME=$HOME/hadoop/hadoop-3.x.x
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

Save the file.

Reload:

```bash
source ~/.zshrc
```

Check:

```bash
echo $HADOOP_HOME
```

Check Hadoop:

```bash
hadoop version
```

---

# 11. Configure Hadoop

Move into the Hadoop configuration directory:

```bash
cd $HADOOP_HOME/etc/hadoop
```

## 11.1 Configure Java

Open:

```bash
nano hadoop-env.sh
```

Make sure Java is configured:

```bash
export JAVA_HOME=$(/usr/libexec/java_home)
```

---

# 12. Configure core-site.xml

Open:

```bash
nano core-site.xml
```

Use:

```xml
<?xml version="1.0"?>
<configuration>

    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>

</configuration>
```

---

# 13. Configure hdfs-site.xml

Open:

```bash
nano hdfs-site.xml
```

Use:

```xml
<?xml version="1.0"?>
<configuration>

    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>

    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///Users/YOUR_USERNAME/hadoopdata/hdfs/namenode</value>
    </property>

    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///Users/YOUR_USERNAME/hadoopdata/hdfs/datanode</value>
    </property>

</configuration>
```

Replace:

```text
YOUR_USERNAME
```

with your macOS username.

You can find it with:

```bash
whoami
```

For example:

```text
/Users/akash/hadoopdata/hdfs/namenode
```

---

# 14. Configure mapred-site.xml

Copy the template:

```bash
cp mapred-site.xml.template mapred-site.xml
```

Open:

```bash
nano mapred-site.xml
```

Use:

```xml
<?xml version="1.0"?>
<configuration>

    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>

</configuration>
```

---

# 15. Configure yarn-site.xml

Open:

```bash
nano yarn-site.xml
```

Use:

```xml
<?xml version="1.0"?>
<configuration>

    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>

    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>
            JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,
            HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,
            HADOOP_YARN_HOME,HADOOP_MAPRED_HOME
        </value>
    </property>

</configuration>
```

---

# 16. Configure SSH for Hadoop

Check whether localhost SSH works:

```bash
ssh localhost
```

If prompted for confirmation:

```text
yes
```

If password authentication is requested and you do not already have a
key, create one:

```bash
ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa
```

Add the public key:

```bash
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

Set permissions:

```bash
chmod 600 ~/.ssh/authorized_keys
```

Test again:

```bash
ssh localhost
```

Exit:

```bash
exit
```

---

# 17. Create Hadoop Data Directories

Create:

```bash
mkdir -p $HOME/hadoopdata/hdfs/namenode
mkdir -p $HOME/hadoopdata/hdfs/datanode
```

---

# 18. Format the HDFS NameNode

**Only perform this when setting up HDFS for the first time.**

Run:

```bash
hdfs namenode -format
```

When successful, you should see a message indicating that the NameNode
has been formatted successfully.

---

# 19. Start Hadoop

Start HDFS:

```bash
start-dfs.sh
```

Start YARN:

```bash
start-yarn.sh
```

Check Java processes:

```bash
jps
```

You should see processes similar to:

```text
NameNode
DataNode
SecondaryNameNode
ResourceManager
NodeManager
```

---

# 20. Verify HDFS

Check the root directory:

```bash
hdfs dfs -ls /
```

Create the project directory:

```bash
hdfs dfs -mkdir -p /bda
```

Create the dataset directory:

```bash
hdfs dfs -mkdir -p /bda/student-performance
```

Check:

```bash
hdfs dfs -ls /bda
```

---

# 21. Upload the Dataset to HDFS

Upload:

```bash
hdfs dfs -put data/raw/student-por.csv /bda/student-performance/
```

Verify:

```bash
hdfs dfs -ls /bda/student-performance
```

You should see:

```text
student-por.csv
```

---

# 22. Read the Dataset Directly from HDFS

Display the header:

```bash
hdfs dfs -cat /bda/student-performance/student-por.csv | head -n 1
```

Display the first five data records:

```bash
hdfs dfs -cat /bda/student-performance/student-por.csv | head -n 6
```

Count lines:

```bash
hdfs dfs -cat /bda/student-performance/student-por.csv | wc -l
```

---

# 23. Useful HDFS Commands

List directories:

```bash
hdfs dfs -ls /
```

List project directory:

```bash
hdfs dfs -ls /bda
```

Check file size:

```bash
hdfs dfs -du -h /bda/student-performance/
```

Check HDFS capacity:

```bash
hdfs dfs -df -h
```

View a file:

```bash
hdfs dfs -cat /bda/student-performance/student-por.csv
```

Download a file from HDFS:

```bash
hdfs dfs -get /bda/student-performance/student-por.csv data/
```

Delete an HDFS file:

```bash
hdfs dfs -rm /bda/student-performance/student-por.csv
```

Delete a directory recursively:

```bash
hdfs dfs -rm -r /bda/student-performance
```

---

# 24. Install Apache Hive

Download a compatible Apache Hive release from:

https://hive.apache.org/

Extract it:

```bash
tar -xzf apache-hive-4.x.x-bin.tar.gz
```

Move it:

```bash
mkdir -p $HOME/hive
mv apache-hive-4.x.x-bin $HOME/hive/
```

Set environment variables:

```bash
nano ~/.zshrc
```

Add:

```bash
export HIVE_HOME=$HOME/hive/apache-hive-4.x.x-bin
export PATH=$PATH:$HIVE_HOME/bin
```

Reload:

```bash
source ~/.zshrc
```

Check:

```bash
hive --version
```

---

# 25. Configure Hive

Create the Hive configuration file:

```bash
cd $HIVE_HOME/conf
cp hive-default.xml.template hive-site.xml
```

For a simple academic/local project, Hive's embedded metastore can be
used.

Create a local warehouse directory:

```bash
mkdir -p $HOME/hive-warehouse
```

The exact Hive 4 configuration can vary by distribution. If the
installation complains about an unset warehouse or metastore property,
add the required property to `hive-site.xml`.

For a simple local setup, the important warehouse location is
conceptually:

```text
hdfs:///user/hive/warehouse
```

Create it:

```bash
hdfs dfs -mkdir -p /user/hive/warehouse
```

Give the current user access:

```bash
hdfs dfs -chmod -R 777 /user/hive/warehouse
```

For a college demonstration this is acceptable on a local single-user
installation. Do not use `777` permissions in a production Hadoop
cluster.

---

# 26. Initialize the Hive Metastore

If using the embedded Derby metastore for the first time:

```bash
schematool -dbType derby -initSchema
```

If the schema already exists, do not initialize it again.

---

# 27. Start Hive

Run:

```bash
hive
```

Depending on your Hive version, the CLI may display a prompt such as:

```text
hive>
```

Test:

```sql
SHOW DATABASES;
```

Exit:

```sql
EXIT;
```

---

# 28. Create the BDA Database

Open Hive:

```bash
hive
```

Create database:

```sql
CREATE DATABASE student_bda;
```

Verify:

```sql
SHOW DATABASES;
```

Select the database:

```sql
USE student_bda;
```

---

# 29. Create the Student Table

The UCI CSV uses semicolon delimiters.

Create the table:

```sql
CREATE TABLE students (
    school STRING,
    sex STRING,
    age INT,
    address STRING,
    famsize STRING,
    Pstatus STRING,
    Medu INT,
    Fedu INT,
    Mjob STRING,
    Fjob STRING,
    reason STRING,
    guardian STRING,
    traveltime INT,
    studytime INT,
    failures INT,
    schoolsup STRING,
    famsup STRING,
    paid STRING,
    activities STRING,
    nursery STRING,
    higher STRING,
    internet STRING,
    romantic STRING,
    famrel INT,
    freetime INT,
    goout INT,
    Dalc INT,
    Walc INT,
    health INT,
    absences INT,
    G1 INT,
    G2 INT,
    G3 INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
STORED AS TEXTFILE;
```

Check:

```sql
DESCRIBE students;
```

---

# 30. Load the HDFS Dataset into Hive

Use:

```sql
LOAD DATA INPATH '/bda/student-performance/student-por.csv'
INTO TABLE students;
```

Verify:

```sql
SELECT COUNT(*) FROM students;
```

Expected result:

```text
649
```

Check sample data:

```sql
SELECT * FROM students LIMIT 10;
```

---

# 31. Important Note About LOAD DATA

When using:

```sql
LOAD DATA INPATH
```

Hive may move the file from its original HDFS location into the Hive
table's managed storage location.

Therefore, after loading, verify:

```bash
hdfs dfs -ls /bda/student-performance/
```

and:

```bash
hdfs dfs -ls /user/hive/warehouse/student_bda.db/students/
```

Do not assume that the original HDFS location still contains the file.

---

# 32. Basic Hive Validation

Show databases:

```sql
SHOW DATABASES;
```

Select project database:

```sql
USE student_bda;
```

Show tables:

```sql
SHOW TABLES;
```

Describe table:

```sql
DESCRIBE students;
```

Count rows:

```sql
SELECT COUNT(*) AS total_students
FROM students;
```

Preview:

```sql
SELECT *
FROM students
LIMIT 10;
```

---

# 33. Analysis Section

## Query 1 --- Total Number of Students

```sql
SELECT COUNT(*) AS total_students
FROM students;
```

### Purpose

Determines the total number of records in the dataset.

---

# 34. Query 2 --- Average Final Grade

```sql
SELECT ROUND(AVG(G3), 2) AS average_final_grade
FROM students;
```

### Purpose

Finds the average final academic grade.

---

# 35. Query 3 --- Highest Final Grade

```sql
SELECT MAX(G3) AS highest_final_grade
FROM students;
```

---

# 36. Query 4 --- Lowest Final Grade

```sql
SELECT MIN(G3) AS lowest_final_grade
FROM students;
```

---

# 37. Query 5 --- Average Grade by Gender

```sql
SELECT
    sex,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY sex
ORDER BY average_final_grade DESC;
```

### Insight

This allows comparison of average performance between student groups.

---

# 38. Query 6 --- Students by School

```sql
SELECT
    school,
    COUNT(*) AS total_students
FROM students
GROUP BY school;
```

---

# 39. Query 7 --- Average Grade by School

```sql
SELECT
    school,
    COUNT(*) AS total_students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY school
ORDER BY average_final_grade DESC;
```

---

# 40. Query 8 --- Performance by Study Time

The UCI coding is:

```text
1 = <2 hours
2 = 2–5 hours
3 = 5–10 hours
4 = >10 hours
```

Query:

```sql
SELECT
    studytime,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY studytime
ORDER BY studytime;
```

For a presentation-friendly result:

```sql
SELECT
    CASE
        WHEN studytime = 1 THEN '<2 hours'
        WHEN studytime = 2 THEN '2–5 hours'
        WHEN studytime = 3 THEN '5–10 hours'
        WHEN studytime = 4 THEN '>10 hours'
    END AS study_time_group,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY studytime
ORDER BY studytime;
```

---

# 41. Query 9 --- Previous Failures vs Performance

```sql
SELECT
    failures,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY failures
ORDER BY failures;
```

This examines whether students with more previous failures have
different average final grades.

---

# 42. Query 10 --- Absence Analysis

```sql
SELECT
    ROUND(AVG(absences), 2) AS average_absences,
    MAX(absences) AS maximum_absences,
    MIN(absences) AS minimum_absences
FROM students;
```

---

# 43. Query 11 --- Absence Categories

```sql
SELECT
    CASE
        WHEN absences = 0 THEN 'No absences'
        WHEN absences BETWEEN 1 AND 5 THEN '1–5'
        WHEN absences BETWEEN 6 AND 10 THEN '6–10'
        WHEN absences BETWEEN 11 AND 20 THEN '11–20'
        ELSE '20+'
    END AS absence_group,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY
    CASE
        WHEN absences = 0 THEN 'No absences'
        WHEN absences BETWEEN 1 AND 5 THEN '1–5'
        WHEN absences BETWEEN 6 AND 10 THEN '6–10'
        WHEN absences BETWEEN 11 AND 20 THEN '11–20'
        ELSE '20+'
    END;
```

---

# 44. Query 12 --- Parent Education vs Performance

Mother:

```sql
SELECT
    Medu,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY Medu
ORDER BY Medu;
```

Father:

```sql
SELECT
    Fedu,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY Fedu
ORDER BY Fedu;
```

---

# 45. Query 13 --- Internet Access vs Performance

```sql
SELECT
    internet,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY internet
ORDER BY average_final_grade DESC;
```

---

# 46. Query 14 --- School Support vs Performance

```sql
SELECT
    schoolsup,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY schoolsup
ORDER BY average_final_grade DESC;
```

---

# 47. Query 15 --- Family Support vs Performance

```sql
SELECT
    famsup,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY famsup
ORDER BY average_final_grade DESC;
```

---

# 48. Query 16 --- Higher Education Intent

```sql
SELECT
    higher,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY higher
ORDER BY average_final_grade DESC;
```

---

# 49. Query 17 --- Grade Categories

Create understandable academic categories:

```sql
SELECT
    CASE
        WHEN G3 < 10 THEN 'Below 10'
        WHEN G3 BETWEEN 10 AND 12 THEN '10–12'
        WHEN G3 BETWEEN 13 AND 15 THEN '13–15'
        WHEN G3 BETWEEN 16 AND 18 THEN '16–18'
        ELSE '19–20'
    END AS grade_group,
    COUNT(*) AS students
FROM students
GROUP BY
    CASE
        WHEN G3 < 10 THEN 'Below 10'
        WHEN G3 BETWEEN 10 AND 12 THEN '10–12'
        WHEN G3 BETWEEN 13 AND 15 THEN '13–15'
        WHEN G3 BETWEEN 16 AND 18 THEN '16–18'
        ELSE '19–20'
    END
ORDER BY grade_group;
```

---

# 50. Query 18 --- Top 10 Students

```sql
SELECT
    school,
    sex,
    age,
    G1,
    G2,
    G3
FROM students
ORDER BY G3 DESC
LIMIT 10;
```

---

# 51. Query 19 --- Students at Academic Risk

For this project, define an academic-risk group as students with a final
grade below 10.

```sql
SELECT
    COUNT(*) AS students_at_risk
FROM students
WHERE G3 < 10;
```

List them:

```sql
SELECT
    school,
    sex,
    age,
    failures,
    absences,
    studytime,
    G1,
    G2,
    G3
FROM students
WHERE G3 < 10
ORDER BY G3 ASC;
```

> This is a project-defined analytical category, not an official UCI
> classification.

---

# 52. Query 20 --- Combined Student Profile Analysis

This is a useful final Hive query:

```sql
SELECT
    school,
    sex,
    studytime,
    failures,
    internet,
    schoolsup,
    famsup,
    COUNT(*) AS students,
    ROUND(AVG(G3), 2) AS average_final_grade
FROM students
GROUP BY
    school,
    sex,
    studytime,
    failures,
    internet,
    schoolsup,
    famsup
ORDER BY average_final_grade DESC;
```

This demonstrates multi-dimensional aggregation.

---

# 53. Advanced Hive Analysis

## 53.1 Average Performance Across G1, G2 and G3

```sql
SELECT
    ROUND(AVG(G1), 2) AS average_G1,
    ROUND(AVG(G2), 2) AS average_G2,
    ROUND(AVG(G3), 2) AS average_G3
FROM students;
```

This can be represented as a progression chart.

---

# 54. G1/G2/G3 Performance by School

```sql
SELECT
    school,
    ROUND(AVG(G1), 2) AS avg_G1,
    ROUND(AVG(G2), 2) AS avg_G2,
    ROUND(AVG(G3), 2) AS avg_G3
FROM students
GROUP BY school;
```

---

# 55. Create an Analytical View

Hive views allow us to save a reusable analytical query.

```sql
CREATE VIEW student_performance_summary AS
SELECT
    school,
    sex,
    studytime,
    failures,
    absences,
    internet,
    schoolsup,
    famsup,
    G1,
    G2,
    G3
FROM students;
```

Check:

```sql
SHOW VIEWS;
```

Use:

```sql
SELECT *
FROM student_performance_summary
LIMIT 10;
```

---

# 56. Export Hive Results

Example:

```bash
mkdir -p output/query-results
```

Run Hive from the terminal:

```bash
hive -e "
USE student_bda;
SELECT school, COUNT(*) AS students, ROUND(AVG(G3),2) AS average_grade
FROM students
GROUP BY school;
" > output/query-results/school-performance.txt
```

View:

```bash
cat output/query-results/school-performance.txt
```

Export another result:

```bash
hive -e "
USE student_bda;
SELECT studytime, COUNT(*) AS students, ROUND(AVG(G3),2) AS average_grade
FROM students
GROUP BY studytime
ORDER BY studytime;
" > output/query-results/study-time-analysis.txt
```

---

# 57. Recommended Dashboard

The final representation should contain approximately:

## KPI Cards

```text
Total Students
Average Final Grade
Highest Grade
Lowest Grade
Average Absences
```

## Chart 1 --- Students by School

Bar chart.

## Chart 2 --- Average Grade by Study Time

Bar chart.

## Chart 3 --- Grade Distribution

Bar chart or pie chart.

## Chart 4 --- Previous Failures vs Average Grade

Line/bar chart.

## Chart 5 --- Absence Group vs Average Grade

Bar chart.

## Chart 6 --- Internet Access vs Average Grade

Bar chart.

## Chart 7 --- G1 → G2 → G3

Line chart showing grade progression.

## Chart 8 --- School Comparison

Grouped bar chart comparing G1, G2, and G3.

---

# 58. Suggested Dashboard Layout

```text
┌────────────────────────────────────────────────────────────┐
│            STUDENT PERFORMANCE ANALYTICS                  │
│              Hadoop + Hive BDA Project                    │
├──────────────┬──────────────┬──────────────┬──────────────┤
│   STUDENTS   │  AVG GRADE   │ HIGH GRADE   │ AVG ABSENCE  │
│     649      │     XX.XX    │      XX      │     XX.XX    │
├──────────────┴──────────────┴──────────────┴──────────────┤
│                                                          │
│        AVERAGE GRADE BY STUDY TIME                      │
│                                                          │
│        █████                                             │
│        ████████                                          │
│        ███████████                                       │
│        █████████                                         │
│                                                          │
├─────────────────────────────┬────────────────────────────┤
│  GRADE DISTRIBUTION         │  PERFORMANCE BY SCHOOL     │
│                             │                            │
│  ███                        │  G1 ████                   │
│  ███████                    │  G2 █████                  │
│  ██████████                 │  G3 ██████                 │
│                             │                            │
├─────────────────────────────┴────────────────────────────┤
│                                                          │
│              G1 → G2 → G3 PERFORMANCE                    │
│                                                          │
│                  ╱────╲                                  │
│          ╱──────╱      ╲────                            │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

# 59. Project Findings

Do not write findings before running the actual Hive queries.

After running the queries, record findings in this format:

```text
Finding 1:
The dataset contains ______ students.

Finding 2:
The overall average final grade is ______.

Finding 3:
The study-time group ______ has the highest average final grade.

Finding 4:
Students with ______ previous failures show the lowest average performance.

Finding 5:
The ______ school has the higher average final grade.

Finding 6:
The grade category ______ contains the largest number of students.

Finding 7:
Students with ______ absences show ______ average performance.
```

This ensures that the report is based on **actual query results**
instead of invented observations.

---

# 60. Important Analytical Limitation

This project is primarily **descriptive Big Data Analytics**.

Hive aggregations can show relationships and patterns, but they do not
prove causation.

For example:

> If students with more study time have higher average grades, we can
> report an association in this dataset.

We should not write:

> More study time definitely causes higher grades.

This distinction makes the project technically stronger.

---

# 61. Stopping Hadoop

When finished, stop YARN:

```bash
stop-yarn.sh
```

Stop HDFS:

```bash
stop-dfs.sh
```

Verify:

```bash
jps
```

The Hadoop daemon processes should no longer be running.

---

# 62. Starting the Project Again

Whenever you want to continue the project:

### Step 1 --- Start HDFS

```bash
start-dfs.sh
```

### Step 2 --- Start YARN

```bash
start-yarn.sh
```

### Step 3 --- Verify

```bash
jps
```

### Step 4 --- Start Hive

```bash
hive
```

### Step 5 --- Select database

```sql
USE student_bda;
```

### Step 6 --- Verify table

```sql
SHOW TABLES;
```

### Step 7 --- Verify data

```sql
SELECT COUNT(*) FROM students;
```

---

# 63. Useful Hadoop Web Interfaces

NameNode UI is commonly available at:

```text
http://localhost:9870
```

YARN ResourceManager UI is commonly available at:

```text
http://localhost:8088
```

Use these interfaces to demonstrate that:

- HDFS is running
- NameNode is active
- DataNode is active
- Files exist in HDFS
- YARN is running
- Hadoop resources are available

---

# 64. Common Problems and Solutions

## Problem 1 --- `hadoop: command not found`

Check:

```bash
echo $HADOOP_HOME
```

Check:

```bash
which hadoop
```

Reload:

```bash
source ~/.zshrc
```

Check:

```bash
hadoop version
```

---

## Problem 2 --- Java not found

Check:

```bash
java -version
```

Check:

```bash
/usr/libexec/java_home
```

Set:

```bash
export JAVA_HOME=$(/usr/libexec/java_home)
```

Then:

```bash
source ~/.zshrc
```

---

## Problem 3 --- HDFS refuses connection

Check:

```bash
jps
```

Start:

```bash
start-dfs.sh
```

Then:

```bash
hdfs dfs -ls /
```

---

## Problem 4 --- NameNode formatting issue

Only format a brand-new NameNode:

```bash
hdfs namenode -format
```

Do not repeatedly format an existing project because formatting destroys
the NameNode metadata.

---

## Problem 5 --- Hive cannot find the table

Inside Hive:

```sql
SHOW DATABASES;
```

Then:

```sql
USE student_bda;
```

Then:

```sql
SHOW TABLES;
```

Then:

```sql
DESCRIBE students;
```

---

## Problem 6 --- Hive returns zero records

Run:

```sql
SELECT COUNT(*) FROM students;
```

Check the HDFS/Hive table location:

```sql
DESCRIBE FORMATTED students;
```

Look for:

```text
Location:
```

Then inspect that HDFS location with:

```bash
hdfs dfs -ls <LOCATION>
```

---

## Problem 7 --- Columns appear incorrectly

The UCI dataset is semicolon-separated.

The Hive table must contain:

```sql
FIELDS TERMINATED BY ';'
```

If you use comma instead, the entire row may be interpreted as one
field.

---

# 65. Suggested SQL Script Organization

Save the following scripts.

## `01_create_database.sql`

```sql
CREATE DATABASE IF NOT EXISTS student_bda;
USE student_bda;
```

## `02_create_table.sql`

Put the complete `CREATE TABLE students` statement here.

## `03_load_data.sql`

```sql
USE student_bda;

LOAD DATA INPATH
'/bda/student-performance/student-por.csv'
INTO TABLE students;
```

## `04_basic_analysis.sql`

Put queries 1--7 here.

## `05_performance_analysis.sql`

Put queries 8--11 here.

## `06_factor_analysis.sql`

Put queries 12--16 here.

## `07_advanced_analysis.sql`

Put queries 17--20 and the view here.

Run a complete script:

```bash
hive -f hive/04_basic_analysis.sql
```

---

# 66. Project Demonstration Order

During the practical/viva, demonstrate in this order:

### Step 1

Show the public UCI dataset.

### Step 2

Show the CSV file.

```bash
head data/raw/student-por.csv
```

### Step 3

Show Hadoop version.

```bash
hadoop version
```

### Step 4

Show running Hadoop services.

```bash
jps
```

### Step 5

Show HDFS directory.

```bash
hdfs dfs -ls /bda/student-performance
```

### Step 6

Show Hive version.

```bash
hive --version
```

### Step 7

Open Hive.

```bash
hive
```

### Step 8

Show database.

```sql
SHOW DATABASES;
```

### Step 9

Show table.

```sql
USE student_bda;
SHOW TABLES;
```

### Step 10

Show schema.

```sql
DESCRIBE students;
```

### Step 11

Show record count.

```sql
SELECT COUNT(*) FROM students;
```

### Step 12

Run your major analysis queries.

### Step 13

Show the dashboard.

### Step 14

Explain the findings and limitations.

---

# 67. Viva Questions and Answers

## Q1. What is Hadoop?

Hadoop is an open-source framework used for distributed storage and
processing of large datasets.

## Q2. What is HDFS?

HDFS stands for Hadoop Distributed File System. It stores files across
distributed storage nodes and is designed for reliable large-scale data
storage.

## Q3. Why did you use HDFS?

HDFS provides the storage layer of our Hadoop-based BDA pipeline.

## Q4. What is Hive?

Apache Hive is a data warehouse and SQL-based query system built for
Hadoop ecosystems. It allows users to analyze data using HiveQL.

## Q5. What is HiveQL?

HiveQL is Hive's SQL-like query language.

## Q6. Why use Hive instead of normal SQL?

Traditional SQL databases are designed primarily for structured database
workloads. Hive provides SQL-like analytics over data stored in
Hadoop-compatible storage.

## Q7. What is the difference between HDFS and Hive?

**HDFS stores the data. Hive queries and analyzes the data.**

## Q8. What dataset did you use?

The UCI Student Performance dataset.

## Q9. How many records are used?

The primary Portuguese-course file contains 649 student records.

## Q10. What is G3?

G3 is the final-period/final-year grade for the course, on a 0--20
scale.

## Q11. Why did you use `student-por.csv`?

It provides a single clean subject dataset with 649 records, keeping the
Hadoop/Hive project straightforward while still allowing multiple
analytical dimensions.

## Q12. What is the role of `GROUP BY`?

It groups records according to one or more dimensions so aggregate
functions such as `COUNT`, `AVG`, `SUM`, `MIN`, and `MAX` can be
applied.

## Q13. What is HDFS replication?

Replication means maintaining multiple copies of data blocks for fault
tolerance. In this local single-node project, replication is configured
as 1.

## Q14. Is this machine-learning project?

No. The main objective is Big Data storage and descriptive analytics
using Hadoop and Hive. Machine learning is outside the core scope.

## Q15. What is the biggest limitation?

The dataset is useful for demonstrating the Hadoop/Hive workflow, but it
is not a massive production-scale dataset. The project demonstrates the
technology pipeline rather than claiming that 649 records alone
constitute industrial-scale Big Data.

---

# 68. Final Project Report Structure

Your final college report should contain:

```text
1. Title Page
2. Certificate
3. Acknowledgement
4. Abstract
5. Introduction
6. Problem Statement
7. Objectives
8. Dataset Description
9. Technologies Used
10. System Architecture
11. Hadoop HDFS Implementation
12. Hive Implementation
13. Database and Table Design
14. HiveQL Queries
15. Results
16. Visualization
17. Findings
18. Limitations
19. Future Scope
20. Conclusion
21. References
```

---

# 69. Abstract

Use the following as the project abstract:

> This project presents a Student Performance Analytics system using
> Hadoop HDFS and Apache Hive. The system uses publicly available
> student performance data from the UCI Machine Learning Repository. The
> dataset contains academic, demographic, social, and school-related
> information about students.
>
> The dataset is stored in Hadoop Distributed File System (HDFS), while
> Apache Hive is used to perform SQL-based analysis through HiveQL. The
> analysis examines student performance across multiple dimensions,
> including study time, previous failures, school, gender, parental
> education, educational support, Internet access, and absences.
>
> The project demonstrates how Hadoop-based technologies can be used to
> store, organize, query, and analyze structured datasets. The results
> are presented through tables and visualizations to identify meaningful
> patterns in student performance. The project focuses on descriptive
> analytics and does not claim causal relationships between student
> characteristics and academic outcomes.

---

# 70. Objectives

The main objectives are:

1. To understand the Hadoop ecosystem.
2. To configure Hadoop and HDFS in a local environment.
3. To store a public dataset in HDFS.
4. To install and configure Apache Hive.
5. To create a Hive database and table.
6. To load HDFS data into Hive.
7. To perform analytical queries using HiveQL.
8. To analyze academic performance patterns.
9. To generate meaningful analytical results.
10. To visualize the results for easier interpretation.
11. To understand the role of distributed storage and SQL-based Big Data
    analytics.

---

# 71. Future Scope

Future versions can extend the project with:

- Larger student datasets
- Multiple academic subjects
- Combining Mathematics and Portuguese datasets
- Apache Spark
- Machine-learning models
- Student-risk prediction
- Automated dashboards
- Real-time academic analytics
- Cloud-based Hadoop/Spark processing

---

# 72. Conclusion

The project demonstrates an end-to-end Big Data Analytics workflow using
Hadoop HDFS and Apache Hive. The student-performance dataset is first
inspected and then stored in HDFS. Hive provides a structured SQL-like
interface for querying the data and performing aggregations.

Through HiveQL, the project analyzes academic performance according to
study time, previous failures, absences, school, gender, parental
education, educational support, Internet access, and other attributes.

The project therefore demonstrates the practical use of Hadoop for
distributed data storage and Hive for structured Big Data analytics
while keeping the dataset and analytical workflow understandable for an
academic project.

---

# 73. References

1. UCI Machine Learning Repository --- Student Performance:
   https://archive.ics.uci.edu/dataset/320/student+performance
2. Hadoop: https://hadoop.apache.org/
3. Apache Hive: https://hive.apache.org/
4. Cortez, P. (2008). Student Performance Dataset. UCI Machine Learning
   Repository.

---

# 74. Final Command Cheat Sheet

## Project setup

```bash
mkdir -p student-performance-bda/data/raw
mkdir -p student-performance-bda/data/processed
mkdir -p student-performance-bda/hive
mkdir -p student-performance-bda/output/query-results
mkdir -p student-performance-bda/docs
cd student-performance-bda
```

## Dataset

```bash
curl -L "https://archive.ics.uci.edu/static/public/320/student+performance.zip" -o data/raw/student-performance.zip
unzip data/raw/student-performance.zip -d data/raw/
head data/raw/student-por.csv
tail -n +2 data/raw/student-por.csv | wc -l
```

## Hadoop

```bash
hadoop version
start-dfs.sh
start-yarn.sh
jps
```

## HDFS

```bash
hdfs dfs -mkdir -p /bda/student-performance
hdfs dfs -put data/raw/student-por.csv /bda/student-performance/
hdfs dfs -ls /bda/student-performance
hdfs dfs -cat /bda/student-performance/student-por.csv | head -n 6
```

## Hive

```bash
hive --version
hive
```

Inside Hive:

```sql
CREATE DATABASE student_bda;
USE student_bda;
SHOW TABLES;
DESCRIBE students;
SELECT COUNT(*) FROM students;
SELECT * FROM students LIMIT 10;
```

## Analysis

```sql
SELECT COUNT(*) FROM students;

SELECT ROUND(AVG(G3),2) FROM students;

SELECT sex, COUNT(*), ROUND(AVG(G3),2)
FROM students
GROUP BY sex;

SELECT school, COUNT(*), ROUND(AVG(G3),2)
FROM students
GROUP BY school;

SELECT studytime, COUNT(*), ROUND(AVG(G3),2)
FROM students
GROUP BY studytime;

SELECT failures, COUNT(*), ROUND(AVG(G3),2)
FROM students
GROUP BY failures;

SELECT internet, COUNT(*), ROUND(AVG(G3),2)
FROM students
GROUP BY internet;

SELECT schoolsup, COUNT(*), ROUND(AVG(G3),2)
FROM students
GROUP BY schoolsup;
```

## Stop services

```bash
stop-yarn.sh
stop-dfs.sh
jps
```

---

# 75. One-Page Project Summary

```text
PROJECT:
Student Performance Analytics Using Hadoop and Hive

DATASET:
UCI Student Performance Dataset

PRIMARY DATA:
student-por.csv

RECORDS:
649

STORAGE:
Hadoop HDFS

QUERY ENGINE:
Apache Hive

QUERY LANGUAGE:
HiveQL

MAIN ANALYTICS:
• Overall performance
• School comparison
• Gender comparison
• Study-time analysis
• Previous-failure analysis
• Absence analysis
• Parental-education analysis
• Internet-access analysis
• School-support analysis
• Family-support analysis
• Grade distribution
• G1/G2/G3 progression
• Academic-risk analysis

OUTPUT:
Hive query results + charts/dashboard

CORE PIPELINE:

Dataset
   ↓
CSV
   ↓
HDFS
   ↓
Hive
   ↓
HiveQL
   ↓
Analytics
   ↓
Visualization
   ↓
Insights
```

---

## Important note for submission

Do not claim that the 649-row dataset itself is "huge Big Data." The
strongest and most honest framing is that this is an **academic
demonstration of a Hadoop/HDFS + Hive Big Data Analytics pipeline**. The
same architecture can scale to much larger datasets. The official UCI
source confirms the dataset's provenance, variables, lack of missing
values, and CC BY 4.0 license.

---

# 76. Streamlit Interactive Dashboard

## 76.1 Why Add Streamlit?

The Hadoop and Hive implementation demonstrates the **Big Data processing pipeline**, but terminal-based Hive results are not the best way to communicate the findings to a professor or evaluator.

Therefore, the project includes a **Streamlit presentation layer**.

The final architecture becomes:

```text
                    UCI DATASET
                        |
                        v
                student-por.csv
                        |
                        v
                 Data Preparation
                        |
                        v
                 +--------------+
                 | Hadoop HDFS  |
                 | Data Storage |
                 +------+-------+
                        |
                        v
                 +--------------+
                 | Apache Hive  |
                 |   HiveQL     |
                 +------+-------+
                        |
                        v
              Analytical Results
                        |
                        v
                 +--------------+
                 |  Streamlit   |
                 |  Dashboard   |
                 +------+-------+
                        |
                        v
              Interactive Insights
```

This separates the project into three clear technical layers:

| Layer        | Technology  | Responsibility           |
| ------------ | ----------- | ------------------------ |
| Storage      | Hadoop HDFS | Store dataset            |
| Analytics    | Apache Hive | Query and aggregate data |
| Presentation | Streamlit   | Display results visually |

---

# 77. Streamlit Dashboard Design

The dashboard should look like a small analytics application rather than a collection of terminal screenshots.

## Dashboard sections

### Header

```text
🎓 Student Performance Analytics
Hadoop HDFS + Apache Hive + Streamlit
```

### KPI Cards

Display:

- Total Students
- Average Final Grade
- Highest Grade
- Average Absences
- Pass Rate

### Interactive Filters

Provide:

- School
- Gender
- Study-time category
- Final-grade range

Changing a filter should update the dashboard.

### Charts

The dashboard contains:

1. Average Final Grade by School
2. Average Grade by Study Time
3. Final Grade Distribution
4. G1 → G2 → G3 Progression
5. Previous Failures vs Average Grade
6. Internet Access vs Average Grade
7. Absence Group vs Average Grade

### Student Tables

Display:

- Students below the project-defined pass threshold
- Top-performing students

---

# 78. Streamlit Project Structure

Add the following files:

```text
student-performance-bda/
├── app.py
├── requirements.txt
├── data/
│   └── student-por.csv
├── hive/
│   ├── 01_create_database.sql
│   ├── 02_create_table.sql
│   ├── 03_load_data.sql
│   ├── 04_basic_analysis.sql
│   ├── 05_performance_analysis.sql
│   ├── 06_factor_analysis.sql
│   └── 07_advanced_analysis.sql
└── output/
    └── query-results/
```

---

# 79. Install Streamlit

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
pip install --upgrade pip
```

Install dependencies:

```bash
pip install streamlit pandas numpy
```

Or create `requirements.txt`:

```text
streamlit>=1.40
pandas>=2.0
numpy>=1.26
```

Then install:

```bash
pip install -r requirements.txt
```

Verify:

```bash
streamlit --version
```

---

# 80. Place the Dataset for Streamlit

Copy the UCI dataset:

```bash
mkdir -p data
cp data/raw/student-por.csv data/student-por.csv
```

The final file should be:

```text
data/student-por.csv
```

The file must remain semicolon-separated.

---

# 81. Create `app.py`

The Streamlit application should:

1. Load `student-por.csv`.
2. Provide sidebar filters.
3. Calculate KPI values.
4. Display performance charts.
5. Display risk students.
6. Display top-performing students.
7. Explain the Hadoop + Hive architecture.

A complete ready-to-run `app.py` is supplied with this project as a separate file.

---

# 82. Run the Dashboard

From the project directory:

```bash
source .venv/bin/activate
```

Then:

```bash
streamlit run app.py
```

Streamlit will normally open the dashboard in your browser.

If it does not open automatically, use the local address printed in the terminal, commonly:

```text
http://localhost:8501
```

---

# 83. What the Professor Should See

The presentation should follow this sequence:

### Screen 1 — Project introduction

```text
Student Performance Analytics
Hadoop + Hive + Streamlit

Analyze student academic performance
using Big Data technologies.
```

### Screen 2 — KPI dashboard

```text
┌────────────┬────────────┬────────────┬────────────┬────────────┐
│ Students   │ Avg Grade  │ Highest    │ Avg Absence│ Pass Rate  │
│    649     │   XX.XX    │    XX      │    XX.X    │   XX.X%    │
└────────────┴────────────┴────────────┴────────────┴────────────┘
```

### Screen 3 — Interactive analysis

Professor can change:

```text
School
Gender
Study Time
Grade Range
```

and the charts update.

### Screen 4 — Performance analysis

Show:

- Study time vs grades
- School vs grades
- Grade distribution

### Screen 5 — Factor analysis

Show:

- Previous failures
- Absences
- Internet access
- School support

### Screen 6 — Student insights

Show:

- Students below G3 = 10
- Top-performing students
- Their academic characteristics

### Screen 7 — Technical architecture

Show:

```text
Dataset
   ↓
HDFS
   ↓
Hive
   ↓
HiveQL
   ↓
Streamlit
```

This makes the connection between the **technical implementation** and the **business/academic result** very clear.

---

# 84. Recommended UI Style

The Streamlit interface should use:

- Clean white/light background
- Dark navy header
- Blue accent elements
- Large KPI cards
- Rounded containers
- Consistent spacing
- Clear chart titles
- Minimal text
- Interactive filters in the sidebar
- Responsive layout
- Tables for detailed records

Avoid adding unnecessary animations or decorative elements. The goal is a professional analytics dashboard.

---

# 85. Streamlit Dashboard Demonstration Script

During the demonstration, say:

> "The Hadoop and Hive layer performs the storage and analytical processing, while Streamlit is used as the presentation layer. Instead of showing only raw Hive terminal results, we have created an interactive dashboard so the analytical findings can be understood visually."

Then demonstrate:

> "These KPI cards summarize the selected student population."

Change the School filter:

> "When I select a particular school, the dashboard recalculates the performance metrics for that subset."

Change Study Time:

> "We can also investigate how different study-time categories are associated with final grades."

Show the risk table:

> "Students with a final grade below 10 are displayed as an academic-risk group. This is a project-defined analytical threshold and is not an official UCI classification."

Finally:

> "The dashboard is therefore the presentation layer on top of our Hadoop and Hive analytics pipeline."

---

# 86. Important Technical Clarification

The Streamlit dashboard does **not replace Hadoop or Hive**.

The project should be presented as:

```text
Hadoop HDFS
    =
Storage Layer

Hive
    =
Analytics / Query Layer

Streamlit
    =
Visualization / Presentation Layer
```

This distinction is important during the viva.

Do not say:

> "Streamlit performs the Big Data processing."

Instead say:

> "Hadoop HDFS provides storage, Hive performs SQL-based analytics, and Streamlit presents the analytical results interactively."

---

# 87. Recommended Final Demonstration

For the strongest demonstration, use this order:

```text
1. Show UCI dataset
        ↓
2. Show Hadoop installation
        ↓
3. Show HDFS
        ↓
4. Upload dataset to HDFS
        ↓
5. Show Hive database
        ↓
6. Show Hive table
        ↓
7. Run HiveQL query
        ↓
8. Show query result
        ↓
9. Open Streamlit dashboard
        ↓
10. Apply filters
        ↓
11. Show charts
        ↓
12. Explain insights
        ↓
13. Explain architecture
```

This gives the evaluator both:

**Technical implementation + visual output.**

---

# 88. Final Technology Stack

The final project stack is:

```text
┌─────────────────────────────────────┐
│       STUDENT PERFORMANCE BDA       │
├─────────────────────────────────────┤
│                                     │
│  Dataset                            │
│  UCI Student Performance            │
│                                     │
│  Storage                            │
│  Hadoop HDFS                        │
│                                     │
│  Analytics                          │
│  Apache Hive + HiveQL               │
│                                     │
│  Visualization                      │
│  Streamlit + Pandas                 │
│                                     │
└─────────────────────────────────────┘
```

---

# 89. Final Project Architecture

```text
                 ┌──────────────────────┐
                 │   UCI DATASET        │
                 │ student-por.csv      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  DATA PREPARATION   │
                 │  Validation/Cleaning│
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     HADOOP HDFS      │
                 │                      │
                 │ Distributed Storage  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    APACHE HIVE       │
                 │                      │
                 │ Database + Tables    │
                 │ HiveQL Queries       │
                 │ Aggregations         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ ANALYTICAL RESULTS   │
                 │                      │
                 │ Grades               │
                 │ Study Time           │
                 │ Absences             │
                 │ Failures             │
                 │ School               │
                 │ Support              │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      STREAMLIT       │
                 │                      │
                 │ KPIs                 │
                 │ Filters              │
                 │ Charts               │
                 │ Tables               │
                 │ Insights             │
                 └──────────────────────┘
```

---

# 90. Final Project Statement

The completed project should be described as:

> **"A Hadoop and Hive-based Student Performance Analytics system with an interactive Streamlit visualization layer."**

This is stronger than calling it only a "Hive project" because it demonstrates the complete flow from **public dataset → distributed storage → SQL-based Big Data analytics → interactive visualization**.
