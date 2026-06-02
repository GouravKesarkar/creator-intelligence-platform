from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def analyze_hook(transcript_text: str):

    prompt = f"""
    You are a YouTube growth expert.

    Analyze the first 60 seconds of this video transcript.

    Evaluate:
    1. Hook strength
    2. Curiosity creation
    3. Emotional engagement
    4. Clarity
    5. Viewer retention potential

    Give:
    - hook score out of 100
    - strengths
    - weaknesses
    - actionable recommendations

    Transcript:
    {transcript_text}
    """

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
