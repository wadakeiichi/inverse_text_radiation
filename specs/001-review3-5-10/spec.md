# 仕様: review3 重大＋中（物理系）指摘の v0.32 パッチ対応

**Feature Branch**: `001-review3-5-10`

**Created**: 2026-07-02

**Status**: Draft

**Input**: `review3-全章監査.md`（v0.31 時点 全章監査レポート）の「重大（修正必須）」6件および「中」のうち物理的正しさに関わる4件を、v0.32 パッチとして先行修正する。

---

## 概要

review3 監査で摘出された指摘のうち、**物理的な誤り・読者に見える事故・逆引き地図の誤誘導**にあたる10項目（重大 R1–R6、中の物理系 M1–M5）を v0.32 のパッチとして修正する。軽微指摘（review3「軽微」節および「中」の残り）は **v0.4 にまとめて送るため本仕様には含めない**。

本書 Constitution の原則 I（逆引き）・II（背景物理を曖昧にしない）・III（天下り式の禁止）を損なわないこと、および品質ゲート（`quarto render` 通過・相互参照解決・式の導出/出典・CHANGELOG 記載）を全項目で満たすことを完了条件とする。

---

## スコープ

### 対象（v0.32 で修正）

| ID | 分類 | 概要 | 主対象ファイル |
|---|---|---|---|
| R1 | 重大・数式 | 19章 自由-自由吸収係数を $\nu^{-3}T_e^{-1/2}$ 化、Kirchhoff 整合、17章 RJ 極限形への接続明記 | `part6/19-continuum-microprocesses.qmd` |
| R2 | 重大・物理/数式 | 17章 温室効果式を $(1+\tfrac34\tau)$ 化、$\tau$ 採用値と数値例（+33 K、CO₂ 倍化）を再設計 | `part6/17-stars-planets-dust.qmd` |
| R3 | 重大・編集事故 | 21章192行の内部コメント「review2 が…」除去 | `part7/21-line-formation.qmd` |
| R4 | 重大・逆引き地図 | 24章 §24.7 逆引き地図の「章」列全行修正＋第VII部の旧節番号残留一括修正 | `part7/24-line-applications.qmd` 他 |
| R5 | 重大・図 | `images/k-space-counting.svg` の弧 sweep フラグ修正 | `images/k-space-counting.svg` |
| R6 | 重大・数式係数 | 06章・17章 H₂ 解離平衡の並進因子を $(\pi m_{\rm H}k_BT/h^2)^{3/2}$ 化 | `part3/06-thermal-equilibrium.qmd`, `part6/17-stars-planets-dust.qmd` |
| M1 | 中・物理 | 05章 $J=S$（放射平衡）と $S=B$（LTE）の根拠分離 | `part2/05-radiative-transfer.qmd` |
| M2 | 中・物理 | 16章 CMB 歪み境界 $z\approx5\times10^4$ 統一、$\mu$/$y$ 予言の書き分け | `part6/16-cmb.qmd` |
| M3 | 中・物理 | 18章 $\nu^{1/3}$ 論法（Wien カットオフ明示 or 完全 Planck 形）＋解答18-1(2) 修正 | `part6/18-accretion-high-energy.qmd` |
| M4 | 中・物理 | 26章 黄金律の次元・Bose 増強の振幅/率・A 係数分母3の由来、25章 $\Delta E=\hbar A_{ul}$ | `part8/26-qed-minimum.qmd`, `part8/25-em-field-quantization.qmd`, exercises |
| M5 | 中・図 | `images/firas-spectrum.svg` の「5.45 cm⁻¹」→「5.35 cm⁻¹」（PNG 併存対応） | `code/firas_fit.py` → svg/png 再生成 |

### 対象外（v0.4 送り）

- review3「軽微（次回改訂時にまとめて）」節の全項目。
- review3「中」節のうち物理系以外（`_planck-map.qmd` のモード密度行、14章 $8\pi$ の起源表、01–13章の記法・年代・言い回し系、23章 Doppler 幅の呼称、24章 禁制線因果、22章 α² 飛び、21章 等価幅の言い回し、付録B $t_{\rm ff}$、演習26-1 転記問題、図版の重なり・はみ出し・豆腐化）。
- 実装（本文 qmd・svg の実編集）そのもの。本仕様は仕様化フェーズであり、qmd/svg は一切変更しない。

