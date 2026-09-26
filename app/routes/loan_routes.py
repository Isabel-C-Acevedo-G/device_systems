"""Endpoints REST para el recurso 'loans'."""

from typing import Literal

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanResponse
from app.services import loan_service

router = APIRouter(prefix="/loans", tags=["Loans"])


def _set_custom_headers(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "5.0"


@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Listar préstamos con detalle (join)",
    description="Lista préstamos con la información completa del usuario y el dispositivo. Requiere rol admin o support.",
)
def get_loans_with_details(
    response: Response,
    status_filter: Literal["active", "returned", "overdue"] | None = None,
    user_email: str | None = None,
    device_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    _set_custom_headers(response)
    return loan_service.list_loans_with_details(
        db, status_filter=status_filter, user_email=user_email, device_type=device_type
    )


@router.get(
    "",
    response_model=list[LoanResponse],
    summary="Listar préstamos",
    description="Lista los préstamos registrados, con filtro opcional por estado.",
)
def get_loans(
    response: Response,
    status_filter: Literal["active", "returned", "overdue"] | None = None,
    db: Session = Depends(get_db),
):
    _set_custom_headers(response)
    return loan_service.list_loans(db, status_filter=status_filter)


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Consultar préstamo por ID",
    description="Devuelve un préstamo específico. Lanza 404 si no existe.",
)
def get_loan_by_id(loan_id: int, response: Response, db: Session = Depends(get_db)):
    _set_custom_headers(response)
    return loan_service.get_loan(db, loan_id)


@router.post(
    "",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Registra un préstamo, validando que el usuario exista, el dispositivo exista y esté disponible. Requiere autenticación.",
)
def create_loan(
    loan: LoanCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    _set_custom_headers(response)
    return loan_service.create_loan(db, loan)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Marca un préstamo como devuelto y libera el dispositivo asociado. Requiere rol admin o support.",
)
def return_loan(
    loan_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    _set_custom_headers(response)
    return loan_service.return_loan(db, loan_id)