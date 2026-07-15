from collections import Counter
import pandas as pd
from nltk.corpus import stopwords

from src.utils.stopwords import HINGLISH_STOPWORDS
from src.data_collection.comments import get_video_comments
from src.preprocessing.text_cleaning import clean_text


def get_word_frequency(video_id):

    comments = get_video_comments(video_id)

    df = pd.DataFrame(comments, columns=["comment"])

    df["clean_comment"] = df["comment"].apply(clean_text)

    english_stopwords = set(stopwords.words("english"))
    all_stopwords = english_stopwords.union(HINGLISH_STOPWORDS)

    all_words = []

    for comment in df["clean_comment"]:
        words = comment.split()

        filtered_words = [
            word
            for word in words
            if word not in all_stopwords and word.isalpha()
        ]

        all_words.extend(filtered_words)

    word_counts = Counter(all_words)

    return word_counts


if __name__ == "__main__":
    counts = get_word_frequency("c35fpGWqXnk")
    print(counts.most_common(20))