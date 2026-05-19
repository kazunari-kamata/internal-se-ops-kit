# AGENTS.md

このリポジトリは、公開可能な社内SE向け運用テンプレート集です。実在する社内情報や機密情報を含めず、すべてサンプルデータとして扱います。

## 方針

- Python は 3.12 を前提にする
- スクリプトは標準ライブラリ中心で実装する
- テストは pytest で実行する
- ドキュメントとテンプレートは日本語で、実務に近い自然な文体にする
- コマンド例はリポジトリルートからコピーして動く形にする

## 公開リポジトリ向けの禁止事項

- 実在する会社名、顧客名、個人名を含めない
- メールアドレス、IPアドレス、ドメインを含めない
- 社内パス、ローカル環境固有の絶対パスを含めない
- private repository や社内サービスを参照しない
- 架空の導入実績や誇張表現を書かない

## 検証

変更後は可能な限り次を実行します。

```sh
python -m pytest
python scripts/validate_inventory.py examples/sample-assets.csv
python scripts/generate_checklist.py onboarding
python scripts/generate_checklist.py offboarding
```
