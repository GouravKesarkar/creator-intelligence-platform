from openai import OpenAI
from app.config import OPENAI_API_KEY
import json

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def analyze_hook(transcript_text: str):

    prompt = f"""
    You are a YouTube growth expert.

    Analyze the first 60 seconds of this transcript.

    IMPORTANT:
    Return ONLY valid JSON.
    Do NOT wrap the JSON in markdown.
    Do NOT use ```json.
    Do NOT include explanations outside the JSON.

    Schema:

    {{
        "hook_score": 0-100,
        "curiosity_score": 0-100,
        "engagement_score": 0-100,
        "clarity_score": 0-100,
        "retention_score": 0-100,
        "strengths": [
            "string"
        ],
        "weaknesses": [
            "string"
        ],
        "recommendations": [
            "string"
        ]
    }}

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

    content = response.choices[0].message.content
    # Remove markdown code fences
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    try:
        return json.loads(content)

    except Exception as e:

        print("JSON PARSE ERROR:", e)
        print("RAW CONTENT:", content)

        return {
            "raw_response": content
        }
