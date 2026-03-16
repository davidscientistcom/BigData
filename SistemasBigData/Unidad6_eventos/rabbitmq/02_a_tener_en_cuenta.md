# RabbitMQ - Advertencias
## Índice
1. ¿Se pueden perder mensajes?
2. Modos de confirmación: Auto-ACK vs Manual ACK
3. Persistencia y Durabilidad: las 3 capas de protección
4. Prefetch (QoS): rendimiento vs seguridad
5. Requeue: bucles infinitos y reentregas
6. Publisher Confirms: ¿llegó el mensaje al broker?
7. Dead Letter Queue (DLQ): mensajes no entregables
8. Problemas comunes y cómo evitarlos
9. Checklist de producción



## 1. ¿Se pueden perder mensajes?

**SÍ. Y de varias formas**.[1][2]

### Escenarios de pérdida de mensajes

| Escenario | ¿Se pierde el mensaje? | Solución |
|---|---|---|
| Producer envía mensaje y RabbitMQ crashea antes de guardarlo | ✅ SÍ | Usar **Publisher Confirms** |
| RabbitMQ entrega mensaje al consumer, consumer crashea sin procesarlo | ✅ SÍ | Usar **Manual ACK** (no auto-ack) |
| RabbitMQ reinicia y la cola no era durable | ✅ SÍ | Declarar colas **durable=True** |
| RabbitMQ reinicia y el mensaje no era persistente | ✅ SÍ | Publicar con **delivery_mode=2** (persistent) |
| El exchange no tiene colas vinculadas (binding) | ✅ SÍ (descartado silenciosamente) | Usar **Dead Letter Exchange** |
| Mensaje expira por TTL antes de ser consumido | ✅ SÍ (o va a DLQ si está configurado) | Ajustar TTL o añadir más consumers |

**RabbitMQ NO garantiza entrega por defecto.** Tienes que activar explícitamente los mecanismos de seguridad.[2][3]



## 2. Modos de confirmación: Auto-ACK vs Manual ACK

### Auto-ACK (automático) ⚠️

**Cómo funciona:** RabbitMQ considera el mensaje **entregado con éxito** en el momento que lo escribe en el socket TCP del consumer.[1]

```python
# Auto-ACK: el mensaje se borra ANTES de procesarlo
channel.basic_consume(queue='cola', on_message_callback=procesar, auto_ack=True)
```

**Problemas:**

- Si el consumer crashea **después de recibir** el mensaje pero **antes de procesarlo**, el mensaje **se pierde para siempre**.[1]
- Si el consumer es lento, RabbitMQ le envía mensajes sin límite → **OOM (Out of Memory)**.[1]
- Se llama también **"fire-and-forget"** (dispara y olvida).

**Cuándo usarlo:** solo en sistemas donde **perder mensajes no importa** (logs no críticos, métricas opcionales).[1]



### Manual ACK (recomendado) ✅

**Cómo funciona:** RabbitMQ **NO borra** el mensaje hasta que el consumer confirme explícitamente que lo procesó.[1]

```python
def procesar(ch, method, properties, body):
    try:
        # Procesar el mensaje (lógica de negocio)
        resultado = hacer_algo_con(body)
        
        # SOLO SI todo va bien, confirmamos
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"Error: {e}")
        # Rechazar y reencolar (o enviar a DLQ)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

channel.basic_consume(queue='cola', on_message_callback=procesar, auto_ack=False)
```

**Ventajas:**

- Si el consumer crashea, RabbitMQ **reencola automáticamente** el mensaje.[1]
- Permite control total sobre cuándo se considera "procesado" un mensaje.
- Se puede combinar con prefetch para controlar la carga.

**Regla de oro:** **SIEMPRE usa manual ACK en producción**.[4][2]



### Comandos de ACK/NACK

