# RabbitMQ con Python — Guía Completa desde Cero

## Índice
1. ¿Qué problema resuelve RabbitMQ?
2. ¿Qué es un Message Broker?
3. Los 3 actores: Producer, Queue y Consumer
4. ¿Qué es una Cola (Queue)?
5. ¿Qué es un Exchange?
6. ¿Qué es un Binding y una Routing Key?
7. Flujo completo de un mensaje
8. Los 4 tipos de Exchange — explicados en detalle
   - 8.1 Default Exchange (sin nombre)
   - 8.2 Direct Exchange
   - 8.3 Fanout Exchange
   - 8.4 Topic Exchange
   - 8.5 Headers Exchange
9. Dead Letter Exchange
10. Instalación y entorno
11. Ejemplos completos en Python



## 1. ¿Qué problema resuelve RabbitMQ?

Imagina que tienes una aplicación web donde los usuarios suben fotos. Cada foto hay que procesarla (redimensionar, aplicar filtros, guardarla en disco). Si haces ese proceso **en el mismo hilo que la petición HTTP**, el usuario espera 10 segundos. Eso es terrible.

La solución es **desacoplar** el trabajo: la web recibe la petición, la mete en una cola, y **otro proceso independiente** (incluso en otra máquina) la procesa cuando pueda. El usuario recibe respuesta inmediata. RabbitMQ es quien gestiona esa cola de mensajes.[1]

Esto también se usa masivamente en Big Data: un sensor manda miles de lecturas por segundo → RabbitMQ las encola → varios workers las procesan en paralelo sin perder ninguna.



## 2. ¿Qué es un Message Broker?

Un **Message Broker** es un intermediario de mensajes. Es como una **oficina de correos**:[1]

- El **remitente** (producer) deposita una carta (mensaje).
- La **oficina** (RabbitMQ) la almacena y decide a qué buzón va.
- El **destinatario** (consumer) recoge la carta cuando quiere.

Lo clave es que el remitente **no sabe nada** del destinatario. No le importa si está disponible, si son 1 o 100 los que leen, ni cuándo lo hacen. Eso es el **desacoplamiento**.

RabbitMQ implementa el protocolo **AMQP 0-9-1** (Advanced Message Queuing Protocol).[1]



## 3. Los 3 actores

| Actor | Rol | Analogía |
|---|---|---|
| **Producer** | Crea y envía mensajes | El remitente de la carta |
| **Queue** | Almacena mensajes hasta que se consumen | El buzón de correos |
| **Consumer** | Recibe y procesa mensajes | El destinatario |

Estos tres actores **no tienen por qué estar en la misma máquina** — de hecho, en sistemas reales nunca lo están.[1]



## 4. ¿Qué es una Cola (Queue)?

Una **Queue** es un **buffer de mensajes** almacenado en RabbitMQ. Funciona como una fila de supermercado: el primero en entrar es el primero en salir (**FIFO — First In, First Out**).[1]

Características importantes:

- Una cola puede recibir mensajes de **múltiples producers**.
- Una cola puede ser consumida por **múltiples consumers** (los mensajes se reparten entre ellos, no se duplican).
- Los mensajes **persisten en la cola** hasta que un consumer los procesa.
- Está limitada solo por la memoria RAM y el disco del servidor.

**Tipos de colas según durabilidad:**

- **Durable**: sobrevive a un reinicio de RabbitMQ. Los mensajes no se pierden.
- **Transient/Temporary**: desaparece si RabbitMQ se reinicia.
- **Auto-delete**: se borra automáticamente cuando el último consumer se desconecta.[2]

```python
# Cola durable (persistente)
channel.queue_declare(queue='tareas_importantes', durable=True)

# Cola temporal (se crea con nombre aleatorio, exclusiva para esta conexión)
result = channel.queue_declare(queue='', exclusive=True)
nombre_cola = result.method.queue  # RabbitMQ le da un nombre aleatorio
```



## 5. ¿Qué es un Exchange?

Aquí está el concepto más importante y que más confunde al principio.

**Un mensaje en RabbitMQ NUNCA va directamente a una cola.**[2]

El producer siempre envía el mensaje a un **Exchange** (intercambiador). El exchange es el encargado de decidir a qué cola o colas reenviar el mensaje, siguiendo unas reglas que tú defines.

