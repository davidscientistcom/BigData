# Explicación de las modificaciones para la entidad Coche y los Repositorios

## 1. Patrón Repositorio y Entidad Coche

El patrón de diseño "Repositorio" nos permite separar la lógica de negocio (los Servicios y Routers) de la forma en que los datos se persisten en nuestra base de datos. Esto nos da la flexibilidad de empezar guardando todo en memoria RAM (como diccionarios) y, el día de mañana, sustituirlo fácilmente por un motor de bases de datos relacional (como SQLite, MySQL, PostgreSQL) u otro (como MongoDB).

### ¿Qué componentes hemos creado?

1. **Modelos (Pydantic):** Añadimos los modelos `CocheCreate`, `CocheUpdate` y `CocheResponse` en `app/models/coche.py`. Tienen un campo `user_id` para enlazar coches con su propietario.
2. **Interfaz de Repositorio:** En `app/repositories/base.py`, creamos la clase abstracta `CocheRepository` con los métodos (`create`, `get_by_id`, `get_by_user_id`, `update`, `delete`). Quien herede de esto **deberá** implementar los métodos.
3. **Servicio (`CocheService`):** Orquesta los repositorios. Antes de añadir un coche a un usuario, debe verificar que el usuario realmente existe. En vez de tocar la base de datos localmente, llama a su propio `coche_repository` y usa el `user_repository` para dichas validaciones.
4. **Router (`coches.py`):** Los endpoints en FastAPI, totalmente independientes y limpios para `/coches`.

## 2. Implementaciones Adicionales de los Repositorios (SQLite y MySQL)

Aunque la aplicación se arranca por defecto usando la memoria RAM (ver las variables globales `_coche_repository` y `_repository` en `app/routers/users.py` y `app/routers/coches.py`), hemos desarrollado dos implementaciones extra de ambos repositorios (tanto la de `User` como la de `Coche`):

- **Repository `SQLite` (`app/repositories/sqlite.py`):**
  - Utiliza la librería estándar y nativa de Python `sqlite3`.
  - Cuando se instancia la clase abstracta por primera vez, el objeto se encarga de realizar un `CREATE TABLE IF NOT EXISTS` en un archivo local llamado `app.db`.
  - Las transacciones de escritura se blindan con un `conn.commit()`.
  
- **Repository `MySQL` (`app/repositories/mysql.py`):**
  - Utiliza el driver externo `pymysql` (añadido previamente al proyecto).
  - Actúa de la misma manera dinámica. Si hay una conexión MySQL local, crea las tablas y devuelve en objetos de Pydantic utilizando un cursor de diccionario (`DictCursor`).
  
### Ventajas del enfoque

Si quisiéramos arrancar la API con una base de datos MySQL real en lugar de Memory, nuestros cambios estarían sumamente localizados: 
Sólo iríamos al router, y en vez de instanciar un `MemoryUserRepository()` o `MemoryCocheRepository()`, importaríamos e instanciaríamos `MySQLUserRepository()` y `MySQLCocheRepository(host="...", ...)` y nuestro `get_user_service` y `get_coche_service` lo utilizarán en los endpoints de FastAPI automáticamente gracias a la **inyección de dependencias (`Depends`)**, de la cual hace gala este grandioso framework. ¡No habría que modificar ni el código de negocio, ni la declaración de los endpoints!
