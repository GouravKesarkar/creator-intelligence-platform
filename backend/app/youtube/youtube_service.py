import re
import requests

from app.config import YOUTUBE_API_KEY


def extract_video_id(youtube_url: str):

    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, youtube_url)

        if match:
            return match.group(1)

    return None


def get_video_metadata(video_id: str):
    print("VIDEO ID:", video_id)

    url = (
        "https://www.googleapis.com/youtube/v3/videos"
    )

    params = {
        "part": "snippet,statistics",
        "id": video_id,
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    print("YOUTUBE RESPONSE:", data)

    items = data.get("items")

    if not items:
        return None

    item = items[0]

    snippet = item["snippet"]
    statistics = item["statistics"]

    return {
        "video_id": video_id,
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "channel_title": snippet.get("channelTitle"),
        "published_at": snippet.get("publishedAt"),
        "thumbnail": snippet["thumbnails"]["high"]["url"],
        "views": statistics.get("viewCount"),
        "likes": statistics.get("likeCount"),
        "comments": statistics.get("commentCount")
    }


from youtube_transcript_api import YouTubeTranscriptApi


def get_video_transcript(video_id: str):

    try:
        api = YouTubeTranscriptApi() 
        transcript_data = api.fetch(video_id)

        transcript_text = " ".join(
            [item.text for item in transcript_data]
        )

        segments = []

        for item in transcript_data:

            segments.append({
                "text": item.text,
                "start": item.start,
                "duration": item.duration
            })

        return {
        "full_transcript": transcript_text,
        "segments": segments
        }

    except Exception as e:

        return {
            "error": str(e)
        }