from openai import OpenAI
from app.config import OPENAI_API_KEY
import json

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def analyze_comments(comments):

    comments_text = "\n".join(
        comments[:100]
    )

    prompt = f"""
    You are a YouTube audience intelligence expert.

    Analyze these YouTube comments.
    Based on audience interests,
    questions and requests,
    suggest 3-5 future video ideas.

    The ideas should be highly relevant
    to what viewers are asking for.

    Each idea must include:
    - title
    - reason

    IMPORTANT:
    Return ONLY valid JSON.
    Do NOT wrap the JSON in markdown.
    Do NOT use ```json.
    Do NOT include explanations outside the JSON.

    Schema:

    {{
        "overall_sentiment": "",

        "top_topics": [
            "string"
        ],

        "viewer_questions": [
            "string"
        ],

        "content_requests": [
            "string"
        ],

        "positive_feedback": [
            "string"
        ],

        "negative_feedback": [
            "string"
        ],

        "next_video_ideas": [
            {{
                "title": "string",
                "reason": "string"
            }}
        ],

        "summary": ""
    }}

    Comments:

    {comments_text}
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