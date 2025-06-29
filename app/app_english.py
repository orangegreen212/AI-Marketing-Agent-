import streamlit as st
import pandas as pd
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# --- CONFIGURATION ---
PROMPT_TEMPLATE = """
You are an experienced marketer and a talented copywriter for our cosmetics and perfumery online store. Your task is to generate a personalized, warm, and friendly email for our customer. Avoid clichés and overly "robotic" phrases.

**Customer Input Data:**
*   **RFM Segment:** {rfm_segment}
*   **Behavioral Segment:** {behavioral_segment}
*   **Average Order Value (Monetary):** {monetary_value:.2f}$
*   **Customer Name:** {customer_name}

**Task:**
Generate the text for an email recommending a new product with a personal discount. Adapt the tone and offer to the customer's segments.

*   **Product to Recommend:** {new_product_name}
*   **Discount Amount:** {discount_amount}
*   **Promo Code:** {promo_code}

**Email structure to follow:**

1.  **Email Subject:** It should be intriguing and personalized. For VIP clients, make it more exclusive. For "At Risk" clients, make it more re-engaging.

2.  **Email Body:**
    *   **Greeting:** Greet the customer by name.
    *   **Acknowledge Status (use RFM segment):**
        *   For "Champions / VIP": Thank them for their exceptional loyalty.
        *   For "Loyal Customers": Say that you value them as a regular customer.
        *   For "At Risk": Say you miss them and want to offer a gift to win them back.
    *   **Smooth Transition (use Behavioral segment):**
        *   For "Promising / Active Shoppers": "We see you're actively interested in new arrivals..."
        *   For "Decisive Shoppers": "We know you value your time, so here's a direct recommendation for you..."
    *   **Product Description:** Briefly and attractively describe {new_product_name}.
    *   **Personal Offer:** Clearly highlight the {discount_amount} discount and the {promo_code} promo code.
    *   **Closing:** Friendly and warm.
"""

# --- API INIT ---
try:
    client = MistralClient(api_key=st.secrets["MISTRAL_API_KEY"])
    API_KEY_CONFIGURED = True
except (KeyError, FileNotFoundError):
    API_KEY_CONFIGURED = False

@st.cache_data
def generate_email_mistral(_client, customer_data, model_name="mistral-small-latest"):
    filled_prompt = PROMPT_TEMPLATE.format(**customer_data)
    messages = [ChatMessage(role="user", content=filled_prompt)]
    chat_response = _client.chat(model=model_name, messages=messages, temperature=0.7)
    return chat_response.choices[0].message.content

# --- PAGE CONFIG ---
st.set_page_config(layout="wide")
st.title("🚀 Segment-Based Personalized Email Generator")

if not API_KEY_CONFIGURED:
    st.error("Mistral API key is not configured! Please add MISTRAL_API_KEY to your Streamlit secrets.")
else:
    # ✅ Replace file upload with auto Google Drive fetch
    csv_url = "https://drive.google.com/uc?id=1LGdi__hMVNflhyTf3ZhzGgYJwt0_o4MD"


    @st.cache_data
    def load_data():
        return pd.read_csv(csv_url)

    try:
        df = load_data()
        df = df[~df['Behavioral_Segment'].str.contains("Bot|Anomaly", na=False)]
        st.success(f"✅ Dataset loaded successfully. Found {len(df)} real users.")

        col1, col2 = st.columns(2)

        with col1:
            st.header("1. Select Target Audience")
            rfm_segments_to_target = st.multiselect(
                "Select RFM segments:",
                options=df['RFM_Segment'].unique(),
                default=df['RFM_Segment'].unique()[0]
            )
            behavioral_segments_to_target = st.multiselect(
                "Select Behavioral segments:",
                options=df['Behavioral_Segment'].unique(),
                default=df['Behavioral_Segment'].unique()[0]
            )

            target_users = df[
                df['RFM_Segment'].isin(rfm_segments_to_target) &
                df['Behavioral_Segment'].isin(behavioral_segments_to_target)
            ]
            st.write(f"🎯 Found **{len(target_users)}** users for the campaign.")

        with col2:
            st.header("2. Configure Campaign Parameters")
            new_product_name = st.text_input("Product Name to Recommend", "Serum 'Magic Glow'")
            discount_amount = st.text_input("Discount Amount", "15%")
            promo_code = st.text_input("Promo Code", "MAGIC15")

        if st.button(f"🚀 Generate emails for {len(target_users)} users"):
            st.subheader("📧 Generated Emails (showing first 5):")
            users_to_process = target_users.head(5)

            for _, user_profile in users_to_process.iterrows():
                with st.spinner(f"Generating email for user_id: {user_profile['user_id']}..."):
                    customer_data = {
                        "rfm_segment": user_profile["RFM_Segment"],
                        "behavioral_segment": user_profile["Behavioral_Segment"],
                        "monetary_value": user_profile["Monetary"],
                        "customer_name": f"customer {user_profile['user_id']}",
                        "new_product_name": new_product_name,
                        "discount_amount": discount_amount,
                        "promo_code": promo_code,
                    }

                    email_text = generate_email_mistral(client, customer_data)

                    with st.expander(f"Email for User ID: {user_profile['user_id']} (RFM: {user_profile['RFM_Segment']}, Behavior: {user_profile['Behavioral_Segment']})"):
                        st.markdown(email_text)

            st.success("✅ Generation complete!")

    except Exception as e:
        st.error(f"🚫 Failed to load the dataset. Error: {e}")
