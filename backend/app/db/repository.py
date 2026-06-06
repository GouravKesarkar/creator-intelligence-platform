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

def save_comments(
    video_id,
    comments
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM comments
            WHERE video_id = %s
            """,
            (video_id,)
        )

        for comment in comments:

            cursor.execute(
                """
                INSERT INTO comments (
                    video_id,
                    comment_text
                )
                VALUES (%s,%s)
                """,
                (
                    video_id,
                    comment
                )
            )

        conn.commit()

    finally:

        conn.close()

def save_comment_analysis(
    video_id,
    analysis
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO comment_analyses (

                video_id,
                overall_sentiment,
                analysis_json

            )
            VALUES (%s,%s,%s)

            ON CONFLICT (video_id)
            DO UPDATE SET

                overall_sentiment =
                    EXCLUDED.overall_sentiment,

                analysis_json =
                    EXCLUDED.analysis_json
            """,
            (
                video_id,

                analysis.get(
                    "overall_sentiment"
                ),

                json.dumps(
                    analysis
                )
            )
        )

        conn.commit()

    finally:

        conn.close()


def get_all_analyses():

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                v.video_id,
                v.title,
                v.channel_name,
                a.hook_score,
                a.curiosity_score,
                a.engagement_score,
                CASE
                    WHEN a.video_id IS NULL
                    THEN 'PENDING'
                    ELSE 'ANALYZED'
                END AS status,
                v.created_at
            FROM videos v
            LEFT JOIN analyses a
                ON v.video_id = a.video_id
            ORDER BY v.created_at DESC
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
                "status": row[6],
                "created_at": str(row[7])
            })

        return results

    finally:

        conn.close()

def get_video_details(video_id):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                video_id,
                title,
                description,
                channel_name,
                published_at,
                thumbnail_url,
                views,
                likes,
                comments
            FROM videos
            WHERE video_id = %s
            """,
            (video_id,)
        )

        video_row = cursor.fetchone()

        if not video_row:
            return None

        video = {
            "video_id": video_row[0],
            "title": video_row[1],
            "description": video_row[2],
            "channel_name": video_row[3],
            "published_at": str(video_row[4]),
            "thumbnail_url": video_row[5],
            "views": video_row[6],
            "likes": video_row[7],
            "comments": video_row[8]
        }

        # Comment Analysis

        cursor.execute(
            """
            SELECT
                analysis_json
            FROM comment_analyses
            WHERE video_id = %s
            """,
            (video_id,)
        )

        comment_row = cursor.fetchone()

        comment_analysis = None

        if comment_row:
            comment_analysis = comment_row[0]

        # Hook Analysis

        cursor.execute(
            """
            SELECT
                analysis_json
            FROM analyses
            WHERE video_id = %s
            AND analysis_type = 'HOOK'
            """,
            (video_id,)
        )

        hook_row = cursor.fetchone()

        hook_analysis = None

        if hook_row:
            hook_analysis = hook_row[0]

        return {
            "video": video,
            "comment_analysis": comment_analysis,
            "hook_analysis": hook_analysis
        }

    finally:

        conn.close()