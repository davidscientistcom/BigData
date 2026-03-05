import json
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

# --- Constantes y Carga de BBDD ---

DB_FILE = "database.json"

def load_db() -> List[dict]:
    """
    Carga la base de datos desde el archivo JSON.
    """
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [] # Devuelve lista vacía si no existe

def save_db():
    """
    Guarda el estado actual de la BBDD (db) en el archivo JSON.
    """
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

# --- Modelos Pydantic (Schemas) ---

class ItemBase(BaseModel):
    """Modelo base con campos comunes."""
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ItemCreate(ItemBase):
    """Modelo para la creación (entrada)."""
    pass

class Item(ItemBase):
    """Modelo para la lectura (salida/almacenamiento)."""
    id: int

# --- Instancia de la App y Carga Inicial de BBDD ---

app = FastAPI(
    title="API Módulo 4 - CRUD",
    description="API completa con CRUD sobre un archivo JSON.",
    version="0.4.0",
)

# Variable global para la BBDD en memoria
db = load_db()

# --- Endpoints CRUD ---

@app.get("/")
def read_root():
    return {"status": "API funcionando", "database_items": len(db)}

# --- CREATE ---
@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    """
    Crea un nuevo ítem en la base de datos.
    
    - Recibe un `ItemCreate` en el body.
    - Genera un nuevo ID.
    - Guarda en `database.json`.
    - Devuelve el `Item` completo (con ID).
    """
    # Lógica para generar un nuevo ID (robusta)
    # Usamos un generador y max() para eficiencia.
    last_id = max((i["id"] for i in db), default=0)
    new_id = last_id + 1
    
    new_item_data = item.model_dump()
    new_item_data["id"] = new_id
    
    # "Guardamos" en la BBDD en memoria
    db.append(new_item_data)
    
    # Guardamos en el archivo JSON
    save_db()
    
    return new_item_data

# --- READ (All) ---
@app.get("/items/", response_model=List[Item])
def read_items(max_price: float | None = Query(None, gt=0, description="Filtrar ítems con precio <= max_price")):
    """
    Lee todos los ítems de la base de datos.
    Permite filtrar por un precio máximo.
    """
    if max_price:
        # List Comprehension para filtrar
        filtered_items = [item for item in db if item["price"] <= max_price]
        return filtered_items
        
    return db

# --- READ (One) ---
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    """
    Lee un ítem por su ID.
    """
    # Usamos filter() y una lambda. next() toma el primero o None.
    item = next(filter(lambda x: x["id"] == item_id, db), None)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
        
    return item

# --- UPDATE (PUT - Reemplazo) ---
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemCreate):
    """
    Actualiza (reemplaza) un ítem por su ID.
    El body debe contener todos los campos del ítem (ItemCreate).
    """
    # Buscamos el índice del ítem en la lista
    index = next((i for i, item in enumerate(db) if item["id"] == item_id), None)
    
    if index is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    # Creamos el nuevo objeto (preservando el ID original)
    updated_item_data = item_update.model_dump()
    updated_item_data["id"] = item_id
    
    # Reemplazamos el ítem en la lista
    db[index] = updated_item_data
    
    save_db()
    return updated_item_data

# --- DELETE ---
@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    """
    Elimina un ítem por su ID.
    """
    global db # Necesario para reasignar la variable global
    
    # Comprobamos si existe
    item_exists = any(item["id"] == item_id for item in db)
    if not item_exists:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    # List comprehension: reconstruimos la lista
    # incluyendosolo los IDs que NO coinciden.
    db = [item for item in db if item["id"] != item_id]
    
    save_db()
    
    return {"detail": "Item eliminado correctamente", "id": item_id}
