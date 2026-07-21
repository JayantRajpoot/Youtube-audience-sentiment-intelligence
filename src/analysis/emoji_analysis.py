from collections import Counter
import emoji


def get_emoji_frequency(df):

    all_emojis = []

    for comment in df["comment"]:

        emoji_list = emoji.emoji_list(comment)

        for item in emoji_list:
            all_emojis.append(item["emoji"])

    return Counter(all_emojis)