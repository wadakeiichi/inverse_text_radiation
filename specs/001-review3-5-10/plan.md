# 実装計画: review3 重大＋中（物理系）指摘の v0.32 パッチ対応

**Branch**: `001-review3-5-10` | **Date**: 2026-07-02 | **Spec**: `specs/001-review3-5-10/spec.md`

**Input**: `specs/001-review3-5-10/spec.md`

## Summary

review3 の重大6件（R1–R6）と中の物理系4件（M1–M5、計10 ID）を v0.32 パッチとして修正する。実装は難易度で2系統に分岐する:

- **系統(a) 機械的修正**（別エージェント）: R3・R4・R5・R6・M1・M2・M5。文言差し替え・章/節番号修正・係数修正・図座標修正・図再生成。物理の新規書き下ろしを伴わない。
- **系統(b) 物理書き直し**（上位モデル）: R1・R2・M3・M4。式の導出・数値例の再設計・章間整合の再構成を伴う。

全項目とも、修正後に検算（Python）・`quarto render`・CHANGELOG 記載の3種検証を通す。

## Technical Context

**Language/Version**: Quarto book（`.qmd`）、本文 `lang: ja`、数式 LaTeX、図版 SVG（一部 matplotlib 生成）、検算/図生成 Python 3.11（`scipy.constants` / CODATA）。

**Primary Dependencies**: Quarto CLI（HTML/PDF/EPUB）、Python（numpy, scipy, matplotlib）、`_filters/`（Lua）、`_includes/`（共通地図）。

**Storage**: N/A（静的サイト、`_book/` 出力）。

**Testing**: `python3` 検算スクリプト（`code/` 既存＋アドホック）、`quarto render` によるビルド検証、`grep` による相互参照・文字列チェック。既存 `code/check_exercises.py` は演習数値の回帰確認に利用可。

**Target Platform**: GitHub Pages（HTML）＋ PDF/EPUB ダウンロード。

**Project Type**: 単一プロジェクト（Quarto book）。

**Constraints**: `quarto render` が HTML/PDF/EPUB で警告なく完了すること（品質ゲート）。相互参照・式ラベルは英語 ID を維持（原則 IV）。図は Python から再現（原則 V）。

**Scale/Scope**: qmd 8ファイル・svg 1・Python 1・演習HTML 1・CHANGELOG。編集箇所は各ファイル局所（数行〜1小節）。

## Constitution Check

*GATE: Phase 0 前に通過必須。設計後に再チェック。*

| 原則 | 本パッチでの遵守方法 | 判定 |
|---|---|---|
| I. 逆引き（改訂不可） | 観測→物理の流れを壊さない。R4 は逆引き地図の誤誘導を正す修正で原則 I を強化。順方向化なし。 | PASS |
| II. 背景物理を曖昧にしない（改訂不可） | R1・R2・M3・M4 で「どの前提から来るか」を明示（Kirchhoff の素過程、エディントン導出、Wien カットオフ、$\rho(E_f)$）。中心地図 include には触れない（触れる場合のみ include 側で行う）。 | PASS |
| III. 天下り式の禁止（改訂不可） | R2 は地表収支からの導出、M3 は積分の物理的根拠、M4c は分母3の由来を本文に補う。 | PASS |
| IV. 言語非依存設計 | @eq-/@sec-/@fig- ラベルは英語維持。R4 は本文中の節番号（表示テキスト）のみ修正しラベルは変えない。 | PASS |
| V. 再現可能なビルドと図版 | M5 は `code/firas_fit.py` から svg/png を再生成（手描き近似しない）。R5 は手書き svg の幾何修正のみ。 | PASS |
| 改訂ワークフロー | v0.32=パッチ。CHANGELOG `[Unreleased]` に Changed/Fixed で記載し指摘 ID を対応づける。 | PASS |
| 品質ゲート | render 通過・相互参照解決・式の導出/出典・CHANGELOG 記載を全項目で確認。 | 実装時に検証 |

**違反なし**。Complexity Tracking は不要。

## Project Structure

### Documentation (this feature)

```text
specs/001-review3-5-10/
├── spec.md              # 仕様（作成済み）
├── plan.md              # 本ファイル
└── tasks.md             # タスク分解（新旧対応表を含む）
```

### Source Code (repository root)

本パッチが編集対象とする実ファイル（実装フェーズで変更、本仕様化フェーズでは変更しない）:

