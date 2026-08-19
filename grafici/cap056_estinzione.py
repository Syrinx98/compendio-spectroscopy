# la curva di estinzione della polvere, per il capitolo dell' arrossamento.
#
# il messaggio e' uno solo: la polvere assorbe MOLTO piu' nel blu che nel rosso, e da li' viene
# tutto il resto (lo spettro si arrossa, la stella sembra piu' fredda, il decremento di Balmer
# misurato viene piu' grande di 2.86).
#
# ho segnato dove cadono Hbeta (4861) e Halpha (6563), perche' e' esattamente il punto: sono due
# righe che escono dallo stesso posto, ma la polvere se ne mangia una piu' dell' altra, e da quel
# dislivello si ricava quanta ce n'e'.
#
# la curva e' l' andamento qualitativo della CCM89 nel visibile, normalizzato in banda V (5500 A).

import numpy as np
import matplotlib.pyplot as plt

lam = np.linspace(3000, 9000, 800)
x = 1e4 / lam                                   # numero d' onda in micron^-1
A_su_Av = (0.45 * x ** 1.8) / (0.45 * (1e4 / 5500) ** 1.8)     # normalizzata a 1 in banda V

fig, ax = plt.subplots(figsize=(9, 5.4))
ax.plot(lam, A_su_Av, lw=2.6, color="#6a3d9a")

# le bande, giusto per orientarsi
for centro, nome in ((3600, "U"), (4400, "B"), (5500, "V"), (7000, "R"), (9000, "I")):
    if centro <= 9000:
        ax.axvline(centro, color="#ccc", lw=0.8, ls=":")
        ax.text(centro, 0.06, nome, fontsize=9, ha="center", color="#999")

# le due righe di Balmer che si usano per misurare
for x0, nome, colore in ((4861, "H$\\beta$\n4861 A", "#1a5fb4"), (6563, "H$\\alpha$\n6563 A", "#c1440e")):
    y = np.interp(x0, lam, A_su_Av)
    ax.plot([x0], [y], "o", ms=9, color=colore, zorder=5)
    ax.vlines(x0, 0, y, color=colore, lw=1.2, ls="--")
    ax.text(x0, y + 0.12, nome, fontsize=9, ha="center", color=colore)

yb = np.interp(4861, lam, A_su_Av)
ya = np.interp(6563, lam, A_su_Av)
ax.annotate("", xy=(5700, ya), xytext=(5700, yb),
            arrowprops=dict(arrowstyle="<->", lw=1.6, color="#333"))
ax.text(5800, (ya + yb) / 2, "questo dislivello e' tutto:\n$H\\beta$ viene mangiata piu' di $H\\alpha$,\n"
                             "quindi il rapporto misurato\nsale sopra 2.86",
        fontsize=9, va="center", color="#333")

ax.text(3150, 1.85, "il blu viene assorbito\nmolto piu' del rosso", fontsize=10, color="#6a3d9a")

ax.set_xlabel("$\\lambda$  [A]")
ax.set_ylabel("$A(\\lambda) / A(V)$      estinzione, normalizzata in banda V")
ax.set_title("la polvere non assorbe uguale a tutte le lunghezze d' onda", fontsize=12)
ax.set_ylim(0, 2.4)
ax.set_xlim(3000, 9000)
ax.grid(alpha=0.2)

fig.tight_layout()
fig.savefig("../data/curva_estinzione.png", dpi=140)
print("scritto data/curva_estinzione.png")
