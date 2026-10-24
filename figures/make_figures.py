"""Draw Fig. 2 (where the cost landed, four designs), Fig. 3 (one product, compute vs convert) and
Fig. 4 (spring-semester simulated TVLA, cropped from the two 60k-trace PNGs in figures/).

Run from midterm_report/:  python3 figures/make_figures.py
Numbers come from the project's cost model and last semester's TVLA runs.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                     "font.size": 7, "pdf.fonttype": 42})
HERE = os.path.dirname(os.path.abspath(__file__))
RED, GREY, DARK, LIGHT = "#b22222", "#e6e6e6", "#222222", "#9a9a9a"

STAGES = ["Store", "Multiply", "Convert\nB→A", "Add\ntree", "Accum.", "Convert\nA→B", "BN/\nReLU"]
ROWS = [
    ("1  Three-share Boolean", ["Add\ntree"], ["Convert\nB→A", "Convert\nA→B"]),
    ("2  Fully arithmetic", ["Store", "Add\ntree"], ["Convert\nB→A"]),
    ("3  Boolean AND + convert", ["Multiply"], []),
    ("4  Boolean XNOR + convert", ["Convert\nB→A"], []),
]


COLW = 3.5  # IEEE conference \\columnwidth in inches, so fonts print at their stated size


def fig_journey():
    # Laid out in inches on a full-figure axis, so nothing is rescaled when placed at column width.
    bw, gap, bh = 0.46, 0.04, 0.22          # box width, gap, box height
    lab, pitch = 0.13, 0.40                 # row-label band above each row, row-to-row pitch
    x0 = (COLW - (7 * bw + 6 * gap)) / 2
    H = (len(ROWS) - 1) * pitch + bh + lab + 0.02
    fig = plt.figure(figsize=(COLW, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, COLW)
    ax.set_ylim(0, H)
    ax.axis("off")
    for k, (name, hot, absent) in enumerate(ROWS):
        y0 = 0.01 + (len(ROWS) - 1 - k) * pitch
        ax.text(x0, y0 + bh + 0.03, name, ha="left", va="bottom", fontsize=7, fontweight="bold", color=DARK)
        for i, st in enumerate(STAGES):
            x = x0 + i * (bw + gap)
            is_hot, is_off = st in hot, st in absent
            ax.add_patch(FancyBboxPatch((x, y0), bw, bh, boxstyle="round,pad=0,rounding_size=0.03",
                                        facecolor=RED if is_hot else ("white" if is_off else GREY),
                                        edgecolor=LIGHT if is_off else "none",
                                        linestyle="--" if is_off else "-", linewidth=0.6))
            ax.text(x + bw / 2, y0 + bh / 2, st, ha="center", va="center", fontsize=6.2,
                    color="white" if is_hot else (LIGHT if is_off else DARK), linespacing=0.95)
    fig.savefig(os.path.join(HERE, "journey.pdf"))
    plt.close(fig)


def fig_product():
    H = 0.95
    fig = plt.figure(figsize=(COLW, H))
    left, right, bottom, top = 1.42, 0.06, 0.30, 0.03   # margins in inches
    ax = fig.add_axes([left / COLW, bottom / H, 1 - (left + right) / COLW, 1 - (bottom + top) / H])
    labels = ["Compute the product\n(XNOR, 8-bit weight, 2 shares)", "Convert it to arithmetic shares\n(one B2A converter)"]
    vals = [16, 150]
    ax.barh([1, 0], vals, height=0.6, color=[GREY, RED])
    for y, v in zip([1, 0], vals):
        ax.text(v + 3, y, f"{v} gates", va="center", fontsize=7, color=DARK)
    ax.set_yticks([1, 0])
    ax.set_yticklabels(labels, fontsize=6.5, linespacing=0.95)
    ax.set_ylim(-0.45, 1.45)
    ax.set_xlim(0, 200)
    ax.set_xticks([0, 50, 100, 150])
    ax.set_xlabel("Two-input logic gates per product", fontsize=7, labelpad=2)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_linewidth(0.6)
    ax.tick_params(axis="x", labelsize=6.5, width=0.6, length=2.5, pad=1.5)
    ax.tick_params(axis="y", length=0, pad=3)
    fig.savefig(os.path.join(HERE, "product.pdf"))
    plt.close(fig)


# Pixel calibration of the spring-semester TVLA PNGs (3600 x 3000, lower t-statistic panel), read from
# their grid lines: t = 0 sits on row 2177 and each unit of t is 18.52 rows, while x = 0 ns sits on
# column 376 and x = 20 ns on column 3405. The PNGs are cropped and placed under new axes, not redrawn.
TV_ROW0, TV_ROW_PER_T, TV_COL0, TV_COL_PER_NS = 2177.0, 18.52, 376.0, (3405.0 - 376.0) / 20.0


def fig_tvla(xlim=(4.0, 7.0), tlim=15.0):
    import matplotlib.image as mpimg
    H = 1.30
    fig = plt.figure(figsize=(COLW, H))
    panels = [("tvla_hybrid_60k.png", "(a) Hybrid, two shares in carry chain"),
              ("tvla_3share_60k.png", "(b) Three-share")]
    left, gapx, right, bottom, top = 0.36, 0.14, 0.04, 0.28, 0.16
    w = (COLW - left - gapx - right) / 2
    for k, (fn, title) in enumerate(panels):
        img = mpimg.imread(os.path.join(HERE, fn))
        r0 = int(round(TV_ROW0 - tlim * TV_ROW_PER_T)); r1 = int(round(TV_ROW0 + tlim * TV_ROW_PER_T))
        c0 = int(round(TV_COL0 + xlim[0] * TV_COL_PER_NS)); c1 = int(round(TV_COL0 + xlim[1] * TV_COL_PER_NS))
        ax = fig.add_axes([(left + k * (w + gapx)) / COLW, bottom / H, w / COLW, 1 - (bottom + top) / H])
        ax.imshow(img[r0:r1, c0:c1], extent=[xlim[0], xlim[1], -tlim, tlim], aspect="auto",
                  interpolation="lanczos")
        ax.set_xlim(*xlim); ax.set_ylim(-tlim, tlim)
        ax.set_xticks([4, 5, 6, 7]); ax.set_yticks([-10, -4.5, 0, 4.5, 10])
        ax.set_yticklabels(["−10", "−4.5", "0", "4.5", "10"] if k == 0 else [])
        ax.set_title(title, fontsize=6.5, pad=2)
        ax.set_xlabel("Time (ns)", fontsize=6.5, labelpad=1)
        if k == 0:
            ax.set_ylabel("$t$-statistic", fontsize=6.5, labelpad=1)
        ax.tick_params(labelsize=6, width=0.5, length=2, pad=1.5)
        for sp in ax.spines.values():
            sp.set_linewidth(0.5)
    fig.savefig(os.path.join(HERE, "tvla.pdf"), dpi=600)
    plt.close(fig)


if __name__ == "__main__":
    fig_journey()
    fig_product()
    fig_tvla()
