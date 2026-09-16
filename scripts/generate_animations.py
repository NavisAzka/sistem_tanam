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
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Wedge

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "img")
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams.update({"font.size": 10})


def save_gif(fig, anim, name, fps=12):
    path = os.path.join(OUT_DIR, name)
    anim.save(path, writer=PillowWriter(fps=fps))
    plt.close(fig)
    print(f"saved {path}")


def hold(seq, n):
    """Ulangi item terakhir dari list n kali (efek jeda/tahan)."""
    return seq + [seq[-1]] * n


def draw_resistor_static(ax, x, y_bottom, y_top, n_zigzag=6, width=0.13, color="#333333"):
    ys = np.linspace(y_bottom, y_top, n_zigzag * 2 + 1)
    xs = [x]
    for i in range(1, len(ys) - 1):
        xs.append(x + (width if i % 2 == 1 else -width))
    xs.append(x)
    (ln,) = ax.plot(xs, ys, color=color, linewidth=1.6, zorder=3)
    return ln


# ---------------------------------------------------------------------------
# 1) Arah putaran quadrature encoder — disc + sinyal + PENGHITUNG PULSA
# ---------------------------------------------------------------------------
def gif_quadrature_direction():
    period = 1.0
    step = 0.10
    forward_frames = 50
    backward_frames = 50
    hold_frames = 10  # jeda saat arah berbalik, supaya kebaca

    p_fwd = list(np.arange(forward_frames) * step)
    p_bwd = list(p_fwd[-1] - np.arange(backward_frames) * step)
    p_vals = hold(p_fwd, hold_frames) + hold(p_bwd, hold_frames)
    n_frames = len(p_vals)
    half_end = forward_frames + hold_frames  # index awal fase mundur

    phase_b = 0.25 * period

    def square(p, offset=0.0):
        return (np.mod(p - offset, period) < period / 2).astype(float)

    window = 3.2

    fig = plt.figure(figsize=(10, 5.4))
    gs = fig.add_gridspec(3, 2, height_ratios=[0.35, 1.5, 0.55], width_ratios=[1, 1.5])
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis("off")
    ax_disc = fig.add_subplot(gs[1, 0])
    ax_sig = fig.add_subplot(gs[1, 1])
    ax_info = fig.add_subplot(gs[2, :])
    ax_info.axis("off")

    title_text = ax_title.text(0.5, 0.5, "", ha="center", va="center", fontsize=15, fontweight="bold",
                                transform=ax_title.transAxes)

    # --- disc panel ---
    ax_disc.set_xlim(-1.6, 1.6)
    ax_disc.set_ylim(-1.6, 1.9)
    ax_disc.axis("off")
    ax_disc.set_aspect("equal")
    ax_disc.set_title("Piringan Encoder (dilihat dari depan)", fontsize=10)

    n_sectors = 8
    wedges = []
    for k in range(n_sectors):
        w = Wedge((0, 0), 1.0, 0, 360 / n_sectors, facecolor="#333333" if k % 2 == 0 else "#ffffff",
                   edgecolor="#333333", linewidth=1)
        ax_disc.add_patch(w)
        wedges.append(w)
    ax_disc.add_patch(Circle((0, 0), 0.12, facecolor="#888888", edgecolor="#333333", zorder=5))

    sensor_a = Circle((1.35, 0.18), 0.09, facecolor="#d62728", edgecolor="black", zorder=6)
    sensor_b = Circle((1.35, -0.18), 0.09, facecolor="#2ca02c", edgecolor="black", zorder=6)
    ax_disc.add_patch(sensor_a)
    ax_disc.add_patch(sensor_b)
    ax_disc.text(1.55, 0.18, "Sensor A", color="#d62728", fontsize=9, va="center", fontweight="bold")
    ax_disc.text(1.55, -0.18, "Sensor B", color="#2ca02c", fontsize=9, va="center", fontweight="bold")
    rotate_arrow = ax_disc.annotate("", xy=(0, 0), xytext=(0, 0),
                                     arrowprops=dict(arrowstyle="-|>", lw=0, color="none"))

    # --- signal panel ---
    ax_sig.set_xlim(0, window)
    ax_sig.set_ylim(-0.3, 2.7)
    ax_sig.set_yticks([0.5, 2.1])
    ax_sig.set_yticklabels(["Channel B", "Channel A"], fontsize=10)
    ax_sig.set_xlabel("waktu berjalan →")
    ax_sig.set_title("Sinyal yang Terbaca ESP32", fontsize=10)
    (line_a,) = ax_sig.step([], [], color="#d62728", linewidth=2.2, where="post")
    (line_b,) = ax_sig.step([], [], color="#2ca02c", linewidth=2.2, where="post")

    info_text = ax_info.text(
        0.5, 0.5, "", ha="center", va="center", fontsize=11.5, transform=ax_info.transAxes, wrap=True
    )

    def frame_state(i):
        going_forward = i < half_end
        p = p_vals[i]
        pulses = int(p / period)
        return going_forward, p, pulses

    def init():
        line_a.set_data([], [])
        line_b.set_data([], [])
        return [line_a, line_b]

    def update(frame):
        going_forward, p, pulses = frame_state(frame)
        angle0_deg = np.degrees(p * 2 * np.pi / period)
        for k, w in enumerate(wedges):
            w.set_theta1(angle0_deg + k * 360 / n_sectors)
            w.set_theta2(angle0_deg + (k + 1) * 360 / n_sectors)

        if going_forward:
            title_text.set_text("MOTOR BERPUTAR MAJU (searah jarum jam)")
            title_text.set_color("#1f4e8c")
            arah = "MAJU"
            pulse_display = pulses
        else:
            title_text.set_text("MOTOR BERPUTAR MUNDUR (berlawanan jarum jam)")
            title_text.set_color("#a3670a")
            arah = "MUNDUR"
            pulse_display = (forward_frames - 1) * step // period - (p_vals[half_end] - p) // period * 0  # placeholder
            pulse_display = int(max(0, (p_vals[half_end] - (p_vals[half_end] - p))))
            pulse_display = int(p)

        t = np.linspace(max(0, p - window), p, 400)
        pa = square(t, offset=0.0) * 1.0 + 1.6
        pb = square(t, offset=phase_b) * 1.0
        tt = t - t[0] if len(t) else t
        line_a.set_data(tt, pa)
        line_b.set_data(tt, pb)

        if going_forward:
            explanation = (
                f"Pulsa dihitung: {pulses}  |  Channel A berubah LEBIH DULU dibanding B\n"
                "→ ISR mendeteksi ini sebagai arah MAJU, counter pulsa BERTAMBAH (+1 tiap rising edge A)"
            )
        else:
            explanation = (
                f"Pulsa dihitung: {pulses}  |  Channel B berubah LEBIH DULU dibanding A\n"
                "→ ISR mendeteksi ini sebagai arah MUNDUR, counter pulsa BERKURANG (-1 tiap rising edge A)"
            )
        info_text.set_text(explanation)

        return [line_a, line_b]

    anim = FuncAnimation(fig, update, frames=n_frames, init_func=init, blit=False, interval=1000 / 11)
    fig.tight_layout()
    save_gif(fig, anim, "anim_quadrature_direction.gif", fps=11)


