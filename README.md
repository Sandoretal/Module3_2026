# Real-world data coding for neuroscientists (ReCoN)
# Module 3: Digital Health Data Science Foundations

### MSc in Translational Neuroscience,

### Department of Brain Sciences, Faculty of Medicine,

### Imperial College London

### Contributors: Katarzyna Zoltowska, Cecilia Rodriguez, Rishideep Chatterjee, Marirena Bafaloukou, Jared Maina, Ratneshwaran Maheswaran, Anastasia Ilina, Sahar Rahbar, Cynthia Sandor

### Autumn 2026

---

## 🧠 About this module
This repository contains the teaching materials for **Module 3** of the **Real-world data coding for neuroscientists (ReCoN)** course.
Across four tutorials, students go from their first lines of Python to applying statistics and machine learning to real-world neuroscience and clinical datasets, including genomics files, Electronic Health Records (EHR), wearable sensor signals and plasma proteomics.

Each tutorial is a set of hands-on **Jupyter notebooks** with explanations, worked examples and exercises, together with the datasets they use.

---

## 🎯 Learning Objectives
By the end of the module, you will be able to:
- Write clean, well-documented Python code, including loops, conditionals and functions.
- Work with numerical data in **NumPy** and tabular data in **pandas**.
- Clean, visualise and summarise Electronic Health Records.
- Process biological time series (ECG and accelerometer data) and extract features from them.
- Choose, run and report basic statistical tests.
- Apply supervised and unsupervised machine learning to neuroscientific data.

---

## 📘 Tutorials

| Tutorial | Topic | Main notebooks |
| :--- | :--- | :--- |
| [Tutorial 1](tutorial_1/README.md) | **Introduction to Python**: syntax, data types, operators, modules, loops and conditionals, files and directories, NumPy and functions. | `Introduction_and_functions.ipynb` |
| [Tutorial 2](tutorial_2/README.md) | **Tabular health records and biological time series**: an introduction to pandas on EHR data, ECG and wearable accelerometer signal processing, and an end-of-day task linking the two. | `pandas_intro_EHR.ipynb`, `TimeSeriesAnalysis.ipynb`, `end_of_day_task.ipynb` |
| [Tutorial 3](tutorial_3/README.md) | **Tabular data with pandas on EHR**: data visualisation, cleaning and preprocessing (Part 1), and statistical analysis (Part 2). | `pandas_ehr_tutorial_part1_2026_exercises.ipynb`, `pandas_ehr_tutorial_part2_2026_exercises.ipynb` |
| [Tutorial 4](tutorial_4/README.md) | **Introduction to Machine Learning**: regression, classification, PCA, UMAP and K-means, plus a plasma proteomics and organ-specific aging challenge. | `Intro_toML.ipynb` |

Each tutorial folder has its own README with the full contents, learning objectives and datasets.

---

## 📂 Repository Structure

```
module3_public/
├── tutorial_1/      # Python fundamentals
│   └── data/
├── tutorial_2/      # pandas intro and time-series analysis
│   └── data/
├── tutorial_3/      # EHR cleaning and statistics
│   ├── data/
│   └── images/
└── tutorial_4/      # Introduction to machine learning
    └── data/
```

- The datasets for each tutorial are in the `data/` folder next to its notebooks.
- Solution notebooks are placed in a `solutions/` folder inside the tutorial and are released after the tutorial has taken place.

---

## ⚙️ Prerequisites and Setup

We go through these steps together in the installation and environment session; use this section as a reference during and after it. No coding experience is needed: copy each command exactly as written.

**You will need:** Windows 10/11, macOS 12+ or Ubuntu 20.04+, at least **10 GB** of free disk space and **8 GB** of RAM. Admin rights are not needed.

To run all the notebooks in this module, you will need **Python 3.11** (3.10–3.12 also fine) and the following libraries:

* `numpy`
* `pandas`
* `matplotlib`
* `seaborn`
* `plotly`
* `scipy`
* `statsmodels`
* `scikit-learn` (`sklearn`)
* `umap-learn`
* `imbalanced-learn` (`imblearn`)
* `statannotations`
* `wfdb`
* `jupyter` and `ipykernel`
* `ipywidgets` (optional, avoids a progress-bar warning when importing `umap`)

We install these with **conda** (via Miniforge) in a separate environment called `m3`, following the steps below.

> 💡 **Where do I type the commands?** On Windows, use **Miniforge Prompt** (installed in Step 1). On macOS and Linux, use **Terminal**.
>
> **Already have Anaconda, Miniconda or Miniforge?** Run `conda --version`. If it prints a version, skip to Step 3.

### 1. Install conda (Miniforge)
Download page: https://conda-forge.org/download/

<details>
<summary><b>Windows</b></summary>

1. Download and run **`Miniforge3-Windows-x86_64.exe`**. This installer works for both x64 and ARM PCs (to check, see *Settings → System → About → System type*).
2. Choose **Just Me** → keep the default location `C:\Users\<you>\miniforge3` (use `C:\miniforge3` if your username contains spaces) → leave **"Add to PATH" unticked** → Install.
3. Open **Miniforge Prompt** from the Start menu and use it for all the commands below.

*Optional:* to use conda in PowerShell or the VS Code terminal, run `conda init powershell` in Miniforge Prompt, then reopen PowerShell. If PowerShell says scripts are disabled, run:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
</details>

<details>
<summary><b>macOS</b></summary>

1. Download and run the installer (this picks the right version for your chip automatically):
   ```bash
   curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
   bash Miniforge3-$(uname)-$(uname -m).sh
   ```
   If you downloaded it from the website instead, check your chip with `uname -m` (or Apple menu → About This Mac) and run `bash ~/Downloads/Miniforge3-MacOSX-arm64.sh` (`arm64` = Apple Silicon) or `bash ~/Downloads/Miniforge3-MacOSX-x86_64.sh` (`x86_64` = Intel).
