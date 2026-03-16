# PRÁCTICA: ARQUITECTURAS MONGODB CON DOCKER-COMPOSE

## **OBJETIVO DE LA PRÁCTICA**

En esta práctica aprenderás a desplegar y gestionar arquitecturas distribuidas de MongoDB utilizando Docker Compose. Implementarás un **Replica Set** (conjunto de réplicas) para entender cómo MongoDB proporciona alta disponibilidad, redundancia de datos y tolerancia a fallos. Al finalizar, comprenderás cómo funciona la replicación automática, el proceso de elección de nodo primario y cómo recuperarse ante fallos. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)

**Conceptos que dominarás:**
- Replica Sets: nodos primarios y secundarios
- Replicación automática mediante oplog
- Proceso de elección (election) cuando falla el primario
- Operaciones de lectura/escritura en arquitecturas distribuidas
- Monitorización del estado del cluster

**Requisitos previos:**
- Docker y Docker Compose instalados
- Conocimientos básicos de MongoDB
- Terminal de comandos (bash/zsh)
- 4GB RAM disponible



##  **PARTE 1: ENTENDIENDO LA ARQUITECTURA**

### **¿Qué es un Replica Set?**

Un Replica Set es un grupo de instancias MongoDB que mantienen los mismos datos. Proporciona redundancia y alta disponibilidad, que son fundamentales en producción. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)

**Componentes:**
- **PRIMARY (Primario)**: Único nodo que acepta escrituras
- **SECONDARY (Secundarios)**: Replican datos del primario automáticamente
- **ARBITER (Opcional)**: Participa en elecciones pero no almacena datos

```
┌─────────────────────────────────────────┐
│         REPLICA SET: rs0                │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐      ┌──────────┐       │
│  │  mongo1  │◄────►│  mongo2  │       │
│  │ PRIMARY  │      │SECONDARY │       │
│  └──────────┘      └──────────┘       │
│       ▲                  ▲             │
│       │                  │             │
│       │    ┌──────────┐  │             │
│       └───►│  mongo3  │◄─┘             │
│            │SECONDARY │                │
│            └──────────┘                │
│                                         │
│  Replicación automática via OPLOG      │
└─────────────────────────────────────────┘
```

**¿Cómo funciona la replicación?**

1. Una aplicación escribe en el PRIMARY
2. El PRIMARY registra la operación en el **oplog** (operations log)
3. Los SECONDARY leen el oplog y aplican las mismas operaciones
4. Si el PRIMARY cae, los SECONDARY eligen un nuevo PRIMARY automáticamente [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)



##  **PARTE 2: PREPARACIÓN DEL ENTORNO**

### **Paso 1: Crear estructura de directorios**

Crea una carpeta para la práctica y organiza los archivos:

```bash
# Crear directorio del proyecto
mkdir mongodb-replicaset-lab
cd mongodb-replicaset-lab

# Crear subdirectorios para datos persistentes
mkdir -p data/mongo1 data/mongo2 data/mongo3

# Crear directorio para scripts
mkdir scripts
```

**¿Qué estamos haciendo?**
- `data/mongo1`, `data/mongo2`, `data/mongo3`: Almacenarán los datos de cada nodo MongoDB. Así los datos persisten aunque eliminemos los contenedores.
- `scripts`: Contendrá scripts de inicialización y configuración.

### **Paso 2: Crear el archivo docker-compose.yml**

Crea el archivo `docker-compose.yml` con el siguiente contenido:

```yaml
version: '3.8'

services:
  # NODO 1: Será el PRIMARY inicialmente
  mongo1:
    image: mongo:7.0
    container_name: mongo1
    hostname: mongo1
    ports:
      - "27017:27017"
    command: mongod --replSet rs0 --bind_ip_all
    volumes:
      - ./data/mongo1:/data/db
    networks:
      - mongo-network
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 40s

  # NODO 2: SECONDARY
  mongo2:
    image: mongo:7.0
    container_name: mongo2
    hostname: mongo2
    ports:
      - "27018:27017"
    command: mongod --replSet rs0 --bind_ip_all
    volumes:
      - ./data/mongo2:/data/db
    networks:
      - mongo-network
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 40s

  # NODO 3: SECONDARY
  mongo3:
    image: mongo:7.0
    container_name: mongo3
    hostname: mongo3
    ports:
      - "27019:27017"
    command: mongod --replSet rs0 --bind_ip_all
    volumes:
      - ./data/mongo3:/data/db
    networks:
      - mongo-network
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 40s

networks:
  mongo-network:
    driver: bridge
```

