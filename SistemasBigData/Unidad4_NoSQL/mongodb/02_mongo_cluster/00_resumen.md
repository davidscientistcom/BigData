# **MONGODB: FUNDAMENTOS Y CONCEPTOS (Prerequisitos)**

***

## **0. ¿Qué es MongoDB y por qué existe?**

### **0.1. El problema con las bases de datos tradicionales**

Durante décadas, las bases de datos relacionales (SQL) han sido la norma. Sistemas como MySQL, PostgreSQL u Oracle utilizan tablas con filas y columnas, relaciones definidas mediante claves foráneas, y un lenguaje estructurado (SQL) para consultar datos. Este modelo funciona perfectamente cuando los datos son estructurados y predecibles: una tabla de clientes con campos fijos (nombre, apellido, email, teléfono), otra de pedidos, otra de productos, y relaciones bien definidas entre ellas.

Sin embargo, a mediados de los años 2000, empresas como Google, Amazon y Facebook empezaron a enfrentarse a problemas que las bases de datos relacionales no podían resolver eficientemente. Imaginemos una red social: cada usuario tiene datos diferentes (algunos tienen fotos, otros no; algunos tienen múltiples empleos, otros ninguno; algunos tienen listas de intereses de cientos de elementos). Intentar meter todo esto en tablas rígidas con esquemas fijos se vuelve un infierno de tablas relacionadas con JOINs complejos que ralentizan todo.

Además, estas empresas necesitaban escalar horizontalmente: añadir más servidores para repartir la carga. Las bases de datos relacionales están diseñadas para escalar verticalmente (comprar un servidor más potente), pero eventualmente llegas al límite de lo que una sola máquina puede hacer. Necesitaban distribuir los datos entre cientos o miles de servidores trabajando en paralelo.

De ahí nació el movimiento **NoSQL** (Not Only SQL): bases de datos diseñadas para flexibilidad de esquema, escalado horizontal masivo y rendimiento en escenarios específicos.

### **0.2. MongoDB: documentos en lugar de filas**

MongoDB pertenece a la familia de bases de datos **orientadas a documentos**. En lugar de almacenar datos en tablas con filas y columnas, MongoDB guarda **documentos JSON** (técnicamente BSON, pero pensemos en JSON por ahora).

**Ejemplo comparativo:**

**Base de datos relacional (SQL):**

```
Tabla: clientes
+----+----------+-----------+-------------------+
| id | nombre   | apellido  | email             |
+----+----------+-----------+-------------------+
| 1  | Juan     | García    | juan@ejemplo.com  |
| 2  | María    | López     | maria@ejemplo.com |
+----+----------+-----------+-------------------+

Tabla: direcciones (relación 1:N)
+----+------------+----------+--------+------------+
| id | cliente_id | ciudad   | cp     | pais       |
+----+------------+----------+--------+------------+
| 1  | 1          | Madrid   | 28001  | España     |
| 2  | 1          | Valencia | 46001  | España     |
| 3  | 2          | Barcelona| 08001  | España     |
+----+------------+----------+--------+------------+

-- Para obtener un cliente con todas sus direcciones:
SELECT c.*, d.*
FROM clientes c
LEFT JOIN direcciones d ON c.id = d.cliente_id
WHERE c.id = 1;
```

**MongoDB (documentos):**

```javascript
// Colección: clientes
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "nombre": "Juan",
  "apellido": "García",
  "email": "juan@ejemplo.com",
  "direcciones": [
    {
      "ciudad": "Madrid",
      "cp": "28001",
      "pais": "España"
    },
    {
      "ciudad": "Valencia",
      "cp": "46001",
      "pais": "España"
    }
  ]
}

{
  "_id": ObjectId("507f191e810c19729de860ea"),
  "nombre": "María",
  "apellido": "López",
  "email": "maria@ejemplo.com",
  "direcciones": [
    {
      "ciudad": "Barcelona",
      "cp": "08001",
      "pais": "España"
    }
  ]
}

// Para obtener un cliente con todas sus direcciones:
db.clientes.findOne({ nombre: "Juan" })
// ¡Una sola operación, sin JOINs!
```

**¿Ves la diferencia?** En MongoDB, toda la información relacionada está **anidada dentro del mismo documento**. No necesitamos hacer JOINs complejos ni consultar múltiples tablas. Un documento MongoDB es una unidad autocontenida de información.

