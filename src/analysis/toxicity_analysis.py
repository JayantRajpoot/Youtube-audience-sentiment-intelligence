import streamlit as st
from detoxify import Detoxify


@st.cache_resource
def load_toxicity_model():
    return Detoxify("unbiased")


toxicity_model = load_toxicity_model()


def analyze_toxicity(text):
    scores = toxicity_model.predict(text)

    toxicity_score = float(scores["toxicity"])

    return {
        "toxicity_score": toxicity_score,
        "is_toxic": toxicity_score >= 0.8
    }


if __name__ == "__main__":
    print(analyze_toxicity("You are terrible and nobody likes you."))