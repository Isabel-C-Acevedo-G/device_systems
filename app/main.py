from fastapi import FastAPI

from app.routes.user_routes import router as user_router

app = FastAPI(title="Device Systems API")

app.include_router(user_router)


@app.get("/", tags=["Root"])
def read_root() -> dict:
    return {"message": "Bienvenido a Device Systems API "}