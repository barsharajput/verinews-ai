from pathlib import Path

import joblib

from src.bert_model import predict_bert
from src.preprocess import clean_text
from src.shap_explainer import get_shap_values

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"

# Load vectorizer
tfidf = joblib.load(MODEL_DIR / "tfidf.pkl")

# Load ML models
MODELS = {
    "logistic": joblib.load(MODEL_DIR / "classifier.pkl"),
    "naive_bayes": joblib.load(MODEL_DIR / "naive_bayes.pkl"),
}

# Sensational words
SENSATIONAL_WORDS = [
    "breaking",
    "shocking",
    "exposed",
    "secret",
    "conspiracy",
    "viral",
    "scam",
]


def sensational_score(text):
    return sum(1 for w in SENSATIONAL_WORDS if w in text.lower())


def explain_prediction(text, model, top_n=6):
    if not hasattr(model, "coef_"):
        return [("Explainability", "Not available for Naive Bayes")]

    vec = tfidf.transform([clean_text(text)])
    feature_names = tfidf.get_feature_names_out()
    weights = model.coef_[0]

    word_scores = {feature_names[i]: weights[i] for i in vec.nonzero()[1]}

    return sorted(word_scores.items(), key=lambda x: abs(x[1]), reverse=True)[:top_n]


def generate_explanation(text):
    suspicious_words = [
        "shocking",
        "breaking",
        "viral",
        "exclusive",
        "unbelievable",
        "alert",
        "must read",
    ]

    found_words = []

    text_lower = text.lower()

    for word in suspicious_words:
        if word in text_lower:
            found_words.append(word)

    if found_words:
        explanation = "⚠️ Uses sensational words: " + ", ".join(found_words)
    else:
        explanation = "✅ Language appears neutral and less biased"

    return explanation, found_words


def predict_news(text, model_choice="logistic"):

    # 🔥 Generate explanation (for both paths)
    reason, keywords = generate_explanation(text)

    # ======================
    # 🤖 BERT MODEL
    # ======================
    if model_choice == "bert":
        try:
            # 🔥 Safety: trim text
            text = text[:512]

            bert_result = predict_bert(text)

            score = bert_result.get("confidence", 0) / 100

            if bert_result.get("label") == "POSITIVE":
                label = "REAL NEWS"
                real_prob = score
                fake_prob = 1 - score
            else:
                label = "FAKE NEWS"
                fake_prob = score
                real_prob = 1 - score

            return {
                "label": label,
                "confidence": bert_result.get("confidence", 0),
                "fake_probability": round(fake_prob, 3),
                "real_probability": round(real_prob, 3),
                "sensational_score": sensational_score(text),
                "model_used": "bert",
                "explanation": [("BERT Model", "Context-based prediction")],
                "recommendation": "Prediction based on advanced AI model (BERT).",
                # ✅ explainable AI
                "reason": reason,
                "keywords": keywords,
            }

        except Exception as e:
            print("🔥 BERT ERROR:", e)

            # ✅ graceful fallback (VERY IMPORTANT)
            return {
                "label": "Error",
                "confidence": 0,
                "fake_probability": 0,
                "real_probability": 0,
                "sensational_score": 0,
                "model_used": "bert",
                "explanation": [("BERT Model", "Failed to load")],
                "recommendation": "BERT model failed to run.",
                "reason": "Model error",
                "keywords": [],
            }
    # ======================
    # 🧠 ML MODELS
    # ======================
    model = MODELS.get(model_choice, MODELS["logistic"])

    vec = tfidf.transform([clean_text(text)])
    fake_prob, real_prob = model.predict_proba(vec)[0]

    confidence = round(max(fake_prob, real_prob) * 100, 2)
    sensational = sensational_score(text)

    try:
        shap_values = get_shap_values(model, tfidf, text)
        shap_result = str(shap_values.values[0][:10])
    except Exception:
        shap_result = "SHAP not available for this input"

    if confidence >= 75:
        label = "REAL NEWS" if real_prob > fake_prob else "FAKE NEWS"
        recommendation = "Prediction is reliable."
    else:
        label = "UNCERTAIN – NEEDS FACT CHECKING"
        recommendation = "Manual verification recommended."

    return {
        "label": label,
        "confidence": confidence,
        "fake_probability": round(fake_prob, 3),
        "real_probability": round(real_prob, 3),
        "sensational_score": sensational,
        "model_used": model_choice,
        "explanation": explain_prediction(text, model),
        "recommendation": recommendation,
        "shap": shap_result,
        # 🔥 NEW (Explain WHY)
        "reason": reason,
        "keywords": keywords,
    }
