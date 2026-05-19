#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path

REQUIRED_FIELDS = [
    "asset_id",
    "asset_type",
    "owner_id",
    "status",
    "purchase_date",
    "next_review_date",
]
ALLOWED_STATUSES = {"in_use", "spare", "repair", "retired"}
ASSET_ID_PATTERN = re.compile(r"^AST-\d{4}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an asset inventory CSV file.")
    parser.add_argument("csv_path", type=Path, help="Path to the asset inventory CSV file.")
    return parser.parse_args()


def parse_iso_date(value: str, field_name: str, row_number: int, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"row {row_number}: {field_name} must be YYYY-MM-DD")
        return None


def validate_rows(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    seen_asset_ids: set[str] = set()

    for index, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if not row.get(field, "").strip():
                errors.append(f"row {index}: {field} is required")

        asset_id = row.get("asset_id", "").strip()
        if asset_id:
            if not ASSET_ID_PATTERN.match(asset_id):
                errors.append(f"row {index}: asset_id must match AST-0000 format")
            if asset_id in seen_asset_ids:
                errors.append(f"row {index}: asset_id is duplicated: {asset_id}")
            seen_asset_ids.add(asset_id)

        status = row.get("status", "").strip()
        if status and status not in ALLOWED_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_STATUSES))
            errors.append(f"row {index}: status must be one of: {allowed}")

        purchase_date = parse_iso_date(row.get("purchase_date", "").strip(), "purchase_date", index, errors)
        next_review_date = parse_iso_date(
            row.get("next_review_date", "").strip(),
            "next_review_date",
            index,
            errors,
        )
        if purchase_date and next_review_date and next_review_date < purchase_date:
            errors.append(f"row {index}: next_review_date must not be earlier than purchase_date")

    return errors


def validate_inventory(csv_path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not csv_path.exists():
        return [], [f"file not found: {csv_path}"]

    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames or []
        missing = [field for field in REQUIRED_FIELDS if field not in headers]
        if missing:
            return [], [f"missing required columns: {', '.join(missing)}"]
        rows = list(reader)

    if not rows:
        return rows, ["inventory has no rows"]

    return rows, validate_rows(rows)


def main() -> int:
    args = parse_args()
    rows, errors = validate_inventory(args.csv_path)

    if errors:
        print("Inventory validation failed.")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Inventory validation passed.")
    print(f"Checked assets: {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
