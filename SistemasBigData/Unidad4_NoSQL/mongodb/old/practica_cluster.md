# **PRÁCTICA GUIADA: Arquitectura Distribuida en MongoDB**
## **Del Standalone al Sharded Cluster - Experimentación Práctica**



## **Objetivos de la práctica**

Al finalizar esta práctica, serás capaz de:

1. Configurar un Replica Set desde cero
2. Simular un failover y observar la elección automática
3. Monitorizar el lag de replicación
4. Configurar un Sharded Cluster completo
5. Observar cómo se distribuyen los datos entre shards
6. Comparar el rendimiento de consultas targeted vs broadcast



## **Requisitos previos**

- Docker y Docker Compose instalados
- Terminal/shell disponible
- mongosh instalado localmente (o usar el de Docker)
- Navegador web (para visualizar métricas opcionales)



## **PARTE 1: Configuración de un Replica Set**

### **Paso 1.1: Preparar el entorno con Docker**

Vamos a crear un Replica Set de 3 nodos usando Docker Compose.

**Crear el directorio de trabajo:**

```bash
mkdir -p ~/mongodb-practica/replica-set
cd ~/mongodb-practica/replica-set
```

**Crear `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  mongo1:
    image: mongo:7.0
    container_name: mongo1
    command: mongod --replSet rsLab --port 27017 --bind_ip_all
    ports:
      - "27017:27017"
    volumes:
      - mongo1_data:/data/db
      - mongo1_config:/data/configdb
    networks:
      - mongo-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh --quiet
      interval: 10s
      timeout: 5s
      retries: 3

  mongo2:
    image: mongo:7.0
    container_name: mongo2
    command: mongod --replSet rsLab --port 27017 --bind_ip_all
    ports:
      - "27018:27017"
    volumes:
      - mongo2_data:/data/db
      - mongo2_config:/data/configdb
    networks:
      - mongo-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh --quiet
      interval: 10s
      timeout: 5s
      retries: 3

  mongo3:
    image: mongo:7.0
    container_name: mongo3
    command: mongod --replSet rsLab --port 27017 --bind_ip_all
    ports:
      - "27019:27017"
    volumes:
      - mongo3_data:/data/db
      - mongo3_config:/data/configdb
    networks:
      - mongo-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh --quiet
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  mongo1_data:
  mongo1_config:
  mongo2_data:
  mongo2_config:
  mongo3_data:
  mongo3_config:

networks:
  mongo-network:
    driver: bridge
```

**Iniciar los contenedores:**

```bash
docker-compose up -d
```

**Verificar que están corriendo:**

```bash
docker ps
```

Deberías ver 3 contenedores: `mongo1`, `mongo2`, `mongo3`.



### **Paso 1.2: Inicializar el Replica Set**

**Conectar a mongo1:**

```bash
docker exec -it mongo1 mongosh
```

**Dentro del shell de MongoDB, inicializar el Replica Set:**

```javascript
rs.initiate({
  _id: "rsLab",
  members: [
    { _id: 0, host: "mongo1:27017", priority: 2 },
    { _id: 1, host: "mongo2:27017", priority: 1 },
    { _id: 2, host: "mongo3:27017", priority: 1 }
  ]
})
```

**Esperar unos 10-20 segundos y verificar el estado:**

```javascript
rs.status()
```

**📝 EJERCICIO 1.1:** 
> Observa la salida de `rs.status()` e identifica:
> - ¿Cuál es el nodo PRIMARY?
> - ¿Cuál es el `electionTime` del primario?
> - ¿Cuál es el `syncSourceHost` de cada secundario?

**Script para monitorizar en tiempo real:**

```javascript
// Guardar este script como monitor.js
function monitorRS() {
  while (true) {
    print("\n=== ESTADO DEL REPLICA SET ===");
    print("Timestamp: " + new Date().toISOString());
    
    rs.status().members.forEach(m => {
      let lag = m.optimeDate && m.state === 2 
        ? Math.round((new Date() - m.optimeDate) / 1000) 
        : 0;
      
      print(`${m.name.padEnd(20)} | ${m.stateStr.padEnd(12)} | Lag: ${lag}s`);
    });
    
    sleep(5000);  // Actualizar cada 5 segundos
  }
}

// Ejecutar
monitorRS();
```

