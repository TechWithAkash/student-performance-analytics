from pathlib import Path

def test_all_seven_scripts_exist():
    scripts = [
        "01_create_database.sql",
        "02_create_table.sql",
        "03_load_data.sql",
        "04_basic_analysis.sql",
        "05_performance_analysis.sql",
        "06_factor_analysis.sql",
        "07_advanced_analysis.sql",
    ]
    for s in scripts:
        p = Path("hive") / s
        assert p.exists(), f"Missing HiveQL script {s}"
        assert p.stat().st_size > 0, f"Script {s} is empty"

def test_script_contents_contain_key_keywords():
    with open("hive/01_create_database.sql") as f:
        content = f.read().upper()
        assert "CREATE DATABASE" in content
        
    with open("hive/02_create_table.sql") as f:
        content = f.read().upper()
        assert "CREATE EXTERNAL TABLE" in content or "CREATE TABLE" in content
        assert "TERMINATED BY ';'" in content
        
    with open("hive/04_basic_analysis.sql") as f:
        content = f.read().upper()
        assert "COUNT(*)" in content
        assert "AVG(G3)" in content