---

## 実装系統の区分（Constitution・品質ゲート由来）

実装は難易度により2系統に分かれる（詳細は plan.md）。本仕様はどちらの系統が担当するかを各要求に付す。

- **系統(a) 機械的修正**（別エージェント担当）: R3, R4, R5, R6, M1, M2, M5。文言差し替え・番号修正・係数修正・図の座標修正・再生成が中心で、新しい物理の書き下ろしを伴わない。
- **系統(b) 物理書き直し**（上位モデル担当）: R1, R2, M3, M4。式の導出・数値例の再設計・章間整合の再構成を伴い、原則 II・III の観点で本文の物理を書き直す。

---

## User Scenarios & Testing

### User Story 1 — 自由-自由吸収係数の物理的正しさ（R1, 系統(b), 優先 P1）

読者（B4–M1）が19章 §19.x（自由-自由）を読み、吸収係数 $\alpha_\nu^{\rm ff}$ の形と、放出係数との比が黒体 $B_\nu(T_e)$ を再現すること（素過程での Kirchhoff）を確認できる。現状の $T_e^{-3/2}\nu^{-2}$ は誘導放出因子の二重計上で、$\varepsilon/\alpha$ が $B_\nu$ を再現せず本節の主張と自己矛盾する。

**Why this priority**: 物理的誤りであり、かつ本節の中心的主張（Kirchhoff が素過程で確かめられる）を直接壊しているため最優先。

**Independent Test**: 修正後の $\alpha_\nu^{\rm ff}\propto n_en_iZ^2 T_e^{-1/2}\nu^{-3}(1-e^{-h\nu/k_BT_e})$ と @eq-ff-emissivity の比を取り、$S_\nu=j_\nu/\alpha_\nu=(2h\nu^3/c^2)\cdot 1/(e^{h\nu/k_BT_e}-1)=B_\nu(T_e)$ が振動数・温度依存も含めて再現されることを検算で確認。

**Acceptance Scenarios**:
1. **Given** 19章 @eq-ff-absorption-micro が $T_e^{-1/2}\nu^{-3}(1-e^{-h\nu/k_BT_e})$ に修正されている、**When** @eq-ff-emissivity との比を取る、**Then** $\nu^3/(e^x-1)$ 形が出て @eq-ff-kirchhoff の $B_\nu(T_e)$ が矛盾なく成立する。
2. **Given** 87行付近の §17.6 参照、**When** 読者が17章へ飛ぶ、**Then** 「RJ 極限（$h\nu\ll k_BT_e$）で17章の $\nu^{-2}T_e^{-3/2}$ 形（誘導放出因子を吸収済みの表現）に帰着する」という接続が本文に明記されている。

### User Story 2 — 温室効果式の物理的正しさと数値整合（R2, 系統(b), 優先 P1）

読者が17章 §17.7（温室効果）を読み、地表温度の式・$\tau$ 採用値・数値例（+33 K、CO₂ 倍化）が互いに整合し、エディントン近似から正しく導かれることを確認できる。現状の $T_g^4\simeq T_{\rm eq}^4(1+\tfrac32\tau)$ は温室効果項を2倍過大評価し、$\tau\approx0.5$–$0.6$ と CO₂ 倍化例（$\tau\simeq0.36\to0.39$）が不整合。

**Why this priority**: 物理的誤り。地球気候という読者の関心が高い題材で、係数と数値が二重に狂っている。

**Independent Test**: 修正後の式 $\sigma T_g^4=F(1+\tfrac34\tau_g)$（本文表現は @eq-greenhouse-surface）で、$+33$ K（$T_{\rm eq}\simeq255$ K→$T_g\simeq288$ K、$(T_g/T_{\rm eq})^4\simeq1.63$）を説明する $\tau$ が採用値として本文と一致すること、CO₂ 倍化の数値例が同じ式・同じ $\tau$ 定義で整合することを検算。

