import pandas as pd
import numpy as np
import os

# -----------------------------
# Create folders if not exist
# -----------------------------
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# -----------------------------
# 1. Generate Synthetic Data
# -----------------------------
np.random.seed(42)

n = 500

data = pd.DataFrame({
    "Respondent_ID": range(1, n + 1),
    "Region": np.random.choice(["North", "South", "East", "West"], n),
    "Age_Group": np.random.choice(["18-25", "26-35", "36-50", "50+"], n),
    "Question": "Which product do you prefer?",
    "Response": np.random.choice(
        ["Product A", "Product B", "Product C"],
        n,
        p=[0.33, 0.35, 0.32]
    ),
    "Date": pd.date_range(start="2024-01-01", periods=n, freq="D")
})

data.to_csv("data/poll_data.csv", index=False)
print("✅ Synthetic dataset created: data/poll_data.csv")

# -----------------------------
# 2. Load Data
# -----------------------------
df = pd.read_csv("data/poll_data.csv")

# -----------------------------
# 3. Cleaning
# -----------------------------
df.dropna(inplace=True)
df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# 4. Overall Analysis
# -----------------------------
response_counts = df["Response"].value_counts()
percentage = (response_counts / len(df)) * 100

summary = pd.DataFrame({
    "Count": response_counts,
    "Percentage": percentage.round(2)
})

summary.to_csv("outputs/summary.csv")

print("\n📊 Summary:\n")
print(summary)

# -----------------------------
# 5. Region-wise Analysis
# -----------------------------
region_analysis = df.groupby(["Region", "Response"]).size().unstack(fill_value=0)
region_analysis.to_csv("outputs/region_analysis.csv")

# -----------------------------
# 6. Monthly Trend Analysis (FIXED)
# -----------------------------
trend_data = (
    df.groupby([pd.Grouper(key="Date", freq="ME"), "Response"])
    .size()
    .reset_index(name="Count")
)

trend_data.to_csv("outputs/trend_analysis.csv", index=False)

# -----------------------------
# 7. Insights
# -----------------------------
top_product = response_counts.idxmax()
top_percent = percentage.max()

top_region = df["Region"].value_counts().idxmax()
least_product = response_counts.idxmin()

print("\n🧠 Insights:")
print(f"✔ Top Product: {top_product} ({top_percent:.2f}%)")
print(f"✔ Most Active Region: {top_region}")
print(f"✔ Least Preferred Product: {least_product}")

print("\n✅ All outputs saved in /outputs folder")