"""
Repositorio abstracto (interfaz) — Patrón Repository.

╔══════════════════════════════════════════════════════════════════╗
║  ¿POR QUÉ USAMOS ESTE PATRÓN?                                  ║
║                                                                  ║
║  El patrón Repository desacopla la LÓGICA DE NEGOCIO del        ║
║  MECANISMO DE PERSISTENCIA.                                      ║
║                                                                  ║
║  Hoy guardamos usuarios en un diccionario en RAM.               ║
║  Mañana podríamos usar SQLite, PostgreSQL o MongoDB              ║
║  simplemente creando una nueva clase que herede de               ║
║  UserRepository y sobrescriba los métodos abstractos.            ║
║                                                                  ║
║  La capa de servicio y los endpoints NO cambian.                ║
║                                                                  ║
║  Flujo:                                                          ║
║    Router → Service → Repository (interfaz)                      ║
║                            ↓                                     ║
║                   MemoryUserRepository  (hoy)                    ║
║                   SQLiteUserRepository  (mañana)                 ║
╚══════════════════════════════════════════════════════════════════╝

Usamos `abc.ABC` y `abc.abstractmethod` de la librería estándar
de Python para definir métodos que OBLIGAN a las clases hijas
a implementarlos. Si no lo hacen, Python lanza un error al
intentar instanciarlas.
"""

from abc import ABC, abstractmethod
from typing import Optional

from app.models.user import UserCreate, UserUpdate, UserResponse


class UserRepository(ABC):
    """
    Contrato (interfaz) que debe cumplir cualquier implementación
    de repositorio de usuarios.

    Cada método está documentado para que quede claro qué debe
    hacer la implementación concreta.
    """

    # ─── CRUD básico ────────────────────────────────────────────

    @abstractmethod
    def create(self, user_data: UserCreate) -> UserResponse:
        """
        Crea un nuevo usuario y le asigna un id único.

        Args:
            user_data: Datos validados del usuario a crear.

        Returns:
            El usuario creado con su id asignado.
        """
        ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserResponse]:
        """
        Busca un usuario por su id.

        Args:
            user_id: Identificador único del usuario.

        Returns:
            El usuario encontrado o None si no existe.
        """
        ...

    @abstractmethod
    def get_all(self) -> list[UserResponse]:
        """
        Devuelve todos los usuarios almacenados.

        Returns:
            Lista de usuarios (puede estar vacía).
        """
        ...

    @abstractmethod
    def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """
        Actualiza parcialmente un usuario existente.

        Solo se modifican los campos que NO sean None
        en user_data (actualización parcial / PATCH).

        Args:
            user_id:   Id del usuario a actualizar.
            user_data: Campos a modificar.

        Returns:
            El usuario actualizado o None si no existe.
        """
        ...

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario por su id.

        Args:
            user_id: Identificador del usuario a eliminar.

        Returns:
            True si se eliminó, False si no existía.
        """
        ...

    # ─── Búsquedas avanzadas ────────────────────────────────────

    @abstractmethod
    def search(
        self,
        name: Optional[str] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        email: Optional[str] = None,
        city: Optional[str] = None,
    ) -> list[UserResponse]:
        """
        Busca usuarios filtrando por uno o varios criterios.

        Todos los filtros son opcionales y se combinan con AND lógico:
        un usuario debe cumplir TODOS los filtros activos para aparecer.

        Args:
            name:    Busca coincidencia parcial (case-insensitive) en el nombre.
            min_age: Edad mínima (inclusive).
            max_age: Edad máxima (inclusive).
            email:   Busca coincidencia parcial en el email.
            city:    Busca coincidencia parcial en la ciudad.

        Returns:
            Lista de usuarios que cumplen todos los criterios.
        """
        ...
