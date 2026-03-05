"""
Modelos Pydantic para la entidad Usuario.

Pydantic nos permite definir esquemas de datos con validación automática.
Separamos en varios modelos según el caso de uso:

- UserCreate:   Datos que envía el cliente al CREAR un usuario (sin id).
- UserUpdate:   Datos opcionales para ACTUALIZAR parcialmente un usuario (PATCH).
- UserResponse: Datos que DEVOLVEMOS al cliente (incluye el id asignado).

Esta separación es una buena práctica porque:
  · El id lo genera el servidor, nunca lo envía el cliente.
  · En una actualización parcial (PATCH) todos los campos son opcionales.
  · El modelo de respuesta puede diferir del de entrada (p.ej. ocultar contraseñas).
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    """
    Esquema de entrada para crear un usuario.

    Todos los campos son obligatorios salvo 'email' que es opcional.
    Usamos `Field(...)` para añadir metadatos que Swagger mostrará.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre completo del usuario",
        examples=["Ana García"],
    )
    age: int = Field(
        ...,
        ge=0,
        le=150,
        description="Edad del usuario (0-150)",
        examples=[28],
    )
    email: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Correo electrónico (opcional)",
        examples=["ana@example.com"],
    )
    city: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Ciudad de residencia (opcional)",
        examples=["Madrid"],
    )

    # Configuración extra para la documentación de Swagger
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Ana García",
                    "age": 28,
                    "email": "ana@example.com",
                    "city": "Madrid",
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    """
    Esquema de entrada para actualizar parcialmente un usuario (PATCH).

    TODOS los campos son opcionales: solo se actualizarán
    los que el cliente envíe en el body.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Nuevo nombre del usuario",
        examples=["Ana López"],
    )
    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=150,
        description="Nueva edad del usuario",
        examples=[29],
    )
    email: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Nuevo correo electrónico",
        examples=["ana.lopez@example.com"],
    )
    city: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Nueva ciudad de residencia",
        examples=["Barcelona"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Ana López",
                    "age": 29,
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """
    Esquema de salida: lo que devolvemos al cliente.

    Incluye el 'id' que el servidor genera automáticamente.
    """

    id: int = Field(..., description="Identificador único del usuario", examples=[1])
    name: str = Field(..., description="Nombre completo del usuario", examples=["Ana García"])
    age: int = Field(..., description="Edad del usuario", examples=[28])
    email: Optional[str] = Field(
        default=None, description="Correo electrónico", examples=["ana@example.com"]
    )
    city: Optional[str] = Field(
        default=None, description="Ciudad de residencia", examples=["Madrid"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Ana García",
                    "age": 28,
                    "email": "ana@example.com",
                    "city": "Madrid",
                }
            ]
        }
    }
