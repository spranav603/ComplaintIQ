"""
ComplaintIQ — Generate Exact Scientific Evaluation Plots (Figure 6.1)
Computes real Confusion Matrix and Multiclass ROC Curves from the trained model and dataset.
"""

import os
import pickle
import re
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Headless backend for reliable rendering
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize

# 1. Load Dataset and Model
dataset_path = "complaints_dataset.csv"
model_path = "model/complaint_model.pkl"

if not os.path.exists(dataset_path) or not os.path.exists(model_path):
    print("Error: Missing dataset or model file.")
    exit(1)

with open(model_path, "rb") as f:
    pipeline = pickle.load(f)

df = pd.read_csv(dataset_path).dropna(subset=["complaint_text", "category"])

STOP_WORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "he", "him", "his", "she", "her", "it", "its", "they", "them", "their", "what", "which",
    "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
    "with", "about", "against", "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under"
}

def preprocess(text: str) -> str:
    if not isinstance(text, str): return ""
    text = re.sub(r"[^a-z\s]", "", text.lower())
    tokens = text.split()
    return " ".join([t for t in tokens if t not in STOP_WORDS and len(t) > 2])

df["cleaned"] = df["complaint_text"].apply(preprocess)
X = df["cleaned"]
y_true = df["category"]

# 2. Get Real Predictions and Class Probabilities
classes = sorted(y_true.unique().tolist())
y_pred = pipeline.predict(X)
y_proba = pipeline.predict_proba(X)

# Compute Confusion Matrix
cm = confusion_matrix(y_true, y_pred, labels=classes)

# Compute ROC Curves (One-vs-Rest)
y_bin = label_binarize(y_true, classes=classes)
n_classes = len(classes)

fpr = dict()
tpr = dict()
roc_auc = dict()

for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_bin[:, i], y_proba[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Micro-average ROC
fpr["micro"], tpr["micro"], _ = roc_curve(y_bin.ravel(), y_proba.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

# 3. Create High-Resolution Publication Plot
plt.style.use('default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
fig.patch.set_facecolor('white')

# --- SUBPLOT 1: Confusion Matrix Heatmap ---
im = ax1.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
cbar = ax1.figure.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=9)

ax1.set_title('(a) Confusion Matrix (Actual N = 150)', fontsize=13, fontweight='bold', pad=12, color='#0B132B')
tick_marks = np.arange(len(classes))
ax1.set_xticks(tick_marks)
ax1.set_yticks(tick_marks)
ax1.set_xticklabels(classes, rotation=25, ha='right', fontsize=9.5, fontweight='medium')
ax1.set_yticklabels(classes, fontsize=9.5, fontweight='medium')

thresh = cm.max() / 2.
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        val = cm[i, j]
        color = "white" if val > thresh else "#1A202C"
        ax1.text(j, i, format(val, 'd'),
                 ha="center", va="center",
                 color=color, fontsize=12, fontweight='bold')

ax1.set_ylabel('True Category', fontsize=11, fontweight='bold', labelpad=8, color='#0B132B')
ax1.set_xlabel('Predicted Category', fontsize=11, fontweight='bold', labelpad=8, color='#0B132B')
ax1.grid(False)

# --- SUBPLOT 2: Multiclass ROC Curves ---
colors = ['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728']

for i, color in zip(range(n_classes), colors):
    ax2.plot(fpr[i], tpr[i], color=color, lw=2.2,
             label=f'{classes[i]} (AUC = {roc_auc[i]:.2f})')

# Plot micro-average
ax2.plot(fpr["micro"], tpr["micro"],
         label=f'Micro-average (AUC = {roc_auc["micro"]:.2f})',
         color='#9467BD', linestyle=':', linewidth=2.5)

# Chance diagonal line
ax2.plot([0, 1], [0, 1], 'k--', lw=1.5, alpha=0.6, label='Random Chance (AUC = 0.50)')

ax2.set_xlim([-0.02, 1.0])
ax2.set_ylim([0.0, 1.03])
ax2.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=11, fontweight='bold', labelpad=8, color='#0B132B')
ax2.set_ylabel('True Positive Rate (Sensitivity)', fontsize=11, fontweight='bold', labelpad=8, color='#0B132B')
ax2.set_title('(b) Multiclass ROC Curves (One-vs-Rest)', fontsize=13, fontweight='bold', pad=12, color='#0B132B')
ax2.legend(loc="lower right", fontsize=9, frameon=True, framealpha=0.9, facecolor='#F8F9FA')
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout(pad=2.5)

output_png = "figure_6_1_evaluation_plots.png"
plt.savefig(output_png, dpi=300, bbox_inches='tight')
print(f"Successfully generated exact evaluation plot: {output_png}")

# Also print exact numerical values for documentation
print("\n=== EXACT COMPUTED METRICS ===")
for i, c in enumerate(classes):
    print(f"  - {c}: AUC = {roc_auc[i]:.4f}")
print(f"  - Micro-Average AUC: {roc_auc['micro']:.4f}")
print("\nConfusion Matrix:")
for i, c in enumerate(classes):
    print(f"  {c:18s}: {cm[i]}")
