# la sezione d' urto di fotoionizzazione dell' idrogeno, che va come nu^-3.
#
# serve a far digerire la cosa controintuitiva del capitolo: un fotone MOLTO energetico NON
# ionizza meglio, ionizza peggio. la sezione d' urto crolla come il cubo della frequenza, quindi
# quei fotoni la nube quasi non la vedono e ci passano attraverso.
#
# nel secondo pannello traduco la stessa cosa in una lunghezza: il libero cammino medio 1/(N sigma),
# cioe' quanto va lontano dentro la nube un fotone di quella energia prima di essere mangiato.
# e' anche il conto che da' lo spessore del bordo di Stromgren.

import numpy as np
import matplotlib.pyplot as plt

E = np.linspace(13.6, 100, 600)            # eV, si parte dalla soglia
sigma = 6.3e-18 * (13.6 / E) ** 3          # cm^2, l' andamento nu^-3 normalizzato alla soglia
N = 10.0                                   # cm^-3 di idrogeno neutro
L_pc = 1 / (N * sigma) / 3.09e18           # libero cammino medio, in parsec

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6))

a1.plot(E, sigma, lw=2.6, color="#1a5fb4")
a1.set_yscale("log")
a1.axvline(13.6, color="#c1440e", lw=1.4, ls="--")
a1.text(14.5, 3e-18, "soglia\n13.6 eV", fontsize=9, color="#c1440e")
a1.plot([13.6], [6.3e-18], "o", ms=8, color="#c1440e", zorder=5)

a1.annotate("qui $\\sigma$ e' massima:\nquesti fotoni vengono\nmangiati subito",
            xy=(16, 3.5e-18), xytext=(34, 3.5e-18), fontsize=9, color="#1a5fb4",
            arrowprops=dict(arrowstyle="->", lw=1, color="#1a5fb4"))
a1.annotate("qui la nube e' quasi\ntrasparente: i fotoni duri\npassano oltre",
            xy=(85, 3e-20), xytext=(40, 6e-20), fontsize=9, color="#666",
            arrowprops=dict(arrowstyle="->", lw=1, color="#666"))

a1.set_xlabel("energia del fotone  [eV]")
a1.set_ylabel("$\\sigma_{bf}$  [cm$^2$]")
a1.set_title("$\\sigma \\propto \\nu^{-3}$: crolla in fretta", fontsize=11)
a1.grid(alpha=0.2, which="both")

a2.plot(E, L_pc, lw=2.6, color="#1a7a3a")
a2.set_yscale("log")
a2.axhline(0.005, color="#c1440e", lw=1.4, ls="--")
a2.text(60, 0.0056, "0.005 pc = lo spessore del bordo\ndi una sfera di Stromgren",
        fontsize=8.5, color="#c1440e", ha="center")

a2.set_xlabel("energia del fotone  [eV]")
a2.set_ylabel("libero cammino medio  $1/(N\\sigma)$  [pc]")
a2.set_title("quanto entra dentro la nube, con $N = 10$ cm$^{-3}$", fontsize=11)
a2.grid(alpha=0.2, which="both")

fig.tight_layout()
fig.savefig("../data/sezione_urto.png", dpi=140)
print("scritto data/sezione_urto.png")
