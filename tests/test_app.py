import pytest
import pandas as pd
from app import load_data, calculate_kpis

def test_load_data():
    df = load_data("data/raw/student-por.csv")
    assert df is not None
    assert len(df) == 649
    assert "G3" in df.columns

def test_calculate_kpis():
    df = load_data("data/raw/student-por.csv")
    kpis = calculate_kpis(df)
    assert kpis["total_students"] == 649
    assert 0 <= kpis["pass_rate"] <= 100
    assert 0 <= kpis["avg_g3"] <= 20
    assert kpis["max_g3"] == 19 or kpis["max_g3"] == 20
