"""Endpoints de autenticación."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.auth import auth_service
from app.dependencies.auth_dependency import get_current_user
from app.dependencies.database_dependency import get_db
from app.models.user_model import User
from app.schemas.auth_schema import AuthUserResponse, Token, UserLogin, UserRegister

router = APIRouter(prefix="/auth", tags=["Auth"])

limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=AuthUserResponse, summary="Registrar usuario")
@limiter.limit("3/minute")
def register(request: Request, user: UserRegister, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user)


@router.post("/login", response_model=Token, summary="Iniciar sesión")
@limiter.limit("5/minute")
def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    token = auth_service.authenticate_user(db, credentials)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=AuthUserResponse, summary="Usuario autenticado actual")
def me(current_user: User = Depends(get_current_user)):
    return current_user