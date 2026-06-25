from collections import Counter

from src.api.database import (
    get_connection
)


def get_recruiter_analytics():

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*),
                COALESCE(AVG(final_score), 0)
            FROM candidate_status;
            """
        )

        total_candidates, average_score = cursor.fetchone()

        cursor.execute(
            """
            SELECT
                status,
                COUNT(*)
            FROM candidate_status
            GROUP BY status;
            """
        )

        status_rows = cursor.fetchall()

        status_counts = {
            row[0]: row[1]
            for row in status_rows
        }

        shortlisted = status_counts.get(
            "Shortlisted",
            0
        )

        rejected = status_counts.get(
            "Rejected",
            0
        )

        selected = status_counts.get(
            "Selected",
            0
        )

        total = total_candidates or 0

        shortlisted_percent = (
            shortlisted / total * 100
            if total
            else 0
        )

        rejected_percent = (
            rejected / total * 100
            if total
            else 0
        )

        selected_percent = (
            selected / total * 100
            if total
            else 0
        )

        return {
            "total_candidates": total,
            "average_score": round(
                float(
                    average_score
                ),
                2
            ),
            "status_counts": status_counts,
            "shortlisted_percent": round(
                shortlisted_percent,
                2
            ),
            "rejected_percent": round(
                rejected_percent,
                2
            ),
            "selected_percent": round(
                selected_percent,
                2
            )
        }

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def get_top_skills(
        limit=10):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT matched_skills
            FROM candidate_explanations
            WHERE matched_skills IS NOT NULL;
            """
        )

        rows = cursor.fetchall()

        all_skills = []

        for row in rows:

            skill_text = row[0]

            if not skill_text:
                continue

            skill_text = (
                skill_text
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
                .replace('"', "")
                .replace(";", ",")
            )

            skills = [
                skill.strip()
                for skill in skill_text.split(",")
                if skill.strip()
            ]

            all_skills.extend(
                skills
            )

        skill_counts = Counter(
            all_skills
        )

        return [
            {
                "skill": skill,
                "count": count
            }
            for skill, count in skill_counts.most_common(
                limit
            )
        ]

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def get_search_history(
        limit=20):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                search_term,
                created_at
            FROM search_history
            ORDER BY created_at DESC
            LIMIT %s;
            """,
            (
                limit,
            )
        )

        rows = cursor.fetchall()

        return [
            {
                "search_term": row[0],
                "created_at": str(
                    row[1]
                )
            }
            for row in rows
        ]

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()