**Acceptance Scenarios**:
1. **Given** @eq-greenhouse-surface が $(1+\tfrac34\tau)$ 形に修正されている、**When** $+33$ K を要求する、**Then** $(1.63-1)/0.75\simeq0.84$ 前後の $\tau$ 採用値が本文に示され、$\tau\approx0.5$–$0.6$ という旧記述が新採用値に置き換わっている。
2. **Given** CO₂ 倍化の数値例、**When** 244行と251行を照合する、**Then** 両者が同一の式・$\tau$ 定義・昇温幅で整合している（旧 $0.36\to0.39$ の矛盾が解消）。
3. **Given** 修正後の導出、**When** エディントン解（§5.10 @eq-eddington-temperature と同型）から辿る、**Then** 地表収支込みで $(1+\tfrac34\tau)$ が導かれる筋道が本文にあり、天下り式でない（原則 III）。

### User Story 3 — 逆引き地図・節番号参照の正確さ（R4, 系統(a), 優先 P1）

読者が第VII部の到達点である §24.7「線スペクトル逆引き地図」に達したとき、各因子から正しい章へ誘導される。また第VII部内の相互参照節番号が現行章立てと一致する。現状は §24.7 の「章」列が全行 +1 ずれ、他にも旧章番号残留の節参照が複数ある。

**Why this priority**: 第VII部の到達点が読者を誤った章へ誘導する。原則 I（逆引き）の中心成果物の誤り。

**Independent Test**: 修正後の §24.7 表の各行の章番号を、実際にその因子を扱う章（本仕様の新旧対応に基づく）と照合し全行一致すること。第VII部の各節参照が指す先の見出しが現行 §番号と一致すること。

**Acceptance Scenarios**:
1. **Given** §24.7 表、**When** 各行の「章」列を確認する、**Then** $\nu_0$→22、$f_{lu}$→22、$n_l$→21・24、$\phi$→23 に修正されている（tasks.md の新旧対応表に基づく全行）。
2. **Given** 第VII部の旧節番号残留（20:12, 20:24, 20:25, 21:297, 22:172, 22:318, 22:366）、**When** それぞれの参照先を確認する、**Then** 現行 §番号（tasks.md 対応表）に一括修正されている。

### User Story 4 — 読者に見える内部コメントの除去（R3, 系統(a), 優先 P1）

読者が21章 §21.5 を読むとき、内部レビュアー向けコメントを目にしない。現状 192行に「― review2 が抽象的と感じた統計平衡の中身は…」が混入している。

**Why this priority**: 編集事故。読者に直接見えており、書籍の信頼性を損なう。修正は一文の書き換えで即完了。

**Independent Test**: 21章本文全体を `review2` で検索してヒットゼロ、当該一文が読者向けの自然な表現に置き換わっていること。

**Acceptance Scenarios**:
1. **Given** 21章 192行、**When** 「review2」で全文検索、**Then** ヒットせず、「統計平衡の抽象論の中身は、この一本の不等式に凝縮できる」等に書き換わっている。

### User Story 5 — 図版の幾何・数値の正確さ（R5, M5, 系統(a), 優先 P2）

読者が図を見たとき、幾何が正しく（k 空間の球面断面が円弧に見える）、注記数値が正しい（FIRAS ピーク波数が 5.35 cm⁻¹）。

**Why this priority**: 図の誤りは読者に直接見えるが、本文の物理そのものは正しいため P2。

**Independent Test**: R5 は修正後 svg をレンダリングして3本の弧が球面（円）方向に湾曲すること。M5 は再生成後の svg/png の注記が「5.35 cm⁻¹」で、$160.2/29.98\simeq5.35$ の検算と一致すること。

**Acceptance Scenarios**:
1. **Given** `k-space-counting.svg` の3本の弧、**When** sweep フラグを反転する、**Then** 円弧が球面断面として自然に湾曲し双曲線状に見えない。数え上げの数値・式は不変。
2. **Given** `firas-spectrum` の注記、**When** `code/firas_fit.py` の注釈文字列を修正し svg/png を再生成する、**Then** 両ファイルの注記が「peak ≈ 160 GHz (5.35 cm⁻¹)」になり、データ点 `[5.45, 18]`（実測波数）は変更されていない。

