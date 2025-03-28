import streamlit as st
import pandas as pd

# --------------------------------------
# ✅ Page Configuration
# --------------------------------------
st.set_page_config(
    page_title="Online Sales Dashboard",
    page_icon="🧴",
    layout="wide"
)

# --------------------------------------
# ✅ Load & Prepare Data
# --------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Online_Retail.csv", encoding='latin1')
    df = df.dropna(subset=["Description", "CustomerID"])
    df["TotalSales"] = df["Quantity"] * df["UnitPrice"]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()

# --------------------------------------
# ✅ Title & Description
# --------------------------------------
st.title("🧴 Online Sales Insights Dashboard")
st.markdown("""
Explore top-selling products by country and time period.  
Great for identifying product trends and marketing opportunities.
""")

# --------------------------------------
# ✅ Sidebar Filters
# --------------------------------------
with st.sidebar:
    st.header("🔍 Filter Options")
    selected_country = st.selectbox("Select Country", sorted(df["Country"].unique()))
    date_range = st.date_input(
        "Select Date Range",
        [df["InvoiceDate"].min().date(), df["InvoiceDate"].max().date()]
    )

# --------------------------------------
# ✅ Filter Data
# --------------------------------------
filtered_df = df[
    (df["Country"] == selected_country) &
    (df["InvoiceDate"].dt.date >= date_range[0]) &
    (df["InvoiceDate"].dt.date <= date_range[1])
]

# --------------------------------------
# ✅ Summary Metrics
# --------------------------------------
st.markdown("### 📈 Overview")
col1, col2 = st.columns(2)
col1.metric("Total Transactions", len(filtered_df))
col2.metric("Total Sales", f"${filtered_df['TotalSales'].sum():,.2f}")

# --------------------------------------
# ✅ Top 5 Products Chart
# --------------------------------------
top_products = (
    filtered_df.groupby("Description")["TotalSales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.markdown(f"### 🏆 Top 5 Products in {selected_country}")
st.bar_chart(top_products)

# --------------------------------------
# ✅ Data Table
# --------------------------------------
st.markdown("### 📋 Product Sales Table")
st.dataframe(
    top_products.reset_index().rename(
        columns={"Description": "Product", "TotalSales": "Sales"}
    )
)

# --------------------------------------
# ✅ Simulated ROPA Table
# --------------------------------------
st.markdown("### 🔐 Record of Processing Activities (ROPA) – Example")

# Simulated ROPA data
ropa_data = {
    "Data Type": ["Customer Name", "Email Address", "Purchase History", "Country"],
    "Purpose": ["Personalization", "Loyalty Program", "Product Recommendations", "Localization"],
    "Retention Period": ["2 years", "2 years", "5 years", "5 years"],
    "Accessed By": ["Marketing Team", "CRM System", "Analytics Team", "Localization Tool"],
    "Legal Basis": ["Consent", "Consent", "Legitimate Interest", "Contract"]
}

ropa_df = pd.DataFrame(ropa_data)

st.dataframe(ropa_df)

# --------------------------------------
# ✅ Footer
# --------------------------------------
st.markdown("---")
st.caption("📊 Built with ❤️ by Khwanchat | Data: UCI Online Retail")
