"""Render the student notebooks to HTML for the course website (docs/).

Only the exercise notebooks tracked in this repository are rendered, and the
build stops if any of them has local edits or differs from origin/main. The
pages are shown un-run, and anything that would reveal an answer is stripped
on the way:

- every saved output and execution count is cleared;
- "DISCUSSION NOTES" code cells and markdown cells that answer the
  "What do you observe?" questions are dropped;
- the "Solution" row of the "How this notebook works" legend is removed.

The source notebooks are not modified.

Usage (from the repository root):
    python tools/render_site_notebooks.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "rendered-notebooks"

NOTEBOOKS = [
    "tutorial_1/Introduction_and_functions.ipynb",
    "tutorial_2/pandas_intro_EHR.ipynb",
    "tutorial_2/TimeSeriesAnalysis.ipynb",
    "tutorial_2/end_of_day_task.ipynb",
    "tutorial_3/pandas_ehr_tutorial_part1_2026_exercises.ipynb",
    "tutorial_3/pandas_ehr_tutorial_part2_2026_exercises.ipynb",
    "tutorial_4/Intro_toML.ipynb",
]

# Images referenced by relative path from the notebooks' markdown.
ASSETS = [
    "tutorial_1/sam_file.png",
    "tutorial_1/vcf_format.png",
    "tutorial_3/images",
]

# Markdown cells that start like this are answers to discussion questions.
ANSWER_MARKDOWN_PREFIXES = (
    "**Why do the fake filter and the real one give different results?**",
    "**Where did the baseline go?**",
    "####  What do you observe?\n\nThe band-passed signal",
)

# The same strings, matched anywhere in the rendered HTML, fail the build.
FORBIDDEN_IN_HTML = ("DISCUSSION NOTES", "Instructors: these cells", "**Solution**")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def check_matches_repo():
    """The site must show exactly what is on GitHub: every notebook tracked,
    with no local edits, and the local branch level with origin/main."""
    tracked = set(git("ls-files", "*.ipynb").stdout.split())
    problems = [f"{rel}: not tracked in git" for rel in NOTEBOOKS if rel not in tracked]
    problems += [f"{rel}: has uncommitted changes" for rel in NOTEBOOKS
                 if git("diff", "--quiet", "HEAD", "--", rel).returncode != 0]
    untracked = tracked - set(NOTEBOOKS)
    if untracked:
        problems.append(f"tracked notebooks missing from NOTEBOOKS: {sorted(untracked)}")
    if git("diff", "--quiet", "HEAD", "origin/main", "--", *NOTEBOOKS).returncode != 0:
        problems.append("notebooks differ from origin/main (push or pull first)")
    if problems:
        sys.exit("Notebooks do not match the repository:\n" + "\n".join(problems))


def strip_answers(nb):
    cells, report = [], []
    for i, cell in enumerate(nb.cells):
        src = cell.source.strip()

        if cell.cell_type == "code" and src.startswith("# DISCUSSION NOTES"):
            report.append(f"dropped discussion notes (cell {i})")
            continue
        if cell.cell_type == "markdown" and src.startswith(ANSWER_MARKDOWN_PREFIXES):
            report.append(f"dropped answer markdown (cell {i})")
            continue
        if cell.cell_type == "markdown" and "**Solution**" in cell.source:
            cell.source = "\n".join(l for l in cell.source.splitlines() if "**Solution**" not in l)
            report.append(f"removed Solution legend row (cell {i})")

        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None

        cells.append(cell)

    nb.cells = cells
    return nb, report


def main():
    check_matches_repo()
    exporter = HTMLExporter()
    problems = []

    for rel in NOTEBOOKS:
        nb, report = strip_answers(nbformat.read(ROOT / rel, as_version=4))
        body, _ = exporter.from_notebook_node(nb)

        hits = [s for s in FORBIDDEN_IN_HTML if s in body]
        if hits:
            problems.append(f"{rel}: still contains {hits}")
        if '<div class="jp-OutputArea-child' in body:
            problems.append(f"{rel}: still contains outputs")

        dest = OUT / Path(rel).with_suffix(".html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body, encoding="utf-8")
        print(f"{rel} -> {dest.relative_to(ROOT)}")
        for line in report:
            print(f"    {line}")

    for rel in ASSETS:
        src, dest = ROOT / rel, OUT / rel
        if src.is_dir():
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dest)

    if problems:
        sys.exit("Rendered HTML is not clean:\n" + "\n".join(problems))


if __name__ == "__main__":
    main()
