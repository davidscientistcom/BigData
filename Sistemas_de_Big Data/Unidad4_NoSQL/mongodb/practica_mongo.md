# **MongoDB con Python - De SQL a NoSQL**


# **0. Configuración del entorno**

## **Instalación de librerías**

```bash
# Instalación básica
pip install pymongo

# Para trabajar con fechas y tipos avanzados
pip install python-dateutil

# Opcional: para trabajo asíncrono
pip install motor
```

## **Conexión a MongoDB**

### **Conexión local**

```python
from pymongo import MongoClient
from datetime import datetime

# Conexión básica a MongoDB local
client = MongoClient('mongodb://localhost:27017/')

# Seleccionar base de datos
db = client['universidad']

# Seleccionar colección (equivalente a tabla en SQL)
estudiantes = db['estudiantes']

# Verificar conexión
try:
    client.admin.command('ping')
    print("✓ Conexión exitosa a MongoDB")
except Exception as e:
    print(f"✗ Error de conexión: {e}")
```

### **Conexión a MongoDB Atlas (nube)**

```python
# URI de conexión a Atlas
uri = "mongodb+srv://usuario:password@cluster.mongodb.net/"
client = MongoClient(uri)
db = client['universidad']
```

### **Buenas prácticas de conexión**

```python
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class DatabaseConnection:
    def __init__(self):
        self.uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.client = None
        self.db = None
    
    def connect(self, db_name='universidad'):
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Verificar conexión
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            print(f"✓ Conectado a la base de datos '{db_name}'")
            return self.db
        except ConnectionFailure as e:
            print(f"✗ No se pudo conectar a MongoDB: {e}")
            return None
    
    def close(self):
        if self.client:
            self.client.close()
            print("✓ Conexión cerrada")

# Uso
db_conn = DatabaseConnection()
db = db_conn.connect('universidad')
```



# **1. Introducción: SQL vs MongoDB**

## **1.1 Paradigma relacional vs documental**

| **Concepto SQL** | **Concepto MongoDB** | **Descripción** |
|------------------|----------------------|-----------------|
| Base de datos | Base de datos (database) | Contenedor principal |
| Tabla | Colección (collection) | Conjunto de registros |
| Fila / Registro | Documento (document) | Unidad de datos |
| Columna | Campo (field) | Atributo individual |
| PRIMARY KEY | _id | Identificador único (auto-generado) |
| FOREIGN KEY | Referencia o embedding | Relaciones entre documentos |
| JOIN | $lookup o embedding | Combinación de datos |
| INDEX | Index | Optimización de consultas |
| TRANSACTION | Transaction | Operaciones atómicas |

## **1.2 Diferencias fundamentales**

### **SQL (Relacional)**
```sql
-- Estructura rígida, esquema fijo
CREATE TABLE estudiantes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    edad INT,
    fecha_registro DATE
);
```

### **MongoDB (Documental)**
```python
# Estructura flexible, esquema dinámico
estudiante = {
    "_id": ObjectId("..."),  # Auto-generado
    "nombre": "María García",
    "email": "maria@example.com",
    "edad": 22,
    "fecha_registro": datetime(2024, 9, 1),
    # Campos opcionales/dinámicos
    "telefono": "+34612345678",  # Algunos estudiantes lo tienen
    "direccion": {  # Subdocumento anidado
        "calle": "Gran Vía 123",
        "ciudad": "Madrid",
        "cp": "28013"
    },
    "cursos": ["Python", "MongoDB", "Docker"]  # Array
}
```

## **1.3 ¿Cuándo usar MongoDB vs SQL?**

### **Usa MongoDB cuando:**
- Los datos tienen estructura variable o evolucionan frecuentemente
- Necesitas alta escalabilidad horizontal
- Trabajas con datos jerárquicos o anidados
- Requieres flexibilidad en el esquema
- Tienes documentos complejos (JSON/BSON)

### **Usa SQL cuando:**
- Necesitas transacciones complejas y múltiples relaciones
- El esquema es estable y bien definido
- Requieres integridad referencial estricta
- Realizas muchas operaciones JOIN complejas
- El modelo relacional encaja naturalmente

## **1.4 El concepto de _id**

```python
from bson import ObjectId

# MongoDB genera automáticamente un _id si no lo proporcionas
doc1 = {"nombre": "Juan"}
estudiantes.insert_one(doc1)
print(doc1["_id"])  # ObjectId('65f1a2b3c4d5e6f7g8h9i0j1')

# Puedes especificar tu propio _id
doc2 = {
    "_id": "EST001",  # Puede ser string, int, ObjectId...
    "nombre": "Ana"
}
estudiantes.insert_one(doc2)

# ObjectId contiene información temporal
oid = ObjectId()
print(f"Timestamp: {oid.generation_time}")  # Fecha de creación
```



# **2. CREATE - Inserción de documentos**

## **2.1 SQL vs MongoDB**

### **SQL**
```sql
-- Insertar un registro
INSERT INTO estudiantes (nombre, email, edad) 
VALUES ('Carlos Ruiz', 'carlos@example.com', 24);

-- Insertar múltiples
INSERT INTO estudiantes (nombre, email, edad) VALUES
    ('Ana López', 'ana@example.com', 22),
    ('Luis Martín', 'luis@example.com', 23);
```

### **MongoDB**
```python
# Insertar un documento
from pymongo import MongoClient
from datetime import datetime

db = MongoClient()['universidad']
estudiantes = db['estudiantes']

# insert_one() - retorna InsertOneResult
resultado = estudiantes.insert_one({
    "nombre": "Carlos Ruiz",
    "email": "carlos@example.com",
    "edad": 24,
    "fecha_registro": datetime.now()
})

print(f"ID insertado: {resultado.inserted_id}")
print(f"¿Insertado? {resultado.acknowledged}")

# insert_many() - insertar múltiples documentos
documentos = [
    {"nombre": "Ana López", "email": "ana@example.com", "edad": 22},
    {"nombre": "Luis Martín", "email": "luis@example.com", "edad": 23}
]

resultado = estudiantes.insert_many(documentos)
print(f"IDs insertados: {resultado.inserted_ids}")
```

## **2.2 Tipos de datos BSON**

```python
from bson import ObjectId, Decimal128
from datetime import datetime
import uuid

# Documento con todos los tipos comunes
documento_completo = {
    # Tipos básicos
    "_id": ObjectId(),                    # ObjectId único
    "nombre": "María García",             # String
    "edad": 28,                           # Int32
    "activo": True,                       # Boolean
    "salario": 45000.50,                  # Double (float)
    "salario_preciso": Decimal128("45000.50"),  # Decimal128 (precisión)
    
    # Fechas y tiempo
    "fecha_nacimiento": datetime(1995, 3, 15),
    "fecha_registro": datetime.now(),
    
    # Identificadores
    "uuid": uuid.uuid4(),                 # UUID
    
    # Valores nulos
    "telefono_secundario": None,          # Null
    
    # Arrays
    "hobbies": ["lectura", "natación", "música"],
    "calificaciones": [8.5, 9.0, 7.5, 9.5],
    
    # Subdocumentos (objetos anidados)
    "direccion": {
        "calle": "Calle Mayor 10",
        "ciudad": "Valencia",
        "codigo_postal": "46001",
        "coordenadas": {
            "lat": 39.4699,
            "lon": -0.3763
        }
    },
    
    # Array de subdocumentos
    "contactos": [
        {"tipo": "email", "valor": "maria@example.com"},
        {"tipo": "telefono", "valor": "+34612345678"}
    ],
    
    # Binario
    "avatar": b'\x89PNG\r\n\x1a\n...',    # Binary data
}

estudiantes.insert_one(documento_completo)
```

## **2.3 Manejo del _id**

```python
# 1. Auto-generado (recomendado)
doc1 = {"nombre": "Juan"}
result = estudiantes.insert_one(doc1)
print(doc1["_id"])  # MongoDB añade el _id al documento original

# 2. _id personalizado (string)
estudiantes.insert_one({
    "_id": "EST2024001",
    "nombre": "Pedro"
})

# 3. _id personalizado (entero)
estudiantes.insert_one({
    "_id": 1001,
    "nombre": "Laura"
})

# 4. _id compuesto (para claves naturales)
estudiantes.insert_one({
    "_id": {"curso": 2024, "numero": 1},
    "nombre": "Sofia"
})
```

## **2.4 Validación y manejo de errores**

```python
from pymongo.errors import DuplicateKeyError, WriteError

# Ejemplo 1: Error por _id duplicado
try:
    estudiantes.insert_one({"_id": "EST001", "nombre": "Carlos"})
    estudiantes.insert_one({"_id": "EST001", "nombre": "Ana"})  # Error
except DuplicateKeyError as e:
    print(f"Error: El _id ya existe - {e}")

# Ejemplo 2: Inserción masiva con manejo de errores
documentos = [
    {"_id": 1, "nombre": "Usuario1"},
    {"_id": 2, "nombre": "Usuario2"},
    {"_id": 1, "nombre": "Duplicado"},  # Este fallará
    {"_id": 3, "nombre": "Usuario3"}
]

try:
    # ordered=False permite continuar después de un error
    resultado = estudiantes.insert_many(documentos, ordered=False)
except DuplicateKeyError as e:
    print(f"Algunos documentos no se insertaron: {e}")
    print(f"Insertados exitosamente: {e.details['nInserted']}")

# Ejemplo 3: Validación antes de insertar
def insertar_estudiante(nombre, email, edad):
    # Validaciones básicas
    if not nombre or len(nombre) < 2:
        return {"error": "Nombre inválido"}
    
    if not email or "@" not in email:
        return {"error": "Email inválido"}
    
    if edad < 16 or edad > 100:
        return {"error": "Edad fuera de rango"}
    
    # Verificar email duplicado
    if estudiantes.find_one({"email": email}):
        return {"error": "Email ya registrado"}
    
    try:
        resultado = estudiantes.insert_one({
            "nombre": nombre,
            "email": email,
            "edad": edad,
            "fecha_registro": datetime.now()
        })
        return {"success": True, "id": resultado.inserted_id}
    except Exception as e:
        return {"error": str(e)}

# Uso
print(insertar_estudiante("María", "maria@example.com", 22))
```

## **2.5 Inserción con valores por defecto**

```python
from datetime import datetime

def crear_estudiante(nombre, email, **kwargs):
    """
    Crea un estudiante con valores por defecto
    """
    documento = {
        "nombre": nombre,
        "email": email,
        "edad": kwargs.get("edad", 18),
        "activo": kwargs.get("activo", True),
        "fecha_registro": datetime.now(),
        "fecha_modificacion": datetime.now(),
        "notas": [],
        "cursos_matriculados": [],
        "metadata": {
            "version": 1,
            "creado_por": "sistema"
        }
    }
    
    # Añadir campos opcionales si se proporcionan
    if "telefono" in kwargs:
        documento["telefono"] = kwargs["telefono"]
    
    if "direccion" in kwargs:
        documento["direccion"] = kwargs["direccion"]
    
    resultado = estudiantes.insert_one(documento)
    return resultado.inserted_id

# Uso
id1 = crear_estudiante("Juan", "juan@example.com")
id2 = crear_estudiante("Ana", "ana@example.com", edad=25, telefono="+34600000")
```



# **3. READ - Consultas (el equivalente al SELECT)**

## **3.1 SELECT básico**

### **SQL vs MongoDB**

```sql
-- SQL: Seleccionar todo
SELECT * FROM estudiantes;

-- SQL: Seleccionar campos específicos
SELECT nombre, email FROM estudiantes;

-- SQL: Un solo resultado
SELECT * FROM estudiantes WHERE id = 1;
```

```python
# MongoDB: Seleccionar todo
estudiantes.find({})

# Iterar resultados
for estudiante in estudiantes.find({}):
    print(estudiante)

# MongoDB: Seleccionar campos específicos (proyección)
estudiantes.find({}, {"nombre": 1, "email": 1, "_id": 0})

# Resultado
for est in estudiantes.find({}, {"nombre": 1, "email": 1, "_id": 0}):
    print(est)  # {"nombre": "María", "email": "maria@example.com"}

# MongoDB: Un solo documento
estudiante = estudiantes.find_one({"_id": ObjectId("...")})
print(estudiante)

# Si no existe, devuelve None
resultado = estudiantes.find_one({"email": "noexiste@example.com"})
if resultado is None:
    print("No encontrado")
```

### **Diferencia entre find() y find_one()**

```python
# find() retorna un cursor (iterable)
cursor = estudiantes.find({"edad": 22})
print(type(cursor))  # <class 'pymongo.cursor.Cursor'>

# Convertir a lista (cuidado con grandes volúmenes)
lista = list(estudiantes.find({"edad": 22}))

# find_one() retorna un diccionario o None
estudiante = estudiantes.find_one({"edad": 22})
print(type(estudiante))  # <class 'dict'> o NoneType
```

## **3.2 WHERE - Filtros**

### **Comparadores**

```sql
-- SQL
SELECT * FROM estudiantes WHERE edad = 22;
SELECT * FROM estudiantes WHERE edad > 22;
SELECT * FROM estudiantes WHERE edad >= 22;
SELECT * FROM estudiantes WHERE edad < 22;
SELECT * FROM estudiantes WHERE edad <= 22;
SELECT * FROM estudiantes WHERE edad != 22;
```

```python
# MongoDB - Operadores de comparación

# Igual ($eq - implícito)
estudiantes.find({"edad": 22})
estudiantes.find({"edad": {"$eq": 22}})  # Equivalente explícito

# Mayor que ($gt)
estudiantes.find({"edad": {"$gt": 22}})

# Mayor o igual ($gte)
estudiantes.find({"edad": {"$gte": 22}})

# Menor que ($lt)
estudiantes.find({"edad": {"$lt": 22}})

# Menor o igual ($lte)
estudiantes.find({"edad": {"$lte": 22}})

# Diferente ($ne)
estudiantes.find({"edad": {"$ne": 22}})

# Rangos (combinar operadores)
# SQL: WHERE edad BETWEEN 20 AND 25
estudiantes.find({"edad": {"$gte": 20, "$lte": 25}})
```

### **Operadores lógicos**

```sql
-- SQL
SELECT * FROM estudiantes WHERE edad > 20 AND activo = true;
SELECT * FROM estudiantes WHERE edad < 18 OR edad > 65;
SELECT * FROM estudiantes WHERE NOT (edad < 18);
```

```python
# MongoDB - Operadores lógicos

# AND implícito (múltiples condiciones en el mismo nivel)
estudiantes.find({
    "edad": {"$gt": 20},
    "activo": True
})

# AND explícito ($and) - necesario para condiciones sobre el mismo campo
estudiantes.find({
    "$and": [
        {"edad": {"$gt": 18}},
        {"edad": {"$lt": 65}}
    ]
})

# OR ($or)
estudiantes.find({
    "$or": [
        {"edad": {"$lt": 18}},
        {"edad": {"$gt": 65}}
    ]
})

# NOT ($not) - sobre un campo específico
estudiantes.find({
    "edad": {"$not": {"$lt": 18}}
})

# NOR ($nor) - ninguna condición se cumple
estudiantes.find({
    "$nor": [
        {"activo": False},
        {"edad": {"$lt": 18}}
    ]
})

# Combinar operadores complejos
# SQL: WHERE (edad < 18 OR edad > 65) AND activo = true
estudiantes.find({
    "$or": [
        {"edad": {"$lt": 18}},
        {"edad": {"$gt": 65}}
    ],
    "activo": True
})
```

### **IN / NOT IN**

```sql
-- SQL
SELECT * FROM estudiantes WHERE ciudad IN ('Madrid', 'Barcelona', 'Valencia');
SELECT * FROM estudiantes WHERE ciudad NOT IN ('Madrid', 'Barcelona');
```

```python
# MongoDB - $in / $nin

# IN ($in)
estudiantes.find({
    "direccion.ciudad": {"$in": ["Madrid", "Barcelona", "Valencia"]}
})

# NOT IN ($nin)
estudiantes.find({
    "direccion.ciudad": {"$nin": ["Madrid", "Barcelona"]}
})

# Ejemplo con múltiples valores
estudiantes.find({
    "edad": {"$in": [18, 19, 20, 21, 22]}
})
```

### **LIKE / Expresiones regulares**

```sql
-- SQL
SELECT * FROM estudiantes WHERE nombre LIKE 'Mar%';  -- Empieza con Mar
SELECT * FROM estudiantes WHERE nombre LIKE '%García%';  -- Contiene García
SELECT * FROM estudiantes WHERE email LIKE '%@gmail.com';  -- Termina con...
```

```python
# MongoDB - $regex

# Empieza con "Mar" (case sensitive)
estudiantes.find({
    "nombre": {"$regex": "^Mar"}
})

# Contiene "García" (case insensitive)
estudiantes.find({
    "nombre": {"$regex": "García", "$options": "i"}
})

# Termina con "@gmail.com"
estudiantes.find({
    "email": {"$regex": "@gmail\\.com$"}
})

# Forma alternativa con expresiones regulares de Python
import re
estudiantes.find({
    "nombre": {"$regex": re.compile("^Mar", re.IGNORECASE)}
})

# Ejemplos avanzados
# Buscar nombres con dos palabras
estudiantes.find({
    "nombre": {"$regex": "^\\w+\\s\\w+$"}
})

# Buscar códigos postales españoles (5 dígitos)
estudiantes.find({
    "direccion.codigo_postal": {"$regex": "^\\d{5}$"}
})
```

### **IS NULL / EXISTS**

```sql
-- SQL
SELECT * FROM estudiantes WHERE telefono IS NULL;
SELECT * FROM estudiantes WHERE telefono IS NOT NULL;
```

```python
# MongoDB - null y $exists

# Campo es null (existe pero está en null)
estudiantes.find({"telefono": None})

# Campo no existe o es null
estudiantes.find({
    "telefono": {"$in": [None, []]}
})

# Campo no existe
estudiantes.find({
    "telefono": {"$exists": False}
})

# Campo existe (independientemente del valor)
estudiantes.find({
    "telefono": {"$exists": True}
})

# Campo existe y no es null
estudiantes.find({
    "telefono": {"$exists": True, "$ne": None}
})

# Campo existe, no es null y no está vacío (para strings)
estudiantes.find({
    "telefono": {"$exists": True, "$ne": None, "$ne": ""}
})
```

## **3.3 ORDER BY, LIMIT, SKIP**

```sql
-- SQL
SELECT * FROM estudiantes ORDER BY edad DESC;
SELECT * FROM estudiantes ORDER BY edad ASC, nombre ASC;
SELECT * FROM estudiantes LIMIT 10;
SELECT * FROM estudiantes LIMIT 10 OFFSET 20;  -- Paginación
```

```python
# MongoDB - sort(), limit(), skip()

# ORDER BY edad DESC
estudiantes.find().sort("edad", -1)  # -1 = descendente, 1 = ascendente

# Múltiples campos de ordenamiento
estudiantes.find().sort([
    ("edad", -1),      # Primero por edad descendente
    ("nombre", 1)      # Luego por nombre ascendente
])

# LIMIT
estudiantes.find().limit(10)

# SKIP (para paginación)
estudiantes.find().skip(20).limit(10)

# Combinar todo
# SQL: SELECT * FROM estudiantes WHERE activo=true ORDER BY edad DESC LIMIT 10
resultados = estudiantes.find(
    {"activo": True}
).sort("edad", -1).limit(10)

# Paginación completa
def paginar_estudiantes(pagina=1, por_pagina=10):
    """
    Pagina=1 es la primera página
    """
    skip = (pagina - 1) * por_pagina
    
    resultados = estudiantes.find().skip(skip).limit(por_pagina)
    total = estudiantes.count_documents({})
    total_paginas = (total + por_pagina - 1) // por_pagina
    
    return {
        "datos": list(resultados),
        "pagina_actual": pagina,
        "total_paginas": total_paginas,
        "total_documentos": total
    }

# Uso
pagina_2 = paginar_estudiantes(pagina=2, por_pagina=20)
```

## **3.4 COUNT, DISTINCT**

```sql
-- SQL
SELECT COUNT(*) FROM estudiantes;
SELECT COUNT(*) FROM estudiantes WHERE activo = true;
SELECT DISTINCT ciudad FROM estudiantes;
SELECT ciudad, COUNT(*) FROM estudiantes GROUP BY ciudad;
```

