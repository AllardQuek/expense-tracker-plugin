from __future__ import annotations

from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, Any
import csv

CSV_HEADER = ["name", "tags", "cost", "currency", "cost_sgd", "city"]
REQUIRED_FIELDS = ["name", "cost"]
OPTIONAL_FIELDS = ["tags", "currency", "cost_sgd", "city"]


def normalize_decimal_string(value: Any) -> str:
    if value is None:
        raise ValueError("Numeric value cannot be None")

    text = str(value).strip()
    if not text:
        raise ValueError("Numeric value cannot be blank")

    try:
        dec = Decimal(text)
    except InvalidOperation:
        raise ValueError(f"Invalid numeric value: {value}")

    normalized = format(dec.normalize(), "f")

    if normalized == "-0":
        normalized = "0"

    return normalized


def normalize_expense_row(row: Dict[str, Any]) -> Dict[str, str]:
    if not isinstance(row, dict):
        raise ValueError("Row must be a dict")

    name = str(row.get("name", "")).strip()
    if not name:
        raise ValueError("Field 'name' is required")

    cost = normalize_decimal_string(row.get("cost"))

    tags = str(row.get("tags", "") or "").strip()
    currency = str(row.get("currency", "") or "").strip().upper()
    city = str(row.get("city", "") or "").strip()

    cost_sgd_raw = row.get("cost_sgd", "")
    cost_sgd = ""
    if cost_sgd_raw not in (None, ""):
        cost_sgd = normalize_decimal_string(cost_sgd_raw)

    return {
        "name": name,
        "tags": tags,
        "cost": cost,
        "currency": currency,
        "cost_sgd": cost_sgd,
        "city": city,
    }


def ensure_csv_exists(csv_path: str | Path) -> Path:
    path = Path(csv_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists() or path.stat().st_size == 0:
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)

    return path


def csv_has_expected_header(csv_path: str | Path) -> bool:
    path = Path(csv_path)
    if not path.exists() or path.stat().st_size == 0:
        return False

    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        first_row = next(reader, None)

    return first_row == CSV_HEADER


def append_expense_row(csv_path: str | Path, row: Dict[str, Any]) -> Path:
    path = ensure_csv_exists(csv_path)
    normalized = normalize_expense_row(row)

    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([normalized[column] for column in CSV_HEADER])

    return path

