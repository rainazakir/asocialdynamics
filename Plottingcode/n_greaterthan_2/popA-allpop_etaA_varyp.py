import os, re, glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
plt.rcParams['figure.dpi'] = 400

# =========================================================
# USER SETTINGS
# =========================================================
folder = "/content"
pattern = "DSB_results_n2_n3_n5_A1_vs_rest_0.92_p*.mat"

n_to_plot = 3          # main curve (2, 3, or 5)
plot_n2_for_p1 = True  # add dashed n=2 when p=1

linewidth = 4
cmap_name = "turbo"

LEGEND_P_NCOL = 2      # p-legend columns
# =========================================================

# ---- find files
files = sorted(glob.glob(os.path.join(folder, pattern)))
if not files:
    raise FileNotFoundError(f"No files found: {os.path.join(folder, pattern)}")

p_re = re.compile(r"_p([0-9]*\.?[0-9]+)\.mat$")

file_info = []
for f in files:
    m = p_re.search(os.path.basename(f))
    if m:
        file_info.append((float(m.group(1)), f))

file_info.sort(key=lambda x: x[0])
p_vals = np.array([p for p, _ in file_info], dtype=float)

# ---- colormap
norm = Normalize(vmin=float(p_vals.min()), vmax=float(p_vals.max()))
cmap = plt.get_cmap(cmap_name)

# =========================================================
# PLOT
# =========================================================
fig, ax = plt.subplots(figsize=(10, 8))

# Collect unique p legend handles (one per p)
p_handles = []

for p, f in file_info:
    mat = loadmat(f)

    eta = mat["eta_vec"].ravel()
    n_list = mat["n_list"].ravel().astype(int)
    A1 = mat["A1_final"]  # population A

    # sort n ordering
    order = np.argsort(n_list)
    n_list = n_list[order]
    A1 = A1[order]

    color = cmap(norm(p))

    # ---- plot MAIN curve (n_to_plot) WITHOUT label
    idx = np.where(n_list == n_to_plot)[0]
    if idx.size > 0:
        ax.plot(
            eta,
            A1[int(idx)],
            color=color,
            linewidth=linewidth,
            linestyle="-",
            label=None
        )

        # add p handle once
        p_handles.append(
            Line2D([0], [0], color=color, lw=linewidth, linestyle="-", label=f"p={p:g}")
        )

    # ---- extra n=2 curve only for p=1 (dashed) WITHOUT label
    if plot_n2_for_p1 and np.isclose(p, 1.0):
        idx2 = np.where(n_list == 2)[0]
        if idx2.size > 0:
            ax.plot(
                eta,
                A1[int(idx2)],
                color=color,
                linewidth=linewidth,
                linestyle="--",
                label=None
            )

# =========================================================
# STYLE
# =========================================================
ax.set_xlabel(r'$\eta$', fontsize=32)
ax.set_ylabel(r'population A', fontsize=32)
ax.set_ylim(0, 1)
ax.grid(False)
ax.tick_params(axis='both', labelsize=32)

# =========================================================
# TWO LEGENDS
#   1) line style legend (n=5 solid, n=2 dashed)
#   2) p legend (colors)
# =========================================================

# Legend 1: line styles (fixed black samples)
style_handles = [
    Line2D([0], [0], color="k", lw=linewidth, linestyle="-",  label=f"n={n_to_plot}"),
    Line2D([0], [0], color="k", lw=linewidth, linestyle="--", label="n=2 "),
]
leg_style = ax.legend(
    handles=style_handles,
    loc="lower left",
    bbox_to_anchor=(0.02, 0.028),
    fontsize=24,
    frameon=False,
)
ax.add_artist(leg_style)

# Legend 2: p values (colors)
# (optional) remove duplicates if something got appended twice
seen = set()
p_handles_unique = []
for h in p_handles:
    if h.get_label() not in seen:
        seen.add(h.get_label())
        p_handles_unique.append(h)

leg_p = ax.legend(
    handles=p_handles_unique,
    title="p values",
    loc="upper right",
    bbox_to_anchor=(1.0, 1.0),
    fontsize=24,
    title_fontsize=0,
    ncol=LEGEND_P_NCOL,
    frameon=False,
    columnspacing=1.0,
    handletextpad=0.4,
    borderaxespad=0.2,
)

fig.tight_layout()
plt.show()