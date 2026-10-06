from pathlib import Path
from scripts.local_query_runner import run_all_queries

def test_local_query_runner_generates_outputs():
    results = run_all_queries("data/raw/student-por.csv", "output/query-results")
    assert "total_students" in results
    assert results["total_students"] == 649
    
    assert Path("output/query-results/04_basic_analysis.csv").exists()
    assert Path("output/query-results/05_gender_analysis.csv").exists()
    assert Path("output/query-results/05_grade_categories.csv").exists()
    assert Path("output/query-results/06_study_time.csv").exists()
    assert Path("output/query-results/07_top_achievers.csv").exists()
    assert Path("output/query-results/all_queries_summary.txt").exists()