Piénsalo como un **clasificador postal**: recibe todos los paquetes y los distribuye a los buzones correctos según la dirección.

```
Producer → Exchange → [Cola A]
                   → [Cola B]
                   → [Cola C]
```

¿Por qué existe esto? Porque así el producer no necesita saber cuántas colas hay ni cómo se llaman. Solo habla con el exchange y él se encarga del resto.[2]



## 6. ¿Qué es un Binding y una Routing Key?

Dos conceptos que van siempre juntos:

- **Binding**: es el **enlace** que conecta un Exchange con una Queue. Sin binding, los mensajes no llegan a ninguna cola.[2]
- **Routing Key**: es una **etiqueta** (string) que el producer pone en el mensaje. El exchange la usa para decidir a qué colas enviar el mensaje (según el tipo de exchange).[2]

```
Exchange (pdf_events)
    │
    ├── Binding: routing_key="pdf_crear"  →  Cola: crear_pdf_queue
    └── Binding: routing_key="pdf_log"   →  Cola: log_pdf_queue
```



## 7. Flujo completo de un mensaje

Este es el flujo exacto que sigue cada mensaje:[2]

1. El **Producer** crea un mensaje y lo publica en el **Exchange** con una **Routing Key**.
2. El **Exchange** recibe el mensaje y evalúa sus **Bindings**.
3. Según el **tipo de exchange**, enruta el mensaje a 1 o más **Queues**.
4. El mensaje **se queda en la cola** hasta que un Consumer lo procese.
5. El **Consumer** recoge el mensaje, lo procesa y envía un **ACK** (confirmación) a RabbitMQ.
6. RabbitMQ elimina el mensaje de la cola al recibir el ACK.



## 8. Los 4 Tipos de Exchange

### 8.1 Default Exchange (exchange sin nombre `""`)

Es el exchange más sencillo. Predefinido por RabbitMQ, sin nombre. Cuando lo usas, la **routing key debe ser exactamente el nombre de la cola**. Es como si el mensaje fuera "directamente" a la cola (aunque técnicamente sigue pasando por un exchange).[2]

```python
# Con el default exchange no necesitas declarar un exchange
channel.queue_declare(queue='hello')
channel.basic_publish(
    exchange='',           # string vacío = default exchange
    routing_key='hello',   # debe ser el nombre exacto de la cola
    body='Hola Mundo'
)
```

**Cuándo usarlo:** pruebas rápidas, ejemplos simples, cuando solo tienes una cola.



### 8.2 Direct Exchange

Enruta el mensaje a **la cola cuya binding key coincide exactamente** con la routing key del mensaje.[2]

**Ejemplo real:** sistema de logs donde queremos que los errores críticos vayan a una cola especial y los informativos a otra.

```
Exchange: logs_directos
    ├── binding_key="error"   →  Cola: cola_errores
    ├── binding_key="warning" →  Cola: cola_warnings
    └── binding_key="info"    →  Cola: cola_info
```

```python
# ---- PRODUCER ----
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar el exchange de tipo direct
channel.exchange_declare(exchange='logs_directos', exchange_type='direct')

# Enviar un error crítico
channel.basic_publish(
    exchange='logs_directos',
    routing_key='error',     # solo llegará a la cola vinculada con "error"
    body='ERROR: Base de datos no disponible'
)

# Enviar un log informativo
channel.basic_publish(
    exchange='logs_directos',
    routing_key='info',
    body='INFO: Usuario admin ha iniciado sesión'
)
connection.close()
```

```python
# ---- CONSUMER para errores ----
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs_directos', exchange_type='direct')

# Crear cola y vincularla al exchange con binding_key='error'
result = channel.queue_declare(queue='', exclusive=True)
cola = result.method.queue
channel.queue_bind(exchange='logs_directos', queue=cola, routing_key='error')

def procesar(ch, method, properties, body):
    print(f"[!] ALERTA: {body.decode()}")

channel.basic_consume(queue=cola, on_message_callback=procesar, auto_ack=True)
print('Esperando errores...')
channel.start_consuming()
```

**Cuándo usarlo:** cuando necesitas clasificar mensajes por categorías bien definidas y fijas.



### 8.3 Fanout Exchange

