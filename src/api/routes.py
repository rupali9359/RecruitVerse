import sys
from pathlib import Path
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import FastAPI
from pydantic import BaseModel

from src.semantic_search.vector_search import (
    semantic_resume_search
)

from src.semantic_search.search_history import (
    save_semantic_search
)

from src.ai_insights.recruiter_copilot import (
    generate_insights
)

from src.services.save_ai_insights import (
    get_saved_ai_insights,
    save_ai_insight
)

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR)
    )


from src.api.database import (
    get_connection
)

from src.auth.login import (
    login_user
)

from src.auth.register import (
    register_user
)

from src.services.analytics_service import (
    get_recruiter_analytics,
    get_search_history,
    get_top_skills
)

from src.services.recommendation_engine import (
    generate_recommendation
)

from src.services.shortlisting import (
    shortlist_candidate
)

from src.utils.email_service import (
    send_email
)


app = FastAPI(
    title="RecruitVerse API"
)


router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class StatusRequest(BaseModel):
    resume_name: str
    final_score: Optional[float] = 0
    status: str


class NoteRequest(BaseModel):
    resume_name: str
    note: str


class ShortlistRequest(BaseModel):
    resume_name: str
    final_score: float


class RecommendationRequest(BaseModel):
    final_score: float
    missing_skills: List[str]


class EmailRequest(BaseModel):
    receiver: str
    subject: str
    message: str


class SearchRequest(BaseModel):
    search_term: str


class InterviewRequest(BaseModel):
    candidate_name: str
    interview_date: str
    status: Optional[str] = "Scheduled"

class AIInsightRequest(BaseModel):
    resume_name: str
    matched_skills: List[str]
    missing_skills: List[str]
    required_skills: Optional[List[str]] = None
    final_score: Optional[float] = None

@router.get("/")
def home():

    return {
        "message": "RecruitVerse API is running"
    }


@router.get("/health")
def health():

    return {
        "status": "OK"
    }


@router.post("/register")
def register(
        request: RegisterRequest):

    user_id = register_user(
        request.username,
        request.email,
        request.password
    )

    if user_id:

        return {
            "success": True,
            "message": "User Registered",
            "user_id": user_id
        }

    return {
        "success": False,
        "message": "User registration failed"
    }


@router.post("/login")
def login(
        request: LoginRequest):

    success = login_user(
        request.username,
        request.password
    )

    return {
        "success": success
    }


@router.post("/update_status")
def update_status(
        request: StatusRequest):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO candidate_status (
                resume_name,
                final_score,
                status
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (resume_name)
            DO UPDATE SET
                final_score = EXCLUDED.final_score,
                status = EXCLUDED.status,
                updated_at = CURRENT_TIMESTAMP;
            """,
            (
                request.resume_name,
                request.final_score,
                request.status
            )
        )

        conn.commit()

        return {
            "success": True,
            "message": "Status Updated"
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


@router.get("/candidate_status")
def candidate_status():

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                resume_name,
                final_score,
                status,
                updated_at
            FROM candidate_status
            ORDER BY updated_at DESC;
            """
        )

        rows = cursor.fetchall()

        return {
            "success": True,
            "data": [
                {
                    "resume_name": row[0],
                    "final_score": row[1],
                    "status": row[2],
                    "updated_at": str(
                        row[3]
                    )
                }
                for row in rows
            ]
        }

    except Exception as error:
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


@router.post("/add_note")
def add_note(
        request: NoteRequest):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO recruiter_notes (
                resume_name,
                note
            )
            VALUES (%s, %s);
            """,
            (
                request.resume_name,
                request.note
            )
        )

        conn.commit()

        return {
            "success": True,
            "message": "Note Added"
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


@router.get("/notes/{resume_name}")
def notes(
        resume_name: str):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                note,
                created_at
            FROM recruiter_notes
            WHERE resume_name = %s
            ORDER BY created_at DESC;
            """,
            (
                resume_name,
            )
        )

        rows = cursor.fetchall()

        return {
            "success": True,
            "data": [
                {
                    "note": row[0],
                    "created_at": str(
                        row[1]
                    )
                }
                for row in rows
            ]
        }

    except Exception as error:
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


@router.post("/shortlist")
def shortlist(
        request: ShortlistRequest):

    status = shortlist_candidate(
        request.final_score
    )

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO candidate_status (
                resume_name,
                final_score,
                status
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (resume_name)
            DO UPDATE SET
                final_score = EXCLUDED.final_score,
                status = EXCLUDED.status,
                updated_at = CURRENT_TIMESTAMP;
            """,
            (
                request.resume_name,
                request.final_score,
                status
            )
        )

        conn.commit()

        return {
            "success": True,
            "resume_name": request.resume_name,
            "final_score": request.final_score,
            "status": status
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


@router.post("/recommendation")
def recommendation(
        request: RecommendationRequest):

    return {
        "success": True,
        "recommendation": generate_recommendation(
            request.final_score,
            request.missing_skills
        )
    }


@router.post("/send_email")
def send_email_api(
        request: EmailRequest):

    return send_email(
        request.receiver,
        request.subject,
        request.message
    )


@router.get("/analytics")
def analytics():

    return {
        "success": True,
        "data": get_recruiter_analytics()
    }


@router.get("/top_skills")
def top_skills():

    return {
        "success": True,
        "data": get_top_skills()
    }


@router.post("/add_search")
def add_search(
        request: SearchRequest):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO search_history (
                search_term
            )
            VALUES (%s);
            """,
            (
                request.search_term,
            )
        )

        conn.commit()

        return {
            "success": True,
            "message": "Search history added"
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


@router.get("/search_history")
def search_history():

    return {
        "success": True,
        "data": get_search_history()
    }


@router.post("/schedule_interview")
def schedule_interview(
        request: InterviewRequest):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO interviews (
                candidate_name,
                interview_date,
                status
            )
            VALUES (%s, %s, %s);
            """,
            (
                request.candidate_name,
                request.interview_date,
                request.status
            )
        )

        conn.commit()

        return {
            "success": True,
            "candidate": request.candidate_name,
            "date": request.interview_date,
            "status": request.status
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


@router.get("/interviews")
def interviews():

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                candidate_name,
                interview_date,
                status,
                created_at
            FROM interviews
            ORDER BY interview_date DESC;
            """
        )

        rows = cursor.fetchall()

        return {
            "success": True,
            "data": [
                {
                    "candidate_name": row[0],
                    "interview_date": str(
                        row[1]
                    ),
                    "status": row[2],
                    "created_at": str(
                        row[3]
                    )
                }
                for row in rows
            ]
        }

    except Exception as error:
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

@router.post("/ai_insights")
def ai_insights(
        request: AIInsightRequest):

    insights = generate_insights(
        request.matched_skills,
        request.missing_skills,
        request.required_skills,
        request.final_score
    )

    save_result = save_ai_insight(
        request.resume_name,
        insights
    )

    return {
        "success": save_result[
            "success"
        ],
        "insights": insights,
        "save_result": save_result
    }


@router.get("/ai_insights")
def saved_ai_insights():

    return {
        "success": True,
        "data": get_saved_ai_insights()
    }


@router.get("/semantic_search")
def semantic_search(
        query: str,
        top_k: int = 10):

    results = semantic_resume_search(
        query,
        top_k=top_k
    )

    save_semantic_search(
        query
    )

    return results

app.include_router(
    router
)