```python
# MongoDB - count_documents(), distinct()

# COUNT total
total = estudiantes.count_documents({})
print(f"Total estudiantes: {total}")

# COUNT con filtro
activos = estudiantes.count_documents({"activo": True})
print(f"Estudiantes activos: {activos}")

# COUNT con condiciones múltiples
jovenes_activos = estudiantes.count_documents({
    "edad": {"$lt": 25},
    "activo": True
})

# DISTINCT - valores únicos
ciudades = estudiantes.distinct("direccion.ciudad")
print(ciudades)  # ['Madrid', 'Barcelona', 'Valencia', ...]

# DISTINCT con filtro
ciudades_activos = estudiantes.distinct(
    "direccion.ciudad",
    {"activo": True}
)

# Contar por ciudad (usando aggregation - ver sección 8)
pipeline = [
    {"$group": {
        "_id": "$direccion.ciudad",
        "total": {"$sum": 1}
    }},
    {"$sort": {"total": -1}}
]
resultado = list(estudiantes.aggregate(pipeline))
# [{"_id": "Madrid", "total": 45}, {"_id": "Barcelona", "total": 32}, ...]
```

## **3.5 Campos anidados y arrays (AMPLIADO)**

### **Dot notation para subdocumentos**

```python
# Documento de ejemplo
{
    "_id": 1,
    "nombre": "María García",
    "direccion": {
        "calle": "Gran Vía 123",
        "ciudad": "Madrid",
        "codigo_postal": "28013",
        "coordenadas": {
            "lat": 40.4168,
            "lon": -3.7038
        }
    }
}

# Buscar por campo anidado (dot notation)
estudiantes.find({"direccion.ciudad": "Madrid"})

# Buscar por campo doblemente anidado
estudiantes.find({
    "direccion.coordenadas.lat": {"$gt": 40.0}
})

# Proyección de campos anidados
estudiantes.find(
    {},
    {
        "nombre": 1,
        "direccion.ciudad": 1,
        "_id": 0
    }
)
# Resultado: {"nombre": "María", "direccion": {"ciudad": "Madrid"}}
```

### **Búsquedas en arrays**

```python
# Documento con array
{
    "_id": 1,
    "nombre": "Carlos",
    "hobbies": ["futbol", "lectura", "videojuegos"],
    "calificaciones": [8.5, 9.0, 7.5, 9.5]
}

# Buscar documentos que contengan un valor específico en el array
estudiantes.find({"hobbies": "futbol"})

# Buscar documentos que contengan TODOS los valores ($all)
estudiantes.find({
    "hobbies": {"$all": ["futbol", "lectura"]}
})

# Array con tamaño específico ($size)
estudiantes.find({
    "hobbies": {"$size": 3}
})

# Array con al menos N elementos
estudiantes.find({
    "hobbies.2": {"$exists": True}  # Al menos 3 elementos (índice 2 existe)
})

# Rangos en arrays numéricos
# Estudiantes con alguna calificación mayor a 9
estudiantes.find({
    "calificaciones": {"$gt": 9.0}
})

# Array vacío
estudiantes.find({"hobbies": []})
estudiantes.find({"hobbies": {"$size": 0}})

# Array no vacío
estudiantes.find({
    "hobbies": {"$exists": True, "$ne": []}
})
```

### **Arrays de subdocumentos ($elemMatch)**

```python
# Documento con array de objetos
{
    "_id": 1,
    "nombre": "Ana López",
    "cursos": [
        {"nombre": "Python", "calificacion": 9.5, "aprobado": True},
        {"nombre": "Java", "calificacion": 6.0, "aprobado": True},
        {"nombre": "MongoDB", "calificacion": 8.5, "aprobado": True}
    ]
}

# Buscar estudiante con un curso específico Y calificación alta
# Sin $elemMatch (INCORRECTO - busca condiciones en elementos diferentes)
estudiantes.find({
    "cursos.nombre": "Python",
    "cursos.calificacion": {"$gte": 9.0}
})

# Con $elemMatch (CORRECTO - ambas condiciones en el MISMO elemento)
estudiantes.find({
    "cursos": {
        "$elemMatch": {
            "nombre": "Python",
            "calificacion": {"$gte": 9.0}
        }
    }
})

# Estudiantes con al menos un curso suspendido
estudiantes.find({
    "cursos": {
        "$elemMatch": {
            "calificacion": {"$lt": 5.0}
        }
    }
})

# Múltiples condiciones complejas
estudiantes.find({
    "cursos": {
        "$elemMatch": {
            "nombre": {"$in": ["Python", "Java"]},
            "calificacion": {"$gte": 8.0},
            "aprobado": True
        }
    }
})
```

### **Proyección avanzada con arrays**

```python
# $slice - limitar elementos del array retornados

# Primeros 2 hobbies
estudiantes.find(
    {},
    {
        "nombre": 1,
        "hobbies": {"$slice": 2}
    }
)

# Últimos 2 hobbies
estudiantes.find(
    {},
    {
        "nombre": 1,
        "hobbies": {"$slice": -2}
    }
)

# Saltar 1 y tomar 2 (offset, limit)
estudiantes.find(
    {},
    {
        "nombre": 1,
        "hobbies": {"$slice": [1, 2]}  # Skip 1, limit 2
    }
)

# $elemMatch en proyección (solo el primer elemento que coincide)
estudiantes.find(
    {"cursos.nombre": "Python"},
    {
        "nombre": 1,
        "cursos": {"$elemMatch": {"nombre": "Python"}}
    }
)
# Resultado: Solo retorna el curso de Python, no todos los cursos
```

### **Consultas complejas en arrays anidados**

```python
# Documento complejo
{
    "_id": 1,
    "nombre": "Pedro Martínez",
    "historial_academico": [
        {
            "año": 2023,
            "cursos": [
                {"nombre": "Python", "creditos": 6, "nota": 9.0},
                {"nombre": "Bases de datos", "creditos": 6, "nota": 8.5}
            ]
        },
        {
            "año": 2024,
            "cursos": [
                {"nombre": "MongoDB", "creditos": 4, "nota": 9.5},
                {"nombre": "Docker", "creditos": 4, "nota": 8.0}
            ]
        }
    ]
}

# Buscar estudiante con curso de Python en cualquier año
estudiantes.find({
    "historial_academico.cursos.nombre": "Python"
})

# Buscar estudiante con curso de MongoDB en 2024
estudiantes.find({
    "historial_academico": {
        "$elemMatch": {
            "año": 2024,
            "cursos": {
                "$elemMatch": {
                    "nombre": "MongoDB"
                }
            }
        }
    }
})

# Estudiantes con más de 5 créditos en algún curso de 2024
estudiantes.find({
    "historial_academico": {
        "$elemMatch": {
            "año": 2024,
            "cursos": {
                "$elemMatch": {
                    "creditos": {"$gt": 5}
                }
            }
        }
    }
})
```



# **4. UPDATE - Actualización de documentos**

## **4.1 SQL vs MongoDB**

```sql
-- SQL
UPDATE estudiantes SET edad = 25 WHERE id = 1;
UPDATE estudiantes SET activo = false WHERE edad < 18;
UPDATE estudiantes SET login_count = login_count + 1 WHERE email = 'user@example.com';
```

```python
# MongoDB

# Actualizar un documento (update_one)
estudiantes.update_one(
    {"_id": 1},  # Filtro
    {"$set": {"edad": 25}}  # Actualización
)

# Actualizar múltiples documentos (update_many)
estudiantes.update_many(
    {"edad": {"$lt": 18}},
    {"$set": {"activo": False}}
)

# Incrementar valor
estudiantes.update_one(
    {"email": "user@example.com"},
    {"$inc": {"login_count": 1}}
)
```

## **4.2 Operadores básicos de actualización**

### **$set - Establecer valor de campos**

```python
# Actualizar un campo
estudiantes.update_one(
    {"_id": 1},
    {"$set": {"edad": 25}}
)

# Actualizar múltiples campos
estudiantes.update_one(
    {"email": "maria@example.com"},
    {"$set": {
        "edad": 26,
        "ciudad": "Barcelona",
        "activo": True,
        "fecha_modificacion": datetime.now()
    }}
)

# Crear campo si no existe
estudiantes.update_one(
    {"_id": 1},
    {"$set": {"telefono": "+34612345678"}}
)

# Actualizar campo anidado (dot notation)
estudiantes.update_one(
    {"_id": 1},
    {"$set": {"direccion.ciudad": "Madrid"}}
)
```

### **$unset - Eliminar campos**

```python
# Eliminar un campo
estudiantes.update_one(
    {"_id": 1},
    {"$unset": {"telefono": ""}}  # El valor no importa, se eliminará
)

# Eliminar múltiples campos
estudiantes.update_one(
    {"_id": 1},
    {"$unset": {
        "telefono": "",
        "telefono_secundario": "",
        "fax": ""
    }}
)

# Eliminar campo anidado
estudiantes.update_one(
    {"_id": 1},
    {"$unset": {"direccion.codigo_postal": ""}}
)
```

### **$inc - Incrementar/decrementar valores numéricos**

```python
# Incrementar en 1
estudiantes.update_one(
    {"email": "user@example.com"},
    {"$inc": {"login_count": 1}}
)

# Decrementar (usar valor negativo)
estudiantes.update_one(
    {"_id": 1},
    {"$inc": {"intentos_restantes": -1}}
)

# Incrementar múltiples campos
estudiantes.update_one(
    {"_id": 1},
    {"$inc": {
        "total_cursos": 1,
        "creditos_totales": 6
    }}
)

# Incrementar con decimales
estudiantes.update_one(
    {"_id": 1},
    {"$inc": {"saldo": 99.99}}
)
```

### **$mul - Multiplicar valores**

```python
# Duplicar un valor
estudiantes.update_one(
    {"_id": 1},
    {"$mul": {"puntos": 2}}
)

# Aplicar descuento del 10% (multiplicar por 0.9)
estudiantes.update_many(
    {"categoria": "estudiante"},
    {"$mul": {"precio_matricula": 0.9}}
)
```

### **$rename - Renombrar campos**

```python
# Renombrar un campo
estudiantes.update_many(
    {},
    {"$rename": {"edad": "age"}}
)

# Renombrar múltiples campos
estudiantes.update_many(
    {},
    {"$rename": {
        "fecha_registro": "created_at",
        "fecha_modificacion": "updated_at"
    }}
)

# Renombrar campo anidado
estudiantes.update_many(
    {},
    {"$rename": {"direccion.cp": "direccion.codigo_postal"}}
)
```

### **$min y $max - Actualizar solo si es menor/mayor**

```python
# Actualizar solo si el nuevo valor es MENOR que el actual
estudiantes.update_one(
    {"_id": 1},
    {"$min": {"mejor_tiempo": 125}}  # Solo actualiza si 125 < valor_actual
)

# Actualizar solo si el nuevo valor es MAYOR que el actual
estudiantes.update_one(
    {"_id": 1},
    {"$max": {"puntuacion_maxima": 950}}  # Solo actualiza si 950 > valor_actual
)

# Ejemplo práctico: registrar fecha más temprana
estudiantes.update_one(
    {"_id": 1},
    {"$min": {"primera_conexion": datetime.now()}}
)
```

### **$currentDate - Establecer fecha actual**

```python
# Establecer fecha actual
estudiantes.update_one(
    {"_id": 1},
    {"$currentDate": {
        "ultima_modificacion": True,
        "ultimo_acceso": {"$type": "date"}
    }}
)

# Timestamp (incluye microsegundos)
estudiantes.update_one(
    {"_id": 1},
    {"$currentDate": {
        "ultimo_login": {"$type": "timestamp"}
    }}
)
```

## **4.3 Operadores de arrays básicos**

### **$push - Añadir elemento al array**

```python
# Añadir un hobby
estudiantes.update_one(
    {"_id": 1},
    {"$push": {"hobbies": "natación"}}
)

# Si el campo no existe, lo crea como array
estudiantes.update_one(
    {"_id": 1},
    {"$push": {"tags": "nuevo"}}
)

# Añadir un subdocumento al array
estudiantes.update_one(
    {"_id": 1},
    {"$push": {
        "cursos": {
            "nombre": "MongoDB",
            "calificacion": 9.0,
            "fecha": datetime.now()
        }
    }}
)
```

### **$pull - Eliminar elemento(s) del array**

```python
# Eliminar un valor específico
estudiantes.update_one(
    {"_id": 1},
    {"$pull": {"hobbies": "natación"}}
)

# Eliminar todos los elementos que cumplan condición
estudiantes.update_one(
    {"_id": 1},
    {"$pull": {
        "calificaciones": {"$lt": 5.0}  # Eliminar calificaciones menores a 5
    }}
)

# Eliminar subdocumentos que cumplan condición
estudiantes.update_one(
    {"_id": 1},
    {"$pull": {
        "cursos": {"nombre": "Java"}  # Eliminar curso de Java
    }}
)
```

### **$addToSet - Añadir solo si no existe (sin duplicados)**

```python
# Añadir hobby solo si no existe
estudiantes.update_one(
    {"_id": 1},
    {"$addToSet": {"hobbies": "lectura"}}
)

# Si "lectura" ya existe, no hace nada
# Si no existe, lo añade

# Muy útil para etiquetas, categorías, etc.
estudiantes.update_one(
    {"_id": 1},
    {"$addToSet": {"tags": "premium"}}
)
```

### **$pop - Eliminar primer o último elemento**

```python
# Eliminar el último elemento
estudiantes.update_one(
    {"_id": 1},
    {"$pop": {"hobbies": 1}}  # 1 = último elemento
)

# Eliminar el primer elemento
estudiantes.update_one(
    {"_id": 1},
    {"$pop": {"hobbies": -1}}  # -1 = primer elemento
)
```

### **$pullAll - Eliminar múltiples valores**

```python
# Eliminar varios valores específicos
estudiantes.update_one(
    {"_id": 1},
    {"$pullAll": {
        "hobbies": ["futbol", "tenis", "golf"]
    }}
)
```

## **4.4 Upsert (INSERT or UPDATE)**

```python
# Actualizar si existe, insertar si no existe
resultado = estudiantes.update_one(
    {"email": "nuevo@example.com"},
    {
        "$set": {
            "nombre": "Usuario Nuevo",
            "edad": 25
        },
        "$setOnInsert": {  # Solo se aplica si se inserta
            "fecha_registro": datetime.now(),
            "activo": True
        }
    },
    upsert=True  # ← Clave del upsert
)

print(f"¿Se insertó? {resultado.upserted_id is not None}")
print(f"¿Se modificó? {resultado.modified_count > 0}")

# Ejemplo práctico: contador de visitas
def registrar_visita(user_id, pagina):
    estudiantes.update_one(
        {"_id": user_id, "visitas.pagina": pagina},
        {
            "$inc": {"visitas.$.contador": 1}
        }
    )
    
    # Si no existe esa página, crear entrada
    estudiantes.update_one(
        {"_id": user_id, "visitas.pagina": {"$ne": pagina}},
        {
            "$push": {
                "visitas": {
                    "pagina": pagina,
                    "contador": 1,
                    "primera_visita": datetime.now()
                }
            }
        }
    )
```

## **4.5 Actualización de estructuras complejas ⭐**

### **4.5.1 Actualizar subdocumentos con dot notation**

```python
# Documento ejemplo
{
    "_id": 1,
    "nombre": "María",
    "direccion": {
        "calle": "Gran Vía 123",
        "ciudad": "Madrid",
        "codigo_postal": "28013",
        "pais": "España"
    },
    "contacto": {
        "email": "maria@example.com",
        "telefono": {
            "movil": "+34612345678",
            "fijo": "+34912345678"
        }
    }
}

# Actualizar un campo dentro del subdocumento
estudiantes.update_one(
    {"_id": 1},
    {"$set": {"direccion.ciudad": "Barcelona"}}
)

# Actualizar múltiples campos anidados
estudiantes.update_one(
    {"_id": 1},
    {"$set": {
        "direccion.ciudad": "Valencia",
        "direccion.codigo_postal": "46001",
        "contacto.telefono.movil": "+34698765432"
    }}
)

# Actualizar subdocumento completo (reemplaza todo el objeto)
estudiantes.update_one(
    {"_id": 1},
    {"$set": {
        "direccion": {
            "calle": "Calle Nueva 456",
            "ciudad": "Sevilla",
            "codigo_postal": "41001",
            "pais": "España"
        }
    }}
)

# Añadir nuevo campo al subdocumento
estudiantes.update_one(
    {"_id": 1},
    {"$set": {"direccion.region": "Andalucía"}}
)

# Eliminar campo del subdocumento
estudiantes.update_one(
    {"_id": 1},
    {"$unset": {"contacto.telefono.fijo": ""}}
)

# Incrementar valor en subdocumento
estudiantes.update_one(
    {"_id": 1},
    {"$inc": {"estadisticas.visitas.total": 1}}
)
```

### **4.5.2 Operador posicional $ (primer elemento que coincide)**

```python
# Documento con array de objetos
{
    "_id": 1,
    "nombre": "Carlos",
    "cursos": [
        {"nombre": "Python", "calificacion": 8.0, "asistencia": 90},
        {"nombre": "Java", "calificacion": 7.0, "asistencia": 85},
        {"nombre": "MongoDB", "calificacion": 9.0, "asistencia": 95}
    ]
}

# Actualizar calificación del curso de Python
estudiantes.update_one(
    {"_id": 1, "cursos.nombre": "Python"},  # Filtro: encuentra el elemento
    {"$set": {"cursos.$.calificacion": 8.5}}  # $: actualiza ese elemento
)

# Resultado: solo la calificación de Python cambia a 8.5

# Actualizar múltiples campos del mismo elemento
estudiantes.update_one(
    {"_id": 1, "cursos.nombre": "Java"},
    {"$set": {
        "cursos.$.calificacion": 7.5,
        "cursos.$.asistencia": 90,
        "cursos.$.fecha_actualizacion": datetime.now()
    }}
)

# Incrementar con operador posicional
estudiantes.update_one(
    {"_id": 1, "cursos.nombre": "MongoDB"},
    {"$inc": {"cursos.$.asistencia": 5}}
)

# ⚠️ LIMITACIÓN: $ solo actualiza el PRIMER elemento que coincide
# Si hay múltiples elementos con nombre="Python", solo actualiza el primero
```

### **4.5.3 Operador $[] (todos los elementos del array)**

```python
# Documento
{
    "_id": 1,
    "nombre": "Ana",
    "cursos": [
        {"nombre": "Python", "activo": false, "notificaciones": true},
        {"nombre": "Java", "activo": false, "notificaciones": true},
        {"nombre": "MongoDB", "activo": false, "notificaciones": true}
    ]
}

# Activar TODOS los cursos
estudiantes.update_one(
    {"_id": 1},
    {"$set": {"cursos.$[].activo": True}}
)

# Resultado: todos los cursos tienen activo=true

# Añadir campo a todos los elementos
estudiantes.update_one(
    {"_id": 1},
    {"$set": {"cursos.$[].fecha_actualizacion": datetime.now()}}
)

# Incrementar asistencia en todos los cursos
estudiantes.update_one(
    {"_id": 1},
    {"$inc": {"cursos.$[].asistencia": 5}}
)

# Desactivar notificaciones en todos los cursos
estudiantes.update_one(
    {"_id": 1},
    {"$set": {"cursos.$[].notificaciones": False}}
)
```

### **4.5.4 Operador $[identifier] con arrayFilters (filtrado selectivo)**

