# la scala dei livelli dell' idrogeno con le tre serie, per il capitolo dei numeri in tasca.
#
# quello che si deve vedere a colpo d' occhio:
#   - i livelli si infittiscono salendo e si accumulano contro lo zero (elettrone libero)
#   - ogni serie parte da un livello diverso, e la sua soglia vale 13.6/n^2
#   - Lyman sta nell' UV, Balmer nel visibile: e' per quello che l' idrogeno si guarda con Balmer
#
# lo zero della scala e' l' elettrone libero e fermo, quindi i livelli legati stanno tutti sotto.
# le etichette le scrivo solo fino a n=4: piu' su si accavallerebbero, e tanto il punto e' proprio
# che li' i livelli si ammassano.

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9.5, 6.2))

XA, XB = 1.6, 6.2                      # dove cominciano e finiscono le righe dei livelli

for n in range(1, 13):
    E = -13.6 / n ** 2
    ax.hlines(E, XA, XB, lw=2.2 if n <= 3 else 1.0, color="#333")
    if n <= 4:
        ax.text(XB + 0.12, E, "$n=%d$      %.2f eV" % (n, E), va="center", fontsize=9.5)

ax.text(XB + 0.12, -0.30, "$n=5, 6, 7 \\dots$   si ammassano qui", va="center", fontsize=8.5,
        color="#777")

# lo zero: elettrone libero, e sopra il continuo
ax.hlines(0, XA, XB, lw=2.4, color="#c1440e")
ax.text(XB + 0.12, 0.28, "$n=\\infty$      0 eV      elettrone libero", va="center", fontsize=9.5,
        color="#c1440e")
ax.fill_between([XA, XB], 0, 2.6, color="#c1440e", alpha=0.07)
ax.text((XA + XB) / 2, 1.3, "continuo:  qui l' elettrone e' libero\ne la sua energia non e' quantizzata",
        fontsize=9.5, ha="center", color="#c1440e")

# le tre serie: una freccia spessa fino al continuo (la soglia) e qualche transizione fra livelli
serie = [(2.3, 1, "Lyman", "912 A  -  UV", "#6a3d9a"),
         (3.6, 2, "Balmer", "3646 A  -  visibile", "#1a5fb4"),
         (4.9, 3, "Paschen", "8208 A  -  infrarosso", "#1a7a3a")]

for x, n, nome, dove, colore in serie:
    base = -13.6 / n ** 2
    # la soglia della serie
    ax.annotate("", xy=(x, base), xytext=(x, 0),
                arrowprops=dict(arrowstyle="->", lw=2.6, color=colore))
    ax.text(x - 0.1, base / 2, "%.1f eV" % (-base), fontsize=8.5, color=colore,
            ha="right", va="center", rotation=90)
    # tre transizioni della serie, spostate a destra per non sovrapporsi alla soglia
    for k, m in enumerate((n + 1, n + 2, n + 3)):
        ax.annotate("", xy=(x + 0.22 + 0.16 * k, base), xytext=(x + 0.22 + 0.16 * k, -13.6 / m ** 2),
                    arrowprops=dict(arrowstyle="->", lw=1.3, color=colore, alpha=0.8))

ax.text(2.3, -15.6, "Lyman\n912 A - UV", fontsize=9, ha="center", color="#6a3d9a")
ax.text(3.6, -5.6, "Balmer\n3646 A - visibile", fontsize=9, ha="center", color="#1a5fb4")
ax.text(6.0, -2.6, "Paschen\n8208 A - infrarosso", fontsize=9, ha="center", color="#1a7a3a")

ax.text(0.35, 2.9, "livelli dell' idrogeno:   $E_n = -13.6/n^2$", fontsize=13, weight="bold")

ax.set_ylim(-17.2, 3.6)
ax.set_xlim(0.3, 9.6)
ax.set_ylabel("energia  [eV]")
ax.set_xticks([])
ax.set_yticks([-13.6, -10, -6, -3.4, -1.5, 0])
for lato in ("top", "right", "bottom"):
    ax.spines[lato].set_visible(False)

fig.tight_layout()
fig.savefig("../data/livelli_idrogeno.png", dpi=140)
print("scritto data/livelli_idrogeno.png")
