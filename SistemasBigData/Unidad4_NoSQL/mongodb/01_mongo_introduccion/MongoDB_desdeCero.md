# MongoDB: Guía Completa con Python

## Introducción

MongoDB es una base de datos NoSQL orientada a documentos que ofrece flexibilidad en el modelado de datos y escalabilidad horizontal. A diferencia de las bases de datos relacionales tradicionales, MongoDB almacena información en documentos JSON (BSON internamente), permitiendo estructuras de datos más naturales y dinámicas.

Esta guía está diseñada para desarrolladores con conocimientos de bases de datos relacionales que desean comprender MongoDB desde sus fundamentos hasta operaciones avanzadas.


## 1. Conceptos Fundamentales

### 1.1. NoSQL vs SQL: Diferencias Clave

Las bases de datos relacionales (SQL) y MongoDB (NoSQL) difieren en varios aspectos fundamentales:

**Bases de Datos Relacionales (SQL)**:
- Estructura rígida definida por esquemas (schema-on-write)
- Los datos se organizan en tablas con filas y columnas
- Relaciones entre datos mediante claves foráneas
- Escalabilidad vertical (más potencia en un solo servidor)
- Transacciones ACID garantizadas

**MongoDB (NoSQL)**:
- Estructura flexible (schema-on-read)
- Los datos se organizan en colecciones de documentos
- Relaciones mediante referencias o documentos embebidos
- Escalabilidad horizontal (distribución en múltiples servidores)
- Transacciones ACID disponibles desde la versión 4.0

### 1.2. Equivalencias entre SQL y MongoDB

| Concepto SQL | Concepto MongoDB | Descripción |
|--------------|------------------|-------------|
| Base de datos | Base de datos | Contenedor principal de datos |
| Tabla | Colección | Agrupación de registros |
| Fila | Documento | Unidad individual de datos |
| Columna | Campo | Atributo dentro de un documento |
| PRIMARY KEY | _id | Identificador único |
| JOIN | $lookup / Embedding | Relación entre datos |
| Índice | Índice | Optimización de consultas |

### 1.3. Documentos y BSON

Los documentos en MongoDB son estructuras JSON que se almacenan internamente en formato BSON (Binary JSON). Un documento puede contener:

- Pares clave-valor simples
- Arrays de valores
- Documentos anidados
- Combinaciones de todos los anteriores

Ejemplo de documento:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "nombre": "Juan Pérez",
  "edad": 30,
  "correo": "juan@ejemplo.com",
  "direcciones": [
    {
      "tipo": "casa",
      "ciudad": "Madrid",
      "codigo_postal": "28001"
    },
    {
      "tipo": "trabajo",
      "ciudad": "Madrid",
      "codigo_postal": "28020"
    }
  ],
  "fecha_registro": ISODate("2024-01-15T10:30:00Z")
}
```

### 1.4. El Campo _id

Cada documento en MongoDB debe tener un campo `_id` único:

- Si no se proporciona, MongoDB genera automáticamente un `ObjectId`
- Un `ObjectId` es un valor hexadecimal de 12 bytes que incluye:
  - Timestamp de creación (4 bytes)
  - Identificador de máquina (3 bytes)
  - ID de proceso (2 bytes)
  - Contador aleatorio (3 bytes)

Esta estructura permite generar IDs únicos de forma distribuida sin necesidad de coordinación central.

## 2. Configuración del Entorno con Docker

### 2.1. ¿Por Qué Docker?

Docker proporciona un entorno aislado y reproducible para MongoDB:

- **Portabilidad**: El mismo entorno funciona en cualquier sistema operativo
- **Aislamiento**: No contamina el sistema operativo local
- **Reproducibilidad**: La configuración se documenta en archivos
- **Fácil gestión**: Iniciar, detener y eliminar el entorno es sencillo

### 2.2. Archivo docker-compose.yml

Crea un archivo `docker-compose.yml` con el siguiente contenido:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    container_name: mongodb_curso
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      # Credenciales del usuario administrador
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
      # Base de datos inicial (opcional)
      MONGO_INITDB_DATABASE: tienda_db
    volumes:
      # Persistencia de datos
      - ./mongo_data:/data/db
      # Scripts de inicialización (opcional)
      - ./init-scripts:/docker-entrypoint-initdb.d
    command: ["mongod", "--auth"]

networks:
  default:
    name: mongo_network
```

### 2.3. Explicación de la Configuración

**Variables de Entorno**:

- `MONGO_INITDB_ROOT_USERNAME`: Nombre del usuario administrador
- `MONGO_INITDB_ROOT_PASSWORD`: Contraseña del usuario administrador
- `MONGO_INITDB_DATABASE`: Base de datos inicial (opcional)

**Importante**: Estas variables solo se aplican durante la **primera inicialización** del contenedor, cuando el directorio `/data/db` está vacío.

**Volúmenes**:

- `./mongo_data:/data/db`: Mapea la carpeta local `mongo_data` al directorio de datos de MongoDB dentro del contenedor
- Esto asegura que los datos persistan aunque el contenedor se elimine

**Comando de Autenticación**:

- `--auth`: Activa el modo de autenticación, requiriendo credenciales para conectarse

### 2.4. Gestión del Ciclo de Vida

**Iniciar MongoDB**:
```bash
docker-compose up -d
```

**Ver logs**:
```bash
docker-compose logs -f mongodb
```

**Detener MongoDB**:
```bash
docker-compose down
```

**Detener y eliminar datos** (¡cuidado!):
```bash
docker-compose down -v
# O manualmente:
rm -rf ./mongo_data
```

### 2.5. Cambiar Credenciales: Proceso Completo

Si necesitas cambiar las credenciales después de la primera inicialización:

1. **Detener el contenedor**:
```bash
docker-compose down
```

2. **Eliminar los datos existentes**:
```bash
rm -rf ./mongo_data
```

3. **Modificar el `docker-compose.yml`** con las nuevas credenciales

4. **Reiniciar el contenedor**:
```bash
docker-compose up -d
```