### **0.3. ¿Cuándo usar MongoDB y cuándo NO usarlo?**

**MongoDB brilla cuando:**

1. **Los datos tienen estructura variable**: No todos los documentos de una colección necesitan tener los mismos campos. Algunos clientes tienen 2 direcciones, otros 10, otros ninguna.

2. **Necesitamos escalar horizontalmente**: Distribuyendo datos entre múltiples servidores (sharding).

3. **Desarrollo ágil**: Podemos cambiar el esquema sobre la marcha sin migraciones complejas de base de datos.

4. **Datos jerárquicos o anidados**: Estructuras JSON naturales como catálogos de productos, perfiles de usuario, logs de aplicaciones.

5. **Alto volumen de lecturas/escrituras**: MongoDB está optimizado para throughput alto.

**MongoDB NO es ideal cuando:**

1. **Necesitamos transacciones complejas multi-documento**: Aunque MongoDB soporta transacciones desde la versión 4.0, no son tan robustas como en bases de datos relacionales.

2. **Relaciones complejas entre muchas entidades**: Si tu modelo de datos es principalmente relacional (muchos-a-muchos, integridad referencial estricta), SQL es mejor opción.

3. **Necesitamos cumplimiento estricto de esquema**: Si el esquema NUNCA cambia y necesitamos validaciones a nivel de base de datos muy estrictas.

4. **Análisis complejos con JOINs**: Aunque MongoDB tiene agregaciones potentes, consultas con múltiples joins siguen siendo más eficientes en SQL.

***

## **1. Conceptos fundamentales de MongoDB**

### **1.1. Documentos y BSON**

Un **documento** en MongoDB es equivalente a una "fila" en SQL, pero mucho más flexible. Los documentos se almacenan en formato **BSON** (Binary JSON), que extiende JSON con tipos de datos adicionales como fechas, ObjectId, binarios, etc.

**Anatomía de un documento:**

```javascript
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),  // ID único automático
  "nombre": "Producto Premium",                  // String
  "precio": 99.99,                               // Number (double)
  "stock": 150,                                  // Number (integer)
  "activo": true,                                // Boolean
  "categorias": ["electrónica", "ofertas"],     // Array
  "fabricante": {                                // Documento embebido
    "nombre": "TechCorp",
    "pais": "España"
  },
  "fecha_alta": ISODate("2026-01-15T10:30:00Z"), // Fecha
  "especificaciones": null,                      // Null
  "imagen": BinData(0, "..."),                   // Datos binarios
  "metadata": {}                                 // Objeto vacío
}
```

**Tipos de datos BSON importantes:**

- **ObjectId**: Identificador único de 12 bytes generado automáticamente. Incluye timestamp, identificador de máquina, ID de proceso y contador. Garantiza unicidad global.
  
- **String**: Texto UTF-8. Puede contener cualquier carácter Unicode.

- **Number**: MongoDB diferencia entre enteros (32 y 64 bits) y decimales (double). Por defecto en el shell, los números son double.

- **Date**: Timestamps en milisegundos desde Unix epoch (1/1/1970).

- **Array**: Listas ordenadas que pueden contener cualquier tipo de dato, incluso otros arrays u objetos.

- **Embedded Document**: Documentos anidados. Un documento puede contener otros documentos sin límite de profundidad (aunque se recomienda no exceder 2-3 niveles).

### **1.2. Colecciones**

Una **colección** es equivalente a una "tabla" en SQL. Es un grupo de documentos relacionados, pero a diferencia de las tablas SQL, **los documentos de una colección NO tienen que tener la misma estructura**.

```javascript
// Colección: productos
// Documento 1: producto físico
{
  "_id": 1,
  "nombre": "Ordenador portátil",
  "peso": 1.8,
  "dimensiones": { "alto": 2, "ancho": 35, "fondo": 25 }
}

// Documento 2: producto digital (diferentes campos)
{
  "_id": 2,
  "nombre": "Curso online de MongoDB",
  "duracion_horas": 20,
  "url_acceso": "https://..."
}

// Documento 3: servicio (campos completamente diferentes)
{
  "_id": 3,
  "nombre": "Consultoría",
  "tarifa_hora": 120,
  "disponibilidad": ["lunes", "miércoles", "viernes"]
}
```

