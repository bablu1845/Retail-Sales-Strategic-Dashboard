import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Retail Sales Strategic Dashboard", layout="wide")
st.title("Retail Sales Strategic Performance Dashboard")
st.markdown("Advanced Business Diagnostics & Performance Intelligence")

# -------------------------------------------------
# DATABASE
# -------------------------------------------------
conn = sqlite3.connect("retail_sales.db")

regions = pd.read_sql("SELECT DISTINCT Region FROM sales", conn)["Region"].tolist()
categories = pd.read_sql("SELECT DISTINCT Category FROM sales", conn)["Category"].tolist()
segments = pd.read_sql("SELECT DISTINCT Segment FROM sales", conn)["Segment"].tolist()

st.sidebar.header("Strategic Filters")

selected_region = st.sidebar.multiselect("Region", regions, default=regions)
selected_category = st.sidebar.multiselect("Category", categories, default=categories)
selected_segment = st.sidebar.multiselect("Segment", segments, default=segments)

query = f"""
SELECT *
FROM sales
WHERE Region IN ({','.join(['?']*len(selected_region))})
AND Category IN ({','.join(['?']*len(selected_category))})
AND Segment IN ({','.join(['?']*len(selected_segment))})
"""

params = selected_region + selected_category + selected_segment
df = pd.read_sql(query, conn, params=params)

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# -------------------------------------------------
# REMOVE INCOMPLETE MONTH
# -------------------------------------------------
monthly_counts = df.groupby(df["Order_Date"].dt.to_period("M")).size()
latest_month = monthly_counts.index.max()

if monthly_counts[latest_month] < monthly_counts.mean():
    df = df[df["Order_Date"].dt.to_period("M") != latest_month]

# -------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------
total_revenue = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = (total_profit / total_revenue) * 100 if total_revenue else 0

df["Year"] = df["Order_Date"].dt.year
yearly = df.groupby("Year")["Sales"].sum()

yoy_growth = yearly.pct_change().iloc[-1] * 100 if len(yearly) > 1 else 0

monthly_rev = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum()
volatility = monthly_rev.std()

p90_order = np.percentile(df["Sales"], 90)

profit_per_order = total_profit / len(df)
revenue_per_customer = total_revenue / df["Customer_ID"].nunique()

# -------------------------------------------------
# EXECUTIVE KPIs
# -------------------------------------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Revenue", f"${total_revenue:,.0f}")
col2.metric("Profit", f"${total_profit:,.0f}")
col3.metric("Margin %", f"{profit_margin:.2f}%")
col4.metric("YoY Growth %", f"{yoy_growth:.2f}%")
col5.metric("Revenue Volatility", f"${volatility:,.0f}")
col6.metric("90th % Order", f"${p90_order:,.0f}")

st.markdown("---")

# -------------------------------------------------
# CONTRIBUTION ANALYSIS
# -------------------------------------------------
st.subheader("Revenue Contribution by Region")

region_contrib = df.groupby("Region")["Sales"].sum()
region_percent = (region_contrib / total_revenue) * 100

fig1, ax1 = plt.subplots()
region_percent.sort_values(ascending=False).plot(kind="bar", ax=ax1)
ax1.set_ylabel("Revenue %")
st.pyplot(fig1)

# -------------------------------------------------
st.subheader("Revenue Contribution by Category")

category_contrib = df.groupby("Category")["Sales"].sum()
category_percent = (category_contrib / total_revenue) * 100

fig2, ax2 = plt.subplots()
category_percent.sort_values(ascending=False).plot(kind="bar", ax=ax2)
ax2.set_ylabel("Revenue %")
st.pyplot(fig2)

# -------------------------------------------------
# PARETO ANALYSIS
# -------------------------------------------------
st.subheader("Customer Revenue Concentration (Pareto)")

customer_rev = df.groupby("Customer_ID")["Sales"].sum().sort_values(ascending=False)
cumulative = customer_rev.cumsum() / total_revenue * 100

fig3, ax3 = plt.subplots()
ax3.plot(cumulative.values)
ax3.set_ylabel("Cumulative Revenue %")
ax3.set_xlabel("Customers Ranked")
st.pyplot(fig3)

# -------------------------------------------------
# DIAGNOSTIC FLAGS
# -------------------------------------------------
st.subheader("Performance Diagnostics")

lowest_margin_category = (
    df.groupby("Category")
    .apply(lambda x: x["Profit"].sum() / x["Sales"].sum())
    .sort_values()
    .index[0]
)

weakest_region = region_contrib.sort_values().index[0]

st.write(f"- Lowest Margin Category: **{lowest_margin_category}**")
st.write(f"- Weakest Revenue Region: **{weakest_region}**")
st.write(f"- Profit per Order: **${profit_per_order:.2f}**")
st.write(f"- Revenue per Customer: **${revenue_per_customer:.2f}**")

conn.close()