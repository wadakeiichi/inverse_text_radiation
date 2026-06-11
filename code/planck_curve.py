"""
planck_curve.py — プランク関数とその古典極限（Wien 極限・Rayleigh-Jeans 極限）

第I部・第II部・第IV部の説明で使う。
天下り的にプランク分布を「与える」のではなく、観測される連続スペクトルの
形を再現するために必要な構造を、コードで段階的に立ち上げる方針に対応。

# 図のラベルについて

matplotlib の図中ラベルは、日本語フォントが OS にインストールされていないと
文字化け（□□□）する。本スクリプトでは：
  - デフォルトでは ASCII / LaTeX 表記の英語ラベルを使う（環境に依存しない）
  - 起動時に日本語フォントを自動検出し、見つかれば使う（OS にあれば自動で日本語化）
  - Quarto の fig-cap（図キャプション）は HTML/PDF 側で日本語フォントで描画されるので、
    そちらに日本語の説明文を書けば十分

# 使い方（Quartoから）:
  ```{python}
  import sys; sys.path.insert(0, "../code")
  from planck_curve import plot_planck_with_limits
  fig, ax = plot_planck_with_limits(temperatures=(2.7, 310, 3000, 5800))
  ```
"""
import numpy as np
import matplotlib

# Quarto の PDF ビルドで matplotlib が PDF backend を直接呼ぶと
# CJK フォント名（"Noto Sans CJK JP"）の ASCII エンコードに失敗するため、
# 明示的に AGG backend（PNG 出力用）を強制する。Quarto 側でも fig-format: png 指定済み。
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from astropy import constants as const


