import json

from src.api.database import (
    get_connection
)


def save_ai_insight(
        resume_name,
        insights):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO ai_insights (
                resume_name,
                summary,
                strengths,
                weaknesses,
                skill_gap_percentage,
                recommended_role,
                final_score
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (
                resume_name,
                insights.get(
                    "summary",
                    ""
                ),
                json.dumps(
                    insights.get(
                        "strengths",
                        []
                    )
                ),
                json.dumps(
                    insights.get(
                        "weaknesses",
                        []
                    )
                ),
                insights.get(
                    "skill_gap_percentage",
                    0
                ),
                insights.get(
                    "recommended_role",
                    ""
                ),
                insights.get(
                    "final_score",
                    0
                )
            )
        )

        insight_id = cursor.fetchone()[0]

        conn.commit()

        return {
            "success": True,
            "message": "AI insight saved successfully",
            "id": insight_id
        }

    except Exception as error:

        if conn:
            conn.rollback()

        return {
            "success": False,
            "message": str(
                error
            )
        }

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def get_saved_ai_insights():

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                resume_name,
                summary,
                strengths,
                weaknesses,
                skill_gap_percentage,
                recommended_role,
                final_score,
                created_at
            FROM ai_insights
            ORDER BY created_at DESC;
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "resume_name": row[1],
                "summary": row[2],
                "strengths": row[3],
                "weaknesses": row[4],
                "skill_gap_percentage": row[5],
                "recommended_role": row[6],
                "final_score": row[7],
                "created_at": str(
                    row[8]
                )
            }
            for row in rows
        ]

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()