**Explicación**: Las variables `MONGO_INITDB_*` solo se procesan cuando MongoDB detecta un directorio `/data/db` vacío. El script de inicialización (`/usr/local/bin/docker-entrypoint.sh`) verifica si ya existe una base de datos y, si es así, ignora estas variables. Por eso es necesario eliminar los datos para que las nuevas credenciales surtan efecto.

### 2.6. Verificación de la Conexión

**Conectarse mediante el shell de MongoDB**:

```bash
# Dentro del contenedor
docker exec -it mongodb_curso mongosh -u admin -p password123 --authenticationDatabase admin
```

Una vez conectado, puedes ejecutar comandos:

```javascript
// Ver bases de datos
show dbs

// Cambiar a una base de datos
use tienda_db

// Ver colecciones
show collections

// Salir
exit
```

---

## 3. Conexión con Python usando PyMongo

### 3.1. Instalación de PyMongo

```bash
pip install pymongo
```

### 3.2. Conexión Básica

```python
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# URI de conexión
MONGO_URI = "mongodb://admin:password123@localhost:27017/"

def conectar_mongodb():
    """
    Establece conexión con MongoDB y verifica que esté disponible.
    """
    try:
        # Crear cliente con timeout
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Verificar conectividad con un ping
        client.admin.command('ping')
        
        print("✅ Conexión exitosa a MongoDB")
        return client
    
    except ConnectionFailure as e:
        print(f"❌ Error de conexión: {e}")
        return None

# Establecer conexión
cliente = conectar_mongodb()

# Seleccionar base de datos
db = cliente['tienda_db']

# Seleccionar colección
coleccion_productos = db['productos']
```

### 3.3. Variables de Entorno para Seguridad

Es recomendable no hardcodear las credenciales:

```python
import os
from pymongo import MongoClient

# Leer desde variables de entorno
MONGO_USER = os.getenv('MONGO_USER', 'admin')
MONGO_PASS = os.getenv('MONGO_PASS', 'password123')
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', '27017')

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

cliente = MongoClient(MONGO_URI)
```

### 3.4. Pool de Conexiones

PyMongo gestiona automáticamente un pool de conexiones. Algunas configuraciones útiles:

```python
cliente = MongoClient(
    MONGO_URI,
    maxPoolSize=50,              # Máximo de conexiones en el pool
    minPoolSize=10,              # Mínimo de conexiones mantenidas
    serverSelectionTimeoutMS=5000  # Timeout para seleccionar servidor
)
```

### 3.5. Manejo de Tipos BSON

**ObjectId**:

```python
from bson import ObjectId

# Convertir string a ObjectId
id_producto = ObjectId("507f1f77bcf86cd799439011")

# Validar si un string es un ObjectId válido
if ObjectId.is_valid("507f1f77bcf86cd799439011"):
    id_valido = ObjectId("507f1f77bcf86cd799439011")
```

**Decimal128 para valores monetarios**:

```python
from bson.decimal128 import Decimal128

# NUNCA usar float para dinero
precio_incorrecto = 19.99  # ❌ Puede tener errores de redondeo

# SIEMPRE usar Decimal128
precio_correcto = Decimal128("19.99")  # ✅ Precisión exacta
```

**Fechas**:

```python
from datetime import datetime

# MongoDB almacena fechas como ISODate
fecha_actual = datetime.now()

# Crear fecha específica
fecha_especifica = datetime(2024, 1, 15, 10, 30, 0)
```

---

## 4. Modelado de Datos en MongoDB

### 4.1. Embedding vs Referencing

La decisión más importante al diseñar un esquema en MongoDB es cómo estructurar las relaciones entre datos.

**Embedding (Documentos Embebidos)**:

Ventajas:
- Una sola lectura obtiene todos los datos relacionados
- Mejor rendimiento para datos que se acceden juntos
- Atomicidad garantizada (las operaciones en un documento son atómicas)

Desventajas:
- Límite de 16 MB por documento
- Duplicación de datos si la relación no es 1:1 o 1:N pequeño
- Difícil actualizar datos embebidos en múltiples documentos

**Cuándo usar Embedding**:
- Relaciones uno a uno
- Relaciones uno a pocos (hasta ~100 subdocumentos)
- Datos que siempre se acceden juntos
- Datos que no cambian frecuentemente

**Referencing (Referencias)**:

Ventajas:
- Sin límite en la cantidad de relaciones
- Evita duplicación de datos
- Facilita actualizaciones centralizadas

Desventajas:
- Requiere múltiples consultas o uso de `$lookup` (JOIN)
- Menor rendimiento si siempre necesitas los datos relacionados

**Cuándo usar Referencing**:
- Relaciones uno a muchos con N grande
- Relaciones muchos a muchos
- Datos que cambian frecuentemente
- Datos compartidos por múltiples documentos

### 4.2. Ejemplo Práctico: Sistema de E-Commerce

**Colección: usuarios**

```javascript
{
  "_id": ObjectId("..."),
  "nombre": "Ana García",
  "email": "ana@ejemplo.com",
  "password_hash": "...",
  "fecha_registro": ISODate("2024-01-10T00:00:00Z"),
  
  // Embedding: direcciones (relación 1:pocos)
  "direcciones": [
    {
      "tipo": "envio",
      "calle": "Calle Mayor 123",
      "ciudad": "Madrid",
      "codigo_postal": "28001",
      "pais": "España"
    }
  ],
  
  // Embedding: carrito actual
  "carrito": {
    "items": [
      {
        "producto_id": ObjectId("..."),
        "cantidad": 2,
        "precio_unitario": Decimal128("29.99")
      }
    ],
    "total": Decimal128("59.98"),
    "ultima_actualizacion": ISODate("2024-02-01T15:30:00Z")
  }
}
```

**Colección: productos**

```javascript
{
  "_id": ObjectId("..."),
  "sku": "LAPTOP-001",
  "nombre": "Portátil HP ProBook",
  "descripcion": "Portátil profesional de 15 pulgadas",
  "precio": Decimal128("899.99"),
  "stock": 25,
  
  // Array simple para categorías
  "categorias": ["electronica", "informatica", "portatiles"],
  
  // Embedding: especificaciones (datos siempre accedidos juntos)
  "especificaciones": {
    "procesador": "Intel Core i7",
    "ram": "16GB",
    "almacenamiento": "512GB SSD",
    "pantalla": "15.6 pulgadas Full HD"
  },
  
  // Array de subdocumentos para variantes
  "imagenes": [
    {
      "url": "https://ejemplo.com/img1.jpg",
      "es_principal": true
    }
  ],
  
  "fecha_creacion": ISODate("2024-01-05T00:00:00Z"),
  "activo": true
}
```

