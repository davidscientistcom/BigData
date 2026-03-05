# API de Usuarios — Curso Testing

API REST de ejemplo construida con **FastAPI** que demuestra un **CRUD completo** sobre usuarios, con una arquitectura modular basada en el **patrón Repository**.



## Estructura del proyecto

```
Curso Testing/
├── app/
│   ├── main.py                ← Punto de entrada FastAPI + configuración Swagger
│   ├── models/
│   │   └── user.py            ← Modelos Pydantic (UserCreate, UserUpdate, UserResponse)
│   ├── repositories/
│   │   ├── base.py            ← Interfaz abstracta (patrón Repository)
│   │   └── memory.py          ← Implementación en RAM con diccionario
│   ├── services/
│   │   └── user_service.py    ← Lógica de negocio
│   └── routers/
│       └── users.py           ← Endpoints REST (CRUD + búsqueda)
├── tests/
│   └── users.http             ← Fichero de pruebas REST Client
├── requirements.txt
└── README.md
```

### ¿Por qué esta estructura?

Cada carpeta tiene una **responsabilidad única**:

| Carpeta | Responsabilidad |
|---------|----------------|
| `models/` | Define la **forma de los datos** (qué campos tiene un usuario, qué validaciones aplican). Usa Pydantic. |
| `repositories/` | Se encarga de **guardar y recuperar datos**. Hoy en RAM, mañana en base de datos. |
| `services/` | Contiene la **lógica de negocio**. Orquesta llamadas al repositorio. |
| `routers/` | Define los **endpoints HTTP** (las URLs de la API). Recibe peticiones y delega al servicio. |

El flujo de una petición es siempre:

```
HTTP Request → Router → Service → Repository → Almacenamiento (RAM)
HTTP Response ← Router ← Service ← Repository ← Almacenamiento (RAM)
```



## Arquitectura: Patrón Repository

El corazón de esta arquitectura es el **patrón Repository**, que **desacopla la lógica de negocio del mecanismo de persistencia**.

```
Router  →  Service  →  UserRepository (interfaz abstracta / ABC)
                              │
                              ├── MemoryUserRepository   ←  HOY (diccionario en RAM)
                              ├── SQLiteUserRepository   ←  MAÑANA (sin tocar nada más)
                              └── PostgresUserRepository ←  FUTURO
```

### ¿Qué significa esto en la práctica?

1. En `repositories/base.py` definimos una **interfaz** (clase abstracta con `ABC`) que dice **qué operaciones** debe soportar cualquier repositorio: `create`, `get_by_id`, `get_all`, `update`, `delete`, `search`.

2. En `repositories/memory.py` implementamos esa interfaz usando un **diccionario de Python** como almacenamiento en RAM.

3. El servicio (`services/user_service.py`) trabaja contra la **interfaz**, no contra la implementación concreta. No sabe ni le importa si los datos están en un dict, en SQLite o en la nube.

4. Si mañana queremos usar **SQLite**, solo hay que:
   - Crear `repositories/sqlite.py` que herede de `UserRepository`.
   - Cambiar **una línea** en `routers/users.py` para instanciar el nuevo repositorio.
   - Los endpoints y la lógica de negocio **no se tocan**.


## Endpoints disponibles

| Método   | Ruta              | Descripción                                    | Código éxito |
|----------|-------------------|------------------------------------------------|:------------:|
| `GET`    | `/`               | Health check / bienvenida                      | 200          |
| `POST`   | `/users/`         | Crear un nuevo usuario                         | 201          |
| `GET`    | `/users/`         | Listar todos los usuarios                      | 200          |
| `GET`    | `/users/{id}`     | Obtener un usuario por su ID                   | 200          |
| `GET`    | `/users/search`   | Buscar usuarios por múltiples criterios        | 200          |
| `PUT`    | `/users/{id}`     | Actualizar parcialmente un usuario             | 200          |
| `DELETE` | `/users/{id}`     | Eliminar un usuario                            | 204          |

### Parámetros de búsqueda (`GET /users/search`)

Todos los filtros son **opcionales** y se combinan con **AND lógico**:

| Parámetro | Tipo  | Descripción                                         | Ejemplo                    |
|-----------|-------|-----------------------------------------------------|----------------------------|
| `name`    | `str` | Búsqueda parcial en el nombre (case-insensitive)    | `?name=ana`                |
| `min_age` | `int` | Edad mínima (inclusive)                              | `?min_age=18`              |
| `max_age` | `int` | Edad máxima (inclusive)                              | `?max_age=30`              |
| `email`   | `str` | Búsqueda parcial en el email (case-insensitive)     | `?email=example.com`       |
| `city`    | `str` | Búsqueda parcial en la ciudad (case-insensitive)    | `?city=madrid`             |

**Ejemplos combinados:**
- `/users/search?city=madrid` → usuarios de Madrid
- `/users/search?min_age=18&max_age=30` → usuarios entre 18 y 30 años
- `/users/search?name=ana&city=madrid` → "Ana" que viva en Madrid



## Instalación y ejecución

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Arrancar el servidor

```bash
uvicorn app.main:app --reload
```

- `app.main` → módulo Python (fichero `app/main.py`)
- `app` → variable que contiene la instancia de FastAPI
- `--reload` → reinicia automáticamente al guardar cambios (solo para desarrollo)

### 3. Acceder a la documentación

| URL | Descripción |
|-----|-------------|
| http://127.0.0.1:8000/docs | **Swagger UI** — documentación interactiva (puedes probar los endpoints) |
| http://127.0.0.1:8000/redoc | **ReDoc** — documentación alternativa más visual |
| http://127.0.0.1:8000/openapi.json | Esquema OpenAPI en formato JSON |



## Fichero de pruebas REST

En lugar de usar Postman, usamos un fichero `.http` que se ejecuta directamente desde VS Code con la extensión **REST Client**.

### Configuración

1. Instala la extensión **REST Client** en VS Code (`humao.rest-client`).
2. Arranca el servidor (`uvicorn app.main:app --reload`).
3. Abre el fichero `tests/users.http`.
4. Verás **"Send Request"** encima de cada petición → haz clic para ejecutarla.
5. La respuesta aparecerá en un panel a la derecha.

### ¿Qué pruebas incluye?

El fichero `tests/users.http` contiene pruebas organizadas por secciones:

| Sección | Qué prueba |
|---------|------------|
| **Health check** | Que la API está activa |
| **Crear usuarios** | 5 usuarios válidos + 2 casos de error (edad negativa, sin nombre) |
| **Listar todos** | Que devuelve la lista completa |
| **Obtener por ID** | Usuarios existentes + usuario inexistente (404) |
| **Búsqueda con filtros** | Por nombre, ciudad, rango de edad, email y combinaciones |
| **Actualizar** | Actualización parcial (solo edad, nombre+ciudad) + verificación + 404 |
| **Eliminar** | Eliminación + doble eliminación (404) + verificar que desaparece |
| **Verificaciones finales** | Estado consistente tras todas las operaciones |



##  Notas importantes

- **Los datos se pierden al reiniciar el servidor** porque se almacenan en memoria RAM (diccionario de Python). Esto es intencional para esta fase del curso.
- FastAPI genera automáticamente la documentación de Swagger a partir de los **modelos Pydantic** y las **descripciones** que hemos puesto en los endpoints.
- La validación de datos (edad entre 0-150, nombre obligatorio, etc.) la hace **Pydantic automáticamente**. Si el cliente envía datos inválidos, FastAPI devuelve un error 422 con los detalles.
