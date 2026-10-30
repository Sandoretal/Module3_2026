# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Teaching materials for **ReCoN Module 3 — "Real-world data coding for neuroscientists" / Digital Health Data Science Foundations** (MSc Translational Neuroscience, Imperial College London, Autumn 2026). It is not a software package: there is no build system, test suite, linter or dependency manifest. The content is Jupyter notebooks, small datasets, and a static HTML course website.

## Layout

- `tutorial_1/` — Python fundamentals and NumPy (`Introduction_and_functions.ipynb`), using genomics text files (`data/clinvar_5000.vcf`, `data/example_sam.sam`).
- `tutorial_2/` — pandas intro on EHR data, wearable/accelerometer time-series analysis, and an end-of-day task.
- `tutorial_3/` — pandas + statistics on Parkinson's EHR/bloodwork data, in two parts (`*_part1_*`, `*_part2_*`).
- `tutorial_4/` — intro to ML: regression/classification on PD proteomics, PCA/UMAP/K-means, plus a plasma-proteomics/organ-ageing challenge (brief at the end of `Intro_toML.ipynb`).
- `docs/` — hand-written static website (plain HTML + `styles.css` + `site.js`, no generator). `site.js` injects an accessibility toolbar (colour-blind mode, contrast, zoom, keyboard shortcuts; state kept in `localStorage` under `module3-*` keys). `docs/rendered-notebooks/` holds nbconvert HTML exports of the notebooks.

## Conventions that span files

- **Exercise / solution pairing.** Student notebooks sit in `tutorial_N/`; completed versions sit in `tutorial_N/solutions/` (e.g. `pandas_ehr_tutorial_part1_2026_exercises.ipynb` ↔ `solutions/pandas_ehr_tutorial_part1_2026_solution.ipynb`). When changing an exercise, make the matching change in its solution, and vice versa.
- **Relative data paths.** Notebooks assume the working directory is their own folder: exercise notebooks read `data/<file>.csv`, solution notebooks read `../data/<file>.csv`. Keep this when adding or moving notebooks. Known exceptions to be aware of: `tutorial_2/TimeSeriesAnalysis.ipynb` uses an absolute `/data/...` path, and `tutorial_1` opens `clinvar_5000.vcf` / `example_sam.sam` without the `data/` prefix and writes to `../results/`.
- **Publishing.** `.gitignore` excludes `tutorial_3/solutions/`, `tutorial_4/solutions/`, `tutorial_4/instructor/`, `Slides/` and `docs/` so they aren't released to students early (the site's rendered notebooks include solutions).
- **READMEs.** Each `tutorial_N/README.md` follows the same pattern as `tutorial_1/README.md` (header block with course/department/contributors/term, emoji section headings, Learning Objectives, per-notebook Contents, datasets table, Prerequisites). The root `README.md` links to all four; keep them consistent when notebooks change.
- **Website ↔ repo sync.** Adding, renaming or removing a notebook or dataset means updating, by hand: the tutorial page (`docs/tutorial-N.html`), the searchable index in `docs/files.html` (each row has a `data-search` string of lowercase keywords), any links in `docs/resources.html` (which point to `github.com/Sandoretal/module3_2026/blob/main/...`), the counts on `docs/index.html`, and the rendered HTML in `docs/rendered-notebooks/`. Every page repeats the same `<nav class="site-nav">` block, so nav changes must be made in all of them.

## Commands

Run a notebook headlessly (from inside its folder so relative data paths resolve):

```bash
cd tutorial_4 && jupyter nbconvert --to notebook --execute Intro_toML.ipynb --output /tmp/out.ipynb
```

Regenerate a rendered page for the site:

```bash
jupyter nbconvert --to html tutorial_4/Intro_toML.ipynb --output-dir docs/rendered-notebooks/tutorial_4
```

Preview the website locally: `python -m http.server -d docs`.

Notebooks have been saved with assorted personal kernels (`intropython`, `module3`, `ledd_calculation`, `GTLvenv`, `deeplearning`); there is no shared environment file. Tutorial 4 lists its requirements in `tutorial_4/README.md` (numpy, pandas, scikit-learn, umap-learn, seaborn, matplotlib, plotly, scipy, statsmodels, imbalanced-learn, statannotations; tested on Python 3.11).