**Colección: pedidos** (Patrón Snapshot)

```javascript
{
  "_id": ObjectId("..."),
  
  // Referencing: ID del usuario
  "usuario_id": ObjectId("..."),
  
  "fecha_pedido": ISODate("2024-02-01T10:00:00Z"),
  "estado": "enviado", // pendiente, procesando, enviado, entregado, cancelado
  
  // Embedding: snapshot de los productos al momento de la compra
  // Esto preserva el precio y detalles históricos
  "items": [
    {
      "producto_id": ObjectId("..."),
      "nombre": "Portátil HP ProBook", // Snapshot del nombre
      "sku": "LAPTOP-001",
      "cantidad": 1,
      "precio_unitario": Decimal128("899.99"), // Precio al momento de la compra
      "subtotal": Decimal128("899.99")
    }
  ],
  
  // Embedding: dirección de envío (snapshot)
  "direccion_envio": {
    "nombre_destinatario": "Ana García",
    "calle": "Calle Mayor 123",
    "ciudad": "Madrid",
    "codigo_postal": "28001",
    "pais": "España"
  },
  
  "subtotal": Decimal128("899.99"),
  "impuestos": Decimal128("189.00"),
  "envio": Decimal128("5.00"),
  "total": Decimal128("1093.99"),
  
  "metodo_pago": "tarjeta",
  "estado_pago": "completado"
}
```

**Colección: reseñas** (Referencing - pueden ser miles)

```javascript
{
  "_id": ObjectId("..."),
  
  // Referencias
  "producto_id": ObjectId("..."),
  "usuario_id": ObjectId("..."),
  
  "puntuacion": 5, // 1-5 estrellas
  "titulo": "Excelente producto",
  "comentario": "Muy satisfecho con la compra...",
  "fecha": ISODate("2024-02-05T00:00:00Z"),
  
  "verificada": true, // ¿El usuario compró el producto?
  "votos_utiles": 12
}
```

### 4.3. Patrón de Atributos (Attribute Pattern)

Para productos con especificaciones variables (problema EAV en SQL):

```javascript
{
  "_id": ObjectId("..."),
  "nombre": "Camiseta Deportiva",
  "precio": Decimal128("24.99"),
  
  // Patrón de atributos para indexación flexible
  "atributos": [
    { "k": "talla", "v": "M" },
    { "k": "color", "v": "azul" },
    { "k": "material", "v": "algodón" }
  ]
}

// Indexar atributos.k y atributos.v permite búsquedas eficientes
// por cualquier combinación de atributos
```


## 5. Operaciones CRUD

### 5.1. Create (Insertar Documentos)

**Insertar un solo documento**:

```python
from bson.decimal128 import Decimal128
from datetime import datetime

producto = {
    "sku": "MOUSE-001",
    "nombre": "Ratón Inalámbrico Logitech",
    "precio": Decimal128("25.99"),
    "stock": 50,
    "categorias": ["electronica", "perifericos"],
    "fecha_creacion": datetime.now(),
    "activo": True
}

resultado = db.productos.insert_one(producto)
print(f"Producto insertado con ID: {resultado.inserted_id}")
```

**Insertar múltiples documentos**:

```python
productos = [
    {
        "sku": "TECLADO-001",
        "nombre": "Teclado Mecánico",
        "precio": Decimal128("89.99"),
        "stock": 30
    },
    {
        "sku": "MONITOR-001",
        "nombre": "Monitor 24 pulgadas",
        "precio": Decimal128("189.99"),
        "stock": 15
    }
]

resultado = db.productos.insert_many(productos)
print(f"Insertados {len(resultado.inserted_ids)} productos")
```

**Manejo de errores en inserciones masivas**:

```python
from pymongo.errors import BulkWriteError

productos = [
    {"_id": 1, "nombre": "Producto A"},
    {"_id": 2, "nombre": "Producto B"},
    {"_id": 2, "nombre": "Producto C"},  # ID duplicado
    {"_id": 3, "nombre": "Producto D"}
]

try:
    # ordered=False: intenta insertar todos, reporta errores al final
    resultado = db.productos.insert_many(productos, ordered=False)
    print(f"Insertados: {len(resultado.inserted_ids)}")
    
except BulkWriteError as e:
    print(f"Documentos insertados: {e.details['nInserted']}")
    print(f"Errores: {len(e.details['writeErrors'])}")
    for error in e.details['writeErrors']:
        print(f"  - Índice {error['index']}: {error['errmsg']}")
```

### 5.2. Read (Consultar Documentos)

**Buscar un documento**:

```python
# Buscar por ID
from bson import ObjectId

producto = db.productos.find_one({"_id": ObjectId("...")})

# Buscar por campo
producto = db.productos.find_one({"sku": "MOUSE-001"})
```

**Buscar múltiples documentos**:

```python
# find() devuelve un cursor (iterador)
cursor = db.productos.find({"activo": True})

# Iterar sobre resultados
for producto in cursor:
    print(producto["nombre"])

# Convertir a lista (cuidado con grandes volúmenes)
productos = list(db.productos.find({"activo": True}))
```

**Operadores de comparación**:

```python
# Mayor que ($gt)
productos_caros = db.productos.find({
    "precio": {"$gt": Decimal128("100.00")}
})

# Mayor o igual ($gte), menor ($lt), menor o igual ($lte)
productos_rango = db.productos.find({
    "precio": {
        "$gte": Decimal128("50.00"),
        "$lte": Decimal128("200.00")
    }
})

# Distinto de ($ne)
productos_activos = db.productos.find({
    "activo": {"$ne": False}
})

# En lista ($in)
productos_categorias = db.productos.find({
    "categorias": {"$in": ["electronica", "informatica"]}
})
```

**Operadores lógicos**:

