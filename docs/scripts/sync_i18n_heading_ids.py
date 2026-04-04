#!/usr/bin/env python3
"""Assign English MkDocs heading ids to translated Markdown ({#slug}).

Reads canonical ids from the default (English) site's built HTML, then updates
docs/<locale>/**/*.md so in-page fragments match English (for shared links and
mkdocs anchor validation).

Prerequisite: run ``make build-docs`` first so ``site/`` contains English HTML.
Or run ``make build-docs-all`` to build and sync in one step.

Usage:
    uv run python docs/scripts/sync_i18n_heading_ids.py [--dry-run] [--strict] [--site SITE]
"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ATX_HEADING = re.compile(r"^(#{1,6}\s+)(.+)$")
TRAILING_HEADING_ID = re.compile(r"\s*\{#[^}]+\}\s*$")
HTML_HEADING_ID = re.compile(r'<h[1-6][^>]*\sid="([^"]+)"', re.IGNORECASE)
LOCALES = frozenset({"ja", "ko", "zh"})


class _ArticleHeadingIdsParser(HTMLParser):
    """Collect id attributes on h1–h6 inside the main Material article body."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._article_depth = 0
        self._in_body = False
        self.ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        if tag == "article":
            classes = ad.get("class", "")
            if self._in_body:
                self._article_depth += 1
            elif "md-content__inner" in classes:
                self._in_body = True
                self._article_depth = 1
            return
        if not self._in_body:
            return
        if len(tag) == 2 and tag.startswith("h") and tag[1].isdigit():
            hid = ad.get("id")
            if hid:
                self.ids.append(hid)

    def handle_endtag(self, tag: str) -> None:
        if tag == "article" and self._in_body:
            self._article_depth -= 1
            if self._article_depth <= 0:
                self._in_body = False
                self._article_depth = 0


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


def english_html_for_doc(site_dir: Path, doc_relpath: str) -> Path:
    """Map docs-relative path (e.g. agents.md, models/index.md) to English HTML."""
    p = Path(doc_relpath)
    if p.name == "index.md":
        if p.parent == Path("."):
            return site_dir / "index.html"
        return site_dir / p.parent / "index.html"
    stem = p.stem
    parent = p.parent
    if parent == Path("."):
        return site_dir / stem / "index.html"
    return site_dir / parent / stem / "index.html"


def extract_heading_ids(html_path: Path) -> list[str]:
    raw = html_path.read_text(encoding="utf-8", errors="replace")
    parser = _ArticleHeadingIdsParser()
    try:
        parser.feed(raw)
        parser.close()
    except Exception:
        pass
    if parser.ids:
        return parser.ids
    return HTML_HEADING_ID.findall(raw)


def markdown_heading_lines(lines: list[str]) -> list[int]:
    """0-based line indices of ATX headings outside fenced code blocks."""
    in_fence = False
    indices: list[int] = []
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if ATX_HEADING.match(line.rstrip("\n")):
            indices.append(i)
    return indices


def strip_trailing_attr(title_part: str) -> str:
    return TRAILING_HEADING_ID.sub("", title_part).rstrip()


def apply_ids_to_markdown(text: str, ids: list[str]) -> tuple[str, bool]:
    """Return (new_text, ok). ok is False only when heading and id counts differ."""
    lines = text.splitlines(keepends=True)
    heading_ixs = markdown_heading_lines(lines)
    if len(heading_ixs) != len(ids):
        return text, False

    for line_i, slug in zip(heading_ixs, ids, strict=True):
        line = lines[line_i]
        m = ATX_HEADING.match(line.rstrip("\n"))
        if not m:
            continue
        prefix, rest = m.group(1), m.group(2)
        body = strip_trailing_attr(rest)
        new_line = f"{prefix}{body} {{#{slug}}}\n"
        if not line.endswith("\n"):
            new_line = new_line.rstrip("\n")
        lines[line_i] = new_line
    return "".join(lines), True


def sync_file(
    locale_md: Path,
    english_html: Path,
    *,
    dry_run: bool,
) -> str | None:
    if not english_html.is_file():
        return f"skip (no English HTML): {english_html}"
    ids = extract_heading_ids(english_html)
    if not ids:
        return f"skip (no heading ids in HTML): {english_html}"
    text = locale_md.read_text(encoding="utf-8")
    new_text, ok = apply_ids_to_markdown(text, ids)
    if not ok:
        return (
            f"MISMATCH headings {markdown_heading_line_count(text)} vs ids {len(ids)}: {locale_md}"
        )
    if new_text == text:
        return None
    if not dry_run:
        locale_md.write_text(new_text, encoding="utf-8", newline="\n")
    return f"updated: {locale_md}"


def markdown_heading_line_count(text: str) -> int:
    return len(markdown_heading_lines(text.splitlines(keepends=True)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site",
        type=Path,
        default=repo_root_from_script() / "site",
        help="MkDocs site output (default: <repo>/site)",
    )
    parser.add_argument(
        "--docs",
        type=Path,
        default=repo_root_from_script() / "docs",
        help="Docs source root (default: <repo>/docs)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing files",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 2 if any locale page has a heading count mismatch",
    )
    args = parser.parse_args()
    site_dir: Path = args.site.resolve()
    docs_dir: Path = args.docs.resolve()

    if not site_dir.is_dir():
        print(
            f"error: site dir not found: {site_dir}\n"
            "Run `uv run mkdocs build` (or `make build-docs`) first.",
            file=sys.stderr,
        )
        return 1

    updates = 0
    skipped = 0
    mismatches: list[str] = []

    for locale in sorted(LOCALES):
        locale_root = docs_dir / locale
        if not locale_root.is_dir():
            continue
        for locale_md in sorted(locale_root.rglob("*.md")):
            rel = locale_md.relative_to(locale_root).as_posix()
            en_html = english_html_for_doc(site_dir, rel)
            msg = sync_file(locale_md, en_html, dry_run=args.dry_run)
            if msg is None:
                continue
            if msg.startswith("MISMATCH"):
                mismatches.append(msg)
            elif msg.startswith("skip"):
                skipped += 1
                print(msg)
            else:
                updates += 1
                print(msg)

    if mismatches:
        print(
            "\nHeading count mismatches (sync skipped for these files; "
            "align headings with English or run with --strict to fail):",
            file=sys.stderr,
        )
        for m in mismatches:
            print(f"  {m}", file=sys.stderr)
        if args.strict:
            return 2

    suffix = " (dry-run)" if args.dry_run else ""
    print(
        f"Done{suffix}: {updates} file(s) updated, {skipped} skipped, "
        f"{len(mismatches)} mismatch(es)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
