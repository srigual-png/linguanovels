# EPUB library

The `/novels/` page is generated from `content/epub_catalog.json` and linked in the site navigation and footer.

The first novel is **Fifteen Years in Ink**, subtitle **The Last Letter**, with B1, B2 and C1 editions. Original EPUBs and matching covers were copied from the user-provided `LinguaNovels_3_EPUB_KDP_RC_V240` folder into `dist/books/`. The originals are unchanged.

Each catalog book has `title`, `subtitle`, `language`, `description` and an `editions` array. Each edition has `level`, `file` (an absolute site path under `/books/`) and `cover`.

Rebuild with `python -X utf8 scripts/build_V230.py`. The build verifies ZIP integrity, EPUB mimetype and container presence for every download. This is a basic container check, not EPUBCheck certification. The source report describes these editions as release candidates; Kindle Previewer review is still pending for Amazon publication.

Publish the updated `dist/` directory through the existing LinguaNovels GitHub and Cloudflare Pages workflow. The deployment commit adds only the EPUB library, navigation and sitemap; existing audio and player scripts are retained.
