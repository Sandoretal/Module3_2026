# Real-world data coding for neuroscientists (ReCoN)
# Tutorial 2

### MSc in Translational Neuroscience,

### Department of Brain Sciences, Faculty of Medicine,

### Imperial College London

### Contributors: [to be added]
w
### Autumn 2026

---

## 🩺 Tabular health records and biological time series
This submodule introduces two of the most common kinds of **real-world data in clinical neuroscience**: **tabular Electronic Health Records (EHR)** and **time-series signals** from medical devices and wearables.
Students learn to load, clean and summarise patient tables with **pandas**, then to process ECG and smartwatch accelerometer recordings and turn raw signals into meaningful features. The day ends with a short task that links the two: wearable sensor features joined to each patient's health record.

---

## 🎯 Learning Objectives
By the end of the notebooks, you will be able to:
- Create, load, save and inspect tables (**DataFrames**) with pandas.
- Select, filter, sort and clean rows and columns, including data types, missing values and messy text.
- Summarise data by group and combine tables.
- Transform data with `.map()`, `.apply()`, `.agg()` and `.transform()`.
- Load, plot and describe a biological time series.
- Clean a signal: handle missing values, smooth, normalise, filter and resample.
- Detect heartbeats in an ECG and extract features such as heart rate.
- Split accelerometer data into windows and compute per-window features.
- Link features from a sensor recording to a patient's clinical record.

---

## 📘 Contents

## `pandas_intro_EHR.ipynb`
Working with synthetic EHR data from people with Parkinson's disease. Every topic follows the same three steps: **Concept**, **Example** and **Task**.

### **2.1 Getting started with DataFrames**
- Creating a DataFrame.
- Loading and saving data (`pd.read_csv()`, `.to_csv()`).
- Inspecting a DataFrame.

### **2.2 Selecting and filtering data**
- Selecting columns, and rows by position (`.iloc`) and by label (`.loc`).
- Filtering rows with one or more conditions.
- Sorting rows.

### **2.3 Changing and cleaning data**
- Adding, renaming and removing columns.
- Data types and missing values.
- Exploring categories and cleaning text.

### **2.4 Grouping and combining tables**
- Grouping rows (e.g. one result per patient).
- Combining tables.

### **2.5 Transforming and summarising data**
- Recoding values with `.map()`.
- Writing your own rules with `.apply()` and `lambda`.
- Summarising groups with `.agg()` and group transformations with `.transform()`.
- Choosing the right tool.

### **2.6 Putting it all together**
A full cleaning exercise on the EHR table, followed by a summary of today's pandas toolbox.

## `TimeSeriesAnalysis.ipynb`
Time-series data as biological signals. Every topic follows the same steps: **Concept**, **Example** and **Your turn**.

### **Part A: ECG data**
Uses the **MIT-BIH Arrhythmia Database** from [PhysioNet](https://physionet.org/content/mitdb/1.0.0/).
- A time series as a list of numbers plus a clock; summary statistics and plotting.
- Missing data (NaNs) and how to handle them.
- Smoothing with a moving average and normalisation (z-scoring).
- Filtering out unwanted frequencies and resampling / downsampling.
- Finding heartbeats with peak detection.
- From signal to features: RR intervals and heart rate.
- Putting it all together: a feature table for several subjects.

### **Part B: Wearable accelerometer data**
Uses a simplified extract of the [Parkinson's Disease Smartwatch (PADS) dataset](https://physionet.org/content/parkinsons-disease-smartwatch/1.0.0/) from PhysioNet.
- Loading, exploring and plotting a tabular time series.
- Estimating the sampling rate from timestamps.
- Downsampling and filtering the accelerometer signal with `.apply()` and `lambda`.
- Windowing (epoching) the signal.
- Time-domain features per window.
- Final task: the signal vector magnitude, combined features and a correlation check.

## `end_of_day_task.ipynb`
Linking wearable sensor data to health records. Six patients wore a wrist accelerometer during a 20-second rest recording at their most recent clinic visit.
- **Part A** (≈ 7 min): keep each patient's most recent visit from the health records.
- **Part B** (≈ 15 min): clean the recordings and compute tremor features (amplitude and IQR of the vector magnitude).
- **Part C** (≈ 8 min): combine the features with the health records and interpret the results.

---

## 📂 Datasets Used

The datasets are in the `data/` folder next to the notebooks:

| Data File | Description | Used in |
| :--- | :--- | :--- |
| `data/ehr_parkinsons.csv` | Synthetic health records, one row per clinic visit (`patient_id`, `sex`, `date_of_birth`, `visit_date`, `clinic_id`, `updrs_iii`, `ledd_mg`, `medication`, `bmi`). | `pandas_intro_EHR.ipynb`, `end_of_day_task.ipynb` |
| `data/patients.csv` | Small synthetic patient table (`age_at_diagnosis`, `smoking_status`), created and saved during the pandas tutorial. | `pandas_intro_EHR.ipynb` |
| `data/medications.csv` | Small synthetic medications table (`drug_name`, `drug_class`, `route`), created and saved during the pandas tutorial. | `pandas_intro_EHR.ipynb` |
| `data/pads10_accelerometer_data.csv` | Accelerometer and gyroscope data for 10 participants from the PADS dataset. | `TimeSeriesAnalysis.ipynb` (Part B) |
| `data/wearable_rest_recordings.csv` | Synthetic 20-second wrist accelerometer rest recordings (100 Hz) for the six EHR patients. | `end_of_day_task.ipynb` |
| `data/ecg.csv` | ECG recordings (`subject_id`, `t_s`, `ecg_mv`, `fs_hz`). | Additional data |
| `data/wrist_accelerometer.csv` | Wrist accelerometer recordings by subject, group and task. | Additional data |

The ECG data in Part A of `TimeSeriesAnalysis.ipynb` is **downloaded directly from PhysioNet** with the `wfdb` library, so an internet connection is needed for that part.

---

## ⚙️ Prerequisites and Setup

To run the notebooks successfully, you will need a Python environment with the following libraries installed:

* `numpy`
* `pandas`
* `matplotlib`
* `seaborn`
* `scipy`
* `wfdb`

Run the cells **in order, from top to bottom**, with the notebook's own folder as the working directory so that the `data/` paths resolve. It is recommended to use an environment manager like `conda` or `pip` to install these dependencies.
