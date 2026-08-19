# mette tutto il compendio in UN file html autoportante, da leggere sul telefono.
#
# stessa idea di ..\esame\tutto.py, ma qui non c'e' una lista di file scritta a mano: i capitoli
# sono numerati (00_, 01_, 02_ ...) quindi basta ordinarli per nome e vengono da soli. Se ne
# aggiungi uno nuovo, lo prende senza toccare niente.
#
#   python build_compendio.py     ->  sito\compendio.html
#
# le immagini finiscono dentro l'html in base64, cosi' il file e' uno solo: te lo mandi su
# telegram o te lo mailli e si apre ovunque, anche senza la cartella dietro.

import base64
import io
import os
import re

import markdown

BASE = os.path.dirname(os.path.abspath(__file__))
FUORI = os.path.join(BASE, "sito", "compendio.html")

CSS = """
:root { --bg:#fff; --fg:#1a1a1a; --bg2:#f4f4f4; --bordo:#ddd; --link:#0b5fa5; --nota:#7a5c00; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#16181c; --fg:#e6e6e6; --bg2:#22252b; --bordo:#3a3f47; --link:#6bb6ff;
          --nota:#e0c060; }
}
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--fg); margin: 0;
       font: 17px/1.7 -apple-system, "Segoe UI", system-ui, sans-serif; }
.wrap { max-width: 780px; margin: 0 auto; padding: 0 16px 120px; }
a { color: var(--link); text-decoration: none; }
h1 { font-size: 25px; margin: 30px 0 14px; line-height: 1.3; }
h2 { font-size: 20px; margin-top: 34px; padding-bottom: 6px; border-bottom: 1px solid var(--bordo); }
h3 { font-size: 17px; margin: 26px 0 10px; padding: 9px 12px; background: var(--bg2);
     border-left: 3px solid var(--link); border-radius: 0 4px 4px 0; }
h4 { font-size: 16px; margin: 22px 0 8px; color: var(--link); }
code { background: var(--bg2); padding: 2px 5px; border-radius: 4px; font-size: 15px; }
pre { background: var(--bg2); padding: 12px; border-radius: 6px; overflow-x: auto; }
img { max-width: 100%; border-radius: 6px; background: #fff; }
hr { border: 0; border-top: 1px solid var(--bordo); margin: 30px 0; }
blockquote { border-left: 3px solid var(--link); margin: 18px 0; padding: 2px 0 2px 14px;
             color: var(--fg); background: var(--bg2); border-radius: 0 4px 4px 0; }
blockquote p { margin: 8px 0; }
table { border-collapse: collapse; display: block; overflow-x: auto; margin: 16px 0; }
td, th { border: 1px solid var(--bordo); padding: 6px 10px; }
th { background: var(--bg2); }
mjx-container { overflow-x: auto; overflow-y: hidden; max-width: 100%; }
/* le "note subito cosi' de botto": sono in corsivo nel markdown, si fanno notare */
em strong, strong em { color: var(--nota); }
.indice { background: var(--bg2); padding: 14px 18px; border-radius: 8px; margin: 20px 0 30px; }
.indice ul { margin: 8px 0 0; padding: 0; list-style: none; }
.indice li { display: flex; gap: 10px; margin: 7px 0; }
.indice .num { flex: none; width: 52px; text-align: right; color: #888;
               font-variant-numeric: tabular-nums; }
.cap { border-top: 3px solid var(--link); margin-top: 46px; padding-top: 6px; }
.su { display: block; text-align: right; font-size: 13px; margin-top: 20px; }
"""