```python
# Documento
{
    "_id": 1,
    "nombre": "Luis",
    "cursos": [
        {"nombre": "Python", "calificacion": 4.5, "aprobado": False},
        {"nombre": "Java", "calificacion": 7.0, "aprobado": True},
        {"nombre": "MongoDB", "calificacion": 3.5, "aprobado": False},
        {"nombre": "Docker", "calificacion": 8.5, "aprobado": True}
    ]
}

# Actualizar SOLO los cursos suspendidos (calificación < 5)
estudiantes.update_one(
    {"_id": 1},
    {"$set": {
        "cursos.$[suspenso].necesita_recuperacion": True,
        "cursos.$[suspenso].fecha_limite": datetime(2024, 9, 30)
    }},
    array_filters=[{"suspenso.calificacion": {"$lt": 5.0}}]
)

# Resultado: solo Python y MongoDB tienen los nuevos campos

# Incrementar calificación de cursos aprobados con nota < 8
estudiantes.update_one(
    {"_id": 1},
    {"$inc": {"cursos.$[elem].calificacion": 0.5}},
    array_filters=[
        {"elem.aprobado": True},
        {"elem.calificacion": {"$lt": 8.0}}
    ]
)

# Múltiples arrayFilters (condiciones complejas)
estudiantes.update_one(
    {"_id": 1},
    {"$set": {"cursos.$[curso].destacado": True}},
    array_filters=[
        {"curso.calificacion": {"$gte": 9.0}},
        {"curso.asistencia": {"$gte": 90}}
    ]
)

# Ejemplo práctico: aplicar descuento a productos caros
db.pedidos.update_one(
    {"_id": "ORDER123"},
    {"$mul": {"items.$[item].precio": 0.9}},  # 10% descuento
    array_filters=[{"item.precio": {"$gt": 100}}]
)
```

### **4.5.5 Operadores avanzados de arrays**

#### **$push con modificadores**

```python
# $each: añadir múltiples elementos
estudiantes.update_one(
    {"_id": 1},
    {"$push": {
        "hobbies": {
            "$each": ["natación", "yoga", "meditación"]
        }
    }}
)

# $each + $position: insertar en posición específica
estudiantes.update_one(
    {"_id": 1},
    {"$push": {
        "hobbies": {
            "$each": ["ajedrez"],
            "$position": 0  # Insertar al principio
        }
    }}
)

# $each + $slice: limitar tamaño del array
# Mantener solo los últimos 5 hobbies
estudiantes.update_one(
    {"_id": 1},
    {"$push": {
        "hobbies": {
            "$each": ["nuevo_hobby"],
            "$slice": -5  # Mantener últimos 5
        }
    }}
)

# $each + $sort: ordenar después de insertar
estudiantes.update_one(
    {"_id": 1},
    {"$push": {
        "calificaciones": {
            "$each": [8.5, 7.0, 9.5],
            "$sort": -1  # Ordenar descendente
        }
    }}
)

# Combinar todos los modificadores
estudiantes.update_one(
    {"_id": 1},
    {"$push": {
        "cursos": {
            "$each": [
                {"nombre": "Python", "nota": 9.0},
                {"nombre": "Java", "nota": 8.0}
            ],
            "$sort": {"nota": -1},  # Ordenar por nota descendente
            "$slice": 10,  # Mantener solo top 10
            "$position": 0  # Insertar al principio
        }
    }}
)
```

#### **$addToSet con $each**

```python
# Añadir múltiples elementos únicos
estudiantes.update_one(
    {"_id": 1},
    {"$addToSet": {
        "tags": {
            "$each": ["premium", "activo", "verificado"]
        }
    }}
)
# Solo añade los que no existan ya
```

#### **Ejemplos prácticos completos**

```python
# Ejemplo 1: Sistema de carrito de compra
def agregar_al_carrito(user_id, producto_id, cantidad):
    # Intentar actualizar cantidad si el producto ya existe
    resultado = estudiantes.update_one(
        {
            "_id": user_id,
            "carrito.producto_id": producto_id
        },
        {"$inc": {"carrito.$.cantidad": cantidad}}
    )
    
    # Si no existía, añadirlo
    if resultado.matched_count == 0:
        estudiantes.update_one(
            {"_id": user_id},
            {"$push": {
                "carrito": {
                    "producto_id": producto_id,
                    "cantidad": cantidad,
                    "fecha_agregado": datetime.now()
                }
            }}
        )

# Ejemplo 2: Sistema de calificaciones con límite
def agregar_calificacion(estudiante_id, calificacion):
    estudiantes.update_one(
        {"_id": estudiante_id},
        {
            "$push": {
                "calificaciones": {
                    "$each": [{
                        "nota": calificacion,
                        "fecha": datetime.now()
                    }],
                    "$sort": {"fecha": -1},  # Más recientes primero
                    "$slice": 20  # Mantener solo últimas 20
                }
            }
        }
    )

# Ejemplo 3: Actualizar precios con descuento en rango específico
def aplicar_descuento_selectivo(categoria, min_precio, max_precio, descuento):
    db.productos.update_many(
        {"categoria": categoria},
        {"$mul": {"items.$[item].precio": (1 - descuento)}},
        array_filters=[
            {"item.precio": {"$gte": min_precio, "$lte": max_precio}}
        ]
    )

# Ejemplo 4: Actualizar estado de tareas completadas
def marcar_tareas_antiguas_como_expiradas(dias=30):
    fecha_limite = datetime.now() - timedelta(days=dias)
    
    db.usuarios.update_many(
        {},
        {"$set": {"tareas.$[tarea].estado": "expirada"}},
        array_filters=[
            {"tarea.completada": False},
            {"tarea.fecha_creacion": {"$lt": fecha_limite}}
        ]
    )
```

## **4.6 replace_one() - Reemplazar documento completo**

```python
# replace_one() reemplaza TODO el documento excepto el _id

# Documento original
{
    "_id": 1,
    "nombre": "Carlos",
    "edad": 25,
    "email": "carlos@example.com",
    "cursos": ["Python", "Java"]
}

# Reemplazar completamente (PELIGROSO - pierde todos los campos)
estudiantes.replace_one(
    {"_id": 1},
    {
        "nombre": "Carlos Ruiz",
        "edad": 26,
        "email": "carlos.ruiz@example.com"
    }
)

# Resultado: el campo "cursos" se perdió

# ⚠️ Diferencia con update_one + $set:
# $set: solo modifica los campos especificados, mantiene el resto
# replace_one: reemplaza TODO el documento

# Uso recomendado: cuando quieres redefinir completamente el documento
nuevo_documento = {
    "nombre": "Carlos Ruiz",
    "edad": 26,
    "email": "carlos.ruiz@example.com",
    "telefono": "+34612345678",
    "direccion": {"ciudad": "Madrid"},
    "activo": True,
    "fecha_actualizacion": datetime.now()
}

estudiantes.replace_one({"_id": 1}, nuevo_documento)
```

## **4.7 Verificar resultados de actualización**

```python
# Los métodos update retornan UpdateResult

resultado = estudiantes.update_one(
    {"_id": 1},
    {"$set": {"edad": 26}}
)

print(f"Documentos que coincidieron: {resultado.matched_count}")
print(f"Documentos modificados: {resultado.modified_count}")
print(f"¿Reconocido por el servidor? {resultado.acknowledged}")

# Con upsert
resultado = estudiantes.update_one(
    {"email": "nuevo@example.com"},
    {"$set": {"nombre": "Nuevo"}},
    upsert=True
)

if resultado.upserted_id:
    print(f"Se insertó nuevo documento con _id: {resultado.upserted_id}")
else:
    print(f"Se actualizó documento existente")

# update_many
resultado = estudiantes.update_many(
    {"activo": False},
    {"$set": {"necesita_reactivacion": True}}
)

print(f"Se modificaron {resultado.modified_count} documentos")
```



# **5. DELETE - Eliminación de documentos**

## **5.1 SQL vs MongoDB**

```sql
-- SQL
DELETE FROM estudiantes WHERE id = 1;
DELETE FROM estudiantes WHERE activo = false;
DELETE FROM estudiantes;  -- Eliminar todo
TRUNCATE TABLE estudiantes;  -- Vaciar tabla (más rápido)
DROP TABLE estudiantes;  -- Eliminar tabla
```

```python
# MongoDB

# Eliminar un documento
estudiantes.delete_one({"_id": 1})

# Eliminar múltiples documentos
estudiantes.delete_many({"activo": False})

# Eliminar todos los documentos
estudiantes.delete_many({})

# Eliminar la colección completa
estudiantes.drop()

# Diferencia entre delete_many({}) y drop():
# - delete_many({}): elimina documentos uno por uno, mantiene índices
# - drop(): elimina la colección completa (más rápido), elimina índices
```

## **5.2 Ejemplos y precauciones**

```python
from pymongo import MongoClient

db = MongoClient()['universidad']
estudiantes = db['estudiantes']

# Eliminar un estudiante específico por _id
resultado = estudiantes.delete_one({"_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1")})
print(f"Documentos eliminados: {resultado.deleted_count}")

# Eliminar por email (único)
resultado = estudiantes.delete_one({"email": "usuario@example.com"})

# ⚠️ delete_one solo elimina el PRIMERO que encuentra
# Si hay múltiples documentos que coinciden, elimina solo uno

# Eliminar estudiantes inactivos
resultado = estudiantes.delete_many({"activo": False})
print(f"Se eliminaron {resultado.deleted_count} estudiantes inactivos")

# Eliminar estudiantes menores de 18
resultado = estudiantes.delete_many({"edad": {"$lt": 18}})

# Eliminar con múltiples condiciones
resultado = estudiantes.delete_many({
    "activo": False,
    "ultimo_acceso": {"$lt": datetime(2023, 1, 1)}
})

# Eliminar con condiciones complejas
resultado = estudiantes.delete_many({
    "$or": [
        {"email": None},
        {"email": ""}
    ]
})
```

### **Precauciones importantes**

```python
# ⚠️ SIEMPRE verificar el filtro antes de eliminar
# Buena práctica: hacer find() primero para ver qué se eliminará

# 1. Ver qué se va a eliminar
documentos_a_eliminar = list(estudiantes.find({"activo": False}))
print(f"Se eliminarán {len(documentos_a_eliminar)} documentos:")
for doc in documentos_a_eliminar:
    print(f"  - {doc['nombre']} ({doc['email']})")

# 2. Confirmar y eliminar
confirmacion = input("¿Confirmar eliminación? (sí/no): ")
if confirmacion.lower() == 'sí':
    resultado = estudiantes.delete_many({"activo": False})
    print(f"✓ {resultado.deleted_count} documentos eliminados")

# Función segura para eliminación
def eliminar_con_confirmacion(coleccion, filtro):
    """
    Elimina documentos con confirmación previa
    """
    # Contar documentos que se eliminarán
    count = coleccion.count_documents(filtro)
    
    if count == 0:
        print("No hay documentos que coincidan con el filtro")
        return 0
    
    print(f"⚠️  Se eliminarán {count} documento(s)")
    
    # Mostrar algunos ejemplos
    ejemplos = list(coleccion.find(filtro).limit(5))
    print("\nEjemplos:")
    for doc in ejemplos:
        print(f"  - {doc.get('nombre', 'Sin nombre')} (ID: {doc['_id']})")
    
    confirmacion = input("\n¿Confirmar eliminación? (sí/no): ")
    
    if confirmacion.lower() in ['sí', 'si', 's', 'yes', 'y']:
        resultado = coleccion.delete_many(filtro)
        print(f"✓ {resultado.deleted_count} documentos eliminados")
        return resultado.deleted_count
    else:
        print("✗ Eliminación cancelada")
        return 0

# Uso
eliminados = eliminar_con_confirmacion(
    estudiantes,
    {"activo": False, "ultimo_acceso": {"$lt": datetime(2023, 1, 1)}}
)
```

### **Soft delete vs Hard delete**

```python
# SOFT DELETE: marcar como eliminado sin borrar realmente
# Útil para mantener histórico y permitir recuperación

# En lugar de delete_many:
estudiantes.update_many(
    {"activo": False},
    {
        "$set": {
            "eliminado": True,
            "fecha_eliminacion": datetime.now()
        }
    }
)

# Luego, en las consultas, excluir eliminados:
estudiantes_activos = estudiantes.find({"eliminado": {"$ne": True}})

# HARD DELETE: eliminar permanentemente
estudiantes.delete_many({"eliminado": True, "fecha_eliminacion": {"$lt": datetime(2023, 1, 1)}})

# Implementación completa de soft delete
class EstudiantesCRUD:
    def __init__(self, db):
        self.collection = db['estudiantes']
    
    def soft_delete(self, filtro):
        """Marcar documentos como eliminados"""
        resultado = self.collection.update_many(
            filtro,
            {
                "$set": {
                    "eliminado": True,
                    "fecha_eliminacion": datetime.now()
                }
            }
        )
        return resultado.modified_count
    
    def restaurar(self, filtro):
        """Restaurar documentos eliminados"""
        resultado = self.collection.update_many(
            {**filtro, "eliminado": True},
            {
                "$set": {"eliminado": False},
                "$unset": {"fecha_eliminacion": ""}
            }
        )
        return resultado.modified_count
    
    def find_activos(self, filtro=None):
        """Buscar solo documentos no eliminados"""
        filtro = filtro or {}
        filtro["eliminado"] = {"$ne": True}
        return self.collection.find(filtro)
    
    def hard_delete_antiguos(self, dias=30):
        """Eliminar permanentemente registros antiguos"""
        fecha_limite = datetime.now() - timedelta(days=dias)
        resultado = self.collection.delete_many({
            "eliminado": True,
            "fecha_eliminacion": {"$lt": fecha_limite}
        })
        return resultado.deleted_count
```

### **Eliminar documentos con referencias**

```python
# Si tienes relaciones (estilo SQL con foreign keys)
# Debes eliminar en cascada manualmente

def eliminar_estudiante_completo(estudiante_id):
    """
    Elimina un estudiante y todos sus datos relacionados
    """
    # 1. Eliminar matrículas
    db.matriculas.delete_many({"estudiante_id": estudiante_id})
    
    # 2. Eliminar calificaciones
    db.calificaciones.delete_many({"estudiante_id": estudiante_id})
    
    # 3. Eliminar mensajes
    db.mensajes.delete_many({
        "$or": [
            {"remitente_id": estudiante_id},
            {"destinatario_id": estudiante_id}
        ]
    })
    
    # 4. Finalmente, eliminar estudiante
    resultado = estudiantes.delete_one({"_id": estudiante_id})
    
    return resultado.deleted_count > 0
```



# **6. Modelado de relaciones: De SQL a MongoDB**

## **6.1 Concepto: Embebido vs Referenciado**

En SQL, las relaciones siempre son por referencia (foreign keys). En MongoDB, tienes dos opciones:

### **Embebido (Embedded)**
- Los datos relacionados se guardan dentro del mismo documento
- **Ventaja**: Una sola consulta, mejor rendimiento para lecturas
- **Desventaja**: Duplicación de datos, documentos grandes, difícil actualizar

### **Referenciado (Referenced)**
- Los datos están en documentos separados, se referencian por _id
- **Ventaja**: No hay duplicación, fácil actualizar
- **Desventaja**: Requiere múltiples consultas o $lookup (JOIN)

### **¿Cuándo usar cada uno?**

| **Usar EMBEBIDO** | **Usar REFERENCIADO** |
|-------------------|----------------------|
| Relación 1:1 o 1:pocos | Relación 1:muchos o N:N |
| Los datos siempre se consultan juntos | Los datos se consultan independientemente |
| Los datos no cambian frecuentemente | Los datos cambian frecuentemente |
| Documentos no muy grandes (<16MB) | Documentos pueden crecer mucho |
| Ejemplo: Usuario y su dirección | Ejemplo: Usuarios y sus pedidos |

## **6.2 Relación 1:1 (One-to-One)**

### **SQL tradicional**
```sql
CREATE TABLE usuarios (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE perfiles (
    id INT PRIMARY KEY,
    usuario_id INT UNIQUE,  -- Clave foránea única
    biografia TEXT,
    avatar VARCHAR(255),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Consulta con JOIN
SELECT u.*, p.biografia, p.avatar
FROM usuarios u
LEFT JOIN perfiles p ON u.id = p.usuario_id
WHERE u.id = 1;
```

### **MongoDB - Opción 1: Embebido (RECOMENDADO para 1:1)**

```python
# Todo en un solo documento
usuario = {
    "_id": ObjectId(),
    "nombre": "María García",
    "email": "maria@example.com",
    "perfil": {  # Subdocumento embebido
        "biografia": "Desarrolladora Python con 5 años de experiencia",
        "avatar": "https://example.com/avatars/maria.jpg",
        "redes_sociales": {
            "twitter": "@mariadev",
            "linkedin": "maria-garcia-dev"
        },
        "fecha_actualizacion": datetime.now()
    }
}

db.usuarios.insert_one(usuario)

# Consulta simple (una sola query)
usuario = db.usuarios.find_one({"_id": ObjectId("...")})
print(usuario['perfil']['biografia'])

# Actualizar perfil
db.usuarios.update_one(
    {"_id": ObjectId("...")},
    {"$set": {
        "perfil.biografia": "Nueva biografía",
        "perfil.fecha_actualizacion": datetime.now()
    }}
)
```

### **MongoDB - Opción 2: Referenciado (menos común para 1:1)**

```python
# Colección usuarios
usuario = {
    "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
    "nombre": "María García",
    "email": "maria@example.com",
    "perfil_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j2")  # Referencia
}

# Colección perfiles (separada)
perfil = {
    "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j2"),
    "usuario_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),  # Referencia inversa
    "biografia": "Desarrolladora Python...",
    "avatar": "https://example.com/avatars/maria.jpg"
}

db.usuarios.insert_one(usuario)
db.perfiles.insert_one(perfil)

# Consulta (requiere dos queries o $lookup)
usuario = db.usuarios.find_one({"_id": ObjectId("...")})
perfil = db.perfiles.find_one({"_id": usuario['perfil_id']})

# O con $lookup (ver sección 7)
resultado = db.usuarios.aggregate([
    {"$match": {"_id": ObjectId("...")}},
    {"$lookup": {
        "from": "perfiles",
        "localField": "perfil_id",
        "foreignField": "_id",
        "as": "perfil"
    }},
    {"$unwind": "$perfil"}
])
```

## **6.3 Relación 1:N (One-to-Many)**

### **SQL tradicional**
```sql
CREATE TABLE blogs (
    id INT PRIMARY KEY,
    titulo VARCHAR(200),
    autor VARCHAR(100)
);

CREATE TABLE posts (
    id INT PRIMARY KEY,
    blog_id INT,  -- Foreign key
    titulo VARCHAR(200),
    contenido TEXT,
    fecha DATE,
    FOREIGN KEY (blog_id) REFERENCES blogs(id)
);

-- Consulta
SELECT b.titulo AS blog, p.titulo AS post, p.fecha
FROM blogs b
LEFT JOIN posts p ON b.id = p.blog_id
WHERE b.id = 1;
```

### **MongoDB - Opción 1: Array embebido (1:POCOS)**

```python
# Recomendado cuando el "many" es limitado (< 100-1000 elementos)

blog = {
    "_id": ObjectId(),
    "titulo": "Mi Blog de Tecnología",
    "autor": "María García",
    "posts": [  # Array de subdocumentos embebidos
        {
            "titulo": "Introducción a MongoDB",
            "contenido": "MongoDB es una base de datos...",
            "fecha": datetime(2024, 1, 15),
            "tags": ["mongodb", "nosql"],
            "comentarios": 25
        },
        {
            "titulo": "Python avanzado",
            "contenido": "En este post veremos...",
            "fecha": datetime(2024, 2, 1),
            "tags": ["python", "programacion"],
            "comentarios": 18
        }
    ],
    "total_posts": 2
}

db.blogs.insert_one(blog)

# Consultas
# Obtener el blog con todos sus posts
blog_completo = db.blogs.find_one({"_id": ObjectId("...")})

# Obtener solo posts con cierto tag
blog_filtrado = db.blogs.find_one(
    {"_id": ObjectId("...")},
    {"posts": {"$elemMatch": {"tags": "mongodb"}}}
)

# Añadir un nuevo post
db.blogs.update_one(
    {"_id": ObjectId("...")},
    {
        "$push": {
            "posts": {
                "titulo": "Nuevo post",
                "contenido": "Contenido...",
                "fecha": datetime.now(),
                "tags": ["nuevo"],
                "comentarios": 0
            }
        },
        "$inc": {"total_posts": 1}
    }
)

# Actualizar un post específico
db.blogs.update_one(
    {"_id": ObjectId("..."), "posts.titulo": "Introducción a MongoDB"},
    {"$set": {"posts.$.comentarios": 30}}
)

# Eliminar un post
db.blogs.update_one(
    {"_id": ObjectId("...")},
    {
        "$pull": {"posts": {"titulo": "Post antiguo"}},
        "$inc": {"total_posts": -1}
    }
)
```

