"""Lógica de negocio para la gestión de usuarios."""

from fastapi import HTTPException, status

from app.data.users_db import users_db
from app.schemas.user_schema import UserCreate, UserUpdate


def list_users(role: str | None = None, is_active: bool | None = None) -> list[dict]:
    result = users_db
    if role is not None:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result


def get_user(user_id: int) -> dict:
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado",
    )


def email_exists(email: str, exclude_id: int | None = None) -> bool:
    return any(
        u["email"] == email for u in users_db if u["id"] != exclude_id
    )


def create_user(user: UserCreate) -> dict:
    if email_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El correo '{user.email}' ya se encuentra registrado.",
        )
    new_id = max((u["id"] for u in users_db), default=0) + 1
    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }
    users_db.append(new_user)
    return new_user


def replace_user(user_id: int, user: UserCreate) -> dict:
    existing = get_user(user_id)
    if email_exists(user.email, exclude_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El correo '{user.email}' ya se encuentra registrado.",
        )
    existing.update(
        name=user.name,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
    )
    return existing


def update_user_partial(user_id: int, user: UserUpdate) -> dict:
    existing = get_user(user_id)
    data = user.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar.",
        )
    if "email" in data and email_exists(data["email"], exclude_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El correo '{data['email']}' ya se encuentra registrado.",
        )
    existing.update(data)
    return existing


def delete_user(user_id: int) -> None:
    user = get_user(user_id)
    users_db.remove(user)
    