```python
# AND implícito (comas)
productos = db.productos.find({
    "activo": True,
    "stock": {"$gt": 0}
})

# OR explícito
productos = db.productos.find({
    "$or": [
        {"precio": {"$lt": Decimal128("30.00")}},
        {"categorias": "ofertas"}
    ]
})

# Combinación de AND y OR
productos = db.productos.find({
    "activo": True,
    "$or": [
        {"stock": {"$gt": 100}},
        {"categorias": "destacado"}
    ]
})
```

**Proyecciones (seleccionar campos)**:

```python
# Incluir solo ciertos campos (1 = incluir)
productos = db.productos.find(
    {"activo": True},
    {"nombre": 1, "precio": 1}  # _id se incluye por defecto
)

# Excluir el _id
productos = db.productos.find(
    {"activo": True},
    {"nombre": 1, "precio": 1, "_id": 0}
)

# Excluir campos (0 = excluir)
productos = db.productos.find(
    {},
    {"descripcion": 0, "fecha_creacion": 0}
)
```

**Ordenamiento, límite y salto**:

```python
# Ordenar por precio ascendente (1)
productos = db.productos.find().sort("precio", 1)

# Ordenar por precio descendente (-1)
productos = db.productos.find().sort("precio", -1)

# Ordenamiento múltiple
productos = db.productos.find().sort([
    ("categorias", 1),
    ("precio", -1)
])

# Limitar resultados
productos = db.productos.find().limit(10)

# Saltar resultados (paginación)
productos = db.productos.find().skip(20).limit(10)  # Página 3

# Combinar todo
productos = db.productos.find(
    {"activo": True}
).sort("precio", -1).limit(5)
```

**Consultas en arrays**:

```python
# Documentos que contienen un valor en un array
productos = db.productos.find({
    "categorias": "electronica"  # Coincide si está en el array
})

# Documentos con array que contenga TODOS los valores
productos = db.productos.find({
    "categorias": {"$all": ["electronica", "ofertas"]}
})

# Tamaño del array
productos = db.productos.find({
    "imagenes": {"$size": 3}  # Exactamente 3 imágenes
})
```

**$elemMatch para subdocumentos en arrays**:

```python
# Problema: consulta incorrecta
# Esta consulta busca documentos donde ALGÚN elemento tenga k="color"
# y ALGÚN elemento (puede ser otro) tenga v="rojo"
productos = db.productos.find({
    "atributos.k": "color",
    "atributos.v": "rojo"
})

# Solución: $elemMatch asegura que ambas condiciones se cumplan
# en EL MISMO elemento del array
productos = db.productos.find({
    "atributos": {
        "$elemMatch": {
            "k": "color",
            "v": "rojo"
        }
    }
})
```

**Expresiones regulares**:

```python
# Búsqueda insensible a mayúsculas/minúsculas
productos = db.productos.find({
    "nombre": {"$regex": "laptop", "$options": "i"}
})

# Usando regex de Python
import re
productos = db.productos.find({
    "nombre": re.compile("laptop", re.IGNORECASE)
})
```

### 5.3. Update (Actualizar Documentos)

**Actualizar un documento**:

```python
# $set: establece un valor
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$set": {"precio": Decimal128("22.99")}}
)

# Actualizar múltiples campos
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {
        "$set": {
            "precio": Decimal128("22.99"),
            "stock": 45,
            "ultima_actualizacion": datetime.now()
        }
    }
)
```

**Actualizar múltiples documentos**:

```python
# Actualizar todos los productos de una categoría
resultado = db.productos.update_many(
    {"categorias": "electronica"},
    {"$set": {"disponible_online": True}}
)

print(f"Documentos modificados: {resultado.modified_count}")
```

**Operadores de actualización**:

```python
# $inc: incrementar/decrementar valor numérico
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$inc": {"stock": -5}}  # Restar 5 unidades
)

# $mul: multiplicar
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$mul": {"precio": Decimal128("0.9")}}  # Aplicar 10% descuento
)

# $min: actualizar solo si el nuevo valor es menor
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$min": {"precio": Decimal128("20.00")}}
)

# $max: actualizar solo si el nuevo valor es mayor
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$max": {"stock": 100}}
)

# $unset: eliminar campo
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$unset": {"campo_obsoleto": ""}}
)

# $rename: renombrar campo
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$rename": {"nombre_antiguo": "nombre_nuevo"}}
)
```

**Operadores de arrays**:

```python
# $push: añadir elemento a un array
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$push": {"categorias": "ofertas"}}
)

# $push con $each: añadir múltiples elementos
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$push": {"categorias": {"$each": ["destacado", "nuevo"]}}}
)

# $addToSet: añadir solo si no existe (evita duplicados)
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$addToSet": {"categorias": "electronica"}}
)

# $pull: eliminar elementos que coincidan
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$pull": {"categorias": "ofertas"}}
)

# $pop: eliminar primer (-1) o último (1) elemento
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$pop": {"categorias": 1}}  # Eliminar último
)
```

**Actualización posicional en arrays ($)**:

```python
# Actualizar el primer elemento que coincida
db.usuarios.update_one(
    {
        "_id": ObjectId("..."),
        "carrito.items.producto_id": ObjectId("...")
    },
    {
        "$set": {
            "carrito.items.$.cantidad": 5
        }
    }
)
```

**Actualización con filtros de array ($[])**:

```python
# Actualizar todos los elementos de un array
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {"$set": {"atributos.$[].actualizado": True}}
)

# Actualizar elementos que cumplan una condición
db.usuarios.update_one(
    {"_id": ObjectId("...")},
    {
        "$mul": {
            "carrito.items.$[item].precio_unitario": Decimal128("0.9")
        }
    },
    array_filters=[
        {"item.producto_id": {"$in": [ObjectId("..."), ObjectId("...")]}}
    ]
)
```

**Upsert (Update o Insert)**:

```python
# Si el documento existe, lo actualiza; si no, lo crea
db.productos.update_one(
    {"sku": "NUEVO-001"},
    {
        "$set": {
            "nombre": "Producto Nuevo",
            "precio": Decimal128("49.99")
        },
        "$setOnInsert": {
            "fecha_creacion": datetime.now()
        }
    },
    upsert=True
)
```

