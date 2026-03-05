"""
Implementación del repositorio de usuarios EN MEMORIA.

Esta clase hereda de UserRepository (la interfaz abstracta) y
almacena los datos en un simple diccionario de Python:

    { user_id: { "id": ..., "name": ..., "age": ..., ... } }

Al estar todo en RAM:
  ✅ Es rapidísimo y perfecto para desarrollo / prototipado.
  ❌ Los datos se pierden al reiniciar el servidor.

Cuando queramos persistir datos de verdad, crearemos por ejemplo
`SQLiteUserRepository(UserRepository)` con la misma interfaz.
El servicio y los endpoints NO se tocan.
"""

from typing import Optional

from app.models.user import UserCreate, UserUpdate, UserResponse
from app.repositories.base import UserRepository


class MemoryUserRepository(UserRepository):
    """
    Repositorio de usuarios que almacena todo en un diccionario
    en memoria RAM.
    """

    def __init__(self) -> None:
        # Diccionario principal:  id → dict con los datos del usuario
        self._storage: dict[int, dict] = {}

        # Contador auto-incremental para asignar ids únicos.
        # Cada vez que creamos un usuario, incrementamos este valor.
        self._next_id: int = 1

    # ─── CRUD ───────────────────────────────────────────────────

    def create(self, user_data: UserCreate) -> UserResponse:
        """
        Crea un nuevo usuario:
          1. Le asigna el siguiente id disponible.
          2. Convierte el modelo Pydantic a diccionario.
          3. Lo guarda en el diccionario _storage.
          4. Devuelve un UserResponse con el id incluido.
        """
        user_id = self._next_id
        self._next_id += 1

        # model_dump() convierte el objeto Pydantic a dict
        user_dict = user_data.model_dump()
        user_dict["id"] = user_id

        self._storage[user_id] = user_dict

        # Construimos el modelo de respuesta a partir del dict
        return UserResponse(**user_dict)

    def get_by_id(self, user_id: int) -> Optional[UserResponse]:
        """
        Busca en el diccionario por clave (id).
        Devuelve None si la clave no existe.
        """
        user_dict = self._storage.get(user_id)
        if user_dict is None:
            return None
        return UserResponse(**user_dict)

    def get_all(self) -> list[UserResponse]:
        """
        Recorre todos los valores del diccionario y los convierte
        a modelos de respuesta.
        """
        return [UserResponse(**data) for data in self._storage.values()]

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """
        Actualización parcial (PATCH):
          1. Comprobamos que el usuario exista.
          2. Extraemos solo los campos que el cliente ha enviado
             (exclude_unset=True ignora los que no vienen en el JSON).
          3. Actualizamos solo esos campos en el diccionario.
          4. Devolvemos el usuario actualizado.

        NOTA sobre exclude_unset:
          Si el cliente envía {"name": "Nuevo nombre"} y no envía "age",
          age NO se tocará. Esto permite actualizaciones parciales reales.
        """
        if user_id not in self._storage:
            return None

        # Solo los campos que el cliente envió explícitamente
        update_fields = user_data.model_dump(exclude_unset=True)

        # Actualizamos el diccionario almacenado
        self._storage[user_id].update(update_fields)

        return UserResponse(**self._storage[user_id])

    def delete(self, user_id: int) -> bool:
        """
        Elimina el usuario del diccionario con `pop`.
        pop devuelve None si la clave no existe → retornamos False.
        """
        removed = self._storage.pop(user_id, None)
        return removed is not None

    # ─── Búsquedas ──────────────────────────────────────────────

    def search(
        self,
        name: Optional[str] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        email: Optional[str] = None,
        city: Optional[str] = None,
    ) -> list[UserResponse]:
        """
        Filtra usuarios combinando todos los criterios con AND.

        Para cada usuario almacenado, comprobamos cada filtro activo.
        Si algún filtro no se cumple, descartamos ese usuario.

        Las búsquedas de texto (name, email, city) son:
          · Parciales: "ana" encuentra "Ana García"
          · Case-insensitive: "ANA" también encuentra "Ana García"
        """
        results: list[UserResponse] = []

        for user_dict in self._storage.values():
            # ── Filtro por nombre (parcial, case-insensitive) ──
            if name is not None:
                stored_name = user_dict.get("name", "")
                if name.lower() not in stored_name.lower():
                    continue  # No cumple → siguiente usuario

            # ── Filtro por edad mínima ──
            if min_age is not None:
                if user_dict.get("age", 0) < min_age:
                    continue

            # ── Filtro por edad máxima ──
            if max_age is not None:
                if user_dict.get("age", 0) > max_age:
                    continue

            # ── Filtro por email (parcial, case-insensitive) ──
            if email is not None:
                stored_email = user_dict.get("email") or ""
                if email.lower() not in stored_email.lower():
                    continue

            # ── Filtro por ciudad (parcial, case-insensitive) ──
            if city is not None:
                stored_city = user_dict.get("city") or ""
                if city.lower() not in stored_city.lower():
                    continue

            # Si llegó aquí, cumple TODOS los filtros activos
            results.append(UserResponse(**user_dict))

        return results
