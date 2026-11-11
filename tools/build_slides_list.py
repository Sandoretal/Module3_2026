"""Write the list of slide PDFs into the website pages (docs/).

The pages used to ask the GitHub API for the contents of slides/ from every visitor's browser.
GitHub allows 60 such requests an hour per network address, and a lecture theatre shares one
address, so most students saw only the fallback list. This script writes the list into the HTML
when the site is built instead, so the pages need no request at all.

Every tracked PDF in slides/ is listed (`git ls-files`, so local files that were never committed
are left out):
- slides.html     one card per PDF, with Open and Download buttons;
- resources.html  the PDFs grouped under each day of the schedule, and one row per PDF in the
                  "All indexed files" table (type "slides", tagged with its lecture's tutorial);
- schedule.html   a "Lecture slides (PDF)" / "Workshop slides (PDF)" link in each session cell
                  that has a data-slides="<lecture id>" attribute.

A PDF belongs to a lecture when its file name contains one of the lecture's words as whole words,
ignoring case and treating spaces, "_" and "-" alike ("ml" matches "Intro_ML.pdf" but not "html").
PDFs that match no lecture are listed under "Other slides".

Lecture or workshop: a PDF whose name contains "workshop", "tutorial" or "practical"
("Module3_ML_workshop_part4.pdf") is a workshop deck; every other PDF is a lecture. A schedule
cell shows the lecture slides, or the workshop slides when it has data-slides-kind="workshop".

The generated HTML sits between <!-- slides:...:start --> and <!-- slides:...:end --> comments,
so the script can be run again and again. It runs in the website workflow on every push; to see
the result locally, run it from the repository root:
    python tools/build_slides_list.py
"""

import html
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO = "Sandoretal/Module3_2026"
FOLDER = "slides"

# One entry per day on schedule.html; `id` must match the day's section id there.
DAYS = [
    {"id": "day-2026-11-05", "label": "Day 1 · Thursday 5 November"},
    {"id": "day-2026-11-06", "label": "Day 2 · Friday 6 November"},
    {"id": "day-2026-11-09", "label": "Day 3 · Monday 9 November"},
    {"id": "day-2026-11-10", "label": "Day 4 · Tuesday 10 November"},
]
# One entry per lecture, in schedule order. `tutorial` is the tutorial the lecture introduces
# ("" for none), used by the file table's Tutorial filter.
LECTURES = [
    {"id": "overview", "tutorial": "", "day": "day-2026-11-05", "words": ["overview", "part1", "part_1"]},
    {"id": "programming", "tutorial": "1", "day": "day-2026-11-05", "words": ["programming", "python"]},
    {"id": "time-series", "tutorial": "2", "day": "day-2026-11-06",
     "words": ["time_series", "timeseries", "wearable", "wearables", "part2", "part_2"]},
    {"id": "statistics", "tutorial": "3", "day": "day-2026-11-09", "words": ["statistics", "ehr", "part3", "part_3"]},
    {"id": "machine-learning", "tutorial": "4", "day": "day-2026-11-10",
     "words": ["machine_learning", "ml", "part4", "part_4"]},
]
WORKSHOP_WORDS = ["workshop", "tutorial", "practical"]
KIND_LABEL = {"lecture": "Lecture", "workshop": "Workshop"}


def words(text):
    """'Module3_ML_part4.pdf' -> '_module3_ml_part4_' (for whole-word matching)."""
    stem = re.sub(r"\.pdf$", "", text, flags=re.I).lower()
    return "_" + re.sub(r"[^a-z0-9]+", "_", stem) + "_"


def title(name):
    return re.sub(r"[_-]+", " ", re.sub(r"\.pdf$", "", name, flags=re.I)).strip()


def kind(name):
    return "workshop" if any(words(w) in words(name) for w in WORKSHOP_WORDS) else "lecture"


def lecture_of(name):
    return next((lec for lec in LECTURES if any(words(w) in words(name) for w in lec["words"])), None)


def part_number(name):
    match = re.search(r"_part_?(\d+)_", words(name))
    return int(match.group(1)) if match else float("inf")


def urls(name):
    path = f"{FOLDER}/{quote(name)}"
    return (f"https://github.com/{REPO}/blob/main/{path}",
            f"https://raw.githubusercontent.com/{REPO}/main/{path}")


