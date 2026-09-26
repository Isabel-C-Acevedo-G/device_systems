"""Lógica de negocio para autenticación."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import create_access_token, get_password_hash, verify_password
from app.models.user_model import User
from app.schemas.auth_schema import UserLogin, UserRegister


def register_user(db: Session, user: UserRegister) -> User:
    existing = db.query(User).filter(User.email == user.email).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El correo '{user.email}' ya está registrado.",
        )
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, credentials: UserLogin) -> str:
    user = db.query(User).filter(User.email == credentials.email).first()
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )
    token = create_access_token(data={"sub": user.email})
    return token