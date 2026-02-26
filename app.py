import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="BIM Prediction Dashboard – Ethiopia",
    page_icon="🏗️",
    layout="wide"
)

# Load latest enriched CSV automatically 
@st.cache_data
def load_data():
    DATA_DIR = Path("data/synthetic_bim")
    
    if not DATA_DIR.exists():
        st.error(f"Folder not found: {DATA_DIR.absolute()}")
        st.stop()
    
    priority_patterns = ["*ready*.csv", "*phase3*.csv", "*enriched*.csv", "*.csv"]
    csv_files = []
    for pattern in priority_patterns:
        csv_files.extend(DATA_DIR.glob(pattern))
    
    if not csv_files:
        st.error("No CSV files found in data/synthetic_bim/")
        st.info("Folder contents: " + ", ".join([f.name for f in DATA_DIR.glob("*")]))
        st.stop()
    
    # Take the newest file
    latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
    df = pd.read_csv(latest_file)
    
    st.success(f"Loaded: {latest_file.name} ({len(df)} elements)")
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

if "ElementType" in df.columns:
    element_types = df["ElementType"].unique()
    selected_types = st.sidebar.multiselect("Element Types", element_types, default=element_types)

if "Material" in df.columns:
    materials = df["Material"].unique()
    selected_materials = st.sidebar.multiselect("Materials", materials, default=materials)

if "TotalCost_ETB" in df.columns:
    min_cost = st.sidebar.slider("Min Total Cost (ETB)", 0, int(df["TotalCost_ETB"].max() or 0), 0)
    max_cost = st.sidebar.slider("Max Total Cost (ETB)", 0, int(df["TotalCost_ETB"].max() or 0), int(df["TotalCost_ETB"].max() or 0))

# Apply filters safely
filtered_df = df.copy()
if "ElementType" in df.columns:
    filtered_df = filtered_df[filtered_df["ElementType"].isin(selected_types)]
if "Material" in df.columns:
    filtered_df = filtered_df[filtered_df["Material"].isin(selected_materials)]
if "TotalCost_ETB" in df.columns:
    filtered_df = filtered_df[filtered_df["TotalCost_ETB"].between(min_cost, max_cost)]

#Dashboard
st.title("🏗️ BIM Data Automation & Prediction Dashboard")

# Metrics row – safe checks
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Elements", len(filtered_df))

if "TotalCost_ETB_pred" in filtered_df.columns:
    col2.metric("Predicted Costs", f"{filtered_df['TotalCost_ETB_pred'].notna().sum():,}")
else:
    col2.metric("Predicted Costs", "N/A")

if "IsHighValue" in filtered_df.columns:
    col3.metric("High Value Items", filtered_df["IsHighValue"].sum())
else:
    col3.metric("High Value Items", "N/A")

if "ClashStatus" in filtered_df.columns:
    col4.metric("Flagged Clashes", filtered_df["ClashStatus"].str.contains("Clash", case=False, na=False).sum())
else:
    col4.metric("Flagged Clashes", "N/A")

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Data Table", "Issues & Predictions"])

with tab1:
    if "TotalCost_ETB" in filtered_df.columns:
        st.subheader("Cost Distribution")
        fig_cost = px.histogram(filtered_df, x="TotalCost_ETB", nbins=50, title="Total Cost Distribution (ETB)")
        st.plotly_chart(fig_cost, use_container_width=True)

    if "TotalCost_ETB" in filtered_df.columns and "TotalCost_ETB_pred" in filtered_df.columns:
        st.subheader("Predicted vs Actual Cost")
        fig_pred = px.scatter(filtered_df, x="TotalCost_ETB", y="TotalCost_ETB_pred", 
                              color="ElementType" if "ElementType" in filtered_df.columns else None,
                              hover_data=["ElementType", "Material", "RoomName"],
                              title="Predicted vs Actual Total Cost")
        st.plotly_chart(fig_pred, use_container_width=True)

with tab2:
    st.subheader(f"Showing {len(filtered_df)} filtered elements")
    
    format_dict = {}
    if "TotalCost_ETB" in filtered_df.columns:
        format_dict["TotalCost_ETB"] = "{:,.0f}"
    if "TotalCost_ETB_pred" in filtered_df.columns:
        format_dict["TotalCost_ETB_pred"] = "{:,.0f}"
    if "Area_m2" in filtered_df.columns:
        format_dict["Area_m2"] = "{:.2f}"
    if "Volume_m3" in filtered_df.columns:
        format_dict["Volume_m3"] = "{:.3f}"

    st.dataframe(
        filtered_df.style.format(format_dict),
        use_container_width=True,
        hide_index=True
    )

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered CSV", csv, "bim_filtered.csv", "text/csv")

with tab3:
    st.subheader("Issues & Predictions")
    
    if "IsHighValue" in filtered_df.columns:
        high_value = filtered_df[filtered_df["IsHighValue"] == True]
        st.metric("High Value Items", len(high_value))
        if not high_value.empty:
            st.dataframe(high_value[["ElementType", "Material", "TotalCost_ETB", "IsHighValue"]])
    
    if "ClashStatus" in filtered_df.columns:
        clashes = filtered_df[filtered_df["ClashStatus"].str.contains("Clash", case=False, na=False)]
        st.metric("Flagged Clashes", len(clashes))
        if not clashes.empty:
            st.dataframe(clashes[["ElementType", "RoomName", "ClashStatus"]])
    
    st.info("No separate anomaly/clash columns found → using IsHighValue & ClashStatus instead.")

# Footer
st.markdown("---")
st.caption("Developed by **Aklilu Abera** • **Python Engineer** (AI & Data Automation)")