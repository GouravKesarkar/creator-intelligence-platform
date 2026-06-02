import json

from app.db.database import get_connection


def save_video(metadata):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO videos (
                video_id,
                title,
                description,
                channel_name,
                published_at,
                thumbnail_url,
                views,
                likes,
                comments
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)

            ON CONFLICT (video_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                views = EXCLUDED.views,
                likes = EXCLUDED.likes,
                comments = EXCLUDED.comments,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                metadata["video_id"],
                metadata["title"],
                metadata["description"],
                metadata["channel_title"],
                metadata["published_at"],
                metadata["thumbnail"],
                int(metadata["views"]),
                int(metadata["likes"]),
                int(metadata["comments"])
            )
        )

        conn.commit()
    
    except Exception as e:

        conn.rollback()
        raise e

    finally:
        conn.close()
		

def save_transcript(video_id, transcript):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO transcripts (
                video_id,
                transcript_text,
                transcript_json
            )
            VALUES (%s,%s,%s)

            ON CONFLICT (video_id)
            DO UPDATE SET
                transcript_text = EXCLUDED.transcript_text,
                transcript_json = EXCLUDED.transcript_json
            """,
            (
                video_id,
                transcript["full_transcript"],
                json.dumps(transcript["segments"])
            )
        )

        conn.commit()

    except Exception as e:

        conn.rollback()
        raise e

    finally:
        conn.close()
		
		
def save_analysis(video_id, hook_analysis):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO analyses (
                video_id,
                analysis_type,
                hook_score,
                curiosity_score,
                engagement_score,
                clarity_score,
                retention_score,
                analysis_json
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s
            )

            ON CONFLICT (video_id, analysis_type)
            DO UPDATE SET
                hook_score = EXCLUDED.hook_score,
                curiosity_score = EXCLUDED.curiosity_score,
                engagement_score = EXCLUDED.engagement_score,
                clarity_score = EXCLUDED.clarity_score,
                retention_score = EXCLUDED.retention_score,
                analysis_json = EXCLUDED.analysis_json
            """,
            (
                video_id,
                "HOOK",
                hook_analysis.get("hook_score"),
                hook_analysis.get("curiosity_score"),
                hook_analysis.get("engagement_score"),
                hook_analysis.get("clarity_score"),
                hook_analysis.get("retention_score"),
                json.dumps(hook_analysis)
            )
        )

        conn.commit()

    except Exception as e:

        conn.rollback()
        raise e

    finally:
        conn.close()


def get_all_analyses():

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                a.video_id,
                v.title,
                v.channel_name,
                a.hook_score,
                a.curiosity_score,
                a.engagement_score,
                a.created_at
            FROM analyses a
            JOIN videos v
                ON a.video_id = v.video_id
            ORDER BY a.created_at DESC
            """
        )

        rows = cursor.fetchall()

        results = []

        for row in rows:

            results.append({
                "video_id": row[0],
                "title": row[1],
                "channel_name": row[2],
                "hook_score": row[3],
                "curiosity_score": row[4],
                "engagement_score": row[5],
                "created_at": str(row[6])
            })

        return results

    finally:

        conn.close()