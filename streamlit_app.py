
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Odisha Dashboard", layout="wide")
st.title("📊 Odisha Market Dashboard")

# Sidebar thresholds
st.sidebar.header("Customize Thresholds")
reach_green = st.sidebar.slider("Reach: Green if >", 0, 100, 75)
reach_yellow = st.sidebar.slider("Reach: Yellow if >", 0, reach_green, 60)

sob_green = st.sidebar.slider("SOB: Green if >", 0, 100, 60)
sob_yellow = st.sidebar.slider("SOB: Yellow if >", 0, sob_green, 45)

ms_green = st.sidebar.slider("M/S: Green if >", 0, 100, 30)
ms_yellow = st.sidebar.slider("M/S: Yellow if >", 0, ms_green, 15)

# File uploader
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df = df.dropna(subset=['District'])
    st.subheader("Raw Data Preview")
    st.dataframe(df, use_container_width=True)

    # Summary Stats
    st.subheader("Summary Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Market Size", int(df['Market Size'].sum()))
    with col2:
        st.metric("Average Reach", f"{df['Reach'].mean():.0f}%")
    with col3:
        st.metric("Total Active Dealers", int(df['Active Dealer'].sum()))

    # Visualizations
    st.subheader("Bar Chart: Reach / SOB / M/S by District")
    bar_df = df[['District', 'Reach', 'SOB', 'M/S']].melt(id_vars='District', var_name='Metric', value_name='Value')
    fig = px.bar(bar_df, x='District', y='Value', color='Metric', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

    # Color coding table
    def color_code(row):
        def color(metric, val, green, yellow):
            if val > green:
                return 'background-color: #00B050'
            elif val > yellow:
                return 'background-color: #FFFF00'
            else:
                return 'background-color: #FF0000'

        return [
            '', '', '', '', '', '', 
            color('Reach', row['Reach'], reach_green, reach_yellow),
            color('SOB', row['SOB'], sob_green, sob_yellow),
            color('M/S', row['M/S'], ms_green, ms_yellow),
            '', '', '', '', ''
        ]

    styled_df = df.style.apply(color_code, axis=1)
    st.subheader("Color-Coded Table")
    st.dataframe(styled_df, use_container_width=True)

    # Optional download
    st.subheader("Download Color-Coded Excel (Planned Feature)")
    st.caption("Feature planned: This will allow exporting styled Excel with colors.")
else:
    st.info("Please upload an Excel file to begin.")
