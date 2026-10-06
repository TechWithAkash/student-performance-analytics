import os
import pandas as pd
from pathlib import Path
from scripts.download_data import validate_dataset

def test_validate_dataset_schema():
    csv_path = Path("data/raw/student-por.csv")
    assert csv_path.exists(), "student-por.csv does not exist"
    
    df = pd.read_csv(csv_path, sep=";")
    assert len(df) == 649, f"Expected 649 rows, got {len(df)}"
    assert len(df.columns) == 33, f"Expected 33 columns, got {len(df.columns)}"
    assert "G1" in df.columns and "G2" in df.columns and "G3" in df.columns
    assert df["G3"].min() >= 0 and df["G3"].max() <= 20
    assert not df.isnull().values.any(), "Dataset contains unexpected NULL values"
