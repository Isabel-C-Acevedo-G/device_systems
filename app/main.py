"""Punto de entrada principal de device_systems."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.database.connection import Base, engine
from app.middlewares.request_middleware import RequestMiddleware
from app.models import User, Device, Loan  # noqa: F401
from app.auth.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos",
    version="5.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(RequestMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"])
def read_root() -> dict:
    return {"message": "Bienvenido a Device Systems API 🚀"}