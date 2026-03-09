"""
Implementación de los repositorios en SQLite.

Aquí no estamos usando un ORM como SQLAlchemy, sino la librería estándar `sqlite3`
para escribir las sentencias SQL a mano. Esto ilustra cómo el patrón
Repositorio nos permite ocultar toda esta complejidad. El Servicio de
Usuarios y Coches no sabrá que debajo hay sentencias SQL crudas.
"""

import sqlite3
from typing import Optional

from app.models.user import UserCreate, UserUpdate, UserResponse
from app.models.coche import CocheCreate, CocheUpdate, CocheResponse
from app.repositories.base import UserRepository, CocheRepository


class SQLiteBaseRepository:
    """Clase base para compartir la conexión a SQLite y crear tablas."""
    def __init__(self, db_path: str = "app.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        # row_factory permite acceder a las columnas por nombre
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        # Creamos las tablas si no existen
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT,
                    city TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS coches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    marca TEXT NOT NULL,
                    modelo TEXT NOT NULL,
                    anyo INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            conn.commit()


class SQLiteUserRepository(UserRepository, SQLiteBaseRepository):
    """
    Repositorio de Usuarios en SQLite.
    """
    def __init__(self, db_path: str = "app.db") -> None:
        SQLiteBaseRepository.__init__(self, db_path)

    def create(self, user_data: UserCreate) -> UserResponse:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, age, email, city) VALUES (?, ?, ?, ?)",
                (user_data.name, user_data.age, user_data.email, user_data.city)
            )
            user_id = cursor.lastrowid
            conn.commit()

            return UserResponse(
                id=user_id,
                name=user_data.name,
                age=user_data.age,
                email=user_data.email,
                city=user_data.city
            )

    def get_by_id(self, user_id: int) -> Optional[UserResponse]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return UserResponse(**dict(row))

    def get_all(self) -> list[UserResponse]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return [UserResponse(**dict(row)) for row in rows]

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        update_fields = user_data.model_dump(exclude_unset=True)
        if not update_fields:
            return self.get_by_id(user_id)

        # Construir la query UPDATE dinámicamente
        set_clauses = [f"{key} = ?" for key in update_fields.keys()]
        values = list(update_fields.values())
        values.append(user_id)

        query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                return None
            
        return self.get_by_id(user_id)

    def delete(self, user_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # foreign keys pragma para que ON DELETE CASCADE funcione
            conn.execute("PRAGMA foreign_keys = ON")
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0

    def search(
        self,
        name: Optional[str] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        email: Optional[str] = None,
        city: Optional[str] = None,
    ) -> list[UserResponse]:
        
        query = "SELECT * FROM users WHERE 1=1"
        params = []

        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")
        if min_age is not None:
            query += " AND age >= ?"
            params.append(min_age)
        if max_age is not None:
            query += " AND age <= ?"
            params.append(max_age)
        if email:
            query += " AND email LIKE ?"
            params.append(f"%{email}%")
        if city:
            query += " AND city LIKE ?"
            params.append(f"%{city}%")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [UserResponse(**dict(row)) for row in rows]


class SQLiteCocheRepository(CocheRepository, SQLiteBaseRepository):
    """
    Repositorio de Coches en SQLite.
    """
    def __init__(self, db_path: str = "app.db") -> None:
        SQLiteBaseRepository.__init__(self, db_path)

    def create(self, coche_data: CocheCreate) -> CocheResponse:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Nota: No verificamos aquí si el user_id existe, de eso se puede
            # encargar el servicio o la propia restricción Foreign Key de SQLite
            # si tenemos los pragmas activados.
            conn.execute("PRAGMA foreign_keys = ON")
            
            try:
                cursor.execute(
                    "INSERT INTO coches (marca, modelo, anyo, user_id) VALUES (?, ?, ?, ?)",
                    (coche_data.marca, coche_data.modelo, coche_data.anyo, coche_data.user_id)
                )
                coche_id = cursor.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                # Ocurriría si el user_id no existe en la tabla users
                raise ValueError(f"El usuario con id {coche_data.user_id} no existe.")

            return CocheResponse(
                id=coche_id,
                marca=coche_data.marca,
                modelo=coche_data.modelo,
                anyo=coche_data.anyo,
                user_id=coche_data.user_id
            )

    def get_by_id(self, coche_id: int) -> Optional[CocheResponse]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM coches WHERE id = ?", (coche_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return CocheResponse(**dict(row))

    def get_by_user_id(self, user_id: int) -> list[CocheResponse]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM coches WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
            return [CocheResponse(**dict(row)) for row in rows]

    def get_all(self) -> list[CocheResponse]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM coches")
            rows = cursor.fetchall()
            return [CocheResponse(**dict(row)) for row in rows]

    def update(self, coche_id: int, coche_data: CocheUpdate) -> Optional[CocheResponse]:
        update_fields = coche_data.model_dump(exclude_unset=True)
        if not update_fields:
            return self.get_by_id(coche_id)

        set_clauses = [f"{key} = ?" for key in update_fields.keys()]
        values = list(update_fields.values())
        values.append(coche_id)

        query = f"UPDATE coches SET {', '.join(set_clauses)} WHERE id = ?"
        
        with self._get_connection() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            try:
                cursor.execute(query, values)
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError("El user_id proporcionado no existe.")
            
            if cursor.rowcount == 0:
                return None
            
        return self.get_by_id(coche_id)

    def delete(self, coche_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM coches WHERE id = ?", (coche_id,))
            conn.commit()
            return cursor.rowcount > 0
