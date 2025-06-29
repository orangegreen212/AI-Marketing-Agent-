{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMNpEvD0OPTd5Ljha8qnx4z",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/orangegreen212/AI-Marketing-Agent-/blob/main/app_py_py.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 385
        },
        "id": "CWXScnYV_4qY",
        "outputId": "7dd2c6ab-9897-4d6e-b74b-bdf269bdefd9"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'streamlit'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipython-input-1-2132262292.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;31m# app.py\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 3\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mpandas\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mpd\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mnumpy\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mnp\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ],
      "source": [
        "# app.py\n",
        "\n",
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import plotly.express as px\n",
        "\n",
        "# === HEADER ===\n",
        "st.title(\"📉 Customer Retention & Churn Dashboard\")\n",
        "\n",
        "# === Data Loading from Google Drive (if the file is shared publicly) ===\n",
        "csv_url = \"https://drive.google.com/file/d/1cCxHQriyEPCPcZ35gcuxpJRUSU7mKopI/view?usp=sharing\"\n",
        "@st.cache_data\n",
        "def load_data():\n",
        "    return pd.read_csv(csv_url)\n",
        "\n",
        "df = load_data()\n",
        "\n",
        "# === Overall Statistics ===\n",
        "st.subheader(\"📊 Overview\")\n",
        "col1, col2, col3 = st.columns(3)\n",
        "col1.metric(\"Total Users\", f\"{len(df):,}\")\n",
        "col2.metric(\"Average Activity Probability\", f\"{df['predicted_activity_proba'].mean():.2f}\")\n",
        "col3.metric(\"Churn Rate\", f\"{1 - df['predicted_activity_binary'].mean():.2%}\")\n",
        "\n",
        "# === Filters ===\n",
        "st.sidebar.header(\"🔍 Filters\")\n",
        "segment = st.sidebar.selectbox(\"Behavioral Segment\", [\"All\"] + df['Behavioral_Segment'].unique().tolist())\n",
        "customer_type = st.sidebar.selectbox(\"Customer Type\", [\"All\"] + df['customer_type'].unique().tolist())\n",
        "\n",
        "filtered_df = df.copy()\n",
        "if segment != \"All\":\n",
        "    filtered_df = filtered_df[filtered_df['Behavioral_Segment'] == segment]\n",
        "if customer_type != \"All\":\n",
        "    filtered_df = filtered_df[filtered_df['customer_type'] == customer_type]\n",
        "\n",
        "# === Churn vs Activity Chart ===\n",
        "st.subheader(\"📈 Activity Probability Distribution\")\n",
        "fig = px.histogram(filtered_df, x=\"predicted_activity_proba\", nbins=30,\n",
        "                   color=\"predicted_activity_binary\", barmode='overlay',\n",
        "                   labels={\"predicted_activity_binary\": \"Active\"})\n",
        "st.plotly_chart(fig, use_container_width=True)\n",
        "\n",
        "# === Users Table ===\n",
        "st.subheader(\"👥 Users\")\n",
        "st.dataframe(filtered_df[['customer_type', 'Behavioral_Segment', 'RFM_Segment',\n",
        "                          'predicted_activity_proba', 'predicted_activity_binary',\n",
        "                          'total_spend_sum_last_3M', 'Recency', 'Frequency', 'Monetary']].sort_values(\n",
        "                          by='predicted_activity_proba', ascending=False).head(20))\n",
        "\n",
        "# === User Details ===\n",
        "st.subheader(\"🔎 Detailed User Profile\")\n",
        "user_id = st.selectbox(\"Select user_id\", df['Unnamed: 0'].unique())\n",
        "user = df[df['Unnamed: 0'] == user_id].squeeze()\n",
        "\n",
        "st.markdown(f\"\"\"\n",
        "- **Customer Type**: {user['customer_type']}\n",
        "- **Segment**: {user['Behavioral_Segment']}\n",
        "- **RFM Segment**: {user['RFM_Segment']}\n",
        "- **Activity Probability**: `{user['predicted_activity_proba']:.2f}`\n",
        "- **Purchases in last 3 months**: `{user['num_purchases_sum_last_3M']}`\n",
        "- **Spend**: `${user['total_spend_sum_last_3M']:.2f}`\n",
        "\"\"\")"
      ]
    }
  ]
}
