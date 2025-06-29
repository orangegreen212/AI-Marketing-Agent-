import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🧪 Minimal App Test")

@st.cache_data
def load_predictions():
    url = "https://drive.google.com/uc?id=1LGdi__hMVNflhyTf3ZhzGgYJwt0_o4MD"
    return pd.read_csv(url)

@st.cache_data
def load_total():
    url = "https://drive.google.com/uc?id=1cCxHQriyEPCPcZ35gcuxpJRUSU7mKopI"
    return pd.read_csv(url)

try:
    st.subheader("🔹 Loading Predictions File")
    pred_df = load_predictions()
    st.success(f"Predictions Loaded: {pred_df.shape[0]} rows")
    st.dataframe(pred_df.head())

    st.subheader("🔹 Loading Total File")
    total_df = load_total()
    st.success(f"Total File Loaded: {total_df.shape[0]} rows")
    st.dataframe(total_df.head())

    st.subheader("🔹 Merging on `user_id`")
    merged_df = pd.merge(pred_df, total_df, on="user_id", how="left")
    st.success(f"Merged Data: {merged_df.shape[0]} rows")
    st.dataframe(merged_df.head())

except Exception as e:
    st.error(f"❌ Error: {e}")
