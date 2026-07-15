from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)


def analyze_emotion(text):
    result = emotion_classifier(text)[0]

    return {
        "emotion": result["label"],
        "emotion_score": result["score"]
    }