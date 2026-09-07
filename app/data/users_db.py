"""Simulación de base de datos en memoria para el recurso 'users'."""

users_db: list[dict] = [
    {
        "id": 1,
        "name": "Facundo Cruz",
        "email": "facundo.cruz@example.com",
        "role": "admin",
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Carlos Vargas",
        "email": "carlos.vargas@example.com",
        "role": "support",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Felipe Acevedo",
        "email": "felipe.acevedo@example.com",
        "role": "user",
        "is_active": False,
    },
]