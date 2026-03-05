"""
Router de usuarios — Endpoints de la API REST.

Aquí definimos las rutas HTTP que expone nuestra API.
Cada función se conecta con el servicio de usuarios para
realizar la operación correspondiente.

╔══════════════════════════════════════════════════════════════════╗
║  CONCEPTOS CLAVE DE FASTAPI USADOS AQUÍ                        ║
║                                                                  ║
║  · APIRouter: permite modularizar los endpoints en ficheros     ║
║    separados. Luego se incluyen en la app con include_router(). ║
║                                                                  ║
║  · Depends(): sistema de inyección de dependencias de FastAPI.  ║
║    Usamos una función `get_user_service()` que devuelve la      ║
║    instancia del servicio. Si mañana cambiamos el repositorio,  ║
║    solo tocamos esa función.                                    ║
║                                                                  ║
║  · response_model: indica a FastAPI qué modelo Pydantic usar   ║
║    para serializar la respuesta y documentar Swagger.           ║
║                                                                  ║
║  · status_code: código HTTP que se devuelve cuando todo va bien.║
║                                                                  ║
║  · Query(): parámetros de query string con validación y docs.   ║
║                                                                  ║
║  · HTTPException: para devolver errores con código HTTP.        ║
║                                                                  ║
║  · tags: agrupa los endpoints en secciones dentro de Swagger.   ║
╚══════════════════════════════════════════════════════════════════╝
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.models.user import UserCreate, UserUpdate, UserResponse
from app.repositories.memory import MemoryUserRepository
from app.services.user_service import UserService


# ──────────────────────────────────────────────────────────────────
# Instancias compartidas (singleton durante la vida de la app)
# ──────────────────────────────────────────────────────────────────

# Creamos UNA sola instancia del repositorio en memoria.
# Todos los endpoints compartirán esta misma instancia,
# por lo que los datos persisten mientras el servidor esté corriendo.
_repository = MemoryUserRepository()
_service = UserService(repository=_repository)


def get_user_service() -> UserService:
    """
    Función de dependencia para FastAPI.

    FastAPI llama a esta función cada vez que un endpoint
    necesita el servicio (gracias a `Depends(get_user_service)`).

    ¿Por qué no usar directamente _service en los endpoints?
    Porque usar Depends() nos permite:
      · Reemplazar fácilmente el servicio en tests (override).
      · Cambiar la implementación sin tocar los endpoints.
    """
    return _service


# ──────────────────────────────────────────────────────────────────
# Creamos el router con prefijo /users y tag para Swagger
# ──────────────────────────────────────────────────────────────────

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"],
    responses={
        404: {"description": "Usuario no encontrado"},
    },
)


# ══════════════════════════════════════════════════════════════════
#  ENDPOINTS CRUD
# ══════════════════════════════════════════════════════════════════


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="""
    Crea un nuevo usuario en el sistema.
    
    El servidor asigna automáticamente un **id único** al usuario.
    
    - **name**: nombre completo (obligatorio)
    - **age**: edad entre 0 y 150 (obligatorio)
    - **email**: correo electrónico (opcional)
    - **city**: ciudad de residencia (opcional)
    """,
)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Endpoint POST /users/ — Crear usuario."""
    return service.create_user(user_data)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar todos los usuarios",
    description="Devuelve la lista completa de usuarios registrados.",
)
def get_all_users(
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    """Endpoint GET /users/ — Listar todos."""
    return service.get_all_users()


@router.get(
    "/search",
    response_model=list[UserResponse],
    summary="Buscar usuarios por criterios",
    description="""
    Busca usuarios aplicando **uno o varios filtros** simultáneamente.
    
    Los filtros se combinan con **AND lógico**: el usuario debe 
    cumplir TODOS los criterios activos.
    
    Las búsquedas de texto son **parciales** y **case-insensitive**:
    buscar `name=ana` encontrará "Ana García" y "Mariana López".
    
    Ejemplos de uso:
    - `/users/search?city=madrid` → usuarios de Madrid
    - `/users/search?min_age=18&max_age=30` → usuarios entre 18 y 30 años
    - `/users/search?name=ana&city=madrid` → "Ana" que viva en Madrid
    """,
)
def search_users(
    name: Optional[str] = Query(
        default=None,
        description="Filtrar por nombre (búsqueda parcial, case-insensitive)",
        examples=["Ana"],
    ),
    min_age: Optional[int] = Query(
        default=None,
        ge=0,
        description="Edad mínima (inclusive)",
        examples=[18],
    ),
    max_age: Optional[int] = Query(
        default=None,
        le=150,
        description="Edad máxima (inclusive)",
        examples=[30],
    ),
    email: Optional[str] = Query(
        default=None,
        description="Filtrar por email (búsqueda parcial, case-insensitive)",
        examples=["example.com"],
    ),
    city: Optional[str] = Query(
        default=None,
        description="Filtrar por ciudad (búsqueda parcial, case-insensitive)",
        examples=["Madrid"],
    ),
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    """Endpoint GET /users/search — Búsqueda con filtros."""
    return service.search_users(
        name=name,
        min_age=min_age,
        max_age=max_age,
        email=email,
        city=city,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener un usuario por ID",
    description="Devuelve los datos de un usuario concreto dado su **id**.",
    responses={
        200: {"description": "Usuario encontrado"},
        404: {"description": "Usuario no encontrado"},
    },
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Endpoint GET /users/{user_id} — Obtener por id."""
    user = service.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado",
        )
    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar un usuario (parcial)",
    description="""
    Actualiza **parcialmente** un usuario existente.
    
    Solo se modifican los campos que envíes en el body.
    Los campos que no envíes se mantienen con su valor actual.
    
    Ejemplo: enviar `{"age": 30}` solo cambia la edad.
    """,
    responses={
        200: {"description": "Usuario actualizado correctamente"},
        404: {"description": "Usuario no encontrado"},
    },
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Endpoint PUT /users/{user_id} — Actualizar parcialmente."""
    user = service.update_user(user_id, user_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado",
        )
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario",
    description="Elimina un usuario del sistema dado su **id**.",
    responses={
        204: {"description": "Usuario eliminado correctamente"},
        404: {"description": "Usuario no encontrado"},
    },
)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> None:
    """
    Endpoint DELETE /users/{user_id} — Eliminar usuario.

    Devuelve 204 No Content si se eliminó correctamente.
    El código 204 indica éxito pero sin cuerpo de respuesta.
    """
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado",
        )
    # 204 → no retornamos body
