# costruisce la wiki navigabile: un file html per capitolo, dentro sito_wiki\.
#
# differenza con build_compendio.py: quello fa UN file solo da leggere sul telefono, questo fa un
# sito vero con una pagina per capitolo, il menu laterale sempre visibile e i tasti avanti/indietro
# in fondo. Si legge meglio da computer, e i link fra capitoli funzionano come link veri.
#
#   python wiki.py       ->  docs\index.html  (poi doppio click, oppure GitHub Pages)
#
# i file si ordinano da soli mettendoli in fila per nome (a0_, a1_, a2_ e poi c02_, c03_ ...),
# quindi aggiungerne uno non richiede di toccare questo file. il numero che si vede nel menu
# e' quello della dispensa, letto dal titolo del capitolo.
#
# nota sulle formule: python-markdown non sa niente di latex e dentro $...$ si mangerebbe gli
# underscore trasformandoli in corsivo (N_e diventerebbe N<em>e</em>). quindi prima di convertire
# si mettono da parte i blocchi math e si rimettono dentro dopo, intatti.

import io
import os
import re
import shutil

import markdown

BASE = os.path.dirname(os.path.abspath(__file__))
SITO = os.path.join(BASE, "docs")
IMMAGINI = os.path.join(BASE, "data")                    # i grafici stanno qui dentro, li fa grafici\

CSS = """
:root { --bg:#fff; --fg:#1a1a1a; --bg2:#f4f4f4; --bordo:#ddd; --link:#0b5fa5; --nota:#7a5c00;
        --barra:#fafafa; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#16181c; --fg:#e6e6e6; --bg2:#22252b; --bordo:#3a3f47; --link:#6bb6ff;
          --nota:#e0c060; --barra:#1b1e23; }
}
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--fg); margin: 0;
       font: 17px/1.7 -apple-system, "Segoe UI", system-ui, sans-serif; }

/* impaginazione: menu fisso a sinistra, testo al centro. sotto i 900px il menu va in cima */
.riga { display: flex; align-items: flex-start; max-width: 1180px; margin: 0 auto; }
.menu { width: 290px; flex: none; padding: 26px 18px; position: sticky; top: 0;
        max-height: 100vh; overflow-y: auto; border-right: 1px solid var(--bordo);
        background: var(--barra); font-size: 14.5px; }
.menu h2 { font-size: 15px; margin: 0 0 14px; border: 0; padding: 0; }
.menu ul { margin: 0; padding: 0; list-style: none; }
.menu li { margin: 9px 0; line-height: 1.35; display: flex; gap: 9px; }
.menu .num { flex: none; width: 46px; text-align: right; color: #999;
             font-variant-numeric: tabular-nums; }
.menu a.qui { font-weight: 600; color: var(--fg); }
.testo { flex: 1; min-width: 0; padding: 26px 30px 100px; max-width: 800px; }
@media (max-width: 900px) {
  .riga { display: block; }
  .menu { width: auto; position: static; max-height: none; border-right: 0;
          border-bottom: 1px solid var(--bordo); }
  .testo { padding: 20px 16px 80px; }
}

a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }
h1 { font-size: 25px; margin: 6px 0 16px; line-height: 1.3; }
h2 { font-size: 20px; margin-top: 34px; padding-bottom: 6px; border-bottom: 1px solid var(--bordo); }
h3 { font-size: 17px; margin: 26px 0 10px; padding: 9px 12px; background: var(--bg2);
     border-left: 3px solid var(--link); border-radius: 0 4px 4px 0; }
h4 { font-size: 16px; margin: 22px 0 8px; color: var(--link); }
code { background: var(--bg2); padding: 2px 5px; border-radius: 4px; font-size: 15px; }
pre { background: var(--bg2); padding: 12px; border-radius: 6px; overflow-x: auto; }
img { max-width: 100%; border-radius: 6px; background: #fff; }
hr { border: 0; border-top: 1px solid var(--bordo); margin: 30px 0; }
blockquote { border-left: 3px solid var(--link); margin: 18px 0; padding: 2px 0 2px 14px;
             background: var(--bg2); border-radius: 0 4px 4px 0; }
blockquote p { margin: 8px 0; }
table { border-collapse: collapse; display: block; overflow-x: auto; margin: 16px 0; }
td, th { border: 1px solid var(--bordo); padding: 6px 10px; }
th { background: var(--bg2); }
mjx-container { overflow-x: auto; overflow-y: hidden; max-width: 100%; }
/* le "note subito cosi' de botto": in corsivo grassetto nel markdown, qui si fanno notare */
em strong, strong em { color: var(--nota); }
/* avanti / indietro in fondo alla pagina */
.piedi { display: flex; justify-content: space-between; gap: 14px; margin-top: 60px;
         padding-top: 18px; border-top: 1px solid var(--bordo); font-size: 15px; }
.piedi a { display: block; max-width: 46%; }
.piedi .avanti { text-align: right; margin-left: auto; }
"""

