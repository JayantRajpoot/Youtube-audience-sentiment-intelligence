from src.analysis.word_frequency import get_top_keywords


def generate_audience_summary(df):

    total_comments = len(df)

    positive_rate = (df["sentiment"] == "Positive").mean() * 100
    toxic_rate = df["is_toxic"].mean() * 100
    suspicious_rate = df["is_suspicious"].mean() * 100

    dominant_emotion = df["emotion"].mode()[0]

    top_keywords = get_top_keywords(df)

    summary = []

    # Sentiment
    if positive_rate >= 70:
        summary.append(
            f"😊 Most viewers reacted positively ({positive_rate:.1f}% positive comments)."
        )
    elif positive_rate >= 40:
        summary.append(
            f"😐 Audience reactions were mixed ({positive_rate:.1f}% positive comments)."
        )
    else:
        summary.append(
            "☹️ Audience reactions were mostly negative."
        )

    # Emotion
    summary.append(
        f"🎭 Dominant emotion: **{dominant_emotion}**."
    )

    # Toxicity
    if toxic_rate < 5:
        summary.append(
            f"🛡️ Very little toxic behavior was detected ({toxic_rate:.1f}%)."
        )
    elif toxic_rate < 15:
        summary.append(
            f"⚠️ Moderate toxicity detected ({toxic_rate:.1f}%)."
        )
    else:
        summary.append(
            f"🚨 High toxicity detected ({toxic_rate:.1f}%)."
        )

    # Suspicious Engagement
    if suspicious_rate < 5:
        summary.append(
            "✅ Audience engagement appears authentic."
        )
    else:
        summary.append(
            "⚠️ Some suspicious engagement patterns were detected."
        )

    # Topics
    summary.append(
        "💬 Top discussion topics: **" +
        ", ".join(top_keywords) +
        "**."
    )

    return summary
