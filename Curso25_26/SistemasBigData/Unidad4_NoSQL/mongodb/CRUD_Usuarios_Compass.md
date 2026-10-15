# CRUD de Usuarios con MongoDB Compass — Guía completa

## Índice

1. Introducción
2. Preparar el entorno en Compass
3. Crear base de datos y colección (GUI)
4. Insertar documentos (Create)
   - Inserción manual (GUI)
   - Inserción por lote (Import)
   - Con ejemplos de tipos de datos
5. Consultas (Read / SELECT)
   - Búsqueda simple
   - Proyección
   - Filtros avanzados (comparadores, lógicos, regex, arrays, campos anidados)
   - Ordenar, limitar y paginación
   - Distinct y count
   - Explain plan
6. Actualizar documentos (Update)
   - Editar en la UI
   - updateOne / updateMany / replaceOne / upsert
   - Operadores: $set, $inc, $push, $pull, $addToSet
7. Borrar documentos (Delete)
   - Borrar en la UI
   - deleteOne / deleteMany
8. Agregaciones (Aggregation Pipeline)
   - Uso del Builder en Compass
   - Ejemplos prácticos
9. Índices y rendimiento
   - Crear índices (incluido único)
   - Índices compuestos
   - Consultas con cobertura
10. Validación de esquema (Schema Validation)
11. Importar / Exportar datos
12. Ejercicios y prácticas para clase
13. Resumen rápido (cheat sheet)
14. Referencias



## 1) Introducción

Esta guía está pensada para usar **MongoDB Compass** (la interfaz gráfica de MongoDB). Los alumnos trabajarán directamente en Compass: crearán la base de datos y la colección, verán cómo insertar y editar documentos con la interfaz, y practicarán consultas de distinto nivel.

> Nota: Para tareas avanzadas (backups, scripting) puedes usar la consola `mongosh`, pero aquí nos centramos en Compass.



## 2) Preparar el entorno en Compass

1. Abre MongoDB Compass y conéctate a tu servidor (URI o localhost). Si usas Docker Compose, asegúrate de que el contenedor de MongoDB esté en ejecución.
2. Verifica que tengas permisos para crear bases de datos y colecciones.



## 3) Crear base de datos y colección (GUI)

1. En Compass, haz clic en "Create Database" (o en español "Crear base de datos").
2. Nombre de la base: `curso_mongodb` (ejemplo).
3. Nombre de la colección: `usuarios`.
4. Puedes crear también opciones de validación desde aquí (lo vemos en la sección 10).



## 4) Insertar documentos (Create)

### a) Inserción manual (GUI)

- Ve a `curso_mongodb` → `usuarios` → pestaña `Documents`.
- Haz clic en **Insert Document** (o "Add Data" → "Insert Document").
- Se abre un editor JSON. Pega un documento y guarda.

Ejemplo (copiar/pegar en el diálogo de Insert):

```json
{
  "name": "María Pérez",
  "email": "maria.perez@example.com",
  "age": 28,
  "country": "Argentina",
  "active": true,
  "hobbies": ["lectura", "tenis"],
  "address": { "city": "Buenos Aires", "zip": "C1001" },
  "createdAt": { "$date": "2024-09-01T10:00:00Z" }
}
```

**Tipos de datos**: Puedes insertar strings, números, boolean, fechas (`$date`), arrays, objetos anidados. Compass interpreta la Extended JSON.

### b) Inserción por lote (Import)

- Botón `ADD DATA` → `Import File`.
- Selecciona JSON o CSV con tus registros y especifica opciones de importación (campo para _id, delimitador CSV, etc.).

Ejemplo: crea un archivo `usuarios_sample.json` con 10 documentos (más abajo hay una muestra completa) y súbelo.

### c) Dataset de ejemplo (10 usuarios)

Pega estos documentos como insert por lote o inserta algunos manualmente para practicar:

```json
[
  { "name": "Juan López", "email": "juan.lopez@example.com", "age": 34, "country": "Chile", "active": true, "hobbies": ["futbol", "cocina"], "loginCount": 5 },
  { "name": "Ana Gómez", "email": "ana.gomez@example.com", "age": 22, "country": "Perú", "active": false, "hobbies": ["ajedrez"] },
  { "name": "Carlos Ruiz", "email": "carlos.ruiz@example.com", "age": 45, "country": "España", "active": true, "hobbies": ["senderismo", "fotografia"], "loginCount": 12 },
  { "name": "Lucía Fernández", "email": "lucia@example.com", "age": 30, "country": "México", "active": true, "hobbies": ["cine"] },
  { "name": "Pedro Martínez", "email": "pedro@example.com", "age": 17, "country": "Argentina", "active": false, "hobbies": ["videojuegos"], "minor": true },
  { "name": "Sofía Torres", "email": "sofia.t@example.com", "age": 27, "country": "Chile", "active": true, "hobbies": ["lectura", "yoga"], "loginCount": 3 },
  { "name": "Diego Vega", "email": "diego@example.com", "age": 40, "country": "Perú", "active": true, "hobbies": ["ciclismo"] },
  { "name": "Mariana Rojas", "email": "mariana@example.com", "age": 19, "country": "Colombia", "active": false, "hobbies": [] },
  { "name": "Carlos Perez", "email": "c.perez@example.com", "age": 29, "country": "España", "active": true, "hobbies": ["tenis", "viajes"] },
  { "name": "Valentina Ruiz", "email": "valentina@example.com", "age": 35, "country": "Argentina", "active": true, "hobbies": ["cocina", "pintura"] }
]
```



