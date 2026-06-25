#!/usr/bin/env python3
"""演習HTMLの整合チェック（reverse-index レビュー「逆引き導線」項目5への対応）。

各 exercises/*.html について次を検証する:
  1. 本文へのリンク partN/NN-stem(.html) が、実在する partN/NN-stem.qmd に対応するか
     （旧章番号・旧ファイル名へのリンク切れを検出）
  2. 問題数（class="problem"）と模範解答数（<details>）の対応
  3. 旧表記の残存（「試作版」「答え：」など編集方針で置換したもの）

使い方:
    python code/check_exercises.py
終了コード 0 = 問題なし、1 = 要修正の指摘あり。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EX_DIR = ROOT / "exercises"

# 本文ファイル名（partN/NN-stem）の実在集合を作る
QMD_STEMS: set[str] = set()
for qmd in ROOT.glob("part*/*.qmd"):
    QMD_STEMS.add(f"{qmd.parent.name}/{qmd.stem}")

LINK_RE = re.compile(r"(part\d)/(\d{2}-[a-z0-9-]+?)(?:\.html|\.qmd|[\"#])")
STALE_STRINGS = ["試作版", "答え："]


def check_file(path: Path) -> list[str]:
    issues: list[str] = []
    text = path.read_text(encoding="utf-8")

    # 1. リンク先の実在チェック
    bad_links: set[str] = set()
    for part, stem in LINK_RE.findall(text):
        ref = f"{part}/{stem}"
        if ref not in QMD_STEMS:
            bad_links.add(ref)
    for ref in sorted(bad_links):
        issues.append(f"リンク切れ/旧章番号: {ref}（対応する .qmd が無い）")

    # 2. 問題数と解答数
    n_prob = len(re.findall(r'class="problem"', text))
    n_details = text.count("<details")
    if n_prob and n_details and n_prob != n_details:
        issues.append(f"問題数({n_prob}) と 模範解答<details>数({n_details}) が不一致")

    # 3. 旧表記の残存
    for s in STALE_STRINGS:
        c = text.count(s)
        if c:
            issues.append(f"旧表記が残存: 「{s}」×{c}")

    return issues


def main() -> int:
    if not EX_DIR.is_dir():
        print(f"exercises ディレクトリが見つかりません: {EX_DIR}")
        return 1

    total_issues = 0
    for path in sorted(EX_DIR.glob("*.html")):
        issues = check_file(path)
        status = "OK" if not issues else f"{len(issues)}件の指摘"
        print(f"[{status}] {path.name}")
        for msg in issues:
            print(f"    - {msg}")
            total_issues += 1

    print()
    if total_issues == 0:
        print("すべての演習HTMLが本文と整合しています。")
        return 0
    print(f"合計 {total_issues} 件の要修正項目があります。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
