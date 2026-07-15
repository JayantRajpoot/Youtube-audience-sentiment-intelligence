from detoxify import Detoxify

toxicity_model = Detoxify("unbiased")


def analyze_toxicity(text):
    scores = toxicity_model.predict(text)

    toxicity_score = float(scores["toxicity"])

    return {
        "toxicity_score": toxicity_score,
        "is_toxic": toxicity_score >= 0.8
    }


if __name__ == "__main__":
    print(analyze_toxicity("You are terrible and nobody likes you."))