Todos estos documentos conviven en la misma colección `productos` porque **conceptualmente representan productos**, aunque sus atributos específicos varían. Esta flexibilidad es poderosa pero requiere disciplina: si abusamos de ella, las consultas se complican.

### **1.3. Bases de datos**

Una **base de datos** en MongoDB es un contenedor de colecciones. Es equivalente a una base de datos en SQL (schema/database). Un servidor MongoDB puede alojar múltiples bases de datos independientes.

```
Servidor MongoDB
├── Base de datos: "ecommerce"
│   ├── Colección: "clientes"
│   ├── Colección: "productos"
│   └── Colección: "pedidos"
├── Base de datos: "analytics"
│   ├── Colección: "eventos"
│   └── Colección: "metricas"
└── Base de datos: "admin" (base de datos del sistema)
```

***

## **2. Modelo de datos en MongoDB**

### **2.1. Modelado por embebido vs. por referencia**

Esta es la decisión de diseño más importante en MongoDB. Cuando tienes relaciones entre entidades, puedes modelarlas de dos formas:

**Embebido (embedded)**: Los datos relacionados se almacenan dentro del documento principal.

**Por referencia (referenced)**: Los datos relacionados se almacenan en documentos separados, referenciados por su ID.

**Ejemplo: Blog con posts y comentarios**

**Opción 1: Embebido**

```javascript
// Colección: posts
{
  "_id": ObjectId("..."),
  "titulo": "Introducción a MongoDB",
  "contenido": "MongoDB es una base de datos...",
  "autor": "Juan García",
  "fecha": ISODate("2026-02-01"),
  "comentarios": [
    {
      "usuario": "María",
      "texto": "Excelente artículo!",
      "fecha": ISODate("2026-02-02")
    },
    {
      "usuario": "Pedro",
      "texto": "Muy útil, gracias",
      "fecha": ISODate("2026-02-03")
    }
  ]
}
```

**Ventajas del embebido:**
- Una sola consulta obtiene el post con todos sus comentarios
- Atomicidad: actualizar el post y sus comentarios es una operación atómica
- Rendimiento: menos operaciones de red

**Desventajas del embebido:**
- Documentos muy grandes (límite de 16MB por documento)
- Si los comentarios crecen ilimitadamente, el documento se vuelve inmanejable
- Difícil consultar "todos los comentarios de un usuario" si están embebidos en posts diferentes

**Opción 2: Por referencia**

```javascript
// Colección: posts
{
  "_id": ObjectId("abc123"),
  "titulo": "Introducción a MongoDB",
  "contenido": "MongoDB es una base de datos...",
  "autor": "Juan García",
  "fecha": ISODate("2026-02-01")
}

// Colección: comentarios
{
  "_id": ObjectId("def456"),
  "post_id": ObjectId("abc123"),  // Referencia al post
  "usuario": "María",
  "texto": "Excelente artículo!",
  "fecha": ISODate("2026-02-02")
}
{
  "_id": ObjectId("ghi789"),
  "post_id": ObjectId("abc123"),
  "usuario": "Pedro",
  "texto": "Muy útil, gracias",
  "fecha": ISODate("2026-02-03")
}
```

**Ventajas de las referencias:**
- Documentos más pequeños
- Escalabilidad: sin límite en el número de comentarios
- Flexibilidad: fácil consultar "todos los comentarios de Pedro" en todos los posts

**Desventajas de las referencias:**
- Dos consultas para obtener post + comentarios (o usar $lookup, que es costoso)
- Sin atomicidad: actualizar post y comentarios requiere múltiples operaciones
- Más complejidad en el código de aplicación

**Regla de oro para decidir:**

- **Usa embebido cuando**: Los datos embebidos son parte intrínseca del documento padre, se consultan juntos siempre, y no crecen sin límite (relaciones 1:pocos).

- **Usa referencias cuando**: Los datos referenciados tienen vida independiente, se consultan por separado, o pueden crecer ilimitadamente (relaciones 1:muchos o muchos:muchos).

### **2.2. Desnormalización controlada**

En bases de datos relacionales, la normalización es sagrada: cada dato se almacena en un solo lugar para evitar redundancia. En MongoDB, **la desnormalización es común y recomendada** cuando mejora el rendimiento.

**Ejemplo: e-commerce**

