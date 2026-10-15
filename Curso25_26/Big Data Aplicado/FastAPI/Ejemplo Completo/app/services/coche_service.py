"""
Servicio de coches — Capa de lógica de negocio.
"""

from typing import Optional

from app.models.coche import CocheCreate, CocheUpdate, CocheResponse
from app.repositories.base import CocheRepository, UserRepository


class CocheService:
    """
    Orquesta las operaciones sobre coches delegando
    la persistencia al repositorio inyectado.
    """

    def __init__(self, coche_repository: CocheRepository, user_repository: UserRepository) -> None:
        """
        Recibe el repositorio de coches y el de usuarios por inyección de dependencias.
        El de usuarios se usa para validar que un usuario existe antes de asignarle un coche.
        """
        self._coche_repo = coche_repository
        self._user_repo = user_repository

    def create_coche(self, coche_data: CocheCreate) -> CocheResponse:
        """Crea un coche nuevo tras validar que el usuario existe."""
        user = self._user_repo.get_by_id(coche_data.user_id)
        if not user:
            raise ValueError(f"El usuario con id {coche_data.user_id} no existe.")
        
        return self._coche_repo.create(coche_data)

    def get_coche(self, coche_id: int) -> Optional[CocheResponse]:
        """Obtiene un coche por id."""
        return self._coche_repo.get_by_id(coche_id)

    def get_coches_by_user(self, user_id: int) -> list[CocheResponse]:
        """Devuelve todos los coches que pertenecen a un usuario."""
        # Se puede validar aquí si el usuario existe para lanzar 404
        # o devolver lista vacía si no existe / no tiene coches
        user = self._user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"El usuario con id {user_id} no existe.")
            
        return self._coche_repo.get_by_user_id(user_id)

    def get_all_coches(self) -> list[CocheResponse]:
        """Devuelve la lista completa de coches."""
        return self._coche_repo.get_all()

    def update_coche(self, coche_id: int, coche_data: CocheUpdate) -> Optional[CocheResponse]:
        """Actualiza parcialmente un coche."""
        if coche_data.user_id is not None:
            user = self._user_repo.get_by_id(coche_data.user_id)
            if not user:
                raise ValueError(f"El usuario con id {coche_data.user_id} no existe.")
                
        return self._coche_repo.update(coche_id, coche_data)

    def delete_coche(self, coche_id: int) -> bool:
        """Elimina un coche."""
        return self._coche_repo.delete(coche_id)
