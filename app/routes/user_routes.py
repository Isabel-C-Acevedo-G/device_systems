"""Endpoints REST para el recurso 'users'."""

from typing import Literal

from fastapi import APIRouter, Response, status

from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


def _set_custom_headers(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"


@router.get("", response_model=list[UserResponse], summary="Listar usuarios")
def get_users(
    response: Response,
    role: Literal["admin", "support", "user"] | None = None,
    is_active: bool | None = None,
) -> list[dict]:
    _set_custom_headers(response)
    return user_service.list_users(role=role, is_active=is_active)


@router.get("/{user_id}", response_model=UserResponse, summary="Consultar usuario por ID")
def get_user_by_id(user_id: int, response: Response) -> dict:
    _set_custom_headers(response)
    return user_service.get_user(user_id)


@router.post(
    "", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
)
def create_user(user: UserCreate, response: Response) -> dict:
    _set_custom_headers(response)
    return user_service.create_user(user)


@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar usuario completo")
def replace_user(user_id: int, user: UserCreate, response: Response) -> dict:
    _set_custom_headers(response)
    return user_service.replace_user(user_id, user)


@router.patch("/{user_id}", response_model=UserResponse, summary="Actualizar usuario parcial")
def update_user_partial(user_id: int, user: UserUpdate, response: Response) -> dict:
    _set_custom_headers(response)
    return user_service.update_user_partial(user_id, user)


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
)
def delete_user(user_id: int, response: Response) -> None:
    _set_custom_headers(response)
    user_service.delete_user(user_id)