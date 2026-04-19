import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Poll Results Visualizer", layout="wide")

st.title("📊 Poll Results Visualizer Dashboard")
st.markdown("### 🚀 Data Analytics Project | Portfolio Ready")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/poll_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

age_filter = st.sidebar.multiselect(
    "Select Age Group",
    options=df["Age_Group"].unique(),
    default=df["Age_Group"].unique()
)

filtered_df = df[
    (df["Region"].isin(region_filter)) &
    (df["Age_Group"].isin(age_filter))
]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📌 Key Metrics")

total_responses = len(filtered_df)
top_choice = filtered_df["Response"].value_counts().idxmax()

top_percent = round(
    filtered_df["Response"].value_counts(normalize=True).max() * 100, 2
)

col1, col2, col3 = st.columns(3)
col1.metric("Total Responses", total_responses)
col2.metric("Top Choice", top_choice)
col3.metric("Top Choice %", f"{top_percent}%")

# -----------------------------
# Vote Share
# -----------------------------
st.subheader("📊 Vote Share")

vote_counts = filtered_df["Response"].value_counts().reset_index()
vote_counts.columns = ["Option", "Count"]

fig_bar = px.bar(
    vote_counts,
    x="Option",
    y="Count",
    color="Option",
    text="Count",
    title="Vote Count by Product"
)
fig_bar.update_traces(textposition="outside")

st.plotly_chart(fig_bar, use_container_width=True)

fig_pie = px.pie(
    vote_counts,
    names="Option",
    values="Count",
    title="Vote Distribution"
)

st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# Region-wise Analysis
# -----------------------------
st.subheader("🌍 Region-wise Analysis")

region_data = filtered_df.groupby(["Region", "Response"]).size().reset_index(name="Count")

fig_region = px.bar(
    region_data,
    x="Region",
    y="Count",
    color="Response",
    barmode="group",
    title="Region-wise Preferences"
)

st.plotly_chart(fig_region, use_container_width=True)

# -----------------------------
# Trend Over Time (FIXED)
# -----------------------------
st.subheader("📈 Trend Over Time")

trend_data = (
    filtered_df.groupby([pd.Grouper(key="Date", freq="ME"), "Response"])
    .size()
    .reset_index(name="Count")
)

fig_trend = px.line(
    trend_data,
    x="Date",
    y="Count",
    color="Response",
    title="Monthly Response Trends"
)

st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------
# Insights Section
# -----------------------------
st.subheader("🧠 Insights")

top_region = (
    filtered_df.groupby("Region")["Response"]
    .count()
    .idxmax()
)

least_product = (
    filtered_df["Response"].value_counts().idxmin()
)

st.write(f"✔ Most active region: **{top_region}**")
st.write(f"✔ Least preferred product: **{least_product}**")
st.write(f"✔ Top product dominates with **{top_percent}% share**")

# -----------------------------
# Download Option
# -----------------------------
st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_data.csv"
)

# -----------------------------
# Raw Data
# -----------------------------
st.subheader("📄 Raw Data")
st.dataframe(filtered_df)