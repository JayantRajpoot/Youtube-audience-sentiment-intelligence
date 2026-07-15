
from src.data_collection.comments import get_video_comments
from src.preprocessing.text_cleaning import clean_text
from src.analysis.sentiment_analysis import analyze_sentiment
from src.analysis.emotion_analysis import analyze_emotion
from src.analysis.toxicity_analysis import analyze_toxicity

import pandas as pd
import matplotlib.pyplot as plt
import emoji

comments = get_video_comments("c35fpGWqXnk")

df = pd.DataFrame(comments, columns=["comment"])

def count_emojis(text):
    return emoji.emoji_count(text)

df["uppercase_count"] = df["comment"].apply(
    lambda x: sum(1 for c in x if c.isupper()))

df["comment_length"] = df["comment"].str.len()
df["word_count"] = df["comment"].str.split().str.len()
df["emoji_count"] = df["comment"].apply(count_emojis)
df["exclamation_count"] = df["comment"].str.count("!")
df["question_count"] = df["comment"].str.count(r"\?")
df["clean_comment"] = df["comment"].apply(clean_text)
comment_frequency = df["clean_comment"].value_counts()

df["duplicate_count"] = df["clean_comment"].map(comment_frequency)

df["is_duplicate_comment"] = df["duplicate_count"] > 1

df["suspicion_score"] = 0

df.loc[df["is_duplicate_comment"], "suspicion_score"] += 70

df.loc[df["word_count"] <= 2, "suspicion_score"] += 10

df.loc[df["emoji_count"] >= 5, "suspicion_score"] += 10

df["is_suspicious"] = df["suspicion_score"] >= 50
df["sentiment_data"] = df["clean_comment"].apply(analyze_sentiment)

df["compound"] = df["sentiment_data"].apply(lambda result: result["compound"])
df["sentiment"] = df["sentiment_data"].apply(lambda result: result["sentiment"])

df["emotion_data"] = df["clean_comment"].apply(analyze_emotion)

df["emotion"] = df["emotion_data"].apply(lambda result: result["emotion"])
df["emotion_score"] = df["emotion_data"].apply(
    lambda result: result["emotion_score"]
)

print(df.head())
print("Average comment length:", df["comment_length"].mean())

print("Longest comment:", df["comment_length"].max())

print("Shortest comment:", df["comment_length"].min())

print("Average word count:", df["word_count"].mean())

plt.figure(figsize=(8, 5))

plt.hist(df["comment_length"], bins=10)

plt.title("Distribution of Comment Length")
plt.xlabel("Comment Length (Characters)")
plt.ylabel("Number of Comments")

plt.show()

sentiment_counts = df["sentiment"].value_counts()

plt.figure(figsize=(7, 4))

plt.bar(
    sentiment_counts.index,
    sentiment_counts.values,
    color=["green", "gray", "red"]
)

plt.title("Sentiment Distribution of YouTube Comments")
plt.xlabel("Sentiment")
plt.ylabel("Number of Comments")

plt.show()

emotion_counts = df["emotion"].value_counts()

plt.figure(figsize=(8, 4))
plt.bar(emotion_counts.index, emotion_counts.values, color="mediumpurple")

plt.title("Emotion Distribution of YouTube Comments")
plt.xlabel("Emotion")
plt.ylabel("Number of Comments")

plt.show()

print(df[["comment", "clean_comment"]].head())
print(df[["comment", "compound", "sentiment"]].head())
print("\nSentiment counts:")
print(df["sentiment"].value_counts())

print("\nSentiment percentages:")
print((df["sentiment"].value_counts(normalize=True) * 100).round(2))

print(df[["comment", "sentiment", "emotion", "emotion_score"]].head())
print(df["emotion"].value_counts()) 

df["toxicity_data"] = df["clean_comment"].apply(analyze_toxicity)

df["toxicity_score"] = df["toxicity_data"].apply(
    lambda result: result["toxicity_score"]
)

df["is_toxic"] = df["toxicity_data"].apply(
    lambda result: result["is_toxic"]
)

toxic_count = df["is_toxic"].sum()
toxic_percentage = (toxic_count / len(df)) * 100

print(f"\nPotentially toxic comments: {toxic_count}")
print(f"Toxicity rate: {toxic_percentage:.2f}%")

print("\nComments flagged for review:")
print(
    df[df["is_toxic"]][["comment", "toxicity_score"]]
    .sort_values("toxicity_score", ascending=False)
    .head(10)
)

suspicious_count = df["is_suspicious"].sum()
suspicious_rate = (suspicious_count / len(df)) * 100

print(f"\nSuspicious engagement comments: {suspicious_count}")
print(f"Suspicious engagement rate: {suspicious_rate:.2f}%")

print("\nPotential duplicate/spam comments:")
print(
    df[df["is_suspicious"]][
        ["comment", "duplicate_count", "suspicion_score"]
    ].sort_values("suspicion_score", ascending=False)
)

df = df.drop(
    columns=["sentiment_data", "emotion_data", "toxicity_data"]
)

df.to_csv(
    "data/raw/processed/comments_with_sentiment.csv",
    index=False,
    encoding="utf-8-sig"
)