def tracked_pdfs():
    out = subprocess.run(["git", "ls-files", "-z", "--", f"{FOLDER}/"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    names = [Path(p).name for p in out.split("\0") if p.lower().endswith(".pdf") and "/" not in p[len(FOLDER) + 1:]]
    # In part order (part1, part2, ...), then by name.
    return sorted(names, key=lambda n: (part_number(n), n.lower()))


def pill(name):
    k = kind(name)
    return f'<span class="pill {k}">{KIND_LABEL[k]}</span>'


def card(name):
    open_url, download_url = urls(name)
    colour = "cool workshop" if kind(name) == "workshop" else "hot lecture"
    return (f'        <article class="card {colour}">\n'
            f'          {pill(name)}\n'
            f'          <h3>{html.escape(title(name))}</h3>\n'
            f'          <div class="cta-row">\n'
            f'            <a class="button primary small" href="{open_url}">Open</a>\n'
            f'            <a class="button secondary small" href="{download_url}" download>↓ Download</a>\n'
            f'          </div>\n'
            f'        </article>\n')


def by_day(pdfs):
    groups = [(day["label"], f'schedule.html#{day["id"]}',
               [n for n in pdfs if (lec := lecture_of(n)) and lec["day"] == day["id"]]) for day in DAYS]
    other = [n for n in pdfs if lecture_of(n) is None]
    if other:
        groups.append(("Other slides", None, other))
    out = []
    for label, href, names in groups:
        head = (f'<a href="{href}" title="See this day on the schedule"><strong>{label}</strong></a>' if href
                else f"<strong>{label}</strong>")
        items = "".join(f'<li><a href="{urls(n)[0]}">{html.escape(title(n))} (PDF)</a> {pill(n)}</li>' for n in names) \
            or '<li class="empty">No slides yet</li>'
        out.append(f"            <li>{head}\n              <ul>{items}</ul>\n            </li>\n")
    return "".join(out)


def table_rows(pdfs):
    out = []
    for n in pdfs:
        lec = lecture_of(n)
        day = next((d for d in DAYS if lec and d["id"] == lec["day"]), None)
        search = f'slides {kind(n)} pdf {title(n)} {day["label"] if day else ""}'.lower().strip()
        out.append(f'            <tr data-type="slides" data-tutorial="{lec["tutorial"] if lec else ""}" '
                   f'data-search="{html.escape(search)}"><td>{FOLDER}</td><td>{html.escape(n)}</td>'
                   f'<td>{kind(n)} slides</td><td><a href="{urls(n)[0]}">Open</a></td></tr>\n')
    return "".join(out)


def schedule_links(pdfs, lecture_id, cell_kind):
    lec = next((l for l in LECTURES if l["id"] == lecture_id), None)
    if lec is None:
        sys.exit(f"schedule.html: unknown data-slides id {lecture_id!r}")
    names = [n for n in pdfs if lecture_of(n) is lec and kind(n) == cell_kind]
    label = KIND_LABEL[cell_kind]
    return "".join(
        f'<br><a href="{urls(n)[0]}">'
        + (f"{label} slides: {html.escape(title(n))} (PDF)" if len(names) > 1 else f"{label} slides (PDF)")
        + "</a>" for n in names)


def replace_block(text, key, content, page):
    pattern = re.compile(rf"(<!-- slides:{key}:start -->)(.*?)(<!-- slides:{key}:end -->)", re.S)
    if not pattern.search(text):
        sys.exit(f"{page}: markers <!-- slides:{key}:start/end --> not found")
    return pattern.sub(lambda m: m.group(1) + "\n" + content + m.group(3), text, count=1)


def main():
    pdfs = tracked_pdfs()

    page = DOCS / "slides.html"
    text = page.read_text(encoding="utf-8")
    text = replace_block(text, "cards", "".join(card(n) for n in pdfs) or "        <p>No slides yet.</p>\n", page.name)
    page.write_text(text, encoding="utf-8")

    page = DOCS / "resources.html"
    text = page.read_text(encoding="utf-8")
    text = replace_block(text, "by-day", by_day(pdfs), page.name)
    text = replace_block(text, "rows", table_rows(pdfs), page.name)
    page.write_text(text, encoding="utf-8")

    page = DOCS / "schedule.html"
    text = page.read_text(encoding="utf-8")
    cell = re.compile(r'(<td\b[^>]*\bdata-slides="([^"]+)"[^>]*>)(.*?)(</td>)', re.S)

    def fill(m):
        cell_kind = (re.search(r'data-slides-kind="([^"]+)"', m.group(1)) or [None, "lecture"])[1]
        body = re.sub(r"<!-- slides:links:start -->.*?<!-- slides:links:end -->", "", m.group(3), flags=re.S)
        links = schedule_links(pdfs, m.group(2), cell_kind)
        return f"{m.group(1)}{body}<!-- slides:links:start -->{links}<!-- slides:links:end -->{m.group(4)}"

    text, n_cells = cell.subn(fill, text)
    page.write_text(text, encoding="utf-8")

    print(f"Slides list: {len(pdfs)} PDF(s) written to slides.html, resources.html "
          f"and {n_cells} schedule cell(s): {', '.join(pdfs) or 'none'}")


if __name__ == "__main__":
    main()
