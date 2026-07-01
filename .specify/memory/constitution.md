# 『宇宙の熱的放射』プロジェクト Constitution

*Thermal Radiation in the Universe: An Inverse Approach to the Physics*
学部後半（B2〜B4）〜修士（M1）向け宇宙物理オンライン教科書（Quarto book, 日本語）。

## Core Principles

### I. 逆引き（NON-NEGOTIABLE）
すべての章は観測スペクトルから出発し、背後の物理（放射輸送・統計力学・量子論・電磁気・原子物理・QED）を逆向きにたどる。新章・改訂は「観測 → 物理」の流れを壊してはならない。順方向（理論 → 応用）の提示に書き換える変更は原則却下。

### II. 背景物理を曖昧にしない
各観測量がどの物理から・どの前提のもとで来ているかを章横断で明示する。二つの中心地図（プランク関数 $B_\nu(T)$ と水素線吸収係数 $\alpha_\nu$）は `_includes/` の共通ファイルで再掲し、章ごとに強調因子を切り替える。中心地図に関わる変更は必ず include ファイル側で行い、全章への影響を確認する。

### III. 天下り的に式を与えない
式は結果ではなく必然として導く。新しい式を導入する改訂では、導出または逆向きの動機づけを本文に含めること。導出を省く場合は付録参照か「なぜ成り立つか」の物理的説明を必須とする。

### IV. 英訳を見据えた言語非依存設計
ファイル名・セクション ID（`{#sec-...}`）・式ラベル（`@eq-...`）・図版/コード ID はすべて英語。本文は `lang: ja`。SCSS は言語非依存（`theme.scss`）＋言語別タイポ（`ja-theme.scss`）の分離を維持する。

### V. 再現可能なビルドと図版
図版・計算例は `code/` の Python スクリプトから再現可能にする（数値計算に基づく曲線を手描きで近似しない）。`quarto render`（HTML + PDF + EPUB）が通らない変更は main にマージしない。

## 改訂・出版ワークフロー

- バージョニングはおおよそ SemVer：誤植・軽微修正 = パッチ（v0.31 → v0.32）、章・節の追加 = マイナー、全体構成の変更・正式版 = メジャー（v1.0）。
- すべての内容変更は `CHANGELOG.md`（Keep a Changelog 形式、日本語）に Added / Changed / Fixed で記録する。未リリース分は `[Unreleased]` に貯める。
- リリース時：`CHANGELOG.md` 確定 → `version-history.qmd` と `CITATION.cff` 更新 → main へ push（GitHub Pages 自動デプロイ）→ 節目の版は PDF を Zenodo に登録し DOI を付与。
- レビュー対応（`REVIEW.md`, `review2*` 等）は指摘ごとに spec 化し、どの章のどの記述で対応したかを CHANGELOG に対応づける。

## 品質ゲート

改訂を完了とみなす条件：(1) `quarto render` が HTML/PDF/EPUB で警告なく完了、(2) 相互参照（`@sec-`, `@eq-`, `@fig-`）が全て解決、(3) 新規の式・数値は導出または出典を持つ、(4) 難易度☆・節タグ（Lua filter）の付与規則に従う、(5) CHANGELOG 記載済み。物理的正しさに関わる変更は可能ならレビュアーの確認を得る。

## Governance

本 constitution は spec-kit ワークフロー（specify → plan → tasks → implement）の全成果物に優先する。原則 I〜III は本書のアイデンティティであり改訂不可。IV〜V およびワークフローの変更は CHANGELOG に理由を記録して改訂できる。

**Version**: 1.0.0 | **Ratified**: 2026-07-02 | **Last Amended**: 2026-07-02