PAGINA = """<!doctype html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo}</title>
<style>{css}</style>
<script>window.MathJax = {{ tex: {{ inlineMath: [['$','$']], displayMath: [['$$','$$']] }} }};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head><body><div class="riga">
<nav class="menu"><h2><a href="index.html">Compendio di<br>Astronomical Spectroscopy</a></h2>
<ul>{menu}</ul></nav>
<main class="testo">
{corpo}
<div class="piedi">{piedi}</div>
</main>
</div></body></html>
"""


def proteggi_math(testo):
    pezzi = []

    def via(m):
        pezzi.append(m.group(0))
        return "\x00M%d\x00" % (len(pezzi) - 1)

    testo = re.sub(r"\$\$.+?\$\$", via, testo, flags=re.S)
    testo = re.sub(r"(?<!\$)\$[^$\n]+?\$", via, testo)
    return testo, pezzi


def capitoli():
    # due famiglie di file, e l' ordine viene da solo mettendoli in fila per nome:
    #   a0_, a1_, a2_   le pagine di apertura, che non sono capitoli della dispensa
    #   c02_, c03_ ...  i capitoli veri, numerati come nelle note (c055_ e' il paragrafo 5.5)
    trovati = [f for f in os.listdir(BASE)
               if re.match(r"^[ac]\d+[a-z]?_.+\.md$", f)
               and os.path.getsize(os.path.join(BASE, f)) > 30]
    return sorted(trovati)


def titolo_di(nome):
    testo = io.open(os.path.join(BASE, nome), encoding="utf-8").read()
    m = re.search(r"^#\s+(.+)$", testo, re.M)
    t = m.group(1).strip() if m else nome
    t = re.sub(r"\\;|\\quad|\\,|[$\\]", " ", t)          # via il latex dal titolo
    return re.sub(r"\s+", " ", t).strip()


def main():
    md = markdown.Markdown(extensions=["extra", "sane_lists", "nl2br"])
    elenco = capitoli()
    titoli = [titolo_di(n) for n in elenco]
    usciti = [n[:-3] + ".html" for n in elenco]
    # la copertina e' anche index.html
    usciti[0] = "index.html"

    # i titoli sono fatti "5.5 - Righe di ricombinazione ...": nel menu il numero va in una
    # colonna sua, se no si perde in mezzo al testo. le pagine di apertura non ce l'hanno
    numeri, nomi = [], []
    for t in titoli:
        m = re.match(r"^([\d.\-]+)\s+-\s+(.+)$", t)
        numeri.append(m.group(1) if m else "")
        nomi.append(m.group(2) if m else t)

    if os.path.isdir(SITO):
        shutil.rmtree(SITO)
    os.makedirs(SITO)
    if os.path.isdir(IMMAGINI):
        shutil.copytree(IMMAGINI, os.path.join(SITO, "data"))

    for i, nome in enumerate(elenco):
        testo = io.open(os.path.join(BASE, nome), encoding="utf-8").read()
        testo, math = proteggi_math(testo)
        md.reset()
        corpo = md.convert(testo)
        for k, p in enumerate(math):
            corpo = corpo.replace("\x00M%d\x00" % k, p)

        # i link fra capitoli: c03_trasporto.md -> c03_trasporto.html (e la copertina -> index.html)
        corpo = re.sub(r'href="a0_[^"]*\.md"', 'href="index.html"', corpo)
        corpo = re.sub(r'(href="[ac]\d+[a-z]?_[^"]+?)\.md"', r'\1.html"', corpo)

        # il numero nel menu e' quello della dispensa, preso dal titolo stesso: se usassi una
        # lista numerata l'html conterebbe 1, 2, 3... e direbbe una cosa diversa dal titolo
        menu = "".join(
            '<li><span class="num">%s</span><a href="%s"%s>%s</a></li>'
            % (numeri[j], usciti[j], ' class="qui"' if j == i else "", nomi[j])
            for j in range(len(elenco)))

        piedi = []
        if i > 0:
            piedi.append('<a href="%s">&larr; %s</a>' % (usciti[i-1], titoli[i-1]))
        if i < len(elenco) - 1:
            piedi.append('<a class="avanti" href="%s">%s &rarr;</a>' % (usciti[i+1], titoli[i+1]))

        io.open(os.path.join(SITO, usciti[i]), "w", encoding="utf-8").write(
            PAGINA.format(titolo=titoli[i], css=CSS, menu=menu, corpo=corpo,
                          piedi="".join(piedi)))
        print("   ", nome, "->", usciti[i])

    print("\nfatto. apri:", os.path.join(SITO, "index.html"))


if __name__ == "__main__":
    main()