Ignora completamente la routing key y **envía una copia del mensaje a TODAS las colas** vinculadas al exchange. Es un **broadcast** puro.[2]

**Ejemplo real:** sistema de notificaciones. Cuando un usuario hace un pedido, queremos notificarlo simultáneamente al sistema de email, al sistema de SMS y al sistema de historial.

```
Exchange: pedido_realizado (fanout)
    ├──  Cola: cola_emails     → servicio de email
    ├──  Cola: cola_sms        → servicio de SMS
    └──  Cola: cola_historial  → servicio de historial
```

```python
# ---- PRODUCER ----
import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='pedido_realizado', exchange_type='fanout')

pedido = {'id': 123, 'producto': 'Laptop', 'usuario': 'juan@email.com'}

channel.basic_publish(
    exchange='pedido_realizado',
    routing_key='',          # se ignora en fanout, puede dejarse vacío
    body=json.dumps(pedido)
)
print("Pedido enviado a todos los servicios")
connection.close()
```

```python
# ---- CONSUMER email (igual estructura para SMS e historial) ----
import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='pedido_realizado', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
cola = result.method.queue
# En fanout NO se especifica routing_key en el binding
channel.queue_bind(exchange='pedido_realizado', queue=cola)

def enviar_email(ch, method, properties, body):
    pedido = json.loads(body)
    print(f"[EMAIL] Enviando confirmación a {pedido['usuario']}")

channel.basic_consume(queue=cola, on_message_callback=enviar_email, auto_ack=True)
channel.start_consuming()
```

**Cuándo usarlo:** notificaciones broadcast, sincronización de cachés, difusión de eventos a múltiples sistemas.



### 8.4 Topic Exchange

Es el más potente y flexible. Enruta según **patrones con wildcards** aplicados a la routing key.[2]

**Reglas de los patrones:**
- La routing key es una cadena de palabras separadas por **puntos**: `pais.ciudad.tipo`
- `*` → sustituye **exactamente una** palabra
- `#` → sustituye **cero o más** palabras

**Ejemplo real:** red de sensores meteorológicos en distintas ciudades y países.

```
Exchange: sensores (topic)
    ├── binding: "españa.#"         →  Cola: todos_españa
    ├── binding: "*.*.temperatura"  →  Cola: todas_temperaturas
    └── binding: "españa.madrid.*" →  Cola: madrid_todos
```

| Routing Key del mensaje | ¿A qué colas llega? |
|---|---|
| `españa.madrid.temperatura` | todos_españa ✅  todas_temperaturas ✅  madrid_todos ✅ |
| `españa.barcelona.humedad` | todos_españa ✅  madrid_todos ❌ |
| `francia.paris.temperatura` | todas_temperaturas ✅ |
| `españa.madrid.presion` | todos_españa ✅  madrid_todos ✅ |

```python
# ---- PRODUCER ----
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='sensores', exchange_type='topic')

# Lectura de temperatura en Madrid
channel.basic_publish(
    exchange='sensores',
    routing_key='españa.madrid.temperatura',
    body='38.5'
)

# Lectura de humedad en Barcelona
channel.basic_publish(
    exchange='sensores',
    routing_key='españa.barcelona.humedad',
    body='72'
)
connection.close()
```

```python
# ---- CONSUMER interesado en TODA España ----
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='sensores', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
cola = result.method.queue

# Este consumer recibe CUALQUIER mensaje que empiece por "españa."
channel.queue_bind(exchange='sensores', queue=cola, routing_key='españa.#')

def procesar(ch, method, properties, body):
    print(f"[España] Clave: {method.routing_key} | Valor: {body.decode()}")

channel.basic_consume(queue=cola, on_message_callback=procesar, auto_ack=True)
channel.start_consuming()
```

```python
# ---- CONSUMER interesado solo en temperaturas (de cualquier lugar) ----
result2 = channel.queue_declare(queue='', exclusive=True)
cola2 = result2.method.queue
channel.queue_bind(exchange='sensores', queue=cola2, routing_key='*.*.temperatura')
```

**Cuándo usarlo:** pipelines de Big Data con múltiples dimensiones de filtrado, telemetría geolocalizada, sistemas de logging avanzados.



### 8.5 Headers Exchange