```text
part2/05-radiative-transfer.qmd          # M1（390, 431行）
part3/06-thermal-equilibrium.qmd         # R6（278行）
part6/16-cmb.qmd                         # M2（66, 122-128, 130行）
part6/17-stars-planets-dust.qmd          # R2（240-244行）, R6（264-266行）
part6/18-accretion-high-energy.qmd       # M3（124-130, 345-357行）
part6/19-continuum-microprocesses.qmd    # R1（85-89, 91行, 87行の§17.6参照）
part7/20-where-lines.qmd                 # R4（12, 24, 25行）
part7/21-line-formation.qmd              # R3（192行）, R4（297行）
part7/22-atomic-physics.qmd              # R4（172, 318, 366行）
part7/24-line-applications.qmd           # R4（197-206行 §24.7表）
part8/25-em-field-quantization.qmd       # M4（135行）
part8/26-qed-minimum.qmd                 # M4（100, 106, 124-125, 415行）
exercises/演習問題_第VIII部_QEDからの俯瞰.html  # M4（26-2 プリレンダ版、297行）
images/k-space-counting.svg              # R5（36, 39行 弧のsweep）
code/firas_fit.py                        # M5（99行 注釈文字列）→ images/firas-spectrum.svg / .png 再生成
CHANGELOG.md                             # [Unreleased] に全ID記載
```

**Structure Decision**: 単一 Quarto プロジェクト。実装は上記の既存ファイルへの局所編集のみで、新規ファイル・ディレクトリの追加はしない（`specs/001-review3-5-10/` の3ドキュメントを除く）。

## 実装系統の割り当てと編集順

### 系統(a) 機械的修正（別エージェント）

編集順（依存の少ない順・ファイル衝突を避ける順）:

1. **R3**（21章192行）: 内部コメント一文を読者向け表現へ。最小・独立。
2. **R6**（06章278行・17章265行）: 並進因子 $2\pi\to\pi$（$(\pi m_{\rm H}k_BT/h^2)^{3/2}$）。2ファイル、係数のみ。17章は R2 と同一ファイルのため、R2（系統(b)）との編集競合に注意（別小節なので行は独立）。
3. **M1**（05章390・431行）: $J=S$/$S=B$ の根拠分離。
4. **M2**（16章66・122-128・130行）: 境界 $z\approx5\times10^4$ 統一＋$\mu$/$y$ 書き分け。
5. **R4**（20章12・24・25行、21章297行、22章172・318・366行、24章197-206行）: 節番号・章番号を tasks.md の新旧対応表どおりに一括修正。21章は R3 と同一ファイル（行独立）。
6. **R5**（`k-space-counting.svg` 36・39行）: sweep フラグ `1`→`0`（3本の弧、line 33 の複合 path も含む）。手書き svg 直接編集。
7. **M5**（`code/firas_fit.py` 99行）: 注釈文字列 `5.45`→`5.35`。→ スクリプト実行で `firas-spectrum.svg`/`.png` を再生成。

### 系統(b) 物理書き直し（上位モデル）

編集順（章順・独立ファイル）:

1. **R1**（19章85-89・91行、87行§17.6参照）: $\alpha_\nu^{\rm ff}$ を $T_e^{-1/2}\nu^{-3}(1-e^{-h\nu/k_BT_e})$ に。@eq-ff-emissivity との比が $B_\nu$ を再現するよう本文の論理（91-97行）を整える。RJ 極限→17章形の接続を明記。
2. **R2**（17章240-244行、249・251行）: @eq-greenhouse-surface を $(1+\tfrac34\tau)$ に。地表収支からの導出を補い、$\tau$ 採用値（$+33$ K 整合）と CO₂ 倍化例を再設計。R6（同ファイル別小節）と行が独立することを確認。
3. **M3**（18章124-130・347-357行）: 解答18-1(2) の RJ 発散積分を完全 Planck 形（収束）または Wien カットオフ明示に。本文の論法（上端抑制の描像）と一致させる。
4. **M4**（25章135行、26章100・106・124-125・415行、演習HTML 297行）: (i) 25章 $\Delta E=\hbar A_{ul}$、(ii) 26章黄金律 $\rho(E_f)$ 明記、(iii) Bose 増強 振幅$\sqrt{n+1}$/率$(n+1)$ 書き分け（本文＋演習26-2＋HTML）、(iv) A係数分母3の由来一文。

**系統間の同期点**: 17章ファイル（R2=系統(b) と R6=系統(a) が同居）は、どちらか一方の編集完了後にもう一方を当てる（別小節・別行のためコンフリクトは想定しないが、最終 render 前に両方反映を確認）。

## 検証手順

### Phase A: 検算（Python）

各物理修正の正しさを `python3`（scipy.constants / CODATA）で確認する。検算項目:

