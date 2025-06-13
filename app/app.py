import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Припускаємо, що PROMPT_TEMPLATE визначений десь тут, як і раніше
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

1.  **Тема листа (Subject):** Має бути інтригуючою та персоналізованою.
2.  **Тіло листа (Body):**
    *   **Звернення:** Привітай клієнта на ім'я або дружньо.
    *   **Визнання статусу:** Подякуй за лояльність або привітай з поверненням, базуючись на сегменті.
    *   **Плавний перехід:** Зв'яжи новинку з інтересами клієнта.
    *   **Опис товару:** Коротко і привабливо.
    *   **Заклик до дії (Call to Action):** Чітка кнопка або посилання.
    *   **Персональна пропозиція:** Яскраво виділи знижку та промокод.
    *   **Завершення:** Дружнє і тепле.
"""


# --- Ініціалізація клієнта ---
# Використовуємо st.secrets для безпечного доступу до ключа
try:
    client = MistralClient(api_key=st.secrets["MISTRAL_API_KEY"])
    API_KEY_CONFIGURED = True
except (KeyError, FileNotFoundError):
    API_KEY_CONFIGURED = False


def generate_email_mistral(customer_data, model_name="mistral-small-latest"):
    """Викликає Mistral API для генерації листа."""
    filled_prompt = PROMPT_TEMPLATE.format(**customer_data)
    
    try:
        messages = [
            ChatMessage(role="user", content=filled_prompt)
        ]
        
        chat_response = client.chat(
            model=model_name,
            messages=messages,
            temperature=0.7
        )
        
        return chat_response.choices[0].message.content
    except Exception as e:
        return f"Помилка при виклику API Mistral: {e}"

# --- ІНТЕРФЕЙС STREAMLIT ---
st.title("🤖 Генератор персоналізованих Email")

if API_KEY_CONFIGURED:
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
        
        # ВИПРАВЛЕНО: Текст для відповідності Mistral
        with st.spinner("Магія Mistral працює... ✨"):
            # ВИПРАВЛЕНО: Назва функції тепер правильна
            email_text = generate_email_mistral(customer_data)
        
        st.subheader("Згенерований лист:")
        st.markdown(email_text)
else:
    st.error("API-ключ Mistral не налаштовано! Будь ласка, додайте MISTRAL_API_KEY до ваших секретів Streamlit.")
