from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Request
from pydantic import BaseModel

from slowapi import Limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.auth.login import (
    login_user
)

from src.auth.register import (
    register_user
)

from src.config.settings import (
    API_VERSION,
    APP_NAME,
    RATE_LIMIT
)

from src.semantic_search.search_history import (
    save_semantic_search
)

from src.semantic_search.vector_search import (
    semantic_resume_search
)

from src.utils.logger import (
    get_logger
)

from monitoring.health_checks import (
    get_health_status
)


logger = get_logger(
    "recruitverse.api"
)


app = FastAPI(
    title=f"{APP_NAME} API",
    version=f"{API_VERSION}.0.0"
)


limiter = Limiter(
    key_func=get_remote_address
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    SlowAPIMiddleware
)


router = APIRouter(
    prefix=f"/api/{API_VERSION}",
    tags=[
        "RecruitVerse API"
    ]
)


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


@app.get("/")
def root():

    return {
        "message": f"{APP_NAME} API is running",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def public_health():

    return {
        "status": "OK"
    }

@app.get("/health/details")
def public_health_details():

    return get_health_status()


@router.get("/")
@limiter.limit(
    RATE_LIMIT
)
def versioned_home(
        request: Request):

    return {
        "message": f"{APP_NAME} {API_VERSION} API is running"
    }


@router.get("/health")
@limiter.limit(
    RATE_LIMIT
)
def health(
        request: Request):

    return get_health_status()


@router.post("/login")
@limiter.limit(
    RATE_LIMIT
)
def login(
        request: Request,
        login_request: LoginRequest):

    success = login_user(
        login_request.username,
        login_request.password
    )

    logger.info(
        "Login attempt for username=%s success=%s",
        login_request.username,
        success
    )

    return {
        "success": success
    }


@router.post("/register")
@limiter.limit(
    "10/minute"
)
def register(
        request: Request,
        register_request: RegisterRequest):

    user_id = register_user(
        register_request.username,
        register_request.email,
        register_request.password
    )

    if user_id:

        logger.info(
            "User registered username=%s user_id=%s",
            register_request.username,
            user_id
        )

        return {
            "success": True,
            "message": "User Registered",
            "user_id": user_id
        }

    logger.warning(
        "User registration failed username=%s",
        register_request.username
    )

    return {
        "success": False,
        "message": "User registration failed"
    }


@router.get("/semantic_search")
@limiter.limit(
    RATE_LIMIT
)
def semantic_search(
        request: Request,
        query: str,
        top_k: int = 10):

    results = semantic_resume_search(
        query,
        top_k=top_k
    )

    save_semantic_search(
        query
    )

    logger.info(
        "Semantic search query=%s top_k=%s results=%s",
        query,
        top_k,
        len(results)
    )

    return results


app.include_router(
    router
)