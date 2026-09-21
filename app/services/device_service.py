"""Lógica de negocio para la gestión de dispositivos."""

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate


def list_devices(
    db: Session,
    device_type: str | None = None,
    is_available: bool | None = None,
    brand: str | None = None,
    search: str | None = None,
) -> list[Device]:
    query = db.query(Device)
    if device_type is not None:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand is not None:
        query = query.filter(Device.brand == brand)
    if search is not None:
        term = f"%{search}%"
        query = query.filter(
            or_(Device.name.ilike(term), Device.serial_number.ilike(term))
        )
    return query.order_by(Device.name).all()


def get_device(db: Session, device_id: int) -> Device:
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )
    return device


def get_device_by_serial(db: Session, serial_number: str) -> Device | None:
    return db.query(Device).filter(Device.serial_number == serial_number).first()


def create_device(db: Session, device: DeviceCreate) -> Device:
    existing_device = get_device_by_serial(db, device.serial_number)
    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El número de serie '{device.serial_number}' ya está registrado.",
        )
    new_device = Device(**device.model_dump())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


def replace_device(db: Session, device_id: int, device: DeviceCreate) -> Device:
    existing = get_device(db, device_id)
    duplicate = get_device_by_serial(db, device.serial_number)
    if duplicate and duplicate.id != device_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El número de serie '{device.serial_number}' ya está registrado.",
        )
    for field, value in device.model_dump().items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


def update_device_partial(db: Session, device_id: int, device: DeviceUpdate) -> Device:
    existing = get_device(db, device_id)
    data = device.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar.",
        )
    if "serial_number" in data:
        duplicate = get_device_by_serial(db, data["serial_number"])
        if duplicate and duplicate.id != device_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El número de serie '{data['serial_number']}' ya está registrado.",
            )
    for field, value in data.items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


def delete_device(db: Session, device_id: int) -> None:
    device = get_device(db, device_id)
    db.delete(device)
    db.commit()