import streamlit as st
import pandas as pd
import plotly.express as px
import nltk

resources = [
    ("corpora/stopwords", "stopwords"),
    ("tokenizers/punkt", "punkt"),
    ("tokenizers/punkt_tab", "punkt_tab"),
    ("corpora/wordnet", "wordnet"),
    ("corpora/omw-1.4", "omw-1.4"),
]

for path, name in resources:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(name)

from src.pipeline.analyze_video import analyze_video
from src.utils.youtube_parser import extract_video_id
from src.data_collection.metadata import get_video_metadata
from src.visualization.wordcloud_visualization import generate_wordcloud
from src.analysis.emoji_analysis import get_emoji_frequency
from src.analysis.audience_summary import generate_audience_summary

# =====================================
# Page Config (MUST BE FIRST)
# =====================================

st.set_page_config(
    page_title="YouTube Audience Intelligence",
    page_icon="📺",
    layout="wide"
)


# =====================================
# Load CSS
# =====================================

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()


# =====================================
# Hero Section
# =====================================

st.markdown(
    """
    <div class="hero">
        <h1>📺 YouTube Audience Intelligence</h1>
        <p>
            Analyze YouTube comments using AI-powered
            sentiment, emotion, toxicity, and engagement analytics.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================
# URL Input
# =====================================

left, right = st.columns([5, 1], vertical_alignment="bottom")

with left:
    video_url = st.text_input(
        "",
        placeholder="Paste a YouTube video URL..."
    )

with right:
    analyze = st.button(
        "🚀 Analyze",
        use_container_width=True
    )   


# =====================================
# Session State
# =====================================

if "df" not in st.session_state:
    st.session_state.df = None

if "metadata" not in st.session_state:
    st.session_state.metadata = None


# =====================================
# Analyze Video
# =====================================

if analyze:

    video_id = extract_video_id(video_url)

    if video_id is None:
        st.error("Please enter a valid YouTube URL.")
        st.stop()

    try:
        with st.spinner("🔍 Analyzing YouTube comments..."):
            st.session_state.df = analyze_video(video_id)
            st.session_state.metadata = get_video_metadata(video_id)

    except Exception as e:
        st.error("❌ Failed to analyze this video.")
        st.exception(e)
        st.stop()


# =====================================
# Wait Until Analysis Completes
# =====================================

if st.session_state.df is None:
    st.info("👆 Paste a YouTube video URL above and click **Analyze**.")
    st.stop()


df = st.session_state.df
metadata = st.session_state.metadata

# =====================================
# Video Information
# =====================================

with st.container(border=True):

    st.subheader("🎥 Video Overview")

    col1, col2 = st.columns([1,3])

    with col1:
        st.image(metadata["thumbnail"], use_container_width=True)

    with col2:
        st.markdown(f"### {metadata['title']}")

        st.markdown(f"👤 **Channel:** {metadata['channel']}")
        st.markdown(f"👀 **Views:** {int(metadata['views']):,}")
        st.markdown(f"💬 **Comments:** {int(metadata['comment_count']):,}")
        st.markdown(f"📅 **Published:** {metadata['published_at'][:10]}")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# Metrics
# ==========================

total_comments = len(df)
positive_rate = (df["sentiment"] == "Positive").mean() * 100
toxic_rate = df["is_toxic"].mean() * 100
suspicious_rate = df["is_suspicious"].mean() * 100

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">💬</div>
        <div class="metric-value">{total_comments:,}</div>
        <div class="metric-label">Comments</div>
    </div>
    """, unsafe_allow_html=True)

with metric2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">😊</div>
        <div class="metric-value">{positive_rate:.1f}%</div>
        <div class="metric-label">Positive</div>
    </div>
    """, unsafe_allow_html=True)

with metric3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-value">{toxic_rate:.1f}%</div>
        <div class="metric-label">Toxicity</div>
    </div>
    """, unsafe_allow_html=True)

with metric4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🚨</div>
        <div class="metric-value">{suspicious_rate:.1f}%</div>
        <div class="metric-label">Spam</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):

    st.subheader("📋 Audience Summary")

    summary = generate_audience_summary(df)

    for line in summary:
        st.markdown(line)
        
st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# Charts
# ==========================

left, right = st.columns(2)

with left:
    with st.container(border=True):

        st.subheader("📊 Sentiment Distribution")

        sentiment_counts = (
            df["sentiment"]
            .value_counts()
            .reset_index()
        )

        sentiment_counts.columns = ["Sentiment", "Count"]

        fig = px.bar(
            sentiment_counts,
            x="Sentiment",
            y="Count",
            color="Sentiment",
            text_auto=True
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Comments"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="sentiment_chart"
        )

with right:
    with st.container(border=True):

        st.subheader("🎭 Emotion Distribution")

        emotion_counts = (
            df["emotion"]
            .value_counts()
            .reset_index()
        )

        emotion_counts.columns = ["Emotion", "Count"]

        fig = px.bar(
            emotion_counts,
            x="Emotion",
            y="Count",
            color="Emotion",
            text_auto=True
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="white",
                size=14
            ),
            margin=dict(
                l=20,
                r=20,
                t=40,
                b=20
            ),
            xaxis=dict(
                title="",
                showgrid=False
            ),
            yaxis=dict(
                title="Comments",
                gridcolor="#334155"
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="emotion_chart"
        )

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    with st.container(border=True):

        st.subheader("☁️ Word Cloud")

        fig = generate_wordcloud(df)

        st.pyplot(fig)

with right:
    with st.container(border=True):

        st.subheader("😂 Top Emojis")

        emoji_counts = get_emoji_frequency(df)

        emoji_df = pd.DataFrame(
            emoji_counts.most_common(10),
            columns=["Emoji", "Count"]
        )

        fig = px.bar(
            emoji_df,
            x="Emoji",
            y="Count",
            text_auto=True
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="white",
                size=14
        ),
            margin=dict(
                l=20,
                r=20,
                t=40,
                b=20
        ),
            xaxis=dict(
                showgrid=False
    ),
    yaxis=dict(
        gridcolor="#334155"
    ),
    showlegend=False
)

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="emoji_chart"
        )

# ==========================
# Comments Table
# ==========================

with st.container(border=True):

    st.subheader("💬 Comments Explorer")

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

    search = st.text_input("🔍 Search comments")

    if search:
        displayed_comments = displayed_comments[
            displayed_comments["comment"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.download_button(
        "📥 Download Analysis CSV",
        data=displayed_comments.to_csv(index=False),
        file_name="youtube_comment_analysis.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.dataframe(
        displayed_comments[
            [
                "comment",
                "sentiment",
                "emotion",
                "toxicity_score",
                "suspicion_score"
            ]
        ],
        use_container_width=True
    )