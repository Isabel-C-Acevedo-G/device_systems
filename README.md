# Device Systems API

API REST desarrollada con **FastAPI**, **SQLAlchemy**, **Alembic** y una capa completa de **seguridad** (OAuth2, JWT, hash de contraseñas, roles, CORS, middleware y rate limiting).

## Descripción general

`device_systems` gestiona usuarios, dispositivos y préstamos, con persistencia real en base de datos, relaciones entre modelos, migraciones versionadas, y autenticación/autorización completa por roles.

## Tecnologías utilizadas

- Python 3.14
- FastAPI
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- SQLite
- passlib (bcrypt)
- python-jose (JWT)
- slowapi (rate limiting)
- uv (gestor de dependencias)

## Instalación de dependencias

```bash
uv sync
```

## Ejecución del servidor

```bash
uv run uvicorn app.main:app --reload
```

Documentación interactiva:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Estructura del proyecto
device_systems/
├── app/
│ ├── main.py
│ ├── auth/
│ │ ├── auth_routes.py
│ │ ├── auth_service.py
│ │ └── security.py
│ ├── database/connection.py
│ ├── models/ (user_model.py, device_model.py, loan_model.py)
│ ├── schemas/ (user_schema.py, device_schema.py, loan_schema.py, auth_schema.py)
│ ├── routes/ (user_routes.py, device_routes.py, loan_routes.py)
│ ├── services/ (user_service.py, device_service.py, loan_service.py)
│ ├── dependencies/ (database_dependency.py, auth_dependency.py)
│ └── middlewares/request_middleware.py
├── alembic/versions/
├── alembic.ini
├── requirements.txt
├── .env / .env.example
└── README.md

## Recurso nuevo: /auth

| Método | Ruta | Descripción | Límite |
|---|---|---|---|
| POST | /auth/register | Registra un usuario nuevo con contraseña segura (hash) | 3/minuto |
| POST | /auth/login | Autentica y devuelve un token JWT | 5/minuto |
| GET | /auth/me | Devuelve los datos del usuario autenticado actual | — |

## Autenticación y seguridad implementadas

- **Hash de contraseñas con passlib (bcrypt)**: las contraseñas nunca se guardan en texto plano, se almacenan como `hashed_password`.
- **JWT (JSON Web Token)**: al hacer login exitoso, se genera un token firmado que el cliente envía en `Authorization: Bearer <token>` para acceder a rutas protegidas.
- **Validaciones avanzadas con Pydantic v2**: `UserRegister` usa `field_validator` para exigir contraseña con mínimo 8 caracteres, mayúscula, minúscula, número y sin espacios.

## Rutas protegidas por rol

| Ruta | Método | Protección |
|---|---|---|
| /users | GET | Usuario autenticado |
| /users/{user_id} | GET | Usuario autenticado |
| /devices | POST | Admin o support |
| /devices/{device_id} | PUT | Admin o support |
| /devices/{device_id} | DELETE | Admin |
| /loans | POST | Usuario autenticado |
| /loans/{loan_id}/return | PATCH | Admin o support |
| /loans/details | GET | Admin o support |

Sin token válido → `401 Unauthorized`. Con token válido pero sin el rol requerido → `403 Forbidden`.

## Middleware personalizado

`RequestMiddleware` se ejecuta en todas las peticiones y agrega:
- `X-App-Name: device_systems`
- `X-Process-Time`: tiempo de respuesta en segundos
- `X-Request-ID`: identificador único de la petición

## CORS configurado

```python
allow_origins=["http://localhost:5173", "http://localhost:3000"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

### ¿Por qué no usar `allow_origins=["*"]` en producción con credenciales?

Cuando `allow_credentials=True`, el navegador exige orígenes explícitos. Usar `"*"` junto con credenciales expondría la API a que cualquier sitio web pueda enviar peticiones autenticadas en nombre del usuario (riesgo de CSRF/robo de sesión). Por eso siempre se listan solo los dominios verificados del frontend real.

## Rate limiting

Implementado con **slowapi**:
- `POST /auth/register`: 3 peticiones por minuto
- `POST /auth/login`: 5 peticiones por minuto

Al superar el límite, la API responde `429 Too Many Requests`.

## Migración Alembic

```bash
alembic revision --autogenerate -m "add authentication fields to users"
alembic upgrade head
```

## Capturas de evidencia

![Registro de usuario](Imagenes/registro-usuario.png)

![Login y token generado](Imagenes/login-token.png)

![Consulta /auth/me](Imagenes/auth-me.png)

![Acceso sin token - 401](Imagenes/sin-token-401.png)

![Rate limiting activado - 429, con cabeceras del middleware visibles](Imagenes/rate-limiting-429.png)

## Reflexión final sobre la importancia de la seguridad en APIs REST

Esta actividad me mostró que una API funcional no es suficiente si no está protegida. Aprendí que las contraseñas nunca deben guardarse en texto plano, y que el hash (con passlib/bcrypt) permite verificar una contraseña sin necesidad de almacenarla de forma reversible. JWT me permitió entender cómo un servidor puede "recordar" que un usuario inició sesión sin guardar estado en el servidor, ya que toda la información viaja firmada dentro del token. Proteger cada ruta según el rol del usuario (admin, support, user) me enseñó la diferencia entre autenticación (quién eres) y autorización (qué puedes hacer). También comprendí la importancia del middleware para tener trazabilidad de cada petición, y por qué CORS y el rate limiting son defensas esenciales contra el mal uso de una API pública.