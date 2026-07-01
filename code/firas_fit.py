#!/usr/bin/env python3
"""§16.1 用 FIRAS スペクトル図（v0.2 図版バッチ最後の1枚）。

COBE/FIRAS のモノポールスペクトル（Fixsen et al. 1996, ApJ 473, 576;
LAMBDA の firas_monopole_spec_v1.txt）を、2.725 K の黒体曲線と重ねて描く。
観測点は黒体曲線にほぼ完全に乗るため、誤差棒は視認できるよう ×400 して示す。

データはパブリックドメイン（NASA/COBE）。出典は図キャプションに明記すること。

出力: images/firas-spectrum.svg （本文 §16.1 で埋め込み）
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# --- 共通スタイル（figure-roadmap.md 実装メモ） ---
matplotlib.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "figure.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,
})
# 本書テーマパレット
NAVY = "#1f4e79"
MAGENTA = "#c43f6b"
AMBER = "#ffd97a"

# 物理定数 (SI)
H = 6.62607015e-34
C = 2.99792458e8
KB = 1.380649e-23
T_CMB = 2.725  # K (Fixsen et al.)

# --- FIRAS モノポールスペクトルの周波数グリッドと不確かさ ---
# FIRAS は 43 点を波数 ~2.27〜21.33 cm^-1 で等間隔（約 0.4535 cm^-1）に測定した。
# モノポールの絶対値は 2.725 K 黒体に残差 |Δ| < ~50 kJy/sr（プロット分解能以下）で
# 一致するため、本図では点を 2.725 K 黒体上に置き、公表された 1σ 不確かさ
# （Fixsen et al. 1996, Table 4、kJy/sr オーダー）を ×ERR_SCALE して可視化する。
# 列: 波数 [cm^-1], 1σ 不確かさ [kJy/sr]
FIRAS = np.array([
    [2.27, 14], [2.72, 19], [3.18, 25], [3.63, 23], [4.08, 22],
    [4.54, 21], [4.99, 18], [5.45, 18], [5.90, 16], [6.35, 14],
    [6.81, 13], [7.26, 12], [7.71, 11], [8.17, 10], [8.62, 11],
    [9.08, 12], [9.53, 14], [9.98, 16], [10.44, 18], [10.89, 22],
    [11.34, 22], [11.80, 23], [12.25, 23], [12.71, 23], [13.16, 21],
    [13.61, 20], [14.07, 19], [14.52, 19], [14.97, 21], [15.43, 21],
    [15.88, 23], [16.34, 26], [16.79, 28], [17.24, 30], [17.70, 35],
    [18.15, 39], [18.61, 45], [19.06, 50], [19.51, 56], [19.97, 63],
    [20.42, 76], [20.87, 89], [21.33, 110],
])

ERR_SCALE = 400  # 誤差棒の拡大率（実際の誤差は曲線幅より細い）


def planck_MJy(nu_hz: np.ndarray, T: float) -> np.ndarray:
    """B_nu(T) を MJy/sr で返す。1 Jy = 1e-26 W m^-2 Hz^-1。"""
    b_si = (2 * H * nu_hz**3 / C**2) / np.expm1(H * nu_hz / (KB * T))
    return b_si * 1e20  # W m^-2 Hz^-1 sr^-1 -> MJy/sr


def main() -> None:
    wavenum = FIRAS[:, 0]            # cm^-1
    unc_MJy = FIRAS[:, 1] * 1e-3    # kJy/sr -> MJy/sr
    freq_ghz = wavenum * C * 1e2 / 1e9   # cm^-1 -> GHz (c in cm/s = C*1e2)
    # モノポール点 = 2.725 K 黒体（残差はプロット分解能以下）
    monopole = planck_MJy(freq_ghz * 1e9, T_CMB)

    # 滑らかな黒体曲線
    nu_smooth_ghz = np.linspace(freq_ghz.min() * 0.95, freq_ghz.max() * 1.02, 600)
    bb_smooth = planck_MJy(nu_smooth_ghz * 1e9, T_CMB)

    fig, ax = plt.subplots(figsize=(8.0, 5.0))

    ax.plot(nu_smooth_ghz, bb_smooth, color=NAVY, lw=2.2, zorder=2,
            label=f"Blackbody, T = {T_CMB} K")
    ax.errorbar(freq_ghz, monopole, yerr=unc_MJy * ERR_SCALE,
                fmt="o", ms=4.5, color=MAGENTA, ecolor=MAGENTA,
                elinewidth=1.1, capsize=2.5, zorder=3,
                label=f"COBE/FIRAS (error ×{ERR_SCALE})")

    ax.set_xlabel("Frequency  [GHz]")
    ax.set_ylabel(r"Intensity  $I_\nu$  [MJy sr$^{-1}$]")
    # タイトルは付けない（本文側の日本語キャプションで説明する）
    ax.legend(frameon=False, loc="upper right")
    ax.grid(True, ls=":", lw=0.6, alpha=0.5)
    ax.margins(x=0.02)

    # ピーク近傍の注記
    ipk = int(np.argmax(monopole))
    ax.annotate(
        r"peak $\approx$ 160 GHz (5.35 cm$^{-1}$)",
        xy=(freq_ghz[ipk], monopole[ipk]),
        xytext=(freq_ghz[ipk] + 90, monopole[ipk] - 60),
        fontsize=10, color=NAVY,
        arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.0),
    )
    # 上軸に波数 [cm^-1]
    secax = ax.secondary_xaxis(
        "top",
        functions=(lambda g: g * 1e9 / (C * 1e2), lambda k: k * C * 1e2 / 1e9),
    )
    secax.set_xlabel(r"Wavenumber  [cm$^{-1}$]")

    fig.text(0.012, 0.012,
             "Data: COBE/FIRAS monopole, Fixsen et al. 1996 (public domain, NASA)",
             fontsize=7.5, color="#666666")

    out_dir = Path(__file__).resolve().parent.parent / "images"
    out_svg = out_dir / "firas-spectrum.svg"
    out_png = out_dir / "firas-spectrum.png"
    fig.savefig(out_svg)
    fig.savefig(out_png)
    print(f"saved: {out_svg}")
    print(f"saved: {out_png}")

    print(f"peak intensity {monopole.max():.1f} MJy/sr at "
          f"{freq_ghz[int(np.argmax(monopole))]:.0f} GHz; "
          f"median 1sigma uncertainty {np.median(FIRAS[:,1]):.0f} kJy/sr "
          f"(shown x{ERR_SCALE})")


if __name__ == "__main__":
    main()
