"""Dependencias para proteger rutas con OAuth2 y JWT."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.dependencies.database_dependency import get_db
from app.models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    email = payload.get("sub")
    if email is None:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")
    return user


def require_admin(user: User = Depends(get_current_active_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requiere rol admin")
    return user


def require_admin_or_support(user: User = Depends(get_current_active_user)) -> User:
    if user.role not in ("admin", "support"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requiere rol admin o support")
    return user