**Ejecutar el script:**

```bash
docker exec -it mongo1 mongosh --file /dev/stdin < monitor.js
```



### **Paso 1.3: Insertar datos de prueba**

**Conectar al PRIMARY (mongo1) y crear una base de datos de prueba:**

```javascript
use laboratorio

// Crear colección con datos de ejemplo
for (let i = 0; i < 10000; i++) {
  db.experimentos.insertOne({
    experimento_id: i,
    tipo: ["temperatura", "presion", "humedad"][i % 3],
    valor: Math.random() * 100,
    timestamp: new Date(),
    ubicacion: ["Madrid", "Barcelona", "Valencia"][i % 3]
  });
  
  if (i % 1000 === 0) {
    print("Insertados: " + i);
  }
}

print("✅ 10,000 documentos insertados");
```

**📝 EJERCICIO 1.2:**
> Verifica que los datos se han replicado a los secundarios:
> 1. Sal del PRIMARY (exit)
> 2. Conecta a mongo2: `docker exec -it mongo2 mongosh`
> 3. Ejecuta: `rs.secondaryOk()` (permite leer en secundarios)
> 4. Ejecuta: `use laboratorio; db.experimentos.countDocuments()`
> 5. ¿Cuántos documentos hay?



### **Paso 1.4: Simular un failover**

Ahora vamos a detener el PRIMARY y observar cómo uno de los secundarios se convierte en el nuevo primario.

**Identificar el PRIMARY actual:**

```bash
docker exec -it mongo1 mongosh --eval "rs.status().members.find(m => m.stateStr === 'PRIMARY')"
```

**Detener el contenedor PRIMARY (asumiendo que es mongo1):**

```bash
docker stop mongo1
```

**📝 EJERCICIO 1.3:**
> 1. Conecta rápidamente a mongo2: `docker exec -it mongo2 mongosh`
> 2. Ejecuta `rs.status()` cada 5 segundos
> 3. Observa el cambio de estado: SECONDARY → (posiblemente RECOVERING) → PRIMARY
> 4. ¿Cuánto tardó en completarse la elección?
> 5. Anota el nuevo `electionTime`

**Verificar que el cluster sigue funcionando:**

```javascript
use laboratorio

// Intentar insertar un nuevo documento
db.experimentos.insertOne({
  experimento_id: 10001,
  tipo: "test_failover",
  timestamp: new Date()
})

// ¿Funcionó? ✅
```

**Restaurar mongo1:**

```bash
docker start mongo1
```

**📝 EJERCICIO 1.4:**
> 1. Observa cómo mongo1 se reincorpora al cluster como SECONDARY
> 2. Ejecuta `rs.status()` en mongo1
> 3. Verifica su `syncSourceHost` (de dónde está replicando)
> 4. ¿Cuánto tarda en sincronizarse completamente?



### **Paso 1.5: Monitorizar el lag de replicación**

Vamos a crear un script que genere escrituras continuas y monitorice el lag.

**Script de escritura continua (`write-load.js`):**

```javascript
use laboratorio

let count = 0;
const startTime = new Date();

print("🚀 Iniciando carga de escritura continua...");
print("Presiona Ctrl+C para detener\n");

while (true) {
  try {
    db.experimentos.insertOne({
      experimento_id: 10000 + count,
      tipo: "load_test",
      valor: Math.random() * 100,
      timestamp: new Date()
    });
    
    count++;
    
    if (count % 100 === 0) {
      const elapsed = (new Date() - startTime) / 1000;
      const rate = count / elapsed;
      print(`Insertados: ${count} | Tasa: ${rate.toFixed(2)} docs/s`);
    }
    
    sleep(10);  // 10ms entre inserts = ~100 inserts/seg
  } catch (e) {
    print("❌ Error: " + e);
    break;
  }
}
```

