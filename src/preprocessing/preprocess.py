
from src.data_collection.comments import get_video_comments
from src.preprocessing.text_cleaning import clean_text
from src.analysis.sentiment_analysis import analyze_sentiment

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
df["sentiment_data"] = df["clean_comment"].apply(analyze_sentiment)

df["compound"] = df["sentiment_data"].apply(lambda result: result["compound"])
df["sentiment"] = df["sentiment_data"].apply(lambda result: result["sentiment"])

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
print(df[["comment", "clean_comment"]].head())
print(df[["comment", "compound", "sentiment"]].head())
print("\nSentiment counts:")
print(df["sentiment"].value_counts())

print("\nSentiment percentages:")
print((df["sentiment"].value_counts(normalize=True) * 100).round(2))

df = df.drop(columns=["sentiment_data"])

df.to_csv(
    "data/raw/processed/comments_with_sentiment.csv",
    index=False,
    encoding="utf-8-sig"
)