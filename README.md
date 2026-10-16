<div align="center">

# 💰 Financial Data Cleaning & EDA Pipeline

### 🚀 Automating Financial Data Integrity with Python

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://seaborn.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**A smart pipeline that cleans, analyzes, and visualizes messy financial data — automatically.**

[Overview](#-overview) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [How It Works](#-how-it-works) • [Output](#-output) • [Contact](#-contact)

</div>

---

## 📖 Overview

> *"Raw financial data is messy. It contains missing values, illogical entries, duplicate reports, and extreme outliers."*

This pipeline solves that problem. It **automatically detects** whether your data is **Stock Prices** or **Company Financials**, then applies the right cleaning strategy for each.

| 🎯 Goal | ✅ Result |
|:--------|:---------|
| Detect data type automatically | Stock OHLCV or SEC Fundamentals |
| Clean errors intelligently | No fake data, no blind deletion |
| Flag real market events | Crashes ≠ Errors |
| Generate visual insights | 6-panel EDA figure |
| Save clean output | `df_clean.csv` ready for ML |

---

## ✨ Features

### 🟢 Stock Price Mode
- 📅 Auto datetime parsing
- 💲 Forward-fill prices
- 📊 Median imputation for Volume
- 🚫 Removes illogical rows (`High < Low`, `Price ≤ 0`)
- 🚩 Flags outliers with IQR + Z-Score
- 🛡️ **Never deletes real crashes**

### 🔵 SEC Fundamentals Mode
- 🏢 Handles restated filings
- 🔄 Unifies changing revenue tags
- 📉 Derives Q4 = FY − (Q1+Q2+Q3)
- 🧮 Calculates YoY Growth & Margins
- ⚠️ Keeps structural nulls as-is
- 🎯 Flags revenue & growth outliers

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/financial-eda-pipeline.git
cd financial-eda-pipeline
```

### 2. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn scipy
```

### 3. Requirements
- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- scipy

---

## 🚀 Usage

### Basic Run
```bash
python eda_pipeline.py
```

### Custom File Path
```bash
python eda_pipeline.py path/to/your/data.csv
```

### Expected Folder Structure

```text
📦 financial-eda-pipeline
 ┣ 📜 eda_pipeline.py
 ┣ 📂 Dataset
 ┃ ┗ 📄 financial_facts.csv
 ┣ 📄 df_clean.csv          ← generated
 ┣ 📄 eda_figure.png        ← generated
 ┗ 📄 README.md             ← this file
```

---

## 🧠 How It Works

```mermaid
flowchart TD
    A[📂 Load CSV] --> B{Detect Mode}
    B -->|Has Date, Close, Volume| C[🟢 Stock Price Mode]
    B -->|Otherwise| D[🔵 SEC Fundamentals Mode]
    C --> E[Clean Prices & Volume]
    D --> F[Clean Filings & Revenue]
    E --> G[📊 Descriptive Stats]
    F --> G
    G --> H[📈 Generate 6 Charts]
    H --> I[💾 Save df_clean.csv]
```

### 📥 Step 1 — Load & Detect
- Reads the CSV file using `pandas`.
- Prints shape, dtypes, missing %, and duplicate count.
- Auto-detects data type based on column names.

### 🧹 Step 2 — Clean the Data

**1. Stock Mode:**

| Issue | Action |
|:------|:-------|
| Missing prices | Forward-fill |
| Missing volume | Median |
| `High < Low` | Delete |
| Volume spikes | Flag only |
| Price crashes (>5σ) | Flag only |

**2. SEC Mode:**

| Issue | Action |
|:------|:-------|
| Duplicate filings | Keep latest |
| Conflicting values | Use restatement |
| Missing Q4 | Calculate |
| Revenue tag change | Unify |

### 📊 Step 3 — Statistics
- Calculates: **Mean, Median, Std, Skewness, Kurtosis**
- Prints plain-English interpretation of distribution shape.

### 📈 Step 4 — Visualize

Generates a 6-panel figure:
1. Histogram — Main variable
2. Histogram — Secondary variable
3. Box plot — Secondary variable
4. Box plot — Returns / Growth
5. Time series — Main variable
6. Time series — Secondary variable

### 💾 Step 5 — Output
- Saves `df_clean.csv`
- Prints final shape and first 5 rows

---

## 📊 Sample Output

```text
Shape: (5000, 7)
Detected mode: PRICE (OHLCV)
Unparseable dates: 0
Illogical rows (<=0 price or High<Low): 3
Volume IQR outliers: 120 | |Z|>3: 45
Return shocks > 5 sigma (kept, flagged): 8

Descriptive statistics:
              mean    median     std    skew    kurt
Close      152.34    150.21   25.67    0.45    1.23
Volume   5234123   4100000  2.1e6    2.87    9.45

Close: skew=0.45 (roughly symmetric),
       excess kurtosis=1.23 (fat tails / shock-prone)
```

---

## 🎯 Key Design Decisions

| ✅ Principle | 💡 Why |
|:-------------|:-------|
| **Flag, Don't Delete** | Extreme values in finance are real events, not errors |
| **No Fake Data** | Missing structural values stay missing |
| **Latest Restated Values** | Companies re-file reports; use the newest |
| **Smart Imputation** | `ffill` for prices, `median` for volume |

---

## 📁 Output Files

| 📄 File | 📝 Description |
|:--------|:---------------|
| `df_clean.csv` | Cleaned dataset ready for analysis |
| `eda_figure.png` | 6-panel visualization of key patterns |

---

## 🧰 Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat-square&logo=python&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=flat-square&logo=python&logoColor=white)

</div>

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. 💾 Commit your changes
4. 🚀 Push and open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — free to use and modify.

---

## 📧 Contact

<div align="center">

**Abdalla Mohamed**

[![Email](https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:abdallamohamed8354@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/abdalla-mohamed-farouk)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat-square&logo=github&logoColor=white)](https://(https://github.com/Abdalla820))

</div>

---

<div align="center">

### ⭐ If you found this project useful, please give it a star!

**Made with ❤️ and Python**

</div>
