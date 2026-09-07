"""Esquemas Pydantic v2 para la gestión de usuarios."""

from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool = True


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3)
    email: EmailStr | None = None
    role: Literal["admin", "support", "user"] | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int