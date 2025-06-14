import streamlit as st
import pandas as pd
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# --- КОНФІГУРАЦІЯ І ФУНКЦІЇ ---

PROMPT_TEMPLATE = """
Ти — досвідчений маркетолог та талановитий копірайтер нашого інтернет-магазину косметики та парфумерії. Твоє завдання — згенерувати персоналізований, теплий та дружній email для нашого клієнта. Уникай кліше та занадто "роботизованих" фраз.

**Вхідні дані про клієнта:**
*   **RFM Сегмент:** {rfm_segment}
*   **Поведінковий Сегмент:** {behavioral_segment}
*   **Середній чек (Monetary):** {monetary_value:.2f}$
*   **Ім'я клієнта:** {customer_name}

**Завдання:**
Згенеруй текст листа з рекомендацією нового товару та персональною знижкою. Адаптуй тон і пропозицію до сегментів клієнта.

*   **Товар для рекомендації:** {new_product_name}
*   **Розмір знижки:** {discount_amount}
*   **Промокод:** {promo_code}

**Структура листа, якої потрібно дотримуватися:**

1.  **Тема листа (Subject):** Має бути інтригуючою та персоналізованою. Для VIP клієнтів зроби її більш ексклюзивною. Для "At Risk" — більш спонукальною.

2.  **Тіло листа (Body):**
    *   **Звернення:** Привітай клієнта на ім'я.
    *   **Визнання статусу (використовуй RFM сегмент):**
        *   Для "Champions / VIP": Подякуй за виняткову лояльність.
        *   Для "Loyal Customers": Скажи, що цінуєш його як постійного клієнта.
        *   Для "At Risk": Скажи, що сумуєш і хочеш зробити подарунок для повернення.
    *   **Плавний перехід (використовуй Поведінковий сегмент):**
        *   Для "Promising / Active Shoppers": "Ми бачимо, ви активно цікавитесь новинками..."
        *   Для "Decisive Shoppers": "Знаємо, що ви цінуєте свій час, тому ось пряма рекомендація для вас..."
    *   **Опис товару:** Коротко і привабливо опиши {new_product_name}.
    *   **Персональна пропозиція:** Яскраво виділи знижку {discount_amount} та промокод {promo_code}.
    *   **Завершення:** Дружнє і тепле.
"""

# Ініціалізація клієнта Mistral
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

# --- НОВИЙ ІНТЕРФЕЙС STREAMLIT ДЛЯ МАСОВОЇ ГЕНЕРАЦІЇ ---

st.set_page_config(layout="wide")
st.title("🚀 Генератор персоналізованих Email на базі сегментів")

if not API_KEY_CONFIGURED:
    st.error("API-ключ Mistral не налаштовано! Будь ласка, додайте MISTRAL_API_KEY до ваших секретів Streamlit.")
else:
    uploaded_file = st.file_uploader(
        "1. Завантажте ваш майстер-файл з сегментами (master_customer_profiles.csv)", 
        type="csv"
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Видаляємо ботів та аномалії
        df = df[~df['Behavioral_Segment'].str.contains("Bot|Anomaly", na=False)]
        
        st.success(f"Файл успішно завантажено! Знайдено {len(df)} реальних клієнтів.")
        
        col1, col2 = st.columns(2)

        with col1:
            st.header("2. Оберіть цільову аудиторію")
            # Вибір сегментів для кампанії
            rfm_segments_to_target = st.multiselect(
                "Оберіть RFM сегменти:", 
                options=df['RFM_Segment'].unique(),
                default=df['RFM_Segment'].unique()[0] # За замовчуванням обираємо перший
            )
            behavioral_segments_to_target = st.multiselect(
                "Оберіть Поведінкові сегменти:",
                options=df['Behavioral_Segment'].unique(),
                default=df['Behavioral_Segment'].unique()[0]
            )
            
            # Фільтруємо користувачів
            target_users = df[
                df['RFM_Segment'].isin(rfm_segments_to_target) & 
                df['Behavioral_Segment'].isin(behavioral_segments_to_target)
            ]
            st.write(f"Знайдено **{len(target_users)}** користувачів для кампанії.")

        with col2:
            st.header("3. Налаштуйте параметри кампанії")
            new_product_name = st.text_input("Назва товару для рекомендації", "Сироватка 'Magic Glow'")
            discount_amount = st.text_input("Розмір знижки", "15%")
            promo_code = st.text_input("Промокод", "MAGIC15")

        if st.button(f"🚀 Згенерувати листи для {len(target_users)} користувачів"):
            st.subheader("Згенеровані листи (показано перші 5):")
            
            # Обмежуємо кількість для демонстрації
            users_to_process = target_users.head(5) 
            
            for _, user_profile in users_to_process.iterrows():
                with st.spinner(f"Генеруємо лист для user_id: {user_profile['user_id']}..."):
                    # Збираємо дані для промпта з рядка DataFrame
                    customer_data = {
                        "rfm_segment": user_profile["RFM_Segment"],
                        "behavioral_segment": user_profile["Behavioral_Segment"],
                        "monetary_value": user_profile["Monetary"],
                        "customer_name": f"клієнт {user_profile['user_id']}",
                        "interested_categories": "парфуми, догляд за шкірою", # Це поле можна буде додати в майбутньому
                        "new_product_name": new_product_name,
                        "discount_amount": discount_amount,
                        "promo_code": promo_code,
                    }
                    
                    email_text = generate_email_mistral(client, customer_data)
                    
                    with st.expander(f"Лист для користувача ID: {user_profile['user_id']} (RFM: {user_profile['RFM_Segment']}, Поведінка: {user_profile['Behavioral_Segment']})"):
                        st.markdown(email_text)

            st.success("Генерація демонстраційних листів завершена!")
