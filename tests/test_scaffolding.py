import os
from pathlib import Path

def test_directory_structure_exists():
    required_dirs = [
        "data/raw",
        "data/processed",
        "docker",
        "hive",
        "output/query-results",
        "scripts",
        "docs",
        "tests",
    ]
    for d in required_dirs:
        assert Path(d).is_dir(), f"Missing directory: {d}"
