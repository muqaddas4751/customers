import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Enterprise Analytics Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data.csv")

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center; color:#2E86C1;'>📊 Enterprise Sales Intelligence Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:gray;'>Real-World Business Analytics & Insights Platform</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- FILTERS ----------------
st.sidebar.header("🔍 Smart Filters")

city = st.sidebar.multiselect("City", df["City"].unique(), default=df["City"].unique())
category = st.sidebar.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())
month = st.sidebar.multiselect("Month", df["Month"].unique(), default=df["Month"].unique())

filtered_df = df[
    (df["City"].isin(city)) &
    (df["Category"].isin(category)) &
    (df["Month"].isin(month))
]

# ---------------- KPIs ----------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
avg_sales = filtered_df["Sales"].mean()

profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

best_city = filtered_df.groupby("City")["Sales"].sum().idxmax()
best_product = filtered_df.groupby("Product")["Sales"].sum().idxmax()

# ---------------- KPI CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"{total_sales:,}")
col2.metric("📈 Total Profit", f"{total_profit:,}")
col3.metric("📊 Avg Sales", f"{avg_sales:,.0f}")
col4.metric("📉 Profit %", f"{profit_margin:.2f}%")

st.divider()

# ---------------- EXECUTIVE INSIGHTS ----------------
st.subheader("📌 Executive Summary")

st.success(f"🏆 Best Performing City: {best_city}")
st.info(f"🛍️ Best Selling Product: {best_product}")

if profit_margin > 30:
    st.success("🔥 High Profit Margin Business")
elif profit_margin > 15:
    st.warning("⚠️ Moderate Profit Performance")
else:
    st.error("❌ Low Profit Margin - Needs Improvement")

st.divider()

# ---------------- TOP ANALYSIS ----------------
st.subheader("🏆 Top Business Performers")

colA, colB = st.columns(2)

with colA:
    st.write("Top 5 Products")
    top_products = filtered_df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top_products)

with colB:
    st.write("Top 5 Customers")
    top_customers = filtered_df.groupby("Name")["Sales"].sum().sort_values(ascending=False).head(5)
    st.bar_chart(top_customers)

st.divider()

# ---------------- DATA TABLE ----------------
st.subheader("📄 Business Data View")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- DOWNLOAD ----------------
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Full Report", csv, "enterprise_report.csv", "text/csv")

st.divider()

# ---------------- CITY ANALYSIS ----------------
st.subheader("📍 City Performance Analysis")

city_sales = filtered_df.groupby("City")["Sales"].sum()

fig1, ax1 = plt.subplots()
city_sales.plot(kind="bar", ax=ax1, color="#3498DB")
ax1.set_ylabel("Sales")
st.pyplot(fig1)

st.divider()

# ---------------- PRODUCT ANALYSIS ----------------
st.subheader("🛍️ Product Performance Analysis")

product_sales = filtered_df.groupby("Product")["Sales"].sum()

fig2, ax2 = plt.subplots()
product_sales.plot(kind="bar", ax=ax2, color="#F39C12")
ax2.set_ylabel("Sales")
st.pyplot(fig2)

st.divider()

# ---------------- CATEGORY INSIGHT ----------------
st.subheader("💰 Category Profit Distribution")

profit_cat = filtered_df.groupby("Category")["Profit"].sum()

fig3, ax3 = plt.subplots()
ax3.pie(profit_cat, labels=profit_cat.index, autopct="%1.1f%%")
st.pyplot(fig3)

st.divider()

# ---------------- MONTHLY TREND ----------------
st.subheader("📈 Monthly Growth Trend")

monthly_sales = filtered_df.groupby("Month")["Sales"].sum()

fig4, ax4 = plt.subplots()
monthly_sales.plot(kind="line", marker="o", ax=ax4, color="green")
ax4.set_ylabel("Sales Growth")
st.pyplot(fig4)

st.divider()

# ---------------- FOOTER ----------------
st.success("🚀 Enterprise Dashboard Ready | Professional Business Intelligence System")