| Método | Acción | Parámetro `requeue` | Uso típico |
|---|---|---|---|
| `basic_ack()` | Confirma procesamiento exitoso | — | Mensaje procesado correctamente |
| `basic_reject()` | Rechaza **un solo** mensaje | `True` = reencola / `False` = descarta | Rechazo simple |
| `basic_nack()` | Rechaza **uno o múltiples** mensajes | `True` = reencola / `False` = descarta | Rechazo en lote |

```python
# Confirmar un mensaje (OK)
ch.basic_ack(delivery_tag=method.delivery_tag)

# Rechazar y reencolar (para que otro consumer lo intente)
ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

# Rechazar y descartar (o enviar a DLQ)
ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
```



## 3. Persistencia y Durabilidad: las 3 capas de protección

Para que un mensaje **sobreviva a un reinicio de RabbitMQ**, necesitas **LAS TRES cosas**:[3][5][2]

### ① Cola durable

```python
channel.queue_declare(queue='mi_cola', durable=True)
```

Sin esto, la cola **desaparece** al reiniciar RabbitMQ.[3]

### ② Mensaje persistente

```python
channel.basic_publish(
    exchange='',
    routing_key='mi_cola',
    body='Mensaje importante',
    properties=pika.BasicProperties(
        delivery_mode=2,  # 1=transient, 2=persistent
    )
)
```

Sin esto, aunque la cola sea durable, **los mensajes se pierden** al reiniciar.[5][2]

### ③ Exchange durable (si usas exchange custom)

```python
channel.exchange_declare(exchange='mi_exchange', exchange_type='direct', durable=True)
```

Sin esto, el exchange desaparece al reiniciar.[5]



### ⚠️ Ventana de pérdida inevitable

**Incluso con las 3 capas activadas**, hay una pequeña ventana de tiempo donde RabbitMQ puede perder mensajes:[6][2]

- RabbitMQ escribe a disco en **lotes** cada pocos cientos de milisegundos (no uno a uno).[2][6]
- Si crashea **entre que acepta el mensaje y lo escribe a disco**, se pierde.

**Solución:** Usar **Publisher Confirms** (siguiente sección).



### Coste de la persistencia

Escribir a disco es **100-1000x más lento** que escribir en RAM. En sistemas de alto throughput, puedes tener:[6]

- **Mensajes críticos**: persistentes (pagos, pedidos).
- **Mensajes no críticos**: transient (logs, métricas en tiempo real).



## 4. Prefetch (QoS): rendimiento vs seguridad

### ¿Qué es el prefetch?

Es el **número máximo de mensajes sin ACK** que RabbitMQ puede enviar a un consumer al mismo tiempo.[1]

```python
# Prefetch = 10: el consumer puede tener hasta 10 mensajes "en vuelo"
channel.basic_qos(prefetch_count=10)
```

### Comportamiento

- Si hay 10 mensajes sin ACK, RabbitMQ **NO envía más** hasta que el consumer confirme al menos uno.[1]
- Con `prefetch_count=0` (sin límite), RabbitMQ envía **todos los mensajes disponibles** → riesgo de **OOM**.[1]



### ¿Qué valor usar?

| Escenario | Prefetch recomendado | Razón |
|---|---|---|
| **Muchos consumers, procesamiento corto** | 100-300 [1] | Maximiza throughput sin saturar |
| **Muchos consumers, procesamiento largo** | 1 [7] | Distribuye carga equitativamente |
| **Un solo consumer, procesamiento rápido** | 100-500 | Evita latencia de red |
| **Máxima seguridad (no perder nada)** | 1 | Cada mensaje se procesa antes de pedir el siguiente |

**Valores mayores a 300 tienen retornos decrecientes**.[1]



### Problema: Requeue con prefetch alto

**Escenario peligroso:**

1. Consumer tiene `prefetch=100`.
2. Recibe 100 mensajes.
3. Consumer crashea **sin hacer ACK de ninguno**.
4. RabbitMQ reencola los 100 mensajes.
5. Si todos los consumers crashean por el mismo error → **bucle infinito de requeue**.[8][1]

**Solución:** Implementar contador de reintentos:

