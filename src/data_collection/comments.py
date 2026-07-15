from src.data_collection.youtube_client import get_youtube_client


def get_video_comments(video_id):

    youtube_client = get_youtube_client()

    video_comments = youtube_client.commentThreads().list(
    videoId=video_id,
    part="snippet",
    maxResults=100,
    textFormat="plainText"
    ).execute()

    comments_list = []

    for comment in video_comments["items"]:
        comment_text = comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        comments_list.append(comment_text)

    return comments_list
