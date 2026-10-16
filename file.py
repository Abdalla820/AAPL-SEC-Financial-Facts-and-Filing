import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


pd.set_option("display.width", 200); pd.set_option("display.max_columns", 30)
sns.set_theme(style="whitegrid")
base_dir = os.path.dirname(os.path.abspath(__file__))
default_path = os.path.join(base_dir, "Dataset/financial_facts.csv")
PATH = sys.argv[1] if len(sys.argv) > 1 else default_path

if not os.path.exists(PATH):
    raise FileNotFoundError(f"Input CSV not found: {PATH}")


raw = pd.read_csv(PATH)
print("Shape:", raw.shape); print("\nDtypes:\n", raw.dtypes)
print("\nNon-null vs total:\n", pd.DataFrame({"non_null": raw.count(), "total": len(raw),
                                             "null_%": (raw.isna().mean() * 100).round(1)}))
print("\nExact duplicate rows:", raw.duplicated().sum())

PRICE_MODE = {"Date", "Close", "Volume"}.issubset(raw.columns)
print("\nDetected mode:", "PRICE (OHLCV)" if PRICE_MODE else "SEC FUNDAMENTALS")


def iqr_mask(s, k=1.5):
    q1, q3 = s.quantile([.25, .75]); i = q3 - q1
    return (s < q1 - k * i) | (s > q3 + k * i)

if PRICE_MODE:
    raw["Date"] = pd.to_datetime(raw["Date"], errors="coerce")
    print("Unparseable dates:", raw["Date"].isna().sum())
    df = raw.dropna(subset=["Date"]).drop_duplicates().sort_values("Date").set_index("Date")
    df = df[~df.index.duplicated(keep="last")]
    num = [c for c in ["Open", "High", "Low", "Close", "Adj Close", "Volume"] if c in df.columns]
    df[num] = df[num].apply(pd.to_numeric, errors="coerce")

    print("\nNaNs per column:\n", df[num].isna().sum())
    price_cols = [c for c in num if c != "Volume"]
    df[price_cols] = df[price_cols].ffill()
    if "Volume" in df: df["Volume"] = df["Volume"].fillna(df["Volume"].median())

    bad = (df[price_cols] <= 0).any(axis=1) | (df["High"] < df["Low"])
    print("Illogical rows (<=0 price or High<Low):", int(bad.sum()))
    df = df[~bad]

    df["Vol_IQR_outlier"] = iqr_mask(df["Volume"])
    df["Vol_Z"] = stats.zscore(df["Volume"])
    df["Vol_Z_outlier"] = df["Vol_Z"].abs() > 3
    print("Volume IQR outliers:", int(df.Vol_IQR_outlier.sum()), "| |Z|>3:", int(df.Vol_Z_outlier.sum()))

    px = "Adj Close" if "Adj Close" in df else "Close"
    df["Ret"] = df[px].pct_change()
    df["Ret_shock"] = df["Ret"].abs() > 5 * df["Ret"].std()
    print("Return shocks > 5 sigma (kept, flagged):", int(df.Ret_shock.sum()))

    df_clean = df
    stat_cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df]
    main, vol = "Close", "Volume"

