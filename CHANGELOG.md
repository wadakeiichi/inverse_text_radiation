# Changelog

本書 *宇宙の熱的放射 ― 連続放射と線スペクトルの背景物理* の改訂履歴。

形式は [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に準拠、
バージョニングはおおよそ [Semantic Versioning](https://semver.org/lang/ja/) に従う。

---

## [Unreleased]

v0.1 のレビュー受付・反映フェーズ。

### Added（追加）
- 中心地図（線）SVG `images/hydrogen-map.svg` ― 第19章で表示
- 第4章 §4.1 比強度の幾何 SVG `specific-intensity.svg`
- 第14章 §14.2 k 空間の格子 SVG `k-space-counting.svg`
- 第19章 §19.3 ／ 第20章 §20.4 吸収線/輝線の幾何 SVG `line-formation-geometry.svg`
- 第20章 §20.1 等価幅の幾何 SVG `equivalent-width.svg`
- 第22章 §22.4 Voigt プロファイル SVG `voigt-profile.svg`
- 第9章 §9.3 紫外破綻 SVG `uv-catastrophe.svg`
- 第7章 §7.2 ／ 第10章 §10.2 量子振動子の凍結 SVG `quantum-freeze-out.svg`
- 中心地図（連続）SVG `planck-map.svg`、Einstein 三過程 SVG `einstein-processes.svg`
- 序章 §0.1 を「宇宙の熱的放射から何を学ぶのか」に刷新
- `requirements.txt`、`docs/figure-roadmap.md`、`docs/release-notes-v0.1.md` 等の運用ドキュメント

### Changed（変更）
- HTML 本文フォントを **IBM Plex Sans JP** に切替（PDF は Noto Sans CJK JP）
- 用語統一：「中赤外 → 中間赤外」（astro-dic 準拠）
- CI を `librsvg2-bin` 追加対応、Python 依存を `requirements.txt` 化

### Fixed（修正）
- §1.6 ・ §2.1 のコードチャンクで Planck 曲線が表示されない問題（末尾 `fig` 追加）
- `\rm` などの旧 TeX フォントコマンドの混入を除去（scrreprt 非互換）
- LaTeX の `tcolorbox skins/breakable` ロード忘れ
- 序章と index の crossref 章カウントを 0 にして、第1章の図番号を `1.1` から始まるよう修正

---

## [v0.1] — 2026-06-11

初版 preprint。

### 公開
- HTML: <https://wadakeiichi.github.io/inverse_text_radiation/>
- PDF preprint: [Zenodo DOI 10.5281/zenodo.20635563](https://doi.org/10.5281/zenodo.20635563)
- ソース: <https://github.com/wadakeiichi/inverse_text_radiation>

### 内容
- 全 8 部 25 章 + 付録 A（数学補章）・B（単位と基本定数）
- 二つの中心地図（プランク関数・水素線吸収係数）を各部冒頭で再掲する逆引き構成
- 三原則：① 逆引き ② 背景物理を曖昧にしない ③ 天下り的に式を与えない
- 序章 + 全章で「この章で答える問い」「到達目標」「使えるようになった道具」を統一フォーマットで実装
- CC BY 4.0 ライセンス

---

*変更点の詳細は [GitHub Releases](https://github.com/wadakeiichi/inverse_text_radiation/releases) を参照。*
