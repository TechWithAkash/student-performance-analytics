import io
import os
import zipfile
import requests
import pandas as pd
from pathlib import Path

UCI_URL = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"

def download_and_extract_data(target_raw_dir="data/raw", target_processed_dir="data/processed"):
    raw_path = Path(target_raw_dir)
    processed_path = Path(target_processed_dir)
    raw_path.mkdir(parents=True, exist_ok=True)
    processed_path.mkdir(parents=True, exist_ok=True)

    dest_csv = raw_path / "student-por.csv"
    if not dest_csv.exists():
        print(f"Fetching dataset from {UCI_URL}...")
        resp = requests.get(UCI_URL, timeout=30)
        resp.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            z.extractall(raw_path)
            
        # The zip typically contains an inner student.zip
        inner_zip = raw_path / "student.zip"
        if inner_zip.exists():
            with zipfile.ZipFile(inner_zip) as iz:
                iz.extractall(raw_path)
                
    if not dest_csv.exists():
        raise FileNotFoundError(f"Failed to find student-por.csv after extraction in {raw_path}")

    df = pd.read_csv(dest_csv, sep=";")
    print(f"Validated student-por.csv: {df.shape[0]} rows, {df.shape[1]} columns.")
    
    clean_csv = processed_path / "student_por_clean.csv"
    df.to_csv(clean_csv, sep=";", index=False)
    print(f"Saved processed dataset to {clean_csv}")
    return df

def validate_dataset(csv_path="data/raw/student-por.csv"):
    path = Path(csv_path)
    if not path.exists():
        return False
    df = pd.read_csv(path, sep=";")
    assert len(df) == 649, f"Expected 649 rows, got {len(df)}"
    assert len(df.columns) == 33, f"Expected 33 columns, got {len(df.columns)}"
    return True

if __name__ == "__main__":
    download_and_extract_data()
    validate_dataset()
