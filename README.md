# 🤖 AI Marketing Agent

An interactive AI-powered dashboard that combines data analytics, user segmentation, and marketing content generation into one intelligent assistant.  
Built with **Python, Streamlit and Mistral**, this project helps marketers make smarter decisions through data-driven insights and AI suggestions.

---

## 🚀 Overview

This tool is designed to simulate how a junior data analyst or marketing team could use AI to:

- Understand user behavior from eCommerce event data.
- Segment customers using two complementary techniques:
  - **RFM Analysis**
  - **Behavioral Clustering** (based on interaction patterns)
- Visualize key marketing metrics such as funnel conversion.
- Interact with a conversational **AI Marketing Agent** that generates ideas and campaign strategies.

---

## 📊 Key Features

### 1. Conversion Funnel Visualization
Track user progression through the sales funnel:
- Product View → Add to Cart → Purchase
- Built with Plotly for interactive exploration.
- Helps identify drop-off stages and conversion efficiency.

### 2. Dual Segmentation Engine
Two segmentation approaches are implemented to provide a deeper understanding of customer behavior:

- **RFM Analysis**:
  - Segments customers based on Recency, Frequency, and Monetary value. Also using unsupervised learning K-Means
  - Clusters include: *New/Occasional Users*, *Loyal Customers*, *Champions*, *Promising / Potential Loyalists*, *Lost* and *At Risk*

- **Behavioral Clustering**:
  - Uses unsupervised learning (KMeans) on engagement metrics.
  - Clusters include: *Newcomers / Casual Visitors*, *Loyal / Regular Shoppers*, *Champions*, *Promising / Active Shoppers*

These two methods **complement each other**, offering layered insights for personalized marketing.

### 3. AI Marketing Agent
Built with  **Mistral** (via `mistralai`), this assistant can:

- Generate tailored marketing campaigns.
- Recommend next best actions for each segment.
- Suggest product pairings or promotions.
- Summarize user behavior in natural language.

---

## 🧰 Tools & Tech Stack

| Category         | Tools                                    |
|------------------|-------------------------------------------|
| Language Model   | Mistral via `mistralai` API            |
| Analytics        | Python, pandas, numpy, matplotlib, seaborn |
| ML / Clustering  | scikit-learn (KMeans)                     |
| AI Agent         | custom Mistral integration                |
| UI / App         | Streamlit + Plotly                        |

---

## 📊 Example Visuals

- Interactive conversion funnel chart
- Segment distribution bar charts
- Cluster plots and heatmaps
- AI-generated text responses

---

## 🌐 Live Demos

You can test the project in Streamlit here:

🔗 **App Version 1 (English version):**  
[streamlit-link-English](https://92ojbikbpkzxyjzjcymybp.streamlit.app/)

🔗 **App Version 2 (Ukrainian version):**  
[[streamlit-link-Ukrainian]](https://streamlit-demo-link2.com](https://vsfn4vshmfdnzcc27mvtzb.streamlit.app)

---

## 🛠️ How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/orangegreen212/AI-Marketing-Agent-.git

    Install dependencies:

pip install -r requirements.txt

    Run the app:

streamlit run app/app_english.py   ```

## 💬 Sample AI Prompts

You can ask the AI agent questions like:

    "Create a campaign idea for VIP users."

    "What do churned users usually do before leaving?"

    "Suggest a cross-sell product for someone who purchased a serum."

    "How can I re-engage occasional buyers?"

## 📈 Project Outcomes

    Built an end-to-end analytics workflow: from raw event logs to business insights.

    Implemented two customer segmentation strategies for flexible targeting.

    Developed a conversational AI agent to support campaign ideation.

    Delivered a full Streamlit interface suitable for both analysts and marketers.

##📌 Future Improvements

    Fine-tune Mistral or test with GPT-4 for richer outputs.

    Enable real-time data upload (CSV/Google Sheets integration).

    Add ability to save campaign drafts.

    Expand funnel tracking with attribution modeling.

##👩‍💻 Author

Olha (orangegreen212)
Junior Data Analyst | Passionate about AI & Marketing Analytics
📍 Ukraine
