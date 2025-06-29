import streamlit as st
import pandas as pd

st.title("🔍 DEBUG: Загружаем и объединяем данные")

@st.cache_data
def load_data():
    try:
        st.write("📂 Загружаем predictions.csv")
        pred = pd.read_csv("https://drive.google.com/uc?id=1LGdi__hMVNflhyTf3ZhzGgYJwt0_o4MD")

        st.write("📂 Загружаем total_file.csv")
        total = pd.read_csv("https://drive.google.com/uc?id=1cCxHQriyEPCPcZ35gcuxpJRUSU7mKopI")

        st.write("🧬 Объединяем по user_id")
        merged = pd.merge(pred, total, on="user_id", how="left")

        st.success("✅ Данные успешно загружены и объединены")
        return merged
    except Exception as e:
        st.error(f"❌ Ошибка загрузки данных: {e}")
        return pd.DataFrame()

df = load_data()
if not df.empty:
    st.dataframe(df.head())
else:
    st.warning("Данных нет — проверяй ссылки и структуру CSV.")
