"""Agrupa los modelos para que SQLAlchemy los registre todos al importar el paquete."""

from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan

__all__ = ["User", "Device", "Loan"]