```javascript
// Colección: pedidos
{
  "_id": ObjectId("..."),
  "numero_pedido": "PED-2026-001",
  "cliente_id": ObjectId("cliente123"),
  "cliente_nombre": "Juan García",  // ← DESNORMALIZADO
  "cliente_email": "juan@ejemplo.com",  // ← DESNORMALIZADO
  "productos": [
    {
      "producto_id": ObjectId("prod456"),
      "nombre": "Portátil Dell",  // ← DESNORMALIZADO
      "precio": 899,  // ← DESNORMALIZADO (precio al momento de compra)
      "cantidad": 1
    }
  ],
  "total": 899,
  "fecha": ISODate("2026-02-09"),
  "estado": "enviado"
}
```

¿Por qué desnormalizamos nombre y email del cliente, y nombre/precio del producto?

- **Para el cliente**: Cuando consultamos un pedido, casi siempre queremos saber quién lo hizo sin tener que buscar en la colección de clientes.

- **Para el precio**: Guardamos el precio al momento de la compra, no el precio actual del producto. Si el producto cambia de precio mañana, los pedidos históricos no deben reflejarlo.

**La desnormalización tiene un coste**: Si Juan García cambia su nombre a "Juan Pérez García", los pedidos antiguos seguirán mostrando "Juan García". Esto es aceptable en muchos casos (un pedido es un documento histórico), pero debemos ser conscientes de ello.

***

## **3. Arquitectura conceptual de MongoDB**

### **3.1. El servidor standalone (modo básico)**

La forma más simple de MongoDB es un único servidor (`mongod`) que almacena todos los datos. Es suficiente para desarrollo y aplicaciones pequeñas, pero tiene problemas obvios:

- **Punto único de fallo**: Si el servidor se cae, la aplicación deja de funcionar.
- **Límite de escalado**: Un solo servidor tiene límites de RAM, CPU, disco y I/O.
- **Sin redundancia**: Si se corrompen los datos o el disco falla, perdemos todo.

Para producción, necesitamos algo más robusto.

### **3.2. Replica Sets: copias sincronizadas**

Un **Replica Set** es un grupo de servidores MongoDB que mantienen copias idénticas de los datos. Piensa en él como un sistema de "espejos sincronizados".

**Conceptualmente:**

```
        ┌─────────────────┐
        │   APLICACIÓN    │
        └────────┬────────┘
                 │
                 ▼
         (escribe aquí)
        ┌─────────────┐
        │   PRIMARY   │ ← Único nodo que acepta escrituras
        └──────┬──────┘
               │
               │ (replica automáticamente)
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
┌───────────┐     ┌───────────┐
│SECONDARY 1│     │SECONDARY 2│ ← Copias sincronizadas
└───────────┘     └───────────┘
  (puede leer)      (puede leer)
```

**¿Cómo funciona?**

1. Todas las escrituras van al **PRIMARY**.
2. El PRIMARY registra cada operación en el **oplog** (operation log).
3. Los SECONDARY leen continuamente el oplog y replican las operaciones.
4. Si el PRIMARY falla, los SECONDARY se comunican entre ellos, votan, y uno se convierte en el nuevo PRIMARY automáticamente.
5. Cuando el antiguo PRIMARY vuelve, se reincorpora como SECONDARY.

**¿Por qué es valioso?**

- **Alta disponibilidad**: Si un nodo falla, el sistema sigue funcionando.
- **Redundancia de datos**: Tienes 3 copias de todos los datos.
- **Escalado de lecturas**: Puedes configurar que las lecturas se distribuyan entre los secundarios.

### **3.3. Sharding: distribución horizontal**

El sharding resuelve un problema diferente: ¿qué pasa cuando los datos no caben en un solo servidor, o cuando el volumen de operaciones es demasiado para una máquina?

**Conceptualmente, el sharding divide los datos entre múltiples servidores:**

```
COLECCIÓN: pedidos (10 millones de documentos)

                    ┌──────────────┐
                    │   MONGOS     │ ← Router que recibe consultas
                    │  (router)    │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌──────────┐     ┌──────────┐     ┌──────────┐
    │ SHARD 1  │     │ SHARD 2  │     │ SHARD 3  │
    │          │     │          │     │          │
    │ Pedidos  │     │ Pedidos  │     │ Pedidos  │
    │ C0000-   │     │ C3333-   │     │ C6666-   │
    │ C3333    │     │ C6666    │     │ C9999    │
    └──────────┘     └──────────┘     └──────────┘
   3.3M docs        3.3M docs        3.4M docs
```

