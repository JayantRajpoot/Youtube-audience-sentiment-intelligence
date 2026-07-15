from collections import Counter
import pandas as pd
import emoji

from src.data_collection.comments import get_video_comments
from src.preprocessing.text_cleaning import clean_text

comments = get_video_comments("c35fpGWqXnk")

df = pd.DataFrame(comments, columns=["comment"])

df["clean_comment"] = df["comment"].apply(clean_text)

all_emojis = []

for comment in df["clean_comment"]:

    emoji_list = emoji.emoji_list(comment)

    for item in emoji_list:
        all_emojis.append(item["emoji"])

emoji_counts = Counter(all_emojis)

print(emoji_counts.most_common(10))