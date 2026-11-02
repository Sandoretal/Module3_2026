"""Build one download per tutorial: docs/downloads/tutorial_N.zip.

Each zip holds exactly what is committed in that tutorial's folder (notebooks,
data, images and README), taken from git with `git archive`, so local edits
and untracked files are never included. render_site_notebooks.py runs this
automatically; it can also be run on its own:

    python tools/build_tutorial_zips.py
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "downloads"
TUTORIALS = ["tutorial_1", "tutorial_2", "tutorial_3", "tutorial_4"]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for folder in TUTORIALS:
        dest = OUT / f"{folder}.zip"
        subprocess.run(
            ["git", "archive", "--format=zip", "-9", f"--output={dest}", "HEAD", folder],
            cwd=ROOT,
            check=True,
        )
        print(f"{folder} -> {dest.relative_to(ROOT)} ({dest.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
