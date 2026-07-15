from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")


def get_youtube_client():
    youtube = build(
        serviceName="youtube",
        version="v3",
        developerKey=api_key
    )
    return youtube