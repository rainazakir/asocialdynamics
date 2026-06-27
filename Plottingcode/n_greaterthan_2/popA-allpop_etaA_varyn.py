import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

# ================= USER CHOICE =================
n_to_plot = [2,3,5]      # e.g. [3] or [2,5]
# =================================================

mat = loadmat("/content/DSB_results_n2_n3_n5_A1_vs_rest_0.92_p1.mat")

eta = mat["eta_vec"].ravel()
n_list = mat["n_list"].ravel().astype(int)
delta = mat["delta1rest"]

# keep ordering consistent
order = np.argsort(n_list)
n_list = n_list[order]
delta = delta[order]

colors = {
    2: "#08306B",
    3: "#2171B5",
    5: "#6BAED6",
}

plt.figure(figsize=(10,8))

for i, n in enumerate(n_list):

    if n not in n_to_plot:   # ← filter happens here
        continue

    plt.plot(
        eta,
        delta[i],
        color=colors.get(n, "blue"),
        linewidth=7,
        label=f"n={n}"
    )

plt.xticks(fontsize=32)
plt.yticks(fontsize=32)
plt.xlabel(r'$\eta$', fontsize=29)
plt.ylabel(r"Population A − others", fontsize=28)
plt.ylim(-1, 1)
plt.grid(False)
plt.legend(loc="best", fontsize=24)
plt.tight_layout()
plt.show()