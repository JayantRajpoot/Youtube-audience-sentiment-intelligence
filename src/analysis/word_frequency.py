from collections import Counter
from nltk.corpus import stopwords
from src.utils.stopwords import HINGLISH_STOPWORDS


def get_word_frequency(df):

    english_stopwords = set(stopwords.words("english"))

    all_stopwords = english_stopwords.union(HINGLISH_STOPWORDS)

    all_words = []

    for comment in df["clean_comment"]:

        words = comment.split()

        filtered_words = [
            word
            for word in words
            if word not in all_stopwords
            and len(word) > 2
            and not word.isdigit()
        ]

        all_words.extend(filtered_words)

    return Counter(all_words)

def get_top_keywords(df, n=5):
    word_counts = get_word_frequency(df)
    return [word for word, _ in word_counts.most_common(n)]