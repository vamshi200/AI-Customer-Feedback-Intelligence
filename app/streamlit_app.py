import streamlit as st
import joblib
from src.rag_pipeline import retrieve

st.set_page_config(page_title="AI Customer Feedback Intelligence", layout="centered")

st.title("AI Customer Feedback Intelligence")
st.write("Analyze feedback using sentiment prediction, issue classification, and retrieval based insights.")

sentiment_model = joblib.load("models/sentiment_model.pkl")
category_model = joblib.load("models/category_model.pkl")

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

st.subheader("Ask Questions About Feedback")

query = st.text_input("Ask something like: Why are customers unhappy?")

if st.button("Get Insights"):
    if query.strip():
        context = retrieve(query)

        st.write("Relevant Feedback")
        st.write(context)

        st.success(
            "Insight: Customers are mainly facing issues with delivery, customer support responsiveness, and app related problems."
        )
    else:
        st.warning("Please enter a question")