1. **R1**: 修正後 $\varepsilon_\nu^{\rm ff}/\alpha_\nu^{\rm ff}$ の振動数・温度依存を評価し、$\propto\nu^3/(e^{h\nu/k_BT_e}-1)=B_\nu(T_e)$ を再現することを確認（現行 $\nu^{-2}T^{-3/2}$ 形は $\propto\nu^2$ となり $B_\nu$ 不再現）。RJ 極限で $\alpha\propto\nu^{-2}T^{-3/2}$（誘導放出因子吸収済み）に帰着することを確認。
2. **R2**: $T_{\rm eq}=255$ K・$T_g=288$ K で $(T_g/T_{\rm eq})^4\simeq1.627$。$(1+\tfrac34\tau)=1.627$ より $\tau\simeq0.84$。CO₂ 倍化の $\Delta\tau$ と $\Delta T_g$ が同一式で整合することを確認。
3. **R6**: 換算質量 $\mu=m_{\rm H}/2$ で $(2\pi\mu k_BT/h^2)^{3/2}=(\pi m_{\rm H}k_BT/h^2)^{3/2}$。旧 $(2\pi m_{\rm H}\ldots)$ との比 $2^{3/2}\simeq2.828$ を確認（両章同値）。
4. **M3**: 指数 $3-11/3+1=1/3$。完全 Planck 積分 $\int_0^\infty x^{5/3}/(e^x-1)dx\simeq1.932$（収束）。RJ のみ $\int_0^X x^{2/3}dx\propto X^{5/3}$（上端発散）を対比し「上端支配」を確認。
5. **M4**: 黄金律の次元 — $\rho(E_f)$［1/エネルギー］なら $\Gamma=(2\pi/\hbar)|M|^2\rho(E_f)$［1/時間］が整合。$A$係数 $\omega^3/(3\pi\epsilon_0\hbar c^3)|d|^2$ を 2p→1s に適用し $6.27\times10^8\,{\rm s^{-1}}$（文献値）を再現（回帰確認）。25章 $\Delta E=\hbar A_{ul}$ が［エネルギー］になることを確認。Bose: 率 $(n+1)=n+1$、振幅 $\sqrt{n+1}$ の関係。
6. **M5**: $160.2\,{\rm GHz}/29.98\simeq5.344\,{\rm cm^{-1}}\to5.35$。データ点 `[5.45, 18]` 不変を確認。
7. **回帰**: `code/check_exercises.py` を実行し、演習数値解答が全一致のまま（M3・M4 の解答修正が数値を壊していない）ことを確認。

（本仕様化フェーズで上記1〜6の主要値は事前検算済み。実装フェーズは修正後の実文面に対し再実行する。）

### Phase B: 相互参照・文字列チェック（grep）

1. **R3**: 全 qmd に対し `grep -rn review2 part*/` がヒットゼロ。
2. **R4**: §24.7 表の各章番号・第VII部の各節参照が、実在見出し（`grep -n "^## " part7/2*.qmd`）と一致。旧番号残留 `20.6`/`21.2`/`21.3`/`21.4`（§参照文脈）が消えていること。
3. **ラベル衝突**: 触れた @eq- ラベルが include 経由の重複展開でないこと（`grep -rn "eq-ff-\|eq-greenhouse\|eq-h2-\|eq-fermi\|eq-A-coefficient" _includes/` で二重定義がないこと）。

### Phase C: ビルド検証（quarto render）

1. `quarto render`（HTML/PDF/EPUB）が警告なく完了。
2. Quarto の未解決相互参照ワーニング（`@sec-`/`@eq-`/`@fig-`）ゼロ。
3. R5・M5 の図が正しく埋め込まれ、幾何・注記が意図どおり表示。
4. R4 修正後、§24.7 表・第VII部節参照がレンダリング結果で正しい章/節を指すこと。

### Phase D: CHANGELOG

1. `[Unreleased]` に Changed（R1・R2・R4・R6・M1・M2・M3・M4 のうち内容変更）／Fixed（R3・R5・M5・誤り訂正系）で全10 ID を記載。
2. 各エントリに review3 指摘 ID（R1–R6, M1–M5）と対象章・式を明記し、レポート指摘との対応を残す。

## Done When

- [ ] 系統(a)・系統(b) の全編集が対象ファイルに反映されている。
- [ ] Phase A 検算が修正後の文面で再現（SC-003）。
- [ ] Phase B の grep チェック全通過（SC-004, SC-005）。
- [ ] Phase C の `quarto render` が HTML/PDF/EPUB で警告なく完了、相互参照解決（SC-002）。
- [ ] Phase D の CHANGELOG に全10 ID 記載（SC-001）。
- [ ] v0.4 送りの軽微指摘が変更されていない（SC-006）。