### 5.4. Delete (Eliminar Documentos)

**Eliminar un documento**:

```python
resultado = db.productos.delete_one({"sku": "MOUSE-001"})
print(f"Documentos eliminados: {resultado.deleted_count}")
```

**Eliminar múltiples documentos**:

```python
# Eliminar todos los productos inactivos
resultado = db.productos.delete_many({"activo": False})
print(f"Documentos eliminados: {resultado.deleted_count}")
```

**Soft Delete (Recomendado en producción)**:

```python
# En lugar de eliminar, marcar como eliminado
db.productos.update_one(
    {"sku": "MOUSE-001"},
    {
        "$set": {
            "eliminado": True,
            "fecha_eliminacion": datetime.now()
        }
    }
)

# Luego filtrar en las consultas
productos_activos = db.productos.find({"eliminado": {"$ne": True}})
```

## 6. Aggregation Framework

El framework de agregación permite realizar transformaciones y análisis complejos de datos. Es equivalente a las operaciones GROUP BY, JOIN y funciones de ventana en SQL.

### 6.1. Estructura de un Pipeline

Un pipeline de agregación es una secuencia de etapas que procesan documentos:

```python
pipeline = [
    # Etapa 1: Filtrar
    { "$match": { ... } },
    
    # Etapa 2: Agrupar
    { "$group": { ... } },
    
    # Etapa 3: Ordenar
    { "$sort": { ... } }
]

resultados = db.coleccion.aggregate(pipeline)
```

### 6.2. Etapas Principales

**$match - Filtrar documentos**:

```python
# Similar a find(), pero dentro del pipeline
pipeline = [
    {
        "$match": {
            "estado": "completado",
            "fecha_pedido": {
                "$gte": datetime(2024, 1, 1),
                "$lt": datetime(2024, 2, 1)
            }
        }
    }
]
```

**$project - Seleccionar y transformar campos**:

```python
pipeline = [
    {
        "$project": {
            "nombre": 1,
            "precio": 1,
            # Crear campo calculado
            "precio_con_iva": {
                "$multiply": ["$precio", 1.21]
            },
            # Renombrar campo
            "descripcion_producto": "$descripcion",
            # Excluir _id
            "_id": 0
        }
    }
]
```

**$group - Agrupar y agregar**:

```python
# Contar productos por categoría
pipeline = [
    {
        "$unwind": "$categorias"  # Desenrollar array
    },
    {
        "$group": {
            "_id": "$categorias",  # Campo de agrupación
            "total_productos": { "$sum": 1 },
            "precio_promedio": { "$avg": "$precio" },
            "precio_minimo": { "$min": "$precio" },
            "precio_maximo": { "$max": "$precio" }
        }
    }
]

# Agrupar sin campo específico (agregar todos los documentos)
pipeline = [
    {
        "$group": {
            "_id": None,
            "total_productos": { "$sum": 1 },
            "valor_total_inventario": {
                "$sum": { "$multiply": ["$precio", "$stock"] }
            }
        }
    }
]
```

**$unwind - Desenrollar arrays**:

```python
# Documento original:
# { "_id": 1, "items": ["A", "B", "C"] }

# Después de $unwind:
# { "_id": 1, "items": "A" }
# { "_id": 1, "items": "B" }
# { "_id": 1, "items": "C" }

pipeline = [
    { "$unwind": "$items" }
]
```

**$sort - Ordenar**:

```python
pipeline = [
    {
        "$sort": {
            "precio": -1,  # Descendente
            "nombre": 1    # Ascendente
        }
    }
]
```

**$limit y $skip - Paginación**:

```python
pipeline = [
    { "$sort": { "precio": -1 } },
    { "$skip": 10 },   # Saltar primeros 10
    { "$limit": 10 }   # Tomar siguientes 10
]
```

**$lookup - JOIN entre colecciones**:

```python
# Unir pedidos con información de usuarios
pipeline = [
    {
        "$lookup": {
            "from": "usuarios",           # Colección a unir
            "localField": "usuario_id",   # Campo en pedidos
            "foreignField": "_id",        # Campo en usuarios
            "as": "info_usuario"          # Nombre del array resultante
        }
    }
]

# El resultado incluirá:
# {
#   "_id": ObjectId("..."),
#   "usuario_id": ObjectId("..."),
#   "total": 100,
#   "info_usuario": [
#     { "_id": ObjectId("..."), "nombre": "Ana", ... }
#   ]
# }

# Desenrollar el resultado del lookup
pipeline = [
    {
        "$lookup": {
            "from": "usuarios",
            "localField": "usuario_id",
            "foreignField": "_id",
            "as": "info_usuario"
        }
    },
    {
        "$unwind": "$info_usuario"  # Convertir array a objeto
    }
]
```

### 6.3. Ejemplo Completo: Reporte de Ventas

```python
from datetime import datetime
from bson.decimal128 import Decimal128

# Reporte de ventas por categoría en enero 2024
pipeline = [
    # 1. Filtrar pedidos completados en enero
    {
        "$match": {
            "estado": "completado",
            "fecha_pedido": {
                "$gte": datetime(2024, 1, 1),
                "$lt": datetime(2024, 2, 1)
            }
        }
    },
    
    # 2. Desenrollar items del pedido
    {
        "$unwind": "$items"
    },
    
    # 3. Hacer JOIN con productos para obtener categorías
    {
        "$lookup": {
            "from": "productos",
            "localField": "items.producto_id",
            "foreignField": "_id",
            "as": "producto_info"
        }
    },
    
    # 4. Desenrollar el resultado del lookup
    {
        "$unwind": "$producto_info"
    },
    
    # 5. Desenrollar categorías del producto
    {
        "$unwind": "$producto_info.categorias"
    },
    
    # 6. Agrupar por categoría y calcular métricas
    {
        "$group": {
            "_id": "$producto_info.categorias",
            "total_ventas": {
                "$sum": "$items.subtotal"
            },
            "cantidad_productos": {
                "$sum": "$items.cantidad"
            },
            "numero_pedidos": {
                "$sum": 1
            },
            "ticket_promedio": {
                "$avg": "$items.subtotal"
            }
        }
    },
    
    # 7. Ordenar por ventas descendente
    {
        "$sort": { "total_ventas": -1 }
    },
    
    # 8. Formatear resultado
    {
        "$project": {
            "_id": 0,
            "categoria": "$_id",
            "total_ventas": 1,
            "cantidad_productos": 1,
            "numero_pedidos": 1,
            "ticket_promedio": 1
        }
    }
]

# Ejecutar agregación
resultados = db.pedidos.aggregate(pipeline, allowDiskUse=True)

# Mostrar resultados
for resultado in resultados:
    print(f"Categoría: {resultado['categoria']}")
    print(f"  Ventas totales: €{resultado['total_ventas']}")
    print(f"  Productos vendidos: {resultado['cantidad_productos']}")
    print(f"  Número de pedidos: {resultado['numero_pedidos']}")
    print(f"  Ticket promedio: €{resultado['ticket_promedio']:.2f}")
    print()
```


