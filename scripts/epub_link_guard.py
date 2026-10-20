#!/usr/bin/env python3
"""Guard the permanent URLs printed in LinguaNovels EPUB books.

After generating dist/, run: python3 scripts/epub_link_guard.py check
New story: python3 scripts/epub_link_guard.py add-book --book slug --level b1 --level b2
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
REGISTRY = ROOT / "docs" / "epub_link_registry.json"
SITE = "https://linguanovels.pages.dev"

def read():
    db = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if db.get("version") != 1 or db.get("site") != SITE:
        raise ValueError("Unknown registry version or site URL")
    return db

def route(row):
    book, level, chapter, part = row["book"], row["level"], row["chapter"], row["part"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", book):
        raise ValueError("Invalid book slug")
    if not re.fullmatch(r"[a-z][0-9]+", level):
        raise ValueError("Invalid level")
    chapter, part = int(chapter), int(part)
    if chapter < 1 or part < 1:
        raise ValueError("Invalid chapter/part number")
    return f"/{book}/{level}/chapter-{chapter}/part-{part}/"

def check():
    db = read()
    seen = set()
    for row in db["links"]:
        path = route(row)
        if row["url"] != SITE + path or path in seen:
            raise ValueError(f"Modified or duplicated permanent link: {row['url']}")
        seen.add(path)
        page = DIST / path.lstrip("/") / "index.html"
        if not page.is_file():
            raise ValueError(f"Broken EPUB link: {SITE + path}. Restore page/redirect.")
    print(f"PASS: {len(seen)} registered listening URLs have published HTML")

def add_book(book, levels):
    db = read()
    if any(r["book"] == book for r in db["links"]):
        raise ValueError("This book already has frozen URLs; do not replace them")
    new = []
    for level in dict.fromkeys(levels):
        # Scan generated HTML; never create links to non-existing listening parts.
        pages = sorted((DIST / book / level).glob("chapter-*/part-*/index.html"))
        if not pages:
            raise ValueError(f"No published listening parts for {book}/{level}")
        for page in pages:
            match = re.fullmatch(r"chapter-(\d+)/part-(\d+)/index\.html", page.relative_to(DIST / book / level).as_posix())
            if match:
                row = dict(book=book, level=level, chapter=int(match[1]), part=int(match[2]))
                row["url"] = SITE + route(row)
                new.append(row)
    db["links"].extend(sorted(new, key=lambda x: (x["book"],x["level"],x["chapter"],x["part"])))
    REGISTRY.write_text(json.dumps(db, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(f"Added {len(new)} immutable URLs for {book}")
    check()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="mode", required=True)
    sub.add_parser("check")
    listing = sub.add_parser("list")
    listing.add_argument("--book", required=True)
    listing.add_argument("--level", required=True)
    new = sub.add_parser("add-book")
    new.add_argument("--book", required=True)
    new.add_argument("--level", required=True, action="append")
    args = ap.parse_args()
    if args.mode == "check":
        check()
    elif args.mode == "list":
        found = [r for r in read()["links"] if r["book"] == args.book and r["level"] == args.level]
        if not found:
            raise ValueError("No registered book/level found")
        for row in sorted(found, key=lambda x: (x["chapter"], x["part"])):
            print(f"C{row['chapter']:02} P{row['part']}: {row['url']}")
    else:
        add_book(args.book, args.level)

if __name__ == "__main__":
    main()