Los datos se dividen según una **shard key** (clave de fragmentación). En este ejemplo, si la shard key es `cliente_id`, MongoDB distribuye los pedidos según el ID del cliente: pedidos de clientes C0000-C3333 van al shard 1, etc.

**¿Cómo sabe mongos dónde están los datos?**

Los **Config Servers** almacenan un mapa completo de qué datos están en qué shard. Cuando una consulta llega a mongos, este pregunta a los config servers: "¿dónde están los pedidos del cliente C5000?" Los config servers responden: "en el shard 2". Mongos enruta la consulta allí.

**Ventajas del sharding:**

- **Capacidad ilimitada**: Si necesitas más espacio, añades más shards.
- **Rendimiento distribuido**: Las consultas se ejecutan en paralelo en múltiples shards.
- **Escalado horizontal económico**: En lugar de un servidor de €50,000, usas 10 servidores de €5,000.

**Complejidad del sharding:**

- Elegir una buena shard key es crítico y difícil de cambiar.
- Más componentes = más cosas que pueden fallar.
- Algunas consultas deben tocar todos los shards (menos eficientes).

***

## **4. Índices: el secreto del rendimiento**

### **4.1. ¿Qué es un índice?**

Un índice es una estructura de datos que permite buscar documentos rápidamente sin tener que escanear toda la colección. Es como el índice alfabético de un libro: en lugar de leer las 500 páginas para encontrar "MongoDB", miras el índice, ves que está en la página 342, y vas directamente allí.

**Sin índice:**

```
Consulta: db.clientes.find({ email: "juan@ejemplo.com" })

MongoDB debe:
1. Leer documento 1: ¿email = juan@ejemplo.com? No
2. Leer documento 2: ¿email = juan@ejemplo.com? No
3. Leer documento 3: ¿email = juan@ejemplo.com? No
...
1,000,000. Leer documento 1M: ¿email = juan@ejemplo.com? Sí! (finalmente)

Resultado: 1,000,000 documentos examinados, 1 devuelto
Tiempo: varios segundos
```

**Con índice en el campo `email`:**

```
MongoDB:
1. Consulta el índice (estructura B-tree ordenada)
2. Encuentra "juan@ejemplo.com" en el índice
3. Obtiene el puntero al documento
4. Lee únicamente ese documento

Resultado: 1 documento examinado, 1 devuelto
Tiempo: milisegundos
```

### **4.2. Tipos de índices conceptualmente**

**Índice simple:** Sobre un campo único.
```javascript
{ email: 1 }  // Índice ascendente en email
```

**Índice compuesto:** Sobre múltiples campos.
```javascript
{ apellido: 1, nombre: 1 }  // Ordenado primero por apellido, luego nombre
```
Útil para consultas que filtran por ambos campos o solo por el primero (apellido), pero NO eficiente para consultas solo por nombre.

**Índice único:** Garantiza que no haya duplicados.
```javascript
{ email: 1, unique: true }  // No puede haber dos clientes con el mismo email
```

**Índice de texto completo:** Para búsquedas de texto.
```javascript
{ contenido: "text" }  // Permite búsquedas como "MongoDB administración"
```

**Índice geoespacial:** Para consultas de ubicación.
```javascript
{ ubicacion: "2dsphere" }  // Permite "encuentra restaurantes a menos de 5km"
```

**Índice hash:** Distribuye uniformemente pero pierde ordenamiento.
```javascript
{ usuario_id: "hashed" }  // Útil para sharding, NO para rangos
```

### **4.3. El dilema de los índices**

Los índices aceleran las lecturas pero ralentizan las escrituras. Cada vez que insertas o actualizas un documento, MongoDB debe actualizar también todos los índices relevantes.

**Ejemplo:**

```
Colección: productos (sin índices adicionales, solo _id)
- Insertar 1 documento: 1ms
- Buscar por nombre: 5000ms (scan completo)

Colección: productos (con 5 índices: nombre, categoria, precio, fabricante, fecha)
- Insertar 1 documento: 6ms (debe actualizar 6 estructuras: 5 índices + datos)
- Buscar por nombre: 2ms (usa índice)
```

