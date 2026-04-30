def compare_models(text):
    results = {}

    models = ["logistic", "naive_bayes", "bert"]

    for model in models:
        try:
            # 🔥 important fix for bert
            input_text = text[:512] if model == "bert" else text

            res = predict_news(input_text, model)

            results[model] = {
                "label": res.get("label", "Error"),
                "confidence": res.get("confidence", 0),
            }

        except Exception as e:
            print(f"{model} error:", e)

            results[model] = {
                "label": "Error",
                "confidence": 0,
            }

    return results
