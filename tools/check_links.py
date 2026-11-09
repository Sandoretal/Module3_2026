"""Check every link on the course website (docs/) before it goes live.

For each page in docs/ (the site pages and the rendered notebooks) it checks:

- links to other files in the site: the file exists, with the exact same
  upper/lower case (GitHub Pages is case-sensitive, macOS is not);
- links to a section (page.html#section): that section exists on the page;
- links to this repository on GitHub (github.com/<repo>/blob|tree/main/...,
  raw.githubusercontent.com/<repo>/main/...): the file is committed;
- no link points at a solution notebook;
- 404.html's <base href> matches the repository name.

With --external it also visits links to other websites. Those only produce
warnings, because outside sites can be slow or block automated checks.

Exits with an error if anything is broken, so the GitHub Action stops before
publishing the site.

Usage (from the repository root):
    python tools/check_links.py              # site, sections and GitHub files
    python tools/check_links.py --external   # also try outside websites
"""

import argparse
import html
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SOLUTION = re.compile(r"(^|/)solutions/|solution|withanswers", re.I)
SKIP_SCHEMES = ("mailto:", "tel:", "data:", "javascript:")


def repo_name():
    """"owner/name" of this repository, from GitHub Actions or the git remote."""
    if os.environ.get("GITHUB_REPOSITORY"):
        return os.environ["GITHUB_REPOSITORY"]
    url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    match = re.search(r"github\.com[:/]([^/]+/[^/.]+?)(\.git)?$", url)
    return match.group(1) if match else ""


class Page(HTMLParser):
    """Collects the links, the section ids and the <base> of one page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.base = [], set(), None

    @property
    def decoded(self):
        return {unquote(i) for i in self.ids}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("id", "name"):
            if attrs.get(key):
                self.ids.add(attrs[key])
        if tag == "base" and attrs.get("href"):
            self.base = attrs["href"]
        for key in ("href", "src"):
            value = attrs.get(key)
            if value and tag in ("a", "link", "img", "script", "source", "iframe"):
                self.links.append((self.getpos()[0], value.strip()))


def exists_exact(path):
    """True if the path exists with exactly this upper/lower case."""
    try:
        rel = path.resolve().relative_to(DOCS.resolve())
    except ValueError:
        return False
    current = DOCS
    for part in rel.parts:
        if part not in os.listdir(current):
            return False
        current = current / part
    return True


def target_file(path):
    """The file GitHub Pages would serve for a link to `path`."""
    if path.is_dir() or str(path).endswith("/"):
        return path / "index.html"
    if not path.suffix and path.with_suffix(".html").exists():
        return path.with_suffix(".html")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--external", action="store_true", help="also visit links to other websites (warnings only)")
    args = parser.parse_args()

    repo = repo_name()
    committed = set(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.splitlines())
    committed_dirs = set()
    for f in committed:
        p = Path(f).parent
        while str(p) != ".":
            committed_dirs.add(str(p))
            p = p.parent
    github_file = re.compile(
        rf"^https://(?:github\.com/{re.escape(repo)}/(?:blob|tree|raw)/main|raw\.githubusercontent\.com/{re.escape(repo)}/main)/(.+)$",
        re.I) if repo else None

    pages = sorted(DOCS.rglob("*.html"))
    parsed = {}
    for page in pages:
        p = Page()
        p.feed(page.read_text(encoding="utf-8", errors="replace"))
        parsed[page.resolve()] = p

    errors, external = [], {}
    for page in pages:
        info = parsed[page.resolve()]
        where = page.relative_to(ROOT).as_posix()
        base_dir = page.parent
        if info.base and not info.base.startswith(("http:", "https:")):
            expected = f"/{repo.split('/')[-1]}/" if repo else info.base
            if info.base != expected:
                errors.append(f"{where}: <base href=\"{info.base}\"> should be \"{expected}\" for this repository")
            base_dir = DOCS  # 404.html sets <base href="/<repo>/">: links are relative to the site root
        for line, raw in info.links:
            link = html.unescape(raw)
            if not link or link.startswith(SKIP_SCHEMES) or "${" in link:
                continue
            here = f"{where}:{line}"
            if SOLUTION.search(unquote(urlsplit(link).path)):
                errors.append(f"{here}: links to a solution: {link}")
                continue

            parts = urlsplit(link)
            if parts.scheme in ("http", "https"):
                match = github_file.match(link.split("#")[0].split("?")[0]) if github_file else None
                if match:
                    rel = unquote(match.group(1)).rstrip("/")
                    if rel not in committed and rel not in committed_dirs:
                        errors.append(f"{here}: not committed in {repo}: {rel}")
                elif args.external and "/" not in where.split("docs/", 1)[1]:
                    external.setdefault(link.split("#")[0], here)
                continue
            if parts.scheme or link.startswith("//"):
                continue

            anchor = parts.fragment
            if parts.path:
                target = target_file(base_dir / unquote(parts.path))
                if not exists_exact(target):
                    errors.append(f"{here}: missing file {parts.path}")
                    continue
            else:
                target = page
            if anchor and target.suffix == ".html":
                ids = parsed.get(target.resolve())
                # Browsers match the section name as written or percent-decoded,
                # and nbconvert writes ids with emoji and symbols percent-encoded.
                if ids is not None and anchor not in ids.ids and unquote(anchor) not in ids.decoded:
                    errors.append(f"{here}: no section #{anchor} in {target.relative_to(DOCS).as_posix()}")

    warnings = []
    for url, here in sorted(external.items()):
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 (link check)"})
        try:
            urllib.request.urlopen(request, timeout=15)
        except urllib.error.HTTPError as error:
            if error.code in (403, 405, 429):  # sites that refuse HEAD or bots
                continue
            warnings.append(f"{here}: {url} returned {error.code}")
        except Exception as error:  # noqa: BLE001 - any network problem is only a warning
            warnings.append(f"{here}: {url} could not be reached ({error.__class__.__name__})")

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")
    print(f"Checked {len(pages)} pages: {len(errors)} broken link(s), {len(warnings)} warning(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
