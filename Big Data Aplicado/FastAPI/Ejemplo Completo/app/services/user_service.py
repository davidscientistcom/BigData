"""
Servicio de usuarios — Capa de lógica de negocio.

╔══════════════════════════════════════════════════════════════════╗
║  ¿POR QUÉ UNA CAPA DE SERVICIO?                                ║
║                                                                  ║
║  Separamos la lógica de negocio de los endpoints (router)       ║
║  y del acceso a datos (repository) para:                        ║
║                                                                  ║
║  1. Mantener los endpoints limpios y fáciles de leer.           ║
║  2. Poder reutilizar la lógica desde distintos sitios.          ║
║  3. Facilitar el testing unitario (mockear el repositorio).     ║
║                                                                  ║
║  Flujo completo:                                                ║
║    HTTP Request → Router → Service → Repository → RAM/DB        ║
║    HTTP Response ← Router ← Service ← Repository ← RAM/DB      ║
╚══════════════════════════════════════════════════════════════════╝

El servicio recibe un repositorio por INYECCIÓN DE DEPENDENCIAS
en el constructor. Esto es clave para el desacoplamiento:
el servicio no sabe si el repo es en memoria, SQLite o MongoDB.
"""

from typing import Optional

from app.models.user import UserCreate, UserUpdate, UserResponse
from app.repositories.base import UserRepository


class UserService:
    """
    Orquesta las operaciones sobre usuarios delegando
    la persistencia al repositorio inyectado.
    """

    def __init__(self, repository: UserRepository) -> None:
        """
        Inyección de dependencias: recibimos CUALQUIER implementación
        de UserRepository. El servicio trabaja contra la interfaz,
        no contra una implementación concreta.
        """
        self._repo = repository

    # ─── CRUD ───────────────────────────────────────────────────

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Crea un usuario nuevo delegando al repositorio."""
        return self._repo.create(user_data)

    def get_user(self, user_id: int) -> Optional[UserResponse]:
        """Obtiene un usuario por id. Devuelve None si no existe."""
        return self._repo.get_by_id(user_id)

    def get_all_users(self) -> list[UserResponse]:
        """Devuelve la lista completa de usuarios."""
        return self._repo.get_all()

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """
        Actualiza parcialmente un usuario.
        Devuelve None si el usuario no existe.
        """
        return self._repo.update(user_id, user_data)

    def delete_user(self, user_id: int) -> bool:
        """
        Elimina un usuario. Devuelve True si se eliminó,
        False si no existía.
        """
        return self._repo.delete(user_id)

    # ─── Búsquedas ──────────────────────────────────────────────

    def search_users(
        self,
        name: Optional[str] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        email: Optional[str] = None,
        city: Optional[str] = None,
    ) -> list[UserResponse]:
        """
        Búsqueda avanzada con múltiples criterios opcionales.
        Los filtros se combinan con AND.
        """
        return self._repo.search(
            name=name,
            min_age=min_age,
            max_age=max_age,
            email=email,
            city=city,
        )
