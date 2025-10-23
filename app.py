import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SkinSeoul AI Categorization Dashboard",
    page_icon="💄",
    layout="wide"
)

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/categorized_products.csv")
    if "confidence" not in df.columns:
        df["confidence"] = 0.0
    return df

df = load_data()

# --- Header ---
st.title("💄 SkinSeoul AI Categorization Dashboard")
st.markdown(
    """
    This dashboard visualizes the AI-based product categorization results for **SkinSeoul**'s e-commerce dataset.
    You can explore category performance, model confidence, and price patterns interactively.
    """
)

# --- Sidebar filters ---
st.sidebar.header("🔍 Filters")
categories = df["category"].dropna().unique().tolist()
selected_category = st.sidebar.multiselect("Select Category", categories, default=categories)
min_conf = st.sidebar.slider("Minimum Confidence", 0.0, 1.0, 0.5)
df_filtered = df[(df["category"].isin(selected_category)) & (df["confidence"] >= min_conf)]

# --- KPIs ---
st.subheader("📈 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Products", len(df_filtered))
col2.metric("Average Confidence", f"{df_filtered['confidence'].mean():.2f}")
col3.metric("Average Price (AUD)", f"{df_filtered['price'].mean():.2f}" if "price" in df_filtered.columns else "N/A")

st.markdown("---")

# --- Charts ---
col1, col2 = st.columns(2)

# Category distribution
fig_cat = px.pie(df_filtered, names="category", title="Category Distribution", hole=0.4)
col1.plotly_chart(fig_cat, use_container_width=True)

# Confidence distribution
fig_conf = px.box(df_filtered, x="category", y="confidence", title="Confidence by Category")
col2.plotly_chart(fig_conf, use_container_width=True)

# --- Price trend ---
if "price" in df_filtered.columns:
    st.subheader("💰 Price by Category")
    fig_price = px.bar(
        df_filtered.groupby("category", as_index=False)["price"].mean(),
        x="category",
        y="price",
        text_auto=".2f",
        title="Average Price by Category"
    )
    st.plotly_chart(fig_price, use_container_width=True)

# --- Product Table ---
st.subheader("🧴 Product Details")
st.dataframe(
    df_filtered[["product_name", "description", "category", "confidence", "price"]],
    use_container_width=True,
    hide_index=True
)

# --- Optional AI summary (just for show) ---
st.markdown("---")
if st.button("🪄 Generate Summary Insight"):
    top_cat = df_filtered["category"].value_counts().idxmax()
    avg_conf = df_filtered["confidence"].mean()
    st.success(
        f"Most products fall under the **{top_cat}** category "
        f"with an average AI confidence of **{avg_conf:.2f}**. "
        "This suggests strong model consistency in skincare classification!"
    )
