import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("data/raw/customer_feedback.csv")


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


df["category"] = df["text"].apply(get_category)

X = df["text"]
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000)),
    ("clf", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

joblib.dump(model, "models/category_model.pkl")
print("Category model saved")