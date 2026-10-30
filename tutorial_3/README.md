# Real-world data coding for neuroscientists (ReCoN)
# Tutorial 3

### MSc in Translational Neuroscience,

### Department of Brain Sciences, Faculty of Medicine,

### Imperial College London

### Contributors: Anastasia Ilina, Jared Maina, Cecilia Rodriguez, Marirena Bafaloukou, Katarzyna Zoltowska, Rishideep Chatterjee, Sahar Rahbar, Cynthia Sandor

### Autumn 2026

---

## 📊 Tabular data with pandas on Electronic Healthcare Records (EHR)
This submodule builds on the pandas introduction and takes students through the full journey from **raw clinical data to statistical results**.
Students learn to visualise and clean real-world EHR data from people with Parkinson's disease, then to choose, run and report basic statistical tests in Python.

---

## 🎯 Learning Objectives
By the end of the notebooks, you will be able to:
- Visualise distributions, trends and relationships in clinical data.
- Flag outliers and data-entry errors, and decide what to do with them.
- Find and resolve duplicate records.
- Describe, diagnose and handle missing data.
- Explain what a hypothesis test, a *p*-value and a confidence interval tell you, and what they don't.
- Check a test's assumptions and choose between parametric and non-parametric tests.
- Compare groups, measure associations and test categorical data with `scipy.stats`.
- Correct for multiple comparisons.
- Report a result in one clear sentence.

---

## 📘 Contents

## `pandas_ehr_tutorial_part1_2026_exercises.ipynb`
**Part 1: Data visualisation. Data cleaning and preprocessing with pandas.**
Overall aim: prepare real-world clinical data for statistical analysis. Each section ends with a ✅ **checkpoint**.

### **1. Visualising categorical data**
- Counts and proportions (`value_counts`).
- From continuous to categorical (`pd.cut`).
- Two categorical variables with `pd.crosstab`.

### **2. Visualising continuous data**
- Summary measures and `describe()`.
- Histograms and log scales for skewed data (`np.log1p`).
- Comparing groups with box and violin plots, and relationships with scatter plots (seaborn).

### **3. Outliers and data-entry errors**
- Spotting outliers visually and flagging them with rules (`.quantile`, `.between`).
- Skewed variables: LEDD.
- Capping and winsorisation (`.clip`).

### **4. Duplicates**
- Finding and resolving duplicate records (`.duplicated`, `.drop_duplicates`, `.groupby().agg`).

### **5. Missing data**
- How much is missing, and why is it missing?
- Handling missing data (`.dropna`, `.fillna`, `IterativeImputer`) and choosing a method.

### **Final challenge: the bloodwork dataset**
Apply the whole workflow to a new dataset: map the missingness, diagnose the mechanism, then impute and compare.

## `pandas_ehr_tutorial_part2_2026_exercises.ipynb`
**Part 2: Statistical Analysis.**
Overall aim: run and interpret basic statistical tests on medical data in Python. This notebook is about *choosing and running* tests, not about the mathematics behind them.

### **1. What does a statistical test do?**
- Building intuition with a permutation test (`numpy`, `groupby`).

### **2. Choosing the right test**
- Checking the assumptions: Q–Q plots, `shapiro`, `levene`.

### **3. Comparing groups**
- Two groups: Welch's t-test (`ttest_ind`) and Mann–Whitney U (`mannwhitneyu`).
- Three or more groups: ANOVA (`f_oneway`) and Kruskal–Wallis (`kruskal`).

### **4. Associations**
- Two numeric variables: correlation (`pearsonr`, `spearmanr`, `.corr`).
- Two categorical variables: the chi-squared test (`pd.crosstab`, `chi2_contingency`).

### **5. Multiple comparisons**
- Correcting *p*-values (`itertools.combinations`, `multipletests`).

### **Reporting your results**
How to report a statistical result in one clear sentence.

---

## 📂 Repository Contents

| File Name | Description |
| :--- | :--- |
| `pandas_ehr_tutorial_part1_2026_exercises.ipynb` | Part 1 student notebook: visualisation, cleaning and preprocessing, **without the solutions**. |
| `pandas_ehr_tutorial_part2_2026_exercises.ipynb` | Part 2 student notebook: statistical analysis, **without the solutions**. |
| `solutions/pandas_ehr_tutorial_part1_2026_solution.ipynb` | The complete version of Part 1, including **all code solutions and answers**. |
| `solutions/pandas_ehr_tutorial_part2_2026_solution.ipynb` | The complete version of Part 2, including **all code solutions and answers**. |
| `images/` | Figures shown inside the notebooks. |

## Datasets Used

| Data File | Description | Used in |
| :--- | :--- | :--- |
| Synthetic EHR dataset | Longitudinal clinical records from people with Parkinson's disease. It is **generated inside each notebook** by the cell marked `RUN THIS CELL TO (RE)CREATE THE SYNTHETIC DATASET`. | Parts 1 and 2 |
| `data/pd_bloodwork.csv` | Single-visit (cross-sectional) bloodwork results with missing values (`age`, `sex`, `bmi`, `years_since_dx`, `LEDD`, `updrs_iii`, `CRP`, `ALT`, and more). | Part 1, final challenge |

---

## ⚙️ Prerequisites and Setup

To run the notebooks successfully, you will need a Python environment with the following libraries installed:

* `numpy`
* `pandas`
* `matplotlib`
* `seaborn`
* `scikit-learn` (`sklearn`)
* `scipy`
* `statsmodels`

Run the notebooks from inside the `tutorial_3/` folder so that the `data/` paths resolve. It is recommended to use an environment manager like `conda` or `pip` to install these dependencies.
