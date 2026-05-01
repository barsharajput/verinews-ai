import hashlib
import os
import sys

import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

from urllib.parse import urlparse

from database.db import db
from deep_translator import GoogleTranslator
from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from models.user_model import History, User
from src.predict import generate_explanation, predict_news
from werkzeug.security import check_password_hash, generate_password_hash


def compare_models(text):
    results = {}

    models = ["logistic", "naive_bayes", "bert"]

    for model in models:
        try:
            res = predict_news(text, model)
            results[model] = {
                "label": res["label"],
                "confidence": res["confidence"],
            }
        except Exception as e:
            print(f"{model} error:", e)
            results[model] = {
                "label": "Error",
                "confidence": 0,
            }

    return results


def check_source(url):
    trusted_sources = ["bbc.com", "reuters.com", "thehindu.com", "ndtv.com", "cnn.com"]

    suspicious_sources = ["clickbait.com", "fakenews.com", "viralnews.com"]

    try:
        domain = urlparse(url).netloc.lower()

        # remove www
        domain = domain.replace("www.", "")

        if any(src in domain for src in trusted_sources):
            return domain, "trusted"
        elif any(src in domain for src in suspicious_sources):
            return domain, "suspicious"
        else:
            return domain, "unknown"

    except:
        return "unknown", "unknown"


app = Flask(__name__)

# ==============================
# ✅ CONFIG
# ==============================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
app.config["SECRET_KEY"] = "secret123"

db.init_app(app)

# ==============================
# ✅ LOGIN MANAGER
# ==============================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # redirect if not logged in


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def extract_news_from_url(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        paragraphs = soup.find_all("p")
        text = " ".join([p.text for p in paragraphs])

        return text.strip()
    except:
        return None


# ==============================
# 🌐 LANDING PAGE (PUBLIC)
# ==============================
@app.route("/")
def landing():
    return render_template("landing.html")


# ==============================
# 🔐 MAIN APP (Protected)
# ==============================


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    result = None
    user_history = History.query.filter_by(user_id=current_user.id).all()

    total = len(user_history)
    real = len([h for h in user_history if "REAL" in h.result])
    fake = len([h for h in user_history if "FAKE" in h.result])

    accuracy = round((real / total) * 100, 2) if total > 0 else 0

    recent = user_history[::-1][:5]

    model_perf = {"bert": 94, "logistic": 91, "naive": 87}

    return render_template(
        "dashboard.html",
        total=total,
        real=real,
        fake=fake,
        accuracy=accuracy,
        recent=recent,
        model_perf=model_perf,
        page="dashboard",
    )


# ==============================
# 📝 REGISTER
# ==============================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already exists")

        if User.query.filter_by(email=email).first():
            return render_template("register.html", error="Email already registered")

        user = User(
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            username=username,
            email=email,
            phone=request.form.get("phone"),
            country=request.form.get("country"),
            password=generate_password_hash(request.form.get("password")),
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# ==============================
# 🔑 LOGIN
# ==============================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ==============================
# 🚪 LOGOUT
# ==============================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing"))  # back to landing


# ==============================
# 🔍 ANALYZE PAGE
# ==============================
@app.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    result = None

    if request.method == "POST":
        news_text = request.form.get("news")
        url = request.form.get("url")
        model_choice = request.form.get("model")

        # 🌐 URL → extract text
        if url and url.strip():
            try:
                import requests
                from bs4 import BeautifulSoup

                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=10)

                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.find_all("p")

                news_text = " ".join([p.get_text() for p in paragraphs]).strip()

            except Exception as e:
                print("ERROR:", e)

        # ❌ empty input
        if not news_text or news_text.strip() == "":
            return render_template("analyze.html", error="⚠️ Enter URL or news text")

        # 🔥 BERT FIX
        if model_choice == "bert":
            news_text = news_text[:512]

        # ✅ prediction
        result = predict_news(news_text, model_choice)

        explanation, keywords = generate_explanation(news_text)

        result["news_text"] = news_text
        result["keywords"] = keywords
        result["reason"] = explanation

        # optional (if you already have)
        try:
            result["comparison"] = compare_models(news_text)
        except:
            result["comparison"] = None

        result["language"] = "en"  # or detect if you want
        result["domain"] = None
        result["source_status"] = None

        clean_text = news_text.strip()
        text_hash = hashlib.md5(clean_text.encode()).hexdigest()

        existing = History.query.filter_by(
            user_id=current_user.id, text=news_text[:200]
        ).first()

        if not existing:
            history_item = History(
                text=news_text[:300],
                result=result["label"],
                confidence=result["confidence"],
                user_id=current_user.id,
            )
            db.session.add(history_item)
            db.session.commit()
    return render_template("analyze.html", result=result)


# ==============================
# 📊 DASHBOARD
# ==============================
@app.route("/history")
@login_required
def history():
    user_history = History.query.filter_by(user_id=current_user.id).all()

    return render_template("history.html", history=user_history)


# -----------------------------
# MODELS PAGE
# -----------------------------
@app.route("/models")
@login_required
def models():

    model_data = {
        "logistic": {
            "accuracy": 91,
            "precision": 89,
            "recall": 88,
            "f1": 88,
            "status": "Good baseline model",
        },
        "naive_bayes": {
            "accuracy": 87,
            "precision": 85,
            "recall": 84,
            "f1": 84,
            "status": "Fast & efficient",
        },
        "bert": {
            "accuracy": 94,
            "precision": 93,
            "recall": 92,
            "f1": 92,
            "status": "Best performance",
        },
    }

    # 🔥 Find best model dynamically
    best_model = max(model_data.items(), key=lambda x: x[1]["accuracy"])

    return render_template("models.html", model_data=model_data, best_model=best_model)


@app.route("/reports")
@login_required
def reports():

    # 🔥 get user history
    history = (
        History.query.filter_by(user_id=current_user.id)
        .order_by(History.id.desc())
        .all()
    )

    # 📊 calculate stats
    total = len(history)
    real = sum(1 for h in history if "REAL" in h.result)
    fake = sum(1 for h in history if "FAKE" in h.result)

    accuracy = round((real / total) * 100, 2) if total > 0 else 0

    stats = {"total": total, "real": real, "fake": fake, "accuracy": accuracy}

    return render_template(
        "reports.html",
        stats=stats,
        reports=history,
    )


# ==============================
# 🗑 DELETE HISTORY
# ==============================
@app.route("/delete/<int:id>")
@login_required
def delete_history(id):
    item = History.query.get(id)

    if item and item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for("history"))


# ==============================
# 🧹 CLEAR HISTORY
# ==============================
@app.route("/clear")
@login_required
def clear_history():
    History.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return redirect(url_for("history"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=False)
