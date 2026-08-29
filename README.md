# Device Systems API

API REST desarrollada con **FastAPI** para la gestión del recurso `users`,
como parte de la actividad **GA1-220501096-01-AA1-EV07 – Fundamentos de FastAPI:
API REST para Gestión de Usuarios**.

## Descripción de la aplicación

La carpeta `device_systems` Me permite administrar usuarios desde una API REST, aplicando
validaciones con Pydantic v2, parámetros de ruta y consulta, cabeceras HTTP
personalizadas y respuestas estructuradas con Response Models.

## Instalación de dependencias

```bash
uv sync
```

## Ejecución del servidor

```bash
uv run uvicorn app.main:app --reload
```

Documentación interactiva (Swagger UI): http://127.0.0.1:8000/docs

## Tabla de endpoints

| Método | Ruta              | Descripción                                        |
|--------|-------------------|-----------------------------------------------------|
| GET    | /users            | Lista usuarios (filtros opcionales: `role`, `is_active`) |
| GET    | /users/{user_id}  | Consulta un usuario específico por su ID            |
| POST   | /users            | Registra un nuevo usuario                           |

## Cabeceras HTTP personalizadas

Todas las respuestas de los endpoints anteriores incluyen:

- `X-App-Name: device_systems`
- `X-API-Version: 1.0`

## Capturas de Swagger UI

![Vista general de Swagger UI](images/swagger-general.png)

## Evidencia de pruebas GET /users

Se probó el endpoint sin filtros (devuelve todos los usuarios) y con los filtros
opcionales `role` e `is_active`, confirmando que las cabeceras personalizadas
aparecen en la respuesta.

![GET /users - lista completa](images/get-users.png)

## Evidencia de pruebas GET /users/{user_id}

Se probó con un ID existente, obteniendo una respuesta 200 con los datos del
usuario correspondiente.

![GET /users/{user_id} - caso exitoso](images/get-users-por-id.png)

## Evidencia de pruebas POST /users

Se probó la creación exitosa de un usuario nuevo (respuesta 201 con el ID
autoincrementado).

![POST /users - creación exitosa](images/post-users-exitoso.png)

## Evidencia de validaciones y errores

- **Correo duplicado (400):** al intentar registrar un usuario con un email ya
  existente en la base de datos simulada, la API responde con un error 400.

![POST /users - correo duplicado](images/post-users-correo-duplicado.png)

- **Rol inválido (422):** al enviar un rol fuera de los valores permitidos
  (`admin`, `support`, `user`), Pydantic rechaza automáticamente la petición.

![POST /users - rol inválido](images/post-users-rol-invalido.png)



## Reflexión sobre el uso de FastAPI para construir APIs REST

En esta actividad, lo que más me costó entender fue la
diferencia entre Path Parameters y Query Parameters, además de comprender
bien cómo funciona Pydantic y algunas partes del código en general. Con la
práctica y probando cada endpoint en Swagger UI, fui entendiendo cuándo se
usa cada uno: los Path Parameters para pedir un recurso específico (como un
usuario por su ID) y los Query Parameters para filtrar resultados.
También tuve errores que tuve que aprender a
identificar y corregir por mí misma, como una coma que faltaba entre
`"support"` y `"user"` en la lista de roles permitidos, y un error de
escritura donde el campo `role` quedó mal escrito como `rolle`. Estos
errores me enseñaron a leer con más atención los mensajes de error que
muestra la terminal.

Yo considero que una API REST es fundamental en el desarrollo de software
porque permite que diferentes aplicaciones o sistemas se comuniquen entre
sí a través de internet. Por ejemplo, cuando uso la aplicación de mi banco
en el celular, esta constantemente está enviando y recibiendo información
del servidor del banco mediante peticiones como las que construí en esta
actividad (GET y POST). Esto me ayudó a entender que, detrás de cada app
que uso a diario, hay una API trabajando para conectar los datos con lo
que veo en pantalla.