** Explicación línea por línea:**

- `image: mongo:7.0`: Usamos MongoDB versión 7.0 (última estable)
- `container_name` y `hostname`: Nombres únicos para cada nodo
- `ports`: Exponemos puertos diferentes en el host (27017, 27018, 27019) pero todos usan 27017 internamente
- `command: mongod --replSet rs0 --bind_ip_all`:
  - `--replSet rs0`: Indica que este nodo pertenece al Replica Set llamado "rs0"
  - `--bind_ip_all`: Permite conexiones desde cualquier IP (necesario en Docker)
- `volumes`: Persiste datos en carpetas locales
- `networks`: Todos los nodos en la misma red para comunicarse
- `healthcheck`: Docker verificará cada 10s que MongoDB responde correctamente

### **Paso 3: Iniciar los contenedores**

```bash
# Iniciar todos los contenedores en segundo plano
docker-compose up -d

# Verificar que estén corriendo
docker-compose ps
```

**Salida esperada:**
```
NAME      IMAGE       STATUS                    PORTS
mongo1    mongo:7.0   Up 30 seconds (healthy)   0.0.0.0:27017->27017/tcp
mongo2    mongo:7.0   Up 30 seconds (healthy)   0.0.0.0:27018->27017/tcp
mongo3    mongo:7.0   Up 30 seconds (healthy)   0.0.0.0:27019->27017/tcp
```

**¿Qué ha pasado?**
Docker ha descargado la imagen de MongoDB 7.0 (si no la tenías) y ha iniciado 3 contenedores independientes. Cada uno ejecuta una instancia de MongoDB, pero **aún no están configurados como Replica Set**. En este momento son 3 instancias standalone separadas.



## **PARTE 3: CONFIGURACIÓN DEL REPLICA SET**

### **Paso 4: Inicializar el Replica Set**

Ahora conectaremos los 3 nodos para formar un Replica Set: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)

```bash
# Conectar al primer nodo (mongo1)
docker exec -it mongo1 mongosh
```

**Dentro de la shell de MongoDB**, ejecuta:

```javascript
// Configuración del Replica Set
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017", priority: 2 },
    { _id: 1, host: "mongo2:27017", priority: 1 },
    { _id: 2, host: "mongo3:27017", priority: 1 }
  ]
})
```

** Explicación del comando:**

- `rs.initiate()`: Inicializa el Replica Set
- `_id: "rs0"`: Nombre del Replica Set (debe coincidir con --replSet del docker-compose)
- `members`: Array con los 3 nodos
  - `_id: 0, 1, 2`: Identificadores únicos de cada miembro
  - `host`: Nombre del host y puerto (usamos nombres de contenedor)
  - `priority: 2` para mongo1: Tiene prioridad más alta, preferido como PRIMARY [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)
  - `priority: 1` para mongo2 y mongo3: Pueden ser PRIMARY si mongo1 falla

**Salida esperada:**
```javascript
{ ok: 1 }
```

**Espera 10-15 segundos** para que se complete la elección del primario. Verás que el prompt cambia de `test>` a `rs0 [direct: primary]>` o similar.

### **Paso 5: Verificar el estado del Replica Set**

```javascript
// Ver estado completo del cluster
rs.status()
```

**Busca en la salida:**
```javascript
{
  set: 'rs0',
  members: [
    {
      _id: 0,
      name: 'mongo1:27017',
      stateStr: 'PRIMARY',
      health: 1,
      ...
    },
    {
      _id: 1,
      name: 'mongo2:27017',
      stateStr: 'SECONDARY',
      health: 1,
      ...
    },
    {
      _id: 2,
      name: 'mongo3:27017',
      stateStr: 'SECONDARY',
      health: 1,
      ...
    }
  ],
  ok: 1
}
```