2. Answer the prompts: Enter → `yes` (licence) → Enter (location) → **`yes`** (initialize conda).
3. Quit Terminal (`Cmd+Q`) and reopen it. If `(base)` doesn't appear at the start of the prompt, run `~/miniforge3/bin/conda init zsh`.
</details>

<details>
<summary><b>Linux (Ubuntu)</b></summary>

1. Download and run the installer:
   ```bash
   curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
   bash Miniforge3-$(uname)-$(uname -m).sh
   ```
   If you downloaded it from the website instead, run `bash ~/Downloads/Miniforge3-Linux-x86_64.sh` (Intel/AMD) or `bash ~/Downloads/Miniforge3-Linux-aarch64.sh` (ARM).
2. Answer the prompts: Enter → `yes` → Enter → **`yes`**.
3. Close and reopen Terminal. If `(base)` doesn't appear, run `~/miniforge3/bin/conda init bash`.
</details>

### 2. Check that conda works
```bash
conda --version
conda info
```

### 3. Create and activate the `m3` environment
```bash
conda create -n m3 python=3.11 -y
conda activate m3        # the prompt changes to (m3); repeat this in every new terminal
python --version
```
<details>
<summary>Miniconda/Anaconda users: <i>Terms of Service</i> error?</summary>

```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
# or skip the Anaconda channels entirely:
conda create -n m3 -c conda-forge --override-channels python=3.11 -y
```
</details>

### 4. Install the packages
Make sure the prompt shows `(m3)` first.

**Option A: conda (recommended)**
```bash
conda install -c conda-forge numpy pandas matplotlib seaborn plotly scipy statsmodels scikit-learn umap-learn imbalanced-learn statannotations wfdb jupyter ipykernel ipywidgets -y
```

**Option B: pip.** Run this from inside the course repository folder (if a `requirements.txt` is provided, `python -m pip install -r requirements.txt` does the same):
```bash
python -m pip install numpy pandas matplotlib seaborn plotly scipy statsmodels scikit-learn umap-learn imbalanced-learn statannotations wfdb jupyter ipykernel ipywidgets
```

**Option C: environment file (replaces Steps 3 and 4).** Save the following as `environment.yml`, then run `conda env create -f environment.yml` and `conda activate m3`:
```yaml
name: m3
channels:
  - conda-forge
dependencies:
  - python=3.11
  - numpy
  - pandas
  - matplotlib
  - seaborn
  - plotly
  - scipy
  - statsmodels
  - scikit-learn
  - umap-learn
  - imbalanced-learn
  - statannotations
  - wfdb
  - jupyter
  - ipykernel
  - ipywidgets
```

### 5. Register the environment with Jupyter
With `(m3)` active:
```bash
python -m ipykernel install --user --name m3 --display-name "Python (m3)"
jupyter kernelspec list     # m3 should be listed
jupyter lab                 # optional: opens Jupyter in your browser; press Ctrl+C to stop
```

### 6. Connect VS Code
1. Install VS Code from https://code.visualstudio.com/ (Windows: tick **Add to PATH**; macOS: move it to **Applications**; Linux: use the `.deb` file or `sudo snap install code --classic`).
2. Install the **Python** and **Jupyter** extensions (`Ctrl+Shift+X` / `Cmd+Shift+X`).
3. Open a notebook → **Select Kernel** → **Python (m3)**. If it is missing: `Ctrl+Shift+P` / `Cmd+Shift+P` → **Python: Select Interpreter** → pick the path containing `envs/m3`.

### 7. Check that everything is installed
```bash
python -c "import sys, numpy, pandas, matplotlib, seaborn, sklearn; print('Python', sys.version.split()[0]); print('numpy', numpy.__version__); print('pandas', pandas.__version__); print('matplotlib', matplotlib.__version__); print('seaborn', seaborn.__version__); print('scikit-learn', sklearn.__version__)"
```
Every package should print a version. If you see `ModuleNotFoundError`, activate `m3` (`conda activate m3`) and redo Step 4.

### Running the notebooks
1. Download or clone this repository.
2. Open Jupyter (`jupyter lab` or `jupyter notebook`) or your preferred editor, e.g. VS Code, and select the **Python (m3)** kernel.
3. Open a notebook **from inside its tutorial folder**, so that the `data/` paths resolve correctly.
4. Run the cells **in order, from top to bottom** (`Shift + Enter`). If something stops working, restart the kernel and run all the cells above the one you are working on.

### Useful commands
```bash
conda activate m3                              # activate the environment
conda deactivate                               # deactivate it
conda env list                                 # list environments
conda list                                     # list installed packages
conda install -c conda-forge <package>         # add a package
conda update -n base conda                     # update conda itself
where python                                   # Windows: which Python is in use
which python                                   # macOS/Linux: which Python is in use
```

<details>
<summary><b>Start over or uninstall</b></summary>

**Start over (all OS)**, then repeat Steps 3–5:
```bash
conda deactivate
conda env remove -n m3 -y
jupyter kernelspec remove m3 -y
```

**Uninstall Miniforge:**
- Windows: *Settings → Apps → Installed apps → Miniforge3 → Uninstall*, then delete the `miniforge3` folder.
- macOS/Linux:
  ```bash
  conda init --reverse --all
  rm -rf ~/miniforge3 ~/.conda ~/.condarc
  ```
</details>

---

## About

* **Course:** Real-world data coding for neuroscientists (ReCoN)
* **Program:** MSc in Translational Neuroscience
* **Institution:** Department of Brain Sciences, Faculty of Medicine, Imperial College London
* **Term:** Autumn 2026
