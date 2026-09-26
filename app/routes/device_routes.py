"""Endpoints REST para el recurso 'devices'."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import require_admin, require_admin_or_support
from app.models.user_model import User
from app.schemas.device_schema import DeviceCreate, DeviceResponse, DeviceUpdate
from app.schemas.loan_schema import LoanResponse
from app.services import device_service
from app.services import loan_service

router = APIRouter(prefix="/devices", tags=["Devices"])


def _set_custom_headers(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "5.0"


@router.get(
    "",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    description="Lista dispositivos, con filtros opcionales por tipo, disponibilidad, marca o búsqueda de texto.",
)
def get_devices(
    response: Response,
    device_type: str | None = None,
    is_available: bool | None = None,
    brand: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    _set_custom_headers(response)
    return device_service.list_devices(
        db, device_type=device_type, is_available=is_available, brand=brand, search=search
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Consultar dispositivo por ID",
    description="Devuelve un dispositivo específico. Lanza 404 si no existe.",
)
def get_device_by_id(device_id: int, response: Response, db: Session = Depends(get_db)):
    _set_custom_headers(response)
    return device_service.get_device(db, device_id)


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Registra un dispositivo nuevo, validando que el número de serie sea único. Requiere rol admin o support.",
)
def create_device(
    device: DeviceCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    _set_custom_headers(response)
    return device_service.create_device(db, device)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo completo",
    description="Reemplaza todos los campos de un dispositivo existente. Requiere rol admin o support.",
)
def replace_device(
    device_id: int,
    device: DeviceCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    _set_custom_headers(response)
    return device_service.replace_device(db, device_id, device)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcial",
    description="Actualiza solo los campos enviados por el cliente.",
)
def update_device_partial(
    device_id: int, device: DeviceUpdate, response: Response, db: Session = Depends(get_db)
):
    _set_custom_headers(response)
    return device_service.update_device_partial(db, device_id, device)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo existente. Requiere rol admin.",
)
def delete_device(
    device_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    _set_custom_headers(response)
    device_service.delete_device(db, device_id)


@router.get(
    "/{device_id}/loans",
    response_model=list[LoanResponse],
    summary="Historial de préstamos de un dispositivo",
    description="Lista todos los préstamos (históricos) asociados a un dispositivo específico.",
)
def get_device_loans(device_id: int, response: Response, db: Session = Depends(get_db)):
    _set_custom_headers(response)
    return loan_service.get_loans_by_device(db, device_id)