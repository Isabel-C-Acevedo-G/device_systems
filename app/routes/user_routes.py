"""Endpoints REST para el recurso 'users', usando persistencia con SQLAlchemy."""

from typing import Literal

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import UserCreate, UserPatch, UserResponse, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


def _set_custom_headers(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "3.0"


@router.get(
    "",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Lista todos los usuarios, con filtros opcionales por rol y estado.",
)
def get_users(
    response: Response,
    role: Literal["admin", "support", "user"] | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
) -> list:
    _set_custom_headers(response)
    return user_service.list_users(db, role=role, is_active=is_active)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario por ID",
    description="Devuelve un usuario específico. Lanza 404 si no existe.",
)
def get_user_by_id(
    user_id: int, response: Response, db: Session = Depends(get_db)
):
    _set_custom_headers(response)
    return user_service.get_user(db, user_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un usuario nuevo en la base de datos.",
)
def create_user(
    user: UserCreate, response: Response, db: Session = Depends(get_db)
):
    _set_custom_headers(response)
    return user_service.create_user(db, user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza todos los campos de un usuario existente.",
)
def replace_user(
    user_id: int, user: UserUpdate, response: Response, db: Session = Depends(get_db)
):
    _set_custom_headers(response)
    return user_service.replace_user(db, user_id, user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcial",
    description="Actualiza solo los campos enviados por el cliente.",
)
def update_user_partial(
    user_id: int, user: UserPatch, response: Response, db: Session = Depends(get_db)
):
    _set_custom_headers(response)
    return user_service.update_user_partial(db, user_id, user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario existente de la base de datos.",
)
def delete_user(
    user_id: int, response: Response, db: Session = Depends(get_db)
) -> None:
    _set_custom_headers(response)
    user_service.delete_user(db, user_id)