# ---------------------------------------------------------------------------
# 日本語フォントの自動検出（環境にあれば使う）
# ---------------------------------------------------------------------------
def _try_set_japanese_font():
    """matplotlib に日本語フォントが利用可能なら設定する。"""
    import matplotlib.font_manager as fm
    candidates = [
        "Hiragino Sans",            # macOS
        "Hiragino Mincho ProN",     # macOS
        "Yu Gothic", "YuGothic",    # Windows / macOS
        "Meiryo",                   # Windows
        "Noto Sans CJK JP",         # Linux / GHA
        "Noto Serif CJK JP",        # Linux / GHA
        "IPAGothic", "IPAexGothic", # Linux
        "TakaoGothic",              # Linux
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for font in candidates:
        if font in available:
            matplotlib.rcParams["font.family"] = font
            return font
    return None


_JP_FONT = _try_set_japanese_font()
matplotlib.rcParams["axes.unicode_minus"] = False  # 軸のマイナス記号の文字化け対策

# PDF 出力時の保険：TrueType フォントを埋め込む（fonttype 42）
# Quarto 側で fig-format: png にしているので通常は経由しないが、念のため。
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42


# ---------------------------------------------------------------------------
# 物理定数（CGS）
# ---------------------------------------------------------------------------
h = const.h.cgs.value      # erg s
c = const.c.cgs.value      # cm/s
kB = const.k_B.cgs.value   # erg/K


# ---------------------------------------------------------------------------
# プランク関数とその両極限（数値アンダーフロー対策つき）
# ---------------------------------------------------------------------------
def planck_nu(nu, T):
    """B_nu(T): 比強度 [erg s^-1 cm^-2 Hz^-1 sr^-1].

    数値オーバーフロー対策：x = hν/kT が大きい領域では、
    expm1(x) が極端に大きくなり 2hν³/c² との比が
    アンダーフローして 10^-300 などになる。これを 0 に潰し、
    log スケール描画で「線が見えない」だけにする（縦軸の自動拡張を防ぐ）。
    """
    nu = np.asarray(nu, dtype=float)
    x = h * nu / (kB * T)
    out = np.zeros_like(nu)
    # x < ~700 で expm1(x) は double で扱える。超えると out = 0。
    safe = x < 700
    if np.any(safe):
        out[safe] = (2.0 * h * nu[safe] ** 3 / c ** 2) / np.expm1(x[safe])
    return out


def rayleigh_jeans_nu(nu, T):
    """Rayleigh-Jeans 極限 (hν ≪ kT)."""
    nu = np.asarray(nu, dtype=float)
    return 2.0 * nu ** 2 * kB * T / c ** 2


def wien_nu(nu, T):
    """Wien 極限 (hν ≫ kT)."""
    nu = np.asarray(nu, dtype=float)
    x = h * nu / (kB * T)
    out = np.zeros_like(nu)
    safe = x < 700
    if np.any(safe):
        out[safe] = (2.0 * h * nu[safe] ** 3 / c ** 2) * np.exp(-x[safe])
    return out


# ---------------------------------------------------------------------------
# B_ν のピーク振動数（Wien の式 振動数表示）
# ν_max / T ≈ 5.879 × 10^10 Hz/K
# ---------------------------------------------------------------------------
_NU_PEAK_PER_T = 5.879e10  # Hz / K


# ---------------------------------------------------------------------------
# プランク曲線の描画
# ---------------------------------------------------------------------------
def plot_planck_with_limits(
    temperatures=(3000, 5800, 10000),
    nu_min=None,
    nu_max=None,
    npts=500,
    show_limits=None,
    ax=None,
    use_japanese=None,
):
    """複数の温度でプランク曲線を描く。

    Parameters
    ----------
    temperatures : tuple of float
        描く温度 [K] の列。例： (2.7, 310, 3000, 5800)
    nu_min, nu_max : float, optional
        プロット範囲の振動数 [Hz]。None なら温度範囲から自動決定する。
    npts : int
        サンプル点数。
    show_limits : bool, optional
        Rayleigh-Jeans / Wien 極限を併記するか。
        None（デフォルト）なら温度数が 3 以下のときだけ表示する。
    ax : matplotlib.axes.Axes, optional
        既存の axes に描く場合に指定。
    use_japanese : bool, optional
        日本語ラベルを使うかどうか。None なら自動（フォントが利用可能なら使う）。
    """
    if not isinstance(temperatures, (list, tuple)):
        temperatures = [temperatures]

    # ピーク位置から振動数範囲を自動決定（指定がなければ）
    if nu_min is None:
        nu_min = _NU_PEAK_PER_T * min(temperatures) / 1e2  # 最低温度のピークから 2 桁下
    if nu_max is None:
        nu_max = _NU_PEAK_PER_T * max(temperatures) * 1e2  # 最高温度のピークから 2 桁上

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    else:
        fig = ax.figure

    nu = np.logspace(np.log10(nu_min), np.log10(nu_max), npts)

    # プランク曲線
    y_max = 0.0
    for T in temperatures:
        B = planck_nu(nu, T)
        ax.loglog(nu, B, label=f"T = {T:g} K", lw=1.8)
        m = B[B > 0]
        if m.size:
            y_max = max(y_max, m.max())

    # 古典極限
    if show_limits is None:
        show_limits = len(temperatures) <= 3
    if show_limits:
        T_ref = temperatures[len(temperatures) // 2]
        ax.loglog(
            nu, rayleigh_jeans_nu(nu, T_ref),
            "--", color="gray", alpha=0.6,
            label=f"Rayleigh-Jeans (T={T_ref:g} K)",
        )
        ax.loglog(
            nu, wien_nu(nu, T_ref),
            ":", color="black", alpha=0.6,
            label=f"Wien (T={T_ref:g} K)",
        )

    # 縦軸範囲を「最大値の 8 桁下まで」に制限（アンダーフロー領域は無視）
    if y_max > 0:
        ax.set_ylim(y_max * 1e-8, y_max * 10)
    ax.set_xlim(nu_min, nu_max)

    # ラベル：日本語フォントが使えるなら日本語、なければ英語
    jp = use_japanese if use_japanese is not None else (_JP_FONT is not None)
    if jp:
        ax.set_xlabel(r"振動数 $\nu$ [Hz]")
        ax.set_ylabel(r"比強度 $B_\nu$ [erg s$^{-1}$ cm$^{-2}$ Hz$^{-1}$ sr$^{-1}$]")
        ax.set_title(r"プランク関数 $B_\nu(T)$")
    else:
        ax.set_xlabel(r"Frequency $\nu$ [Hz]")
        ax.set_ylabel(r"$B_\nu$ [erg s$^{-1}$ cm$^{-2}$ Hz$^{-1}$ sr$^{-1}$]")
        ax.set_title(r"Planck function $B_\nu(T)$")

    ax.legend(loc="lower center", fontsize=9, framealpha=0.9, ncol=2)
    ax.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    return fig, ax


if __name__ == "__main__":
    # 第 1 章の図と同じ温度組（4 桁の温度範囲）
    fig, ax = plot_planck_with_limits(temperatures=(2.7, 310, 3000, 5800))
    plt.show()
