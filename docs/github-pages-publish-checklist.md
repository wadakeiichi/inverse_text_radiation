# GitHub Pages 公開チェックリスト（v0.1）

push 後にGitHubの設定で確認・操作する手順をまとめる。

---

## 0. 前提：Mac で push 完了

```bash
cd "/Users/wada/Library/Mobile Documents/com~apple~CloudDocs/宇宙物理教科書/spectra-of-the-universe"
rm -f .git/index.lock
git add -A
git status   # ← 変更内容を確認（タイトル変更・付録・第VI-VIII部・cover.svg ほか）
git commit -m "Retitle + Add Part VI-VIII + Appendices + Reviewer onboarding (v0.1)

主な変更:
- 本書改題: 宇宙の熱的放射 ― 連続放射と線スペクトルの背景物理
  (Thermal Radiation in the Universe: An Inverse Approach to the Physics)
- 扉絵 cover.svg を連続+線スペクトル左右並置で再デザイン
- 第VI部（15-18章）、第VII部（19-23章）、第VIII部（24-25章）本文ドラフト
- 付録 A（数学補章）、付録 B（単位と基本定数）追記
- 付録 C → 序章 §0.4 に統合
- レビュー優先度高〜低 50項目超の修正
- レビュアー向けドキュメント追加（REVIEW.md, docs/）"
git push origin main
```

push 後、GitHub Actions が走り始める。

---

## 1. GitHub Actions の状態確認

1. ブラウザで <https://github.com/wadakeiichi/inverse_text_radiation/actions> を開く
2. 「**Quarto Publish**」の最新ワークフローを確認
3. 緑のチェックなら成功、赤の × なら失敗

### よくある失敗パターン

| 症状 | 対処 |
|---|---|
| Python パッケージのインストールでタイムアウト | 再実行（Re-run jobs ボタン） |
| TinyTeX セットアップで失敗 | `.github/workflows/publish.yml` で `tinytex: true` を再確認 |
| Japanese フォントの取得失敗 | apt-get の URL 変更が必要なことがある（Issues を確認） |
| Permission denied で gh-pages にプッシュできない | リポジトリ Settings → Actions → Workflow permissions → "Read and write permissions" |

ローカルでまず：

```bash
quarto render --to html
```

が通るかを試しておくと、CI 失敗時の切り分けが早い。

---

## 2. GitHub Pages の有効化

CI 成功後、初回のみリポジトリ設定が必要：

1. <https://github.com/wadakeiichi/inverse_text_radiation/settings/pages> を開く
2. **Build and deployment**
   - Source: **Deploy from a branch**
   - Branch: **gh-pages** / **(root)** を選択
3. 「Save」を押す

数分待つと、公開 URL が表示される：

→ **<https://wadakeiichi.github.io/inverse_text_radiation/>**

カスタムドメインを使いたい場合は、同じ画面の「Custom domain」に DNS 設定済みのドメインを入力。

---

## 3. 公開ページの動作確認

URL を開いて、以下が正しく表示されるか確認：

- [ ] 表紙（index.qmd）に新タイトルとサブタイトル
- [ ] 数式が MathJax で正しくレンダリング
- [ ] サイドバーに 25 章 + 付録 が並ぶ
- [ ] 各章冒頭の中心地図 callout
- [ ] 図（cover.svg, planck_curve.png 等）が表示される
- [ ] PDF ダウンロードボタン（右上）が機能する
- [ ] EPUB ダウンロードボタンが機能する

スマートフォン・タブレットからもアクセス可能か確認。

---

## 4. README の Pages URL を実 URL に差替

```diff
- ## リポジトリ
- 
- - ソース：<https://github.com/wadakeiichi/inverse_text_radiation>
- - 公開ページ：（GitHub Pages 公開後にここに URL を記載）
+ ## リポジトリ
+ 
+ - ソース：<https://github.com/wadakeiichi/inverse_text_radiation>
+ - 公開ページ：<https://wadakeiichi.github.io/inverse_text_radiation/>
```

これも commit & push。

---

## 5. Issues テンプレートを設置（任意・推奨）

レビュアーが Issue を立てる際の枠組みを用意しておくと、整理しやすい。

`.github/ISSUE_TEMPLATE/review-feedback.md` を作る：

```markdown
---
name: 📝 Review feedback (レビューコメント)
about: 本書 v0.1 への指摘・提案を投稿
title: "[Review] 第X章 §X.Y - 短い要約"
labels: review
---

## 該当箇所
- 章・節：
- 行・式 ID（あれば）：

## 種別
- [ ] 物理的誤り
- [ ] 数値・単位の誤り
- [ ] 用語・記法の不統一
- [ ] 説明の不明瞭さ
- [ ] 教育的観点（難易度・順序）
- [ ] 文献の追加提案
- [ ] その他

## 詳細
（現状の記述、問題点、提案を具体的に）

## 参考文献（あれば）
```

これも commit。

---

## 6. 完了したら

- Pages URL を REVIEW.md と docs/review-request-email-template.md に書き込む
- Zenodo に PDF を登録（`docs/zenodo-upload-guide.md` 参照）
- DOI が出たら README / REVIEW.md を更新
- レビューメール送信開始（`docs/review-request-email-template.md`）

---

*このチェックリストも CC BY 4.0。*