**¿Qué significa cada campo?**
- `stateStr: 'PRIMARY'`: Este nodo acepta escrituras
- `stateStr: 'SECONDARY'`: Este nodo replica datos del primario
- `health: 1`: El nodo está operativo (0 = caído)

También puedes usar comandos más simples:

```javascript
// Resumen rápido
rs.isMaster()

// Ver configuración
rs.conf()
```



##  **PARTE 4: PROBANDO LA REPLICACIÓN**

### **Paso 6: Insertar datos en el PRIMARY**

Desde la misma shell de mongosh conectada a mongo1 (PRIMARY):

```javascript
// Cambiar a una base de datos de prueba
use tiendaOnline

// Insertar documentos
db.productos.insertMany([
  { nombre: "Laptop Dell", precio: 899, stock: 15, categoria: "Informática" },
  { nombre: "Mouse Logitech", precio: 25, stock: 100, categoria: "Periféricos" },
  { nombre: "Teclado Mecánico", precio: 120, stock: 30, categoria: "Periféricos" },
  { nombre: "Monitor 27''", precio: 350, stock: 20, categoria: "Informática" },
  { nombre: "Webcam HD", precio: 65, stock: 45, categoria: "Periféricos" }
])

// Verificar inserción
db.productos.find().pretty()
```

**Salida esperada:**
```javascript
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("..."),
    '1': ObjectId("..."),
    ...
  }
}
```

### **Paso 7: Verificar que los datos se replicaron**

Abre **otra terminal** (sin cerrar la anterior) y conéctate a mongo2 (SECONDARY):

```bash
# Terminal 2
docker exec -it mongo2 mongosh
```

Dentro de mongosh de mongo2:

```javascript
// Habilitar lecturas en SECONDARY (por defecto están deshabilitadas)
rs.secondaryOk()
// O en versiones más nuevas:
// db.getMongo().setReadPref('secondary')

// Cambiar a la misma base de datos
use tiendaOnline

// ¡Leer los datos replicados!
db.productos.find().pretty()
```

** ¡Deberías ver los mismos 5 productos!**

**¿Qué ha pasado?**
1. Insertaste datos en el PRIMARY (mongo1)
2. MongoDB registró las operaciones en el oplog del PRIMARY
3. Los SECONDARY (mongo2 y mongo3) leyeron el oplog automáticamente
4. Aplicaron las mismas operaciones de inserción en sus propias copias de datos
5. **Replicación completada en segundos** (normalmente milisegundos) [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)

### **Paso 8: Intentar escribir en un SECONDARY (debe fallar)**

Desde la shell de mongo2 (SECONDARY):

```javascript
// Intentar insertar en un SECONDARY
db.productos.insertOne({ nombre: "Prueba", precio: 10 })
```

**Error esperado:**
```javascript
MongoServerError: not primary
```

**¿Por qué?**
Los SECONDARY **SOLO pueden leer**, no escribir. Esto garantiza consistencia de datos. Todas las escrituras deben ir al PRIMARY, que luego las replica a los SECONDARY. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)



## **PARTE 5: SIMULANDO FALLO DEL PRIMARY (FAILOVER)**

Esta es la parte más importante: verás cómo MongoDB maneja automáticamente la caída del nodo primario.

### **Paso 9: Detener el nodo PRIMARY**

```bash
# En una nueva terminal
docker stop mongo1
```

**¿Qué va a pasar?**
1. Los SECONDARY detectarán que mongo1 no responde (después de 10 segundos de heartbeats fallidos) [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)
2. Iniciarán un proceso de elección (election)
3. El SECONDARY con mayor prioridad (ambos tienen priority=1) será elegido como nuevo PRIMARY
4. El proceso es **completamente automático**, sin intervención humana

### **Paso 10: Observar la elección automática**

Vuelve a la terminal donde tienes mongo2 abierto y ejecuta:

```javascript
// Ver el nuevo estado del cluster
rs.status()
```

Espera unos 10-15 segundos y vuelve a ejecutar `rs.status()` hasta que veas algo como:

```javascript
{
  members: [
    {
      _id: 0,
      name: 'mongo1:27017',
      stateStr: '(not reachable/healthy)',
      health: 0,  // ¡Caído!
      ...
    },
    {
      _id: 1,
      name: 'mongo2:27017',
      stateStr: 'PRIMARY',  // ¡Ahora es PRIMARY!
      health: 1,
      ...
    },
    {
      _id: 2,
      name: 'mongo3:27017',
      stateStr: 'SECONDARY',
      health: 1,
      ...
    }
  ]
}
```

** ¡Failover completado! mongo2 es ahora el PRIMARY.**

### **Paso 11: Escribir en el nuevo PRIMARY**

Desde mongo2 (que ahora es PRIMARY):

```javascript
// Insertar nuevo producto
db.productos.insertOne({ 
  nombre: "SSD 1TB", 
  precio: 95, 
  stock: 50, 
  categoria: "Almacenamiento",
  agregadoDespuesFailover: true 
})

// Verificar
db.productos.find({ agregadoDespuesFailover: true })
```

**Ahora mongo2 acepta escrituras** porque es el nuevo PRIMARY.

### **Paso 12: Verificar replicación en mongo3**

Abre otra terminal y conéctate a mongo3:

```bash
docker exec -it mongo3 mongosh
```

```javascript
rs.secondaryOk()
use tiendaOnline

// ¡El nuevo producto debería estar aquí también!
db.productos.find({ agregadoDespuesFailover: true })
```

**¿Qué demuestra esto?**
El cluster sigue funcionando con 2 de 3 nodos. La replicación continúa normalmente entre el nuevo PRIMARY (mongo2) y el SECONDARY restante (mongo3).



##  **PARTE 6: RECUPERACIÓN DEL NODO CAÍDO**

### **Paso 13: Reiniciar mongo1**

```bash
# Reiniciar el contenedor
docker start mongo1
```

Espera 20-30 segundos y observa qué pasa:

```javascript
// Desde mongo2 (actual PRIMARY), verifica el estado
rs.status()
```

Verás que mongo1 ha vuelto como **SECONDARY**:

```javascript
{
  _id: 0,
  name: 'mongo1:27017',
  stateStr: 'SECONDARY',  // ¡Ha vuelto pero como SECONDARY!
  health: 1,
  ...
}
```

**¿Por qué no vuelve como PRIMARY automáticamente?**

Aunque mongo1 tiene `priority: 2`, no reemplaza al PRIMARY actual inmediatamente. MongoDB es conservador para evitar elecciones innecesarias que interrumpirían brevemente las operaciones.

**¿mongo1 tiene los datos actualizados?**

¡Sí! Al reconectarse, mongo1 lee el oplog y se sincroniza automáticamente con todos los cambios que ocurrieron mientras estaba caído.

### **Paso 14: Forzar que mongo1 vuelva a ser PRIMARY (opcional)**

Si quieres que mongo1 recupere su rol de PRIMARY:

```javascript
// Desde cualquier nodo conectado al cluster
rs.stepDown(60)
```

Este comando hace que el PRIMARY actual (mongo2) renuncie voluntariamente durante 60 segundos, forzando una nueva elección. mongo1, con mayor prioridad, será elegido.



##  **PARTE 7: MONITORIZACIÓN Y COMANDOS ÚTILES**

### **Comandos de monitorización**

```javascript
// Ver estadísticas de replicación
rs.printReplicationInfo()
// Muestra: tamaño del oplog, cuánto tiempo de operaciones contiene

// Ver retraso (lag) de los SECONDARY
rs.printSecondaryReplicationInfo()
// Muestra: cuánto van retrasados los SECONDARY respecto al PRIMARY

// Ver qué nodos votan en elecciones
rs.conf().members.forEach(m => {
  print(`${m.host}: votes=${m.votes}, priority=${m.priority}`)
})

// Monitorear el oplog (operations log)
use local
db.oplog.rs.find().limit(5).sort({$natural: -1})
// Muestra las últimas 5 operaciones replicadas
```

