"""Schemas Pydantic v2 para autenticación."""

import re
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class UserRegister(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Literal["admin", "support", "user"] = "user"

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contraseña no debe contener espacios")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Debe tener al menos una mayúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("Debe tener al menos una minúscula")
        if not re.search(r"\d", v):
            raise ValueError("Debe tener al menos un número")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None


class AuthUserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)