**Ejecutar en una terminal:**

```bash
docker exec -it mongo1 mongosh < write-load.js
```

**Script de monitorización de lag (`monitor-lag.js`):**

```javascript
function monitorLag() {
  while (true) {
    const status = rs.status();
    const primary = status.members.find(m => m.state === 1);
    
    print("\n=== REPLICATION LAG ===");
    print("Time: " + new Date().toISOString());
    
    status.members.forEach(m => {
      if (m.state === 2 && primary) {
        const lag = Math.round((primary.optimeDate - m.optimeDate) / 1000);
        const lagColor = lag > 5 ? "⚠️" : "✅";
        print(`${lagColor} ${m.name}: ${lag} segundos de lag`);
      } else if (m.state === 1) {
        print(`🔵 ${m.name}: PRIMARY`);
      }
    });
    
    sleep(2000);
  }
}

monitorLag();
```

**Ejecutar en otra terminal:**

```bash
docker exec -it mongo2 mongosh < monitor-lag.js
```

**📝 EJERCICIO 1.5:**
> Mientras corre la carga de escritura:
> 1. Observa el lag en los secundarios
> 2. Detén mongo2 temporalmente: `docker pause mongo2`
> 3. Espera 30 segundos
> 4. Reactiva mongo2: `docker unpause mongo2`
> 5. ¿Cuánto tarda en recuperarse del lag?



## **PARTE 2: Configuración de Sharded Cluster**

Ahora vamos a desplegar un cluster con sharding completo.

### **Paso 2.1: Preparar el entorno sharded**

**Crear nuevo directorio:**

```bash
mkdir -p ~/mongodb-practica/sharded-cluster
cd ~/mongodb-practica/sharded-cluster
```

**Crear `docker-compose.yml` para cluster sharded:**

```yaml
version: '3.8'

services:
  # Config Servers (Replica Set)
  config1:
    image: mongo:7.0
    container_name: config1
    command: mongod --configsvr --replSet configRS --port 27019 --bind_ip_all
    ports:
      - "27019:27019"
    volumes:
      - config1_data:/data/db
    networks:
      - mongo-network

  config2:
    image: mongo:7.0
    container_name: config2
    command: mongod --configsvr --replSet configRS --port 27019 --bind_ip_all
    ports:
      - "27020:27019"
    volumes:
      - config2_data:/data/db
    networks:
      - mongo-network

  config3:
    image: mongo:7.0
    container_name: config3
    command: mongod --configsvr --replSet configRS --port 27019 --bind_ip_all
    ports:
      - "27021:27019"
    volumes:
      - config3_data:/data/db
    networks:
      - mongo-network

  # Shard 1 (Replica Set)
  shard1a:
    image: mongo:7.0
    container_name: shard1a
    command: mongod --shardsvr --replSet shard1RS --port 27018 --bind_ip_all
    ports:
      - "27101:27018"
    volumes:
      - shard1a_data:/data/db
    networks:
      - mongo-network

  shard1b:
    image: mongo:7.0
    container_name: shard1b
    command: mongod --shardsvr --replSet shard1RS --port 27018 --bind_ip_all
    ports:
      - "27102:27018"
    volumes:
      - shard1b_data:/data/db
    networks:
      - mongo-network

  # Shard 2 (Replica Set)
  shard2a:
    image: mongo:7.0
    container_name: shard2a
    command: mongod --shardsvr --replSet shard2RS --port 27018 --bind_ip_all
    ports:
      - "27201:27018"
    volumes:
      - shard2a_data:/data/db
    networks:
      - mongo-network

  shard2b:
    image: mongo:7.0
    container_name: shard2b
    command: mongod --shardsvr --replSet shard2RS --port 27018 --bind_ip_all
    ports:
      - "27202:27018"
    volumes:
      - shard2b_data:/data/db
    networks:
      - mongo-network

  # Mongos Router
  mongos:
    image: mongo:7.0
    container_name: mongos
    command: mongos --configdb configRS/config1:27019,config2:27019,config3:27019 --bind_ip_all --port 27017
    ports:
      - "27017:27017"
    depends_on:
      - config1
      - config2
      - config3
    networks:
      - mongo-network

volumes:
  config1_data:
  config2_data:
  config3_data:
  shard1a_data:
  shard1b_data:
  shard2a_data:
  shard2b_data:

networks:
  mongo-network:
    driver: bridge
```

