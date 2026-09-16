"""
Generate dummy/ilustratif theory diagrams for Modul 1, 2, and 4
(bukan hasil pengukuran alat sungguhan -- ilustrasi konsep saja).

Usage:
    python scripts/generate_theory_diagrams.py
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "img")
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams.update(
    {
        "font.size": 11,
        "figure.dpi": 150,
    }
)

rng = np.random.default_rng(7)


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {path}")


def box(ax, xy, w, h, text, fc="#cfe8ff", ec="#1f4e8c", fontsize=10.5):
    b = FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.4,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(b)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fontsize, wrap=True)
    return b


def arrow(ax, start, end, text=None, color="#333333", connectionstyle="arc3,rad=0.0", lw=1.6):
    a = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=lw,
        color=color,
        connectionstyle=connectionstyle,
    )
    ax.add_patch(a)
    if text:
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        ax.text(mx, my, text, ha="center", va="bottom", fontsize=8.5, color=color)


# ---------------------------------------------------------------------------
# Modul 1 — Gambar: bouncing vs debounce
# ---------------------------------------------------------------------------
def plot_bouncing_debounce():
    fs = 4000  # sample points per ms unit for smooth steps
    t = np.linspace(0, 40, fs)

    def bounce_signal(t, press_at, release_at, bounce_ms=3.5, n_bounces=6):
        sig = np.ones_like(t)  # idle HIGH (pull-up)
        # press: bounce down to LOW before settling
        for i in range(n_bounces):
            edge = press_at + i * (bounce_ms / n_bounces)
            sig[t >= edge] = 0 if i % 2 == 0 else 1
        sig[t >= press_at + bounce_ms] = 0
        # release: bounce back up to HIGH before settling
        for i in range(n_bounces):
            edge = release_at + i * (bounce_ms / n_bounces)
            sig[t >= edge] = 1 if i % 2 == 0 else 0
        sig[t >= release_at + bounce_ms] = 1
        return sig

    raw = bounce_signal(t, press_at=8, release_at=25)
    debounced = np.ones_like(t)
    debounced[(t >= 8 + 3.5) & (t < 25 + 3.5)] = 0

    fig, axes = plt.subplots(2, 1, figsize=(8.5, 4), sharex=True)
    axes[0].step(t, raw, where="post", color="#d62728", linewidth=1.3)
    axes[0].set_title("Sinyal Mentah — Bouncing Saat Tombol Ditekan & Dilepas", fontsize=10.5)
    axes[0].set_yticks([0, 1])
    axes[0].set_yticklabels(["LOW", "HIGH"])
    axes[0].set_ylim(-0.3, 1.3)

    axes[1].step(t, debounced, where="post", color="#1f77b4", linewidth=1.8)
    axes[1].set_title("Sinyal Setelah Debounce — Satu Transisi Bersih", fontsize=10.5)
    axes[1].set_yticks([0, 1])
    axes[1].set_yticklabels(["LOW", "HIGH"])
    axes[1].set_ylim(-0.3, 1.3)
    axes[1].set_xlabel("waktu (ms)")

    for ax in axes:
        ax.axvline(8, color="gray", ls=":", lw=0.8)
        ax.axvline(25, color="gray", ls=":", lw=0.8)
    axes[0].text(8, 1.18, "tekan", fontsize=8, ha="center", color="gray")
    axes[0].text(25, 1.18, "lepas", fontsize=8, ha="center", color="gray")

    fig.suptitle("Bouncing vs Debounce pada Sinyal Tombol Mekanik", y=1.0)
    fig.tight_layout()
    save(fig, "grafik_bouncing_debounce.png")


# ---------------------------------------------------------------------------
# Modul 1 — Gambar: skematik pull-up vs pull-down (konsep)
# ---------------------------------------------------------------------------
def draw_resistor(ax, x, y_bottom, y_top, n_zigzag=6, width=0.12, color="#333333"):
    ys = np.linspace(y_bottom, y_top, n_zigzag * 2 + 1)
    xs = [x]
    for i in range(1, len(ys) - 1):
        xs.append(x + (width if i % 2 == 1 else -width))
    xs.append(x)
    ax.plot(xs, ys, color=color, linewidth=1.6)


def draw_switch(ax, x, y_bottom, y_top, color="#333333"):
    ax.plot([x, x], [y_bottom, y_bottom + (y_top - y_bottom) * 0.28], color=color, linewidth=1.6)
    ax.plot([x, x], [y_top - (y_top - y_bottom) * 0.28, y_top], color=color, linewidth=1.6)
    ax.plot(
        [x, x + 0.18],
        [y_bottom + (y_top - y_bottom) * 0.28, y_top - (y_top - y_bottom) * 0.35],
        color=color,
        linewidth=1.6,
    )
    ax.plot(x, y_bottom + (y_top - y_bottom) * 0.28, "o", color=color, markersize=3)
    ax.plot(x, y_top - (y_top - y_bottom) * 0.28, "o", color=color, markersize=3)


def plot_pullup_pulldown_concept():
    fig, axes = plt.subplots(1, 2, figsize=(9, 5))

    # --- Pull-up ---
    ax = axes[0]
    ax.set_title("Pull-Up Resistor", fontsize=12, fontweight="bold")
    ax.plot([0, 0], [0, 4], color="#333333", linewidth=1.6)  # vertical rail
    draw_resistor(ax, 0, 2.6, 4)
    draw_switch(ax, 0, 0, 2.2)
    ax.plot([0, 1.2], [2.3, 2.3], color="#1f77b4", linewidth=2)  # tap to GPIO
    ax.text(1.3, 2.3, "GPIO\n(baca HIGH)", fontsize=9, va="center", color="#1f77b4")
    ax.text(0, 4.15, "VCC (3.3V)", ha="center", fontsize=10, fontweight="bold")
    ax.text(0, -0.35, "GND", ha="center", fontsize=10, fontweight="bold")
    ax.text(-0.55, 1.1, "tombol", fontsize=9, ha="center", color="gray")
    ax.text(0.35, 3.3, "R", fontsize=10, color="gray")
    ax.text(0, -1.0, "Idle: HIGH (ditarik ke VCC)\nDitekan: LOW (terhubung ke GND)", ha="center", fontsize=9)

    # --- Pull-down ---
    ax = axes[1]
    ax.set_title("Pull-Down Resistor", fontsize=12, fontweight="bold")
    ax.plot([0, 0], [0, 4], color="#333333", linewidth=1.6)
    draw_resistor(ax, 0, 0, 1.4)
    draw_switch(ax, 0, 1.8, 4)
    ax.plot([0, 1.2], [1.7, 1.7], color="#d62728", linewidth=2)
    ax.text(1.3, 1.7, "GPIO\n(baca LOW)", fontsize=9, va="center", color="#d62728")
    ax.text(0, 4.15, "VCC (3.3V)", ha="center", fontsize=10, fontweight="bold")
    ax.text(0, -0.35, "GND", ha="center", fontsize=10, fontweight="bold")
    ax.text(-0.55, 2.9, "tombol", fontsize=9, ha="center", color="gray")
    ax.text(0.35, 0.7, "R", fontsize=10, color="gray")
    ax.text(0, -1.0, "Idle: LOW (ditarik ke GND)\nDitekan: HIGH (terhubung ke VCC)", ha="center", fontsize=9)

    for ax in axes:
        ax.set_xlim(-1.6, 2.6)
        ax.set_ylim(-1.6, 4.6)
        ax.axis("off")

    fig.suptitle("Konsep Rangkaian Pull-Up vs Pull-Down Resistor", y=1.02, fontsize=13)
    fig.tight_layout()
    save(fig, "skematik_pullup_pulldown.png")


# ---------------------------------------------------------------------------
# Modul 2 — Gambar: PWM duty cycle
# ---------------------------------------------------------------------------
def plot_pwm_duty_cycle():
    t = np.linspace(0, 4, 4000)  # 4 periode
    period = 1.0

    fig, axes = plt.subplots(3, 1, figsize=(8.5, 5), sharex=True)
    for ax, duty, color in zip(axes, [0.25, 0.5, 0.75], ["#2ca02c", "#1f77b4", "#d62728"]):
        sig = (np.mod(t, period) < period * duty).astype(float)
        ax.step(t, sig, where="post", color=color, linewidth=1.6)
        ax.axhline(duty, color="black", ls="--", lw=1)
        ax.set_yticks([0, duty, 1])
        ax.set_yticklabels(["0V", f"{duty*100:.0f}%\n(avg)", "3.3V"], fontsize=8)
        ax.set_title(f"Duty Cycle {duty*100:.0f}%", fontsize=10.5)
        ax.set_ylim(-0.15, 1.25)

    axes[-1].set_xlabel("waktu (periode)")
    fig.suptitle("Sinyal PWM pada Beberapa Nilai Duty Cycle", y=1.0)
    fig.tight_layout()
    save(fig, "grafik_pwm_duty_cycle.png")


# ---------------------------------------------------------------------------
# Modul 2 — Gambar: diagram pulsa servo
# ---------------------------------------------------------------------------
def plot_servo_pulse_diagram():
    period_ms = 20
    pulses = [(1.0, "0°"), (1.5, "90°"), (2.0, "180°")]

    fig, axes = plt.subplots(3, 1, figsize=(9, 4.6), sharex=True)
    for ax, (pulse_ms, angle) in zip(axes, pulses):
        t = np.linspace(0, period_ms * 1.4, 3000)
        sig = np.zeros_like(t)
        for k in range(2):
            start = k * period_ms
            sig[(t >= start) & (t < start + pulse_ms)] = 1
        ax.step(t, sig, where="post", color="#1f77b4", linewidth=1.6)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["LOW", "HIGH"])
        ax.set_title(f"Sudut {angle} — Lebar Pulsa {pulse_ms:.1f} ms (periode {period_ms} ms)", fontsize=10)
        ax.axvspan(0, pulse_ms, color="#1f77b4", alpha=0.12)
        ax.set_ylim(-0.3, 1.3)

    axes[-1].set_xlabel("waktu (ms)")
    fig.suptitle("Lebar Pulsa Sinyal Servo vs Sudut yang Dihasilkan", y=1.0)
    fig.tight_layout()
    save(fig, "diagram_pulsa_servo.png")


# ---------------------------------------------------------------------------
# Modul 2 — Gambar: blok ESC + motor brushless
# ---------------------------------------------------------------------------
def plot_esc_brushless_block():
    fig, ax = plt.subplots(figsize=(9, 3.6))

    box(ax, (0, 1), 2.0, 1.0, "ESP32\n(sinyal PWM)")
    box(ax, (3.3, 1), 2.0, 1.0, "ESC\n(Electronic Speed\nController)", fc="#ffe4b3", ec="#a3670a")
    box(ax, (6.6, 1), 2.0, 1.0, "Motor Brushless\n(BLDC)", fc="#d6f5d6", ec="#2e7d32")
    box(ax, (3.3, -0.7), 2.0, 1.0, "Baterai LiPo\n(2S–3S)", fc="#ffd6d6", ec="#a31515")

    arrow(ax, (2.0, 1.5), (3.3, 1.5), "sinyal PWM\n(1000–2000µs)")
    arrow(ax, (5.3, 1.5), (6.6, 1.5), "3-fasa")
    arrow(ax, (4.3, 0.3), (4.3, 1.0), "daya utama")

    ax.set_xlim(-0.5, 9)
    ax.set_ylim(-1.2, 2.3)
    ax.axis("off")
    ax.set_title("Diagram Blok Kontrol ESC & Motor Brushless (BLDC)", fontsize=12)
    fig.tight_layout()
    save(fig, "wiring_esc_brushless.png")


# ---------------------------------------------------------------------------
# Modul 4 — Gambar: alur eksekusi program utama vs ISR
# ---------------------------------------------------------------------------
def plot_isr_flow():
    fig, ax = plt.subplots(figsize=(9, 2.8))

    ax.broken_barh([(0, 10)], (2, 1), facecolors="#cfe8ff", edgecolor="#1f4e8c")
    ax.broken_barh([(4, 1.2)], (2, 1), facecolors="#ffcccc", edgecolor="#a31515")
    ax.text(2, 2.5, "Program Utama\nberjalan", ha="center", va="center", fontsize=9)
    ax.text(4.6, 2.5, "ISR", ha="center", va="center", fontsize=9, fontweight="bold")
    ax.text(7.5, 2.5, "Program Utama\nlanjut", ha="center", va="center", fontsize=9)

    ax.annotate(
        "interrupt terjadi\n(mis. tombol ditekan)",
        xy=(4, 3.3),
        xytext=(2.3, 4.0),
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", lw=1),
    )
    ax.annotate(
        "ISR selesai,\nkembali ke titik semula",
        xy=(5.2, 3.3),
        xytext=(6.0, 4.0),
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", lw=1),
    )

    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(1.5, 4.6)
    ax.axis("off")
    ax.set_title("Alur Eksekusi Program Utama yang Dijeda oleh ISR", fontsize=12)
    fig.tight_layout()
    save(fig, "diagram_alur_isr.png")


# ---------------------------------------------------------------------------
# Modul 4 — Gambar: timeline delay() vs timer interrupt
# ---------------------------------------------------------------------------
def plot_delay_vs_timer_timeline():
    fig, axes = plt.subplots(2, 1, figsize=(9, 3.6), sharex=True)

    # delay() blocking: CPU busy penuh selama delay
    ax = axes[0]
    for start in range(0, 10, 2):
        ax.broken_barh([(start, 1.4)], (0, 1), facecolors="#d62728", alpha=0.8)
        ax.broken_barh([(start + 1.4, 0.6)], (0, 1), facecolors="#cfe8ff")
    ax.set_yticks([0.5])
    ax.set_yticklabels(["CPU"])
    ax.set_title("delay() — Blocking: CPU tidak bisa mengerjakan apa pun selama delay", fontsize=10)
    ax.set_ylim(-0.3, 1.6)

    # timer interrupt: CPU singkat lalu bebas
    ax = axes[1]
    for start in range(0, 10, 2):
        ax.broken_barh([(start, 0.25)], (0, 1), facecolors="#d62728", alpha=0.8)
        ax.broken_barh([(start + 0.25, 1.75)], (0, 1), facecolors="#cfe8ff")
    ax.set_yticks([0.5])
    ax.set_yticklabels(["CPU"])
    ax.set_title("Timer Interrupt — Non-blocking: CPU bebas mengerjakan tugas lain di antara interrupt", fontsize=10)
    ax.set_xlabel("waktu")
    ax.set_ylim(-0.3, 1.6)

    legend_elems = [
        Line2D([0], [0], color="#d62728", lw=6, alpha=0.8, label="CPU sibuk"),
        Line2D([0], [0], color="#cfe8ff", lw=6, label="CPU bebas / idle"),
    ]
    fig.legend(handles=legend_elems, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.06), fontsize=9)
    fig.tight_layout()
    save(fig, "timeline_delay_vs_timer.png")


# ---------------------------------------------------------------------------
# Modul 4 — Gambar: watchdog timer
# ---------------------------------------------------------------------------
def plot_watchdog_timer():
    fig, axes = plt.subplots(2, 1, figsize=(9, 3.6), sharex=True)

    ax = axes[0]
    feed_times = [0, 2, 4, 6, 8, 10]
    for ft in feed_times:
        ax.axvline(ft, color="#2ca02c", lw=1.4)
    ax.plot(feed_times, [1] * len(feed_times), "o", color="#2ca02c")
    for ft in feed_times:
        ax.annotate("", xy=(ft, 0.15), xytext=(ft, 0.85), arrowprops=dict(arrowstyle="-", color="#2ca02c", lw=1))
    ax.set_title("Program Normal — Watchdog Rutin \"Diberi Makan\" (Reset Berkala)", fontsize=10.5)
    ax.set_yticks([])
    ax.set_ylim(0, 1.3)

    ax = axes[1]
    feed_times2 = [0, 2, 4]
    for ft in feed_times2:
        ax.axvline(ft, color="#2ca02c", lw=1.4)
    ax.axvspan(4, 7, color="#ffcccc", alpha=0.6)
    ax.axvline(7, color="#d62728", lw=2)
    ax.text(5.5, 0.6, "program hang\n(tidak memberi makan)", ha="center", fontsize=8.5, color="#a31515")
    ax.annotate(
        "watchdog timeout\n→ reset otomatis",
        xy=(7, 1.0),
        xytext=(8.2, 1.1),
        fontsize=8.5,
        color="#a31515",
        arrowprops=dict(arrowstyle="->", color="#a31515", lw=1),
    )
    ax.set_title("Program Hang — Watchdog Timeout Memicu Reset Otomatis", fontsize=10.5)
    ax.set_yticks([])
    ax.set_xlabel("waktu")
    ax.set_ylim(0, 1.3)
    ax.set_xlim(-0.5, 10.5)

    fig.tight_layout()
    save(fig, "diagram_watchdog_timer.png")


# ---------------------------------------------------------------------------
# Modul 4 — Gambar: FreeRTOS dual-core
# ---------------------------------------------------------------------------
def plot_freertos_dualcore():
    fig, ax = plt.subplots(figsize=(8.5, 3.6))

    box(ax, (0, 0.5), 3, 1.4, "Task A\nCore 0\n(mis. baca sensor)", fc="#cfe8ff", ec="#1f4e8c")
    box(ax, (5.5, 0.5), 3, 1.4, "Task B\nCore 1\n(mis. kontrol motor)", fc="#d6f5d6", ec="#2e7d32")
    box(ax, (3.15, 0.75), 2.2, 0.9, "Queue", fc="#fff3cf", ec="#a3670a", fontsize=10)

    arrow(ax, (3.0, 1.2), (3.15, 1.2), text="xQueueSend", color="#1f4e8c")
    arrow(ax, (5.35, 1.2), (5.5, 1.2), text="xQueueReceive", color="#2e7d32")

    ax.set_xlim(-0.5, 9)
    ax.set_ylim(0, 2.3)
    ax.axis("off")
    ax.set_title("Dua Task FreeRTOS pada Core 0 & Core 1, Berkomunikasi via Queue", fontsize=12)
    fig.tight_layout()
    save(fig, "diagram_freertos_dualcore.png")


# ---------------------------------------------------------------------------
# Modul 3 — Gambar: blocking vs DMA
# ---------------------------------------------------------------------------
def plot_blocking_vs_dma():
    fig = plt.figure(figsize=(11, 6.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.4, 1], hspace=0.55, wspace=0.25)

    # --- Panel kiri atas: blocking ---
    ax = fig.add_subplot(gs[0, 0])
    box(ax, (0, 1.6), 2.2, 1.2, "CPU", fc="#cfe8ff", ec="#1f4e8c")
    box(ax, (5, 1.6), 2.2, 1.2, "Peripheral\n(mis. SPI)", fc="#d6f5d6", ec="#2e7d32")
    for i, y in enumerate([2.5, 2.1, 1.7]):
        arrow(ax, (2.2, y), (5.0, y), color="#a31515" if i == 1 else "#333333", lw=1.3)
    ax.text(3.6, 2.9, "CPU minta & menunggu\nbyte demi byte", ha="center", fontsize=8.5, color="#a31515")
    ax.set_xlim(-0.5, 7.7)
    ax.set_ylim(1.3, 3.3)
    ax.axis("off")
    ax.set_title("Blocking — CPU Menangani Tiap Byte", fontsize=11.5, fontweight="bold")

    # --- Panel kanan atas: DMA ---
    ax = fig.add_subplot(gs[0, 1])
    box(ax, (0, 1.6), 2.0, 1.2, "CPU", fc="#cfe8ff", ec="#1f4e8c")
    box(ax, (2.9, 1.6), 2.2, 1.2, "DMA\nController", fc="#fff3cf", ec="#a3670a")
    box(ax, (6.7, 1.6), 2.0, 1.2, "Peripheral", fc="#d6f5d6", ec="#2e7d32")
    arrow(ax, (2.0, 2.35), (2.9, 2.35), text="trigger\n(1x saja)", color="#1f4e8c")
    arrow(ax, (5.1, 2.2), (6.7, 2.2), text="semua byte", color="#a3670a")
    arrow(ax, (2.9, 1.9), (2.0, 1.9), text="selesai (interrupt)", color="#2e7d32")
    ax.set_xlim(-0.5, 9.1)
    ax.set_ylim(1.2, 3.3)
    ax.axis("off")
    ax.set_title("DMA — Hardware Menangani Transfer", fontsize=11.5, fontweight="bold")

    # --- Panel bawah: timeline perbandingan ---
    ax = fig.add_subplot(gs[1, 0])
    for start in range(0, 10, 2):
        ax.broken_barh([(start, 1.5)], (0, 1), facecolors="#d62728", alpha=0.85)
        ax.broken_barh([(start + 1.5, 0.5)], (0, 1), facecolors="#cfe8ff")
    ax.set_yticks([0.5])
    ax.set_yticklabels(["CPU"])
    ax.set_xlabel("waktu")
    ax.set_ylim(-0.3, 1.5)
    ax.set_title("CPU sibuk sepanjang transfer", fontsize=10)

    ax = fig.add_subplot(gs[1, 1])
    for start in range(0, 10, 2):
        ax.broken_barh([(start, 0.3)], (0, 1), facecolors="#d62728", alpha=0.85)
        ax.broken_barh([(start + 0.3, 1.7)], (0, 1), facecolors="#cfe8ff")
    ax.set_yticks([0.5])
    ax.set_yticklabels(["CPU"])
    ax.set_xlabel("waktu")
    ax.set_ylim(-0.3, 1.5)
    ax.set_title("CPU bebas selama DMA bekerja", fontsize=10)

    legend_elems = [
        Line2D([0], [0], color="#d62728", lw=6, alpha=0.85, label="CPU sibuk"),
        Line2D([0], [0], color="#cfe8ff", lw=6, label="CPU bebas / idle"),
    ]
    fig.legend(handles=legend_elems, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 0.98), fontsize=9.5)
    fig.suptitle("Perbandingan Alur Transfer Data: Blocking vs DMA", fontsize=13, y=1.04)
    save(fig, "diagram_blocking_vs_dma.png")


if __name__ == "__main__":
    plot_bouncing_debounce()
    plot_pullup_pulldown_concept()
    plot_pwm_duty_cycle()
    plot_servo_pulse_diagram()
    plot_esc_brushless_block()
    plot_isr_flow()
    plot_delay_vs_timer_timeline()
    plot_watchdog_timer()
    plot_freertos_dualcore()
    plot_blocking_vs_dma()