else:
    for c in ["filed", "start", "end"]: raw[c] = pd.to_datetime(raw[c])
    key = ["concept", "unit", "start", "end"]
    print("Same fact repeated across filings:", raw.duplicated(key, keep=False).sum())

    conflicts = raw.groupby(key, dropna=False).value.nunique()
    print("Facts with conflicting values across filings (restatements/splits):", int((conflicts > 1).sum()))

    dedup = raw.sort_values("filed").drop_duplicates(key, keep="last").copy()
    pos = ["Assets", "SalesRevenueNet", "Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "GrossProfit"]
    print("Non-positive values in must-be-positive concepts:", int((dedup[dedup.concept.isin(pos)].value <= 0).sum()))

    REV = ["SalesRevenueNet", "Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"]  
    def duration_series(concepts):
        s = dedup[dedup.concept.isin(concepts) & dedup.start.notna() & (dedup.unit == "USD")].copy()
        s["days"] = (s.end - s.start).dt.days
        return s.sort_values("filed").drop_duplicates(["start", "end"], keep="last")
    def quarterly(concepts):
        s = duration_series(concepts)
        q = s[s.days.between(80, 100)].set_index("end").value
        fy = s[s.days.between(350, 380)].set_index("end").value
        out = q.copy()
        for e, v in fy.items():                     
            prior = q[(q.index < e) & (q.index > e - pd.Timedelta(days=300))]
            if len(prior) == 3 and e not in out.index: out.loc[e] = v - prior.sum()
        return out.sort_index()

    df = pd.DataFrame({"Revenue": quarterly(REV), "NetIncome": quarterly(["NetIncomeLoss"])}).dropna()
    df.index.name = "PeriodEnd"
    df["RevYoY_%"] = df.Revenue.pct_change(4) * 100
    df["NI_Margin_%"] = df.NetIncome / df.Revenue * 100
    print("\nQuarterly panel:", df.shape, "| gaps >100d:", int((df.index.to_series().diff().dt.days > 100).sum()))
    print("Zero/negative revenue:", int((df.Revenue <= 0).sum()))

    df["Rev_IQR_outlier"] = iqr_mask(df.Revenue)
    df["YoY_Z"] = stats.zscore(df["RevYoY_%"], nan_policy="omit")
    df["YoY_outlier"] = df["YoY_Z"].abs() > 3
    print("IQR outliers (Revenue):", int(df.Rev_IQR_outlier.sum()), "| |Z|>3 (YoY):", int(df.YoY_outlier.sum()))
    df_clean = df
    stat_cols = ["Revenue", "NetIncome", "RevYoY_%", "NI_Margin_%"]
    main, vol = "NetIncome", "Revenue"      


desc = df_clean[stat_cols].agg(["mean", "median", "std", "skew", "kurt"]).T  
print("\nDescriptive statistics:\n", desc.round(3))
for c in (main, vol):
    s, k = df_clean[c].skew(), df_clean[c].kurt()
    print(f"{c}: skew={s:.2f} ({'right-tailed: rare spikes' if s > .5 else 'left-tailed' if s < -.5 else 'roughly symmetric'}), "
          f"excess kurtosis={k:.2f} ({'fat tails / shock-prone' if k > 1 else 'thin tails' if k < -1 else 'near-normal tails'})")


scale = 1 if PRICE_MODE else 1e9
fig, ax = plt.subplots(3, 2, figsize=(15, 13))
sns.histplot(df_clean[main] / scale, kde=True, ax=ax[0, 0]);          ax[0, 0].set_title(f"{main}: histogram + KDE")
sns.histplot(df_clean[vol] / scale, kde=True, ax=ax[0, 1], color="C2"); ax[0, 1].set_title(f"{vol}: histogram + KDE")
sns.boxplot(x=df_clean[vol] / scale, ax=ax[1, 0], color="C2");        ax[1, 0].set_title(f"{vol} box plot (outliers)")
second = "Ret" if PRICE_MODE else "RevYoY_%"
sns.boxplot(x=df_clean[second].dropna(), ax=ax[1, 1], color="C1");    
ax[1, 1].set_title(f"{second} box plot")
ax[2, 0].plot(df_clean.index, df_clean[main] / scale);                
ax[2, 0].set_title(f"{main} over time")
ax[2, 1].plot(df_clean.index, df_clean[vol] / scale, color="C2");     
ax[2, 1].set_title(f"{vol} over time")
plt.tight_layout(); plt.savefig("EDA_Figure.png", dpi=130)


df_clean.to_csv("cleaned_data   .csv")
print("\nFinal df_clean:", df_clean.shape); print(df_clean.head())