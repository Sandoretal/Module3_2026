# Introduction to Machine Learning (ReCoN Module) 

This repository contains the Jupyter notebooks for the **Introduction to Machine Learning** workshop, a tutorial of the **Real-world data coding for neuroscientists (ReCoN)** module at Imperial College London.

This tutorial is designed to provide MSc students in Translational Neuroscience with practical experience applying core machine learning techniques to neuroscientific datasets using Python.

---

## Tutorial Overview and Learning Objectives

This tutorial focuses on both supervised and unsupervised learning, moving from data preparation to model evaluation.

### Key Topics Covered:

* **Supervised Learning:** Predicting Tremor Severity (Regression) and Predicting Disease Status (Classification).
* **Data Handling:** **Data splitting**, handling **missing values**, **scaling** and **stratified splitting**.
* **Feature Engineering:** **Feature selection** and understanding the **Curse of dimensionality**.
* **Model Evaluation:** Using **residuals**, **coefficients**, and interpreting the **Confusion Matrix**.
* **Unsupervised Learning:** Dimensionality reduction with **PCA** and **UMAP**, and clustering with **K-means** (elbow method and silhouette score).
* **Challenge:** Plasma proteomics and **organ-specific aging**.
---

## Repository Contents

| File Name | Description |
| :--- | :--- |
| `Intro_toML.ipynb` | The primary student workshop notebook. It contains all theoretical explanations, guided practical exercises, and questions **without the solutions**. |
| `solutions/Intro_toML_withanswers.ipynb` | The complete version of the workshop notebook, including **all code solutions and answers** to the guided questions. |
| `solutions/Challenge_solution.ipynb` | The complete solution for the end-of-tutorial challenge focusing on **Plasma Proteomics and Organ-Specific Aging**. The challenge brief itself is at the end of `Intro_toML.ipynb`. |

## Datasets Used

This tutorial utilizes the following specific datasets, which are in the `data/` folder next to the notebooks:

| Data File | Description | Tasks Covered |
| :--- | :--- | :--- |
| `data/Proteomics_tremor_PD.csv` | Contains Parkinson's disease data used for both **regression** (predicting tremor severity) and **classification** (predicting disease status). | Tasks 1 and 2 |
| `data/DF_for_unsupervised.csv` | Synthetic proteomics data (500 participants, 209 proteins) for dimensionality reduction and clustering. | Task 3 (PCA, UMAP, K-means) |
| `data/Data_for_challenge.csv` | The dataset for the end-of-tutorial challenge on **Plasma Proteomics and Organ-Specific Aging**. | Challenge |

---

## Prerequisites and Setup

To run the notebooks successfully, you will need a Python environment with the following libraries installed:

* `numpy`
* `pandas`
* `scikit-learn` (`sklearn`)
* `umap-learn`
* `seaborn`
* `matplotlib`
* `plotly`
* `scipy`
* `statsmodels`
* `imbalanced-learn` (`imblearn`)
* `statannotations`
* `ipywidgets` (optional, avoids a progress-bar warning when importing `umap`)

The notebooks were tested with Python 3.11. It is recommended to use an environment manager like `conda` or `pip` to install these dependencies.

---

## About

* **Course:** Real-world data coding for neuroscientists (ReCoN)
* **Program:** MSc in Translational Neuroscience
* **Institution:** Department of Brain Sciences, Faculty of Medicine, Imperial College London
* **Term:** Autumn 2026
* **Contributors:** Marirena Bafaloukou, Anastasia Ilina, Cecilia Rodriguez, Katarzyna Zoltowska, Rishideep Chatterjee, Sahar Rahbar, Ratneshwaran Maheswaran, Cynthia Sandor