En lugar de usar la routing key, enruta basándose en las **cabeceras (headers)** del mensaje. El binding define qué headers debe tener el mensaje para llegar a esa cola.[2]

El parámetro clave es `x-match`:
- `x-match = all` → **todos** los headers del binding deben coincidir (AND lógico)
- `x-match = any` → **basta con que uno** coincida (OR lógico)

**Ejemplo real:** procesador de documentos que trata diferente un PDF de informe vs un ZIP de logs.

```
Exchange: procesador_docs (headers)
    ├── Cola A: binding {format=pdf, type=report, x-match=all}
    ├── Cola B: binding {format=pdf, type=log,    x-match=any}
    └── Cola C: binding {format=zip, type=report, x-match=all}
```

| Mensaje con headers | Cola A | Cola B | Cola C |
|---|---|---|---|
| `format=pdf, type=report` | ✅ (ambos coinciden) | ✅ (format=pdf coincide) | ❌ |
| `format=pdf` | ❌ (falta type) | ✅ (format=pdf coincide) | ❌ |
| `format=zip, type=log` | ❌ | ✅ (type=log coincide) | ❌ (falta type=report) |

```python
# ---- PRODUCER ----
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='procesador_docs', exchange_type='headers')

# Enviar un informe PDF
channel.basic_publish(
    exchange='procesador_docs',
    routing_key='',   # se ignora en headers exchange
    properties=pika.BasicProperties(
        headers={'format': 'pdf', 'type': 'report'}
    ),
    body='Contenido del informe trimestral'
)
connection.close()
```

```python
# ---- CONSUMER para PDFs de tipo report ----
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='procesador_docs', exchange_type='headers')

result = channel.queue_declare(queue='', exclusive=True)
cola = result.method.queue

# Binding con condición: TODOS los headers deben coincidir
channel.queue_bind(
    exchange='procesador_docs',
    queue=cola,
    arguments={
        'x-match': 'all',   # AND: format=pdf AND type=report
        'format': 'pdf',
        'type': 'report'
    }
)

def procesar_informe(ch, method, properties, body):
    print(f"[PDF Report] Procesando: {body.decode()}")

channel.basic_consume(queue=cola, on_message_callback=procesar_informe, auto_ack=True)
channel.start_consuming()
```

**Cuándo usarlo:** cuando el criterio de enrutado es multidimensional y no encaja bien en una string de routing key.



## 9. Dead Letter Exchange

¿Qué pasa si ninguna cola recibe el mensaje? Por defecto, **RabbitMQ lo descarta silenciosamente**. Para evitar perder mensajes, existe el **Dead Letter Exchange (DLX)**: una cola especial donde van los mensajes no entregables (por TTL expirado, cola llena, o mensaje rechazado).[2]

```python
# Cola normal con DLX configurado
channel.queue_declare(
    queue='cola_principal',
    arguments={
        'x-dead-letter-exchange': 'dead_letters',  # si falla, va aquí
        'x-message-ttl': 60000  # mensaje expira en 60 segundos
    }
)
```



## 10. Instalación y entorno

**RabbitMQ con Docker (recomendado para desarrollo):**

```bash
# Levanta RabbitMQ con panel de administración web
docker run -d --name rabbitmq \
  -p 5672:5672 \    # puerto AMQP (conexiones Python)
  -p 15672:15672 \  # puerto panel web
  rabbitmq:3-management
```

Panel web disponible en: `http://localhost:15672` (usuario: `guest`, contraseña: `guest`)

**Librería Python:**
```bash
pip install pika
```



## 11. Resumen visual de los Exchange Types

| Tipo | Criterio de enrutado | Wildcard | Nº colas destino | Caso de uso típico |
|---|---|---|---|---|
| **Default** `""` | routing_key = nombre de la cola | No | 1 | Pruebas, ejemplos simples |
| **Direct** | routing_key exacta | No | 1 (o más con misma key) | Logs por nivel, tareas por tipo |
| **Fanout** | Ninguno (broadcast) | — | Todas las vinculadas | Notificaciones a múltiples servicios |
| **Topic** | Patrón con `.`, `*`, `#` | `*` y `#` | 1 o más (por coincidencia) | Telemetría, pipelines multi-dimensión |
| **Headers** | Cabeceras del mensaje (AND/OR) | No | 1 o más (por headers) | Routing por metadatos complejos |