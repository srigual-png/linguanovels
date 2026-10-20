# LinguaNovels — enllaços permanents per als EPUB (V01)

**Model:** listenings, transcripcions i preguntes gratuïtes; la novel·la digital és una compra voluntària.

## Contracte d'URL (immutable)

Domini inicial: `https://linguanovels.pages.dev`

- Obra: `/{book-slug}/`
- Nivell: `/{book-slug}/{level}/`
- Capítol: `/{book-slug}/{level}/chapter-{n}/`
- Listening concret: `/{book-slug}/{level}/chapter-{n}/part-{p}/`

**Exemple confirmat:** `https://linguanovels.pages.dev/the-last-letter/b1/chapter-1/part-1/`

La nova novel·la tindrà un slug propi (p. ex. `/second-story/`). **Mai no es canvia, elimina ni reutilitza el camí d'un listening publicat en un EPUB.** Si cal una remodelació, es conserva la ruta antiga i s'hi serveix el mateix contingut o una redirecció funcional. Si algun dia hi ha domini propi, els enllaços anteriors a `pages.dev` s'han de mantenir accessibles.

## Contracte de l'EPUB

- Tres edicions independents per a *The Last Letter*: B1, B2 i C1.
- Cada edició conté la novel·la completa, navegable i llegible sense Internet.
- Per cada capítol, tres enllaços externs opcionals i descriptius a les pàgines gratuïtes de listening del mateix nivell.
- Un enllaç a l'índex general del nivell, preferiblement al principi i al final del llibre.
- No s'enllacen directament fitxers MP3 (`_V228.mp3`) ni altres recursos versionats: es poden canviar sense alterar la pàgina de pràctica.
- Evitar enllaços comercials que interrompin la lectura; les fitxes d'Amazon s'enllaçaran **des del web** quan tinguin una URL verificada.
- Provar cada edició a Kindle Previewer. Els enllaços externs funcionen en dispositius compatibles amb navegació web; els exercicis requereixen connexió.
- Els enllaços han de ser contingut complementari, no substituts de capítols absents de l'EPUB.

## Registre de compatibilitat

`docs/epub_link_registry.json` fixa 135 enllaços de *The Last Letter*: 15 capítols × 3 parts × 3 nivells.

Executar després de cada generació de `dist/`:

```bash
python3 scripts/epub_link_guard.py check
python3 scripts/epub_link_guard.py list --book the-last-letter --level b1
```

Abans de publicar noves novel·les: generar les pàgines a `dist/`, després registrar-les amb:

```bash
python3 scripts/epub_link_guard.py add-book --book SLUG --level b1 --level b2 --level c1
```

L'script afegeix enllaços nous, però rebutja substituir el registre d'una obra ja publicada. El `check` falla quan falten rutes antigues. **Cal incorporar aquest check al flux habitual abans de desplegar**: el fitxer per si sol no activa cap bloqueig automàtic.

Referències KDP: [hipervincles](https://kdp.amazon.com/es_ES/help/topic/GQ6JQ7FM6C72HE4X), [qualitat i comprovació d'enllaços](https://kdp.amazon.com/en_US/help/topic/G200952510).
