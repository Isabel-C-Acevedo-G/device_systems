"""Punto de entrada principal de device_systems."""

from fastapi import FastAPI

from app.database.connection import Base, engine
from app.models import User, Device, Loan  # noqa: F401
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios, dispositivos y préstamos del sistema device_systems, con persistencia en base de datos mediante SQLAlchemy y migraciones con Alembic",
    version="4.0.0",
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"])
def read_root() -> dict:
    return {"message": "Bienvenido a Device Systems API 🚀"}