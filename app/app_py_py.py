import streamlit as st
import pandas as pd
import plotly.express as px

# --- Custom CSS ---
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        h1 { color: #3F8CFF; }
        .stMetricValue { color: #1a1a1a; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #3F8CFF;'>📉 Customer Retention & Churn Dashboard</h1>", unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    pred_url = "https://drive.google.com/uc?id=1LGdi__hMVNflhyTf3ZhzGgYJwt0_o4MD"
    total_url = "https://drive.google.com/uc?id=1cCxHQriyEPCPcZ35gcuxpJRUSU7mKopI"
    pred_df = pd.read_csv(pred_url)
    total_df = pd.read_csv(total_url)
    merged = pd.merge(pred_df, total_df, on="user_id", how="left")
    return merged

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
segment = st.sidebar.selectbox("Behavioral Segment", ["All"] + sorted(df['Behavioral_Segment'].dropna().unique().tolist()))
customer_type = st.sidebar.selectbox("Customer Type", ["All"] + sorted(df['customer_type'].dropna().unique().tolist()))

filtered_df = df.copy()
if segment != "All":
    filtered_df = filtered_df[filtered_df['Behavioral_Segment'] == segment]
if customer_type != "All":
    filtered_df = filtered_df[filtered_df['customer_type'] == customer_type]

# --- Tabs ---
tab1, tab2 = st.tabs(["📊 Overview", "🧠 AI Recommendations"])

# --- Tab 1: Overview ---
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Users", f"{len(filtered_df):,}")
    col2.metric("📈 Avg Retention Probability", f"{filtered_df['probability'].mean():.2f}")
    churn_rate = 1 - filtered_df["actual_activity"].mean()
    col3.metric("❌ Churn Rate", f"{churn_rate:.2%}")

    st.subheader("📈 Probability Distribution")
    fig1 = px.histogram(filtered_df, x="probability", color="predicted_status",
                        color_discrete_map={"Churn": "red", "Retention": "green"},
                        nbins=30, barmode="overlay")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📌 Retention Rate by Behavioral Segment")
    chart_data = (
        filtered_df.groupby("Behavioral_Segment")["actual_activity"]
        .mean().reset_index().rename(columns={"actual_activity": "Retention Rate"})
    )
    fig2 = px.bar(chart_data, x="Behavioral_Segment", y="Retention Rate", color="Behavioral_Segment")
    st.plotly_chart(fig2, use_container_width=True)

# --- Tab 2: AI Recommendations ---
with tab2:
    st.markdown("### 🧠 AI Agent Recommendations")

    if segment == "All":
        st.info("Please select a specific Behavioral Segment to generate recommendations.")
    else:
        st.success(f"Segment selected: **{segment}**")

        insights = {
            "promising / active shoppers": [
                "👉 Send them an email with personalized discounts.",
                "✅ Offer a loyalty program.",
                "🧲 Use social media retargeting."
            ],
            "newcomers / casual visitors": [
                "📢 Run a welcome campaign with bonuses.",
                "🔍 Help with onboarding (FAQ, tips).",
                "📬 Remind about incomplete actions (cart, viewed items)."
            ],
            "at risk": [
                "🔥 Send a 'one-day-only' offer.",
                "🕵️ Review your communication channels.",
                "📉 Check their last activity and offer a bonus."
            ],
            "can't lose them": [
                "🎁 Give a loyalty gift or bonus level-up.",
                "📣 Private sales access.",
                "🤝 Satisfaction survey to show care."
            ],
            "Champions / VIP": [
                "👑 Exclusive offers and service.",
                "🎉 Invite to private events.",
                "💎 VIP bonuses and rewards."
            ]
        }

        for tip in insights.get(segment.lower(), ["❓ No recommendations for selected segment."]):
            st.markdown(f"- {tip}")

        st.markdown("---")
        st.markdown("📬 **Want to launch a full email campaign?**")
        st.markdown("[➡️ Go to Email Generator App](https://92ojbikbpkzxyjzjcymybp.streamlit.app/)")