```python
def procesar(ch, method, properties, body):
    # RabbitMQ marca con 'redelivered=True' si es un reenvío
    if method.redelivered:
        print("⚠️ Mensaje reenviado, posible error persistente")
        # Opción 1: enviarlo a DLQ después de N intentos
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    else:
        try:
            hacer_algo(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            # Primera vez que falla: reencolar
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
```



## 5. Requeue: bucles infinitos y reentregas

### ¿Cuándo se reencola automáticamente?

RabbitMQ **automáticamente reencola** mensajes sin ACK cuando:[1]

- El consumer se desconecta (TCP connection loss).
- El canal (channel) se cierra.
- El proceso del consumer crashea.

**Importante:** Detectar que un consumer se cayó **toma tiempo** (varios segundos).[1]



### Problema: Bucle de requeue

Si un mensaje **siempre causa un error** (por ejemplo, JSON malformado), y todos los consumers hacen `requeue=True`, el mensaje circula infinitamente consumiendo CPU y red.[1]

**Solución 1: Contador de reintentos en headers**

```python
def procesar(ch, method, properties, body):
    headers = properties.headers or {}
    retry_count = headers.get('x-retry-count', 0)
    
    try:
        hacer_algo(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        if retry_count < 3:
            # Reintentar: incrementar contador y reencolar
            headers['x-retry-count'] = retry_count + 1
            ch.basic_publish(
                exchange='',
                routing_key='mi_cola',
                body=body,
                properties=pika.BasicProperties(headers=headers)
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)  # Eliminar el original
        else:
            # Ya se intentó 3 veces: mandar a DLQ
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
```

**Solución 2: Usar Dead Letter Exchange (DLQ)** — ver sección 7.



## 6. Publisher Confirms: ¿llegó el mensaje al broker?

### El problema

Cuando haces `channel.basic_publish()`, el método **retorna inmediatamente**. Pero eso **NO garantiza** que RabbitMQ haya recibido el mensaje:[2][1]

- Puede haberse perdido en la red.
- RabbitMQ puede haber crasheado antes de escribirlo a disco.

### La solución: Publisher Confirms

Es un **ACK del broker al producer** confirmando que el mensaje fue recibido y almacenado.[1]

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Activar modo confirm en el canal
channel.confirm_delivery()

try:
    channel.basic_publish(
        exchange='',
        routing_key='mi_cola',
        body='Mensaje crítico',
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
        mandatory=True  # falla si no hay cola que lo reciba
    )
    print("✅ RabbitMQ confirmó recepción")
except pika.exceptions.UnroutableError:
    print("❌ No hay cola vinculada al routing key")
except pika.exceptions.NackError:
    print("❌ RabbitMQ rechazó el mensaje (error interno)")
```

### Cuándo se confirma un mensaje

- **Mensaje no persistente**: cuando lo acepta el exchange.[1]
- **Mensaje persistente + cola durable**: cuando **se escribe a disco**.[1]
- **Quorum queues**: cuando un quorum de réplicas lo confirma.[1]

**Latencia:** Con mensajes persistentes, el confirm puede tardar **cientos de milisegundos** porque RabbitMQ escribe a disco en lotes.[1]

**Recomendación:** Publicar en lotes y procesar confirms de forma asíncrona.[1]



## 7. Dead Letter Queue (DLQ): mensajes no entregables

### ¿Qué es?

Una **cola especial** donde van los mensajes que no se pudieron entregar:[1]

- Mensaje rechazado con `requeue=False`.
- Mensaje expiró por TTL.
- Cola alcanzó su límite de tamaño.
- Consumer rechazó el mensaje múltiples veces.

```python
# Cola principal con DLX configurado
channel.queue_declare(
    queue='cola_principal',
    durable=True,
    arguments={
        'x-dead-letter-exchange': 'dlx_exchange',      # Exchange para mensajes fallidos
        'x-dead-letter-routing-key': 'failed_messages', # Routing key en DLX
        'x-message-ttl': 60000  # Mensajes expiran en 60 segundos
    }
)

