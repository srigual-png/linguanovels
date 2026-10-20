# LinguaNovels V230 — integrated web package

This package combines the reviewed V223 story and exercises (from V224 MASTER) with the 135 technically validated V228 MP3 files. No new speech synthesis is needed. All public-facing pages are in English.

## What is included

- `dist/`: the complete prebuilt static website; publish this directory.
- `content/master_V230.json`: 135 learning units and 810 questions, including audio paths, durations and hashes.
- `site_config_V230.json`: the desired canonical URL and site settings.
- `scripts/build_V230.py`: rebuild the HTML and SEO files using Python 3; no third-party Python packages required.
- `scripts/validate_V230.py`: check coverage, local links, content/audio hashes, duration, SEO and learning logic. Requires Python 3, Node.js and ffprobe.
- `validation/`: verification results and an audio integrity manifest.
- `provenance/`: original production records for review; these files are outside the published directory.

The 188 sitemap pages comprise the homepage, story overview, three level indexes, 45 chapter indexes, 135 listening parts and three information pages. A separate 404 page is included.

## GitHub + Cloudflare Pages

The intended public address is `https://linguanovels.pages.dev`. It has not been reserved or checked for availability. This ZIP does not publish or create accounts.

1. Extract this ZIP. Create a GitHub repository named `linguanovels` using the account you want to own the project.
2. Commit the contents of `LinguaNovels_V230_WEB` to the repository root. Use Git or GitHub Desktop for the whole folder: the website contains more files than a small browser upload can conveniently handle. Do not put the ZIP itself in the repository.
3. In Cloudflare, create a **Pages** project using the GitHub integration, then select that repository and its production branch (usually `main`). Choose **None** as the framework preset.
4. Leave the build command empty, or use `exit 0` if the interface requires a command. Set the build output directory to `dist`. No environment variables, API keys, server functions, database or paid services are required by this website.
5. Request the project name `linguanovels` if available. If the resulting hostname differs, update `site_url` in `site_config_V230.json`, run `python3 scripts/build_V230.py`, and commit the regenerated files before treating the site as final.
6. Check the live homepage, a B1/B2/C1 audio, a long joined audio, quiz submission and navigation on both a phone and a computer.
7. Add the actual site to Google Search Console, verify ownership using the method Google offers for the hostname, and submit `/sitemap.xml`. Search indexing and ad approval are not guaranteed.

GitHub stores the source; Cloudflare Pages serves the website and MP3 files. Subsequent commits to the connected production branch can trigger deployment. No Google Cloud TTS credentials belong in this repository.

## Learning behavior preserved

Each part has six required, closed multiple-choice questions, each with three options, one correct answer and an explanation. Submission displays a score and unlocks the transcript. A perfect score is not required to unlock it. Retrying clears the current form while leaving the previous submitted progress intact until another submission.

The existing `linguanovels:progress:1:` storage format and reviewed content hashes are retained. Saved progress can carry over only on the same browser origin; it cannot automatically migrate from an old local preview or another domain. No sign-in or cross-device sync is included. Progress storage errors do not block grading.

Transcripts are present in each page's HTML. With JavaScript enabled they are revealed after submission; without JavaScript the audio and transcript remain available and grading is disabled. Answers are necessarily inspectable in a static educational app; this is a practice tool, not a secure exam system.

## SEO and advertising

The package includes stable level/chapter/part URLs, unique English titles and descriptions, canonical links, Open Graph metadata, structured WebPage data, a sitemap, robots.txt, internal navigation and static HTML content. Canonical URLs must match the final hostname. The package includes no guaranteed ranking claims or invented reviews.

Advertising is **not active**. Invisible `<template data-ad-slot>` hooks exist at the end of the homepage and listening parts, so no empty ad boxes interrupt practice. To activate ads later, configure a real publisher account, get the site approved, insert the provider's real code, add any required ads.txt, update privacy information and configure the appropriate consent platform. There are no fake publisher IDs or placeholder ads.txt entries.

The privacy page accurately describes this package's local storage and use of GoatCounter analytics and absence of advertising. Review operator/contact disclosures and provider requirements before launching advertising or collecting personal data; this package does not invent an operator address or contact details.

## Validation and limits

Run from this directory:

```bash
python3 scripts/build_V230.py
python3 scripts/validate_V230.py
```

All 135 input MP3s were decoded without errors before integration. The integrated bytes are verified by hash. Their spoken texts match the master transcripts exactly at the text-input level. Technical validation does not establish pronunciation, intonation or full auditory quality. The user accepted the pilot; full production listening remains pending. The master distinguishes technical validation from auditory approval.

Browser visual and interaction QA was not available in the current managed environment; responsive styling and markup were checked statically and the grading/progress module was tested with Node. Live mobile/desktop checks remain necessary before publication is considered verified.

No file exceeds Cloudflare Pages' documented 25 MiB asset limit; the file count is far below 20,000. Audio is loaded only on demand, with no autoplay or preload of the whole library. The total website size and largest asset are recorded in `validation/validation_V230.json`.

The original filename suffix `_V228.mp3` is intentionally retained. V229 fixed the generator's consumption accounting; V230 integrates the resulting audio without regenerating or recompressing it. The original ledger's preventive bound is not a verified bill or exact provider usage.

Official references used for deployment preparation:
- https://developers.cloudflare.com/pages/configuration/git-integration/
- https://developers.cloudflare.com/pages/framework-guides/deploy-anything/
- https://developers.cloudflare.com/pages/platform/limits/

## Preview locally

To preview, run `python3 -m http.server 8000 --directory dist` and open `http://localhost:8000` in your own browser. Absolute asset paths mean opening HTML directly with `file://` is not supported.

## Visitor statistics

All generated HTML pages include the asynchronous GoatCounter script. The dedicated endpoint is configured in `site_config_V230.json` as `https://linguanovels.goatcounter.com/count`, keeping these statistics separate from MI. Rebuild and commit `dist/` after changing the configuration. The privacy page describes the integration.
