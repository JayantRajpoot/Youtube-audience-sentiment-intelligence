from src.pipeline.analyze_video import analyze_video

video_id = "c35fpGWqXnk"

df = analyze_video(video_id)

df.to_csv(
    "data/raw/processed/comments_with_sentiment.csv",
    index=False,
    encoding="utf-8-sig"
)

print("CSV generated successfully!")