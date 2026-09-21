"""Esquemas Pydantic v2 para la gestión de dispositivos."""

from datetime import datetime

from pydantic import BaseModel, Field


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=3)
    serial_number: str = Field(..., min_length=3)
    device_type: str = Field(..., min_length=3)
    brand: str | None = None
    is_available: bool = True


class DeviceCreate(DeviceBase):
    """Usado para crear un dispositivo nuevo (POST)."""
    pass


class DeviceUpdate(BaseModel):
    """Usado para actualización parcial (PATCH) — todo es opcional."""
    name: str | None = Field(default=None, min_length=3)
    serial_number: str | None = Field(default=None, min_length=3)
    device_type: str | None = None
    brand: str | None = None
    is_available: bool | None = None


class DeviceResponse(DeviceBase):
    """Lo que la API devuelve — incluye id y fecha de creación."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True