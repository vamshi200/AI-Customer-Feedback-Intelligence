import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

from src.rag_pipeline import retrieve
from src.llm_service import generate_insight

st.set_page_config(page_title="AI Customer Feedback Intelligence", layout="wide")

st.title("AI Customer Feedback Intelligence")
st.write("Analyze customer feedback using sentiment prediction, issue classification, retrieval, and LLM-based insights.")

df = pd.read_csv("data/raw/customer_feedback.csv")

sentiment_model = joblib.load("models/sentiment_model.pkl")
category_model = joblib.load("models/category_model.pkl")


def get_category(text):
    text = text.lower()
    if "refund" in text or "payment" in text:
        return "billing"
    elif "delivery" in text or "order" in text:
        return "delivery"
    elif "app" in text or "login" in text:
        return "app_issue"
    elif "support" in text or "service" in text:
        return "customer_support"
    else:
        return "other"


df["predicted_sentiment"] = sentiment_model.predict(df["text"])
df["predicted_category"] = df["text"].apply(get_category)

tab1, tab2, tab3 = st.tabs(["Dashboard", "Feedback Analysis", "Ask Questions"])

with tab1:
    st.subheader("Sentiment Distribution")
    sentiment_counts = df["predicted_sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]
    fig1 = px.bar(sentiment_counts, x="sentiment", y="count", title="Sentiment Distribution")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Category Distribution")
    category_counts = df["predicted_category"].value_counts().reset_index()
    category_counts.columns = ["category", "count"]
    fig2 = px.bar(category_counts, x="category", y="count", title="Category Distribution")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Feedback Data Preview")
    st.dataframe(df)

with tab2:
    st.subheader("Feedback Classification")

    text = st.text_area("Enter customer feedback")

    if st.button("Analyze Feedback"):
        if text.strip():
            sentiment = sentiment_model.predict([text])[0]
            category = category_model.predict([text])[0]

            st.success(f"Sentiment: {sentiment}")
            st.info(f"Category: {category}")
        else:
            st.warning("Please enter some text")

with tab3:
    st.subheader("Ask Questions About Feedback")

    query = st.text_input("Ask something like: Why are customers unhappy?")

    if st.button("Get Insights"):
        if query.strip():
            context = retrieve(query)

            st.write("Relevant Feedback")
            st.write(context)

            answer = generate_insight(query, context)
            st.success(answer)
        else:
            st.warning("Please enter a question")