from wordcloud import WordCloud
from src.analysis.word_frequency import get_word_frequency
import matplotlib.pyplot as plt


def generate_wordcloud(df):

    word_counts = get_word_frequency(df)

    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color="#111d31",
        colormap="cool"
    ).generate_from_frequencies(word_counts)

    fig, ax = plt.subplots(figsize=(12, 6), facecolor="#111d31")
    ax.set_facecolor("#111d31")

    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    return fig
