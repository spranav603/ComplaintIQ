# ComplaintIQ — AI-Powered Smart Help Desk & Ticket Triage

ComplaintIQ is an intelligent customer support help desk and ticket triage platform. It automatically processes inbound customer complaints, classifies problem categories using machine learning, assigns priority and SLA targets, routes tickets to the appropriate support teams, and generates contextual AI responses.

---

## 🌟 Key Features

- **Customer Portal**: Submit complaints, specify product/service, select preferred response language, and receive instant AI assistance.
- **Dual-Engine AI Triage**: Combines TF-IDF + Machine Learning classification with rule-based heuristics for accurate category and priority scoring.
- **SLA & Breach Tracking**: Automatically sets resolution deadlines, monitors breach risks, and tracks customer satisfaction (CSAT).
- **Agent Dashboard**: Manage incoming tickets, override categories, update statuses, export CSVs, and inspect defect trends.
- **Product Health Scoreboard**: Identifies trending defect keywords (e.g., `#screen-flicker`, `#delivery-delay`).
- **Reports & Exporting**: Generate automated PDF and DOCX analytics reports.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLite
- **Machine Learning**: Scikit-Learn (TF-IDF + Logistic Regression / SVM)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (Responsive Dashboard & Portals)
- **Reporting**: ReportLab (PDF), Python-Docx (Word Documents), Matplotlib (Visualizations)

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/spranav603/ComplaintIQ.git
cd ComplaintIQ
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the ML Model (Optional)
The backend auto-checks and trains if needed, but you can train manually:
```bash
python train.py
```

### 5. Run the Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000/login.html`.

---

## 📂 Project Structure

```text
├── app.py                   # Main Flask backend application & API endpoints
├── train.py                 # ML model training script
├── eval_model.py            # Model evaluation script
├── plot_metrics.py          # Metrics visualization script
├── generate_pdf.py          # PDF report generator
├── generate_report_docx.py  # DOCX documentation and report generator
├── login.html               # Authentication & login interface
├── customer.html            # Customer submission portal
├── agent.html               # Support agent & admin dashboard
├── complaints_dataset.csv   # Training dataset
├── model/                   # Serialized ML models and category mappings
├── PROJECT_GUIDE.md         # Detailed architectural documentation
└── requirements.txt         # Project dependencies
```

---

## 📄 License
MIT License