# Declarar el DLX y la cola de destino
channel.exchange_declare(exchange='dlx_exchange', exchange_type='direct', durable=True)
channel.queue_declare(queue='cola_dlq', durable=True)
channel.queue_bind(exchange='dlx_exchange', queue='cola_dlq', routing_key='failed_messages')
```

**Consumer para la DLQ (monitoreo/alertas):**

```python
def procesar_fallidos(ch, method, properties, body):
    print(f"[DLQ] Mensaje fallido: {body.decode()}")
    # Enviar alerta, registrar en base de datos, etc.
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='cola_dlq', on_message_callback=procesar_fallidos, auto_ack=False)
```



## 8. Problemas comunes y cómo evitarlos

### ① "Unknown delivery tag"

**Error:** `PRECONDITION_FAILED - unknown delivery tag 100`[1]

**Causas:**

- Hacer ACK del mismo mensaje dos veces.
- Hacer ACK en un **canal diferente** al que recibió el mensaje.
- Hacer ACK de un mensaje que ya se reencoló (porque la conexión se cerró).

**Solución:** Asegúrate de hacer ACK **solo una vez** y **en el mismo canal**.



### ② Consumers saturados (OOM)

**Síntoma:** El consumer se queda sin memoria y el OS lo mata.

**Causa:** `auto_ack=True` o `prefetch_count=0` → RabbitMQ envía miles de mensajes sin esperar confirmación.[1]

**Solución:**

```python
channel.basic_qos(prefetch_count=100)  # Limitar mensajes en vuelo
channel.basic_consume(queue='cola', on_message_callback=procesar, auto_ack=False)
```



### ③ Mensajes duplicados

**Escenario:** Consumer procesa un mensaje pero crashea **antes de hacer ACK** → RabbitMQ lo reencola → otro consumer lo procesa de nuevo.[1]

**Solución:** Implementar **idempotencia**:

```python
mensajes_procesados = set()  # En producción: Redis o DB

def procesar(ch, method, properties, body):
    msg_id = properties.message_id or body.decode()
    
    if msg_id in mensajes_procesados:
        print(f"⚠️ Mensaje {msg_id} ya procesado, ignorando")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    
    hacer_algo(body)
    mensajes_procesados.add(msg_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)
```



### ④ Orden de mensajes no garantizado

**Por defecto, RabbitMQ NO garantiza orden estricto** en estos casos:

- Múltiples consumers en la misma cola: cada uno recibe mensajes diferentes.
- Requeue: el mensaje se reencola pero puede no volver a su posición original.[1]
- Publisher confirms asíncronos: pueden llegar en orden diferente.[1]

**Solución si necesitas orden:**

- Usar `prefetch_count=1` con **un solo consumer**.
- Usar **Single Active Consumer** (característica avanzada de RabbitMQ).
- Usar **Quorum Queues** en lugar de colas clásicas.



### ⑤ Pérdida de mensajes "silenciosa"

**Escenario:** Publicas un mensaje pero el exchange no tiene ninguna cola vinculada → RabbitMQ lo **descarta sin avisar**.

**Solución:** Usar `mandatory=True` al publicar:

```python
try:
    channel.basic_publish(
        exchange='mi_exchange',
        routing_key='clave_inexistente',
        body='Mensaje',
        mandatory=True  # Falla si no hay binding
    )
except pika.exceptions.UnroutableError:
    print("❌ No hay cola para este mensaje")