## 5) Consultas (Read / SELECT)

En Compass hay una barra de filtro JSON encima de los documentos. También puedes usar campos para `Project`, `Sort`, `Limit`, `Skip` y opciones de `Explain`.

> Consejo: pega las consultas JSON en la barra Filter y usa Project para la proyección.

### Ejemplos básicos

- Todos los usuarios:

Filter: `{}`

- Usuarios activos:

Filter: `{ "active": true }`

- Usuarios mayores de 30 años:

Filter: `{ "age": { "$gt": 30 } }`

- Usuarios con email que contiene "example.com" (regex):

Filter: `{ "email": { "$regex": "example.com$" } }`

- Usuarios cuyo nombre empieza por 'C' (case-insensitive):

Filter: `{ "name": { "$regex": "^C", "$options": "i" } }`

### Proyección (mostrar solo campos)

En `Project` pega por ejemplo:

```json
{ "name": 1, "email": 1, "_id": 0 }
```

Esto muestra sólo `name` y `email` y oculta `_id`.

### Ordenar, limitar y paginar

Options → Sort:

```json
{ "age": -1 }
```

Limit: `5` (muestra 5 resultados)

Skip: `5` (para paginar)

### Búsquedas avanzadas

- Usuarios en Chile o Perú:

Filter: `{ "country": { "$in": ["Chile", "Perú"] } }`

- Usuarios que tienen hobbies (array no vacío):

Filter: `{ "hobbies": { "$exists": true, "$ne": [] } }`

- Buscar por campo anidado (ciudad):

Filter: `{ "address.city": "Buenos Aires" }`

- Contar resultados con la UI: usa el botón `Count Documents` o mira el número en la cabecera (según versión de Compass).

### Distinct (valores únicos)

Usa la pestaña `Aggregations` o ejecuta en el `Playground`: `db.usuarios.distinct("country")`.

### Explain Plan

1. Escribe tu Filter.
2. Haz clic en `Explain Plan` (o en la versión en inglés `Explain`) para ver si la consulta usa índices y cuánto tiempo tomó.



## 6) Actualizar documentos (Update)

### Editar en la UI

- En `Documents`, abre el documento y haz clic en `Edit Document` (o `Modify`). Cambia el campo y guarda.

### Update con Playground (scripting en Compass)

Abre `Playground` (o usa la pestaña `Aggregations` para pipelines). Ejemplos:

- Incrementar el loginCount de un usuario:

```js
// Playground
db.usuarios.updateOne(
  { "email": "juan.lopez@example.com" },
  { "$inc": { "loginCount": 1 } }
)
```

- Marcar a todos los menores de edad con `minor:true`:

```js
db.usuarios.updateMany(
  { "age": { "$lt": 18 } },
  { "$set": { "minor": true } }
)
```

- Agregar un hobby si no existe ($addToSet):

```js
db.usuarios.updateOne(
  { "email": "sofia.t@example.com" },
  { "$addToSet": { "hobbies": "meditacion" } }
)
```

- Reemplazar por completo un documento:

```js
db.usuarios.replaceOne(
  { "email": "mariana@example.com" },
  { "name": "Mariana Rojas", "email": "mariana@example.com", "age": 20 }
)
```

- Upsert (insertar si no existe):

```js
db.usuarios.updateOne(
  { "email": "nuevo@example.com" },
  { "$set": { "name": "Nuevo Usuario", "active": true } },
  { "upsert": true }
)
```

**Tip:** Siempre prueba el filtro primero con `find()` antes de ejecutar un `updateMany` para evitar cambios no deseados.



## 7) Borrar documentos (Delete)

### Borrar en la UI

- En la lista de documentos, selecciona el documento y usa el botón `Delete Document`.

### Borrar con Playground

- Borrar uno:

```js
db.usuarios.deleteOne({ "email": "pedro@example.com" })
```

- Borrar muchos:

```js
db.usuarios.deleteMany({ "active": false })
```

