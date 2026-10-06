from pathlib import Path

def test_documentation_files_exist_and_populated():
    docs = ["docs/project-report.md", "docs/viva-prep-guide.md", "README.md"]
    for d in docs:
        p = Path(d)
        assert p.exists(), f"Missing doc file: {d}"
        assert p.stat().st_size > 500, f"Doc file {d} too short"
