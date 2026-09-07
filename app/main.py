"""Punto de entrada principal de device_systems."""

from fastapi import FastAPI

from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems",
    version="2.0.0",
)

app.include_router(user_router)

@app.get("/", tags=["Root"])
def read_root() -> dict:
    return {"message": "Bienvenido a Device Systems API 🚀"}