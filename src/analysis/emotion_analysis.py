import streamlit as st
from transformers import pipeline


@st.cache_resource
def load_emotion_model():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base"
    )


emotion_classifier = load_emotion_model()


def analyze_emotion(text):
    result = emotion_classifier(
        text,
        truncation=True,
        max_length=512
    )[0]

    return {
        "emotion": result["label"],
        "emotion_score": result["score"]
    }