### User Story 6 — 解離平衡係数の正確さ（R6, 系統(a), 優先 P2）

読者が06章 §6.7 の質量作用表と17章 §17.8 の H₂ 解離平衡を見たとき、並進因子が換算質量に基づく正しい係数 $(\pi m_{\rm H}k_BT/h^2)^{3/2}$ になっている。現状は両章とも $(2\pi m_{\rm H}k_BT/h^2)^{3/2}$ で $2^{3/2}\simeq2.8$ 倍過大。

**Why this priority**: 数式係数の誤りだが局所的で、係数差し替え（または $Z$ 定義注記）で完結するため P2。

**Independent Test**: 換算質量 $\mu=m_{\rm H}/2$ より並進因子は $(2\pi\mu k_BT/h^2)^{3/2}=(\pi m_{\rm H}k_BT/h^2)^{3/2}$。両章の係数が一致し、$Z$ が並進部を含むか否かの扱いが明示されていること。

**Acceptance Scenarios**:
1. **Given** 06章 278行の質量作用表 解離行と17章 264–266行 @eq-h2-dissociation、**When** 並進因子を確認する、**Then** 両者とも $(\pi m_{\rm H}k_BT/h^2)^{3/2}$（または $Z$ 定義に並進部を含める旨の注記付き）で一致している。

### User Story 7 — LTE と放射平衡の根拠分離（M1, 系統(a), 優先 P2）

読者が05章 §5.x を読むとき、$J=S$ が放射平衡の帰結、$S=B$ が LTE の帰結であると根拠が分離して書かれている。現状 390行・431行は「LTE では $S=J=B$」と両者を混同し、本書の核心（§5.5・問題5-5「LTE でも $J_\nu\ne B_\nu$」）と自己矛盾する。

**Why this priority**: 本書の核心概念（LTE と熱平衡の区別）に触れる論理的誤りだが、修正は根拠の書き分けで局所的に完結。

**Independent Test**: 390行・431行に「$J=S$ は放射平衡から、$S=B$ は LTE から」の分離が明記され、§5.5・問題5-5 の記述と矛盾しないこと。

**Acceptance Scenarios**:
1. **Given** 431行「LTE では $S=J=B$」、**When** 修正、**Then** 「放射平衡から $J=S$、LTE から $S=B$、両者が揃って $J=S=B$」と根拠が分離されている。
2. **Given** 390行「$J$…（LTE では $S$ に等しい）」、**When** 修正、**Then** 「放射平衡では $S$ に等しい」等に訂正されている。

### User Story 8 — CMB 歪み境界と μ/y 予言の整合（M2, 系統(a), 優先 P2）

読者が16章 §16.x を読むとき、$y$ 歪みと $\mu$ 歪みの境界赤方偏移が一貫し、$\mu$ と $y$ の標準予言が別々の値・起源で書き分けられている。現状は $z\lesssim10^4$ と $z\sim5\times10^4$ の間の帯域が宙に浮き、$|\mu|,|y|\sim10^{-8}$ とまとめて過小評価している。

**Why this priority**: 物理的整合の欠落だが、境界値の統一と予言の書き分けという局所修正で完結。

**Independent Test**: 境界が $z\approx5\times10^4$ に統一（または中間型 $r$ 歪みの一文注記）され、$\mu\sim10^{-8}$ と $y\sim10^{-6}$（再電離・構造形成起源、FIRAS 限界の1桁下）が書き分けられていること。

**Acceptance Scenarios**:
1. **Given** 66行・122–128行の境界、**When** 確認、**Then** $y$/$\mu$ の境界が $z\approx5\times10^4$ に統一されている（または帯域に中間型 $r$ 歪みの注記がある）。
2. **Given** 130行の予言、**When** 確認、**Then** $\mu$ と $y$ が別々に書かれ、$y\sim10^{-6}$（FIRAS 限界の約1桁下）と $\mu\sim10^{-8}$ が区別されている。

