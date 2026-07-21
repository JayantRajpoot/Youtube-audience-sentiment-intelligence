# 📺 YouTube Audience Intelligence

An end-to-end data analytics and NLP application that analyzes YouTube comments to uncover audience sentiment, emotions, toxicity, engagement patterns, and discussion trends.

The application uses the YouTube Data API to collect comments, processes them using Natural Language Processing (NLP) techniques, and presents the results through an interactive Streamlit dashboard.

---

## Features

- Analyze comments from any public YouTube video
- Sentiment Analysis (Positive, Neutral, Negative)
- Emotion Detection using Hugging Face Transformers
- Toxicity Detection with Detoxify
- Suspicious/Spam Comment Detection
- AI-generated audience insights
- Interactive visualizations with Plotly
- Word Cloud and Emoji Analysis
- Search and filter comments
- Export analysis as CSV

---

## Dashboard Preview

![Dashboard Overview](assets/dashboard.png)

---

## Tech Stack

**Languages**
- Python

**Libraries & Frameworks**
- Streamlit
- Pandas
- Plotly
- NLTK
- Hugging Face Transformers
- Detoxify
- WordCloud
- Emoji

**APIs**
- YouTube Data API v3

---

## Project Structure

```text
Youtube-Audience-Intelligence/
│
├── app.py
├── assets/
├── src/
│   ├── analysis/
│   ├── data_collection/
│   ├── pipeline/
│   ├── preprocessing/
│   ├── utils/
│   └── visualization/
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/Youtube-audience-sentiment-intelligence.git
```

Navigate to the project

```bash
cd Youtube-audience-sentiment-intelligence
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your YouTube API key

```env
YOUTUBE_API_KEY=YOUR_API_KEY
```

Run the application

```bash
streamlit run app.py
```

---

## How It Works

```
YouTube Video
      │
      ▼
Fetch Comments
      │
      ▼
Text Cleaning
      │
      ▼
Sentiment Analysis
      │
      ▼
Emotion Detection
      │
      ▼
Toxicity Detection
      │
      ▼
Suspicious Engagement Detection
      │
      ▼
Interactive Dashboard
```

---

## Future Improvements

- PDF report export
- Multi-language support
- Topic modeling
- Time-series sentiment analysis
- Cloud deployment

---

## Author

**Jayant Rajput**

BCA Student | Aspiring Data Analyst

If you have any suggestions or feedback, feel free to open an issue or connect with me on LinkedIn.