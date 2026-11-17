# Filesystem and Serialization Utilities Module.
import json
import csv
from pathlib import Path
from typing import Any, Dict, List, Union

# Ensure directory exists, creating parents if necessary.
def ensure_dir(path: Union[str, Path]) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

# Serialize and write data to a UTF-8 JSON file.
def save_json(data: Any, file_path: Union[str, Path], indent: int = 2) -> None:
    p = Path(file_path)
    ensure_dir(p.parent)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

# Load JSON data from file path, returning None if file does not exist.
def load_json(file_path: Union[str, Path]) -> Any:
    p = Path(file_path)
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

# Write text content to file with UTF-8 encoding.
def save_text(text: str, file_path: Union[str, Path]) -> None:
    p = Path(file_path)
    ensure_dir(p.parent)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)

# Read text content from file, returning empty string if missing.
def load_text(file_path: Union[str, Path]) -> str:
    p = Path(file_path)
    if not p.exists():
        return ""
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

# Write list of record dictionaries to an RFC 4180 compliant CSV file.
def save_csv(records: List[Dict[str, Any]], file_path: Union[str, Path], fieldnames: List[str] = None) -> None:
    p = Path(file_path)
    ensure_dir(p.parent)
    if not records and not fieldnames:
        with open(p, "w", newline="", encoding="utf-8") as f:
            pass
        return

    if not fieldnames and records:
        fieldnames = list(records[0].keys())

    with open(p, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        if records:
            writer.writerows(records)

# Load list of record dictionaries from an RFC 4180 compliant CSV file.
def load_csv(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    p = Path(file_path)
    if not p.exists():
        return []
    with open(p, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

