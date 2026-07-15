from wordcloud import WordCloud
import matplotlib.pyplot as plt

from src.analysis.word_frequency import get_word_frequency


word_counts = get_word_frequency("c35fpGWqXnk")

wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color="white"
).generate_from_frequencies(word_counts)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most Frequent Words in YouTube Comments")
plt.show()