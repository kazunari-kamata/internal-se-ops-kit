from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


validate_inventory = load_module(ROOT / "scripts" / "validate_inventory.py", "validate_inventory")
generate_checklist = load_module(ROOT / "scripts" / "generate_checklist.py", "generate_checklist")


def test_sample_assets_are_valid():
    rows, errors = validate_inventory.validate_inventory(ROOT / "examples" / "sample-assets.csv")

    assert len(rows) == 5
    assert errors == []


def test_invalid_asset_status_is_reported(tmp_path: Path):
    csv_path = tmp_path / "assets.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=validate_inventory.REQUIRED_FIELDS)
        writer.writeheader()
        writer.writerow(
            {
                "asset_id": "AST-9999",
                "asset_type": "laptop",
                "owner_id": "user-999",
                "status": "unknown",
                "purchase_date": "2025-01-01",
                "next_review_date": "2026-01-01",
            }
        )

    _, errors = validate_inventory.validate_inventory(csv_path)

    assert any("status must be one of" in error for error in errors)


def test_generate_onboarding_checklist():
    output = generate_checklist.render_checklist("onboarding")

    assert "# 入社対応チェックリスト" in output
    assert "- [ ] 標準アカウントを作成した" in output
    assert "## 初回利用確認" in output
    assert "- [ ] 初回サインインが完了した" in output
    assert "- 対応担当:" in output


def test_generate_offboarding_checklist():
    output = generate_checklist.render_checklist("offboarding")

    assert "# 退社対応チェックリスト" in output
    assert "- [ ] 標準アカウントを停止した" in output
