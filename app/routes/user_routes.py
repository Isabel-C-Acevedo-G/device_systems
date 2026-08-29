from typing import Literal

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

users_db: list[dict] = [
    {
        "id": 1,
        "name": "Facundo Cruz",
        "email": "facundo.cruz@example.com",
        "role": "admin",
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Carlos Vargas",
        "email": "carlos.vargas@example.com",
        "role": "support",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Felipe Acevedo",
        "email": "felipe.acevedo@example.com",
        "role": "user",
        "is_active": False,
    },
]


def _set_custom_headers(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

@router.get("", response_model=list[UserResponse])
def get_users(
    response: Response,
    role: Literal["admin", "support", "user"] | None = Query(default=None),
    is_active: bool | None = Query(default=None),
) -> list[dict]:
    _set_custom_headers(response)

    result = users_db
    if role is not None:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]

    return result

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, response: Response) -> dict:
    _set_custom_headers(response)

    for user in users_db:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario con id {user_id} no fue encontrado.",
    )

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, response: Response) -> dict:
    _set_custom_headers(response)

    if any(existing["email"] == user.email for existing in users_db):
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