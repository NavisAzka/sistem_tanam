"""
Generate short looping GIF animations to replace/accompany a few static
diagrams (bukan hasil rekaman alat sungguhan -- ilustrasi konsep, dibuat
dengan matplotlib.animation + Pillow).

Usage:
    python scripts/generate_animations.py
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyBboxPatch, Circle

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "img")
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams.update({"font.size": 10})


def save_gif(fig, anim, name, fps=14):
    path = os.path.join(OUT_DIR, name)
    anim.save(path, writer=PillowWriter(fps=fps))
    plt.close(fig)
    print(f"saved {path}")


# ---------------------------------------------------------------------------
# 1) Arah putaran quadrature encoder (Channel A/B) — CW lalu CCW, looping
# ---------------------------------------------------------------------------
def gif_quadrature_direction():
    n_frames = 90
    half = n_frames // 2
    step = 0.12  # kenaikan posisi (p) per frame
    p_vals = np.concatenate([np.arange(half) * step, (half - 1) * step - np.arange(n_frames - half) * step])

    period = 1.0
    phase_b = 0.25 * period  # B lag 90 derajat dari A pada disc (tetap secara fisik)

    def square(p, period=period, offset=0.0):
        return (np.mod(p - offset, period) < period / 2).astype(float)

    window = 4.0  # tampilkan 4 periode terakhir

    fig, axes = plt.subplots(1, 2, figsize=(8, 3.2), gridspec_kw={"width_ratios": [1, 1.6]})
    fig.subplots_adjust(wspace=0.35)

    ax_disc = axes[0]
    ax_disc.set_xlim(-1.4, 1.4)
    ax_disc.set_ylim(-1.4, 1.6)
    ax_disc.axis("off")
    ax_disc.set_aspect("equal")
    disc = Circle((0, 0), 1.0, fill=False, linewidth=1.5, edgecolor="#333333")
    ax_disc.add_patch(disc)
    n_sectors = 8
    sector_lines = []
    for k in range(n_sectors):
        (ln,) = ax_disc.plot([], [], color="#999999", linewidth=1)
        sector_lines.append(ln)
    (arrow_line,) = ax_disc.plot([], [], color="#1f77b4", linewidth=3)
    dir_text = ax_disc.text(0, 1.35, "", ha="center", fontsize=11, fontweight="bold")
    sensor_a = ax_disc.plot([1.05], [0.25], "o", color="#d62728", markersize=7)[0]
    sensor_b = ax_disc.plot([1.05], [-0.25], "o", color="#2ca02c", markersize=7)[0]
    ax_disc.text(1.25, 0.25, "A", color="#d62728", fontsize=9, va="center")
    ax_disc.text(1.25, -0.25, "B", color="#2ca02c", fontsize=9, va="center")

    ax_sig = axes[1]
    ax_sig.set_xlim(0, window)
    ax_sig.set_ylim(-0.3, 2.6)
    ax_sig.set_yticks([0.5, 2.1])
    ax_sig.set_yticklabels(["Ch B", "Ch A"])
    ax_sig.set_xlabel("waktu")
    (line_a,) = ax_sig.step([], [], color="#d62728", linewidth=1.8, where="post")
    (line_b,) = ax_sig.step([], [], color="#2ca02c", linewidth=1.8, where="post")

    def init():
        for ln in sector_lines:
            ln.set_data([], [])
        arrow_line.set_data([], [])
        line_a.set_data([], [])
        line_b.set_data([], [])
        return sector_lines + [arrow_line, line_a, line_b, dir_text]

    def update(frame):
        p = p_vals[frame]
        angle0 = p * 2 * np.pi / period
        for k, ln in enumerate(sector_lines):
            a = angle0 + k * 2 * np.pi / n_sectors
            ln.set_data([0, np.cos(a)], [0, np.sin(a)])
        arrow_line.set_data([0, 0.9 * np.cos(angle0)], [0, 0.9 * np.sin(angle0)])

        going_forward = frame < half
        dir_text.set_text("Maju (CW) — A mendahului B" if going_forward else "Mundur (CCW) — B mendahului A")
        dir_text.set_color("#1f4e8c" if going_forward else "#a3670a")

        t = np.linspace(max(0, p - window), p, 400)
        pa = square(t, offset=0.0) * 1.0 + 1.6
        pb = square(t, offset=phase_b) * 1.0
        tt = t - t[0] if len(t) else t
        line_a.set_data(tt, pa)
        line_b.set_data(tt, pb)
        return sector_lines + [arrow_line, line_a, line_b, dir_text]

    anim = FuncAnimation(fig, update, frames=n_frames, init_func=init, blit=False, interval=1000 / 14)
    save_gif(fig, anim, "anim_quadrature_direction.gif")


# ---------------------------------------------------------------------------
# 2) Program utama dijeda oleh ISR (playhead bergerak), looping
# ---------------------------------------------------------------------------
def gif_isr_flow():
    fig, ax = plt.subplots(figsize=(7.5, 2.6))
    ax.broken_barh([(0, 10)], (2, 1), facecolors="#cfe8ff", edgecolor="#1f4e8c")
    ax.broken_barh([(4, 1.2)], (2, 1), facecolors="#ffcccc", edgecolor="#a31515")
    ax.text(2, 2.5, "Program Utama", ha="center", va="center", fontsize=9)
    ax.text(4.6, 2.5, "ISR", ha="center", va="center", fontsize=9, fontweight="bold")
    ax.text(7.7, 2.5, "Program Utama lanjut", ha="center", va="center", fontsize=9)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(1.4, 3.6)
    ax.axis("off")
    ax.set_title("Alur Eksekusi Program Utama yang Dijeda oleh ISR", fontsize=11)

    (marker,) = ax.plot([], [], "o", color="#d62728", markersize=11, zorder=5)
    status_text = ax.text(5, 3.3, "", ha="center", fontsize=9.5, color="#333333")

    # lintasan x: 0 -> 4 (main), 4 -> 5.2 (ISR, y sedikit turun), 5.2 -> 10 (main lanjut)
    xs_main1 = np.linspace(0.2, 4.0, 22)
    xs_isr = np.linspace(4.0, 5.2, 14)
    xs_main2 = np.linspace(5.2, 9.8, 22)
    pause = np.full(6, xs_main1[-1])  # jeda sesaat sebelum masuk ISR (efek "freeze")

    xs_all = np.concatenate([xs_main1, pause, xs_isr, xs_isr[-6:], xs_main2])
    ys_all = np.concatenate(
        [
            np.full(len(xs_main1), 2.5),
            np.full(len(pause), 2.5),
            np.full(len(xs_isr), 2.5),
            np.full(6, 2.5),
            np.full(len(xs_main2), 2.5),
        ]
    )
    labels = (
        ["Program utama berjalan..."] * (len(xs_main1) + len(pause))
        + ["interrupt terjadi -> masuk ISR"] * (len(xs_isr) + 6)
        + ["ISR selesai, program lanjut"] * len(xs_main2)
    )

    def init():
        marker.set_data([], [])
        status_text.set_text("")
        return marker, status_text

    def update(frame):
        marker.set_data([xs_all[frame]], [ys_all[frame]])
        marker.set_color("#a31515" if 4.0 <= xs_all[frame] <= 5.2 else "#1f4e8c")
        status_text.set_text(labels[frame])
        return marker, status_text

    anim = FuncAnimation(fig, update, frames=len(xs_all), init_func=init, blit=False, interval=1000 / 16)
    save_gif(fig, anim, "anim_isr_flow.gif", fps=16)


# ---------------------------------------------------------------------------
# 3) Watchdog timer: feed rutin vs hang -> reset, looping
# ---------------------------------------------------------------------------
def gif_watchdog_timer():
    fig, ax = plt.subplots(figsize=(7.5, 3.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    bar_bg = FancyBboxPatch((0.15, 0.35), 0.7, 0.18, boxstyle="round,pad=0.01,rounding_size=0.02",
                             linewidth=1.4, edgecolor="#555555", facecolor="#eeeeee")
    ax.add_patch(bar_bg)
    bar_fill = FancyBboxPatch((0.15, 0.35), 0.7, 0.18, boxstyle="round,pad=0.01,rounding_size=0.02",
                               linewidth=0, facecolor="#2ca02c")
    ax.add_patch(bar_fill)
    title_text = ax.text(0.5, 0.75, "", ha="center", fontsize=12, fontweight="bold")
    sub_text = ax.text(0.5, 0.15, "", ha="center", fontsize=9.5, color="#555555")

    n_feed_cycles = 3
    frames_per_feed = 10
    hang_frames = 40

    def make_feed_segment():
        return list(np.linspace(1.0, 0.05, frames_per_feed))

    fill_sequence = []
    labels = []
    for _ in range(n_feed_cycles):
        fill_sequence += make_feed_segment()
        labels += ["Program normal — watchdog rutin di-\"feed\" sebelum timeout"] * frames_per_feed
    fill_sequence += list(np.linspace(1.0, 0.0, hang_frames))
    labels += ["Program HANG — tidak memberi makan watchdog!"] * hang_frames
    fill_sequence += [0.0] * 6
    labels += ["WATCHDOG TIMEOUT -> RESET OTOMATIS"] * 6

    def init():
        bar_fill.set_width(0.0)
        title_text.set_text("")
        sub_text.set_text("")
        return bar_fill, title_text, sub_text

    def update(frame):
        level = fill_sequence[frame]
        bar_fill.set_width(0.7 * level)
        is_reset_flash = labels[frame].startswith("WATCHDOG")
        if is_reset_flash and frame % 2 == 0:
            bar_fill.set_facecolor("#d62728")
        elif level < 0.25:
            bar_fill.set_facecolor("#d62728")
        elif level < 0.5:
            bar_fill.set_facecolor("#ffb84d")
        else:
            bar_fill.set_facecolor("#2ca02c")

        title_text.set_text("RESET!" if is_reset_flash else "Watchdog Timer Countdown")
        title_text.set_color("#a31515" if is_reset_flash else "#333333")
        sub_text.set_text(labels[frame])
        return bar_fill, title_text, sub_text

    anim = FuncAnimation(fig, update, frames=len(fill_sequence), init_func=init, blit=False, interval=1000 / 14)
    save_gif(fig, anim, "anim_watchdog_timer.gif")


if __name__ == "__main__":
    gif_quadrature_direction()
    gif_isr_flow()
    gif_watchdog_timer()