### **Verificar sincronización**

```javascript
// Desde el PRIMARY
db.serverStatus().repl
// Muestra información detallada de replicación

// Comparar tamaños de colecciones (deben ser iguales)
db.productos.countDocuments()
```



## 🧪 **PARTE 8: EXPERIMENTOS ADICIONALES**

### **Experimento 1: Leer desde SECONDARY**

MongoDB permite configurar preferencias de lectura:

```javascript
// Conectar a mongo2 (SECONDARY)
db.getMongo().setReadPref('secondary')

// Ahora puedes leer sin rs.secondaryOk()
db.productos.find()

// Leer desde el nodo más cercano (útil en clusters geográficamente distribuidos)
db.getMongo().setReadPref('nearest')
```

**Casos de uso:**
- Leer desde SECONDARY: Descargar trabajo de lectura del PRIMARY
- Aplicaciones de análisis/reportes que no requieren datos en tiempo real exacto

### **Experimento 2: Añadir un nodo ARBITER**

Un ARBITER participa en elecciones pero no almacena datos. Útil para tener número impar de votantes sin el coste de almacenamiento. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)

Añade esto al `docker-compose.yml`:

```yaml
  mongo-arbiter:
    image: mongo:7.0
    container_name: mongo-arbiter
    command: mongod --replSet rs0 --bind_ip_all
    networks:
      - mongo-network
```

Reinicia y añádelo al Replica Set:

```javascript
rs.addArb("mongo-arbiter:27017")
rs.status()  // Verás stateStr: 'ARBITER'
```

### **Experimento 3: Simular caída de mayoría**

```bash
# Detener 2 de 3 nodos
docker stop mongo2 mongo3
```

Conéctate a mongo1:

```javascript
// Verificar estado
rs.status()

// Intentar escribir
db.productos.insertOne({ nombre: "Test" })
```

**Error esperado:**
```
NotWritablePrimary: not primary
```

**¿Por qué?**
Con solo 1 de 3 nodos activos, no hay **mayoría (quorum)**. MongoDB requiere que la mayoría de nodos estén operativos para garantizar consistencia de datos. Con 3 nodos, se necesitan al menos 2. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)

```bash
# Reiniciar uno de los nodos para recuperar mayoría
docker start mongo2
# Esperar 15 segundos y las operaciones volverán a funcionar
```



## **PARTE 9: PRUEBAS DE EVALUACIÓN**

### **Test de conocimientos**

Ejecuta estas tareas para verificar tu comprensión:

1. **Insertar 100 documentos en el PRIMARY y verificar que todos lleguen a los SECONDARY**

```javascript
// En PRIMARY
use testReplica
for(let i=1; i<=100; i++) {
  db.test.insertOne({ numero: i, fecha: new Date() })
}

// En SECONDARY
rs.secondaryOk()
use testReplica
db.test.countDocuments()  // Debe ser 100
```

2. **Simular un failover completo: detén el PRIMARY, escribe en el nuevo PRIMARY, reinicia el antiguo PRIMARY**

3. **Medir el tiempo de failover:**

```javascript
// Script de monitorización continua
while(true) {
  try {
    rs.isMaster().primary
    sleep(1000)
  } catch(e) {
    print("PRIMARY NO DISPONIBLE")
  }
}
```

Ejecuta esto en una terminal, detén el PRIMARY en otra, y cuenta cuántos segundos tarda en detectarse y elegirse nuevo PRIMARY. Normalmente 10-15 segundos. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)



## **PARTE 10: LIMPIEZA Y CONCLUSIÓN**

### **Detener y limpiar el entorno**

```bash
# Detener todos los contenedores
docker-compose down

# Eliminar también los datos persistentes (¡CUIDADO!)
sudo rm -rf data/

# O mantener los datos para futuras prácticas
# (solo detiene contenedores, los datos persisten)
```

### **Verificar limpieza**

```bash
docker ps -a | grep mongo
# No debería mostrar contenedores mongo
```