## 7. Índices y Optimización

### 7.1. ¿Por Qué Necesitamos Índices?

Sin índices, MongoDB debe escanear toda la colección (Collection Scan) para encontrar documentos, lo cual es ineficiente con grandes volúmenes de datos.

**Ejemplo sin índice**:
```python
# Buscar producto por SKU sin índice
# MongoDB escanea TODOS los documentos
producto = db.productos.find_one({"sku": "LAPTOP-001"})
```

**Ejemplo con índice**:
```python
# Crear índice en SKU
db.productos.create_index("sku")

# Ahora la búsqueda es instantánea
producto = db.productos.find_one({"sku": "LAPTOP-001"})
```

### 7.2. Tipos de Índices

**Índice de campo único**:

```python
# Índice ascendente
db.productos.create_index("sku")

# Índice descendente (útil para ordenamiento)
db.productos.create_index([("precio", -1)])

# Índice único (garantiza unicidad)
db.usuarios.create_index("email", unique=True)
```

**Índice compuesto**:

```python
# Índice en múltiples campos
# El orden importa: diseñar según la Regla ESR
db.pedidos.create_index([
    ("estado", 1),      # E: Equality (igualdad)
    ("fecha_pedido", -1), # S: Sort (ordenamiento)
    ("total", 1)        # R: Range (rango)
])
```

**Regla ESR (Equality, Sort, Range)**:

1. Campos de igualdad primero
2. Campos de ordenamiento después
3. Campos de rango al final

```python
# Consulta optimizada con índice ESR
pedidos = db.pedidos.find({
    "estado": "completado",  # Equality
    "total": {"$gt": Decimal128("100.00")}  # Range
}).sort("fecha_pedido", -1)  # Sort

# Crear índice correspondiente
db.pedidos.create_index([
    ("estado", 1),
    ("fecha_pedido", -1),
    ("total", 1)
])
```

**Índice multikey (arrays)**:

```python
# MongoDB automáticamente crea índice multikey para arrays
db.productos.create_index("categorias")

# Ahora búsquedas en arrays son eficientes
productos = db.productos.find({"categorias": "electronica"})
```

**Índice de texto**:

```python
# Crear índice de texto para búsqueda full-text
db.productos.create_index({
    "nombre": "text",
    "descripcion": "text"
})

# Buscar productos que contengan palabras
productos = db.productos.find({
    "$text": {"$search": "laptop gaming"}
})
```

### 7.3. Gestión de Índices

**Listar índices**:

```python
indices = db.productos.list_indexes()
for indice in indices:
    print(indice)
```

**Eliminar índice**:

```python
# Por nombre
db.productos.drop_index("sku_1")

# Por especificación
db.productos.drop_index([("sku", 1)])

# Eliminar todos excepto _id
db.productos.drop_indexes()
```

**Información de índices**:

```python
# Ver estadísticas de índices
stats = db.command("collstats", "productos")
print(stats["indexSizes"])
```

### 7.4. Análisis de Consultas con explain()

```python
# Analizar plan de ejecución
explicacion = db.productos.find(
    {"sku": "LAPTOP-001"}
).explain()

# Revisar información clave
print(f"Tipo de escaneo: {explicacion['queryPlanner']['winningPlan']['stage']}")
# COLLSCAN = Collection Scan (sin índice) - MALO
# IXSCAN = Index Scan (usa índice) - BUENO

# Estadísticas de ejecución
explicacion_detallada = db.productos.find(
    {"sku": "LAPTOP-001"}
).explain("executionStats")

stats = explicacion_detallada["executionStats"]
print(f"Documentos examinados: {stats['totalDocsExamined']}")
print(f"Documentos devueltos: {stats['nReturned']}")
print(f"Tiempo: {stats['executionTimeMillis']} ms")

# Idealmente: totalDocsExamined == nReturned
```

## 8. Transacciones

Desde MongoDB 4.0, se soportan transacciones ACID multi-documento.

### 8.1. Cuándo Usar Transacciones

**Usar transacciones para**:
- Operaciones que afectan múltiples documentos que deben ser atómicas
- Transferencias de dinero entre cuentas
- Reservas que requieren múltiples actualizaciones

**Evitar transacciones para**:
- Operaciones en un solo documento (ya son atómicas)
- Cargas masivas de datos
- Operaciones de lectura

### 8.2. Ejemplo de Transacción

```python
from pymongo import MongoClient

cliente = MongoClient("mongodb://admin:password123@localhost:27017/")
db = cliente["tienda_db"]

# Iniciar sesión
with cliente.start_session() as session:
    try:
        # Iniciar transacción
        session.start_transaction()
        
        # Operación 1: Reducir stock
        db.productos.update_one(
            {"sku": "LAPTOP-001"},
            {"$inc": {"stock": -1}},
            session=session
        )
        
        # Operación 2: Crear pedido
        pedido = {
            "usuario_id": ObjectId("..."),
            "items": [...],
            "total": Decimal128("899.99"),
            "estado": "pendiente"
        }
        db.pedidos.insert_one(pedido, session=session)
        
        # Confirmar transacción
        session.commit_transaction()
        print("✅ Transacción completada")
        
    except Exception as e:
        # Revertir en caso de error
        session.abort_transaction()
        print(f"❌ Error en transacción: {e}")
```