### **MongoDB - Opción 2: Referencias (1:MUCHOS)**

```python
# Recomendado cuando el "many" es muy grande o crece indefinidamente

# Colección blogs
blog = {
    "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
    "titulo": "Mi Blog de Tecnología",
    "autor": "María García",
    "fecha_creacion": datetime(2024, 1, 1)
}

# Colección posts (documentos separados)
posts = [
    {
        "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j2"),
        "blog_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),  # Referencia al blog
        "titulo": "Introducción a MongoDB",
        "contenido": "MongoDB es una base de datos...",
        "fecha": datetime(2024, 1, 15),
        "tags": ["mongodb", "nosql"],
        "vistas": 1250,
        "comentarios": 25
    },
    {
        "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j3"),
        "blog_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
        "titulo": "Python avanzado",
        "contenido": "En este post veremos...",
        "fecha": datetime(2024, 2, 1),
        "tags": ["python", "programacion"],
        "vistas": 980,
        "comentarios": 18
    }
]

db.blogs.insert_one(blog)
db.posts.insert_many(posts)

# Consultas
# 1. Obtener el blog
blog = db.blogs.find_one({"_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1")})

# 2. Obtener posts del blog
posts_del_blog = list(db.posts.find({"blog_id": blog['_id']}))

# 3. Con función helper
def obtener_blog_con_posts(blog_id):
    blog = db.blogs.find_one({"_id": blog_id})
    if not blog:
        return None
    
    blog['posts'] = list(db.posts.find(
        {"blog_id": blog_id}
    ).sort("fecha", -1))
    
    return blog

# 4. Con $lookup (JOIN) - ver sección 7
resultado = db.blogs.aggregate([
    {"$match": {"_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1")}},
    {"$lookup": {
        "from": "posts",
        "localField": "_id",
        "foreignField": "blog_id",
        "as": "posts"
    }}
])

# Operaciones
# Crear nuevo post
nuevo_post = {
    "blog_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
    "titulo": "Nuevo tutorial",
    "contenido": "Contenido del tutorial...",
    "fecha": datetime.now(),
    "tags": ["tutorial"],
    "vistas": 0,
    "comentarios": 0
}
db.posts.insert_one(nuevo_post)

# Actualizar post
db.posts.update_one(
    {"_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j2")},
    {"$inc": {"vistas": 1}}
)

# Eliminar post
db.posts.delete_one({"_id": ObjectId("...")})

# Eliminar blog y todos sus posts (cascada manual)
def eliminar_blog_completo(blog_id):
    db.posts.delete_many({"blog_id": blog_id})
    db.blogs.delete_one({"_id": blog_id})
```

### **MongoDB - Opción 3: Híbrida (lo mejor de ambos mundos)**

```python
# Blog con resumen de posts embebidos + posts completos en colección separada

# Colección blogs
blog = {
    "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
    "titulo": "Mi Blog de Tecnología",
    "autor": "María García",
    "ultimos_posts": [  # Solo los últimos 5 posts (resumen)
        {
            "post_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j2"),
            "titulo": "Introducción a MongoDB",
            "fecha": datetime(2024, 1, 15),
            "vistas": 1250
        },
        {
            "post_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j3"),
            "titulo": "Python avanzado",
            "fecha": datetime(2024, 2, 1),
            "vistas": 980
        }
    ],
    "total_posts": 45,
    "total_vistas": 15600
}

# Colección posts (completos)
post = {
    "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j2"),
    "blog_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
    "titulo": "Introducción a MongoDB",
    "contenido": "Contenido completo del post... (puede ser muy largo)",
    "fecha": datetime(2024, 1, 15),
    "tags": ["mongodb", "nosql"],
    "vistas": 1250,
    "comentarios": []  # Array de comentarios embebidos
}

# Ventaja: consultas rápidas al blog (tiene resumen) + acceso a posts completos cuando se necesitan
```

## **6.4 Relación N:N (Many-to-Many)**

### **SQL tradicional**
```sql
CREATE TABLE estudiantes (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE cursos (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    creditos INT
);

-- Tabla intermedia (junction table)
CREATE TABLE matriculas (
    estudiante_id INT,
    curso_id INT,
    fecha_matricula DATE,
    calificacion DECIMAL(3,1),
    PRIMARY KEY (estudiante_id, curso_id),
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id)
);

-- Consulta: cursos de un estudiante
SELECT c.nombre, m.calificacion
FROM estudiantes e
JOIN matriculas m ON e.id = m.estudiante_id
JOIN cursos c ON m.curso_id = c.id
WHERE e.id = 1;
```

### **MongoDB - Opción 1: Array de referencias en ambos lados**

```python
# Colección estudiantes
estudiante = {
    "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
    "nombre": "María García",
    "email": "maria@example.com",
    "cursos_matriculados": [  # Array de IDs de cursos
        ObjectId("65f1a2b3c4d5e6f7g8h9i0j5"),
        ObjectId("65f1a2b3c4d5e6f7g8h9i0j6"),
        ObjectId("65f1a2b3c4d5e6f7g8h9i0j7")
    ]
}

# Colección cursos
curso = {
    "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j5"),
    "nombre": "Python Avanzado",
    "creditos": 6,
    "estudiantes_matriculados": [  # Array de IDs de estudiantes
        ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
        ObjectId("65f1a2b3c4d5e6f7g8h9i0j2"),
        ObjectId("65f1a2b3c4d5e6f7g8h9i0j3")
    ]
}

db.estudiantes.insert_one(estudiante)
db.cursos.insert_one(curso)

# Matricular estudiante en curso (actualizar ambos)
def matricular(estudiante_id, curso_id):
    # Añadir curso al estudiante
    db.estudiantes.update_one(
        {"_id": estudiante_id},
        {"$addToSet": {"cursos_matriculados": curso_id}}
    )
    
    # Añadir estudiante al curso
    db.cursos.update_one(
        {"_id": curso_id},
        {"$addToSet": {"estudiantes_matriculados": estudiante_id}}
    )

# Desmatricular
def desmatricular(estudiante_id, curso_id):
    db.estudiantes.update_one(
        {"_id": estudiante_id},
        {"$pull": {"cursos_matriculados": curso_id}}
    )
    
    db.cursos.update_one(
        {"_id": curso_id},
        {"$pull": {"estudiantes_matriculados": estudiante_id}}
    )

# Obtener cursos de un estudiante
estudiante = db.estudiantes.find_one({"_id": ObjectId("...")})
cursos = list(db.cursos.find({"_id": {"$in": estudiante['cursos_matriculados']}}))

# Con $lookup (ver sección 7)
resultado = db.estudiantes.aggregate([
    {"$match": {"_id": ObjectId("...")}},
    {"$lookup": {
        "from": "cursos",
        "localField": "cursos_matriculados",
        "foreignField": "_id",
        "as": "cursos"
    }}
])
```

### **MongoDB - Opción 2: Colección intermedia (como SQL)**

```python
# Colección estudiantes
estudiante = {
    "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
    "nombre": "María García",
    "email": "maria@example.com"
}

# Colección cursos
curso = {
    "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j5"),
    "nombre": "Python Avanzado",
    "creditos": 6,
    "profesor": "Dr. Juan López"
}

# Colección matriculas (intermedia con información adicional)
matricula = {
    "_id": ObjectId(),
    "estudiante_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
    "curso_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j5"),
    "fecha_matricula": datetime(2024, 9, 1),
    "calificacion": 9.5,
    "asistencia": 95.0,
    "estado": "aprobado"
}

db.estudiantes.insert_one(estudiante)
db.cursos.insert_one(curso)
db.matriculas.insert_one(matricula)

# Matricular estudiante
def matricular_con_datos(estudiante_id, curso_id, **kwargs):
    matricula = {
        "estudiante_id": estudiante_id,
        "curso_id": curso_id,
        "fecha_matricula": datetime.now(),
        "estado": "activo",
        **kwargs
    }
    
    # Verificar que no existe ya
    existe = db.matriculas.find_one({
        "estudiante_id": estudiante_id,
        "curso_id": curso_id
    })
    
    if existe:
        return {"error": "Ya está matriculado en este curso"}
    
    resultado = db.matriculas.insert_one(matricula)
    return {"success": True, "id": resultado.inserted_id}

# Obtener cursos de un estudiante con calificaciones
def obtener_cursos_estudiante(estudiante_id):
    pipeline = [
        {"$match": {"estudiante_id": estudiante_id}},
        {"$lookup": {
            "from": "cursos",
            "localField": "curso_id",
            "foreignField": "_id",
            "as": "curso"
        }},
        {"$unwind": "$curso"},
        {"$project": {
            "curso_nombre": "$curso.nombre",
            "creditos": "$curso.creditos",
            "calificacion": 1,
            "asistencia": 1,
            "estado": 1,
            "fecha_matricula": 1
        }}
    ]
    
    return list(db.matriculas.aggregate(pipeline))

# Obtener estudiantes de un curso
def obtener_estudiantes_curso(curso_id):
    pipeline = [
        {"$match": {"curso_id": curso_id}},
        {"$lookup": {
            "from": "estudiantes",
            "localField": "estudiante_id",
            "foreignField": "_id",
            "as": "estudiante"
        }},
        {"$unwind": "$estudiante"},
        {"$project": {
            "estudiante_nombre": "$estudiante.nombre",
            "estudiante_email": "$estudiante.email",
            "calificacion": 1,
            "asistencia": 1,
            "estado": 1
        }}
    ]
    
    return list(db.matriculas.aggregate(pipeline))

# Actualizar calificación
db.matriculas.update_one(
    {
        "estudiante_id": ObjectId("..."),
        "curso_id": ObjectId("...")
    },
    {"$set": {"calificacion": 9.5, "estado": "aprobado"}}
)
```

### **MongoDB - Opción 3: Array de objetos con información completa**

```python
# Útil cuando necesitas información adicional en la relación
# y consultas principalmente desde un lado

estudiante = {
    "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
    "nombre": "María García",
    "email": "maria@example.com",
    "cursos": [  # Array de objetos con ID + info adicional
        {
            "curso_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j5"),
            "nombre": "Python Avanzado",  # Duplicado para acceso rápido
            "fecha_matricula": datetime(2024, 9, 1),
            "calificacion": 9.5,
            "asistencia": 95.0,
            "estado": "aprobado"
        },
        {
            "curso_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j6"),
            "nombre": "MongoDB Profesional",
            "fecha_matricula": datetime(2024, 9, 1),
            "calificacion": 8.5,
            "asistencia": 92.0,
            "estado": "en_curso"
        }
    ]
}

# Ventaja: consultas rápidas del estudiante con toda su info
# Desventaja: duplicación (nombre del curso está en ambas colecciones)

# Matricular
db.estudiantes.update_one(
    {"_id": ObjectId("...")},
    {"$push": {
        "cursos": {
            "curso_id": ObjectId("..."),
            "nombre": "Nuevo Curso",
            "fecha_matricula": datetime.now(),
            "estado": "activo"
        }
    }}
)

# Actualizar calificación
db.estudiantes.update_one(
    {
        "_id": ObjectId("..."),
        "cursos.curso_id": ObjectId("...")
    },
    {"$set": {
        "cursos.$.calificacion": 9.5,
        "cursos.$.estado": "aprobado"
    }}
)
```

### **Comparación de opciones N:N**

| **Opción** | **Ventajas** | **Desventajas** | **Mejor para** |
|------------|--------------|-----------------|----------------|
| Arrays de IDs en ambos lados | Simple, relación bidireccional | Requiere múltiples queries | Relaciones simples sin metadatos |
| Colección intermedia | Muy flexible, permite metadatos | Más complejo, más queries | Cuando necesitas información adicional de la relación |
| Array de objetos completos | Una sola query para todo | Duplicación de datos | Cuando consultas principalmente desde un lado |



# **7. JOINs en MongoDB: $lookup (Aggregation Pipeline)**

## **7.1 SQL JOIN vs $lookup**

En SQL, los JOINs son fundamentales. En MongoDB, **se recomienda diseñar documentos para minimizar la necesidad de JOINs** (usando embedding). Sin embargo, cuando necesitas combinar colecciones, usas `$lookup` en el aggregation pipeline.

### **SQL JOINs**
```sql
-- INNER JOIN
SELECT e.nombre, c.nombre AS curso
FROM estudiantes e
INNER JOIN matriculas m ON e.id = m.estudiante_id
INNER JOIN cursos c ON m.curso_id = c.id;

-- LEFT JOIN
SELECT e.nombre, c.nombre AS curso
FROM estudiantes e
LEFT JOIN matriculas m ON e.id = m.estudiante_id
LEFT JOIN cursos c ON m.curso_id = c.id;
```

### **MongoDB $lookup (equivalente a LEFT OUTER JOIN)**
```python
# $lookup siempre es LEFT OUTER JOIN
# Si quieres INNER JOIN, filtras después con $match

# JOIN básico
pipeline = [
    {"$lookup": {
        "from": "cursos",           # Colección a unir
        "localField": "curso_id",   # Campo local (esta colección)
        "foreignField": "_id",      # Campo en la otra colección
        "as": "curso_info"          # Nombre del array resultado
    }}
]

resultado = db.estudiantes.aggregate(pipeline)
```

## **7.2 $lookup básico**

### **Ejemplo 1: Obtener estudiantes con su información de dirección**

```python
# Colección estudiantes
{
    "_id": ObjectId("...1"),
    "nombre": "María García",
    "email": "maria@example.com",
    "direccion_id": ObjectId("...5")
}

# Colección direcciones
{
    "_id": ObjectId("...5"),
    "calle": "Gran Vía 123",
    "ciudad": "Madrid",
    "codigo_postal": "28013"
}

# $lookup para unirlas
pipeline = [
    {"$lookup": {
        "from": "direcciones",
        "localField": "direccion_id",
        "foreignField": "_id",
        "as": "direccion"
    }}
]

resultado = list(db.estudiantes.aggregate(pipeline))

# Resultado:
{
    "_id": ObjectId("...1"),
    "nombre": "María García",
    "email": "maria@example.com",
    "direccion_id": ObjectId("...5"),
    "direccion": [  # ← Array con el documento unido
        {
            "_id": ObjectId("...5"),
            "calle": "Gran Vía 123",
            "ciudad": "Madrid",
            "codigo_postal": "28013"
        }
    ]
}

# Si quieres el objeto en lugar de array, usa $unwind
pipeline = [
    {"$lookup": {
        "from": "direcciones",
        "localField": "direccion_id",
        "foreignField": "_id",
        "as": "direccion"
    }},
    {"$unwind": "$direccion"}  # Convierte array en objeto
]

# Resultado:
{
    "_id": ObjectId("...1"),
    "nombre": "María García",
    "direccion": {  # ← Ahora es objeto, no array
        "_id": ObjectId("...5"),
        "calle": "Gran Vía 123",
        "ciudad": "Madrid"
    }
}
```

### **Ejemplo 2: Posts de un blog con información del autor**

```python
# Colección posts
{
    "_id": ObjectId("...1"),
    "titulo": "Introducción a MongoDB",
    "contenido": "...",
    "autor_id": ObjectId("...5"),
    "fecha": datetime(2024, 1, 15)
}

# Colección usuarios (autores)
{
    "_id": ObjectId("...5"),
    "nombre": "María García",
    "email": "maria@example.com"
}

# $lookup
pipeline = [
    {"$lookup": {
        "from": "usuarios",
        "localField": "autor_id",
        "foreignField": "_id",
        "as": "autor"
    }},
    {"$unwind": "$autor"},
    {"$project": {  # Seleccionar solo campos necesarios
        "titulo": 1,
        "contenido": 1,
        "fecha": 1,
        "autor_nombre": "$autor.nombre",
        "autor_email": "$autor.email"
    }}
]

resultado = list(db.posts.aggregate(pipeline))

# Resultado:
{
    "_id": ObjectId("...1"),
    "titulo": "Introducción a MongoDB",
    "contenido": "...",
    "fecha": datetime(2024, 1, 15),
    "autor_nombre": "María García",
    "autor_email": "maria@example.com"
}
```

## **7.3 $lookup con múltiples documentos (1:N)**

```python
# Colección blogs
{
    "_id": ObjectId("...1"),
    "titulo": "Mi Blog de Tecnología",
    "autor": "María García"
}

# Colección posts (múltiples posts por blog)
{
    "_id": ObjectId("...10"),
    "blog_id": ObjectId("...1"),
    "titulo": "Post 1",
    "contenido": "..."
}

# $lookup obtiene TODOS los posts del blog
pipeline = [
    {"$match": {"_id": ObjectId("...1")}},
    {"$lookup": {
        "from": "posts",
        "localField": "_id",
        "foreignField": "blog_id",
        "as": "posts"
    }}
]

resultado = list(db.blogs.aggregate(pipeline))

# Resultado:
{
    "_id": ObjectId("...1"),
    "titulo": "Mi Blog de Tecnología",
    "autor": "María García",
    "posts": [  # Array con TODOS los posts
        {"_id": ObjectId("...10"), "titulo": "Post 1", ...},
        {"_id": ObjectId("...11"), "titulo": "Post 2", ...},
        {"_id": ObjectId("...12"), "titulo": "Post 3", ...}
    ]
}
```

## **7.4 $lookup con condiciones complejas (pipeline syntax)**

```python
# Sintaxis avanzada de $lookup con pipeline interno
# Permite filtros, proyecciones y transformaciones

# Ejemplo: Obtener estudiantes con sus cursos aprobados (calificación >= 5)

# Colección estudiantes
{
    "_id": ObjectId("...1"),
    "nombre": "María García"
}

# Colección matriculas
{
    "estudiante_id": ObjectId("...1"),
    "curso_id": ObjectId("...5"),
    "calificacion": 9.5
}

# $lookup con pipeline
pipeline = [
    {"$lookup": {
        "from": "matriculas",
        "let": {"estudiante_id": "$_id"},  # Variables para el pipeline
        "pipeline": [
            {"$match": {
                "$expr": {
                    "$and": [
                        {"$eq": ["$estudiante_id", "$$estudiante_id"]},
                        {"$gte": ["$calificacion", 5.0]}  # Solo aprobados
                    ]
                }
            }},
            {"$lookup": {  # Nested lookup para obtener info del curso
                "from": "cursos",
                "localField": "curso_id",
                "foreignField": "_id",
                "as": "curso"
            }},
            {"$unwind": "$curso"},
            {"$project": {
                "curso_nombre": "$curso.nombre",
                "calificacion": 1,
                "creditos": "$curso.creditos"
            }}
        ],
        "as": "cursos_aprobados"
    }}
]

# Ejemplo 2: Posts con más de 100 comentarios
pipeline = [
    {"$lookup": {
        "from": "comentarios",
        "let": {"post_id": "$_id"},
        "pipeline": [
            {"$match": {
                "$expr": {"$eq": ["$post_id", "$$post_id"]}
            }},
            {"$count": "total"}
        ],
        "as": "stats"
    }},
    {"$unwind": "$stats"},
    {"$match": {"stats.total": {"$gte": 100}}}
]
```

## **7.5 Múltiples $lookup (varios JOINs)**

```python
# SQL equivalente:
# SELECT e.nombre, c.nombre AS curso, p.nombre AS profesor
# FROM estudiantes e
# JOIN matriculas m ON e.id = m.estudiante_id
# JOIN cursos c ON m.curso_id = c.id
# JOIN profesores p ON c.profesor_id = p.id

pipeline = [
    # JOIN con matriculas
    {"$lookup": {
        "from": "matriculas",
        "localField": "_id",
        "foreignField": "estudiante_id",
        "as": "matriculas"
    }},
    {"$unwind": "$matriculas"},
    
    # JOIN con cursos
    {"$lookup": {
        "from": "cursos",
        "localField": "matriculas.curso_id",
        "foreignField": "_id",
        "as": "curso"
    }},
    {"$unwind": "$curso"},
    
    # JOIN con profesores
    {"$lookup": {
        "from": "profesores",
        "localField": "curso.profesor_id",
        "foreignField": "_id",
        "as": "profesor"
    }},
    {"$unwind": "$profesor"},
    
    # Proyección final
    {"$project": {
        "estudiante": "$nombre",
        "curso": "$curso.nombre",
        "profesor": "$profesor.nombre",
        "calificacion": "$matriculas.calificacion"
    }}
]

resultado = list(db.estudiantes.aggregate(pipeline))
```

