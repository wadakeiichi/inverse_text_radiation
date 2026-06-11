# Zenodo 登録手順書（v0.1）

`spectra-of-the-universe` 教科書 v0.1 の PDF を Zenodo に登録し、DOI を取得するための手順とメタデータ案をまとめる。

---

## 0. なぜ Zenodo か

- **DOI が永続的**：論文等で引用可能
- **CC BY 4.0 と相性が良い**：オープンライセンスを前提とする
- **無料**：CERN が運営、Open Science の中心インフラ
- **バージョン管理**：v0.1, v0.2, v1.0... と版を重ねるたびに新 DOI を取得できる
- **GitHub 連携可能**：リリース時に自動アップロードもできる

---

## 1. Zenodo アカウント作成

1. <https://zenodo.org> にアクセス
2. 「Sign up」→ GitHub アカウントで認証（ORCID とも紐付け可能）
3. プロフィールに ORCID を登録（持っていれば <https://orcid.org/0000-XXXX-XXXX-XXXX>）

---

## 2. PDF の準備

Mac の Terminal で：

```bash
cd "/Users/wada/Library/Mobile Documents/com~apple~CloudDocs/宇宙物理教科書/spectra-of-the-universe"

# PDF のみ生成
quarto render --to pdf
```

成果物：`_book/Thermal-Radiation-in-the-Universe.pdf`（フル原稿、約 200-300 ページ想定）

**もし日本語フォントエラーが出たら**：

```bash
# macOS で Noto CJK JP がない場合
brew install --cask font-noto-serif-cjk-jp
brew install --cask font-noto-sans-cjk-jp
```

それでもダメなら、`_quarto.yml` 内の PDF セクションを以下に書き換える：

```yaml
pdf:
  documentclass: ltjsbook  # ← jlreq でもOK
  pdf-engine: lualatex
  include-in-header:
    - text: |
        \usepackage{luatexja-fontspec}
        \setmainjfont{Hiragino Mincho ProN}  # macOS 標準フォントに切替
        \setsansjfont{Hiragino Sans}
```

ファイルサイズが大きい場合（>30MB）は `pdftk` や `gs` で圧縮：

```bash
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer \
   -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=v0.1.pdf _book/Thermal-Radiation-in-the-Universe.pdf
```

---

## 3. Zenodo へのアップロード（手動）

### 3-1. 新規 Upload を開始

1. 右上「**+ New upload**」をクリック
2. 「Files」セクションに上記 PDF をドラッグ＆ドロップ
3. 公開後の改訂は別バージョンとして扱う（**Reserve DOI** をチェックすると先に DOI が分かる）

### 3-2. メタデータ入力（下記コピー＆ペースト）

| フィールド | 入力値 |
|---|---|
| **Upload type** | Publication → Book |
| **Title** | 宇宙の熱的放射 ― 連続放射と線スペクトルの背景物理 (Thermal Radiation in the Universe: An Inverse Approach to the Physics) |
| **Authors** | 和田 桂一 (Wada, Keiichi) — Kagoshima University — ORCID: [your ORCID] |
| **Description** | 下記参照 |
| **Version** | v0.1 |
| **Language** | Japanese |
| **Keywords** | astrophysics; spectroscopy; blackbody radiation; line spectrum; statistical mechanics; quantum mechanics; QED; textbook; inverse approach |
| **Additional notes** | 下記参照 |
| **License** | Creative Commons Attribution 4.0 International (CC-BY-4.0) |
| **Funding** | （該当する科研費等あれば） |
| **Communities** | （該当する Zenodo Community があれば追加） |

### 3-3. Description（コピー用）

```text
学部後半〜大学院修士課程向けの宇宙物理教科書（ドラフト v0.1）。

宇宙物理の中心的観測対象である「連続スペクトル（黒体放射）」と「線スペクトル」を入口に、基礎物理（放射輸送・統計力学・量子論・電磁気学・原子物理・QED）を逆向きに学び直す。次の三つの原則を貫く：

1. 逆引き — 観測スペクトルから基礎物理を逆向きにたどる
2. 背景物理を曖昧にしない — 各観測量がどの物理から来ているかを章を横断して明示
3. 天下り的に式を与えない — 式を結果ではなく必然として理解させる

全 8 部 25 章 + 付録 A/B（数学補章・単位と基本定数）。二つの「中心地図」（プランク関数と水素線吸収係数）を各部冒頭で再掲し、各章で強調する因子を切り替えてどの物理が解き明かされているかを示す構成。最終章で電気双極子相互作用 Hamiltonian から両中心地図が QED で統一される。

本ドラフトは v0.1 として、批判的レビューを受け付けている段階（カバーレター: REVIEW.md および GitHub Pages を参照）。次バージョンで反映予定。

非熱的放射（シンクロトロン等）は本書の主軸ではなく、第18章で限定的に触れる。

ソース: https://github.com/wadakeiichi/inverse_text_radiation
公開ページ: https://wadakeiichi.github.io/inverse_text_radiation/
ライセンス: CC BY 4.0
```

### 3-4. Additional notes（コピー用）

```text
This is the v0.1 draft of an astrophysics textbook for senior undergraduates and master's students. The book is written in Japanese. An English translation will follow upon completion of the Japanese version.

Review and feedback from domain experts (astrophysics, atomic physics, quantum optics, statistical mechanics, QED) are actively being collected to inform v1.0. See REVIEW.md in the source repository for the review cover letter.

The accompanying source code (Quarto book) is also publicly available under the same CC BY 4.0 license at the GitHub repository link above.
```

### 3-5. Related identifiers（推奨）

- **Is supplement to** → URL: https://github.com/wadakeiichi/inverse_text_radiation (Repository)
- **Is documented by** → URL: https://wadakeiichi.github.io/inverse_text_radiation/ (Website)

### 3-6. Publish

「**Publish**」を押すと DOI が確定する。**プレビューで OK なら publish**（公開後は版を切らないと内容変更不可なので、最終確認を）。

---

## 4. DOI が取れたら

1. CITATION.cff の `doi` フィールドを追加：

   ```yaml
   doi: 10.5281/zenodo.XXXXXXX
   ```

2. README の「Zenodo に登録された preprint」リンクを実 URL に差し替え
3. REVIEW.md の DOI 欄を更新
4. 再 commit & push（実 DOI を反映した v0.1.1 として）

---

## 5. GitHub Release と連動させる場合（任意）

将来 v1.0 リリース時には、GitHub の Settings → Webhooks に Zenodo の webhook を登録すれば、GitHub Release を作るたびに自動的に新 DOI が振られる。設定方法：

1. Zenodo の「GitHub」タブを開く
2. 該当リポジトリを ON にする
3. GitHub で「Create a new release」（v1.0.0, v1.1.0, ...）

これで以降は手動アップロード不要。

---

## 6. 注意点

- **公開後はファイル差し替えできない**：誤字訂正だけのために新版を切るかは慎重に
- **CC BY 4.0** を選んだ以上、引用条件は CC BY 4.0 に準拠する
- **共著者の追加** は版を切るときにのみ可能。v0.1 で先に登録した著者は固定される（並べ替えは可能）

---

*このガイドも本書と同じ CC BY 4.0。*
