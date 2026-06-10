# 宇宙の熱的スペクトル ― 観測から基礎物理への逆引き

*Thermal Spectra of the Universe: An Inverse Approach to Fundamental Physics*

学部後半〜大学院修士課程向けの宇宙物理教科書プロジェクト。**連続スペクトル（黒体放射）** と **線スペクトル** という熱的放射を入口に、基礎物理（統計力学・量子論・電磁気・原子物理・QED）を逆向きに学び直す。非熱的放射（シンクロトロン等）は限定的に触れる（第18章等）。

## 三つの原則

1. **逆引き** ― 観測スペクトルから基礎物理を逆向きにたどる
2. **背景物理を曖昧にしない** ― 各観測量がどの物理から来ているかを章を横断して明示
3. **天下り的に式を与えない** ― 式を結果ではなく必然として理解させる

## 二つの中心地図

- **連続**：プランク関数 $B_\nu(T) = \dfrac{2h\nu^3}{c^2} \cdot \dfrac{1}{e^{h\nu/kT}-1}$
- **線**：水素線吸収係数 $\alpha_\nu = \dfrac{\pi e^2}{m_e c} f_{lu} n_l \phi(\nu - \nu_0)$
- **統合**：第VIII部の Einstein 関係 $A_{21} = \dfrac{2h\nu^3}{c^2}\dfrac{g_1}{g_2} B_{12}$

## ローカルでのビルド

```bash
# プレビュー（変更を保存するたびに自動再描画）
quarto preview

# 完全レンダリング（HTML + PDF + EPUB）
quarto render

# HTML だけ
quarto render --to html

# 単一ファイルのプレビュー
quarto preview part1/01-where-blackbody.qmd
```

VS Code を使う場合は、Quarto 拡張をインストールして `.qmd` ファイルを開き、右上のプレビューボタンで起動できる。

## 必要な環境

- [Quarto](https://quarto.org/docs/get-started/) ≥ 1.4
- Python 3.10+ と次のパッケージ：
  ```bash
  pip install jupyter matplotlib numpy scipy astropy sympy
  ```
- （PDF を出すなら）TeX Live + 日本語フォント（Noto CJK JP 推奨）

## ディレクトリ構造

```
spectra-of-the-universe/
├── _quarto.yml              # book プロジェクト設定
├── index.qmd                # 表紙＋三原則
├── 00-prologue.qmd          # 序章
├── part1/ … part8/          # 各部の章ファイル（.qmd）
├── appendix/                # 付録 A, B, C
├── _includes/               # 中心地図 include（再利用）
│   ├── _planck-map.qmd
│   ├── _hydrogen-map.qmd
│   └── _einstein-relation.qmd
├── _assets/                 # SCSS テーマ
│   ├── theme.scss           # 共通レイアウト（言語非依存）
│   ├── ja-theme.scss        # 和文タイポ
│   └── en-theme.scss        # 欧文タイポ（英語版用、現時点未使用）
├── _filters/                # Lua filter
│   ├── difficulty-stars.lua # 難易度☆
│   ├── tags.lua             # 節タグ [形] [線]
│   └── boxed-factor.lua     # 数式の因子強調
├── code/                    # Python 計算例
│   ├── planck-curve.py      # プランク曲線と Wien/RJ 極限
│   ├── voigt-profile.py     # Voigt 線形
│   └── rydberg-series.py    # 水素のリュードベリ系列
├── images/                  # 図版
├── references.bib           # BibTeX 参考文献
└── .github/workflows/
    └── publish.yml          # GitHub Pages 自動デプロイ
```

## 設計ルール（Day 1 から守る）

将来の英訳を楽にするため、最初から守るルール：

1. ファイル名は英語（`02-reading-spectra.qmd`）
2. セクション ID は英語（`{#sec-blackbody-where}`）
3. 式ラベルは英語（`@eq-planck-function`）
4. 図版・コード・キャプション ID も英語
5. CSS/SCSS は言語非依存に設計
6. 共通の数式 include ファイルで DRY
7. YAML に `lang: ja` を明示

詳細はメモリ参照（`textbook_design_rules.md`）。

## 公開

GitHub Pages で公開予定。`main` ブランチへの push で自動的に再ビルド・デプロイされる（`.github/workflows/publish.yml`）。

リリース時は Zenodo と連携して DOI を付与する予定。

## バイリンガル戦略

- **日本語版を完成させてから英語版**を作る方針
- 現時点では日本語のみのシングルプロジェクト
- 英語版開始時に `ja/` `en/` サブディレクトリ構造へリファクタリング

## ライセンス

本書は [**Creative Commons Attribution 4.0 International License (CC BY 4.0)**](https://creativecommons.org/licenses/by/4.0/) のもとで公開されています。

つまり、適切なクレジットを示せば、共有・改変・商用利用も自由に行えます。引用例：

> 和田 桂一 (Keiichi Wada), 『宇宙の熱的スペクトル ― 観測から基礎物理への逆引き』 (*Thermal Spectra of the Universe: An Inverse Approach to Fundamental Physics*), 2026. Licensed under CC BY 4.0. Source: <https://github.com/wadakeiichi/inverse_text_radiation>

詳しくは [`LICENSE`](LICENSE) と [`CITATION.cff`](CITATION.cff) を参照してください。

## 引用

GitHub のリリース作成時に Zenodo と連携することで、各バージョンに DOI が付与されます。引用用のメタデータは [`CITATION.cff`](CITATION.cff) に集約しています。GitHub の「Cite this repository」ボタンからも BibTeX が取得できます。

## リポジトリ

- ソース：<https://github.com/wadakeiichi/inverse_text_radiation>
- 公開ページ：（GitHub Pages 公開後にここに URL を記載）

## 著者

和田 桂一 (Keiichi Wada) — <wada@astrophysics.jp>