## **7.6 $unwind para aplanar arrays**

```python
# $unwind convierte cada elemento de un array en un documento separado

# Documento original
{
    "_id": 1,
    "nombre": "María",
    "hobbies": ["lectura", "natación", "música"]
}

# Sin $unwind
db.estudiantes.find({"_id": 1})
# Resultado: 1 documento con array

# Con $unwind
db.estudiantes.aggregate([
    {"$match": {"_id": 1}},
    {"$unwind": "$hobbies"}
])

# Resultado: 3 documentos
{
    "_id": 1,
    "nombre": "María",
    "hobbies": "lectura"
}
{
    "_id": 1,
    "nombre": "María",
    "hobbies": "natación"
}
{
    "_id": 1,
    "nombre": "María",
    "hobbies": "música"
}

# Uso práctico: contar hobbies más populares
pipeline = [
    {"$unwind": "$hobbies"},
    {"$group": {
        "_id": "$hobbies",
        "total": {"$sum": 1}
    }},
    {"$sort": {"total": -1}},
    {"$limit": 10}
]

# $unwind preservando documentos sin array
pipeline = [
    {"$unwind": {
        "path": "$hobbies",
        "preserveNullAndEmptyArrays": True  # Incluye docs sin hobbies
    }}
]
```

## **7.7 Populate manual (sin aggregation)**

```python
# Alternativa a $lookup cuando prefieres queries simples
# Útil para casos sencillos o cuando necesitas lógica compleja

def obtener_estudiante_con_cursos(estudiante_id):
    # 1. Obtener estudiante
    estudiante = db.estudiantes.find_one({"_id": estudiante_id})
    
    if not estudiante:
        return None
    
    # 2. Obtener matrículas
    matriculas = list(db.matriculas.find({"estudiante_id": estudiante_id}))
    
    # 3. Obtener cursos
    curso_ids = [m['curso_id'] for m in matriculas]
    cursos = list(db.cursos.find({"_id": {"$in": curso_ids}}))
    
    # 4. Combinar información
    curso_dict = {c['_id']: c for c in cursos}
    
    estudiante['cursos'] = []
    for matricula in matriculas:
        curso = curso_dict.get(matricula['curso_id'])
        if curso:
            estudiante['cursos'].append({
                "nombre": curso['nombre'],
                "creditos": curso['creditos'],
                "calificacion": matricula['calificacion'],
                "fecha_matricula": matricula['fecha_matricula']
            })
    
    return estudiante

# Uso
estudiante = obtener_estudiante_con_cursos(ObjectId("..."))
print(estudiante['cursos'])
```

### **Ventajas y desventajas: $lookup vs populate manual**

| **$lookup (aggregation)** | **Populate manual** |
|---------------------------|---------------------|
| ✅ Todo en una query | ❌ Múltiples queries |
| ✅ Mejor rendimiento (generalmente) | ❌ Más round-trips al servidor |
| ❌ Sintaxis más compleja | ✅ Código más legible y flexible |
| ❌ Limitado a capacidades de aggregation | ✅ Puedes aplicar lógica de Python |
| ✅ Mejor para agregaciones complejas | ✅ Mejor para casos simples |



# **8. Agregaciones (GROUP BY, HAVING, funciones)**

## **8.1 SQL vs MongoDB Aggregation Framework**

El **Aggregation Pipeline** de MongoDB es equivalente a las operaciones GROUP BY, HAVING y funciones agregadas de SQL, pero mucho más potente.

### **Conceptos básicos**

| **SQL** | **MongoDB Aggregation** |
|---------|-------------------------|
| WHERE | $match |
| GROUP BY | $group |
| HAVING | $match (después de $group) |
| SELECT | $project |
| ORDER BY | $sort |
| LIMIT | $limit |
| JOIN | $lookup |
| COUNT(), SUM(), AVG() | $sum, $avg, $count, etc. |

### **Pipeline concept**

Un pipeline es una secuencia de **stages** (etapas) donde cada una transforma los documentos:

```python
# SQL: SELECT ciudad, COUNT(*) FROM estudiantes GROUP BY ciudad HAVING COUNT(*) > 10 ORDER BY COUNT(*) DESC

# MongoDB Aggregation Pipeline
pipeline = [
    {"$group": {                          # GROUP BY
        "_id": "$ciudad",
        "total": {"$sum": 1}
    }},
    {"$match": {"total": {"$gt": 10}}},   # HAVING
    {"$sort": {"total": -1}}              # ORDER BY
]

resultado = db.estudiantes.aggregate(pipeline)
```

## **8.2 Pipeline stages principales**

### **$match - Filtrar documentos (WHERE)**

```python
# SQL: SELECT * FROM estudiantes WHERE edad > 20

pipeline = [
    {"$match": {"edad": {"$gt": 20}}}
]

# Múltiples condiciones
pipeline = [
    {"$match": {
        "edad": {"$gte": 18, "$lte": 30},
        "activo": True,
        "ciudad": {"$in": ["Madrid", "Barcelona"]}
    }}
]

# Buena práctica: $match lo antes posible para reducir documentos
pipeline = [
    {"$match": {"activo": True}},  # ← Primero filtrar
    {"$group": {...}},
    {"$match": {...}}  # ← Luego filtrar resultados agregados (HAVING)
]
```

### **$group - Agrupar documentos (GROUP BY)**

```python
# Funciones agregadas disponibles:
# $sum, $avg, $min, $max, $first, $last, $push, $addToSet

# SQL: SELECT COUNT(*) FROM estudiantes
pipeline = [
    {"$group": {
        "_id": None,  # Sin agrupar, todo junto
        "total": {"$sum": 1}
    }}
]
# Resultado: {"_id": None, "total": 150}

# SQL: SELECT ciudad, COUNT(*) FROM estudiantes GROUP BY ciudad
pipeline = [
    {"$group": {
        "_id": "$ciudad",  # Agrupar por ciudad
        "total": {"$sum": 1}
    }}
]
# Resultado: 
# {"_id": "Madrid", "total": 45}
# {"_id": "Barcelona", "total": 32}

# SQL: SELECT ciudad, AVG(edad) FROM estudiantes GROUP BY ciudad
pipeline = [
    {"$group": {
        "_id": "$ciudad",
        "edad_promedio": {"$avg": "$edad"},
        "total_estudiantes": {"$sum": 1}
    }}
]

# Múltiples agregaciones
pipeline = [
    {"$group": {
        "_id": "$ciudad",
        "total": {"$sum": 1},
        "edad_promedio": {"$avg": "$edad"},
        "edad_minima": {"$min": "$edad"},
        "edad_maxima": {"$max": "$edad"},
        "suma_edades": {"$sum": "$edad"}
    }}
]

# Agrupar por múltiples campos (GROUP BY ciudad, activo)
pipeline = [
    {"$group": {
        "_id": {
            "ciudad": "$ciudad",
            "activo": "$activo"
        },
        "total": {"$sum": 1}
    }}
]
# Resultado: {"_id": {"ciudad": "Madrid", "activo": true}, "total": 40}
```

### **$project - Seleccionar y transformar campos (SELECT)**

```python
# SQL: SELECT nombre, edad FROM estudiantes

pipeline = [
    {"$project": {
        "nombre": 1,
        "edad": 1,
        "_id": 0  # Excluir _id
    }}
]

# Renombrar campos
pipeline = [
    {"$project": {
        "nombre_completo": "$nombre",
        "años": "$edad",
        "_id": 0
    }}
]

# Campos calculados
pipeline = [
    {"$project": {
        "nombre": 1,
        "edad": 1,
        "mayor_edad": {"$gte": ["$edad", 18]},  # Boolean
        "edad_en_meses": {"$multiply": ["$edad", 12]}
    }}
]

# Concatenar strings
pipeline = [
    {"$project": {
        "nombre_completo": {
            "$concat": ["$nombre", " ", "$apellido"]
        },
        "email_mayusculas": {"$toUpper": "$email"}
    }}
]

# Extraer subdocumentos
pipeline = [
    {"$project": {
        "nombre": 1,
        "ciudad": "$direccion.ciudad",  # Dot notation
        "coordenadas": "$direccion.coordenadas"
    }}
]
```

### **$sort - Ordenar resultados (ORDER BY)**

```python
# SQL: SELECT * FROM estudiantes ORDER BY edad DESC

pipeline = [
    {"$sort": {"edad": -1}}  # -1 = descendente, 1 = ascendente
]

# Ordenar por múltiples campos
pipeline = [
    {"$sort": {
        "ciudad": 1,      # Primero por ciudad (ascendente)
        "edad": -1        # Luego por edad (descendente)
    }}
]

# Ordenar después de agrupar
pipeline = [
    {"$group": {
        "_id": "$ciudad",
        "total": {"$sum": 1}
    }},
    {"$sort": {"total": -1}}  # Ordenar por total descendente
]
```

### **$limit y $skip - Limitar y paginar**

```python
# SQL: SELECT * FROM estudiantes LIMIT 10

pipeline = [
    {"$limit": 10}
]

# SQL: SELECT * FROM estudiantes LIMIT 10 OFFSET 20
pipeline = [
    {"$skip": 20},
    {"$limit": 10}
]

# Top 5 ciudades con más estudiantes
pipeline = [
    {"$group": {
        "_id": "$ciudad",
        "total": {"$sum": 1}
    }},
    {"$sort": {"total": -1}},
    {"$limit": 5}
]
```

### **$unwind - Aplanar arrays**

```python
# Documento original
{
    "_id": 1,
    "nombre": "María",
    "cursos": ["Python", "MongoDB", "Docker"]
}

# Con $unwind
pipeline = [
    {"$unwind": "$cursos"}
]

# Resultado: 3 documentos
{
    "_id": 1,
    "nombre": "María",
    "cursos": "Python"
}
{
    "_id": 1,
    "nombre": "María",
    "cursos": "MongoDB"
}
{
    "_id": 1,
    "nombre": "María",
    "cursos": "Docker"
}
```

## **8.3 Ejemplos completos**

### **Ejemplo 1: Ventas por categoría**

```python
# Colección ventas
{
    "_id": ObjectId("..."),
    "producto": "Laptop HP",
    "categoria": "Electrónica",
    "precio": 899.99,
    "cantidad": 2,
    "fecha": datetime(2024, 1, 15),
    "ciudad": "Madrid"
}

# SQL equivalente:
# SELECT categoria, SUM(precio * cantidad) as total_ventas, COUNT(*) as num_ventas
# FROM ventas
# WHERE fecha >= '2024-01-01'
# GROUP BY categoria
# HAVING SUM(precio * cantidad) > 10000
# ORDER BY total_ventas DESC

pipeline = [
    # WHERE: filtrar por fecha
    {"$match": {
        "fecha": {"$gte": datetime(2024, 1, 1)}
    }},
    
    # Calcular total por venta
    {"$addFields": {
        "total_venta": {"$multiply": ["$precio", "$cantidad"]}
    }},
    
    # GROUP BY categoria
    {"$group": {
        "_id": "$categoria",
        "total_ventas": {"$sum": "$total_venta"},
        "num_ventas": {"$sum": 1},
        "venta_promedio": {"$avg": "$total_venta"},
        "venta_maxima": {"$max": "$total_venta"}
    }},
    
    # HAVING: filtrar grupos
    {"$match": {
        "total_ventas": {"$gt": 10000}
    }},
    
    # ORDER BY
    {"$sort": {"total_ventas": -1}},
    
    # Renombrar _id a categoria
    {"$project": {
        "_id": 0,
        "categoria": "$_id",
        "total_ventas": 1,
        "num_ventas": 1,
        "venta_promedio": {"$round": ["$venta_promedio", 2]},
        "venta_maxima": 1
    }}
]

resultado = list(db.ventas.aggregate(pipeline))

# Resultado:
# [
#   {
#     "categoria": "Electrónica",
#     "total_ventas": 45000.50,
#     "num_ventas": 25,
#     "venta_promedio": 1800.02,
#     "venta_maxima": 3500.00
#   },
#   ...
# ]
```

### **Ejemplo 2: Top 10 productos más vendidos**

```python
# SQL:
# SELECT producto, SUM(cantidad) as total_vendido, SUM(precio * cantidad) as ingresos
# FROM ventas
# GROUP BY producto
# ORDER BY total_vendido DESC
# LIMIT 10

pipeline = [
    {"$group": {
        "_id": "$producto",
        "total_vendido": {"$sum": "$cantidad"},
        "ingresos": {"$sum": {"$multiply": ["$precio", "$cantidad"]}},
        "num_transacciones": {"$sum": 1}
    }},
    {"$sort": {"total_vendido": -1}},
    {"$limit": 10},
    {"$project": {
        "_id": 0,
        "producto": "$_id",
        "total_vendido": 1,
        "ingresos": {"$round": ["$ingresos", 2]},
        "num_transacciones": 1
    }}
]

resultado = list(db.ventas.aggregate(pipeline))
```

### **Ejemplo 3: Ventas mensuales (agrupación por fecha)**

```python
# SQL:
# SELECT 
#   YEAR(fecha) as año, 
#   MONTH(fecha) as mes, 
#   SUM(precio * cantidad) as total
# FROM ventas
# GROUP BY YEAR(fecha), MONTH(fecha)
# ORDER BY año, mes

pipeline = [
    {"$group": {
        "_id": {
            "año": {"$year": "$fecha"},
            "mes": {"$month": "$fecha"}
        },
        "total": {"$sum": {"$multiply": ["$precio", "$cantidad"]}},
        "num_ventas": {"$sum": 1}
    }},
    {"$sort": {
        "_id.año": 1,
        "_id.mes": 1
    }},
    {"$project": {
        "_id": 0,
        "año": "$_id.año",
        "mes": "$_id.mes",
        "total": {"$round": ["$total", 2]},
        "num_ventas": 1
    }}
]

resultado = list(db.ventas.aggregate(pipeline))

# Resultado:
# [
#   {"año": 2024, "mes": 1, "total": 15000.50, "num_ventas": 45},
#   {"año": 2024, "mes": 2, "total": 18500.75, "num_ventas": 52},
#   ...
# ]
```

### **Ejemplo 4: Estudiantes por rango de edad**

```python
# Clasificar estudiantes en rangos de edad

pipeline = [
    {"$bucket": {
        "groupBy": "$edad",
        "boundaries": [0, 18, 25, 35, 50, 100],  # Rangos
        "default": "Otros",
        "output": {
            "total": {"$sum": 1},
            "edad_promedio": {"$avg": "$edad"}
        }
    }},
    {"$project": {
        "rango": "$_id",
        "total": 1,
        "edad_promedio": {"$round": ["$edad_promedio", 1]},
        "_id": 0
    }}
]

# Resultado:
# [
#   {"rango": 0, "total": 5, "edad_promedio": 16.5},     # 0-17
#   {"rango": 18, "total": 45, "edad_promedio": 21.2},   # 18-24
#   {"rango": 25, "total": 35, "edad_promedio": 28.5},   # 25-34
#   ...
# ]

# Alternativa con $cond (más flexible)
pipeline = [
    {"$project": {
        "nombre": 1,
        "edad": 1,
        "rango_edad": {
            "$switch": {
                "branches": [
                    {"case": {"$lt": ["$edad", 18]}, "then": "Menor"},
                    {"case": {"$lt": ["$edad", 25]}, "then": "Joven"},
                    {"case": {"$lt": ["$edad", 35]}, "then": "Adulto joven"},
                    {"case": {"$lt": ["$edad", 50]}, "then": "Adulto"},
                ],
                "default": "Senior"
            }
        }
    }},
    {"$group": {
        "_id": "$rango_edad",
        "total": {"$sum": 1}
    }}
]
```

### **Ejemplo 5: Análisis de texto - dominios de email más comunes**

```python
# Extraer dominio de email y contar

pipeline = [
    {"$project": {
        "dominio": {
            "$arrayElemAt": [
                {"$split": ["$email", "@"]},
                1  # Tomar la segunda parte (después del @)
            ]
        }
    }},
    {"$group": {
        "_id": "$dominio",
        "total": {"$sum": 1}
    }},
    {"$sort": {"total": -1}},
    {"$limit": 10}
]

resultado = list(db.estudiantes.aggregate(pipeline))

# Resultado:
# [
#   {"_id": "gmail.com", "total": 45},
#   {"_id": "example.com", "total": 32},
#   {"_id": "yahoo.com", "total": 18},
#   ...
# ]
```

## **8.4 Agregaciones con arrays ($unwind, $group)**

### **Ejemplo 1: Hobbies más populares**

```python
# Documento
{
    "_id": 1,
    "nombre": "María",
    "hobbies": ["lectura", "natación", "música"]
}

# SQL equivalente (con tabla normalizada):
# SELECT hobby, COUNT(*) FROM estudiante_hobbies GROUP BY hobby

pipeline = [
    {"$unwind": "$hobbies"},  # Convertir array en documentos separados
    {"$group": {
        "_id": "$hobbies",
        "total_estudiantes": {"$sum": 1}
    }},
    {"$sort": {"total_estudiantes": -1}},
    {"$limit": 10}
]

resultado = list(db.estudiantes.aggregate(pipeline))

# Resultado:
# [
#   {"_id": "lectura", "total_estudiantes": 45},
#   {"_id": "deportes", "total_estudiantes": 38},
#   ...
# ]
```

### **Ejemplo 2: Análisis de cursos - promedio de calificaciones por curso**

```python
# Documento estudiante
{
    "_id": 1,
    "nombre": "María",
    "cursos": [
        {"nombre": "Python", "calificacion": 9.5},
        {"nombre": "MongoDB", "calificacion": 8.5}
    ]
}

# Promedio de calificación por curso (todos los estudiantes)
pipeline = [
    {"$unwind": "$cursos"},
    {"$group": {
        "_id": "$cursos.nombre",
        "calificacion_promedio": {"$avg": "$cursos.calificacion"},
        "total_estudiantes": {"$sum": 1},
        "calificacion_maxima": {"$max": "$cursos.calificacion"},
        "calificacion_minima": {"$min": "$cursos.calificacion"}
    }},
    {"$sort": {"calificacion_promedio": -1}},
    {"$project": {
        "_id": 0,
        "curso": "$_id",
        "calificacion_promedio": {"$round": ["$calificacion_promedio", 2]},
        "total_estudiantes": 1,
        "calificacion_maxima": 1,
        "calificacion_minima": 1
    }}
]

resultado = list(db.estudiantes.aggregate(pipeline))

# Resultado:
# [
#   {
#     "curso": "Python",
#     "calificacion_promedio": 8.75,
#     "total_estudiantes": 45,
#     "calificacion_maxima": 10.0,
#     "calificacion_minima": 5.0
#   },
#   ...
# ]
```

### **Ejemplo 3: Estudiantes con más de N cursos aprobados**

```python
# Contar cursos aprobados por estudiante

pipeline = [
    {"$unwind": "$cursos"},
    {"$match": {
        "cursos.calificacion": {"$gte": 5.0}  # Solo aprobados
    }},
    {"$group": {
        "_id": "$_id",
        "nombre": {"$first": "$nombre"},
        "cursos_aprobados": {"$sum": 1},
        "promedio_general": {"$avg": "$cursos.calificacion"},
        "mejor_nota": {"$max": "$cursos.calificacion"}
    }},
    {"$match": {
        "cursos_aprobados": {"$gte": 5}  # Al menos 5 cursos aprobados
    }},
    {"$sort": {"promedio_general": -1}},
    {"$project": {
        "_id": 0,
        "nombre": 1,
        "cursos_aprobados": 1,
        "promedio_general": {"$round": ["$promedio_general", 2]},
        "mejor_nota": 1
    }}
]

resultado = list(db.estudiantes.aggregate(pipeline))
```

### **Ejemplo 4: Array operations - $push y $addToSet en aggregation**

```python
# Agrupar emails por ciudad (crear array)

pipeline = [
    {"$group": {
        "_id": "$ciudad",
        "emails": {"$push": "$email"},  # Array con duplicados
        "emails_unicos": {"$addToSet": "$email"},  # Array sin duplicados
        "total": {"$sum": 1}
    }}
]

# Resultado:
# {
#   "_id": "Madrid",
#   "emails": ["maria@...", "juan@...", "maria@...", ...],
#   "emails_unicos": ["maria@...", "juan@...", "ana@...", ...],
#   "total": 45
# }

# Obtener primeros y últimos estudiantes por ciudad (por fecha registro)
pipeline = [
    {"$sort": {"fecha_registro": 1}},
    {"$group": {
        "_id": "$ciudad",
        "primer_estudiante": {"$first": "$nombre"},
        "ultimo_estudiante": {"$last": "$nombre"},
        "total": {"$sum": 1}
    }}
]
```