def immagine(percorso):
    try:
        with open(percorso, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    except OSError:
        print("      immagine non trovata:", percorso)
        return ""


def proteggi_math(testo):
    # python-markdown dentro $...$ si mangerebbe gli underscore (N_e -> corsivo), quindi i blocchi
    # latex si mettono da parte prima di convertire e si rimettono dentro intatti dopo
    pezzi = []

    def via(m):
        pezzi.append(m.group(0))
        return "\x00M%d\x00" % (len(pezzi) - 1)

    testo = re.sub(r"\$\$.+?\$\$", via, testo, flags=re.S)
    testo = re.sub(r"(?<!\$)\$[^$\n]+?\$", via, testo)
    return testo, pezzi


def capitoli():
    # a0_, a1_, a2_ sono le pagine di apertura; c02_, c03_ ... i capitoli, numerati come nelle
    # note della dispensa (c055_ e' il paragrafo 5.5). ordinandoli per nome vengono giusti.
    trovati = [f for f in os.listdir(BASE)
               if re.match(r"^[ac]\d+[a-z]?_.+\.md$", f)
               and os.path.getsize(os.path.join(BASE, f)) > 30]
    return sorted(trovati)


def main():
    md = markdown.Markdown(extensions=["extra", "sane_lists", "nl2br"])
    pezzi, voci = [], []

    elenco = capitoli()
    posizione = {nome: i for i, nome in enumerate(elenco)}   # serve per le ancore interne

    for i, nome in enumerate(elenco):
        percorso = os.path.join(BASE, nome)
        testo = io.open(percorso, encoding="utf-8").read()

        m = re.search(r"^#\s+(.+)$", testo, re.M)
        titolo = m.group(1).strip() if m else nome
        titolo = re.sub(r"\\;|\\quad|\\,|[$\\]", " ", titolo)      # via il latex dal titolo
        titolo = re.sub(r"\s+", " ", titolo).strip()
        # nell' indice il numero e' quello della dispensa, preso dal titolo: una lista numerata
        # conterebbe 1, 2, 3... e direbbe una cosa diversa da quello che c'e' scritto nel capitolo
        m = re.match(r"^([\d.\-]+)\s+-\s+(.+)$", titolo)
        num, nome_solo = (m.group(1), m.group(2)) if m else ("", titolo)
        voci.append('<li><span class="num">%s</span><a href="#c%d">%s</a></li>'
                    % (num, i, nome_solo))

        testo, math = proteggi_math(testo)
        md.reset()
        html = md.convert(testo)
        for k, p in enumerate(math):
            html = html.replace("\x00M%d\x00" % k, p)

        def incorpora(m):
            src = m.group(1)
            if src.startswith("data:"):
                return m.group(0)
            f = os.path.normpath(os.path.join(os.path.dirname(percorso), src))
            return m.group(0).replace(src, immagine(f))

        html = re.sub(r'<img[^>]+src="([^"]+)"', incorpora, html)
        # i link fra capitoli diventano ancore interne (qui e' tutto in una pagina sola), gli
        # altri .md si spengono. la posizione la da' l' ordine dei file, non il loro numero:
        # i capitoli si chiamano come nella dispensa (c055 = 5.5) e non sono progressivi
        html = re.sub(r'<a href="([ac]\d+[a-z]?_[^"]*)\.md">(.*?)</a>',
                      lambda m: '<a href="#c%d">%s</a>' % (posizione[m.group(1) + ".md"], m.group(2))
                      if m.group(1) + ".md" in posizione else m.group(2), html)
        html = re.sub(r'<a href="[^"]*\.md[^"]*">(.*?)</a>', r"\1", html)

        pezzi.append('<div class="cap" id="c%d">%s<a class="su" href="#top">torna su</a></div>'
                     % (i, html))
        print("   ", nome)

    pagina = """<!doctype html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Compendio di Astronomical Spectroscopy</title>
<style>%s</style>
<script>window.MathJax = { tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] } };</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head><body><div class="wrap" id="top">
<h1>Compendio di Astronomical Spectroscopy</h1>
<div class="indice"><b>Capitoli</b><ul>%s</ul></div>
%s
</div></body></html>""" % (CSS, "\n".join(voci), "\n".join(pezzi))

    os.makedirs(os.path.dirname(FUORI), exist_ok=True)
    io.open(FUORI, "w", encoding="utf-8").write(pagina)
    print("\nfatto: %s  (%.2f MB)" % (FUORI, os.path.getsize(FUORI) / 1e6))


if __name__ == "__main__":
    main()
