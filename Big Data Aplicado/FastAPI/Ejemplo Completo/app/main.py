"""
Punto de entrada de la aplicación FastAPI.

╔══════════════════════════════════════════════════════════════════╗
║  EJECUCIÓN                                                       ║
║                                                                  ║
║  Desde la terminal:                                              ║
║    uvicorn app.main:app --reload                                 ║
║                                                                  ║
║  · app.main  → módulo Python (fichero app/main.py)              ║
║  · app       → variable que contiene la instancia FastAPI        ║
║  · --reload  → reinicia automáticamente al guardar cambios       ║
║                                                                  ║
║  Documentación interactiva (Swagger UI):                         ║
║    http://127.0.0.1:8000/docs                                    ║
║                                                                  ║
║  Documentación alternativa (ReDoc):                              ║
║    http://127.0.0.1:8000/redoc                                   ║
║                                                                  ║
║  Esquema OpenAPI en JSON:                                        ║
║    http://127.0.0.1:8000/openapi.json                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

from fastapi import FastAPI

from app.routers import users, coches

# ──────────────────────────────────────────────────────────────────
# Creamos la instancia de FastAPI con metadatos para Swagger
# ──────────────────────────────────────────────────────────────────

app = FastAPI(
    title="API de Usuarios — Curso Testing",
    description="""
## API REST de ejemplo para el Curso de Testing

Esta API demuestra un **CRUD completo** sobre usuarios 
usando FastAPI con una arquitectura modular basada en el 
**patrón Repository**.

### Características

* ✅ **CRUD completo**: Crear, Leer, Actualizar y Eliminar usuarios
* 🔍 **Búsqueda avanzada**: Filtrar por nombre, edad, email y ciudad
* 📦 **Persistencia en RAM**: Los datos se almacenan en un diccionario
* 🔄 **Patrón Repository**: Desacoplamiento de la capa de persistencia
* 📝 **Documentación automática**: Swagger UI generada por FastAPI

### Arquitectura

```
Router  →  Service  →  Repository (interfaz)
                            ↓
                   MemoryUserRepository (implementación actual)
```

> **Nota**: Los datos se pierden al reiniciar el servidor porque 
> se almacenan en memoria RAM. En futuras lecciones se integrará 
> una base de datos real.
    """,
    version="1.0.0",
    contact={
        "name": "Curso de Testing",
    },
    license_info={
        "name": "MIT",
    },
)

# ──────────────────────────────────────────────────────────────────
# Incluimos el router de usuarios
# ──────────────────────────────────────────────────────────────────
# El prefijo /users y el tag ya están definidos en el router.
# include_router() los "monta" en la app principal.
app.include_router(users.router)
app.include_router(coches.router)


# ──────────────────────────────────────────────────────────────────
# Endpoint raíz (health check / bienvenida)
# ──────────────────────────────────────────────────────────────────


@app.get(
    "/",
    summary="Raíz de la API",
    description="Endpoint de bienvenida y verificación de que la API está activa.",
    tags=["General"],
)
def root():
    """Devuelve un mensaje de bienvenida."""
    return {
        "message": "🚀 API de Usuarios activa",
        "docs": "/docs",
        "redoc": "/redoc",
    }
