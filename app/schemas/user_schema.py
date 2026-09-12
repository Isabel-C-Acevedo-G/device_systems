"""Esquemas Pydantic v2 para la gestión de usuarios."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool = True


class UserCreate(UserBase):
    """Usado para crear un usuario nuevo (POST)."""
    pass


class UserUpdate(UserBase):
    """Usado para reemplazar un usuario completo (PUT)."""
    pass


class UserPatch(BaseModel):
    """Usado para actualización parcial (PATCH) — todo es opcional."""
    name: str | None = Field(default=None, min_length=3)
    email: EmailStr | None = None
    role: Literal["admin", "support", "user"] | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """Lo que la API devuelve — incluye id y fecha de creación."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True