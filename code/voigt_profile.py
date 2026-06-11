"""
voigt-profile.py — 自然線形・ドップラー線形・Voigt 線形

第22章「線形（line shape）の物理」で使う。
自然幅 → ドップラー → 圧力 → Voigt の順に逆引きで構築する。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")  # PDF backend を回避（CJK フォント名のASCIIエンコード問題を避ける）
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
import matplotlib.pyplot as plt
from scipy.special import wofz


def lorentz(nu, nu0, gamma):
    """自然線形（Lorentz型）"""
    return (gamma / np.pi) / ((nu - nu0)**2 + gamma**2)


def gaussian(nu, nu0, sigma):
    """ドップラー線形（Gauss型）"""
    return (1.0 / (sigma * np.sqrt(2.0 * np.pi))) * \
           np.exp(-((nu - nu0)**2) / (2 * sigma**2))


def voigt(nu, nu0, sigma, gamma):
    """Voigt 線形（自然 + ドップラーの合成）= Re[w(z)] / (sigma sqrt(2pi))"""
    z = ((nu - nu0) + 1j * gamma) / (sigma * np.sqrt(2.0))
    return np.real(wofz(z)) / (sigma * np.sqrt(2.0 * np.pi))


def plot_voigt_decomposition(nu0=1.0, sigma=0.3, gamma=0.3, span=3.0, npts=600):
    """
    Lorentz, Gauss, Voigt を同じ軸に描いて、
    Voigt が両者の合成であることを視覚化する。
    """
    nu = np.linspace(nu0 - span, nu0 + span, npts)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(nu, lorentz(nu, nu0, gamma), "--",
            label=f"Lorentz (γ={gamma})")
    ax.plot(nu, gaussian(nu, nu0, sigma), ":",
            label=f"Gauss (σ={sigma})")
    ax.plot(nu, voigt(nu, nu0, sigma, gamma), "-", lw=2,
            label="Voigt (合成)")

    ax.axvline(nu0, color="gray", lw=0.5, alpha=0.5)
    ax.set_xlabel(r"$\nu - \nu_0$")
    ax.set_ylabel(r"線形 $\phi(\nu - \nu_0)$")
    ax.set_title("線形の三層構造：Lorentz × Gauss = Voigt")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig, ax


if __name__ == "__main__":
    fig, ax = plot_voigt_decomposition()
    plt.show()
