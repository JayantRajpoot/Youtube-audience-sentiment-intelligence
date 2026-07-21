import pandas as pd
import emoji
import streamlit as st

from src.data_collection.comments import get_video_comments
from src.preprocessing.text_cleaning import clean_text
from src.analysis.sentiment_analysis import analyze_sentiment
from src.analysis.emotion_analysis import analyze_emotion
from src.analysis.toxicity_analysis import analyze_toxicity




def count_emojis(text):
    return emoji.emoji_count(text)

@st.cache_data(show_spinner=False)
def analyze_video(video_id):

    comments = get_video_comments(video_id)

    df = pd.DataFrame(comments, columns=["comment"])

    # =============================
    # Feature Engineering
    # =============================

    df["uppercase_count"] = df["comment"].apply(
        lambda x: sum(1 for c in x if c.isupper())
    )

    df["comment_length"] = df["comment"].str.len()
    df["word_count"] = df["comment"].str.split().str.len()
    df["emoji_count"] = df["comment"].apply(count_emojis)
    df["exclamation_count"] = df["comment"].str.count("!")
    df["question_count"] = df["comment"].str.count(r"\?")
    df["clean_comment"] = df["comment"].apply(clean_text)

    # =============================
    # Suspicious Engagement
    # =============================

    comment_frequency = df["clean_comment"].value_counts()

    df["duplicate_count"] = df["clean_comment"].map(comment_frequency)

    df["is_duplicate_comment"] = df["duplicate_count"] > 1

    df["suspicion_score"] = 0

    df.loc[df["is_duplicate_comment"], "suspicion_score"] += 70
    df.loc[df["word_count"] <= 2, "suspicion_score"] += 10
    df.loc[df["emoji_count"] >= 5, "suspicion_score"] += 10

    df["is_suspicious"] = df["suspicion_score"] >= 50

    # =============================
    # Sentiment Analysis
    # =============================

    df["sentiment_data"] = df["clean_comment"].apply(analyze_sentiment)

    df["compound"] = df["sentiment_data"].apply(
        lambda result: result["compound"]
    )

    df["sentiment"] = df["sentiment_data"].apply(
        lambda result: result["sentiment"]
    )

    # =============================
    # Emotion Analysis
    # =============================

    df["emotion_data"] = df["clean_comment"].apply(analyze_emotion)

    df["emotion"] = df["emotion_data"].apply(
        lambda result: result["emotion"]
    )

    df["emotion_score"] = df["emotion_data"].apply(
        lambda result: result["emotion_score"]
    )

    # =============================
    # Toxicity Analysis
    # =============================

    df["toxicity_data"] = df["clean_comment"].apply(analyze_toxicity)

    df["toxicity_score"] = df["toxicity_data"].apply(
        lambda result: result["toxicity_score"]
    )

    df["is_toxic"] = df["toxicity_data"].apply(
        lambda result: result["is_toxic"]
    )

    # =============================
    # Cleanup
    # =============================

    df = df.drop(
        columns=[
            "sentiment_data",
            "emotion_data",
            "toxicity_data"
        ]
    )

    return df