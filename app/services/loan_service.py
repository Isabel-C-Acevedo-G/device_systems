"""Lógica de negocio para la gestión de préstamos."""

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate


def list_loans(db: Session, status_filter: str | None = None) -> list[Loan]:
    query = db.query(Loan)
    if status_filter is not None:
        query = query.filter(Loan.status == status_filter)
    return query.order_by(Loan.loan_date.desc()).all()


def get_loan(db: Session, loan_id: int) -> Loan:
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado",
        )
    return loan


def create_loan(db: Session, loan: LoanCreate) -> Loan:
    user = db.query(User).filter(User.id == loan.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )

    if not device.is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El dispositivo no está disponible para préstamo",
        )

    new_loan = Loan(
        user_id=loan.user_id,
        device_id=loan.device_id,
        status="active",
    )
    device.is_available = False

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan


def return_loan(db: Session, loan_id: int) -> Loan:
    loan = get_loan(db, loan_id)

    if loan.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este préstamo ya fue devuelto anteriormente",
        )

    loan.status = "returned"
    loan.return_date = datetime.utcnow()
    loan.device.is_available = True

    db.commit()
    db.refresh(loan)
    return loan

def list_loans_with_details(
    db: Session,
    status_filter: str | None = None,
    user_email: str | None = None,
    device_type: str | None = None,
) -> list[Loan]:
    query = db.query(Loan).join(User).join(Device)
    if status_filter is not None:
        query = query.filter(Loan.status == status_filter)
    if user_email is not None:
        query = query.filter(User.email.ilike(f"%{user_email}%"))
    if device_type is not None:
        query = query.filter(Device.device_type == device_type)
    return query.order_by(Loan.loan_date.desc()).all()


def get_loans_by_user(db: Session, user_id: int) -> list[Loan]:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return (
        db.query(Loan)
        .filter(Loan.user_id == user_id)
        .order_by(Loan.loan_date.desc())
        .all()
    )


def get_loans_by_device(db: Session, device_id: int) -> list[Loan]:
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )
    return (
        db.query(Loan)
        .filter(Loan.device_id == device_id)
        .order_by(Loan.loan_date.desc())
        .all()
    )
