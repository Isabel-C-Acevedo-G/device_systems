"""Lógica de negocio para la gestión de usuarios, usando SQLAlchemy."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserPatch, UserUpdate


def list_users(
    db: Session,
    role: str | None = None,
    is_active: bool | None = None,
) -> list[User]:
    query = db.query(User)
    if role is not None:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.order_by(User.name).all()


def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    if get_user_by_email(db, user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El correo '{user.email}' ya se encuentra registrado.",
        )
    new_user = User(
        name=user.name,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def replace_user(db: Session, user_id: int, user: UserUpdate) -> User:
    existing = get_user(db, user_id)
    duplicate = get_user_by_email(db, user.email)
    if duplicate is not None and duplicate.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El correo '{user.email}' ya se encuentra registrado.",
        )
    existing.name = user.name
    existing.email = user.email
    existing.role = user.role
    existing.is_active = user.is_active
    db.commit()
    db.refresh(existing)
    return existing


def update_user_partial(db: Session, user_id: int, user: UserPatch) -> User:
    existing = get_user(db, user_id)
    data = user.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar.",
        )
    if "email" in data:
        duplicate = get_user_by_email(db, data["email"])
        if duplicate is not None and duplicate.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El correo '{data['email']}' ya se encuentra registrado.",
            )
    for field, value in data.items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


def delete_user(db: Session, user_id: int) -> None:
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()