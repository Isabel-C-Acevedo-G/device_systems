"""Esquemas Pydantic v2 para la gestión de préstamos."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class LoanBase(BaseModel):
    user_id: int
    device_id: int


class LoanCreate(LoanBase):
    """Usado para crear un préstamo nuevo (POST)."""
    pass


class LoanUpdate(BaseModel):
    """Usado para actualización parcial (PATCH) — todo es opcional."""
    status: Literal["active", "returned", "overdue"] | None = None
    return_date: datetime | None = None


class LoanResponse(LoanBase):
    """Lo que la API devuelve — datos básicos del préstamo."""
    id: int
    loan_date: datetime
    return_date: datetime | None = None
    status: str

    class Config:
        from_attributes = True


class UserMiniResponse(BaseModel):
    """Datos básicos del usuario, para mostrar dentro de un préstamo."""
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class DeviceMiniResponse(BaseModel):
    """Datos básicos del dispositivo, para mostrar dentro de un préstamo."""
    id: int
    name: str
    serial_number: str
    device_type: str

    class Config:
        from_attributes = True


class LoanDetailResponse(BaseModel):
    """Préstamo con información completa del usuario y el dispositivo."""
    loan_id: int = Field(..., validation_alias="id")
    status: str
    loan_date: datetime
    return_date: datetime | None = None
    user: UserMiniResponse
    device: DeviceMiniResponse

    class Config:
        from_attributes = True
        populate_by_name = True