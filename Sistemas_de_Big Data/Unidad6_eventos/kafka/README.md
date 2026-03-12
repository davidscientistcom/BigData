# 🐳 Docker Compose para Kafka

## Quick Start (KRaft - Moderno)

```bash
# 1. Crear carpeta
mkdir kafka-cluster
cd kafka-cluster

# 2. Copiar docker-compose.yml (modo KRaft, ver abajo)
# 3. Levantar
docker-compose up -d

# 4. Esperar 15 segundos (brokers se inicializan)
sleep 15

# 5. Crear topic
docker exec kafka1 kafka-topics --create \
  --topic events \
  --partitions 3 \
  --replication-factor 2 \
  --bootstrap-server localhost:9092

# ✅ ¡Listo! Sin ZooKeeper 🎉
```

---

## 📄 docker-compose.yml (KRaft - Recomendado)

```yaml
version: '3.8'

services:
  kafka1:
    image: confluentinc/cp-kafka:7.5.0
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka1:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_NODE_ID: 1
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka1:29093,2@kafka2:29093,3@kafka3:29093
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LOG_DIRS: /tmp/kraft-combined-logs
      CLUSTER_ID: IoTab_g3S9qt37B55K_H6w
    ports:
      - "9092:9092"
    networks:
      - kafka-network

  kafka2:
    image: confluentinc/cp-kafka:7.5.0
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka2:29092,PLAINTEXT_HOST://localhost:9093
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_NODE_ID: 2
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka1:29093,2@kafka2:29093,3@kafka3:29093
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LOG_DIRS: /tmp/kraft-combined-logs
      CLUSTER_ID: IoTab_g3S9qt37B55K_H6w
    ports:
      - "9093:9093"
    networks:
      - kafka-network

  kafka3:
    image: confluentinc/cp-kafka:7.5.0
    environment:
      KAFKA_BROKER_ID: 3
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka3:29092,PLAINTEXT_HOST://localhost:9094
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_NODE_ID: 3
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka1:29093,2@kafka2:29093,3@kafka3:29093
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LOG_DIRS: /tmp/kraft-combined-logs
      CLUSTER_ID: IoTab_g3S9qt37B55K_H6w
    ports:
      - "9094:9094"
    networks:
      - kafka-network

networks:
  kafka-network:
    driver: bridge
```

---

## 📦 docker-compose.yml (ZooKeeper - Legacy, solo si Kafka < 3.3)

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_SYNC_LIMIT: 2
      ZOOKEEPER_INIT_LIMIT: 5
    ports:
      - "2181:2181"
    networks:
      - kafka-network

  kafka1:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka1:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
    networks:
      - kafka-network

  kafka2:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9093:9093"
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka2:29093,PLAINTEXT_HOST://localhost:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
    networks:
      - kafka-network

  kafka3:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9094:9094"
    environment:
      KAFKA_BROKER_ID: 3
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka3:29094,PLAINTEXT_HOST://localhost:9094
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
    networks:
      - kafka-network

networks:
  kafka-network:
    driver: bridge
```

---

## 🔨 Comandos Útiles

### Gestión del Cluster

```bash
# Levantar
docker-compose up -d

# Detener (datos persisten)
docker-compose down

# Detener y limpiar TODOS los datos
docker-compose down -v

# Ver logs
docker-compose logs -f kafka1

# Restart un servicio
docker-compose restart kafka1
```

### Gestión de Topics

```bash
# Crear topic
docker exec kafka1 kafka-topics --create \
  --topic mi-topic \
  --partitions 3 \
  --replication-factor 2 \
  --bootstrap-server localhost:9092

# Listar topics
docker exec kafka1 kafka-topics --list \
  --bootstrap-server localhost:9092

# Describir topic (ver particiones, replicación)
docker exec kafka1 kafka-topics --describe \
  --topic mi-topic \
  --bootstrap-server localhost:9092

# Aumentar particiones (no se puede reducir!)
docker exec kafka1 kafka-topics --alter \
  --topic mi-topic \
  --partitions 5 \
  --bootstrap-server localhost:9092

# Borrar topic
docker exec kafka1 kafka-topics --delete \
  --topic mi-topic \
  --bootstrap-server localhost:9092
```

### Gestión de Consumer Groups

```bash
# Listar grupos
docker exec kafka1 kafka-consumer-groups --list \
  --bootstrap-server localhost:9092

# Ver detalles de un grupo
docker exec kafka1 kafka-consumer-groups --describe \
  --group mi-grupo \
  --bootstrap-server localhost:9092

# Resetear offset a earliest
docker exec kafka1 kafka-consumer-groups --reset-offsets \
  --group mi-grupo \
  --topic mi-topic \
  --to-earliest \
  --execute \
  --bootstrap-server localhost:9092

# Resetear offset a latest
docker exec kafka1 kafka-consumer-groups --reset-offsets \
  --group mi-grupo \
  --topic mi-topic \
  --to-latest \
  --execute \
  --bootstrap-server localhost:9092

