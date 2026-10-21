# LinguaNovels — títols comercials i URL permanents

## Novel·la 1

- **Títol comercial en proves (octubre 2026):** `Fifteen Years in Ink`
- **Subtítol de l'EPUB B1:** `A Graded English Mystery — B1`
- **Títol anterior:** `The Last Letter`
- **Slug públic permanent:** `the-last-letter` (**NO CANVIAR**)
- **Web principal de l'obra:** https://linguanovels.pages.dev/the-last-letter/
- **Exercicis B1:** https://linguanovels.pages.dev/the-last-letter/b1/
- **Parts:** https://linguanovels.pages.dev/the-last-letter/b1/chapter-1/part-1/ (mateix esquema fins al capítol 15)

La versió de prova de l'EPUB incorpora el títol nou; aquesta documentació no canvia encara cap pàgina pública ni cap ruta indexada. El canvi de títol visible al web, metadades SEO i els fitxers del generador s'ha de fer en un únic desplegament coherent.

### Requisits obligatoris

1. Mai no canviar ni reutilitzar el `slug`, les 135 URLs de listening o les URLs canòniques.
2. El títol és **contingut**, no part de l'identificador públic.
3. Per a cada llibre nou, triar un `slug` nou i registrar-lo a `docs/epub_link_registry.json`; no alterar els anteriors.
4. Després de qualsevol reconstrucció de `dist/`, executar `python3 scripts/epub_link_guard.py check`.
5. Abans de comercialitzar, comprovar disponibilitat/possibles conflictes de marca, qualitat final dels textos, material generat amb IA, portada i compatibilitat Kindle. La cerca preliminar de títols no implica una validació jurídica.

Aquest document registra una decisió de títol comercial; el nom dels fitxers, els enllaços impresos i les rutes antigues són independents del nou títol.
