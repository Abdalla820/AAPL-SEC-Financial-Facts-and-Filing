# -AAPL-SEC-Financial-Facts-and-Filing
Financial Data Cleaning & EDA Pipeline
A Python pipeline that automatically cleans, analyzes, and visualizes raw financial data. It handles two types of data: Stock Prices (OHLCV) and Company Financials (SEC Fundamentals).

📌 Overview
Raw financial data is messy. It contains missing values, illogical entries, duplicate reports, and extreme outliers. This pipeline solves that by:

Detecting the type of data automatically.

Cleaning errors and filling gaps intelligently.

Flagging outliers without deleting real market events.

Visualizing the data with 6 professional charts.

Saving a clean CSV file ready for machine learning.

📂 Project Structure
text
project/
│
├── eda_pipeline.py          # Main script
├── Dataset/
│   └── financial_facts.csv  # Input data (you provide this)
│
├── df_clean.csv             # Output: Cleaned data
├── eda_figure.png           # Output: 6-panel visualization
└── README.md                # This file
🚀 How to Run
1. Install Requirements
bash
pip install pandas numpy matplotlib seaborn scipy
2. Run the Script
bash
python eda_pipeline.py
Or specify a custom file path:

bash
python eda_pipeline.py path/to/your/data.csv
🧠 How It Works
Step 1: Load & Detect
Reads the CSV file.

Prints a summary (rows, columns, missing values, duplicates).

Auto-detects the data type:

If columns Date, Close, Volume exist → Stock Price Mode.

Otherwise → SEC Fundamentals Mode.

Step 2: Clean the Data
🟢 Stock Price Mode
Issue	Solution
Missing prices	Forward-fill (last known price)
Missing volume	Fill with median
Price ≤ 0 or High < Low	Delete row (impossible data)
Volume spikes	Flag with IQR + Z-Score
Price crashes (>5σ)	Flag only — never delete real events
🔵 SEC Fundamentals Mode
Issue	Solution
Missing dates	Leave empty (structural, not an error)
Duplicate filings	Keep the latest filed value
Conflicting values	Use the most recent restatement
Missing Q4	Calculate: FY - (Q1 + Q2 + Q3)
Revenue tag changes	Unify different tags into one series
Revenue outliers	Flag with IQR + Z-Score
Step 3: Descriptive Statistics
Calculates mean, median, std, skewness, and kurtosis. Prints a plain-English interpretation.

Step 4: Visualization
Generates a 6-panel figure (eda_figure.png):

Histogram of main variable

Histogram of secondary variable

Box plot of secondary variable

Box plot of returns/growth

Time series of main variable

Time series of secondary variable

Step 5: Output
Saves the cleaned DataFrame to df_clean.csv.

🎯 Key Design Decisions
✅ Flag, Don't Delete: Extreme values in finance are usually real events (crashes, earnings surprises). We mark them, not remove them.

✅ No Fake Data: We never invent dates or financial periods. Missing structural data stays missing.

✅ Latest Restated Values: When companies re-file reports, we use the newest version.

✅ Smart Imputation: We use ffill for prices (valid until changed) but median for volume (ffill would invent trades).

📊 Output Files
File	Description
df_clean.csv	Cleaned dataset ready for analysis
eda_figure.png	6-panel visualization of key patterns
🛠️ Requirements
Python 3.8+

pandas

numpy

matplotlib

seaborn

scipy

📝 Example Output
text
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

Close: skew=0.45 (roughly symmetric), excess kurtosis=1.23 (fat tails / shock-prone)
💡 Why This Project Matters
Saves Time: Automates hours of manual data cleaning.

Model-Ready: Output is ready for machine learning without distortion.

Domain-Aware: Understands that financial outliers are often real events, not errors.

📧 Contact
[AbdallaMohamed] — abdallamohamed8354@gmail.com

📜 License
MIT License — free to use and modify.
