# il continuo di una nebulosa con i gradini, che e' la cosa che a parole non si capisce mai.
#
# quello che si deve vedere: arrivando da destra (lunghezze d' onda lunghe, fotoni fiacchi) il
# continuo sale di colpo ogni volta che si passa una soglia, perche' li' si apre un canale di
# cattura nuovo. sotto quella soglia le catture su quel livello non possono proprio contribuire,
# visto che il fotone minimo che producono vale 13.6/n^2.
#
# le soglie: 8208 A (n=3, Paschen), 3646 A (n=2, Balmer), 912 A (n=1, Lyman, fuori dal disegno).
# in sovrapposizione ci metto il free-free, che invece e' liscio e non ha nessun gradino.

import numpy as np
import matplotlib.pyplot as plt

lam = np.linspace(2000, 11000, 3000)

# ogni livello contribuisce solo SOTTO la sua lambda di soglia, e poi cala andando verso il blu
def canale(soglia, peso, scala):
    y = np.where(lam <= soglia, peso * np.exp(-(soglia - lam) / scala), 0.0)
    return y

fb = canale(3646, 1.00, 2600) + canale(8208, 0.42, 3200)
ff = 0.30 * np.ones_like(lam)                  # liscio, senza soglie

fig, ax = plt.subplots(figsize=(9, 5.2))

ax.plot(lam, fb + ff, lw=2.5, color="#1a5fb4", label="totale (free-bound + free-free)")
ax.plot(lam, ff, lw=1.8, ls="--", color="#c1440e", label="solo free-free: liscio, nessun gradino")

for x, nome, n in ((3646, "salto di Balmer", 2), (8208, "salto di Paschen", 3)):
    ax.axvline(x, color="#777", lw=1, ls=":")
    ax.text(x + 90, 1.28, "%s\n%d A   ($n=%d$)" % (nome, x, n), fontsize=8.5, color="#444")

ax.annotate("arrivando da qui i fotoni sono fiacchi:\nle catture su $n=2$ non possono contribuire",
            xy=(4600, 0.36), xytext=(5600, 0.72), fontsize=8.5, color="#1a5fb4",
            arrowprops=dict(arrowstyle="->", lw=1, color="#1a5fb4"))
ax.annotate("appena passata la soglia si apre\nun canale nuovo: l' emissione salta su",
            xy=(3560, 1.05), xytext=(2400, 0.72), fontsize=8.5, color="#1a5fb4",
            arrowprops=dict(arrowstyle="->", lw=1, color="#1a5fb4"))

ax.set_xlabel("$\\lambda$  [A]        (verso destra i fotoni sono meno energetici)")
ax.set_ylabel("emissione del continuo")
ax.set_title("il continuo di ricombinazione ha i gradini, il free-free no", fontsize=12)
ax.set_ylim(0, 1.6)
ax.set_xlim(2000, 11000)
ax.grid(alpha=0.2)
ax.legend(fontsize=9, loc="upper right")

fig.tight_layout()
fig.savefig("../data/continui_gradini.png", dpi=140)
print("scritto data/continui_gradini.png")