## **8.5 Operaciones masivas (Bulk Operations)**

Las operaciones masivas permiten realizar múltiples escrituras (insert, update, delete) en una sola llamada, mejorando significativamente el rendimiento.

### **Tipos de bulk operations**

```python
from pymongo import InsertOne, UpdateOne, DeleteOne, ReplaceOne

# bulk_write() acepta una lista de operaciones
```

### **Ejemplo 1: Bulk write básico**

```python
from pymongo import InsertOne, UpdateOne, DeleteOne

# Preparar operaciones
operaciones = [
    # Insertar documentos
    InsertOne({"nombre": "Juan", "edad": 25}),
    InsertOne({"nombre": "Ana", "edad": 30}),
    
    # Actualizar documentos
    UpdateOne(
        {"nombre": "María"},
        {"$set": {"edad": 26}}
    ),
    UpdateOne(
        {"edad": {"$lt": 18}},
        {"$set": {"menor_edad": True}},
    ),
    
    # Eliminar documentos
    DeleteOne({"nombre": "Usuario Temporal"}),
]

# Ejecutar todas las operaciones
resultado = db.estudiantes.bulk_write(operaciones)

# Información del resultado
print(f"Insertados: {resultado.inserted_count}")
print(f"Modificados: {resultado.modified_count}")
print(f"Eliminados: {resultado.deleted_count}")
print(f"IDs insertados: {resultado.inserted_ids}")
```

### **Ejemplo 2: Ordered vs Unordered**

```python
# ORDERED (por defecto): se detiene en el primer error
# Útil cuando el orden importa o quieres parar ante errores

operaciones = [
    InsertOne({"_id": 1, "nombre": "Juan"}),
    InsertOne({"_id": 2, "nombre": "Ana"}),
    InsertOne({"_id": 1, "nombre": "Duplicado"}),  # ← ERROR aquí
    InsertOne({"_id": 3, "nombre": "Pedro"})  # ← NO se ejecuta
]

try:
    resultado = db.estudiantes.bulk_write(operaciones, ordered=True)
except Exception as e:
    print(f"Error: {e}")
    # Solo se insertaron 1 y 2

# UNORDERED: continúa ejecutando aunque haya errores
# Útil cuando quieres procesar todo lo que se pueda

operaciones = [
    InsertOne({"_id": 1, "nombre": "Juan"}),
    InsertOne({"_id": 2, "nombre": "Ana"}),
    InsertOne({"_id": 1, "nombre": "Duplicado"}),  # ← ERROR
    InsertOne({"_id": 3, "nombre": "Pedro"})  # ← SÍ se ejecuta
]

try:
    resultado = db.estudiantes.bulk_write(operaciones, ordered=False)
    print(f"Insertados: {resultado.inserted_count}")  # 3 (1, 2 y 3)
except BulkWriteError as e:
    print(f"Errores: {e.details['nErrors']}")
    print(f"Insertados exitosamente: {e.details['nInserted']}")
```

### **Ejemplo 3: Importación masiva con bulk**

```python
import csv
from datetime import datetime

def importar_estudiantes_csv(archivo_csv):
    """
    Importa estudiantes desde CSV usando bulk operations
    """
    operaciones = []
    
    with open(archivo_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            operacion = InsertOne({
                "nombre": row['nombre'],
                "email": row['email'],
                "edad": int(row['edad']),
                "ciudad": row['ciudad'],
                "fecha_registro": datetime.now(),
                "activo": True
            })
            operaciones.append(operacion)
            
            # Ejecutar en lotes de 1000 para evitar problemas de memoria
            if len(operaciones) >= 1000:
                resultado = db.estudiantes.bulk_write(operaciones, ordered=False)
                print(f"Lote procesado: {resultado.inserted_count} insertados")
                operaciones = []
        
        # Procesar el último lote
        if operaciones:
            resultado = db.estudiantes.bulk_write(operaciones, ordered=False)
            print(f"Último lote: {resultado.inserted_count} insertados")

# Uso
importar_estudiantes_csv('estudiantes.csv')
```

### **Ejemplo 4: Actualización masiva con condiciones diferentes**

```python
def actualizar_estudiantes_bulk(actualizaciones):
    """
    Actualiza múltiples estudiantes con diferentes criterios
    
    actualizaciones = [
        {"filtro": {"email": "user1@..."}, "datos": {"edad": 26}},
        {"filtro": {"email": "user2@..."}, "datos": {"ciudad": "Madrid"}},
        ...
    ]
    """
    operaciones = []
    
    for item in actualizaciones:
        operacion = UpdateOne(
            item['filtro'],
            {"$set": {**item['datos'], "fecha_modificacion": datetime.now()}}
        )
        operaciones.append(operacion)
    
    if operaciones:
        resultado = db.estudiantes.bulk_write(operaciones, ordered=False)
        return {
            "matched": resultado.matched_count,
            "modified": resultado.modified_count
        }

# Uso
actualizaciones = [
    {"filtro": {"email": "maria@example.com"}, "datos": {"edad": 26, "ciudad": "Barcelona"}},
    {"filtro": {"email": "juan@example.com"}, "datos": {"activo": False}},
    {"filtro": {"_id": ObjectId("...")}, "datos": {"telefono": "+34600111222"}},
]

resultado = actualizar_estudiantes_bulk(actualizaciones)
print(f"Actualizados: {resultado['modified']} de {resultado['matched']}")
```

### **Ejemplo 5: Sincronización de datos (upsert masivo)**

```python
def sincronizar_datos_externos(datos_externos):
    """
    Sincroniza datos desde sistema externo
    Si existe (por email), actualiza. Si no, inserta.
    """
    operaciones = []
    
    for dato in datos_externos:
        operacion = UpdateOne(
            {"email": dato['email']},  # Filtro
            {"$set": dato},  # Datos a actualizar/insertar
            upsert=True  # Insertar si no existe
        )
        operaciones.append(operacion)
    
    resultado = db.estudiantes.bulk_write(operaciones, ordered=False)
    
    return {
        "actualizados": resultado.modified_count,
        "insertados": resultado.upserted_count,
        "total_procesados": len(datos_externos)
    }

# Uso
datos_api = [
    {"email": "maria@example.com", "nombre": "María García", "edad": 26},
    {"email": "nuevo@example.com", "nombre": "Nuevo Usuario", "edad": 22},
    {"email": "juan@example.com", "nombre": "Juan López", "edad": 30},
]

resultado = sincronizar_datos_externos(datos_api)
print(f"Insertados: {resultado['insertados']}, Actualizados: {resultado['actualizados']}")
```

### **Cuándo usar bulk operations**

| **Usa bulk_write cuando** | **No uses bulk si** |
|----------------------------|---------------------|
| ✅ Necesitas insertar miles de documentos | ❌ Solo tienes 1-10 operaciones |
| ✅ Múltiples updates con diferentes filtros | ❌ Una actualización simple |
| ✅ Importación de datos (CSV, API, etc.) | ❌ Necesitas lógica compleja entre operaciones |
| ✅ Sincronización periódica | ❌ Requieres transacciones ACID |
| ✅ Rendimiento es crítico | ❌ Debugging (bulk oculta errores individuales) |

### **Rendimiento comparado**

```python
import time

# Método 1: Inserts individuales (LENTO)
inicio = time.time()
for i in range(1000):
    db.test.insert_one({"numero": i, "cuadrado": i**2})
tiempo1 = time.time() - inicio
print(f"Inserts individuales: {tiempo1:.2f} segundos")

# Método 2: Bulk insert (RÁPIDO)
db.test.drop()
inicio = time.time()
operaciones = [InsertOne({"numero": i, "cuadrado": i**2}) for i in range(1000)]
db.test.bulk_write(operaciones)
tiempo2 = time.time() - inicio
print(f"Bulk insert: {tiempo2:.2f} segundos")

print(f"Mejora: {tiempo1/tiempo2:.1f}x más rápido")
# Típicamente: 10-50x más rápido
```



# **9. Índices: Optimización de consultas**

## **9.1 Concepto de índice (igual que en SQL)**

Los índices en MongoDB funcionan igual que en SQL: estructuras de datos que mejoran la velocidad de las consultas a cambio de espacio adicional y overhead en escrituras.

### **¿Por qué son importantes?**

```python
# Sin índice: Collection Scan (escanea TODOS los documentos)
db.estudiantes.find({"email": "maria@example.com"})
# MongoDB debe revisar los 100,000 documentos → LENTO

# Con índice en email: Index Scan (búsqueda directa)
db.estudiantes.create_index("email")
db.estudiantes.find({"email": "maria@example.com"})
# MongoDB usa el índice → encuentra en milisegundos → RÁPIDO
```

### **Costo vs Beneficio**

| **Ventajas** | **Desventajas** |
|--------------|-----------------|
| ✅ Consultas mucho más rápidas | ❌ Ocupa espacio en disco |
| ✅ Ordenamiento eficiente | ❌ Escrituras más lentas (insert, update, delete) |
| ✅ Permite constraints (unique) | ❌ Requiere mantenimiento |

## **9.2 Tipos de índices**

### **Índice simple (single field)**

```python
# Crear índice en un campo
db.estudiantes.create_index("email")

# Con opciones
db.estudiantes.create_index("email", name="idx_email")

# Índice descendente (útil para ordenamiento)
db.estudiantes.create_index([("edad", -1)])  # -1 = descendente

# Ver índices existentes
indices = db.estudiantes.list_indexes()
for idx in indices:
    print(idx)
```

### **Índice único (unique)**

```python
# Similar a UNIQUE constraint en SQL
db.estudiantes.create_index("email", unique=True)

# Ahora no se puede insertar emails duplicados
try:
    db.estudiantes.insert_one({"email": "maria@example.com", "nombre": "María"})
    db.estudiantes.insert_one({"email": "maria@example.com", "nombre": "María2"})  # ERROR
except DuplicateKeyError:
    print("Email duplicado no permitido")

# Índice único con sparse (solo indexa docs que tienen el campo)
db.estudiantes.create_index("telefono", unique=True, sparse=True)
# Permite múltiples docs sin campo "telefono"
# Pero no permite dos docs con el mismo telefono
```

### **Índice compuesto (compound index)**

```python
# Índice en múltiples campos (como en SQL)
# El ORDEN importa mucho

db.estudiantes.create_index([
    ("ciudad", 1),  # Primero ciudad (ascendente)
    ("edad", -1)    # Luego edad (descendente)
])

# Este índice es útil para:
# ✅ find({"ciudad": "Madrid"})
# ✅ find({"ciudad": "Madrid"}).sort("edad", -1)
# ✅ find({"ciudad": "Madrid", "edad": {"$gt": 20}})
# ❌ find({"edad": 25})  ← NO usa el índice (edad es segundo campo)

# Regla: el índice sirve para queries que usan:
# - Solo el primer campo
# - Primer + segundo campo
# - Primer + segundo + tercer campo
# Pero NO sirve si omites el primer campo

# Ejemplo con 3 campos
db.ventas.create_index([
    ("categoria", 1),
    ("fecha", -1),
    ("precio", 1)
])

# Queries que usan el índice:
# ✅ {categoria: "Electrónica"}
# ✅ {categoria: "Electrónica", fecha: ...}
# ✅ {categoria: "Electrónica", fecha: ..., precio: ...}
# ❌ {fecha: ...}  ← NO usa índice
# ❌ {precio: ...}  ← NO usa índice
```

### **Índice de texto (text search)**

```python
# Para búsquedas de texto completo
db.posts.create_index([("contenido", "text"), ("titulo", "text")])

# Buscar documentos que contengan palabras
resultados = db.posts.find({
    "$text": {"$search": "mongodb python tutorial"}
})

# Búsqueda con frase exacta
resultados = db.posts.find({
    "$text": {"$search": '"aggregation pipeline"'}  # Comillas dobles
})

# Excluir palabras (con -)
resultados = db.posts.find({
    "$text": {"$search": "mongodb -sql"}  # MongoDB pero NO sql
})

# Ordenar por relevancia
resultados = db.posts.find(
    {"$text": {"$search": "mongodb"}},
    {"score": {"$meta": "textScore"}}
).sort([("score", {"$meta": "textScore"})])

# Solo un índice de texto por colección
# Alternativa: usar regex para búsquedas simples
db.posts.find({"titulo": {"$regex": "mongodb", "$options": "i"}})
```

### **Índice en arrays (multikey index)**

```python
# Automáticamente se crea multikey index si el campo es array
db.estudiantes.create_index("hobbies")

# Ahora estas queries son eficientes:
db.estudiantes.find({"hobbies": "lectura"})
db.estudiantes.find({"hobbies": {"$in": ["lectura", "deportes"]}})

# Índice en arrays de subdocumentos
db.estudiantes.create_index("cursos.nombre")

# Query eficiente:
db.estudiantes.find({"cursos.nombre": "Python"})
```

### **Índice en subdocumentos (dot notation)**

```python
# Índice en campo anidado
db.estudiantes.create_index("direccion.ciudad")

# Query eficiente:
db.estudiantes.find({"direccion.ciudad": "Madrid"})

# Índice compuesto con campos anidados
db.estudiantes.create_index([
    ("direccion.ciudad", 1),
    ("edad", -1)
])
```

### **Índice TTL (Time To Live) - auto-eliminación**

```python
# Documentos se eliminan automáticamente después de N segundos
db.sesiones.create_index("fecha_creacion", expireAfterSeconds=3600)  # 1 hora

# Insertar sesión
db.sesiones.insert_one({
    "usuario_id": ObjectId("..."),
    "token": "abc123",
    "fecha_creacion": datetime.now()  # Debe ser datetime
})

# MongoDB elimina automáticamente documentos donde:
# fecha_creacion + 3600 segundos < fecha_actual

# Útil para:
# - Sesiones temporales
# - Logs que caducan
# - Caché temporal
# - Tokens de verificación
```

### **Índice parcial (partial index)**

```python
# Indexa solo documentos que cumplen un criterio
# Ahorra espacio y mejora rendimiento

db.estudiantes.create_index(
    "email",
    partialFilterExpression={"activo": True}
)

# El índice solo incluye estudiantes activos
# Query que USA el índice:
db.estudiantes.find({"email": "maria@example.com", "activo": True})

# Query que NO usa el índice:
db.estudiantes.find({"email": "maria@example.com"})  # Falta activo:True

# Ejemplo: índice solo para mayores de edad
db.estudiantes.create_index(
    "fecha_nacimiento",
    partialFilterExpression={"edad": {"$gte": 18}}
)
```

### **Índice geoespacial (2dsphere)**

```python
# Para consultas de ubicación (coordenadas)
db.lugares.create_index([("ubicacion", "2dsphere")])

# Documento
{
    "nombre": "Restaurante",
    "ubicacion": {
        "type": "Point",
        "coordinates": [-3.7038, 40.4168]  # [longitud, latitud]
    }
}

# Buscar lugares cerca de una ubicación
db.lugares.find({
    "ubicacion": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": [-3.7000, 40.4000]
            },
            "$maxDistance": 5000  # 5 km
        }
    }
})
```

## **9.3 explain() - Análisis de rendimiento**

```python
# explain() muestra cómo MongoDB ejecuta la query
# Similar a EXPLAIN en SQL

# Ver plan de ejecución
explicacion = db.estudiantes.find({"email": "maria@example.com"}).explain()

print(explicacion['executionStats'])

# Información importante:
# - executionTimeMillis: tiempo de ejecución
# - totalDocsExamined: documentos examinados
# - totalKeysExamined: claves de índice examinadas
# - executionStages.stage: tipo de scan (COLLSCAN vs IXSCAN)

# Ejemplo sin índice
db.estudiantes.find({"ciudad": "Madrid"}).explain("executionStats")
# stage: "COLLSCAN" ← escanea toda la colección
# totalDocsExamined: 100000 ← revisó todos los documentos

# Crear índice
db.estudiantes.create_index("ciudad")

# Ejemplo con índice
db.estudiantes.find({"ciudad": "Madrid"}).explain("executionStats")
# stage: "IXSCAN" ← usa índice
# totalDocsExamined: 1500 ← solo revisó los que coinciden
# totalKeysExamined: 1500 ← usó índice

# Modos de explain:
# "queryPlanner" - solo muestra el plan (default)
# "executionStats" - ejecuta y muestra estadísticas
# "allPlansExecution" - prueba todos los planes posibles
```

### **Interpretar explain()**

```python
# Ejemplo completo
resultado = db.estudiantes.find(
    {"ciudad": "Madrid", "edad": {"$gte": 18}}
).sort("edad", -1).explain("executionStats")

# Información clave:
stats = resultado['executionStats']

print(f"Tiempo: {stats['executionTimeMillis']} ms")
print(f"Docs examinados: {stats['totalDocsExamined']}")
print(f"Docs devueltos: {stats['nReturned']}")
print(f"Índice usado: {stats['executionStages']['inputStage']['indexName']}")

# Eficiencia del índice
eficiencia = stats['nReturned'] / stats['totalDocsExamined']
print(f"Eficiencia: {eficiencia:.2%}")

# Ideal: eficiencia cercana a 100%
# Significa que el índice es muy selectivo
```

### **Índices cubiertos (covered queries)**

```python
# Query cubierta: el resultado se obtiene SOLO del índice
# Sin necesidad de acceder a los documentos completos

# Crear índice con los campos que se consultan y proyectan
db.estudiantes.create_index([("email", 1), ("nombre", 1)])

# Query cubierta
resultado = db.estudiantes.find(
    {"email": "maria@example.com"},
    {"email": 1, "nombre": 1, "_id": 0}  # ← Importante: _id: 0
).explain("executionStats")

# Si totalDocsExamined = 0 → query cubierta
# MongoDB obtuvo todo del índice, sin leer documentos

# Ventajas:
# - Mucho más rápido (índice está en RAM)
# - Menos I/O
```

## **9.4 Buenas prácticas con índices**

### **Cuándo crear índices**

```python
# ✅ Crea índices para:
# - Campos en queries frecuentes (WHERE, filtros)
# - Campos usados en sort()
# - Campos de foreign keys (referencias)
# - Campos únicos (email, username, etc.)

# ❌ NO crear índices para:
# - Campos que rara vez se consultan
# - Campos con baja cardinalidad (pocos valores únicos)
#   Ejemplo: campo "activo" con solo true/false
# - Colecciones pequeñas (< 1000 docs)
# - Campos que cambian constantemente

# Ejemplo: índices recomendados para colección estudiantes
db.estudiantes.create_index("email", unique=True)  # Búsquedas frecuentes + único
db.estudiantes.create_index([("ciudad", 1), ("edad", -1)])  # Filtros + ordenamiento
db.estudiantes.create_index("fecha_registro")  # Para reportes temporales
```

### **Monitorear uso de índices**

```python
# Ver estadísticas de uso de índices
stats = db.estudiantes.aggregate([
    {"$indexStats": {}}
])

for stat in stats:
    print(f"Índice: {stat['name']}")
    print(f"  Accesos: {stat['accesses']['ops']}")
    print(f"  Última vez: {stat['accesses']['since']}")

# Eliminar índices no utilizados
# Si un índice tiene 0 accesos, considera eliminarlo
db.estudiantes.drop_index("nombre_indice_no_usado")
```

### **Límites y consideraciones**

```python
# Límites de MongoDB:
# - Máximo 64 índices por colección
# - Tamaño máximo de clave de índice: 1024 bytes
# - Solo un índice de texto por colección

# Overhead de índices:
# - Cada insert/update/delete debe actualizar todos los índices
# - Los índices ocupan RAM (idealmente deben caber en memoria)

# Estrategia óptima:
# - Crea índices para queries críticas
# - Monitorea rendimiento
# - Elimina índices no utilizados
# - Considera índices compuestos en lugar de múltiples simples
```

### **Ejemplo: análisis completo de una query lenta**