> Precaución: `deleteMany` es irreversible en la UI — revisa el filtro antes de ejecutar.



## 8) Agregaciones (Aggregation Pipeline)

En Compass abre la pestaña `Aggregations`. Ahí puedes construir pipelines visualmente o pegar un array de etapas.

### Ejemplo 1: Contar usuarios por país (sólo activos)

Pipeline:

```json
[
  { "$match": { "active": true } },
  { "$group": { "_id": "$country", "total": { "$sum": 1 } } },
  { "$sort": { "total": -1 } }
]
```

### Ejemplo 2: Edad promedio por país

```json
[
  { "$group": { "_id": "$country", "avgAge": { "$avg": "$age" }, "count": { "$sum": 1 } } },
  { "$sort": { "avgAge": -1 } }
]
```

### Ejemplo 3: Contar dominios de email (extraer dominio)

```json
[
  { "$project": { "domain": { "$arrayElemAt": [ { "$split": ["$email", "@"] }, 1 ] } } },
  { "$group": { "_id": "$domain", "count": { "$sum": 1 } } },
  { "$sort": { "count": -1 } }
]
```

### Ejemplo 4: Unwind arrays

Si quieres contar hobbies más populares:

```json
[
  { "$unwind": "$hobbies" },
  { "$group": { "_id": "$hobbies", "count": { "$sum": 1 } } },
  { "$sort": { "count": -1 } }
]
```



## 9) Índices y rendimiento

### Crear un índice (UI)

- Ve a la pestaña `Indexes` → `Create Index`.
- Ejemplo: índice único en `email`:

Key: `{ "email": 1 }` → Opciones: `Unique: true`.

### Índice compuesto

Key: `{ "country": 1, "age": -1 }` — útil para consultas que filtran por país y ordenan por edad.

### Queries cubiertas

Si tu proyección sólo incluye campos cubiertos por el índice, MongoDB puede responder desde el índice sin leer documentos completos. Utiliza `Explain Plan` para comprobarlo.



## 10) Validación de esquema (Schema Validation)

Puedes agregar reglas de validación cuando creas la colección o modificando las opciones de la colección.

Ejemplo de validación básica (JSON Schema):

```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["name", "email"],
    "properties": {
      "name": { "bsonType": "string" },
      "email": { "bsonType": "string", "pattern": "^\\S+@\\S+\\.\\S+$" },
      "age": { "bsonType": "int", "minimum": 0 }
    }
  }
}
```

Si insertas o actualizas un documento que no cumple la validación, MongoDB rechaza la operación.



## 11) Importar / Exportar datos

- `ADD DATA` → `Import File` para importar JSON/CSV.
- En la cabecera de la colección, hay opción `Export Collection` para exportar a JSON o CSV.

Esto es útil para compartir ejercicios o respaldar una muestra.



## 12) Ejercicios y prácticas para clase

1. Crea la colección `usuarios` y carga el dataset de ejemplo.
2. Encuentra todos los usuarios activos en Chile y ordénalos por edad descendente.
3. Cuenta cuántos usuarios hay por país usando Aggregations.
4. Crea un índice único en `email` y prueba a insertar un usuario con email duplicado — observa el error.
5. Implementa una validación que requiera `name` y `email` y prueba a insertar un registro inválido.
6. Añade `"loginCount": 0` a todos los usuarios que no lo tengan (updateMany con $set y $exists).
7. Encuentra los 3 hobbies más frecuente con $unwind y $group.



## 13) Resumen rápido (cheat sheet)

- Búsqueda básica: `{ "field": value }`
- Comparadores: `{ "age": { "$gt": 30 } }`
- Lógicos: `{ "$or": [ {..}, {..} ] }`
- Array contains: `{ "hobbies": "futbol" }`
- Proyección: `{ "name": 1, "email": 1 }`
- Sort: `{ "age": -1 }` (1 asc, -1 desc)
- Update increment: `{ "$inc": { "loginCount": 1 } }`
- Add to array (no duplicados): `{ "$addToSet": { "hobbies": "nuevo" } }`



## 14) Referencias

- MongoDB Manual — Query Documents: https://www.mongodb.com/docs/manual/crud/
- Aggregation Pipeline: https://www.mongodb.com/docs/manual/aggregation/
- Compass User Guide: https://www.mongodb.com/docs/compass/current/



> Si quieres, puedo añadir:
> - Capturas de pantalla paso a paso de Compass (útil para clases presenciales),
> - Un archivo JSON listo para importar (dataset ampliado),
> - Un PDF formato presentación con los ejercicios y sus soluciones.



**Fin** — Documento preparado para usar en clase con MongoDB Compass. Si quieres que agregue capturas, ejercicios resueltos, o una versión corta para una diapositiva, dime cuál prefieres.
