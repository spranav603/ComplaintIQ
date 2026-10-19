"""
ComplaintIQ — High-Efficiency ML Classifier Training Script
Trains a TF-IDF + LogisticRegression pipeline with probability confidence estimation.
Saves model to model/complaint_model.pkl and categories to model/categories.pkl
"""

import pandas as pd
import numpy as np
import pickle
import os
import re
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

STOP_WORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "he", "him", "his", "she", "her", "it", "its", "they", "them", "their", "what", "which",
    "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
    "with", "about", "against", "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all",
    "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don",
    "should", "now"
}

def preprocess(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]
    return " ".join(tokens)

dataset_path = "complaints_dataset.csv"
if not os.path.exists(dataset_path):
    dataset_path = "complaint_text,category.txt"

print(f"Loading dataset from: {dataset_path}")
df = pd.read_csv(dataset_path)
df.dropna(subset=["complaint_text", "category"], inplace=True)
df["cleaned"] = df["complaint_text"].apply(preprocess)

print(f"Total samples: {len(df)} across {df['category'].nunique()} categories.")

X = df["cleaned"]
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=8000, sublinear_tf=True)),
    ("clf",   LogisticRegression(C=2.5, solver="lbfgs", max_iter=2000, random_state=42))
])

print("Training high-efficiency Logistic Regression model...")
pipeline.fit(X_train, y_train)

preds = pipeline.predict(X_test)
acc = accuracy_score(y_test, preds)
cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")

print("=" * 60)
print(f"Hold-out Test Accuracy: {acc:.2%}")
print(f"5-Fold CV Accuracy:    {cv_scores.mean():.2%} +/- {cv_scores.std():.2%}")
print("=" * 60)
print(classification_report(y_test, preds))

os.makedirs("model", exist_ok=True)
with open("model/complaint_model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

categories = sorted(y.unique().tolist())
with open("model/categories.pkl", "wb") as f:
    pickle.dump(categories, f)

print("Saved model -> model/complaint_model.pkl")
print("Saved categories -> model/categories.pkl")

# Test probability output
sample_test = "Payment processor deducted money twice from my card for order invoice #992"
probs = pipeline.predict_proba([preprocess(sample_test)])[0]
best_idx = probs.argmax()
pred_cat = pipeline.classes_[best_idx]
conf = probs[best_idx] * 100

print(f"\nSample Prediction Test:\n  Text: '{sample_test}'")
print(f"  Predicted Category: {pred_cat} ({conf:.1f}% Confidence)")