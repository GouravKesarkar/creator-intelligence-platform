from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ai.hook_analyzer import analyze_hook


from app.youtube.youtube_service import (
    extract_video_id,
    get_video_metadata,
    get_video_transcript
)

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

    transcript = get_video_transcript(video_id)

    hook_analysis = None

    segments = transcript.get("segments", [])

    if segments:

        hook_text = " ".join(
            segment["text"]
            for segment in segments
            if segment["start"] <= 60
        )

        hook_analysis = analyze_hook(hook_text)

    return {
        "metadata": metadata,
        "transcript": transcript,
        "hook_analysis": hook_analysis
    }