### User Story 9 — ν^{1/3} 論法の正しい根拠（M3, 系統(b), 優先 P2）

読者が18章 §18.2 と演習解答18-1(2) を読むとき、多色円盤の $\nu^{1/3}$ べき則が **Wien カットオフ（積分上端の抑制）** に基づいて正しく導かれる。現状は RJ 近似のみで積分し「端の寄与が効かない」としているが、RJ のみの $\int x^{2/3}dx$ は上端発散で、実際は上端支配。因果が逆。

**Why this priority**: 物理的論法の誤り。演習解答という読者が手を動かして辿る箇所で結論の根拠が破綻している。

**Independent Test**: 完全 Planck 形 $F_\nu\propto\nu^{1/3}\int_0^\infty x^{5/3}/(e^x-1)\,dx$（収束、値 $\simeq1.93$）に書き換えるか、RJ の有効上限 $T\sim h\nu/k_B$（Wien カットオフ）を明示。指数 $3-11/3+1=1/3$ が保たれること。

**Acceptance Scenarios**:
1. **Given** 解答18-1(2)（353行付近）、**When** 修正、**Then** RJ のみの発散積分に代えて完全 Planck 形の収束積分、または Wien カットオフ $T\lesssim h\nu/k_B$ による上端抑制が明示され、「端の寄与が効かない」という逆の記述が訂正されている。
2. **Given** 本文 124–130行の $\nu^{1/3}$ 説明、**When** 確認、**Then** 「$k_BT\sim h\nu$ の円環が最も効き、それより熱い内側は Wien で抑えられる」という上端抑制の描像が本文の論法と一致している。

### User Story 10 — QED（黄金律・Bose 増強・A 係数）の次元と分解（M4, 系統(b), 優先 P2）

読者が25–26章と演習26-2 を読むとき、(i) 25章の自然幅が $\Delta E=\hbar A_{ul}$（次元整合）、(ii) 26章の Fermi 黄金律が終状態密度 $\rho(E_f)$ の明示（次元整合）、(iii) Bose 増強が振幅の $\sqrt{n+1}$ と率の $(n+1)$ を書き分け、(iv) A 係数の分母 3 の由来（偏光和＋方向平均 $|\mathbf d\cdot\boldsymbol\epsilon|^2\to|\mathbf d|^2/3$）が一文で説明されている。

**Why this priority**: 章間不整合・次元不整合・分解の破綻を含む物理誤り。第VIII部（QED からの俯瞰）の到達点。

**Independent Test**: 25章135行が $\Delta E=\hbar A_{ul}$、26章 @eq-fermi-golden-rule が $\rho(E_f)$ で係数と次元が整合、本文と演習26-2 で Bose 増強が振幅 $\sqrt{n+1}$／率 $(n+1)=n$（誘導）$+1$（自発）と分解、@eq-A-coefficient-QED の 3 の由来が本文にあること。

**Acceptance Scenarios**:
1. **Given** 25章 135行「エネルギー幅 $\Gamma=A_{ul}$」、**When** 修正、**Then** $\Delta E=\hbar A_{ul}$（次元 [エネルギー]）に訂正され、26章の記法と整合している。
2. **Given** 26章 @eq-fermi-golden-rule（100行）、**When** 確認、**Then** 終状態密度が $\rho(E_f)$（単位エネルギーあたり）と明記され、係数 $2\pi/\hbar$ と次元が整合している（角振動数あたりなら係数を対応させる）。
3. **Given** 本文124–125行・演習26-2 解答（415行）・演習HTML、**When** 確認、**Then** 振幅の $\sqrt{n+1}$ と率の $(n+1)=n$（誘導）$+1$（自発）が書き分けられ、$A_{ul}/B_{ul}$ 分解が成立している。
4. **Given** @eq-A-coefficient-QED（106行）の分母 3、**When** 確認、**Then** 偏光和＋方向平均 $|\mathbf d\cdot\boldsymbol\epsilon|^2\to|\mathbf d|^2/3$ に由来する旨が一文で説明されている（$\omega^3$ の丁寧さと対称）。

