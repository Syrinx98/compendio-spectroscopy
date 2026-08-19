# due disegni per il capitolo dell' atomo a due livelli.
#
# 1) lo schema dei quattro processi: due che portano su, due che portano giu'. il punto e' far
#    vedere che il canale radiativo in salita (U B12) si butta via, e che dei due modi di scendere
#    uno produce un fotone che esce (lo vedo) e l' altro no (resta calore).
#
# 2) l' emissivita' in funzione della densita', in log-log: sotto Nc va come Ne^2, sopra come Ne.
#    e' il grafico che spiega da solo perche' le righe proibite si vedono solo dove il gas e' rado.

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- 1. i quattro processi
fig, ax = plt.subplots(figsize=(11, 5.4))

for y, nome in ((0.0, "livello 1"), (1.0, "livello 2")):
    ax.hlines(y, 0.4, 6.4, lw=3, color="#333")
    ax.text(6.55, y, nome, va="center", fontsize=11)

frecce = [
    (1.0, 0, 1, "assorbo un fotone\n$N_1 U B_{12}$", "#999", "si butta via:\nil campo e' diluito"),
    (2.4, 0, 1, "mi urta un elettrone\n$N_1 N_e Q_{12}$", "#c1440e", "l' unica strada\nche resta"),
    (4.0, 1, 0, "emetto un fotone\n$N_2 A_{21}$", "#1a7a3a", "il fotone esce:\nla riga la vedo"),
    (5.6, 1, 0, "mi urta un elettrone\n$N_2 N_e Q_{21}$", "#1a5fb4", "l' energia resta\nnel gas: calore"),
]

for x, ya, yb, testo, colore, nota in frecce:
    ax.annotate("", xy=(x, yb), xytext=(x, ya),
                arrowprops=dict(arrowstyle="->", lw=2.2, color=colore,
                                linestyle="--" if colore == "#999" else "-"))
    ax.text(x, 1.14, testo, fontsize=9, color=colore, ha="center", va="bottom")
    ax.text(x, -0.22, nota, fontsize=8.5, color=colore, ha="center", va="top", style="italic")

ax.text(1.7, 1.92, "per salire", fontsize=12, weight="bold", ha="center")
ax.text(4.8, 1.92, "per scendere", fontsize=12, weight="bold", ha="center")
ax.plot([0.4, 3.0], [1.85, 1.85], lw=1, color="#bbb")
ax.plot([3.5, 6.4], [1.85, 1.85], lw=1, color="#bbb")

ax.set_xlim(0.1, 7.6)
ax.set_ylim(-0.85, 2.15)
ax.axis("off")
fig.tight_layout()
fig.savefig("../data/due_livelli_processi.png", dpi=140)
print("scritto data/due_livelli_processi.png")

# ---------------------------------------------------------------- 2. emissivita' contro densita'
Ne = np.logspace(0, 8, 500)
Nc = 1e4                      # densita' critica di esempio

# eps ~ Ne * N2/N1 * A21, con N2/N1 = Ne Q12 / (A21 + Ne Q21). in unita' comode:
eps = Ne * (Ne / (1 + Ne / Nc))

fig, ax = plt.subplots(figsize=(8.5, 5))
ax.loglog(Ne, eps, lw=2.5, color="#1a5fb4")
ax.axvline(Nc, color="#c1440e", lw=1.8, ls="--")
ax.text(Nc * 1.3, 2e1, "$N_c = A_{21}/Q_{21}$", color="#c1440e", fontsize=10, rotation=90,
        va="bottom")

ax.text(60, 1e6, "$N_e \\ll N_c$\n$\\varepsilon \\propto N_e^2$\n\n$A_{21}$ si cancella:\nogni eccitazione\ndiventa un fotone",
        fontsize=9, ha="center", color="#1a5fb4")
ax.text(3e6, 3e3, "$N_e \\gg N_c$\n$\\varepsilon \\propto N_e$\n\ntorna Boltzmann:\nle righe lente\nsi spengono",
        fontsize=9, ha="center", color="#666")

# la fascia dove stanno davvero le nebulose
ax.axvspan(1e2, 1e4, color="#1a7a3a", alpha=0.10)
ax.text(1e3, 2, "qui stanno\nle nebulose", fontsize=8.5, ha="center", color="#1a7a3a")

ax.set_xlabel("$N_e$   densita' elettronica  [cm$^{-3}$]")
ax.set_ylabel("$\\varepsilon$   emissivita' della riga")
ax.set_title("la pendenza cambia alla densita' critica", fontsize=12)
ax.set_ylim(1, 1e10)
ax.grid(alpha=0.25, which="both")

fig.tight_layout()
fig.savefig("../data/emissivita_densita.png", dpi=140)
print("scritto data/emissivita_densita.png")
