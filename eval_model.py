"""
ComplaintIQ — Comprehensive ML Model Efficiency & Performance Evaluator
Measures inference speed, memory footprint, classification metrics, and confusion matrix.
"""

import os
import time
import pickle
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score

# Load model and dataset
model_path = "model/complaint_model.pkl"
dataset_path = "complaints_dataset.csv"

if not os.path.exists(model_path):
    print("Error: model/complaint_model.pkl not found.")
    exit(1)

model_size_kb = os.path.getsize(model_path) / 1024.0

with open(model_path, "rb") as f:
    pipeline = pickle.load(f)

df = pd.read_csv(dataset_path)
df.dropna(subset=["complaint_text", "category"], inplace=True)

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

import re
def preprocess(text: str) -> str:
    if not isinstance(text, str): return ""
    text = re.sub(r"[^a-z\s]", "", text.lower())
    tokens = text.split()
    return " ".join([t for t in tokens if t not in STOP_WORDS and len(t) > 2])

df["cleaned"] = df["complaint_text"].apply(preprocess)
X = df["cleaned"]
y = df["category"]

# 1. Inference Speed Benchmark
sample_text = "I was charged twice on my invoice #9821 and deducted $149 twice"
cleaned_sample = preprocess(sample_text)

# Warmup
pipeline.predict([cleaned_sample])

start_t = time.perf_counter()
n_runs = 1000
for _ in range(n_runs):
    _ = pipeline.predict_proba([cleaned_sample])
end_t = time.perf_counter()

avg_latency_ms = ((end_t - start_t) / n_runs) * 1000.0
throughput_qps = n_runs / (end_t - start_t)

# 2. Batch Inference Speed Benchmark
batch_samples = X.tolist()
start_batch_t = time.perf_counter()
batch_preds = pipeline.predict(batch_samples)
end_batch_t = time.perf_counter()
batch_latency_ms = (end_batch_t - start_batch_t) * 1000.0

# 3. Overall Accuracy & Cross-Validation Metrics
cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")

print("\n" + "=" * 65)
print(" COMPLAINTIQ ML MODEL EFFICIENCY BENCHMARK REPORT")
print("=" * 65)

print(f"\n1. MODEL MEMORY & DISK FOOTPRINT:")
print(f"   - Model Pickle Size:         {model_size_kb:.2f} KB (Ultra-Lightweight)")
print(f"   - Total Training Vocabulary: {len(pipeline.named_steps['tfidf'].vocabulary_)} TF-IDF n-gram features")

print(f"\n2. INFERENCE LATENCY & THROUGHPUT (CPU):")
print(f"   - Single Complaint Latency:  {avg_latency_ms:.3f} ms / request")
print(f"   - Prediction Throughput:     {throughput_qps:.1f} queries / second")
print(f"   - Batch ({len(batch_samples)} samples) Time:   {batch_latency_ms:.2f} ms")

print(f"\n3. CLASSIFICATION ACCURACY & CROSS-VALIDATION:")
print(f"   - 5-Fold CV Accuracy:       {cv_scores.mean():.2%} +/- {cv_scores.std():.2%}")
print(f"   - Minimum Fold Accuracy:     {cv_scores.min():.2%}")
print(f"   - Maximum Fold Accuracy:     {cv_scores.max():.2%}")

print(f"\n4. CONFUSION MATRIX ({len(df)} Samples):")
cats = sorted(y.unique().tolist())
cm = confusion_matrix(y, batch_preds, labels=cats)
cm_df = pd.DataFrame(cm, index=[f"Actual {c}" for c in cats], columns=[f"Pred {c}" for c in cats])
print(cm_df.to_string())

print(f"\n5. DETAILED CLASSIFICATION REPORT:")
print(classification_report(y, batch_preds))

print("=" * 65)