# ---------------------------------------------------------------------------
# 2) Program utama dijeda ISR — skenario konkret: LED berkedip + tombol
# ---------------------------------------------------------------------------
def gif_isr_flow():
    fig = plt.figure(figsize=(9, 5.6))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.3, 0.9, 0.7])
    ax_scene = fig.add_subplot(gs[0])
    ax_timeline = fig.add_subplot(gs[1])
    ax_info = fig.add_subplot(gs[2])
    ax_scene.axis("off")
    ax_timeline.axis("off")
    ax_info.axis("off")
    ax_scene.set_xlim(0, 10)
    ax_scene.set_ylim(0, 4)

    # MCU box, LED, button
    mcu = FancyBboxPatch((3.8, 0.8), 2.4, 1.8, boxstyle="round,pad=0.02,rounding_size=0.06",
                          linewidth=1.6, edgecolor="#333333", facecolor="#eeeeee")
    ax_scene.add_patch(mcu)
    ax_scene.text(5.0, 1.7, "ESP32", ha="center", fontsize=10, fontweight="bold")

    led = Circle((1.3, 1.7), 0.45, facecolor="#dddddd", edgecolor="#333333", linewidth=1.5)
    ax_scene.add_patch(led)
    ax_scene.text(1.3, 2.5, "LED", ha="center", fontsize=9)
    led_status = ax_scene.text(1.3, 0.9, "", ha="center", fontsize=8.5, color="#555555")

    button = FancyBboxPatch((7.6, 1.35), 1.3, 0.7, boxstyle="round,pad=0.02,rounding_size=0.08",
                             linewidth=1.6, edgecolor="#333333", facecolor="#cccccc")
    ax_scene.add_patch(button)
    ax_scene.text(8.25, 1.7, "Tombol", ha="center", fontsize=9)
    press_text = ax_scene.text(8.25, 2.4, "", ha="center", fontsize=9.5, color="#a31515", fontweight="bold")

    counter_text = ax_scene.text(5.0, 3.4, "", ha="center", fontsize=11, fontweight="bold")

    # timeline
    ax_timeline.set_xlim(-0.5, 10.5)
    ax_timeline.set_ylim(1.4, 3.6)
    ax_timeline.broken_barh([(0, 10)], (2, 1), facecolors="#cfe8ff", edgecolor="#1f4e8c")
    ax_timeline.broken_barh([(4, 1.4)], (2, 1), facecolors="#ffcccc", edgecolor="#a31515")
    ax_timeline.text(2, 2.5, "loop() — Program Utama", ha="center", va="center", fontsize=9)
    ax_timeline.text(4.7, 2.5, "ISR", ha="center", va="center", fontsize=9, fontweight="bold")
    ax_timeline.text(7.7, 2.5, "loop() lanjut dari titik semula", ha="center", va="center", fontsize=9)
    (marker,) = ax_timeline.plot([], [], "o", color="#1f4e8c", markersize=13, zorder=5)

    info_text = ax_info.text(0.5, 0.5, "", ha="center", va="center", fontsize=11, transform=ax_info.transAxes, wrap=True)

    # --- build frame sequence ---
    xs_main1 = list(np.linspace(0.2, 4.0, 20))
    xs_isr = list(np.linspace(4.0, 5.4, 14))
    xs_main2 = list(np.linspace(5.4, 9.8, 22))
    xs_all = hold(xs_main1, 6) + hold(xs_isr, 10) + hold(xs_main2, 8)
    n_frames = len(xs_all)

    # blink pattern for LED during "main program" segments (0.5s period simplified as frame-based toggle)
    def blink_on(idx):
        return (idx // 4) % 2 == 0

    isr_start = len(hold(xs_main1, 6))
    isr_end = isr_start + len(hold(xs_isr, 10))

    def init():
        marker.set_data([], [])
        return [marker]

    def update(frame):
        x = xs_all[frame]
        marker.set_data([x], [2.5])
        in_isr = isr_start <= frame < isr_end
        before_isr = frame < isr_start
        after_isr = frame >= isr_end

        if in_isr:
            marker.set_color("#a31515")
            led.set_facecolor("#dddddd")
            led_status.set_text("LED dipegang OFF\n(dipaksa oleh ISR)")
            press_text.set_text("DITEKAN!")
            counter_text.set_text("ISR berjalan: matikan LED, set flag darurat = 1")
            info_text.set_text(
                "Saat tombol ditekan, hardware LANGSUNG menjalankan ISR — tidak peduli loop() sedang\n"
                "mengerjakan apa. ISR dibuat SINGKAT: cuma matikan LED & set flag, lalu langsung kembali."
            )
        else:
            marker.set_color("#1f4e8c")
            press_text.set_text("")
            if blink_on(frame):
                led.set_facecolor("#ffd400")
                led_status.set_text("LED berkedip: NYALA")
            else:
                led.set_facecolor("#dddddd")
                led_status.set_text("LED berkedip: MATI")
            if before_isr:
                counter_text.set_text("loop() sedang berjalan normal (LED berkedip tiap 500ms)")
                info_text.set_text(
                    "Program utama (loop()) berjalan seperti biasa — LED berkedip terus tanpa henti,\n"
                    "sampai suatu saat interrupt terjadi (tombol ditekan)."
                )
            else:
                counter_text.set_text("loop() lanjut PERSIS dari titik sebelum diinterupsi")
                info_text.set_text(
                    "Setelah ISR selesai (sangat cepat, biasanya < 1ms), program utama melanjutkan\n"
                    "PERSIS dari baris kode tempat ia berhenti tadi — seolah tidak pernah terjeda."
                )
        return [marker]

    anim = FuncAnimation(fig, update, frames=n_frames, init_func=init, blit=False, interval=1000 / 10)
    fig.tight_layout()
    save_gif(fig, anim, "anim_isr_flow.gif", fps=10)


# ---------------------------------------------------------------------------
# 3) Watchdog timer — bar countdown + papan MCU + status jelas
# ---------------------------------------------------------------------------
def gif_watchdog_timer():
    fig = plt.figure(figsize=(9, 5.2))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.5, 1])
    ax = fig.add_subplot(gs[0])
    ax_info = fig.add_subplot(gs[1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax_info.axis("off")

    # papan MCU icon
    board = FancyBboxPatch((0.06, 0.55), 0.16, 0.3, boxstyle="round,pad=0.01,rounding_size=0.02",
                            linewidth=1.6, edgecolor="#333333", facecolor="#e8e8e8")
    ax.add_patch(board)
    ax.text(0.14, 0.7, "ESP32", ha="center", fontsize=8, rotation=90, va="center")
    led_status = Circle((0.14, 0.6), 0.025, facecolor="#2ca02c", edgecolor="black", zorder=6)
    ax.add_patch(led_status)

    bar_bg = FancyBboxPatch((0.32, 0.62), 0.6, 0.16, boxstyle="round,pad=0.01,rounding_size=0.02",
                             linewidth=1.4, edgecolor="#555555", facecolor="#eeeeee")
    ax.add_patch(bar_bg)
    bar_fill = FancyBboxPatch((0.32, 0.62), 0.6, 0.16, boxstyle="round,pad=0.01,rounding_size=0.02",
                               linewidth=0, facecolor="#2ca02c")
    ax.add_patch(bar_fill)
    ax.text(0.32, 0.82, "Waktu sebelum Watchdog Reset:", fontsize=9.5)
    countdown_num = ax.text(0.94, 0.7, "", ha="left", va="center", fontsize=11, fontweight="bold")

    title_text = ax.text(0.5, 0.45, "", ha="center", fontsize=15, fontweight="bold")
    sub_text = ax.text(0.5, 0.30, "", ha="center", fontsize=10.5, color="#555555")
    feed_flash = ax.text(0.5, 0.15, "", ha="center", fontsize=11, color="#2ca02c", fontweight="bold")

    info_text = ax_info.text(0.5, 0.5, "", ha="center", va="center", fontsize=11, transform=ax_info.transAxes, wrap=True)

    timeout_s = 5.0
    n_feed_cycles = 3
    frames_per_feed = 9

    fill_sequence = []
    labels = []
    feed_flags = []
    for _ in range(n_feed_cycles):
        fill_sequence += list(np.linspace(1.0, 0.08, frames_per_feed))
        labels += ["normal"] * frames_per_feed
        feed_flags += [True] + [False] * (frames_per_feed - 1)

    hang_frames = 42
    fill_sequence += list(np.linspace(1.0, 0.0, hang_frames))
    labels += ["hang"] * hang_frames
    feed_flags += [False] * hang_frames

    reset_frames = 10
    fill_sequence += [0.0] * reset_frames
    labels += ["reset"] * reset_frames
    feed_flags += [False] * reset_frames

    reboot_frames = 8
    fill_sequence += [1.0] * reboot_frames
    labels += ["reboot"] * reboot_frames
    feed_flags += [False] * reboot_frames

    n_frames = len(fill_sequence)

    def init():
        bar_fill.set_width(0.0)
        title_text.set_text("")
        sub_text.set_text("")
        countdown_num.set_text("")
        feed_flash.set_text("")
        return [bar_fill]

    def update(frame):
        level = fill_sequence[frame]
        state = labels[frame]
        bar_fill.set_width(0.6 * level)
        countdown_num.set_text(f"{level * timeout_s:.1f} s")

        if state == "normal":
            bar_fill.set_facecolor("#2ca02c")
            title_text.set_text("Program Berjalan Normal")
            title_text.set_color("#2ca02c")
            sub_text.set_text("esp_task_wdt_reset() dipanggil secara rutin sebelum waktu habis")
            led_status.set_facecolor("#2ca02c")
            feed_flash.set_text("watchdog di-\"FEED\" ✓" if feed_flags[frame] else "")
            info_text.set_text(
                "Selama program sehat, ia rutin memanggil esp_task_wdt_reset() untuk mengisi ulang\n"
                "hitungan mundur watchdog SEBELUM mencapai nol — mencegah reset terjadi."
            )
        elif state == "hang":
            bar_fill.set_facecolor("#d62728" if level < 0.3 else "#ffb84d")
            title_text.set_text("PROGRAM HANG!")
            title_text.set_color("#a31515")
            sub_text.set_text("Terjebak infinite loop — esp_task_wdt_reset() TIDAK pernah dipanggil lagi")
            led_status.set_facecolor("#a31515")
            feed_flash.set_text("")
            info_text.set_text(
                "Program macet (mis. infinite loop / menunggu sensor yang tidak pernah merespons).\n"
                "Watchdog terus menghitung mundur tanpa pernah di-reset — waktu hampir habis!"
            )
        elif state == "reset":
            flash_on = frame % 2 == 0
            bar_fill.set_facecolor("#d62728" if flash_on else "#ffffff")
            title_text.set_text("WATCHDOG TIMEOUT -> RESET!")
            title_text.set_color("#a31515")
            sub_text.set_text("Sistem di-reset paksa oleh hardware watchdog")
            led_status.set_facecolor("#d62728" if flash_on else "#ffffff")
            feed_flash.set_text("")
            info_text.set_text(
                "Karena tidak pernah di-reset, watchdog hardware mengambil alih dan me-restart\n"
                "chip secara paksa — inilah tujuannya: sistem tidak boleh macet selamanya."
            )
        else:  # reboot
            bar_fill.set_facecolor("#2ca02c")
            title_text.set_text("Sistem Boot Ulang...")
            title_text.set_color("#1f4e8c")
            sub_text.set_text("Program mulai dari awal, watchdog aktif kembali")
            led_status.set_facecolor("#2ca02c")
            feed_flash.set_text("")
            info_text.set_text(
                "Setelah reboot, program berjalan dari awal lagi (setup() dipanggil ulang) dan\n"
                "siklus feed-watchdog normal dimulai kembali."
            )
        return [bar_fill]

    anim = FuncAnimation(fig, update, frames=n_frames, init_func=init, blit=False, interval=1000 / 9)
    fig.tight_layout()
    save_gif(fig, anim, "anim_watchdog_timer.gif", fps=9)


# ---------------------------------------------------------------------------
# 4) Pull-up vs pull-down — animasi arus (bola-bola) mengalir saat tombol
#    ditekan (sirkuit tertutup), berhenti saat idle (sirkuit terbuka)
# ---------------------------------------------------------------------------
def gif_pullup_pulldown_current():
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 6.6))

    def setup_panel(ax, title, resistor_range, switch_range, gpio_y, tap_color):
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.plot([0, 0], [0, 4], color="#333333", linewidth=1.6, zorder=1)
        draw_resistor_static(ax, 0, *resistor_range)
        ax.text(0, 4.15, "VCC (3.3V)", ha="center", fontsize=10, fontweight="bold")
        ax.text(0, -0.35, "GND", ha="center", fontsize=10, fontweight="bold")
        ax.plot([0, 1.2], [gpio_y, gpio_y], color=tap_color, linewidth=2, zorder=2)
        gpio_label = ax.text(1.3, gpio_y, "", va="center", fontsize=10, fontweight="bold", color=tap_color)
        state_dot = Circle((1.25, gpio_y), 0.09, facecolor="#cccccc", edgecolor="black", zorder=6)
        ax.add_patch(state_dot)
        r_mid = (resistor_range[0] + resistor_range[1]) / 2
        ax.text(0.32, r_mid, "R", fontsize=10, color="gray")
        ax.set_xlim(-1.6, 2.7)
        ax.set_ylim(-1.7, 4.6)
        ax.axis("off")
        return gpio_label, state_dot

    gpio_label_up, dot_up = setup_panel(axes[0], "Pull-Up Resistor", (2.6, 4.0), (0, 2.2), 2.3, "#1f4e8c")
    gpio_label_dn, dot_dn = setup_panel(axes[1], "Pull-Down Resistor", (0, 1.4), (1.8, 4.0), 1.7, "#a3670a")

    # elemen switch yang diganti tiap frame (garis pemutus + label)
    (switch_line_up,) = axes[0].plot([], [], color="#333333", linewidth=1.6, zorder=3)
    (switch_line_dn,) = axes[1].plot([], [], color="#333333", linewidth=1.6, zorder=3)
    axes[0].text(-0.6, 1.1, "tombol", fontsize=9, ha="center", color="gray")
    axes[1].text(-0.6, 2.9, "tombol", fontsize=9, ha="center", color="gray")

    status_text = fig.text(0.5, 0.05, "", ha="center", va="bottom", fontsize=11.5, fontweight="bold")

    n_dots = 5
    (dots_up,) = axes[0].plot([], [], "o", color="#ffb300", markersize=9, zorder=5)
    (dots_dn,) = axes[1].plot([], [], "o", color="#ffb300", markersize=9, zorder=5)

    def draw_switch_state(y_bottom, y_top, closed):
        gap0 = y_bottom + (y_top - y_bottom) * 0.28
        gap1 = y_top - (y_top - y_bottom) * 0.28
        if closed:
            return [0, 0], [gap0, gap1]
        else:
            return [0, 0.22], [gap0, gap1]

    # --- sekuens frame: idle(terbuka) -> ditekan(tertutup, arus mengalir) -> lepas ---
    idle_frames = 14
    closed_frames = 34
    release_frames = 6
    seq = ["idle"] * idle_frames + ["closed"] * closed_frames + ["idle"] * release_frames
    n_frames = len(seq)

    def init():
        return [switch_line_up, switch_line_dn, dots_up, dots_dn]

    def update(frame):
        state = seq[frame]
        closed = state == "closed"

        xs, ys = draw_switch_state(0, 2.2, closed)
        switch_line_up.set_data(xs, ys)
        xs2, ys2 = draw_switch_state(1.8, 4.0, closed)
        switch_line_dn.set_data(xs2, ys2)

        if closed:
            flow = (frame - idle_frames) / max(1, closed_frames)
            # posisi y menurun dari VCC (4) ke GND (0) -> arus mengalir turun
            positions = [4.0 - ((flow * 4 + i / n_dots) % 1.0) * 4.0 for i in range(n_dots)]
            dots_up.set_data([0] * n_dots, positions)
            dots_dn.set_data([0] * n_dots, positions)
            gpio_label_up.set_text("GPIO baca: LOW")
            dot_up.set_facecolor("#d62728")
            gpio_label_dn.set_text("GPIO baca: HIGH")
            dot_dn.set_facecolor("#2ca02c")
            status_text.set_text(
                "Tombol DITEKAN -> sirkuit TERTUTUP\narus mengalir dari VCC ke GND melalui R"
            )
            status_text.set_color("#a31515")
        else:
            dots_up.set_data([], [])
            dots_dn.set_data([], [])
            gpio_label_up.set_text("GPIO baca: HIGH")
            dot_up.set_facecolor("#2ca02c")
            gpio_label_dn.set_text("GPIO baca: LOW")
            dot_dn.set_facecolor("#d62728")
            status_text.set_text(
                "Tombol TIDAK ditekan -> sirkuit TERBUKA\ntidak ada arus mengalir (GPIO hanya membaca tegangan)"
            )
            status_text.set_color("#1f4e8c")

        return [switch_line_up, switch_line_dn, dots_up, dots_dn]

    anim = FuncAnimation(fig, update, frames=n_frames, init_func=init, blit=False, interval=1000 / 12)
    fig.suptitle("Aliran Arus pada Rangkaian Pull-Up vs Pull-Down", fontsize=13, y=0.98)
    fig.tight_layout(rect=[0.02, 0.15, 0.98, 0.95])
    save_gif(fig, anim, "anim_pullup_pulldown_arus.gif", fps=12)


if __name__ == "__main__":
    gif_quadrature_direction()
    gif_isr_flow()
    gif_watchdog_timer()
    gif_pullup_pulldown_current()
