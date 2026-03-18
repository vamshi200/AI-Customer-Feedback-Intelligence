import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Customer Feedback Intelligence", layout="wide")

st.title("AI Customer Feedback Intelligence")
st.write("A simple, deployable dashboard for customer feedback analysis.")

# Sample fallback data
default_data = pd.DataFrame(
    {
        "text": [
            "Customer support was very rude and unhelpful",
            "The product quality is poor and not worth the money",
            "This is the worst service I have used",
            "Amazing experience and very smooth service",
            "Delivery was late and the package was damaged",
            "The app keeps crashing after the latest update",
            "Refund process took too long",
            "Everything worked perfectly and I am happy",
        ],
        "sentiment": [
            "negative",
            "negative",
            "negative",
            "positive",
            "negative",
            "negative",
            "negative",
            "positive",
        ],
    }
)


def classify_category(text: str) -> str:
    text = str(text).lower()
    if "refund" in text or "payment" in text or "money" in text:
        return "billing"
    if "delivery" in text or "package" in text or "late" in text:
        return "delivery"
    if "app" in text or "login" in text or "crash" in text:
        return "app_issue"
    if "support" in text or "service" in text:
        return "customer_support"
    return "other"


def simple_sentiment(text: str) -> str:
    text = str(text).lower()
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
    ]

    neg_count = sum(word in text for word in negative_words)
    pos_count = sum(word in text for word in positive_words)

    if neg_count > pos_count:
        return "negative"
    if pos_count > neg_count:
        return "positive"
    return "neutral"


def generate_mock_insight(question: str, df: pd.DataFrame) -> str:
    negative_df = df[df["predicted_sentiment"] == "negative"]
    top_categories = (
        negative_df["category"].value_counts().head(3).index.tolist()
        if not negative_df.empty
        else []
    )

    if not top_categories:
        top_categories = df["category"].value_counts().head(3).index.tolist()

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


st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if "text" not in df.columns:
        st.error("Uploaded CSV must contain a 'text' column.")
        st.stop()
    if "sentiment" not in df.columns:
        df["sentiment"] = df["text"].apply(simple_sentiment)
else:
    df = default_data.copy()

df["predicted_sentiment"] = df["text"].apply(simple_sentiment)
df["category"] = df["text"].apply(classify_category)

tab1, tab2, tab3 = st.tabs(["Dashboard", "Feedback Analysis", "Ask Questions"])

with tab1:
    st.subheader("Sentiment Distribution")
    sentiment_counts = df["predicted_sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]
    fig1 = px.bar(sentiment_counts, x="sentiment", y="count", title="Sentiment Distribution")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Category Distribution")
    category_counts = df["category"].value_counts().reset_index()
    category_counts.columns = ["category", "count"]
    fig2 = px.bar(category_counts, x="category", y="count", title="Category Distribution")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Feedback Preview")
    st.dataframe(df, use_container_width=True)

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
            st.write("\n\n".join(df["text"].head(3).tolist()))

            insight = generate_mock_insight(question, df)
            st.success(insight)
        else:
            st.warning("Please enter a question.")