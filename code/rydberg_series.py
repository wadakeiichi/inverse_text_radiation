"""
rydberg-series.py — 水素のリュードベリ系列（Lyman, Balmer, Paschen, Brackett）

第19章・第21章で使う。リュードベリ公式から線位置を計算し、
天文観測でよく出会う Lyα・Hα・21cm との対応を見せる。
"""
import numpy as np
import matplotlib.pyplot as plt
from astropy import constants as const
from astropy import units as u

# Rydberg 定数（水素、波長系で R_H = m_e e^4 / (8 ε_0^2 h^3 c)）
R_H = const.Ryd.to(1 / u.cm).value  # 1/cm


def rydberg_wavelength_cm(n1, n2):
    """1/λ = R_H (1/n1^2 - 1/n2^2), n2 > n1 で光子放出"""
    inv_lambda = R_H * (1.0 / n1**2 - 1.0 / n2**2)
    return 1.0 / inv_lambda


def series(n1, max_n2=10):
    """系列の波長を返す（cm単位）"""
    return np.array([rydberg_wavelength_cm(n1, n2) for n2 in range(n1 + 1, max_n2 + 1)])


def print_series_table():
    series_info = [
        (1, "Lyman", "紫外"),
        (2, "Balmer", "可視"),
        (3, "Paschen", "近赤外"),
        (4, "Brackett", "中赤外"),
    ]
    print(f"{'系列':<10} {'n1':>3} {'第一線':>15} {'限界':>15} 領域")
    print("-" * 60)
    for n1, name, region in series_info:
        wls = series(n1, max_n2=20)
        first = wls[0] * 1e7  # cm → nm
        limit = (1.0 / R_H * n1**2) * 1e7  # nm
        print(f"{name:<10} {n1:>3} {first:>15.2f} nm {limit:>12.2f} nm  {region}")


def plot_series_lines():
    """各系列の線を波長軸上に並べる"""
    series_info = [
        (1, "Lyman", "tab:purple"),
        (2, "Balmer", "tab:red"),
        (3, "Paschen", "tab:orange"),
        (4, "Brackett", "tab:brown"),
    ]
    fig, ax = plt.subplots(figsize=(9, 3.5))
    for n1, name, color in series_info:
        wls = series(n1, max_n2=15) * 1e7  # nm
        for w in wls:
            ax.axvline(w, color=color, lw=0.8, alpha=0.7)
        ax.text(wls[0], n1, name, color=color, fontsize=9, ha="left", va="bottom")

    ax.set_xscale("log")
    ax.set_xlabel("波長 [nm]")
    ax.set_yticks([1, 2, 3, 4])
    ax.set_yticklabels(["Lyman", "Balmer", "Paschen", "Brackett"])
    ax.set_xlim(80, 5e4)
    ax.set_title("水素のリュードベリ系列：Lyα は宇宙の高赤方偏移天文学を、Hα は星形成と AGN を支える")
    ax.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    return fig, ax


if __name__ == "__main__":
    print_series_table()
    fig, ax = plot_series_lines()
    plt.show()