### Edge Cases

- **ラベル付き数式の include 多重展開**: 本仕様が触れる @eq- ラベルはいずれも初出章のもので include 経由でないことを実装前に確認する（`_includes/` の再掲版と衝突しないこと）。
- **図版とデータ点の混同（M5）**: firas の注記文字列「5.45」と実測データ点 `[5.45, 18]` は別物。データ点は変更しない。
- **図の二重管理（M5）**: svg は matplotlib 生成で文字がパス化されており直接編集不可。Python 再生成で svg/png を同時更新する。
- **演習の二重管理（M4d）**: 演習26-2 は qmd 本体と `exercises/演習問題_第VIII部_QEDからの俯瞰.html`（プリレンダ版）の双方に存在する。両方の $\sqrt{n+1}$ 記述を整合させる。
- **R4 の caption 範囲（20:12）**: 「§19-23」は第VII部の章範囲を指す注記。現行章立て（20–24章）に合わせる（推奨値は tasks.md で確定）。

---

## Requirements

### Functional Requirements

- **FR-R1**: 19章 @eq-ff-absorption-micro を $\alpha_\nu^{\rm ff}\propto n_en_iZ^2 T_e^{-1/2}\nu^{-3}(1-e^{-h\nu/k_BT_e})$ に修正し、@eq-ff-emissivity との比が $B_\nu(T_e)$ を再現することを本文の論理と一致させる。87行付近の §17.6 参照を整理し、「RJ 極限で17章の $\nu^{-2}T_e^{-3/2}$ 形に帰着」を明記する。
- **FR-R2**: 17章 @eq-greenhouse-surface を $(1+\tfrac34\tau)$ 形に修正し、地表収支込みの導出を示す。$+33$ K を説明する $\tau$ 採用値を提示し、CO₂ 倍化の数値例（244行・251行）を同一式・同一 $\tau$ 定義で整合するよう再設計する。
- **FR-R3**: 21章 192行の「review2」を含む内部コメントを読者向け表現に書き換える。章内 `review2` 検索でヒットゼロにする。
- **FR-R4**: 24章 §24.7 逆引き地図の「章」列を全行、実際に各因子を扱う現行章番号へ修正する。第VII部の旧節番号残留（20:12, 20:24, 20:25, 21:297, 22:172, 22:318, 22:366）を現行 §番号へ一括修正する。
- **FR-R5**: `images/k-space-counting.svg` の該当3本の弧の sweep フラグを反転し、球面断面が円弧として自然に湾曲するようにする。数え上げの数値・式は不変。
- **FR-R6**: 06章 278行および17章 264–266行の H₂ 解離平衡の並進因子を $(\pi m_{\rm H}k_BT/h^2)^{3/2}$ に統一する（または $Z$ 定義に並進部を含める旨を明記）。両章の係数を一致させる。
- **FR-M1**: 05章 390行・431行で $J=S$（放射平衡の帰結）と $S=B$（LTE の帰結）を根拠分離して記述し、§5.5・問題5-5 と矛盾しないようにする。
- **FR-M2**: 16章の $y$/$\mu$ 歪みの境界を $z\approx5\times10^4$ に統一（または中間型 $r$ 歪みを一文注記）し、130行の予言を $\mu\sim10^{-8}$／$y\sim10^{-6}$ に書き分ける。
- **FR-M3**: 18章 §18.2 本文と解答18-1(2) の $\nu^{1/3}$ 論法を、完全 Planck 形の収束積分または RJ の有効上限 $T\sim h\nu/k_B$（Wien カットオフ）に基づく形へ修正し、「端の寄与が効かない」という逆の記述を訂正する。
- **FR-M4**: 26章の Fermi 黄金律に $\rho(E_f)$ を明記し次元整合させ、Bose 増強を振幅 $\sqrt{n+1}$／率 $(n+1)$ で書き分け（本文＋演習26-2＋演習HTML）、A 係数分母 3 の由来を一文で説明する。25章 135行を $\Delta E=\hbar A_{ul}$ に修正する。
- **FR-M5**: `code/firas_fit.py` の注釈文字列「5.45 cm⁻¹」を「5.35 cm⁻¹」に修正し、`firas-spectrum.svg` と `firas-spectrum.png` を同時に再生成する。実測データ点 `[5.45, 18]` は変更しない。
- **FR-CHANGELOG**: 全10項目を `CHANGELOG.md` `[Unreleased]` に Changed / Fixed で記載し、各エントリに review3 の指摘 ID（R1–R6, M1–M5）を対応づける。
- **FR-RENDER**: 全修正後に `quarto render`（HTML/PDF/EPUB）が警告なく完了し、相互参照（@sec-/@eq-/@fig-）が全て解決すること。
- **FR-NO-REGRESSION**: 本パッチは v0.4 送りの軽微指摘を先取りして修正しない（スコープ厳守）。既存の正しい記述・数値・図を壊さない。

