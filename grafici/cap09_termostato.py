# il grafico del termostato: perche' una nebulosa si assesta a 10^4 K e non sale all' infinito.
#
# il punto del disegno sono le DUE FORME, non i numeri:
#   - il riscaldamento e' quasi piatto, perche' l' energia che il fotone regala all' elettrone la
#     decide lo spettro della stella, non la temperatura del gas
#   - il raffreddamento sale ripidissimo, perche' dentro ha e^(-dE/kT): sotto una certa temperatura
#     gli elettroni non arrivano ai livelli metastabili e il canale e' proprio spento
#   - dove si incrociano c'e' la temperatura di equilibrio
#
# ho messo anche la curva del solo free-free (nebulosa senza metalli) per far vedere che li'
# l' incrocio si sposta molto piu' a destra: sono i metalli a tenere fredde le nebulose.

import numpy as np
import matplotlib.pyplot as plt

T = np.linspace(3000, 150000, 2000)

# riscaldamento: dipende dalla stella, non da Te. cala solo pianissimo
# tarato perche' l' incrocio col raffreddamento totale cada proprio a 10^4 K
gamma = 1.02e-24 * (T / 1e4) ** -0.35

# raffreddamento per righe proibite: il pezzo che comanda e' l' esponenziale di boltzmann.
# 2.877e4 K e' dE/kB della riga 5007 di [O III]
lam_coll = 1.57e-21 * np.exp(-2.877e4 / T) / np.sqrt(T)

# free-free: sale come radice di T, senza soglie. e' l' unico che resta se non ci sono metalli
lam_ff = 1.4e-27 * np.sqrt(T)

fig, ax = plt.subplots(figsize=(8, 5.5))

ax.loglog(T, gamma, lw=2.5, color="#c1440e", label="riscaldamento  $\\Gamma$  (fotoionizzazione)")
ax.loglog(T, lam_coll + lam_ff, lw=2.5, color="#1a5fb4",
          label="raffreddamento  $\\Lambda$  (righe proibite + free-free)")
ax.loglog(T, lam_ff, lw=1.6, ls="--", color="#777", label="solo free-free (nebulosa di solo H)")

# gli incroci: dove gamma = lambda
def incrocio(curva):
    i = np.argmin(np.abs(gamma - curva))
    return T[i], gamma[i]

Teq, yeq = incrocio(lam_coll + lam_ff)
Tff, yff = incrocio(lam_ff)

ax.plot([Teq], [yeq], "o", ms=9, color="#111", zorder=5)
ax.annotate("equilibrio\n$T_e \\simeq %d$ K" % round(Teq, -2),
            xy=(Teq, yeq), xytext=(Teq * 0.30, yeq * 5), fontsize=10, ha="center",
            arrowprops=dict(arrowstyle="->", lw=1.2, color="#111"))

ax.plot([Tff], [yff], "o", ms=7, color="#777", zorder=5)
ax.annotate("senza metalli\nl' incrocio si sposta qui", xy=(Tff, yff), xytext=(Tff * 0.42, yff * 3.2),
            fontsize=9, color="#555", ha="center",
            arrowprops=dict(arrowstyle="->", lw=1, color="#777"))

# le due frecce che spiegano perche' e' STABILE
ax.annotate("", xy=(Teq * 1.03, yeq * 0.42), xytext=(Teq * 1.9, yeq * 0.42),
            arrowprops=dict(arrowstyle="->", lw=1.8, color="#1a7a3a"))
ax.text(Teq * 2.0, yeq * 0.38, "se sale, il raffreddamento\nesplode e la ributta giu'",
        fontsize=8.5, color="#1a7a3a", va="center")

ax.set_xlabel("$T_e$   temperatura degli elettroni del gas  [K]")
ax.set_ylabel("tassi, normalizzati per $N_e N_p$")
ax.set_title("il termostato: dove le due curve si incrociano sta la temperatura", fontsize=12)
ax.set_xlim(3000, 150000)
ax.set_ylim(3e-26, 3e-23)
ax.grid(alpha=0.25, which="both")
ax.legend(fontsize=9, loc="lower left")

fig.tight_layout()
fig.savefig("../data/termostato.png", dpi=140)
print("scritto data/termostato.png")
