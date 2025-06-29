import streamlit as st
import pandas as pd
import plotly.express as px

# ========== Custom CSS ==========
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        h1 { color: #3F8CFF; }
        .stMetricValue { color: #1a1a1a; font-weight: bold; }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f0f2f6;
            border-radius: 8px;
            padding: 0.25rem;
        }
    </style>
""", unsafe_allow_html=True)

# === HEADER ===
st.markdown("<h1 style='text-align: center; color: #3F8CFF;'>📉 Customer Retention & Churn Dashboard</h1>", unsafe_allow_html=True)

# === Data Loading ===
preds_url = "https://drive.google.com/uc?id=1cCxHQriyEPCPcZ35gcuxpJRUSU7mKopI"
rfm_url = "https://drive.google.com/uc?id=1LGdi__hMVNflhyTf3ZhzGgYJwt0_o4MD"

@st.cache_data
def load_data():
    preds = pd.read_csv(preds_url)
    rfm = pd.read_csv(rfm_url)
    df = pd.merge(preds, rfm, on="user_id", how="left")
    return df

df = load_data()

# === Filters ===
st.sidebar.header("🔍 Filters")
segment = st.sidebar.selectbox("Behavioral Segment", ["All"] + sorted(df['Behavioral_Segment'].dropna().unique().tolist()))
customer_type = st.sidebar.selectbox("Customer Type", ["All"] + sorted(df['customer_type'].dropna().unique().tolist()))

# === Data Filtering ===
filtered_df = df.copy()
if segment != "All":
    filtered_df = filtered_df[filtered_df['Behavioral_Segment'] == segment]
if customer_type != "All":
    filtered_df = filtered_df[filtered_df['customer_type'] == customer_type]

# === Tabs ===
tab1, tab2 = st.tabs(["📊 Overview", "🧠 AI Recommendations"])

# --- Tab 1: Overview ---
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Users", f"{len(filtered_df):,}")
    col2.metric("📈 Avg Activity", f"{filtered_df['probability'].mean():.2f}")
    col3.metric("❌ Churn Rate", f"{1 - filtered_df['actual_activity'].mean():.2%}")

    st.subheader("📈 Probability Distribution")
    fig1 = px.histogram(filtered_df,
                        x="probability",
                        color="predicted_status",
                        color_discrete_map={"Retention": "green", "Churn": "red"},
                        nbins=30,
                        barmode="overlay",
                        labels={"predicted_status": "Predicted"})
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📌 Retention Rate by Segment")
    seg_chart = (
        filtered_df.groupby("Behavioral_Segment")["actual_activity"]
        .mean().reset_index().rename(columns={"actual_activity": "Retention Rate"})
    )
    fig2 = px.bar(seg_chart, x="Behavioral_Segment", y="Retention Rate", color="Behavioral_Segment")
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
                "✅ Offer them a loyalty program.",
                "🧲 Use social media retargeting."
            ],
            "newcomers / casual visitors": [
                "📢 Launch a welcome campaign with bonuses.",
                "🔍 Support their onboarding with tips and an FAQ.",
                "📬 Remind them about incomplete actions (e.g., abandoned cart, viewed items)."
            ],
            "at risk": [
                "🔥 Send a special 'today only' offer to create urgency.",
                "🕵️ Review your communication channels – they might be outdated.",
                "📉 Check when they were last active and offer a reactivation bonus."
            ],
            "can't lose them": [
                "🎁 Give a gift for loyalty or a level-up bonus.",
                "📣 Invite them to exclusive, members-only sales.",
                "🤝 Conduct a satisfaction survey to show you care."
            ],
            "Champions / VIP": [
                "👑 Provide personal offers and exclusive concierge service.",
                "🎉 Invite them to private events or product previews.",
                "💎 Implement a VIP bonus and rewards program."
            ]
        }

        for tip in insights.get(segment.lower(), ["❓ No recommendations available for the selected segment."]):
            st.markdown(f"- {tip}")

        st.markdown("---")
        st.markdown("📬 **Want to launch a full email campaign?**")
        st.markdown("[➡️ Go to Email Generator App](https://92ojbikbpkzxyjzjcymybp.streamlit.app/)")
