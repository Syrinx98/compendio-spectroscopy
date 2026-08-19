# il profilo di ionizzazione dentro una sfera di Stromgren, piu' la stratificazione.
#
# il disegno serve a una cosa sola: far vedere che il bordo NON sfuma. la frazione di idrogeno
# ionizzato resta incollata a 1 per tutto il raggio e poi crolla dentro una buccia sottilissima
# (0.005 pc contro parecchi pc di raggio, quindi nel disegno il bordo e' gia' esagerato).
#
# il secondo pannello e' la stratificazione: He III dentro, poi He II, poi H II. i raggi sono
# diversi perche' cambia Q, cioe' quanti fotoni ci sono sopra la soglia, non perche' cambi alpha.

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- 1. il profilo e il bordo
r = np.linspace(0, 1.4, 1500)
Rs = 1.0
spessore = 0.012                          # il bordo, gia' disegnato piu' largo del vero
x = np.clip((r - Rs) / spessore, -40, 40)
ion = 1 / (1 + np.exp(x))                 # crollo brusco attorno a Rs

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.5))

a1.plot(r, ion, lw=2.5, color="#1a5fb4")
a1.axvline(Rs, color="#c1440e", lw=1.5, ls="--")
a1.text(Rs - 0.055, 0.62, "$R_S$", color="#c1440e", fontsize=12)

a1.fill_between(r, 0, ion, color="#1a5fb4", alpha=0.12)
a1.text(0.35, 0.5, "tutto ionizzato\n(H II)", fontsize=10, ha="center", color="#1a5fb4")
a1.text(1.26, 0.5, "tutto neutro\n(H I)", fontsize=10, ha="center", color="#555")

a1.annotate("il bordo e' spesso\n~0.005 pc, contro\n1-100 pc di raggio",
            xy=(Rs, 0.5), xytext=(0.62, 0.85), fontsize=8.5, color="#c1440e",
            arrowprops=dict(arrowstyle="->", lw=1, color="#c1440e"))

a1.set_xlabel("distanza dalla stella  /  $R_S$")
a1.set_ylabel("frazione di idrogeno ionizzato")
a1.set_title("la ionizzazione non sfuma: crolla", fontsize=11)
a1.set_ylim(-0.05, 1.15)
a1.grid(alpha=0.2)

# ---------------------------------------------------------------- 2. la stratificazione
a2.set_aspect("equal")
gusci = [(1.00, "#1a5fb4", "H II        (13.6 eV)"),
         (0.62, "#1a7a3a", "He II      (24.6 eV)"),
         (0.30, "#c1440e", "He III     (54.4 eV)")]

for raggio, colore, nome in gusci:
    a2.add_patch(plt.Circle((0, 0), raggio, color=colore, alpha=0.22))
    a2.add_patch(plt.Circle((0, 0), raggio, fill=False, color=colore, lw=1.8))
    a2.text(0, raggio - 0.09, nome, fontsize=8.5, ha="center", color=colore)

a2.plot([0], [0], "*", ms=16, color="#e8a30c")
a2.text(0, -1.32, "piu' alta e' la soglia, meno fotoni ci sono sopra,\npiu' piccola e' la sfera:"
                  " cambia $Q$, non $\\alpha$",
        fontsize=9, ha="center", color="#444")

a2.set_xlim(-1.15, 1.15)
a2.set_ylim(-1.5, 1.15)
a2.axis("off")
a2.set_title("stratificazione: sfere concentriche", fontsize=11)

fig.tight_layout()
fig.savefig("../data/stromgren_profilo.png", dpi=140)
print("scritto data/stromgren_profilo.png")
