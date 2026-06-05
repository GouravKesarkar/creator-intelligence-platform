import requests

from app.config import YOUTUBE_API_KEY


def get_video_comments(
    video_id: str,
    max_results: int = 50
):

    url = (
        "https://www.googleapis.com/youtube/v3/commentThreads"
    )

    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    comments = []

    for item in data.get("items", []):

        text = item["snippet"][
            "topLevelComment"
        ]["snippet"]["textDisplay"]

        comments.append(text)

    return comments