# due disegni per il capitolo delle righe in assorbimento.
#
# 1) la EW disegnata come rettangolo nero: e' il modo piu' veloce per capire cosa vuol dire
#    "larghezza equivalente", cioe' che si prende tutta la luce che manca e la si impacchetta.
#
# 2) gaussiana contro lorentziana contro voigt. il punto e' far vedere PERCHE' il voigt ha nucleo
#    gaussiano e ali lorentziane: la gaussiana va a zero come e^(-x^2) e la lorentziana come x^(-2),
#    quindi vicino al centro comanda la prima e lontano restano solo le ali della seconda.
#    va guardato in scala log sull' asse y, se no le ali non si vedono proprio.

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- 1. la EW come rettangolo
x = np.linspace(-6, 6, 600)
riga = 1 - 0.6 * np.exp(-x ** 2 / 1.2)          # profilo finto, continuo normalizzato a 1
ew = np.trapz(1 - riga, x)                       # l' area che manca

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)

a1.plot(x, riga, lw=2, color="#1a5fb4")
a1.axhline(1, lw=1.2, ls="--", color="#888")
a1.fill_between(x, riga, 1, color="#1a5fb4", alpha=0.25)
a1.text(0, 0.78, "questa area\ne' la luce che manca", fontsize=9, ha="center", color="#1a5fb4")
a1.text(3.4, 1.03, "continuo", fontsize=9, color="#888")
a1.set_title("la riga vera", fontsize=11)

a2.plot(x, np.where(np.abs(x) < ew / 2, 0, 1), lw=2, color="#333")
a2.axhline(1, lw=1.2, ls="--", color="#888")
a2.fill_between(x, np.where(np.abs(x) < ew / 2, 0, 1), 1, color="#333", alpha=0.75)
a2.annotate("", xy=(-ew / 2, 0.5), xytext=(ew / 2, 0.5),
            arrowprops=dict(arrowstyle="<->", lw=1.5, color="#c1440e"))
a2.text(0, 0.56, "EW = %.2f A" % ew, fontsize=10, ha="center", color="#c1440e")
a2.set_title("lo stesso buco, impacchettato in un rettangolo nero", fontsize=11)

for a in (a1, a2):
    a.set_xlabel("$\\lambda - \\lambda_0$  [A]")
    a.set_ylim(0, 1.15)
    a.grid(alpha=0.2)
a1.set_ylabel("flusso / continuo")

fig.tight_layout()
fig.savefig("../data/ew_rettangolo.png", dpi=140)
print("scritto data/ew_rettangolo.png")

# ---------------------------------------------------------------- 2. gaussiana, lorentziana, voigt
x = np.linspace(-8, 8, 1200)
g = np.exp(-x ** 2)                      # e^(-x^2): crolla in fretta
l = 1 / (1 + x ** 2)                     # x^(-2) lontano: crolla piano
v = np.convolve(g, l, mode="same")
v = v / v.max()

fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(x, g, lw=2, color="#1a7a3a", label="gaussiana  (Doppler, microturbolenza)")
ax.semilogy(x, l, lw=2, color="#c1440e", label="lorentziana  (naturale, collisionale)")
ax.semilogy(x, v, lw=2.6, color="#1a5fb4", label="Voigt = convoluzione delle due")

ax.axvspan(-1.2, 1.2, color="#1a7a3a", alpha=0.08)
ax.text(0, 2.5e-4, "qui comanda\nla gaussiana", fontsize=9, ha="center", color="#1a7a3a")
ax.text(5.4, 4e-4, "qui la gaussiana\ne' gia' sparita:\nrestano le ali\nlorentziane",
        fontsize=9, ha="center", color="#c1440e")

ax.set_xlabel("distanza dal centro riga")
ax.set_ylabel("profilo normalizzato  (scala log)")
ax.set_title("nucleo gaussiano, ali lorentziane: si vede solo in scala logaritmica", fontsize=12)
ax.set_ylim(8e-5, 6)
ax.grid(alpha=0.25, which="both")
ax.legend(fontsize=9, loc="lower center", ncol=1, framealpha=0.95)

fig.tight_layout()
fig.savefig("../data/profili_voigt.png", dpi=140)
print("scritto data/profili_voigt.png")