## 9. Mejores Prácticas

### 9.1. Diseño de Esquema

1. **Diseña basándote en patrones de acceso**, no en normalización
2. **Embebe datos que se leen juntos**
3. **Referencia datos que cambian frecuentemente** o tienen relaciones N:M
4. **Usa el patrón Snapshot** para datos históricos (precios, direcciones)
5. **Respeta el límite de 16 MB** por documento

### 9.2. Rendimiento

1. **Crea índices para todas las consultas frecuentes**
2. **Usa `explain()` para verificar** que las consultas usan índices
3. **Proyecta solo los campos necesarios** para reducir transferencia de datos
4. **Usa agregación para análisis complejos** en lugar de procesar en Python
5. **Habilita `allowDiskUse=True`** para agregaciones grandes

### 9.3. Seguridad

1. **Nunca desactives la autenticación** en producción
2. **Usa variables de entorno** para credenciales
3. **Aplica principio de mínimo privilegio** (crea usuarios con permisos específicos)
4. **Habilita SSL/TLS** para conexiones en producción
5. **Audita accesos** a la base de datos

### 9.4. Mantenimiento

1. **Realiza backups regulares** con `mongodump`
2. **Monitorea métricas** de rendimiento
3. **Revisa logs** periódicamente
4. **Actualiza MongoDB** a versiones estables más recientes
5. **Documenta el esquema** y patrones de uso

## 10. Ejercicio Práctico Completo: CRUD con MongoDB Compass

### 10.1. Preparación del Entorno

**Instalación de MongoDB Compass**:

