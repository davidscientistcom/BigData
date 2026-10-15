"""
Router de coches — Endpoints de la API REST para la entidad Coche.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.coche import CocheCreate, CocheUpdate, CocheResponse
from app.repositories.memory import MemoryCocheRepository, MemoryUserRepository

# Ojo: Para utilizar la misma instancia en memoria de usuarios, deberíamos 
# importarla desde el router de users o crear un singleton común.
# Para este ejemplo de Coche usaremos instancias nuevas en memoria por simplicidad
# y para no romper el router original sin modificar mucho.
# En un entorno real (con DB) se instanciarían conexiones de igual manera.
from app.routers.users import _repository as shared_user_repository
from app.services.coche_service import CocheService

# Creamos UNA instancia de repositorio en memoria para los coches
_coche_repository = MemoryCocheRepository()
# Reutilizamos el repositorio en memoria de usuarios para que compartan los mismos datos en RAM
_coche_service = CocheService(coche_repository=_coche_repository, user_repository=shared_user_repository)


def get_coche_service() -> CocheService:
    return _coche_service


router = APIRouter(
    prefix="/coches",
    tags=["Coches"],
    responses={
        404: {"description": "Coche no encontrado"},
    },
)

@router.post(
    "/",
    response_model=CocheResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo coche",
)
def create_coche(
    coche_data: CocheCreate,
    service: CocheService = Depends(get_coche_service),
) -> CocheResponse:
    """Crea un nuevo coche."""
    try:
        return service.create_coche(coche_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=list[CocheResponse],
    summary="Listar todos los coches",
)
def get_all_coches(
    service: CocheService = Depends(get_coche_service),
) -> list[CocheResponse]:
    """Lista todos los coches."""
    return service.get_all_coches()


@router.get(
    "/user/{user_id}",
    response_model=list[CocheResponse],
    summary="Listar coches por usuario",
)
def get_coches_by_user(
    user_id: int,
    service: CocheService = Depends(get_coche_service),
) -> list[CocheResponse]:
    """Devuelve los coches asociados a un ID de usuario."""
    try:
        return service.get_coches_by_user(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/{coche_id}",
    response_model=CocheResponse,
    summary="Obtener un coche por ID",
)
def get_coche(
    coche_id: int,
    service: CocheService = Depends(get_coche_service),
) -> CocheResponse:
    coche = service.get_coche(coche_id)
    if coche is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coche con id {coche_id} no encontrado",
        )
    return coche


@router.put(
    "/{coche_id}",
    response_model=CocheResponse,
    summary="Actualizar un coche (parcial)",
)
def update_coche(
    coche_id: int,
    coche_data: CocheUpdate,
    service: CocheService = Depends(get_coche_service),
) -> CocheResponse:
    try:
        coche = service.update_coche(coche_id, coche_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    if coche is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coche con id {coche_id} no encontrado",
        )
    return coche


@router.delete(
    "/{coche_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un coche",
)
def delete_coche(
    coche_id: int,
    service: CocheService = Depends(get_coche_service),
) -> None:
    deleted = service.delete_coche(coche_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coche con id {coche_id} no encontrado",
        )
