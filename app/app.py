
import os

import streamlit as st
import mistralai

# Правильний спосіб для Streamlit Cloud
mistralai.api_key = st.secrets["MISTRAL_API_KEY"]

PROMPT_TEMPLATE = """
Ти — досвідчений маркетолог та талановитий копірайтер нашого інтернет-магазину косметики та парфумерії. Твоє завдання — згенерувати персоналізований, теплий та дружній email для нашого клієнта. Уникай кліше та занадто "роботизованих" фраз.

**Вхідні дані про клієнта:**
*   **Сегмент:** {customer_segment}
*   **Категорії, що його цікавлять:** {interested_categories}
*   **Середній чек:** {average_check}
*   **Ім'я клієнта (якщо є):** {customer_name}

**Завдання:**
Згенеруй текст листа з рекомендацією нового товару та персональною знижкою.
*   **Товар для рекомендації:** {new_product_name}
*   **Категорія товару:** {new_product_category}
*   **Розмір знижки:** {discount_amount}
*   **Промокод:** {promo_code}

**Структура листа, якої потрібно дотримуватися:**

1.  **Тема листа (Subject):** Має бути інтригуючою та персоналізованою. Використовуй інформацію про улюблені категорії клієнта.

2.  **Тіло листа (Body):**
    *   **Звернення:** Привітай клієнта на ім'я. Якщо імені немає, використовуй дружнє "Вітаємо!".
    *   **Визнання статусу:** Базуючись на сегменті клієнта, почни лист.
        *   Для "VIP / Чемпіони" або "Оптові покупці": Подякуй за лояльність та довіру.
        *   Для "Лояльні / Регулярні покупці": Скажи, що ти цінуєш його як постійного клієнта.
        *   Для "Новачки" або "Затихаючі": Звернись з теплотою, скажи, що ти радий його бачити знову.
    *   **Плавний перехід до рекомендації:** Зв'яжи новий товар з улюбленими категоріями клієнта. Наприклад: "Ми знаємо, як ви любите {interested_categories}, тому вирішили, що вас точно зацікавить наша новинка..."
    *   **Опис товару:** Коротко і привабливо опиши {new_product_name}, підкреслюючи його переваги.
    *   **Заклик до дії (Call to Action):** Чітка кнопка або посилання, наприклад: "Дізнатись більше", "Подивитись новинку".
    *   **Персональна пропозиція:** Яскраво виділи інформацію про знижку {discount_amount} за промокодом {promo_code}. Вкажи, що ця пропозиція — саме для нього.
    *   **Завершення:** Дружнє і тепле завершення, наприклад: "З найкращими побажаннями, команда [Назва магазину]".
"""

def generate_email_chatgpt(customer_data):
    """Викликає ChatGPT API для генерації листа."""
    filled_prompt = PROMPT_TEMPLATE.format(**customer_data)
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти — копірайтер-маркетолог для магазину косметики."},
                {"role": "user", "content": filled_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Помилка при виклику API: {e}"

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