### Key Entities

- **指摘 ID**: R1–R6（重大）、M1–M5（中・物理系）。CHANGELOG エントリと1対1で対応づける traceability キー。
- **対象ファイル**: qmd 本文（8ファイル）、svg 図版（1）、Python 生成スクリプト（1）、演習HTML（1）、CHANGELOG。
- **@eq- ラベル**: eq-ff-absorption-micro, eq-ff-emissivity, eq-ff-kirchhoff, eq-greenhouse-surface, eq-h2-dissociation, eq-fermi-golden-rule, eq-A-coefficient-QED, eq-J-of-tau, eq-eddington-temperature, eq-disk-13-powerlaw。
- **新旧章/節対応表**: R4 の §24.7 表および第VII部節参照の新旧マッピング（tasks.md に掲載）。

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: 10項目（R1–R6, M1–M5）すべてが受け入れ条件を満たし、対応する CHANGELOG エントリ（指摘 ID 付き）が `[Unreleased]` に存在する。
- **SC-002**: `quarto render` が HTML/PDF/EPUB で警告なく完了し、相互参照の未解決・重複・誤参照がゼロ。
- **SC-003**: 物理修正（R1, R2, R6, M3, M4）の検算が Python で再現され、R1 は $\varepsilon/\alpha=B_\nu$、R2 は $+33$ K に対応する $\tau$、R6 は $2^{3/2}$ 係数差、M3 は指数 $1/3$ と収束積分、M5 は $160.2/29.98\simeq5.35$ を確認できる。
- **SC-004**: R3 について本文全 qmd の `review2` 全文検索がヒットゼロ。
- **SC-005**: R4 について §24.7 表の全行と第VII部の対象節参照が、実在の現行章/節見出しと100%一致する。
- **SC-006**: v0.4 送りとした軽微・非物理系の指摘が本パッチで変更されていない（スコープ逸脱ゼロ）。

---

## Assumptions

- 本仕様は **仕様化フェーズ** であり、qmd/svg/py の実編集は行わない。実装は別フェーズ（系統(a)/(b)）で行う。
- 行番号は review3（v0.31 時点）を基準としつつ、本仕様策定時に Grep/Read で実在確認し正確な位置に更新済み（tasks.md に確定行番号を記載）。実装着手時に再確認する。
- R2 の $\tau$ 採用値・数値例の具体値は系統(b)（上位モデル）が導出時に確定する。本仕様は「$+33$ K と CO₂ 倍化が同一式で整合する」ことを条件として与える。
- M3 は「完全 Planck 形」か「Wien カットオフ明示」のいずれかを系統(b)が選択する。本仕様は結論の指数 $1/3$ と論法の物理的正しさを条件とする。
- M5 の firas 図は Python 再生成が可能（`code/firas_fit.py` が svg/png を出力）であることを前提とする。k-space 図（R5）は手書き svg であり直接編集する。
- CHANGELOG の `[Unreleased]` は現状空であり、本パッチが最初のエントリ群を追加する。
- リリース時作業（version-history.qmd・CITATION.cff 更新、Zenodo/DOI）は v0.32 確定時に別途行い、本仕様の完了条件には含めない。
