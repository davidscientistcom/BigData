"""
Implementación de los repositorios en MySQL usando pymysql.

A diferencia del SQLite en un solo archivo, MySQL requiere conexión
a un servidor de base de datos. Configurable por variables de entorno
o parámetros.
"""

import pymysql
from pymysql.cursors import DictCursor
from typing import Optional

from app.models.user import UserCreate, UserUpdate, UserResponse
from app.models.coche import CocheCreate, CocheUpdate, CocheResponse
from app.repositories.base import UserRepository, CocheRepository


class MySQLBaseRepository:
    """Clase base para compartir la conexión a MySQL y crear tablas."""
    def __init__(
        self, 
        host: str = "localhost", 
        user: str = "root", 
        password: str = "", 
        database: str = "fastapi_db"
    ) -> None:
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "cursorclass": DictCursor
        }
        self._init_db()

    def _get_connection(self) -> pymysql.Connection:
        # Se asume que la base de datos existe. Caso contrario habría que crearla
        # conectándose sin base de datos primero. Para simplificar, asumimos que existe.
        try:
            return pymysql.connect(**self.config)
        except pymysql.err.OperationalError:
            # Si la DB no existe, intentamos crearla conectando sin DB
            config_no_db = self.config.copy()
            db_name = config_no_db.pop("database")
            conn = pymysql.connect(**config_no_db)
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            conn.commit()
            conn.close()
            return pymysql.connect(**self.config)

    def _init_db(self) -> None:
        # Creamos las tablas si no existen
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        age INT NOT NULL,
                        email VARCHAR(255),
                        city VARCHAR(100)
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS coches (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        marca VARCHAR(50) NOT NULL,
                        modelo VARCHAR(50) NOT NULL,
                        anyo INT NOT NULL,
                        user_id INT NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                ''')
            conn.commit()
        finally:
            conn.close()


class MySQLUserRepository(UserRepository, MySQLBaseRepository):
    """
    Repositorio de Usuarios en MySQL.
    """
    def create(self, user_data: UserCreate) -> UserResponse:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, age, email, city) VALUES (%s, %s, %s, %s)",
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
        finally:
            conn.close()

    def get_by_id(self, user_id: int) -> Optional[UserResponse]:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                return UserResponse(**row)
        finally:
            conn.close()

    def get_all(self) -> list[UserResponse]:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                rows = cursor.fetchall()
                return [UserResponse(**row) for row in rows]
        finally:
            conn.close()

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        update_fields = user_data.model_dump(exclude_unset=True)
        if not update_fields:
            return self.get_by_id(user_id)

        set_clauses = [f"{key} = %s" for key in update_fields.keys()]
        values = list(update_fields.values())
        values.append(user_id)

        query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = %s"
        
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                if cursor.rowcount == 0:
                    # Comprobar si el usuario existe o si los datos eran los mismos
                    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
                    if not cursor.fetchone():
                        return None
            conn.commit()
        finally:
            conn.close()
            
        return self.get_by_id(user_id)

    def delete(self, user_id: int) -> bool:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
        finally:
            conn.close()

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
            query += " AND name LIKE %s"
            params.append(f"%{name}%")
        if min_age is not None:
            query += " AND age >= %s"
            params.append(min_age)
        if max_age is not None:
            query += " AND age <= %s"
            params.append(max_age)
        if email:
            query += " AND email LIKE %s"
            params.append(f"%{email}%")
        if city:
            query += " AND city LIKE %s"
            params.append(f"%{city}%")

        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [UserResponse(**row) for row in rows]
        finally:
            conn.close()


class MySQLCocheRepository(CocheRepository, MySQLBaseRepository):
    """
    Repositorio de Coches en MySQL.
    """
    def create(self, coche_data: CocheCreate) -> CocheResponse:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO coches (marca, modelo, anyo, user_id) VALUES (%s, %s, %s, %s)",
                        (coche_data.marca, coche_data.modelo, coche_data.anyo, coche_data.user_id)
                    )
                    coche_id = cursor.lastrowid
                except pymysql.err.IntegrityError:
                    raise ValueError(f"El usuario con id {coche_data.user_id} no existe.")
            conn.commit()
            return CocheResponse(
                id=coche_id,
                marca=coche_data.marca,
                modelo=coche_data.modelo,
                anyo=coche_data.anyo,
                user_id=coche_data.user_id
            )
        finally:
            conn.close()

    def get_by_id(self, coche_id: int) -> Optional[CocheResponse]:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM coches WHERE id = %s", (coche_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                return CocheResponse(**row)
        finally:
            conn.close()

    def get_by_user_id(self, user_id: int) -> list[CocheResponse]:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM coches WHERE user_id = %s", (user_id,))
                rows = cursor.fetchall()
                return [CocheResponse(**row) for row in rows]
        finally:
            conn.close()

    def get_all(self) -> list[CocheResponse]:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM coches")
                rows = cursor.fetchall()
                return [CocheResponse(**row) for row in rows]
        finally:
            conn.close()

    def update(self, coche_id: int, coche_data: CocheUpdate) -> Optional[CocheResponse]:
        update_fields = coche_data.model_dump(exclude_unset=True)
        if not update_fields:
            return self.get_by_id(coche_id)

        set_clauses = [f"{key} = %s" for key in update_fields.keys()]
        values = list(update_fields.values())
        values.append(coche_id)

        query = f"UPDATE coches SET {', '.join(set_clauses)} WHERE id = %s"
        
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, values)
                except pymysql.err.IntegrityError:
                    raise ValueError("El user_id proporcionado no existe.")
                
                if cursor.rowcount == 0:
                    cursor.execute("SELECT id FROM coches WHERE id = %s", (coche_id,))
                    if not cursor.fetchone():
                        return None
            conn.commit()
        finally:
            conn.close()
            
        return self.get_by_id(coche_id)

    def delete(self, coche_id: int) -> bool:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM coches WHERE id = %s", (coche_id,))
                deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
        finally:
            conn.close()