"""Dependencias reutilizables para las rutas de usuarios."""

from fastapi import Header, HTTPException, status

from app.data.users_db import users_db
from app.services.user_service import email_exists


def get_user_or_404(user_id: int) -> dict:
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado",
    )


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Simula una autenticación básica mediante cabecera."""
    if x_api_key != "device-systems-secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida o no proporcionada",
        )