```



## 9. Checklist de producción

Antes de llevar tu sistema RabbitMQ a producción, verifica:

- [ ] **Colas durables**: `durable=True` en todas las colas críticas.
- [ ] **Mensajes persistentes**: `delivery_mode=2` en todos los mensajes importantes.
- [ ] **Manual ACK**: `auto_ack=False` en todos los consumers.
- [ ] **Prefetch configurado**: valores entre 1-300 según tu caso.[7][1]
- [ ] **Publisher Confirms activado**: `channel.confirm_delivery()` en producers críticos.
- [ ] **Dead Letter Queue**: configurado en colas principales.
- [ ] **Manejo de reintentos**: contador de redeliveries o headers `x-retry-count`.
- [ ] **Idempotencia**: consumers preparados para recibir mensajes duplicados.
- [ ] **Monitoreo**: alertas sobre tamaño de colas, tasa de errores, mensajes en DLQ.
- [ ] **Logging**: registrar `delivery_tag`, `redelivered`, `message_id` para debug.
- [ ] **Timeouts**: configurar `heartbeat` en conexiones (default 60s).
- [ ] **High Availability**: usar quorum queues o clustering en producción.



## Resumen de garantías

| Configuración | Pérdida por crash de consumer | Pérdida por crash de RabbitMQ | Pérdida por red |
|---|---|---|---|
| `auto_ack=True` | ✅ **SÍ** | ✅ **SÍ** | ✅ **SÍ** |
| Manual ACK | ❌ NO | ✅ **SÍ** | ✅ **SÍ** |
| Manual ACK + Durable Queue | ❌ NO | ✅ **SÍ** | ✅ **SÍ** |
| Manual ACK + Durable + Persistent | ❌ NO | ⚠️ Ventana pequeña | ✅ **SÍ** |
| **Manual ACK + Durable + Persistent + Publisher Confirms** | ❌ NO | ❌ NO | ❌ NO |

La última fila es **la configuración de máxima seguridad**.[2]

**Referencias:**[4][7][3][5][6][2][1]

Fuentes
[1] Consumer Acknowledgements and Publisher Confirms - RabbitMQ https://www.rabbitmq.com/docs/confirms
[2] Reliable Messaging with RabbitMQ: Acknowledgments, Durability ... https://widhianbramantya.com/rabbitmq/reliable-messaging-with-rabbitmq-acknowledgments-durability-and-persistence/3/
[3] Persistence Documentation https://www.cloudamqp.com/docs/persistence.html
[4] RabbitMQ Message Loss https://drdroid.io/stack-diagnosis/rabbitmq-message-loss
[5] RabbitMQ - Persistency vs Durability · I Pity the foo()! - Blog https://asafdav2.github.io/2017/rabbit-mq-persistentcy-vs-durability/
[6] Configuring RabbitMQ Persistence https://support.huaweicloud.com/eu/usermanual-rabbitmq/rabbitmq_ug_0010.html
[7] Configuring RabbitMQ Message Prefetch - 华为云 https://support.huaweicloud.com/eu/usermanual-rabbitmq/rabbitmq_ug_0013.html
[8] RabbitMQ Single Active Consumer losing message order ... https://stackoverflow.com/questions/76563078/rabbitmq-single-active-consumer-losing-message-order-on-consumer-shutdown
[9] Persistence Configuration https://www.rabbitmq.com/docs/persistence-conf
[10] Best practices for message durability and reliability in Amazon MQ ... https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/best-practices-message-reliability.html
[11] In RabbitMQ, how to handle the conflict between prefetch and 'redelivered' https://stackoverflow.com/questions/47707448/in-rabbitmq-how-to-handle-the-conflict-between-prefetch-and-redelivered
[12] FAQ: How to persist messages during RabbitMQ broker restart? https://www.cloudamqp.com/blog/how-to-persist-messages-during-RabbitMQ-broker-restart.html
[13] Configuring RabbitMQ Message Prefetch - 华为云 https://support.huaweicloud.com/intl/en-us/usermanual-rabbitmq/rabbitmq_ug_0013.html
[14] Persistence and durability #5119 - rabbitmq rabbitmq-server https://github.com/rabbitmq/rabbitmq-server/discussions/5119
[15] Configuring RabbitMQ Persistence - 华为云 - Huawei Cloud https://support.huaweicloud.com/intl/en-us/usermanual-rabbitmq/rabbitmq_ug_0010.html
