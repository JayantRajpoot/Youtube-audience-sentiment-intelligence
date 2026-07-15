import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="YouTube Audience Intelligence",
    page_icon="📺",
    layout="wide"
)

df = pd.read_csv(
    "data/raw/processed/comments_with_sentiment.csv",
    encoding="utf-8-sig"
)

st.title("📺 YouTube Audience Intelligence")
st.caption("Comment sentiment, emotion, toxicity, and engagement analysis")

total_comments = len(df)
positive_rate = (df["sentiment"] == "Positive").mean() * 100
toxic_rate = df["is_toxic"].mean() * 100
suspicious_rate = df["is_suspicious"].mean() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Comments", total_comments)
col2.metric("Positive Sentiment", f"{positive_rate:.1f}%")
col3.metric("Toxicity Rate", f"{toxic_rate:.1f}%")
col4.metric("Suspicious Engagement", f"{suspicious_rate:.1f}%")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Sentiment Distribution")
    st.bar_chart(df["sentiment"].value_counts())

with right:
    st.subheader("Emotion Distribution")
    st.bar_chart(df["emotion"].value_counts())

st.subheader("Comments for Review")

filter_option = st.selectbox(
    "Choose comments to display",
    ["All", "Negative", "Potentially Toxic", "Suspicious"]
)

if filter_option == "Negative":
    displayed_comments = df[df["sentiment"] == "Negative"]

elif filter_option == "Potentially Toxic":
    displayed_comments = df[df["is_toxic"]]

elif filter_option == "Suspicious":
    displayed_comments = df[df["is_suspicious"]]

else:
    displayed_comments = df

st.dataframe(
    displayed_comments[
        ["comment", "sentiment", "emotion", "toxicity_score", "suspicion_score"]
    ],
    use_container_width=True
)