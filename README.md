# 🔍 VeriNews AI — Explainable Fake News Detection and Verification System


<div align="center">

![VeriNews AI](https://img.shields.io/badge/VeriNews-AI%20Powered-blue?style=for-the-badge&logo=artificial-intelligence)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.0-black?style=for-the-badge&logo=flask)
![BERT](https://img.shields.io/badge/BERT-Transformer-orange?style=for-the-badge&logo=huggingface)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An AI-powered web application to detect fake news using Machine Learning and Deep Learning**

[🌐 Live Demo](https://barshasingh-verinews-ai.hf.space) • [📊 Features](#-features) • [🚀 Getting Started](#-getting-started) • [📖 Documentation](#-system-architecture)

</div>

---

## 📌 Overview

**VeriNews AI** is an intelligent fake news detection system that analyzes news articles through text or URLs and provides real-time predictions with confidence scores, visual insights, and explainable AI reasoning.

The system integrates **three AI models** — Logistic Regression, Naive Bayes, and BERT — to ensure accuracy, reliability, and transparency.

---

## 🌐 Live Demo

👉 **[https://barshasingh-verinews-ai.hf.space](https://barshasingh-verinews-ai.hf.space)**

> Deployed on **Hugging Face Spaces** with Docker

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **News Analysis** | Analyze news via text input or URL |
| 🌐 **Multi-Language** | Supports Hindi and English inputs |
| 🤖 **Multi-Model AI** | Logistic Regression, Naive Bayes, BERT |
| 📊 **Confidence Score** | Percentage-based prediction confidence |
| 🧠 **Explainable AI** | Reasoning and keyword highlighting |
| 📈 **Visualizations** | Interactive graphs and model comparisons |
| 🔐 **Authentication** | Secure login and registration system |
| 🕘 **History Tracking** | Personalized analysis history |
| 📊 **Analytics Dashboard** | Real vs Fake distribution charts |
| 🌍 **Source Verification** | Trusted / Suspicious / Unknown classification |

---

## 🧠 Model Performance

| Model | Accuracy | Type |
|---|---|---|
| 🥇 BERT | **94%** | Deep Learning |
| 🥈 Logistic Regression | **91%** | Machine Learning |
| 🥉 Naive Bayes | **87%** | Machine Learning |

---

## 🏗️ System Architecture

```
User Input (Text / URL)
        ↓
Content Extraction (BeautifulSoup)
        ↓
Language Detection & Translation
        ↓
Text Preprocessing & Cleaning
        ↓
Multi-Model Prediction
  ├── Logistic Regression
  ├── Naive Bayes
  └── BERT (Transformer)
        ↓
Explainable AI + Keyword Extraction
        ↓
Graph Visualization Generation
        ↓
Database Storage (PostgreSQL)
        ↓
Result Display + Analytics
```

---

## 🛠️ Tech Stack

### Frontend
- HTML + Tailwind CSS
- Jinja2 Templates

### Backend
- Python (Flask 3.1.0)
- Flask-Login (Authentication)
- SQLAlchemy + PostgreSQL (Database)

### Machine Learning & AI
- Logistic Regression (scikit-learn)
- Naive Bayes (scikit-learn)
- BERT (HuggingFace Transformers + PyTorch)

### Libraries
```
transformers    — BERT model
torch           — Deep learning framework
scikit-learn    — ML models
pandas/numpy    — Data processing
BeautifulSoup   — Web scraping
deep-translator — Language translation
nltk            — Text preprocessing
shap            — Explainable AI
gunicorn        — Production server
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/barsharajput/verinews-ai.git
cd verinews-ai

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -m nltk.downloader stopwords punkt wordnet

# Set up database
python create_db.py

# Run the application
python app.py
```

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
```

### Access the App
Open your browser and go to:
```
http://localhost:5000
```

---

## 🗄️ Database Structure

### User Table
| Field | Type | Description |
|---|---|---|
| id | Integer (PK) | Unique identifier |
| first_name | String | First name |
| last_name | String | Last name |
| username | String (Unique) | Login username |
| email | String (Unique) | Email address |
| phone | String | Phone number |
| country | String | Country |
| password | String (Hashed) | Bcrypt hashed password |

### History Table
| Field | Type | Description |
|---|---|---|
| id | Integer (PK) | Unique identifier |
| text | Text | News content analyzed |
| result | String | REAL or FAKE |
| confidence | Float | Confidence score (%) |
| user_id | Integer (FK) | References User table |

---

## 📁 Project Structure

```
verinews-ai/
│
├── app.py                  # Main Flask application
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── create_db.py            # Database initialization
│
├── src/
│   ├── predict.py          # Prediction logic
│   ├── preprocess.py       # Text preprocessing
│   ├── bert_model.py       # BERT model integration
│   ├── shap_explainer.py   # Explainable AI
│   ├── compare_models.py   # Model comparison
│   └── train.py            # Model training
│
├── model/
│   ├── tfidf.pkl           # TF-IDF vectorizer
│   ├── classifier.pkl      # Logistic Regression model
│   └── naive_bayes.pkl     # Naive Bayes model
│
├── templates/              # HTML templates
│   ├── index.html
│   ├── analyze.html
│   ├── dashboard.html
│   ├── login.html
│   └── ...
│
└── static/                 # CSS, JS, Images
```

---

## 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t verinews-ai .

# Run container
docker run -p 7860:7860 verinews-ai
```

---

## ☁️ Deployment

This project is deployed on **Hugging Face Spaces** using Docker.

👉 **Live at: [https://barshasingh-verinews-ai.hf.space](https://barshasingh-verinews-ai.hf.space)**

---

## ⚠️ Challenges & Solutions

| Challenge | Solution |
|---|---|
| BERT 512-token limit | Intelligent text truncation |
| Multi-language input | deep-translator library |
| Large model files | Hugging Face model hosting |
| Database persistence | PostgreSQL via Neon |
| Scikit-learn version mismatch | Version-safe prediction fallback |

---

## 🔮 Future Enhancements

- [ ] Fake news category classification
- [ ] Real-time news API integration
- [ ] Advanced graph dashboards
- [ ] Voice-based input support
- [ ] Mobile application (Android/iOS)

---

## 👩‍💻 Developer

**Barsha Singh**

[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-barshasingh-yellow?style=flat-square&logo=huggingface)](https://huggingface.co/barshasingh)
[![GitHub](https://img.shields.io/badge/GitHub-barsharajput-black?style=flat-square&logo=github)](https://github.com/barsharajput)

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

**⭐ If you found this project helpful, please give it a star!**

Made with ❤️ by Barsha Singh

</div>