**Regla de diseño:** Indexa solo los campos que realmente consultas frecuentemente. Cada índice tiene un coste en espacio y rendimiento de escritura.

***

## **5. Transacciones y consistencia**

### **5.1. Atomicidad a nivel de documento**

En MongoDB, las operaciones sobre un **documento único** son atómicas. Esto significa que una actualización compleja sobre un documento se ejecuta completamente o no se ejecuta en absoluto. No puede quedar "a medias".

```javascript
// Esta operación es atómica
db.cuentas.updateOne(
  { _id: "cuenta123" },
  {
    $inc: { saldo: -100 },
    $push: { movimientos: { tipo: "retiro", cantidad: 100, fecha: new Date() } }
  }
)

// O se ejecutan ambas operaciones ($inc y $push), o ninguna
// Nunca puede quedar el saldo decrementado sin el movimiento registrado
```

Esta es una de las razones por las que el modelado embebido es poderoso: si toda la información relacionada está en un documento, todas las actualizaciones son automáticamente atómicas.

### **5.2. Transacciones multi-documento**

Desde MongoDB 4.0, se soportan transacciones ACID multi-documento, similar a las bases de datos SQL. Sin embargo, tienen más overhead y deben usarse solo cuando son realmente necesarias.

**Ejemplo conceptual: transferencia bancaria**

```javascript
// Sin transacción: ¡PELIGROSO!
db.cuentas.updateOne({ _id: "cuentaA" }, { $inc: { saldo: -100 } })  // Se resta de A
// Si aquí falla el servidor, perdimos €100 en el éter
db.cuentas.updateOne({ _id: "cuentaB" }, { $inc: { saldo: 100 } })   // Se suma a B

// Con transacción: SEGURO
session.startTransaction()
try {
  db.cuentas.updateOne({ _id: "cuentaA" }, { $inc: { saldo: -100 } }, { session })
  db.cuentas.updateOne({ _id: "cuentaB" }, { $inc: { saldo: 100 } }, { session })
  session.commitTransaction()  // Se ejecutan ambas o ninguna
} catch (error) {
  session.abortTransaction()  // Rollback si algo falla
}
```

**¿Cuándo usar transacciones?**

- Cuando necesitas actualizar múltiples documentos de forma atómica
- Operaciones financieras, inventarios críticos
- Cualquier caso donde la consistencia absoluta sea obligatoria

**¿Cuándo NO usarlas?**

- Operaciones sobre un solo documento (ya son atómicas)
- Casos donde eventual consistency es aceptable
- Alta concurrencia (las transacciones tienen overhead)

***

## **6. Consistencia eventual vs. inmediata**

En un Replica Set, cuando escribes al PRIMARY, los SECONDARY replican los datos, pero hay un **pequeño retraso** (típicamente milisegundos, a veces segundos si hay problemas de red).

**Escenario:**

```
17:00:00.000 - Aplicación escribe: db.usuarios.insertOne({ nombre: "Ana" })
17:00:00.001 - PRIMARY guarda el documento
17:00:00.002 - PRIMARY responde a la aplicación: "OK, insertado"
17:00:00.010 - SECONDARY 1 replica el documento (9ms de retraso)
17:00:00.015 - SECONDARY 2 replica el documento (14ms de retraso)
```

Si a las 17:00:00.005 otra parte de la aplicación lee desde SECONDARY 1, **no verá el documento de Ana todavía**. Esto se llama **consistencia eventual**: eventualmente todos los nodos tendrán los mismos datos, pero hay una ventana temporal donde pueden estar desincronizados.

**Read Concerns (nivel de consistencia de lectura):**

- **local**: Lee lo que haya en el nodo (puede no estar replicado todavía)
- **majority**: Lee solo datos confirmados por mayoría de nodos (más seguro, pero puede tener retraso)
- **linearizable**: Lee lo más reciente garantizado (el más lento)

**Write Concerns (nivel de confirmación de escritura):**

- **w:1**: Confirma cuando el PRIMARY ha escrito (rápido, pero sin garantía de replicación)
- **w:"majority"**: Confirma cuando la mayoría de nodos ha replicado (más lento, pero seguro)
- **w:3**: Confirma cuando 3 nodos específicos han replicado

**Trade-off:** Más consistencia = más latencia. Elige según tus necesidades.