```python
# 1. Identificar query lenta
query = {"ciudad": "Madrid", "edad": {"$gte": 18, "$lte": 30}}
sort = [("fecha_registro", -1)]

# 2. Ejecutar con explain
resultado = db.estudiantes.find(query).sort(sort).explain("executionStats")

# 3. Analizar
stats = resultado['executionStats']
print(f"Tiempo: {stats['executionTimeMillis']} ms")
print(f"Stage: {stats['executionStages']['stage']}")

if stats['executionStages']['stage'] == 'COLLSCAN':
    print("⚠️ No usa índice - escaneo completo")
    
    # 4. Crear índice apropiado
    db.estudiantes.create_index([
        ("ciudad", 1),
        ("edad", 1),
        ("fecha_registro", -1)
    ])
    
    # 5. Volver a probar
    resultado2 = db.estudiantes.find(query).sort(sort).explain("executionStats")
    stats2 = resultado2['executionStats']
    
    mejora = stats['executionTimeMillis'] / stats2['executionTimeMillis']
    print(f"✅ Mejora: {mejora:.1f}x más rápido")
```



# **10. Transacciones (opcional pero importante)**

## **10.1 ACID en MongoDB**

MongoDB soporta transacciones ACID multi-documento desde la versión 4.0 (replica sets) y 4.2 (sharded clusters).

### **¿Qué es ACID?**

- **Atomicity**: Todo o nada (rollback si falla algo)
- **Consistency**: Los datos quedan en estado válido
- **Isolation**: Las transacciones no se interfieren
- **Durability**: Los cambios persisten

### **Cuándo usar transacciones**

```python
# ✅ Usa transacciones cuando necesitas:
# - Operaciones relacionadas que deben ejecutarse todas o ninguna
# - Transferencias (dinero, inventario, etc.)
# - Actualizar múltiples colecciones de forma atómica

# ❌ NO necesitas transacciones para:
# - Operaciones en un solo documento (ya son atómicas)
# - Lecturas simples
# - La mayoría de casos (diseño de documentos embebidos suele evitarlas)
```

## **10.2 Ejemplo práctico: Transferencia bancaria**

```python
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Configuración
client = MongoClient('mongodb://localhost:27017/')
db = client['banco']
cuentas = db['cuentas']

# Datos iniciales
cuentas.delete_many({})
cuentas.insert_many([
    {"_id": "cuenta_A", "titular": "María", "saldo": 1000.00},
    {"_id": "cuenta_B", "titular": "Juan", "saldo": 500.00}
])

def transferir_dinero(origen, destino, cantidad):
    """
    Transferir dinero de una cuenta a otra usando transacciones
    """
    # Iniciar sesión
    with client.start_session() as session:
        # Iniciar transacción
        with session.start_transaction():
            try:
                # 1. Verificar saldo suficiente
                cuenta_origen = cuentas.find_one(
                    {"_id": origen},
                    session=session
                )
                
                if not cuenta_origen:
                    raise ValueError(f"Cuenta origen {origen} no existe")
                
                if cuenta_origen['saldo'] < cantidad:
                    raise ValueError(f"Saldo insuficiente: {cuenta_origen['saldo']}")
                
                # 2. Restar de cuenta origen
                cuentas.update_one(
                    {"_id": origen},
                    {"$inc": {"saldo": -cantidad}},
                    session=session
                )
                
                # 3. Sumar a cuenta destino
                resultado = cuentas.update_one(
                    {"_id": destino},
                    {"$inc": {"saldo": cantidad}},
                    session=session
                )
                
                if resultado.matched_count == 0:
                    raise ValueError(f"Cuenta destino {destino} no existe")
                
                # 4. Registrar transacción
                db.transacciones.insert_one({
                    "origen": origen,
                    "destino": destino,
                    "cantidad": cantidad,
                    "fecha": datetime.now(),
                    "estado": "completada"
                }, session=session)
                
                # Si todo va bien, se hace commit automático al salir del with
                print(f"✅ Transferencia exitosa: {cantidad}€ de {origen} a {destino}")
                return True
                
            except Exception as e:
                # Si hay error, se hace rollback automático
                print(f"❌ Error en transferencia: {e}")
                # No es necesario llamar a abort_transaction(), se hace automático
                return False

# Ejemplo 1: Transferencia exitosa
transferir_dinero("cuenta_A", "cuenta_B", 200.00)

# Verificar saldos
print("Cuenta A:", cuentas.find_one({"_id": "cuenta_A"})['saldo'])  # 800
print("Cuenta B:", cuentas.find_one({"_id": "cuenta_B"})['saldo'])  # 700

# Ejemplo 2: Transferencia fallida (saldo insuficiente)
transferir_dinero("cuenta_A", "cuenta_B", 2000.00)

# Verificar saldos (no cambiaron)
print("Cuenta A:", cuentas.find_one({"_id": "cuenta_A"})['saldo'])  # 800
print("Cuenta B:", cuentas.find_one({"_id": "cuenta_B"})['saldo'])  # 700
```

### **Transacciones con callback**

```python
def callback_transferencia(session, origen, destino, cantidad):
    """
    Función callback para la transacción
    """
    # Verificar saldo
    cuenta_origen = cuentas.find_one({"_id": origen}, session=session)
    if cuenta_origen['saldo'] < cantidad:
        raise ValueError("Saldo insuficiente")
    
    # Operaciones
    cuentas.update_one(
        {"_id": origen},
        {"$inc": {"saldo": -cantidad}},
        session=session
    )
    cuentas.update_one(
        {"_id": destino},
        {"$inc": {"saldo": cantidad}},
        session=session
    )

# Ejecutar con manejo de reintentos automático
with client.start_session() as session:
    session.with_transaction(
        lambda s: callback_transferencia(s, "cuenta_A", "cuenta_B", 100),
        read_concern=ReadConcern("snapshot"),
        write_concern=WriteConcern("majority")
    )
```

### **Niveles de aislamiento**

```python
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern

# Transacción con configuración de aislamiento
with client.start_session() as session:
    session.start_transaction(
        read_concern=ReadConcern("snapshot"),  # Aislamiento snapshot
        write_concern=WriteConcern("majority"),  # Mayoría de nodos
        read_preference=ReadPreference.PRIMARY
    )
    
    # ... operaciones ...
    
    session.commit_transaction()
```



# **11. Caso práctico completo**

## **Sistema de blog: usuarios, posts, comentarios, categorías**

Vamos a implementar un sistema completo que incluye todas las técnicas aprendidas.

### **11.1 Diseño del esquema**

```python
# Colección: usuarios
{
    "_id": ObjectId(),
    "username": "mariadev",
    "email": "maria@example.com",
    "password_hash": "...",
    "perfil": {
        "nombre_completo": "María García",
        "avatar": "https://...",
        "biografia": "Desarrolladora Python",
        "redes_sociales": {
            "twitter": "@mariadev",
            "github": "mariadev"
        }
    },
    "estadisticas": {
        "posts_publicados": 15,
        "comentarios_realizados": 48,
        "seguidores": 120,
        "siguiendo": 85
    },
    "fecha_registro": datetime(2024, 1, 15),
    "ultimo_acceso": datetime(2024, 2, 5),
    "activo": True
}

# Colección: posts
{
    "_id": ObjectId(),
    "autor_id": ObjectId("..."),  # Referencia a usuario
    "titulo": "Introducción a MongoDB",
    "slug": "introduccion-a-mongodb",
    "contenido": "MongoDB es una base de datos...",
    "resumen": "Aprende los fundamentos de MongoDB...",
    "imagen_destacada": "https://...",
    "categorias": ["mongodb", "bases-de-datos", "nosql"],  # Array de strings
    "tags": ["tutorial", "principiante"],
    "estado": "publicado",  # borrador, publicado, archivado
    "fecha_publicacion": datetime(2024, 1, 20),
    "fecha_modificacion": datetime(2024, 1, 21),
    "estadisticas": {
        "vistas": 1250,
        "likes": 45,
        "comentarios": 12,
        "compartidos": 8
    },
    "seo": {
        "meta_descripcion": "...",
        "palabras_clave": ["mongodb", "tutorial"]
    }
}

# Colección: comentarios
{
    "_id": ObjectId(),
    "post_id": ObjectId("..."),  # Referencia a post
    "autor_id": ObjectId("..."),  # Referencia a usuario
    "contenido": "Excelente tutorial, muy claro!",
    "fecha": datetime(2024, 1, 21, 10, 30),
    "editado": False,
    "fecha_edicion": None,
    "likes": 5,
    "respuesta_a": None,  # ObjectId si es respuesta a otro comentario
    "estado": "aprobado"  # pendiente, aprobado, spam
}

# Colección: categorias (opcional, para metadatos)
{
    "_id": "mongodb",
    "nombre": "MongoDB",
    "descripcion": "Todo sobre MongoDB",
    "color": "#13AA52",
    "total_posts": 15
}
```

### **11.2 Implementación paso a paso**

```python
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId
from datetime import datetime
import re

# Conexión
client = MongoClient('mongodb://localhost:27017/')
db = client['blog']
usuarios = db['usuarios']
posts = db['posts']
comentarios = db['comentarios']
categorias = db['categorias']

# Crear índices
def crear_indices():
    """Índices para optimizar consultas"""
    # Usuarios
    usuarios.create_index("email", unique=True)
    usuarios.create_index("username", unique=True)
    
    # Posts
    posts.create_index([("autor_id", ASCENDING), ("fecha_publicacion", DESCENDING)])
    posts.create_index("slug", unique=True)
    posts.create_index("categorias")  # Multikey index
    posts.create_index([("titulo", "text"), ("contenido", "text")])  # Text search
    posts.create_index([("estado", ASCENDING), ("fecha_publicacion", DESCENDING)])
    
    # Comentarios
    comentarios.create_index([("post_id", ASCENDING), ("fecha", DESCENDING)])
    comentarios.create_index("autor_id")
    
    print("✅ Índices creados")

crear_indices()
```

### **CRUD completo del blog**

```python
class BlogManager:
    def __init__(self, db):
        self.db = db
        self.usuarios = db['usuarios']
        self.posts = db['posts']
        self.comentarios = db['comentarios']
        self.categorias = db['categorias']
    
    # ============ USUARIOS ============
    
    def crear_usuario(self, username, email, password, nombre_completo):
        """Crear nuevo usuario"""
        # Verificar que no existe
        if self.usuarios.find_one({"$or": [{"email": email}, {"username": username}]}):
            return {"error": "Email o username ya existe"}
        
        usuario = {
            "username": username,
            "email": email,
            "password_hash": self._hash_password(password),
            "perfil": {
                "nombre_completo": nombre_completo,
                "avatar": None,
                "biografia": "",
                "redes_sociales": {}
            },
            "estadisticas": {
                "posts_publicados": 0,
                "comentarios_realizados": 0,
                "seguidores": 0,
                "siguiendo": 0
            },
            "fecha_registro": datetime.now(),
            "ultimo_acceso": datetime.now(),
            "activo": True
        }
        
        resultado = self.usuarios.insert_one(usuario)
        return {"success": True, "user_id": resultado.inserted_id}
    
    def _hash_password(self, password):
        """Simula hash de contraseña"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    def autenticar(self, email, password):
        """Autenticar usuario"""
        usuario = self.usuarios.find_one({"email": email})
        
        if not usuario:
            return {"error": "Usuario no encontrado"}
        
        if usuario['password_hash'] != self._hash_password(password):
            return {"error": "Contraseña incorrecta"}
        
        # Actualizar último acceso
        self.usuarios.update_one(
            {"_id": usuario['_id']},
            {"$set": {"ultimo_acceso": datetime.now()}}
        )
        
        return {"success": True, "user_id": usuario['_id']}
    
    # ============ POSTS ============
    
    def crear_post(self, autor_id, titulo, contenido, categorias, resumen=None):
        """Crear nuevo post"""
        slug = self._generar_slug(titulo)
        
        # Verificar slug único
        if self.posts.find_one({"slug": slug}):
            slug = f"{slug}-{int(datetime.now().timestamp())}"
        
        post = {
            "autor_id": autor_id,
            "titulo": titulo,
            "slug": slug,
            "contenido": contenido,
            "resumen": resumen or contenido[:200],
            "categorias": categorias,
            "tags": [],
            "estado": "publicado",
            "fecha_publicacion": datetime.now(),
            "fecha_modificacion": datetime.now(),
            "estadisticas": {
                "vistas": 0,
                "likes": 0,
                "comentarios": 0,
                "compartidos": 0
            }
        }
        
        resultado = self.posts.insert_one(post)
        
        # Incrementar contador de posts del usuario
        self.usuarios.update_one(
            {"_id": autor_id},
            {"$inc": {"estadisticas.posts_publicados": 1}}
        )
        
        # Actualizar contador de categorías
        for cat in categorias:
            self.categorias.update_one(
                {"_id": cat},
                {"$inc": {"total_posts": 1}},
                upsert=True
            )
        
        return {"success": True, "post_id": resultado.inserted_id}
    
    def _generar_slug(self, titulo):
        """Generar slug URL-friendly"""
        slug = titulo.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        return slug
    
    def obtener_post(self, slug, incrementar_vista=True):
        """Obtener post por slug con información del autor"""
        pipeline = [
            {"$match": {"slug": slug, "estado": "publicado"}},
            {"$lookup": {
                "from": "usuarios",
                "localField": "autor_id",
                "foreignField": "_id",
                "as": "autor"
            }},
            {"$unwind": "$autor"},
            {"$project": {
                "titulo": 1,
                "contenido": 1,
                "resumen": 1,
                "categorias": 1,
                "fecha_publicacion": 1,
                "estadisticas": 1,
                "autor": {
                    "username": 1,
                    "perfil.nombre_completo": 1,
                    "perfil.avatar": 1
                }
            }}
        ]
        
        resultado = list(self.posts.aggregate(pipeline))
        
        if not resultado:
            return None
        
        post = resultado[0]
        
        # Incrementar contador de vistas
        if incrementar_vista:
            self.posts.update_one(
                {"slug": slug},
                {"$inc": {"estadisticas.vistas": 1}}
            )
            post['estadisticas']['vistas'] += 1
        
        return post
    
    def listar_posts(self, pagina=1, por_pagina=10, categoria=None, autor_id=None):
        """Listar posts con paginación y filtros"""
        filtro = {"estado": "publicado"}
        
        if categoria:
            filtro["categorias"] = categoria
        
        if autor_id:
            filtro["autor_id"] = autor_id
        
        skip = (pagina - 1) * por_pagina
        
        pipeline = [
            {"$match": filtro},
            {"$sort": {"fecha_publicacion": -1}},
            {"$skip": skip},
            {"$limit": por_pagina},
            {"$lookup": {
                "from": "usuarios",
                "localField": "autor_id",
                "foreignField": "_id",
                "as": "autor"
            }},
            {"$unwind": "$autor"},
            {"$project": {
                "titulo": 1,
                "slug": 1,
                "resumen": 1,
                "categorias": 1,
                "fecha_publicacion": 1,
                "estadisticas": 1,
                "autor.username": 1,
                "autor.perfil.nombre_completo": 1
            }}
        ]
        
        posts = list(self.posts.aggregate(pipeline))
        total = self.posts.count_documents(filtro)
        
        return {
            "posts": posts,
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total": total,
            "total_paginas": (total + por_pagina - 1) // por_pagina
        }
    
    def buscar_posts(self, query):
        """Búsqueda de texto completo"""
        resultados = self.posts.find(
            {"$text": {"$search": query}, "estado": "publicado"},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(20)
        
        return list(resultados)
    
    def actualizar_post(self, post_id, **campos):
        """Actualizar campos de un post"""
        campos['fecha_modificacion'] = datetime.now()
        
        resultado = self.posts.update_one(
            {"_id": post_id},
            {"$set": campos}
        )
        
        return {"success": resultado.modified_count > 0}
    
    def eliminar_post(self, post_id):
        """Eliminar post (soft delete)"""
        resultado = self.posts.update_one(
            {"_id": post_id},
            {"$set": {
                "estado": "archivado",
                "fecha_eliminacion": datetime.now()
            }}
        )
        
        if resultado.modified_count > 0:
            # Decrementar contador del usuario
            post = self.posts.find_one({"_id": post_id})
            self.usuarios.update_one(
                {"_id": post['autor_id']},
                {"$inc": {"estadisticas.posts_publicados": -1}}
            )
        
        return {"success": resultado.modified_count > 0}
    
    # ============ COMENTARIOS ============
    
    def agregar_comentario(self, post_id, autor_id, contenido, respuesta_a=None):
        """Agregar comentario a un post"""
        comentario = {
            "post_id": post_id,
            "autor_id": autor_id,
            "contenido": contenido,
            "fecha": datetime.now(),
            "editado": False,
            "likes": 0,
            "respuesta_a": respuesta_a,
            "estado": "aprobado"
        }
        
        resultado = self.comentarios.insert_one(comentario)
        
        # Incrementar contador de comentarios del post
        self.posts.update_one(
            {"_id": post_id},
            {"$inc": {"estadisticas.comentarios": 1}}
        )
        
        # Incrementar contador de comentarios del usuario
        self.usuarios.update_one(
            {"_id": autor_id},
            {"$inc": {"estadisticas.comentarios_realizados": 1}}
        )
        
        return {"success": True, "comentario_id": resultado.inserted_id}
    
    def obtener_comentarios(self, post_id):
        """Obtener comentarios de un post con información del autor"""
        pipeline = [
            {"$match": {"post_id": post_id, "estado": "aprobado"}},
            {"$sort": {"fecha": -1}},
            {"$lookup": {
                "from": "usuarios",
                "localField": "autor_id",
                "foreignField": "_id",
                "as": "autor"
            }},
            {"$unwind": "$autor"},
            {"$project": {
                "contenido": 1,
                "fecha": 1,
                "editado": 1,
                "likes": 1,
                "respuesta_a": 1,
                "autor": {
                    "username": 1,
                    "perfil.nombre_completo": 1,
                    "perfil.avatar": 1
                }
            }}
        ]
        
        return list(self.comentarios.aggregate(pipeline))
    
    # ============ ESTADÍSTICAS ============
    
    def estadisticas_globales(self):
        """Estadísticas del blog"""
        return {
            "total_usuarios": self.usuarios.count_documents({"activo": True}),
            "total_posts": self.posts.count_documents({"estado": "publicado"}),
            "total_comentarios": self.comentarios.count_documents({"estado": "aprobado"}),
            "total_categorias": self.categorias.count_documents({})
        }
    
    def posts_mas_populares(self, limite=10):
        """Posts con más vistas"""
        pipeline = [
            {"$match": {"estado": "publicado"}},
            {"$sort": {"estadisticas.vistas": -1}},
            {"$limit": limite},
            {"$project": {
                "titulo": 1,
                "slug": 1,
                "estadisticas.vistas": 1,
                "estadisticas.likes": 1,
                "estadisticas.comentarios": 1
            }}
        ]
        
        return list(self.posts.aggregate(pipeline))
    
    def autores_mas_activos(self, limite=10):
        """Autores con más posts"""
        pipeline = [
            {"$match": {"estado": "publicado"}},
            {"$group": {
                "_id": "$autor_id",
                "total_posts": {"$sum": 1},
                "total_vistas": {"$sum": "$estadisticas.vistas"},
                "total_comentarios": {"$sum": "$estadisticas.comentarios"}
            }},
            {"$sort": {"total_posts": -1}},
            {"$limit": limite},
            {"$lookup": {
                "from": "usuarios",
                "localField": "_id",
                "foreignField": "_id",
                "as": "usuario"
            }},
            {"$unwind": "$usuario"},
            {"$project": {
                "_id": 0,
                "username": "$usuario.username",
                "nombre": "$usuario.perfil.nombre_completo",
                "total_posts": 1,
                "total_vistas": 1,
                "total_comentarios": 1
            }}
        ]
        
        return list(self.posts.aggregate(pipeline))
    
    def posts_por_categoria(self):
        """Cantidad de posts por categoría"""
        pipeline = [
            {"$match": {"estado": "publicado"}},
            {"$unwind": "$categorias"},
            {"$group": {
                "_id": "$categorias",
                "total": {"$sum": 1}
            }},
            {"$sort": {"total": -1}},
            {"$project": {
                "_id": 0,
                "categoria": "$_id",
                "total": 1
            }}
        ]
        
        return list(self.posts.aggregate(pipeline))

# ============ USO DEL SISTEMA ============

# Crear instancia
blog = BlogManager(db)

# Crear usuario
usuario = blog.crear_usuario(
    username="mariadev",
    email="maria@example.com",
    password="password123",
    nombre_completo="María García"
)
print("Usuario creado:", usuario)

# Autenticar
auth = blog.autenticar("maria@example.com", "password123")
print("Autenticación:", auth)

# Crear post
post = blog.crear_post(
    autor_id=usuario['user_id'],
    titulo="Introducción a MongoDB con Python",
    contenido="En este tutorial aprenderemos los fundamentos de MongoDB...",
    categorias=["mongodb", "python", "tutorial"],
    resumen="Aprende MongoDB desde cero"
)
print("Post creado:", post)

# Obtener post
post_completo = blog.obtener_post("introduccion-a-mongodb-con-python")
print("Post:", post_completo['titulo'])
print("Autor:", post_completo['autor']['perfil']['nombre_completo'])

# Agregar comentario
comentario = blog.agregar_comentario(
    post_id=post['post_id'],
    autor_id=usuario['user_id'],
    contenido="Excelente tutorial, muy claro!"
)
print("Comentario agregado:", comentario)

# Listar posts
posts = blog.listar_posts(pagina=1, por_pagina=10)
print(f"Total de posts: {posts['total']}")
for p in posts['posts']:
    print(f"  - {p['titulo']} por {p['autor']['username']}")

# Estadísticas
stats = blog.estadisticas_globales()
print("Estadísticas:", stats)

# Posts más populares
populares = blog.posts_mas_populares(limite=5)
print("Posts más populares:")
for p in populares:
    print(f"  - {p['titulo']}: {p['estadisticas']['vistas']} vistas")

# Posts por categoría
por_categoria = blog.posts_por_categoria()
print("Posts por categoría:")
for c in por_categoria:
    print(f"  - {c['categoria']}: {c['total']} posts")
```



