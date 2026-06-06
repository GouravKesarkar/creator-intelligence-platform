from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db.repository import (
    save_video,
    save_transcript,
    save_analysis,
    save_comments,
    save_comment_analysis,
    get_video_details
)
from app.db.repository import get_all_analyses

from app.youtube.youtube_service import (
    extract_video_id,
    get_video_metadata,
    get_video_transcript
)
from app.youtube.comment_service import (
    get_video_comments
)

from app.ai.hook_analyzer import analyze_hook
from app.ai.comment_analyzer import analyze_comments

router = APIRouter()


class AnalyzeRequest(BaseModel):
    youtube_url: str


@router.post("/analyze")
async def analyze_video(request: AnalyzeRequest):

    video_id = extract_video_id(request.youtube_url)

    if not video_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL"
        )

    metadata = get_video_metadata(video_id)

    if not metadata:
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )
    save_video(metadata)

    comments = get_video_comments(video_id)
    comment_analysis = None

    if comments:

        save_comments(
            video_id,
            comments
        )

        comment_analysis = analyze_comments(
            comments
        )

        if comment_analysis:
            save_comment_analysis(
                video_id,
                comment_analysis
            )

 

    transcript = get_video_transcript(video_id)
    transcript_available = (
        "segments" in transcript
    )
    if transcript_available:
        save_transcript(
            video_id,
            transcript
        )

    hook_analysis = None

    segments = transcript.get("segments", [])

    if segments:

        hook_text = " ".join(
            segment["text"]
            for segment in segments
            if segment["start"] <= 60
        )

        hook_analysis = analyze_hook(hook_text)
        if hook_analysis:
            save_analysis(
                video_id,
                hook_analysis
            )

    return {
        "metadata": metadata,
        "comments": comments,
        "comment_analysis": comment_analysis,
        "transcript": transcript,
        "transcript_available": transcript_available,
        "hook_analysis": hook_analysis
    }



@router.get("/analyses")
async def analyses():

    return get_all_analyses()

"""
@router.get("/comments/{video_id}")
async def comments(video_id: str):

    return get_video_comments(video_id)
"""

@router.get(
    "/videos/{video_id}"
)
async def video_details(
    video_id: str
):

    result = get_video_details(
        video_id
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    return result