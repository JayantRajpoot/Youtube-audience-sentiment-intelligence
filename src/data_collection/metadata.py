from src.data_collection.youtube_client import get_youtube_client


def get_video_metadata(video_id):

    youtube_client = get_youtube_client()

    video_response = youtube_client.videos().list(
        id=video_id,
        part="snippet,statistics"
    ).execute()

    snippet = video_response["items"][0]["snippet"]
    statistics = video_response["items"][0]["statistics"]

    video_metadata = {
        "title": snippet["title"],
        "channel": snippet["channelTitle"],
        "published_at": snippet["publishedAt"],
        "description": snippet["description"],
        "views": statistics["viewCount"],
        "comment_count": statistics["commentCount"],
        "thumbnail": snippet["thumbnails"]["high"]["url"]
    }

    return video_metadata