# **12. Buenas prácticas y patrones**

## **Naming conventions**

```python
# Bases de datos y colecciones: snake_case minúsculas
db = client['mi_aplicacion']
usuarios = db['usuarios']
historial_compras = db['historial_compras']

# Campos de documentos: snake_case (consistente con Python)
documento = {
    "nombre_completo": "María García",
    "fecha_nacimiento": datetime(1995, 3, 15),
    "direccion_principal": {
        "calle": "Gran Vía",
        "codigo_postal": "28013"
    }
}

# Evitar nombres genéricos
# ❌ data, info, item, object
# ✅ estudiante, producto, pedido

# Usar plural para colecciones
# ✅ usuarios, posts, comentarios
# ❌ usuario, post, comentario
```

## **Validación con JSON Schema**

```python
# Definir esquema de validación
esquema_validacion = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nombre", "email", "edad"],
        "properties": {
            "nombre": {
                "bsonType": "string",
                "description": "Nombre completo del estudiante"
            },
            "email": {
                "bsonType": "string",
                "pattern": "^\\S+@\\S+\\.\\S+$",
                "description": "Email válido"
            },
            "edad": {
                "bsonType": "int",
                "minimum": 16,
                "maximum": 100,
                "description": "Edad entre 16 y 100"
            },
            "telefono": {
                "bsonType": ["string", "null"],
                "description": "Teléfono opcional"
            }
        }
    }
}

# Aplicar validación a colección existente
db.command({
    "collMod": "estudiantes",
    "validator": esquema_validacion,
    "validationLevel": "strict",  # strict o moderate
    "validationAction": "error"  # error o warn
})

# O crear colección con validación
db.create_collection("estudiantes", validator=esquema_validacion)

# Probar validación
try:
    db.estudiantes.insert_one({"nombre": "Juan"})  # Falta email y edad
except Exception as e:
    print("Error de validación:", e)
```

## **Manejo de errores y excepciones**

```python
from pymongo.errors import (
    DuplicateKeyError,
    WriteError,
    ConnectionFailure,
    ServerSelectionTimeoutError,
    BulkWriteError
)

def insertar_estudiante_seguro(datos):
    """Insertar con manejo completo de errores"""
    try:
        resultado = db.estudiantes.insert_one(datos)
        return {"success": True, "id": resultado.inserted_id}
    
    except DuplicateKeyError as e:
        # Email o username duplicado
        campo = list(e.details['keyPattern'].keys())[0]
        return {"error": f"El {campo} ya está registrado"}
    
    except WriteError as e:
        # Error de validación de esquema
        return {"error": f"Datos inválidos: {e.details}"}
    
    except ConnectionFailure:
        # Problema de conexión
        return {"error": "No se pudo conectar a la base de datos"}
    
    except Exception as e:
        # Cualquier otro error
        return {"error": f"Error inesperado: {str(e)}"}

# Uso
resultado = insertar_estudiante_seguro({
    "nombre": "Juan López",
    "email": "juan@example.com",
    "edad": 25
})

if "error" in resultado:
    print(f"❌ {resultado['error']}")
else:
    print(f"✅ Estudiante creado con ID: {resultado['id']}")
```

## **Conexiones y pools**

```python
from pymongo import MongoClient
from pymongo.pool import PoolOptions

# Configuración de pool de conexiones
client = MongoClient(
    'mongodb://localhost:27017/',
    maxPoolSize=50,  # Máximo de conexiones simultáneas
    minPoolSize=10,  # Mínimo de conexiones mantenidas
    maxIdleTimeMS=30000,  # Tiempo antes de cerrar conexión inactiva
    serverSelectionTimeoutMS=5000,  # Timeout para selección de servidor
    connectTimeoutMS=10000,  # Timeout para conexión inicial
    socketTimeoutMS=20000  # Timeout para operaciones
)

# Singleton pattern para conexión
class Database:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_client(self):
        if self._client is None:
            self._client = MongoClient('mongodb://localhost:27017/')
        return self._client
    
    def get_db(self, db_name='mi_app'):
        return self.get_client()[db_name]

# Uso
db_singleton = Database()
db = db_singleton.get_db('universidad')
```

## **Logging de queries**

```python
import logging
from pymongo import monitoring

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mongodb')

# Listener para monitorear comandos
class CommandLogger(monitoring.CommandListener):
    def started(self, event):
        logger.info(f"Comando iniciado: {event.command_name}")
        logger.debug(f"Detalles: {event.command}")
    
    def succeeded(self, event):
        logger.info(f"Comando exitoso en {event.duration_micros / 1000:.2f}ms")
    
    def failed(self, event):
        logger.error(f"Comando fallido: {event.failure}")

# Registrar listener
monitoring.register(CommandLogger())

# Ahora todas las operaciones se loguean
db.estudiantes.find({"edad": {"$gt": 20}})
# INFO: Comando iniciado: find
# INFO: Comando exitoso en 2.45ms
```



# **13. Ejercicios propuestos**

## **Ejercicio 1: CRUD básico**

```python
"""
Crea una aplicación de gestión de biblioteca con:
- Colección 'libros' con: titulo, autor, isbn (único), año, genero, disponible
- Colección 'prestamos' con: libro_id, usuario, fecha_prestamo, fecha_devolucion

Implementa:
1. Insertar libros
2. Buscar libros por género
3. Registrar préstamo (cambiar disponible=False)
4. Registrar devolución (cambiar disponible=True)
5. Listar libros prestados actualmente
6. Usuario con más préstamos
"""

# Solución comentada...
# (Ver solución al final del documento)
```

## **Ejercicio 2: Agregaciones**

```python
"""
Base de datos de e-commerce con colección 'pedidos':
{
    "cliente_id": ObjectId(),
    "fecha": datetime(),
    "productos": [
        {"nombre": "...", "cantidad": 2, "precio": 29.99},
        {"nombre": "...", "cantidad": 1, "precio": 49.99}
    ],
    "total": 109.97,
    "estado": "completado"
}

Calcula usando aggregation:
1. Total de ventas por mes
2. Producto más vendido (cantidad)
3. Cliente que más ha gastado
4. Promedio de items por pedido
5. Pedidos por estado
"""
```

## **Ejercicio 3: Modelado relacional**

```python
"""
Sistema de gestión de cursos online:
- Profesores (pueden dar múltiples cursos)
- Cursos (pertenecen a un profesor, tienen múltiples estudiantes)
- Estudiantes (pueden estar en múltiples cursos)
- Lecciones (pertenecen a un curso)
- Progreso (estudiante x lección: completada, tiempo)

Diseña el esquema decidiendo qué embeber y qué referenciar.
Implementa:
1. Matricular estudiante en curso
2. Marcar lección como completada
3. Obtener progreso de un estudiante en un curso (%)
4. Listar cursos de un profesor con número de estudiantes
5. Estudiantes que han completado un curso (100%)
"""
```

## **Ejercicio 4: Búsqueda y filtros complejos**

```python
"""
Base de datos de inmuebles:
{
    "tipo": "piso",
    "direccion": {...},
    "caracteristicas": {
        "habitaciones": 3,
        "baños": 2,
        "metros_cuadrados": 85,
        "planta": 3,
        "ascensor": true,
        "parking": true
    },
    "precio": 250000,
    "disponible": true,
    "fecha_publicacion": datetime()
}

Implementa búsqueda con filtros:
1. Por rango de precio
2. Mínimo de habitaciones y baños
3. Características específicas (ascensor, parking)
4. Por proximidad (coordenadas geoespaciales)
5. Ordenar por precio, fecha, metros cuadrados
"""
```

## **Ejercicio 5: Optimización**

```python
"""
Tienes una colección 'logs' con millones de registros:
{
    "timestamp": datetime(),
    "nivel": "INFO",
    "mensaje": "...",
    "usuario_id": ObjectId(),
    "servicio": "api",
    "duracion_ms": 125
}

Queries frecuentes:
- Logs de un usuario en un rango de fechas
- Logs de nivel ERROR
- Logs de un servicio específico
- Promedio de duracion_ms por servicio
- Logs de últimas 24 horas

Tareas:
1. Crear índices apropiados
2. Implementar auto-eliminación con TTL (logs > 30 días)
3. Usar aggregation para reportes diarios
4. Optimizar query que tarda > 5 segundos
5. Implementar paginación eficiente
"""
```



# **14. Cheat Sheet SQL → MongoDB**

```python
# ===============================
# CREAR / INSERTAR
# ===============================

# SQL
"""
CREATE TABLE estudiantes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    edad INT
);

INSERT INTO estudiantes (nombre, edad) VALUES ('Juan', 25);
"""

# MongoDB
db.create_collection("estudiantes")  # Opcional, se crea automáticamente
db.estudiantes.insert_one({"nombre": "Juan", "edad": 25})

# ===============================
# CONSULTAR
# ===============================

# SQL: SELECT * FROM estudiantes
db.estudiantes.find({})

# SQL: SELECT nombre, edad FROM estudiantes
db.estudiantes.find({}, {"nombre": 1, "edad": 1, "_id": 0})

# SQL: SELECT * FROM estudiantes WHERE edad > 20
db.estudiantes.find({"edad": {"$gt": 20}})

# SQL: SELECT * FROM estudiantes WHERE edad BETWEEN 20 AND 30
db.estudiantes.find({"edad": {"$gte": 20, "$lte": 30}})

# SQL: SELECT * FROM estudiantes WHERE nombre LIKE 'Mar%'
db.estudiantes.find({"nombre": {"$regex": "^Mar"}})

# SQL: SELECT * FROM estudiantes WHERE ciudad IN ('Madrid', 'Barcelona')
db.estudiantes.find({"ciudad": {"$in": ["Madrid", "Barcelona"]}})

# SQL: SELECT * FROM estudiantes WHERE edad > 20 AND activo = true
db.estudiantes.find({"edad": {"$gt": 20}, "activo": True})

# SQL: SELECT * FROM estudiantes WHERE edad < 18 OR edad > 65
db.estudiantes.find({"$or": [{"edad": {"$lt": 18}}, {"edad": {"$gt": 65}}]})

# ===============================
# ORDENAR Y LIMITAR
# ===============================

# SQL: SELECT * FROM estudiantes ORDER BY edad DESC
db.estudiantes.find().sort("edad", -1)

# SQL: SELECT * FROM estudiantes ORDER BY edad DESC LIMIT 10
db.estudiantes.find().sort("edad", -1).limit(10)

# SQL: SELECT * FROM estudiantes LIMIT 10 OFFSET 20
db.estudiantes.find().skip(20).limit(10)

# ===============================
# ACTUALIZAR
# ===============================

# SQL: UPDATE estudiantes SET edad = 26 WHERE id = 1
db.estudiantes.update_one({"_id": 1}, {"$set": {"edad": 26}})

# SQL: UPDATE estudiantes SET activo = false WHERE edad < 18
db.estudiantes.update_many({"edad": {"$lt": 18}}, {"$set": {"activo": False}})

# SQL: UPDATE estudiantes SET login_count = login_count + 1 WHERE id = 1
db.estudiantes.update_one({"_id": 1}, {"$inc": {"login_count": 1}})

# ===============================
# ELIMINAR
# ===============================

# SQL: DELETE FROM estudiantes WHERE id = 1
db.estudiantes.delete_one({"_id": 1})

# SQL: DELETE FROM estudiantes WHERE activo = false
db.estudiantes.delete_many({"activo": False})

# SQL: DELETE FROM estudiantes
db.estudiantes.delete_many({})

# SQL: DROP TABLE estudiantes
db.estudiantes.drop()

# ===============================
# AGREGACIONES
# ===============================

# SQL: SELECT COUNT(*) FROM estudiantes
db.estudiantes.count_documents({})

# SQL: SELECT ciudad, COUNT(*) FROM estudiantes GROUP BY ciudad
db.estudiantes.aggregate([
    {"$group": {"_id": "$ciudad", "total": {"$sum": 1}}}
])

# SQL: SELECT ciudad, AVG(edad) FROM estudiantes GROUP BY ciudad
db.estudiantes.aggregate([
    {"$group": {"_id": "$ciudad", "edad_promedio": {"$avg": "$edad"}}}
])

# SQL: SELECT ciudad, COUNT(*) FROM estudiantes GROUP BY ciudad HAVING COUNT(*) > 10
db.estudiantes.aggregate([
    {"$group": {"_id": "$ciudad", "total": {"$sum": 1}}},
    {"$match": {"total": {"$gt": 10}}}
])

# SQL: SELECT DISTINCT ciudad FROM estudiantes
db.estudiantes.distinct("ciudad")

# ===============================
# JOINS
# ===============================

# SQL: SELECT e.nombre, c.nombre FROM estudiantes e LEFT JOIN cursos c ON e.curso_id = c.id
db.estudiantes.aggregate([
    {"$lookup": {
        "from": "cursos",
        "localField": "curso_id",
        "foreignField": "_id",
        "as": "curso"
    }},
    {"$unwind": "$curso"},
    {"$project": {
        "nombre_estudiante": "$nombre",
        "nombre_curso": "$curso.nombre"
    }}
])

# ===============================
# ÍNDICES
# ===============================

# SQL: CREATE INDEX idx_email ON estudiantes(email)
db.estudiantes.create_index("email")

# SQL: CREATE UNIQUE INDEX idx_email ON estudiantes(email)
db.estudiantes.create_index("email", unique=True)

# SQL: CREATE INDEX idx_ciudad_edad ON estudiantes(ciudad, edad)
db.estudiantes.create_index([("ciudad", 1), ("edad", -1)])

# SQL: DROP INDEX idx_email ON estudiantes
db.estudiantes.drop_index("idx_email")

# SQL: SHOW INDEXES FROM estudiantes
list(db.estudiantes.list_indexes())
```



# **Anexos**

## **Recursos adicionales**

### **Documentación oficial**
- MongoDB Manual: https://www.mongodb.com/docs/manual/
- PyMongo Documentation: https://pymongo.readthedocs.io/
- MongoDB University (cursos gratuitos): https://university.mongodb.com/

### **Herramientas**
- **MongoDB Compass**: Interfaz gráfica oficial
- **mongosh**: Shell interactivo
- **Studio 3T**: IDE profesional (pago)
- **NoSQLBooster**: Cliente GUI alternativo
- **MongoDB Atlas**: Base de datos en la nube

### **Librerías Python útiles**
```bash
pip install pymongo          # Driver oficial
pip install motor            # Driver asíncrono
pip install mongoengine      # ODM (Object-Document Mapper)
pip install mongomock        # Mock para testing
pip install pymongo-schema   # Analizar esquemas
```

### **Ejemplo de configuración con Docker**
```yaml
# docker-compose.yml
version: '3.8'
services:
  mongodb:
    image: mongo:8
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```



## **Solución Ejercicio 1: Biblioteca**

```python
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId

# Conexión
client = MongoClient('mongodb://localhost:27017/')
db = client['biblioteca']
libros = db['libros']
prestamos = db['prestamos']

# Crear índices
libros.create_index("isbn", unique=True)
prestamos.create_index([("libro_id", 1), ("fecha_prestamo", -1)])

# 1. Insertar libros
def insertar_libro(titulo, autor, isbn, año, genero):
    try:
        libro = {
            "titulo": titulo,
            "autor": autor,
            "isbn": isbn,
            "año": año,
            "genero": genero,
            "disponible": True
        }
        resultado = libros.insert_one(libro)
        return {"success": True, "id": resultado.inserted_id}
    except DuplicateKeyError:
        return {"error": "ISBN ya existe"}

# 2. Buscar libros por género
def buscar_por_genero(genero):
    return list(libros.find({"genero": genero, "disponible": True}))

# 3. Registrar préstamo
def registrar_prestamo(isbn, usuario):
    libro = libros.find_one({"isbn": isbn, "disponible": True})
    
    if not libro:
        return {"error": "Libro no disponible"}
    
    # Actualizar libro
    libros.update_one(
        {"_id": libro['_id']},
        {"$set": {"disponible": False}}
    )
    
    # Crear préstamo
    prestamo = {
        "libro_id": libro['_id'],
        "usuario": usuario,
        "fecha_prestamo": datetime.now(),
        "fecha_devolucion": None
    }
    prestamos.insert_one(prestamo)
    
    return {"success": True, "fecha_limite": datetime.now() + timedelta(days=14)}

# 4. Registrar devolución
def registrar_devolucion(isbn):
    libro = libros.find_one({"isbn": isbn})
    
    if not libro:
        return {"error": "Libro no encontrado"}
    
    # Actualizar préstamo
    prestamos.update_one(
        {"libro_id": libro['_id'], "fecha_devolucion": None},
        {"$set": {"fecha_devolucion": datetime.now()}}
    )
    
    # Marcar libro como disponible
    libros.update_one(
        {"_id": libro['_id']},
        {"$set": {"disponible": True}}
    )
    
    return {"success": True}

# 5. Listar libros prestados actualmente
def libros_prestados():
    pipeline = [
        {"$match": {"fecha_devolucion": None}},
        {"$lookup": {
            "from": "libros",
            "localField": "libro_id",
            "foreignField": "_id",
            "as": "libro"
        }},
        {"$unwind": "$libro"},
        {"$project": {
            "titulo": "$libro.titulo",
            "usuario": 1,
            "fecha_prestamo": 1,
            "dias_prestado": {
                "$divide": [
                    {"$subtract": [datetime.now(), "$fecha_prestamo"]},
                    1000 * 60 * 60 * 24
                ]
            }
        }}
    ]
    
    return list(prestamos.aggregate(pipeline))

# 6. Usuario con más préstamos
def usuario_mas_activo():
    pipeline = [
        {"$group": {
            "_id": "$usuario",
            "total_prestamos": {"$sum": 1}
        }},
        {"$sort": {"total_prestamos": -1}},
        {"$limit": 1}
    ]
    
    resultado = list(prestamos.aggregate(pipeline))
    return resultado[0] if resultado else None

# Uso
print(insertar_libro("1984", "George Orwell", "978-0451524935", 1949, "Ficción"))
print(insertar_libro("Python Crash Course", "Eric Matthes", "978-1593279288", 2019, "Programación"))

print(buscar_por_genero("Ficción"))
print(registrar_prestamo("978-0451524935", "María García"))
print(libros_prestados())
print(registrar_devolucion("978-0451524935"))
print(usuario_mas_activo())
```
