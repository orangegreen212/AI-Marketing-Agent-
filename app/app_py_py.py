import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        h1 { color: #3F8CFF; text-align: center; }
        .stMetricValue { color: #1a1a1a; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 📉 Customer Retention & Churn Dashboard")

@st.cache_data
def load_data():
    predictions_url = "https://drive.google.com/uc?id=1LGdi__hMVNflhyTf3ZhzGgYJwt0_o4MD"
    total_url = "https://drive.google.com/uc?id=1cCxHQriyEPCPcZ35gcuxpJRUSU7mKopI"
    pred_df = pd.read_csv(predictions_url)
    total_df = pd.read_csv(total_url)
    df = pd.merge(pred_df, total_df, on="user_id", how="left")
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
segment = st.sidebar.selectbox("Behavioral Segment", ["All"] + sorted(df['Behavioral_Segment'].dropna().unique()))
customer_type = st.sidebar.selectbox("Customer Type", ["All"] + sorted(df['customer_type'].dropna().unique()))

filtered_df = df.copy()
if segment != "All":
    filtered_df = filtered_df[filtered_df['Behavioral_Segment'] == segment]
if customer_type != "All":
    filtered_df = filtered_df[filtered_df['customer_type'] == customer_type]

# === Tabs ===
tab1, tab2 = st.tabs(["📊 Overview", "🧠 AI Recommendations"])

# --- Tab 1 ---
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Users", f"{len(filtered_df):,}")
    col2.metric("📈 Avg Probability", f"{filtered_df['probability'].mean():.2f}")
    churn_rate = 1 - filtered_df["actual_activity"].mean()
    col3.metric("❌ Churn Rate", f"{churn_rate:.2%}")

    st.subheader("📈 Probability Distribution")
    fig1 = px.histogram(
        filtered_df, x="probability", color="predicted_status",
        nbins=30, barmode="overlay",
        color_discrete_map={"Churn": "red", "Retention": "green"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📌 Retention Rate by Behavioral Segment")
    seg_chart = (
        filtered_df.groupby("Behavioral_Segment")["actual_activity"]
        .mean().reset_index().rename(columns={"actual_activity": "Retention Rate"})
    )
    fig2 = px.bar(seg_chart, x="Behavioral_Segment", y="Retention Rate", color="Behavioral_Segment")
    st.plotly_chart(fig2, use_container_width=True)

# --- Tab 2 ---
with tab2:
    st.markdown("### 🧠 AI Agent Recommendations")

    if segment == "All":
        st.info("Please select a specific Behavioral Segment to generate recommendations.")
    else:
        st.success(f"Segment selected: **{segment}**")

        insights = {
            "promising / active shoppers": [
                "👉 Send personalized discounts via email.",
                "✅ Invite to loyalty program.",
                "🧲 Use social media retargeting."
            ],
            "newcomers / casual visitors": [
                "📢 Welcome campaign with bonuses.",
                "🔍 Tips, onboarding, and FAQs.",
                "📬 Reminders for incomplete actions."
            ],
            "at risk": [
                "🔥 'Only today' limited-time offer.",
                "🕵️ Check communication channel freshness.",
                "📉 Offer based on last activity date."
            ],
            "can't lose them": [
                "🎁 Reward or status upgrade.",
                "📣 Private sale invitations.",
                "🤝 Satisfaction survey."
            ],
            "Champions / VIP": [
                "👑 Exclusive offers and service.",
                "🎉 Access to private events.",
                "💎 VIP bonuses and rewards."
            ]
        }

        for tip in insights.get(segment.lower(), ["❓ No recommendations found."]):
            st.markdown(f"- {tip}")

        st.markdown("---")
        st.markdown("📬 **Want to launch a full email campaign?**")
        st.markdown("[➡️ Go to Email Generator App](https://92ojbikbpkzxyjzjcymybp.streamlit.app/)")
