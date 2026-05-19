#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import date

CHECKLISTS = {
    "onboarding": {
        "title": "入社対応チェックリスト",
        "sections": {
            "事前確認": [
                "申請内容に不足がない",
                "必要な業務ロールが明記されている",
                "利用開始日が確認済み",
                "端末の要否が確認済み",
                "承認者と依頼元が確認済み",
                "既存アカウントや重複申請がないことを確認した",
            ],
            "アカウント": [
                "標準アカウントを作成した",
                "初期認証手順を案内した",
                "多要素認証の設定手順を案内した",
                "必要なグループに追加した",
                "不要な権限が付与されていないことを確認した",
                "一時的な権限がある場合、棚卸し予定日を記録した",
            ],
            "デバイス": [
                "資産IDを台帳に登録した",
                "端末管理の対象に登録した",
                "暗号化と画面ロックを確認した",
                "更新状態を確認した",
                "貸与品を記録した",
                "標準アプリケーションの導入状態を確認した",
            ],
            "初回利用確認": [
                "初回サインインが完了した",
                "多要素認証が利用できることを確認した",
                "業務に必要な基本アプリケーションへアクセスできることを確認した",
                "利用者向けの問い合わせ窓口を案内した",
            ],
            "完了確認": [
                "利用開始できることを確認した",
                "作業記録を保存した",
                "依頼元に完了を連絡した",
                "未完了項目がある場合、対応予定日を記録した",
            ],
        },
    },
    "offboarding": {
        "title": "退社対応チェックリスト",
        "sections": {
            "事前確認": [
                "利用終了日が確認済み",
                "停止対象システムが確認済み",
                "引き継ぎ要否が確認済み",
                "貸与品の有無が確認済み",
            ],
            "アカウント": [
                "標準アカウントを停止した",
                "業務システムの権限を削除した",
                "管理者権限を削除した",
                "停止結果を確認した",
            ],
            "デバイス": [
                "端末を回収した",
                "貸与品を回収した",
                "保存データの扱いを確認した",
                "台帳の状態を更新した",
            ],
            "完了確認": [
                "依頼元に完了を連絡した",
                "作業記録を保存した",
                "未完了項目がある場合、対応予定日を記録した",
            ],
        },
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an operations checklist.")
    parser.add_argument("kind", choices=sorted(CHECKLISTS), help="Checklist type to generate.")
    return parser.parse_args()


def render_checklist(kind: str) -> str:
    checklist = CHECKLISTS[kind]
    lines = [
        f"# {checklist['title']}",
        "",
        "## 基本情報",
        "",
        f"- 作成日: {date.today().isoformat()}",
        "- 利用者ID:",
        "- 依頼ID:",
        "- 承認者区分:",
        "- 対応担当:",
        "",
    ]

    for section, items in checklist["sections"].items():
        lines.extend([f"## {section}", ""])
        lines.extend(f"- [ ] {item}" for item in items)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    sys.stdout.write(render_checklist(args.kind))
    return 0


if __name__ == "__main__":
    sys.exit(main())