## 📚 **RESUMEN DE CONCEPTOS APRENDIDOS**

✅ **Replica Set**: Conjunto de instancias MongoDB que mantienen los mismos datos  
✅ **PRIMARY**: Único nodo que acepta escrituras  
✅ **SECONDARY**: Nodos que replican datos del PRIMARY automáticamente  
✅ **Oplog**: Log de operaciones que permite la replicación asíncrona [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)
✅ **Failover**: Proceso automático de elección de nuevo PRIMARY cuando el actual falla  
✅ **Quorum**: Mayoría de nodos necesaria para operaciones de escritura  
✅ **Priority**: Determina qué nodos son preferidos para ser PRIMARY [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)
✅ **Heartbeats**: Verificaciones cada 2 segundos para detectar nodos caídos  

### **Aplicaciones en producción**

Esta arquitectura es **esencial** en sistemas de producción porque:

1. **Alta disponibilidad**: Si un servidor falla, otro toma el control automáticamente
2. **Redundancia de datos**: Múltiples copias previenen pérdida de información
3. **Escalado de lecturas**: Los SECONDARY pueden servir consultas de lectura
4. **Backups sin downtime**: Puedes hacer backup desde un SECONDARY sin afectar el PRIMARY
5. **Tolerancia a fallos**: El sistema sigue operativo mientras haya mayoría de nodos

### **Próximos pasos**

Para seguir aprendiendo:
- **Sharding**: Distribución horizontal de datos entre múltiples Replica Sets [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)
- **Config Servers y mongos**: Componentes para arquitecturas con sharding
- **Zonas y distribución geográfica**: Replica Sets en múltiples datacenters
- **Monitorización con MongoDB Atlas o Ops Manager**



## **ANEXO: COMANDOS DE REFERENCIA RÁPIDA**

```javascript
// ESTADO DEL CLUSTER
rs.status()                    // Estado completo
rs.isMaster()                  // ¿Quién es el PRIMARY?
rs.conf()                      // Configuración actual

// INFORMACIÓN DE REPLICACIÓN
rs.printReplicationInfo()      // Info del oplog
rs.printSecondaryReplicationInfo()  // Lag de secundarios

// MODIFICAR CLUSTER
rs.add("host:port")            // Añadir nodo
rs.remove("host:port")         // Eliminar nodo
rs.addArb("host:port")         // Añadir árbitro
rs.stepDown(60)                // PRIMARY renuncia 60 segundos

// CONFIGURACIÓN DE NODOS
rs.reconfigure(config)         // Aplicar nueva configuración
rs.freeze(seconds)             // Evita que SECONDARY sea elegido PRIMARY

// LECTURAS
rs.secondaryOk()               // Permitir lecturas en SECONDARY
db.getMongo().setReadPref('secondary')  // Preferencia de lectura
```



## **PREGUNTAS FRECUENTES**

**P: ¿Por qué necesito 3 nodos mínimo?**  
R: Para tener mayoría (quorum). Con 2 nodos, si uno cae, no hay mayoría y el cluster se bloquea para escrituras.

**P: ¿Cuánto datos puede perder en un failover?**  
R: Por defecto, MongoDB usa write concern `w:1`, que confirma escritura cuando el PRIMARY la registra. Con `w:majority`, espera confirmación de la mayoría de nodos, garantizando durabilidad pero con mayor latencia.

**P: ¿Los SECONDARY están siempre exactamente sincronizados?**  
R: No, puede haber un pequeño retraso (lag) de milisegundos a segundos. Depende de la carga y la red. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/58c1624d-8c24-476d-99f1-b65440f4443a/02.md)

**P: ¿Qué pasa si falla más de la mitad de los nodos?**  
R: El cluster deja de aceptar escrituras hasta que se recupere la mayoría. Las aplicaciones recibirán errores.

**P: ¿Puedo tener Replica Sets en diferentes ubicaciones geográficas?**  
R: Sí, MongoDB soporta Replica Sets distribuidos geográficamente. Debes ajustar timeouts y considerar latencias de red.