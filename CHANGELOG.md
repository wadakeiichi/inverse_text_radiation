# Changelog

本書 *宇宙の熱的放射 ― 連続放射と線スペクトルの背景物理* の改訂履歴。

形式は [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に準拠、
バージョニングはおおよそ [Semantic Versioning](https://semver.org/lang/ja/) に従う。

---

## [Unreleased]

---

## [v0.3] — 2026-06-28

図版（幾何・概念図）フェーズに加え、中田好一氏の講義ノート『天体物理学 I』に着想を得た最優先トピックの本文反映、演習解答 UI の刷新、全体再検証（逆引き・演習切り分け・相互参照）を含む版。

### Added（追加）
- **エディントン近似と恒星大気の温度構造**：第5章 §5.10–§5.11 を新設。平面平行大気のモーメント方程式（$J,H,K$）→ エディントン近似 $K=J/3$ → ロスランド平均 → 温度構造 $T(\tau)^4=\tfrac34 T_\mathrm{e}^4(\tau+\tfrac23)$（$T(\tau=2/3)=T_\mathrm{e}$、表面 $T_0\simeq0.84\,T_\mathrm{e}$）。さらに「見える深さ」による統一公式 $F_\lambda=\pi B_\lambda[T(\tau_\lambda=2/3)]$, $T=T_\mathrm{e}[\tfrac12(1+k_R/k_\lambda)]^{1/4}$ を導入し、連続スペクトルの形と吸収線を一つの式で説明。図 `images/eddington-atmosphere.svg` を追加
- 第5章 §5.2 に被覆率（紙片モデル）から透過率 $e^{-\tau}$ を導く導出ノート
- 第5章 §5.10 に「なぜモーメントを取るのか（利点と代償）」の問いノートと、クロージャーは一つでない旨の注記（可変エディントン因子・流束制限拡散 FLD・M1 クロージャー）
- 第6章 §6.7「質量作用の法則」を新設し、励起（Boltzmann）・電離（Saha）・解離を一つの平衡 $\sum_i a_i\mu_i=0$ から導く統一フレームを提示
- 第17章 §17.7「温室効果」（惑星をエディントン大気として、CO₂ 倍化のバンド縁機構）、§17.8「分子の解離平衡」（CO・H₂O・TiO、炭素星 vs 酸素星）を新設
- 第23章 §23.1 に古典振動子（強制減衰）から吸収断面積・振動子強度 $f$・等価幅へ至る導出ノート
- 第15・21章に統一公式（§5.11）を参照するコールアウト（連続のずれ・吸収線を同じ $k_\lambda$ 構造で説明）
- **謝辞ページ**（`acknowledgments.qmd`）を序章直後に追加（レビュアー・中田ノートへの着想・AI 補助の明記）
- 図版：放射輸送の形式解・占有数分布・双極子放射(Larmor)・成長曲線・プランク曲線の読み取り（5点）、水素エネルギー準位図、エディントン大気図

### Changed（変更）
- **演習解答の UI を刷新**：各問直後の折りたたみ「模範解答」を廃止し、名称を「解答例」に統一。章末の「解答例」節に集約し、HTML 版は右サイドパネル（Bootstrap offcanvas、背景非暗転）で問題文と並べて表示。各問直後と章末にボタン。PDF/EPUB は順次掲載にフォールバック（全 26 章・105 問）
- 第26章 §26.5 に選択則の物理（パリティ・角運動量）を加筆

### Fixed（修正）
- 相互参照を整合化：重複していた数式ラベルを解消（付録 A の平均強度 → `eq-mean-intensity-mu`、エネルギー密度 → `eq-energy-density-T4-explicit`、いずれも本文定義を参照）。第23章の §番号誤記（§22.6 → §23.6）を修正
- 第18章 §18.3：コンプトン1回散乱の利得係数「4」の動機づけ（二次ドップラー押し上げの Maxwell 平均）を追記
- 第20章 §20.3：禁制線の見え方を決める臨界密度 $n_\mathrm{crit}=A_{ul}/q_{ul}$ への前方参照（§21.5）を追加
- 図 17.1（k 空間）の凡例の重なりを解消、図のフォントを底上げ

### Verified（検証）
- 逆引き原則（天下り回避）・演習⇔本文の切り分け・相互参照整合性を全章でレビュー。重要な天下りは無く、相互参照は未定義参照・重複 ID ともゼロ

---

## [v0.2] — 2026-06-26

v0.1 のレビュー受付・反映フェーズの成果をまとめた版。2件のレビュー（日本語表現・逆引き／物理内容）に基づく全面改訂と、v0.2 図版バッチの完了を含む。

### Added（追加・本改訂）
- §16.1 に **FIRAS スペクトル図**（COBE/FIRAS モノポール × 2.725 K 黒体）を追加 `images/firas-spectrum.svg`（`code/firas_fit.py`）。これにより **v0.2 図版バッチ 8/8 完了（100%）**。データは Fixsen et al. 1996（パブリックドメイン、NASA/COBE）
- 第14章 §14.5 に中心地図因子の「初出／仮に借りる場所／本当に導出する場所」一覧表を新設（第9章で予告した借用→返済の往復構造を回収）
- 線スペクトル中心地図 `_includes/_hydrogen-map.qmd` に適用範囲注記（前因子 $\pi e^2/m_e c$・$f_{lu}$ は E1 許容線用、21 cm／禁制線は $A_{ul}$ から $B_{lu}$ に読み替え）
- 応用章（第15・17・18・24章）冒頭に「観測特徴→最小モデル→逆引き物理量→破れる仮定」の4列表、第2章に観測三特徴→プランク三因子の対応表
- 付録 B に「SI ⇔ Gauss 式形対応表」、第26章に双極子近似とゲージの説明
- 演習 HTML の章番号・リンク・問題数を検査する `code/check_exercises.py`
- 第VI部演習に第19章5問と 17-5 を収録（全21問）
- 改訂報告 `revision-notes.html`（採用／非採用の判断記録）

### Changed（用語・表現の統一）
- 用語統一：**線形 → 線輪郭（line profile）**、**源泉関数 → ソース関数**、$j_\nu$＝放出係数／$\varepsilon_\nu$＝体積放射率（$\varepsilon_\nu=4\pi j_\nu$）、emergent flux→射出フラックス、greybody→修正黒体、curve of growth→成長曲線、Local TE→局所熱力学平衡（LTE）ほか。コールアウト見出し「対応（観測）→観測との対応」
- 口語・比喩表現を物理的記述に置換（ちょっかい／本丸／白眉／絶頂例 等）
- 演習 HTML：第VII部を第20〜24章、第VIII部を第25〜26章に同期し全リンク更新。「試作版」表記・解答見出しを整理（全105問に整合）
- 句読点・数値範囲（〜）・太字の整理

### Fixed（物理・誤記）
- 振動子強度の式を次元整合（位置形 $|\langle u|r|l\rangle|^2$ と双極子形 $|\langle u|d|l\rangle|^2$ を分離、SI/CGS 明記）
- 自然幅を上準位から全下準位への全崩壊率の和で定義（分岐比に言及）、誘導放出の扱いを「負の吸収」流儀に統一
- 第19章 Kirchhoff 式の $4\pi$ 因子整合、放射輸送方程式の幾何・統計平衡式の明確化、立体角表の重複ヘッダ削除、誤字「線形ぴーく」→「線輪郭のピーク」

### Added（v0.1.x で先行投入：図版・第19章）
- **第19章「自由電子が作る連続光 ― 自由-自由・束縛-自由・再結合」を新設**（第VI部末尾）。連続放射の素過程（制動放射・光電離・再結合）を放出/吸収の両面で扱い、Kirchhoff・Milne 関係・Saha 平衡で結ぶ。H⁻ 連続不透明度、観測逆引き、再結合線への橋渡し節を含む。設計メモ `docs/continuum-microprocesses-chapter-plan.md`
- 第19章 §19.1 連続を作る三素過程の準位図 SVG `images/continuum-processes.svg`（`einstein-processes.svg` の姉妹図）
- 第19章 §19.2 自由-自由放射のスペクトル（電波の黒体漸近〜X線の指数カットオフ）SVG `images/continuum-ff-spectrum.svg`
- 第19章 §19.3–19.4 連続吸収端と再結合連続光（Lyman/Balmer/Paschen のしきい値、吸収端 vs 放出端）SVG `images/continuum-edges-recomb.svg`
- 中心地図（線）SVG `images/hydrogen-map.svg` ― 第20章で表示
- 第4章 §4.1 比強度の幾何 SVG `specific-intensity.svg`
- 第14章 §14.2 k 空間の格子 SVG `k-space-counting.svg`
- 第20章 §20.3 ／ 第21章 §21.4 吸収線/輝線の幾何 SVG `line-formation-geometry.svg`
- 第21章 §21.1 等価幅の幾何 SVG `equivalent-width.svg`
- 第23章 §23.4 Voigt プロファイル SVG `voigt-profile.svg`
- 第9章 §9.3 紫外破綻 SVG `uv-catastrophe.svg`
- 第7章 §7.2 ／ 第10章 §10.2 量子振動子の凍結 SVG `quantum-freeze-out.svg`
- 中心地図（連続）SVG `planck-map.svg`、Einstein 三過程 SVG `einstein-processes.svg`
- 序章 §0.1 を「宇宙の熱的放射から何を学ぶのか」に刷新
- `requirements.txt`、`docs/figure-roadmap.md`、`docs/release-notes-v0.1.md` 等の運用ドキュメント

### Changed（変更）
- **第19章の新設に伴い第VII・VIII部を1章ずつ繰り下げ**（旧19–25章 → 20–26章、全 8 部 26 章）。`#sec-`/`#eq-` ID は維持、旧ファイル名 `part7/19–23`・`part8/24–25` は `20–24`・`25–26` にリネーム（要：旧URLのリダイレクト設定）
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
