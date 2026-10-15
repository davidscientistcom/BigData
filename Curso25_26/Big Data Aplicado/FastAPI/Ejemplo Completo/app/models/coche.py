"""
Modelos Pydantic para la entidad Coche.

Al igual que con User, separamos en varios modelos:
- CocheCreate
- CocheUpdate
- CocheResponse
"""

from pydantic import BaseModel, Field
from typing import Optional


class CocheCreate(BaseModel):
    """Esquema para crear un coche."""
    marca: str = Field(..., min_length=1, max_length=50, description="Marca del coche", examples=["Toyota"])
    modelo: str = Field(..., min_length=1, max_length=50, description="Modelo del coche", examples=["Corolla"])
    anyo: int = Field(..., ge=1886, le=2100, description="Año de fabricación", examples=[2022])
    user_id: int = Field(..., description="ID del usuario propietario del coche", examples=[1])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "marca": "Toyota",
                    "modelo": "Corolla",
                    "anyo": 2022,
                    "user_id": 1,
                }
            ]
        }
    }


class CocheUpdate(BaseModel):
    """Esquema para actualizar parcialmente un coche."""
    marca: Optional[str] = Field(default=None, min_length=1, max_length=50, description="Marca del coche")
    modelo: Optional[str] = Field(default=None, min_length=1, max_length=50, description="Modelo del coche")
    anyo: Optional[int] = Field(default=None, ge=1886, le=2100, description="Año de fabricación")
    user_id: Optional[int] = Field(default=None, description="Nuevo ID del usuario propietario")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "anyo": 2023,
                }
            ]
        }
    }


class CocheResponse(BaseModel):
    """Esquema de respuesta para un coche."""
    id: int = Field(..., description="Identificador único del coche", examples=[1])
    marca: str = Field(..., description="Marca del coche", examples=["Toyota"])
    modelo: str = Field(..., description="Modelo del coche", examples=["Corolla"])
    anyo: int = Field(..., description="Año de fabricación", examples=[2022])
    user_id: int = Field(..., description="ID del usuario propietario", examples=[1])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "marca": "Toyota",
                    "modelo": "Corolla",
                    "anyo": 2022,
                    "user_id": 1,
                }
            ]
        }
    }
