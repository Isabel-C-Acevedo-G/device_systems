# Device Systems API

API REST con **FastAPI**, **SQLAlchemy** y **Alembic** — actividad **EV10**: migraciones, asociaciones de modelos y consultas con joins.

## Descripción

device_systems - ahora gestiona ,usuarios, dispositivos y préstamos, con relaciones entre tablas (User , Loan , Device), migraciones versionadas con Alembic, y consultas avanzadas con joins y filtros.

## Tecnologías

Python 3.14 · FastAPI · SQLAlchemy 2.0 · Alembic · Pydantic v2 · SQLite · uv

## Estructura del proyecto
device_systems/
├── app/
│ ├── main.py
│ ├── database/connection.py
│ ├── models/ (user_model.py, device_model.py, loan_model.py)
│ ├── schemas/ (user_schema.py, device_schema.py, loan_schema.py)
│ ├── routes/ (user_routes.py, device_routes.py, loan_routes.py)
│ ├── services/ (user_service.py, device_service.py, loan_service.py)
│ └── dependencies/database_dependency.py
├── alembic/versions/
├── alembic.ini
├── requirements.txt
└── README.md

## Diferencia entre modelo SQLAlchemy y schema Pydantic

El modelo (models/) define la tabla en la base de datos (columnas, nullable, unique, ForeignKey). El schema (schemas/) define cómo se validan y muestran los datos en la API. from_attributes = True conecta ambos, permitiendo que Pydantic lea directamente los objetos de SQLAlchemy.

## Asociaciones entre modelos

- User.loans - Loan.user (One-to-Many)
- Device.loans - Loan.device (One-to-Many)
- Loan.user_id y Loan.device_id son ForeignKey , garantizando integridad referencial.

## Migraciones con Alembic

![alembic init](Imagenes/alembic-init.png)

![migración generada](Imagenes/alembic-migracion.png)

![alembic upgrade head](Imagenes/alembic-upgrade.png)

## Estructura de tablas generadas

![tablas](Imagenes/estructura-tablas.png)

## Swagger UI

![swagger general](Imagenes/swagger-general-ev10.png)

## Evidencia: creación de usuario, dispositivo y préstamo

![crear préstamo](Imagenes/crear-usuario-dispositivo-prestamo.png)

## Evidencia: consultas con joins

![loans details](Imagenes/loans-details-join.png)

## Evidencia: filtros aplicados

![filtro status](Imagenes/filtro-status.png)

## Evidencia: devolución de dispositivo

![devolución](Imagenes/devolucion-prestamo.png)

## Reflexión final

Esta actividad me permitió entender cómo evoluciona una API desde una sola tabla hacia un sistema relacional real. Aprendí que Alembic versiona los cambios de la base de datos igual que Git versiona el código, permitiendo aplicar y revertir cambios estructurales de forma controlada. Las relaciones (relationship, back_populates, ForeignKey) muestra cómo conectar las tablas sin perder integridad referencial, y los joins me dejaron combinar información de usuarios, dispositivos y préstamos en una sola respuesta. Creo que estas herramientas son esenciales para construir APIs que reflejen relaciones del mundo real, como un sistema de préstamos.