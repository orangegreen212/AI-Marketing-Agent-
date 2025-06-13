
import os

import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# ... (код ініціалізації клієнта) ...
client = MistralClient(api_key=st.secrets["MISTRAL_API_KEY"])


def generate_email_mistral(customer_data, model_name="mistral-small-latest"):
    """Викликає Mistral API для генерації листа."""
    filled_prompt = PROMPT_TEMPLATE.format(**customer_data)
    
    try:
        # Формуємо повідомлення для чату
        messages = [
            ChatMessage(role="user", content=filled_prompt)
        ]
        
        #
        # --- ОСЬ ТУТ КЛЮЧОВИЙ МОМЕНТ ---
        # Викликаємо метод .chat() напряму з об'єкта client
        #
        chat_response = client.chat(
            model=model_name,
            messages=messages,
            temperature=0.7
        )
        # --- КІНЕЦЬ КЛЮЧОВОГО МОМЕНТУ ---
        #
        
        return chat_response.choices[0].message.content
    except Exception as e:
        return f"Помилка при виклику API Mistral: {e}"

# ... (решта вашого коду Streamlit) ...

# --- ІНТЕРФЕЙС STREAMLIT ---
st.title("🤖 Генератор персоналізованих Email")

with st.form("customer_form"):
    st.header("Дані про клієнта та пропозицію")
    
    customer_segment = st.selectbox("Сегмент клієнта", ["VIP / Чемпіони", "Лояльні / Регулярні покупці", "Оптові покупці / Професіонали", "Новачки"])
    interested_categories = st.text_input("Категорії, що цікавлять", "парфуми, nail art")
    new_product_name = st.text_input("Назва нового товару", "Лак для нігтів 'Galaxy Dust'")
    discount_amount = st.text_input("Розмір знижки", "20%")
    promo_code = st.text_input("Промокод", "GALAXY20")
    
    submitted = st.form_submit_button("Згенерувати лист")

if submitted:
    customer_data = {
        "customer_segment": customer_segment,
        "interested_categories": interested_categories,
        "average_check": "45.00$",
        "customer_name": "шановний клієнте",
        "new_product_name": new_product_name,
        "new_product_category": "nail art",
        "discount_amount": discount_amount,
        "promo_code": promo_code,
    }
    
    with st.spinner("Магія GPT працює... ✨"):
        email_text = generate_email_chatgpt(customer_data)
    
    st.subheader("Згенерований лист:")
    st.markdown(email_text)