**Iniciar todos los contenedores:**

```bash
docker-compose up -d
```



### **Paso 2.2: Inicializar componentes**

**A. Inicializar Config Servers:**

```bash
docker exec -it config1 mongosh --port 27019
```

```javascript
rs.initiate({
  _id: "configRS",
  configsvr: true,
  members: [
    { _id: 0, host: "config1:27019" },
    { _id: 1, host: "config2:27019" },
    { _id: 2, host: "config3:27019" }
  ]
})

// Verificar
rs.status()
```

**B. Inicializar Shard 1:**

```bash
docker exec -it shard1a mongosh --port 27018
```

```javascript
rs.initiate({
  _id: "shard1RS",
  members: [
    { _id: 0, host: "shard1a:27018" },
    { _id: 1, host: "shard1b:27018" }
  ]
})

rs.status()
```

**C. Inicializar Shard 2:**

```bash
docker exec -it shard2a mongosh --port 27018
```

```javascript
rs.initiate({
  _id: "shard2RS",
  members: [
    { _id: 0, host: "shard2a:27018" },
    { _id: 1, host: "shard2b:27018" }
  ]
})

rs.status()
```



### **Paso 2.3: Conectar shards al cluster**

**Conectar a mongos:**

```bash
docker exec -it mongos mongosh
```

```javascript
// Añadir shards
sh.addShard("shard1RS/shard1a:27018,shard1b:27018")
sh.addShard("shard2RS/shard2a:27018,shard2b:27018")

// Verificar
sh.status()
```

**📝 EJERCICIO 2.1:**
> En la salida de `sh.status()`, identifica:
> - El nombre de cada shard
> - El estado de cada shard
> - ¿Cuántos mongos están conectados?



### **Paso 2.4: Habilitar sharding y fragmentar colecciones**

```javascript
// Habilitar sharding en la base de datos
sh.enableSharding("tienda")

use tienda

// Crear índice para shard key
db.pedidos.createIndex({ cliente_id: 1 })

// Fragmentar la colección
sh.shardCollection("tienda.pedidos", { cliente_id: 1 })

// Verificar
sh.status()
```



### **Paso 2.5: Insertar datos y observar distribución**

**Script de inserción masiva:**

```javascript
use tienda

print("🚀 Insertando 100,000 pedidos...\n");

for (let i = 0; i < 100000; i++) {
  db.pedidos.insertOne({
    _id: i,
    cliente_id: "C" + String(i % 1000).padStart(5, '0'),
    total: Math.random() * 1000,
    productos: [
      {
        nombre: "Producto " + (i % 100),
        cantidad: Math.floor(Math.random() * 5) + 1
      }
    ],
    fecha: new Date(),
    estado: ["pendiente", "procesando", "enviado"][i % 3]
  });
  
  if (i % 10000 === 0) {
    print(`Insertados: ${i} / 100000`);
  }
}

print("\n✅ Inserción completada");
```

**📝 EJERCICIO 2.2:**
> 1. Ejecuta el script de inserción
> 2. Mientras se ejecuta, en otra terminal ejecuta: `sh.status()`
> 3. Observa la sección de chunks
> 4. ¿Cuántos chunks se han creado?
> 5. ¿Cómo se distribuyen entre los shards?

**Ver distribución detallada:**

```javascript
db.pedidos.getShardDistribution()
```

**Salida esperada:**

