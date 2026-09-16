"""
Generate dummy reference signal plots for Modul 5 (Filtering & PID).

Bukan data hasil pengukuran alat sungguhan -- hanya sinyal buatan (simulasi)
untuk memberi gambaran bentuk grafik yang diharapkan praktikan di Serial
Plotter. Jalankan ulang skrip ini jika ingin memperbarui gambar di img/.

Usage:
    python scripts/generate_modul5_signals.py
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "img")
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams.update(
    {
        "font.size": 11,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "figure.dpi": 150,
    }
)

rng = np.random.default_rng(42)


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {path}")


def alpha_filter(raw, alpha):
    out = np.empty_like(raw)
    out[0] = raw[0]
    for i in range(1, len(raw)):
        out[i] = alpha * out[i - 1] + (1 - alpha) * raw[i]
    return out


# ---------------------------------------------------------------------------
# Gambar 1 (teori C.1): sinyal quadrature encoder Channel A & Channel B
# ---------------------------------------------------------------------------
def plot_quadrature_encoder():
    t = np.linspace(0, 8, 4000)
    period = 1.0  # satu siklus A/B per 1 satuan waktu
    a = (np.mod(t, period) < period / 2).astype(float)
    # Channel B tertinggal 90 derajat (seperempat periode) dari Channel A
    b = (np.mod(t - period / 4, period) < period / 2).astype(float)

    fig, axes = plt.subplots(2, 1, figsize=(8, 3.6), sharex=True)
    axes[0].step(t, a + 2.2, where="post", color="#d62728", linewidth=1.6)
    axes[0].set_yticks([2.2, 3.2])
    axes[0].set_yticklabels(["LOW", "HIGH"])
    axes[0].set_ylabel("Channel A", rotation=0, ha="right", va="center")

    axes[1].step(t, b, where="post", color="#1f77b4", linewidth=1.6)
    axes[1].set_yticks([0, 1])
    axes[1].set_yticklabels(["LOW", "HIGH"])
    axes[1].set_ylabel("Channel B", rotation=0, ha="right", va="center")
    axes[1].set_xlabel("waktu")

    for i in range(3):
        axes[0].axvline(i * period + period / 4, color="gray", ls=":", lw=0.8)

    axes[0].annotate(
        "rising edge Channel A dipakai\nsebagai trigger interrupt",
        xy=(period, 3.2),
        xytext=(period + 1.4, 2.9),
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", lw=0.8),
    )
    axes[1].annotate(
        "Channel B dibaca saat interrupt\nuntuk menentukan arah putar",
        xy=(period / 4, 1.0),
        xytext=(period + 1.4, 1.3),
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", lw=0.8),
    )

    fig.suptitle("Sinyal Quadrature Encoder — Channel A & Channel B", y=1.06)
    save(fig, "diagram_quadrature_encoder.png")


# ---------------------------------------------------------------------------
# Gambar 2 (teori C.2) & Gambar 8 (Percobaan 2): RPM mentah vs filter alpha
# ---------------------------------------------------------------------------
def make_noisy_rpm(n=400, base=100.0, noise_std=6.0, step_at=None, step_to=None):
    t = np.arange(n)
    signal = np.full(n, base, dtype=float)
    if step_at is not None:
        signal[step_at:] = step_to
    # noise + sedikit ripple periodik supaya terlihat "sinyal nyata"
    noise = rng.normal(0, noise_std, n)
    ripple = 2.5 * np.sin(t / 3.3)
    return t, signal + noise + ripple


def plot_alpha_theory():
    t, raw = make_noisy_rpm(n=300, base=100.0, noise_std=7.0)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(t, raw, color="#bbbbbb", linewidth=1, label="RPM Mentah (noisy)")
    for alpha, color in [(0.3, "#2ca02c"), (0.7, "#1f77b4"), (0.9, "#d62728")]:
        ax.plot(t, alpha_filter(raw, alpha), color=color, linewidth=2, label=f"Filter Alpha (α={alpha})")
    ax.set_xlabel("sample ke-n")
    ax.set_ylabel("RPM")
    ax.set_title("Perbandingan Filter Alpha pada Beberapa Nilai α")
    ax.legend(loc="upper right", fontsize=9)
    save(fig, "grafik_filter_alpha.png")


def plot_alpha_percobaan2():
    t, raw = make_noisy_rpm(n=250, base=100.0, noise_std=6.5)
    filtered = alpha_filter(raw, 0.7)
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(t, raw, color="#d62728", linewidth=1, label="RPM_Mentah")
    ax.plot(t, filtered, color="#1f77b4", linewidth=2, label="RPM_Alpha (α=0.7)")
    ax.set_xlabel("sample ke-n")
    ax.set_ylabel("RPM")
    ax.set_title("Contoh Tampilan Serial Plotter — RPM_Mentah vs RPM_Alpha")
    ax.legend(loc="upper right", fontsize=9)
    save(fig, "plot_filter_alpha_contoh.png")


# ---------------------------------------------------------------------------
# Gambar 9 (Percobaan 3): RPM Mentah vs Alpha vs Kalman
# ---------------------------------------------------------------------------
def kalman_1d(raw, q=0.001, r=0.1):
    n = len(raw)
    x = np.empty(n)
    p = 1.0
    x[0] = raw[0]
    for i in range(1, n):
        # predict
        x_pred = x[i - 1]
        p_pred = p + q
        # update
        k = p_pred / (p_pred + r)
        x[i] = x_pred + k * (raw[i] - x_pred)
        p = (1 - k) * p_pred
    return x


def plot_kalman_contoh():
    t, raw = make_noisy_rpm(n=250, base=100.0, noise_std=6.5)
    alpha_out = alpha_filter(raw, 0.7)
    kalman_out = kalman_1d(raw, q=0.05, r=4.0)

    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(t, raw, color="#bbbbbb", linewidth=1, label="RPM_Mentah")
    ax.plot(t, alpha_out, color="#2ca02c", linewidth=2, label="RPM_Alpha")
    ax.plot(t, kalman_out, color="#1f77b4", linewidth=2, label="RPM_Kalman")
    ax.set_xlabel("sample ke-n")
    ax.set_ylabel("RPM")
    ax.set_title("Contoh Tampilan Serial Plotter — RPM_Mentah vs RPM_Alpha vs RPM_Kalman")
    ax.legend(loc="upper right", fontsize=9)
    save(fig, "plot_filter_kalman_contoh.png")


# ---------------------------------------------------------------------------
# Gambar 11 (Percobaan 4): mode On-Off vs Proportional
# ---------------------------------------------------------------------------
def plot_onoff_vs_p():
    t = np.arange(0, 300)
    target = 100.0

    # On-off: berosilasi terus-menerus di sekitar target
    onoff = target + 8 * np.sign(np.sin(t / 6.0)) + rng.normal(0, 1.2, len(t))

    # Proportional: naik menuju target lalu menetap dengan steady-state error
    p_response = target - 25 * np.exp(-t / 40.0) - 6  # -6 = steady-state error
    p_response += rng.normal(0, 1.0, len(t))

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)

    axes[0].plot(t, onoff, color="#d62728", linewidth=1.2)
    axes[0].axhline(target, color="black", ls="--", lw=1, label="Target RPM")
    axes[0].set_title("Mode On-Off (berosilasi)")
    axes[0].set_xlabel("waktu (sample)")
    axes[0].set_ylabel("RPM")
    axes[0].legend(fontsize=8, loc="lower right")

    axes[1].plot(t, p_response, color="#1f77b4", linewidth=1.4)
    axes[1].axhline(target, color="black", ls="--", lw=1, label="Target RPM")
    axes[1].set_title("Mode Proportional (steady-state error)")
    axes[1].set_xlabel("waktu (sample)")
    axes[1].legend(fontsize=8, loc="lower right")

    fig.suptitle("Perbandingan Respons Mode On-Off vs Proportional (P)", y=1.03)
    save(fig, "plot_onoff_vs_p_contoh.png")


# ---------------------------------------------------------------------------
# Gambar 13 (Percobaan 5): respons sebelum vs sesudah tuning PID
# ---------------------------------------------------------------------------
def plot_pid_tuning():
    t = np.arange(0, 300)
    target = 100.0

    # Sebelum tuning: naik cepat, overshoot besar, lalu berosilasi lambat meredam
    before = target * (1 - np.exp(-t / 25.0)) + 45 * np.exp(-t / 70.0) * np.cos(t / 18.0)
    before += rng.normal(0, 1.5, len(t))

    # Sesudah tuning: naik cepat, overshoot kecil, cepat stabil
    after = target * (1 - np.exp(-t / 20.0)) + 6 * np.exp(-t / 18.0) * np.cos(t / 9.0)
    after += rng.normal(0, 1.0, len(t))

    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(t, before, color="#d62728", linewidth=1.3, label="Sebelum Tuning")
    ax.plot(t, after, color="#1f77b4", linewidth=1.6, label="Sesudah Tuning")
    ax.axhline(target, color="black", ls="--", lw=1, label="Target RPM")
    ax.set_xlabel("waktu (sample)")
    ax.set_ylabel("RPM")
    ax.set_title("Respons Kontrol PID — Sebelum vs Sesudah Tuning")
    ax.legend(fontsize=9)
    save(fig, "plot_pid_sebelum_sesudah_tuning.png")


if __name__ == "__main__":
    plot_quadrature_encoder()
    plot_alpha_theory()
    plot_alpha_percobaan2()
    plot_kalman_contoh()
    plot_onoff_vs_p()
    plot_pid_tuning()