# Resetear a offset específico
docker exec kafka1 kafka-consumer-groups --reset-offsets \
  --group mi-grupo \
  --topic mi-topic:0:100 \
  --execute \
  --bootstrap-server localhost:9092
```

### Producción/Consumo Manual

```bash
# Productor (escribe en consola)
docker exec -it kafka1 kafka-console-producer \
  --topic mi-topic \
  --bootstrap-server localhost:9092

# (Escribe, presiona Enter después de cada mensaje, Ctrl+C para salir)

# Consumidor (lee desde earliest)
docker exec -it kafka1 kafka-console-consumer \
  --topic mi-topic \
  --from-beginning \
  --bootstrap-server localhost:9092

# Consumidor (solo nuevos mensajes)
docker exec -it kafka1 kafka-console-consumer \
  --topic mi-topic \
  --bootstrap-server localhost:9092
```

---

## 🔍 Debugging

### Ver logs detallados
```bash
docker-compose logs zookeeper
docker-compose logs kafka1
docker-compose logs kafka-ui
```

### Conectar a un broker
```bash
# SSH al broker
docker exec -it kafka1 /bin/bash

# Una vez dentro:
kafka-broker-api-versions --bootstrap-server localhost:9092
```

### Ver estado del cluster
```bash
docker exec kafka1 zookeeper-shell localhost:2181 ls /brokers/ids
```

---

## 📊 Monitoreo con Kafka UI

Kafka UI está incluida en el docker-compose.yml arriba.

**URL:** http://localhost:8080

### Características:
- Ver topics y particiones
- Ver mensajes en tiempo real
- Ver consumer groups y offsets
- Enviar mensajes manualmente
- Monitor de métricas

---

## 🐛 Troubleshooting

### ❌ "Connection refused"
```
Causa: Kafka aún no está listo
Solución: Espera 15-30 segundos después de docker-compose up -d
```

### ❌ "Address already in use"
```
Causa: Ya tienes algo en los puertos 9092-9094
Solución:
  1. docker-compose down
  2. Cambia los puertos en docker-compose.yml
  3. docker-compose up -d
```

### ❌ "Topic does not exist"
```
Causa: No creaste el topic
Solución: Ejecuta el comando docker exec kafka1 kafka-topics --create...
```

### ❌ Los contenedores mueren inmediatamente
```
Causa: Falta de memoria o disco
Solución:
  docker system prune -a
  docker-compose down -v
  docker-compose up -d
```

---

## 💯 Configuración Producción-Ready

Para un setup más robusto:

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_SYNC_LIMIT: 5
      ZOOKEEPER_INIT_LIMIT: 10
      ZOOKEEPER_MAX_CLIENT_CNXNS: 0  # Sin límite
    volumes:
      - zk-data:/var/lib/zookeeper/data
      - zk-logs:/var/lib/zookeeper/log
    ports:
      - "2181:2181"
    networks:
      - kafka-network

  kafka1:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka1:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 2
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 3
      KAFKA_LOG_RETENTION_HOURS: 168
      KAFKA_LOG_SEGMENT_BYTES: 1073741824
      KAFKA_NUM_NETWORK_THREADS: 8
      KAFKA_NUM_IO_THREADS: 8
      KAFKA_SOCKET_SEND_BUFFER_BYTES: 102400
      KAFKA_SOCKET_RECEIVE_BUFFER_BYTES: 102400
      KAFKA_SOCKET_REQUEST_MAX_BYTES: 104857600
    volumes:
      - kafka1-data:/var/lib/kafka/data
    networks:
      - kafka-network
    restart: on-failure

volumes:
  zk-data:
  zk-logs:
  kafka1-data:

networks:
  kafka-network:
    driver: bridge
```

**Cambios:**
- `volumes` para persistencia
- `restart: on-failure` para recuperación automática
- Mejor configuración de threading y buffers
- Aumentado `ZOOKEEPER_MAX_CLIENT_CNXNS` (sin límite)

---

## 🎯 Próximos Pasos

1. **Levanta el cluster:** `docker-compose up -d`
2. **Espera:** 15-30 segundos
3. **Verifica:** `docker-compose logs kafka1` (busca "started")
4. **Crea un topic:** `docker exec kafka1 kafka-topics --create...`
5. **Corre los ejemplos Python** de la sección "Ejemplos Prácticos"
6. **Monitorea:** Abre http://localhost:8080 (Kafka UI)

---

## 📚 Recursos

- [Confluent Kafka Docker](https://hub.docker.com/r/confluentinc/cp-kafka)
- [Kafka Topics Command](https://kafka.apache.org/documentation/#basic_ops_add_topic)
- [Kafka Consumer Groups](https://kafka.apache.org/documentation/#consumerconfigs)
- [Kafka UI GitHub](https://github.com/provectus/kafka-ui)
