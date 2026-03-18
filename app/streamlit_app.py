import streamlit as st
from collections import Counter

st.set_page_config(page_title="AI Customer Feedback Intelligence", layout="wide")

st.title("AI Customer Feedback Intelligence")
st.write("A lightweight, deployment-safe customer feedback demo.")

default_feedback = [
    "Customer support was very rude and unhelpful",
    "The product quality is poor and not worth the money",
    "This is the worst service I have used",
    "Amazing experience and very smooth service",
    "Delivery was late and the package was damaged",
    "The app keeps crashing after the latest update",
    "Refund process took too long",
    "Everything worked perfectly and I am happy",
]


def classify_category(text: str) -> str:
    text = text.lower()

    if "refund" in text or "payment" in text or "money" in text:
        return "billing"
    elif "delivery" in text or "package" in text or "late" in text:
        return "delivery"
    elif "app" in text or "login" in text or "crash" in text or "issue" in text:
        return "app_issue"
    elif "support" in text or "service" in text:
        return "customer_support"
    else:
        return "other"


def simple_sentiment(text: str) -> str:
    text = text.lower()

    negative_words = [
        "bad",
        "worst",
        "poor",
        "late",
        "damaged",
        "rude",
        "crashing",
        "crash",
        "unhelpful",
        "issue",
        "problem",
        "refund",
        "unhappy",
        "angry",
        "terrible",
        "slow",
        "broken",
        "frustrated",
        "frustrating",
        "delay",
        "delayed",
        "failed",
        "failure",
        "error",
    ]

    positive_words = [
        "amazing",
        "great",
        "smooth",
        "happy",
        "excellent",
        "perfectly",
        "good",
        "love",
        "fast",
        "satisfied",
        "awesome",
        "nice",
        "easy",
    ]

    neg_count = sum(word in text for word in negative_words)
    pos_count = sum(word in text for word in positive_words)

    if neg_count > pos_count:
        return "negative"
    elif pos_count > neg_count:
        return "positive"
    else:
        return "neutral"


def generate_mock_insight(question: str, feedback_items: list[str]) -> str:
    categories = [classify_category(x) for x in feedback_items]
    counts = Counter(categories)
    top_categories = [k for k, _ in counts.most_common(3)]
    categories_text = ", ".join(top_categories) if top_categories else "general service quality"

    return f"""
Insight Summary

Question:
{question}

Key Findings:
- The most common complaint themes are related to {categories_text}.
- Negative feedback suggests recurring friction in customer experience.
- Users are highlighting service quality, delays, and support responsiveness as major concerns.

Suggested Actions:
- Improve response time for support requests.
- Investigate the top recurring complaint categories.
- Prioritize fixes for high-frequency customer pain points.

Note:
This is a lightweight mock insight generator for deployment-safe demo purposes.
"""


sentiments = [simple_sentiment(x) for x in default_feedback]
categories = [classify_category(x) for x in default_feedback]

tab1, tab2, tab3 = st.tabs(["Dashboard", "Feedback Analysis", "Ask Questions"])

with tab1:
    st.subheader("Sentiment Distribution")
    sentiment_counts = Counter(sentiments)
    st.bar_chart(sentiment_counts)

    st.subheader("Category Distribution")
    category_counts = Counter(categories)
    st.bar_chart(category_counts)

    st.subheader("Feedback Preview")
    for i, text in enumerate(default_feedback, start=1):
        st.write(f"{i}. {text}")

with tab2:
    st.subheader("Feedback Analysis")
    user_text = st.text_area("Enter customer feedback")

    if st.button("Analyze Feedback"):
        if user_text.strip():
            sentiment = simple_sentiment(user_text)
            category = classify_category(user_text)

            st.success(f"Sentiment: {sentiment}")
            st.info(f"Category: {category}")
        else:
            st.warning("Please enter some feedback text.")

with tab3:
    st.subheader("Ask Questions About Feedback")
    question = st.text_input("Ask something like: Why are customers unhappy?")

    if st.button("Get Insights"):
        if question.strip():
            st.write("Relevant Feedback")
            for item in default_feedback[:3]:
                st.write(f"- {item}")

            insight = generate_mock_insight(question, default_feedback)
            st.success(insight)
        else:
            st.warning("Please enter a question.")