MongoDB Compass es la interfaz gráfica oficial de MongoDB. Descárgala desde [mongodb.com/products/compass](https://www.mongodb.com/products/compass).

**Conexión a MongoDB**:

1. Abre MongoDB Compass
2. En la pantalla de conexión, usa la siguiente URI:
   ```
   mongodb://admin:password123@localhost:27017/
   ```
3. Haz clic en "Connect"

### 10.2. Creación de la Base de Datos y Colección

1. En el panel izquierdo, haz clic en "Create Database"
2. Introduce:
   - **Database name**: `tienda_practica`
   - **Collection name**: `productos`
3. Haz clic en "Create Database"

### 10.3. Ejercicio Paso a Paso

#### Paso 1: Insertar Productos (CREATE)

1. Selecciona la base de datos `tienda_practica` y la colección `productos`
2. Haz clic en la pestaña "Documents"
3. Haz clic en "ADD DATA" → "Insert Document"
4. Introduce el siguiente documento:

```json
{
  "sku": "PORT-001",
  "nombre": "Portátil Dell XPS 15",
  "descripcion": "Portátil profesional de alto rendimiento",
  "precio": 1299.99,
  "stock": 15,
  "categorias": ["electronica", "informatica", "portatiles"],
  "especificaciones": {
    "procesador": "Intel Core i7-11800H",
    "ram": "16GB DDR4",
    "almacenamiento": "512GB SSD",
    "pantalla": "15.6 pulgadas 4K"
  },
  "imagenes": [
    {
      "url": "https://ejemplo.com/dell-xps-1.jpg",
      "es_principal": true
    }
  ],
  "activo": true
}
```

5. Haz clic en "Insert"

**Inserta 4 productos más** usando el botón "INSERT DOCUMENT":

```json
{
  "sku": "RATON-001",
  "nombre": "Ratón Logitech MX Master 3",
  "precio": 89.99,
  "stock": 50,
  "categorias": ["electronica", "perifericos"],
  "activo": true
}
```

```json
{
  "sku": "TECLADO-001",
  "nombre": "Teclado Mecánico Keychron K2",
  "precio": 79.99,
  "stock": 30,
  "categorias": ["electronica", "perifericos"],
  "activo": true
}
```

```json
{
  "sku": "MONITOR-001",
  "nombre": "Monitor LG 27 pulgadas 4K",
  "precio": 399.99,
  "stock": 20,
  "categorias": ["electronica", "monitores"],
  "activo": true
}
```

```json
{
  "sku": "TABLET-001",
  "nombre": "iPad Air 2024",
  "precio": 649.99,
  "stock": 0,
  "categorias": ["electronica", "tablets"],
  "activo": false
}
```

#### Paso 2: Consultar Productos (READ)

**Consulta 1: Buscar todos los productos**

1. En la pestaña "Documents", el filtro por defecto es `{}`
2. Esto muestra todos los documentos

**Consulta 2: Buscar productos activos**

1. En el campo de filtro, introduce:
```json
{ "activo": true }
```
2. Haz clic en "Find"

**Consulta 3: Buscar productos con stock > 20**

```json
{ "stock": { "$gt": 20 } }
```

**Consulta 4: Buscar productos de categoría "perifericos"**

```json
{ "categorias": "perifericos" }
```

**Consulta 5: Buscar productos con precio entre 70 y 100 euros**

```json
{ 
  "precio": { 
    "$gte": 70, 
    "$lte": 100 
  } 
}
```

**Consulta 6: Productos activos con stock disponible**

```json
{
  "activo": true,
  "stock": { "$gt": 0 }
}
```

**Consulta 7: Buscar por texto en el nombre (expresión regular)**

```json
{ 
  "nombre": { 
    "$regex": "ratón", 
    "$options": "i" 
  } 
}
```

#### Paso 3: Actualizar Productos (UPDATE)

**Actualización 1: Reducir precio del ratón**

1. Busca el documento con SKU "RATON-001"
2. Haz clic en el ícono de lápiz (editar) en ese documento
3. Modifica el campo `precio` a `79.99`
4. Haz clic en "Update"

**Actualización 2: Actualizar stock usando filtros**

1. Ve a la pestaña "Documents"
2. Filtra: `{ "sku": "PORT-001" }`
3. Edita el documento y cambia `stock` a `12`
4. Haz clic en "Update"

**Actualización 3: Añadir categoría a un producto**

1. Busca el portátil (PORT-001)
2. Edita el documento
3. En el array `categorias`, añade `"oferta"`
4. El array debería verse así:
```json
"categorias": ["electronica", "informatica", "portatiles", "oferta"]
```
5. Haz clic en "Update"

**Actualización 4: Marcar producto como inactivo**

1. Busca el teclado (TECLADO-001)
2. Edita el documento
3. Cambia `"activo": true` a `"activo": false`
4. Haz clic en "Update"

#### Paso 4: Eliminar Productos (DELETE)

**Eliminación 1: Eliminar un producto específico**

1. Busca la tablet: `{ "sku": "TABLET-001" }`
2. Haz clic en el ícono de papelera (eliminar) en ese documento
3. Confirma la eliminación

**Verificación**: Busca todos los productos activos para confirmar que la tablet ya no está.

#### Paso 5: Agregaciones en Compass

**Agregación 1: Contar productos por categoría**

1. Ve a la pestaña "Aggregations"
2. Haz clic en "ADD STAGE"
3. **Stage 1**: Selecciona `$unwind`
   ```json
   {
     "path": "$categorias"
   }
   ```

4. **Stage 2**: Añade otra etapa, selecciona `$group`
   ```json
   {
     "_id": "$categorias",
     "total": { "$sum": 1 }
   }
   ```

5. **Stage 3**: Añade otra etapa, selecciona `$sort`
   ```json
   {
     "total": -1
   }
   ```

6. Haz clic en "Run" para ver los resultados

**Agregación 2: Calcular valor total del inventario**

1. Nueva agregación
2. **Stage 1**: `$match` para productos activos
   ```json
   {
     "activo": true
   }
   ```

3. **Stage 2**: `$project` para calcular valor
   ```json
   {
     "nombre": 1,
     "valor_inventario": {
       "$multiply": ["$precio", "$stock"]
     }
   }
   ```

4. **Stage 3**: `$group` para sumar total
   ```json
   {
     "_id": null,
     "valor_total": { "$sum": "$valor_inventario" }
   }
   ```

5. Haz clic en "Run"

#### Paso 6: Crear Índices

1. Ve a la pestaña "Indexes"
2. Haz clic en "CREATE INDEX"
3. En el campo, introduce:
   ```json
   {
     "sku": 1
   }
   ```
4. Marca "Create unique index"
5. Haz clic en "Create Index"

**Verificación**: Intenta insertar un producto con un SKU duplicado y observa el error.

#### Paso 7: Análisis de Consultas (Explain Plan)

1. Ve a la pestaña "Explain Plan"
2. Introduce una consulta:
   ```json
   { "sku": "PORT-001" }
   ```
3. Haz clic en "Explain"
4. Observa:
   - **Query** usa índice "IXSCAN" (Index Scan)
   - **Documents Examined** = 1
   - **Documents Returned** = 1

5. Ahora prueba sin índice:
   - Elimina el índice `sku_1` en la pestaña "Indexes"
   - Vuelve a "Explain Plan" y ejecuta la misma consulta
   - Observa que ahora usa "COLLSCAN" (Collection Scan)
   - **Documents Examined** = todos los documentos

### 10.4. Ejercicio Adicional con Python

Ahora replica las mismas operaciones usando PyMongo:

```python
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from datetime import datetime

# Conectar
cliente = MongoClient("mongodb://admin:password123@localhost:27017/")
db = cliente['tienda_practica']
productos = db['productos']

# 1. CREATE - Insertar un producto nuevo
nuevo_producto = {
    "sku": "CAMARA-001",
    "nombre": "Cámara Canon EOS R6",
    "precio": Decimal128("2499.99"),
    "stock": 8,
    "categorias": ["electronica", "fotografia"],
    "activo": True,
    "fecha_creacion": datetime.now()
}
resultado = productos.insert_one(nuevo_producto)
print(f"✅ Producto insertado con ID: {resultado.inserted_id}")

# 2. READ - Buscar productos activos con stock
activos = productos.find({
    "activo": True,
    "stock": {"$gt": 0}
})
print("\n📦 Productos activos con stock:")
for producto in activos:
    print(f"  - {producto['nombre']}: {producto['stock']} unidades")

# 3. UPDATE - Aplicar descuento del 10% a periféricos
resultado = productos.update_many(
    {"categorias": "perifericos"},
    {"$mul": {"precio": Decimal128("0.9")}}
)
print(f"\n💰 Descuento aplicado a {resultado.modified_count} productos")

# 4. DELETE - Eliminar productos sin stock e inactivos
resultado = productos.delete_many({
    "stock": 0,
    "activo": False
})
print(f"\n🗑️ Eliminados {resultado.deleted_count} productos")

# 5. AGGREGATION - Reporte de inventario
pipeline = [
    {"$match": {"activo": True}},
    {"$group": {
        "_id": None,
        "total_productos": {"$sum": 1},
        "total_unidades": {"$sum": "$stock"},
        "valor_total": {"$sum": {"$multiply": ["$precio", "$stock"]}}
    }}
]
reporte = list(productos.aggregate(pipeline))
if reporte:
    print("\n📊 Reporte de inventario:")
    print(f"  Total productos: {reporte[0]['total_productos']}")
    print(f"  Total unidades: {reporte[0]['total_unidades']}")
    print(f"  Valor total: €{reporte[0]['valor_total']}")

# Cerrar conexión
cliente.close()
```

## Conclusión

MongoDB ofrece una alternativa flexible y escalable a las bases de datos relacionales tradicionales. Los conceptos clave son:

1. **Documentos flexibles** permiten modelar datos de forma natural
2. **Embedding vs Referencing** es la decisión de diseño más importante
3. **Aggregation Framework** proporciona capacidades analíticas potentes
4. **Índices** son esenciales para el rendimiento
5. **Docker** facilita la gestión del entorno de desarrollo




## Recursos Adicionales

- **Documentación oficial**: [docs.mongodb.com](https://docs.mongodb.com)
- **Universidad MongoDB**: [university.mongodb.com](https://university.mongodb.com)
- **PyMongo Documentation**: [pymongo.readthedocs.io](https://pymongo.readthedocs.io)
- **MongoDB Compass**: [mongodb.com/products/compass](https://www.mongodb.com/products/compass)