```
Shard shard1RS at shard1RS/shard1a:27018,shard1b:27018
  data: 5.2MB docs: 49234 chunks: 3
  estimated data per chunk: 1.7MB
  estimated docs per chunk: 16411

Shard shard2RS at shard2RS/shard2a:27018,shard2b:27018
  data: 5.3MB docs: 50766 chunks: 3
  estimated data per chunk: 1.7MB
  estimated docs per chunk: 16922

Totals
  data: 10.5MB docs: 100000 chunks: 6
  Shard shard1RS contains 49.23% data, 49.23% docs
  Shard shard2RS contains 50.77% data, 50.77% docs
```



### **Paso 2.6: Comparar consultas targeted vs broadcast**

**Consulta TARGETED (usa shard key):**

```javascript
db.pedidos.find({ cliente_id: "C00042" }).explain("executionStats")
```

**📝 EJERCICIO 2.3:**
> En la salida de explain(), busca:
> - `winningPlan.stage`: ¿Dice "SINGLE_SHARD"?
> - `executionTimeMillis`: ¿Cuánto tardó?
> - `totalDocsExamined` vs `nReturned`: ¿Cuál es el ratio?

**Consulta BROADCAST (sin shard key):**

```javascript
db.pedidos.find({ total: { $gt: 900 } }).explain("executionStats")
```

**📝 EJERCICIO 2.4:**
> Compara con la consulta anterior:
> - `winningPlan.stage`: ¿Dice "SHARD_MERGE"?
> - ¿Cuántos shards consultó?
> - ¿Cuánto tardó en comparación?



### **Paso 2.7: Monitorizar el balanceador**

```javascript
// Ver estado del balancer
sh.getBalancerState()  // ¿true o false?

// Ver si hay migraciones en progreso
sh.isBalancerRunning()

// Ver configuración del balancer
sh.getBalancerConfig()

// Ver historial de migraciones
use config
db.changelog.find({ what: "moveChunk.commit" }).sort({ time: -1 }).limit(5)
```



## **PARTE 3: Experimentos avanzados**

### **Experimento 3.1: Simular crecimiento desigual**

```javascript
// Insertar muchos documentos con cliente_id similar
for (let i = 0; i < 50000; i++) {
  db.pedidos.insertOne({
    cliente_id: "CVIP0001",  // Todos van al mismo chunk!
    total: Math.random() * 1000,
    fecha: new Date()
  });
}

// Ver distribución
db.pedidos.getShardDistribution()

// ¿Se ha creado un jumbo chunk?
use config
db.chunks.find({ jumbo: true })
```



### **Experimento 3.2: Benchmark de rendimiento**

```javascript
// Función de benchmark
function benchmark(query, iterations) {
  const start = Date.now();
  
  for (let i = 0; i < iterations; i++) {
    db.pedidos.find(query).toArray();
  }
  
  const elapsed = Date.now() - start;
  const avgTime = elapsed / iterations;
  
  print(`\nBenchmark Results:`);
  print(`Iterations: ${iterations}`);
  print(`Total time: ${elapsed}ms`);
  print(`Avg per query: ${avgTime.toFixed(2)}ms`);
}

// Test 1: Query con shard key (targeted)
print("=== TARGETED QUERY ===");
benchmark({ cliente_id: "C00042" }, 1000);

// Test 2: Query sin shard key (broadcast)
print("\n=== BROADCAST QUERY ===");
benchmark({ total: { $gt: 900 } }, 1000);
```



## **ENTREGABLES DE LA PRÁCTICA**

Crea un documento (Markdown, PDF o Google Doc) con:

1. **Screenshots de `rs.status()`** mostrando tu Replica Set configurado
2. **Log del failover** con timestamps mostrando el tiempo de elección
3. **Output de `sh.status()`** mostrando tu cluster con sharding
4. **Output de `getShardDistribution()`** con los datos distribuidos
5. **Comparación de explain()** entre consultas targeted y broadcast
6. **Gráfica o tabla** comparando tiempos de las consultas del benchmark
7. **Respuestas a las preguntas** de los ejercicios marcados como 📝



## **LIMPIEZA**

```bash
# Detener y eliminar todos los contenedores
cd ~/mongodb-practica/replica-set
docker-compose down -v

cd ~/mongodb-practica/sharded-cluster
docker-compose down -v
```