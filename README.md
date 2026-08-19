# Compendio di Astronomical Spectroscopy

Compendio del corso di Astronomical Spectroscopy, pensato per chi lo sta preparando.

Non e' un riassunto della dispensa e non la sostituisce: e' il percorso logico che porta a ogni
formula, coi casi limite e il motivo per cui quella formula ha quella faccia li'.

**Si legge qui: [https://syrinx98.github.io/compendio-spectroscopy/](https://syrinx98.github.io/compendio-spectroscopy/)**

Se serve offline o sul telefono, [**compendio.html**](https://syrinx98.github.io/compendio-spectroscopy/compendio.html)
e' tutto quanto in un file solo, immagini comprese.

---

## Cosa ci trovi

- niente derivazioni: quelle stanno nella dispensa e li' sono fatte bene
- il problema di partenza, le assunzioni, la formula, e cosa succede nei casi limite
- **i capitoli numerati come nella dispensa**, sottoparagrafi compresi: se qui leggi 5.7, nelle
  note e' il paragrafo 5.7
- un disegno per ogni concetto che a parole non si capisce
- in fondo a ogni capitolo qualche domanda, da rispondere ragionando e non a memoria, con il
  rimando alla sezione dove trovare la risposta

---

## Indice

| | capitolo |
|---|---|
| | [Di cosa parla tutto il corso](a1_di_cosa_parla.md) |
| | [Numeri e conversioni da avere in tasca](a2_numeri_in_tasca.md) |
| **2** | [Popolazioni: Boltzmann, Saha e perche' Balmer ha un massimo](c02_boltzmann_saha.md) |
| **3** | [Trasporto radiativo](c03_trasporto.md) |
| **4** | [Righe in assorbimento: EW e allargamenti](c04_righe_assorbimento.md) |
| **5.1-5.4** | [Atomo a due livelli, densita' critica, quenching](c051_atomo_due_livelli.md) |
| **5.5** | [Righe di ricombinazione otticamente sottili](c055_ricombinazione.md) |
| **5.6** | [Estinzione da polvere](c056_polvere.md) |
| **5.7** | [Righe proibite](c057_righe_proibite.md) |
| **6** | [I continui](c06_continui.md) |
| **7** | [Sezione d' urto ed equilibrio di ionizzazione](c07_ionizzazione.md) |
| **8** | [La sfera di Stromgren](c08_stromgren.md) |
| **9** | [Equilibrio termico: chi scalda e chi raffredda](c09_equilibrio_termico.md) |

Ogni capitolo sta in piedi da solo.

---

## Com'è fatto il repo

| | |
|---|---|
| `*.md` | i sorgenti, uno per capitolo |
| `data\` | i grafici in png |
| `grafici\` | gli script matplotlib che li generano |
| `docs\` | il sito, quello che si vede su GitHub Pages |
| `docs\compendio.html` | tutto in un file unico, per leggerlo sul telefono senza la cartella dietro |

Il prefisso dei file serve solo a tenerli in ordine: `c055_` e' il paragrafo 5.5.

---

## Per modificarlo

I sorgenti sono i `.md`, si aprono con qualsiasi editor. Per rigenerare il sito serve Python con
`markdown` (e `matplotlib` se si vogliono rifare anche i grafici):

```
pip install markdown matplotlib
python wiki.py               # rifa' docs\
python build_compendio.py    # rifa' compendio.html
```

I due script leggono da soli tutti i `.md` presenti e li ordinano per nome, quindi aggiungendo un
capitolo nuovo non c'e' niente da configurare. Per rifare un grafico si entra in `grafici\` e si
lancia lo script che serve (scrivono in `..\data`).

---

## Sulle formule

Le ho ricontrollate contro la dispensa, ma le sviste sono possibili: se qualcosa non torna fa fede
la dispensa. Se trovi un errore apri una issue o mandami una pull request.
