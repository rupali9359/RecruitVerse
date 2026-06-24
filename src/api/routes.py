import sys
from pathlib import Path

from fastapi import APIRouter
from fastapi import FastAPI
from pydantic import BaseModel


ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR)
    )


from src.auth.login import (
    login_user
)

from src.auth.register import (
    register_user
)


app = FastAPI(
    title="RecruitVerse Authentication API"
)


router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


@router.get("/")
def home():

    return {
        "message": "RecruitVerse Authentication API is running"
    }


@router.get("/health")
def health():

    return {
        "status": "OK"
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


app.include_router(
    router
)