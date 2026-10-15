
# 🐰 RabbitMQ con Python — Guía de Prácticas

## Índice de prácticas

| Nº | Título                          | Dificultad | Tiempo | Prereq. |
|----|---------------------------------|:----------:|:------:|:-------:|
| P1 | Hello World                     | ⭐         | 20 min | —       |
| P2 | Work Queue y Distribución       | ⭐⭐       | 30 min | P1      |
| P3 | Direct Exchange                 | ⭐⭐       | 30 min | P2      |
| P4 | Fanout Exchange                 | ⭐⭐       | 25 min | P3      |
| P5 | Topic Exchange                  | ⭐⭐⭐     | 35 min | P4      |
| P6 | Dead Letter Queue               | ⭐⭐⭐     | 35 min | P3      |
| P7 | Publisher Confirms e Idempotencia | ⭐⭐⭐   | 30 min | P6      |
| P8 | Proyecto Integrador             | ⭐⭐⭐⭐   | 60 min | P1–P7   |

---

## Preparación común (hacer ANTES de cualquier práctica)

```bash
# Levantar RabbitMQ
docker run -d --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3-management

# Instalar librería Python
pip install pika

# Panel de administración → http://localhost:15672
# Usuario: guest / Contraseña: guest
```

---

# Práctica 1 — Hello World

```
⭐ Dificultad: Básica
⏱ Tiempo estimado: 20 minutos
📋 Prerrequisitos: Preparación común
```

## Objetivos

- Enviar y recibir el primer mensaje en RabbitMQ.
- Entender el rol del Producer, la Queue y el Consumer.
- Ver el Default Exchange en acción.

## Contexto

Una tienda online recibe un pedido. El servidor web lo mete en una cola
y un worker lo procesa por separado. El usuario no espera.

```
producer.py  →  [cola: pedidos]  →  consumer.py
```

## Estructura de archivos

```
practica1/
├── producer.py
└── consumer.py
```

## producer.py

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='pedidos')

channel.basic_publish(
    exchange='',           # Default exchange
    routing_key='pedidos', # = nombre de la cola
    body='Pedido #001: 2x Laptop, 1x Ratón'
)

print("[✓] Pedido enviado")
connection.close()
```

## consumer.py

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='pedidos')

def procesar(ch, method, properties, body):
    print(f"[📦] Pedido recibido: {body.decode()}")

channel.basic_consume(queue='pedidos', on_message_callback=procesar, auto_ack=True)
print("[*] Esperando pedidos. CTRL+C para salir")
channel.start_consuming()
```

## Cómo ejecutarlo

```bash
# Terminal 1 — Arrancar primero el consumer
python practica1/consumer.py

# Terminal 2 — Enviar el mensaje
python practica1/producer.py
```

## ¿Qué observar?

- El mensaje aparece en el consumer en tiempo real.
- Si lanzas el producer **sin el consumer activo**, el mensaje queda
  esperando en la cola. Verifica en http://localhost:15672 → Queues.
- Si lanzas **dos consumers** en paralelo y envías varios mensajes,
  RabbitMQ los reparte entre los dos (round-robin).

## Preguntas de reflexión

1. ¿Qué pasa si ejecutas el producer 5 veces antes de lanzar el consumer?
2. ¿Por qué `routing_key='pedidos'` tiene que ser igual al nombre de la cola?
3. ¿Dónde dice "Default Exchange" en el código? ¿Qué indica `exchange=''`?

---

# Práctica 2 — Work Queue y Durabilidad

```
⭐⭐ Dificultad: Media-Baja
⏱ Tiempo estimado: 30 minutos
📋 Prerrequisitos: Práctica 1
```

## Objetivos

- Distribuir trabajo entre múltiples workers.
- Evitar pérdida de mensajes con Manual ACK.
- Proteger mensajes ante reinicios con durabilidad.

## Contexto

La tienda tiene pedidos que tardan diferente tiempo en procesarse.
Necesitamos varios workers y que ningún pedido se pierda si uno de
ellos falla a mitad del trabajo.

## El problema de la Práctica 1

Con `auto_ack=True`, si el worker crashea mientras procesa un pedido,
ese pedido **desaparece para siempre**. Hay que corregirlo.

## Estructura de archivos

```
practica2/
├── producer.py
├── worker.py   ← mismo código para ambos workers
```

## producer.py

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# ① Cola DURABLE: sobrevive a reinicios
channel.queue_declare(queue='pedidos_trabajo', durable=True)

pedidos = [
    'Pedido #001: Laptop       (tarda: 4s)',
    'Pedido #002: Ratón        (tarda: 1s)',
    'Pedido #003: Monitor      (tarda: 5s)',
    'Pedido #004: Teclado      (tarda: 1s)',
    'Pedido #005: Auriculares  (tarda: 3s)',
    'Pedido #006: Webcam       (tarda: 2s)',
]

for pedido in pedidos:
    channel.basic_publish(
        exchange='',
        routing_key='pedidos_trabajo',
        body=pedido,
        properties=pika.BasicProperties(
            delivery_mode=2  # ② Mensaje PERSISTENTE: se escribe a disco
        )
    )
    print(f"[→] Enviado: {pedido}")

connection.close()
```

## worker.py

```python
import pika
import time
import sys

nombre = sys.argv if len(sys.argv) > 1 else 'Worker' [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/c782bf8d-ace1-476a-b004-7c6d4299406d/02_a_tener_en_cuenta.md)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='pedidos_trabajo', durable=True)

# ③ PREFETCH = 1: no recibe el siguiente hasta confirmar el actual
channel.basic_qos(prefetch_count=1)

def procesar(ch, method, properties, body):
    mensaje = body.decode()
    print(f"[{nombre}] ▶ Procesando: {mensaje}")

    segundos = int(mensaje.split('tarda: ').replace('s)', '')) [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/138042210/c782bf8d-ace1-476a-b004-7c6d4299406d/02_a_tener_en_cuenta.md)
    time.sleep(segundos)

    print(f"[{nombre}] ✓ Completado tras {segundos}s")

    # ④ MANUAL ACK: confirmamos SOLO cuando el trabajo está hecho
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='pedidos_trabajo', on_message_callback=procesar)
print(f"[{nombre}] Listo. CTRL+C para salir")
channel.start_consuming()
```

## Cómo ejecutarlo

```bash
# Terminal 1
python practica2/worker.py Worker-A

# Terminal 2
python practica2/worker.py Worker-B

# Terminal 3
python practica2/producer.py
```

## ¿Qué observar?

- Con `prefetch=1`: Worker-A procesa el pedido lento (5s) mientras
  Worker-B ya terminó dos pedidos rápidos. La carga se distribuye
  de forma justa.
- **Prueba de crash**: mata uno de los workers con CTRL+C mientras
  procesa. El mensaje se **reencola automáticamente** y el otro worker
  lo recoge.

## Experimentos guiados

| Experimento | Cambio | Resultado esperado |
|-------------|--------|--------------------|
| Sin prefetch | `basic_qos(0)` | Worker-A recibe todos; Worker-B se queda sin trabajo |
| Sin durabilidad | quitar `durable=True` y `delivery_mode=2`, reiniciar Docker | Los mensajes desaparecen |
| Crash manual | CTRL+C en un worker durante procesamiento | El mensaje se reencola al otro worker |

## Preguntas de reflexión

1. ¿Qué diferencia hay entre `durable=True` en la cola y `delivery_mode=2`
   en el mensaje? ¿Se puede tener uno sin el otro?
2. ¿Qué pasaría con `prefetch=100` si un worker crashea?
3. ¿Cuándo sería aceptable usar `auto_ack=True`?

---

# Práctica 3 — Direct Exchange: clasificar mensajes

```
⭐⭐ Dificultad: Media-Baja
⏱ Tiempo estimado: 30 minutos
📋 Prerrequisitos: Práctica 2
```

## Objetivos

- Entender que los mensajes SIEMPRE pasan por un Exchange.
- Enrutar mensajes a diferentes colas según su categoría exacta.
- Comprender Binding y Routing Key.

## Contexto

La tienda genera eventos de tres tipos: `error`, `warning`, `info`.
Los errores deben ir a un sistema de alertas urgente. Los demás,
a un registro general.

```
Exchange: logs_tienda (direct)
    ├── binding "error"   →  cola_alertas   → consumer_alertas.py
    ├── binding "warning" →  cola_registro  → consumer_registro.py
    └── binding "info"    →  cola_registro  → consumer_registro.py
```

## Estructura de archivos

```
practica3/
├── producer.py
├── consumer_alertas.py
└── consumer_registro.py
```

## producer.py

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs_tienda', exchange_type='direct')

eventos = [
    ('error',   'Fallo al procesar pago del pedido #003'),
    ('warning', 'Stock bajo: Laptop (quedan 2 unidades)'),
    ('info',    'Usuario carlos@ua.es ha iniciado sesión'),
    ('error',   'Timeout en conexión con proveedor externo'),
    ('info',    'Pedido #005 enviado al almacén'),
]

for nivel, mensaje in eventos:
    channel.basic_publish(
        exchange='logs_tienda',
        routing_key=nivel,        # ← La routing key decide el destino
        body=f'[{nivel.upper()}] {mensaje}'
    )
    print(f"[→] {nivel:8s} → {mensaje}")

connection.close()
```

## consumer_alertas.py

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs_tienda', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
cola = result.method.queue

# Solo mensajes con routing_key exacta = "error"
channel.queue_bind(exchange='logs_tienda', queue=cola, routing_key='error')

def alertar(ch, method, properties, body):
    print(f"[🚨 ALERTA] {body.decode()}")

channel.basic_consume(queue=cola, on_message_callback=alertar, auto_ack=True)
print("[*] Sistema de alertas activo — escuchando: error")
channel.start_consuming()
```

## consumer_registro.py

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs_tienda', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
cola = result.method.queue

# Una misma cola puede tener MÚLTIPLES bindings
channel.queue_bind(exchange='logs_tienda', queue=cola, routing_key='warning')
channel.queue_bind(exchange='logs_tienda', queue=cola, routing_key='info')

def registrar(ch, method, properties, body):
    print(f"[📋 REGISTRO] {body.decode()}")

channel.basic_consume(queue=cola, on_message_callback=registrar, auto_ack=True)
print("[*] Registro general activo — escuchando: warning + info")
channel.start_consuming()
```

## Cómo ejecutarlo

```bash
# Terminal 1
python practica3/consumer_alertas.py

# Terminal 2
python practica3/consumer_registro.py

# Terminal 3
python practica3/producer.py
```

## ¿Qué observar?

- El consumer de alertas recibe **solo** los 2 mensajes de tipo `error`.
- El consumer de registro recibe los 3 restantes.
- Envía `routing_key='critical'` sin ningún binding → el mensaje
  desaparece silenciosamente.

## Preguntas de reflexión

1. ¿Qué pasa si envías `routing_key='critical'` y no hay binding para esa key?
2. ¿Puedes hacer que los errores lleguen **simultáneamente** a dos colas
   distintas (alertas Y registro)? ¿Cómo?
3. ¿En qué se diferencia esto del Default Exchange de la Práctica 1?

---

# Práctica 4 — Fanout Exchange: notificaciones broadcast

```
⭐⭐ Dificultad: Media-Baja
⏱ Tiempo estimado: 25 minutos
📋 Prerrequisitos: Práctica 3
```

## Objetivos

- Enviar el mismo mensaje a múltiples colas simultáneamente.
- Entender que el Fanout ignora completamente la routing key.
- Añadir nuevos consumidores sin tocar el producer.

## Contexto

Al confirmar un pedido, hay que notificar en paralelo al servicio
de email, al de SMS y al sistema de historial. Los tres necesitan
la misma información al mismo tiempo.

```
Exchange: pedido_confirmado (fanout)
    ├──  cola aleatoria  →  consumer_email.py
    ├──  cola aleatoria  →  consumer_sms.py
    └──  cola aleatoria  →  consumer_historial.py
```

## Estructura de archivos

```
practica4/
├── producer.py
├── consumer_email.py
├── consumer_sms.py
└── consumer_historial.py
```

## producer.py

```python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='pedido_confirmado', exchange_type='fanout')

pedido = {
    'id': 'PED-2024-001',
    'cliente': 'carlos@ua.es',
    'telefono': '+34 600 111 222',
    'total': 320.00,
    'productos': ['Monitor 4K', 'Cable HDMI']
}

channel.basic_publish(
    exchange='pedido_confirmado',
    routing_key='',           # ← Se ignora en fanout, da igual lo que pongas
    body=json.dumps(pedido)
)
print(f"[✓] Pedido {pedido['id']} confirmado — broadcast enviado")
connection.close()
```

## consumer_email.py

```python
import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='pedido_confirmado', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)  # Cola temporal única
channel.queue_bind(exchange='pedido_confirmado', queue=result.method.queue)
# ↑ Sin routing_key: en fanout no tiene sentido

def enviar_email(ch, method, properties, body):
    p = json.loads(body)
    print(f"[📧 EMAIL] Para: {p['cliente']}")
    print(f"           Pedido {p['id']} confirmado — {p['total']}€")

channel.basic_consume(queue=result.method.queue, on_message_callback=enviar_email, auto_ack=True)
print("[*] Servicio EMAIL activo...")
channel.start_consuming()
```

## consumer_sms.py

```python
import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='pedido_confirmado', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='pedido_confirmado', queue=result.method.queue)

def enviar_sms(ch, method, properties, body):
    p = json.loads(body)
    print(f"[📱 SMS] A {p['telefono']}: Tu pedido {p['id']} está confirmado.")

channel.basic_consume(queue=result.method.queue, on_message_callback=enviar_sms, auto_ack=True)
print("[*] Servicio SMS activo...")
channel.start_consuming()
```

## consumer_historial.py

```python
import pika, json
from datetime import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='pedido_confirmado', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='pedido_confirmado', queue=result.method.queue)

def guardar(ch, method, properties, body):
    p = json.loads(body)
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"[🗃️  HIST] [{ts}] {p['id']} → {p['productos']}")

channel.basic_consume(queue=result.method.queue, on_message_callback=guardar, auto_ack=True)
print("[*] Sistema HISTORIAL activo...")
channel.start_consuming()
```

## Cómo ejecutarlo

```bash
# Terminales 1, 2, 3
python practica4/consumer_email.py
python practica4/consumer_sms.py
python practica4/consumer_historial.py

# Terminal 4
python practica4/producer.py
```

## Preguntas de reflexión

1. Añade un `consumer_almacen.py`. ¿Tienes que modificar el producer?
2. Detén un consumer y envía un mensaje. ¿Lo recibe cuando vuelve
   a conectarse? ¿Por qué?
3. ¿Cuál es la diferencia clave entre Direct y Fanout en cuanto a routing key?

---

# Práctica 5 — Topic Exchange: filtros con wildcards

```
⭐⭐⭐ Dificultad: Media
⏱ Tiempo estimado: 35 minutos
📋 Prerrequisitos: Práctica 3
```

## Objetivos

- Filtrar mensajes usando patrones jerárquicos (`*` y `#`).
- Entender la diferencia entre `*` (una palabra) y `#` (cero o más).
- Diseñar routing keys estructuradas como `nivel1.nivel2.nivel3`.

## Contexto

La tienda tiene almacenes en varias ciudades con sensores IoT.
La routing key sigue el formato: `pais.ciudad.sensor`

```
Exchange: sensores (topic)
    ├── "españa.#"         →  Todo lo de España (cualquier ciudad, cualquier sensor)
    ├── "*.*.temperatura"  →  Temperaturas de cualquier país y ciudad
    └── "españa.madrid.*"  →  Todos los sensores de Madrid
```

## Reglas de los wildcards

| Wildcard | Sustituye | Ejemplo |
|:--------:|-----------|---------|
| `*` | Exactamente UNA palabra | `españa.*.temperatura` → españa.X.temperatura |
| `#` | CERO o más palabras | `españa.#` → españa / españa.madrid / españa.madrid.temp |

## Estructura de archivos

```
practica5/
├── producer.py
├── consumer_espana.py
└── consumer_temperatura.py
```

## producer.py

```python
import pika, random

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='sensores', exchange_type='topic')

lecturas = [
    ('españa.madrid.temperatura',    f'{random.uniform(18,30):.1f}°C'),
    ('españa.madrid.humedad',        f'{random.uniform(40,80):.0f}%'),
    ('españa.barcelona.temperatura', f'{random.uniform(15,28):.1f}°C'),
    ('españa.barcelona.co2',         f'{random.uniform(400,800):.0f}ppm'),
    ('francia.paris.temperatura',    f'{random.uniform(10,20):.1f}°C'),
    ('alemania.berlin.temperatura',  f'{random.uniform(5,15):.1f}°C'),
    ('alemania.berlin.humedad',      f'{random.uniform(30,70):.0f}%'),
]

for routing_key, valor in lecturas:
    channel.basic_publish(
        exchange='sensores',
        routing_key=routing_key,
        body=valor
    )
    print(f"[→] {routing_key:<40} = {valor}")

connection.close()
```

## consumer_espana.py

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='sensores', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
cola = result.method.queue

# "#" = cero o más palabras: cualquier mensaje que empiece por "españa."
channel.queue_bind(exchange='sensores', queue=cola, routing_key='españa.#')

def mostrar(ch, method, properties, body):
    print(f"[🇪🇸 ESPAÑA]  {method.routing_key:<40} → {body.decode()}")

channel.basic_consume(queue=cola, on_message_callback=mostrar, auto_ack=True)
print("[*] Monitor España (patrón: españa.#)")
channel.start_consuming()
```

## consumer_temperatura.py

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='sensores', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
cola = result.method.queue

# "*" = exactamente una palabra: pais.ciudad.temperatura
channel.queue_bind(exchange='sensores', queue=cola, routing_key='*.*.temperatura')

def mostrar(ch, method, properties, body):
    pais, ciudad, _ = method.routing_key.split('.')
    print(f"[🌡️ TEMP]  {ciudad.capitalize()} ({pais.capitalize()}): {body.decode()}")

channel.basic_consume(queue=cola, on_message_callback=mostrar, auto_ack=True)
print("[*] Monitor Temperaturas (patrón: *.*.temperatura)")
channel.start_consuming()
```

## Tabla de enrutamiento esperada

| Routing Key                    | España | Temperatura |
|-------------------------------|:------:|:-----------:|
| españa.madrid.temperatura     | ✅     | ✅          |
| españa.madrid.humedad         | ✅     | ❌          |
| españa.barcelona.temperatura  | ✅     | ✅          |
| españa.barcelona.co2          | ✅     | ❌          |
| francia.paris.temperatura     | ❌     | ✅          |
| alemania.berlin.temperatura   | ❌     | ✅          |
| alemania.berlin.humedad       | ❌     | ❌          |

## Preguntas de reflexión

1. Crea un `consumer_madrid.py` que use el patrón `españa.madrid.*`.
   ¿Qué mensajes recibe?
2. ¿Cuál es la diferencia entre `españa.#` y `españa.*.*`?
   Diseña un caso donde difieran.
3. ¿Cómo modelarías un Topic Exchange para un sistema de logs con
   formato `app.módulo.nivel` (ej: `tienda.pagos.error`)?

---

# Práctica 6 — Dead Letter Queue

```
⭐⭐⭐ Dificultad: Media
⏱ Tiempo estimado: 35 minutos
📋 Prerrequisitos: Práctica 3 (Direct Exchange)
```

## Objetivos

- Capturar mensajes que no se pueden procesar en lugar de perderlos.
- Configurar TTL para mensajes que nadie consume.
- Construir un sistema de revisión manual de fallos.

## Contexto

Los pedidos con datos inválidos (total negativo) no se pueden procesar.
En lugar de descartarlos, los enviamos a una cola de revisión manual
para que el equipo de soporte los revise.

```
cola_pedidos ──(fallo/TTL)──▶ DLX ──▶ cola_revision_manual
```

## Estructura de archivos

```
practica6/
├── producer.py
├── consumer_principal.py   ← procesa pedidos válidos
└── consumer_dlq.py         ← revisa los fallidos
```

## producer.py

```python
import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# ① Declarar el DLX y su cola de destino
channel.exchange_declare(exchange='dlx', exchange_type='direct', durable=True)
channel.queue_declare(queue='cola_revision_manual', durable=True)
channel.queue_bind(exchange='dlx', queue='cola_revision_manual', routing_key='pedido_fallido')

# ② Cola principal que apunta al DLX cuando un mensaje falla
channel.queue_declare(
    queue='cola_pedidos',
    durable=True,
    arguments={
        'x-dead-letter-exchange': 'dlx',
        'x-dead-letter-routing-key': 'pedido_fallido',
        'x-message-ttl': 15000   # Si nadie lo consume en 15s → DLQ
    }
)

pedidos = [
    {'id': 'PED-001', 'cliente': 'ana@ua.es',    'total':  150.00},
    {'id': 'PED-002', 'cliente': 'bob@ua.es',    'total':  -50.00},  # ← INVÁLIDO
    {'id': 'PED-003', 'cliente': 'carlos@ua.es', 'total':    0.00},  # ← INVÁLIDO
    {'id': 'PED-004', 'cliente': 'diana@ua.es',  'total':  320.00},
]

for pedido in pedidos:
    channel.basic_publish(
        exchange='',
        routing_key='cola_pedidos',
        body=json.dumps(pedido),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"[→] {pedido['id']} — Total: {pedido['total']}€")

connection.close()
```

## consumer_principal.py

```python
import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(
    queue='cola_pedidos',
    durable=True,
    arguments={
        'x-dead-letter-exchange': 'dlx',
        'x-dead-letter-routing-key': 'pedido_fallido',
        'x-message-ttl': 15000
    }
)
channel.basic_qos(prefetch_count=1)

def validar(ch, method, properties, body):
    pedido = json.loads(body)
    print(f"[🔍] Validando {pedido['id']}: {pedido['total']}€")

    if pedido['total'] <= 0:
        print(f"[❌] Inválido → enviando a revisión manual")
        # requeue=False + DLX configurado = mensaje va a cola_revision_manual
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    else:
        print(f"[✅] Válido — procesando pedido {pedido['id']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='cola_pedidos', on_message_callback=validar)
print("[*] Validador activo...")
channel.start_consuming()
```

## consumer_dlq.py

```python
import pika, json
from datetime import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='cola_revision_manual', durable=True)

def revisar(ch, method, properties, body):
    pedido = json.loads(body)
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"\n[⚠️  DLQ] [{ts}] Pedido para revisión:")
    print(f"          ID      : {pedido['id']}")
    print(f"          Cliente : {pedido['cliente']}")
    print(f"          Total   : {pedido['total']}€")
    print(f"          Acción  : Notificar a soporte@tienda.es")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='cola_revision_manual', on_message_callback=revisar)
print("[*] Monitor DLQ activo...")
channel.start_consuming()
```

## Cómo ejecutarlo

```bash
# Terminal 1 — Monitor DLQ (arranca primero para no perder nada)
python practica6/consumer_dlq.py

# Terminal 2 — Validador principal
python practica6/consumer_principal.py

# Terminal 3 — Enviar pedidos
python practica6/producer.py
```

## Experimento con TTL

```bash
# 1. Arranca SOLO el consumer_dlq.py (sin el consumer_principal)
# 2. Envía los pedidos con producer.py
# 3. Espera 15 segundos
# → Los mensajes expiran y van automáticamente a la DLQ
#   aunque nunca hubo un "fallo", sino simplemente TTL expirado
```

## Preguntas de reflexión

1. ¿Qué tres situaciones hacen que un mensaje vaya a la DLQ?
2. Sin DLX configurado, ¿qué pasaría con los pedidos inválidos
   al hacer `requeue=False`?
3. ¿Cómo añadirías un contador de reintentos para intentar procesar
   el pedido 3 veces antes de mandarlo a la DLQ?

---

# Práctica 7 — Publisher Confirms e Idempotencia

```
⭐⭐⭐ Dificultad: Media-Alta
⏱ Tiempo estimado: 30 minutos
📋 Prerrequisitos: Práctica 6
```

## Objetivos

- Garantizar que el broker recibió el mensaje desde el lado del producer.
- Evitar procesar el mismo mensaje dos veces (idempotencia).
- Combinar ambas técnicas para máxima fiabilidad.

## Contexto

El sistema de pagos es crítico: no podemos perder un pago ni cobrarlo
dos veces. Necesitamos garantías en ambos extremos.

## Estructura de archivos

```
practica7/
├── producer_seguro.py   ← con Publisher Confirms
└── consumer_idempotente.py
```

## producer_seguro.py

```python
import pika, json, uuid, time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='pagos', exchange_type='direct', durable=True)
channel.queue_declare(queue='cola_pagos', durable=True)
channel.queue_bind(exchange='pagos', queue='cola_pagos', routing_key='pago')

# ① Activar Publisher Confirms en este canal
channel.confirm_delivery()

pagos = [
    {'importe': 150.00, 'metodo': 'tarjeta', 'cliente': 'ana@ua.es'},
    {'importe': 320.00, 'metodo': 'paypal',  'cliente': 'bob@ua.es'},
    {'importe':  75.50, 'metodo': 'bizum',   'cliente': 'carlos@ua.es'},
]

for pago in pagos:
    pago['id'] = str(uuid.uuid4())[:8].upper()  # ID único por mensaje
    try:
        channel.basic_publish(
            exchange='pagos',
            routing_key='pago',
            body=json.dumps(pago),
            properties=pika.BasicProperties(
                delivery_mode=2,
                message_id=pago['id']  # ② ID para idempotencia en el consumer
            ),
            mandatory=True  # ③ Error si no hay ninguna cola vinculada
        )
        # ④ Si llegamos aquí: RabbitMQ escribió el mensaje a disco
        print(f"[✅] Pago {pago['id']} confirmado por broker — {pago['importe']}€")

    except pika.exceptions.UnroutableError:
        # No hay ninguna cola vinculada a ese routing key
        print(f"[❌] Pago {pago['id']} sin destino — GUARDAR EN BD PARA REINTENTO")

    except pika.exceptions.NackError:
        # RabbitMQ tuvo un error interno
        print(f"[❌] Broker rechazó pago {pago['id']} — REINTENTAR")

    time.sleep(0.1)

connection.close()
```

## consumer_idempotente.py

```python
import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='cola_pagos', durable=True)
channel.basic_qos(prefetch_count=1)

# En producción esto sería Redis o una tabla en base de datos
pagos_procesados = set()

def procesar_pago(ch, method, properties, body):
    pago = json.loads(body)
    msg_id = properties.message_id or pago['id']

    # ① Comprobar si ya procesamos este pago antes
    if msg_id in pagos_procesados:
        print(f"[⚠️ ] Pago {msg_id} ya procesado — ignorando duplicado")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Advertir si es un reenvío (consumer crasheó antes de hacer ACK)
    if method.redelivered:
        print(f"[⚠️ ] Pago {msg_id} es un reenvío — procesando igualmente")

    # ② Procesar el pago (lógica de negocio)
    print(f"[💳] Procesando pago {msg_id}: {pago['importe']}€ via {pago['metodo']}")

    # ③ Registrar como procesado ANTES del ACK
    pagos_procesados.add(msg_id)

    # ④ Manual ACK solo si todo salió bien
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[✅] Pago {msg_id} completado")

channel.basic_consume(queue='cola_pagos', on_message_callback=procesar_pago)
print("[*] Consumer de pagos idempotente activo...")
channel.start_consuming()
```

## Experimento: simular duplicado

Para probar la idempotencia sin crashes reales, modifica el producer
para enviar el mismo `message_id` dos veces:

```python
# Al final de producer_seguro.py, añade:
pago_duplicado = {'id': pagos['id'], 'importe': 150.00, 'metodo': 'tarjeta', 'cliente': 'ana@ua.es'}
channel.basic_publish(
    exchange='pagos',
    routing_key='pago',
    body=json.dumps(pago_duplicado),
    properties=pika.BasicProperties(
        delivery_mode=2,
        message_id=pago_duplicado['id']  # mismo ID → consumer lo ignorará
    )
)
print(f"[→] Pago DUPLICADO enviado: {pago_duplicado['id']}")
```

## Preguntas de reflexión

1. ¿Cuándo se confirma un mensaje persistente vs uno no persistente?
2. ¿Qué diferencia hay entre `UnroutableError` y `NackError`?
3. ¿Por qué no es suficiente con el `redelivered` flag para detectar
   duplicados? ¿Cuándo puede ser `False` y el mensaje haberse procesado ya?

---

# Práctica 8 — Proyecto Integrador

```
⭐⭐⭐⭐ Dificultad: Alta
⏱ Tiempo estimado: 60 minutos
📋 Prerrequisitos: Prácticas 1–7 completadas
```

## Objetivo general

Construir un sistema de backend completo para una tienda online
combinando todos los conceptos aprendidos, con decisiones de diseño
justificadas.

## Arquitectura objetivo

```
tienda_producer.py
        │
        ├─[direct rk=pago]──────────▶ cola_pagos ──(DLQ)──▶ cola_pagos_fallidos
        │                                  │
        │                            worker_pagos.py
        │                          (Manual ACK + Idempotencia)
        │
        ├─[direct rk=inventario]───▶ cola_inventario
        │                                  │
        │                         worker_inventario.py
        │
        └─[fanout]─────────────────▶ cola_email
                                   ▶ cola_sms
                                   ▶ cola_historial
                                          │
                                 worker_notificaciones.py
```

## Archivos a crear

```
practica8/
├── tienda_producer.py        ← envía los 3 tipos de mensajes
├── worker_pagos.py           ← Manual ACK + DLQ + Idempotencia + Prefetch
├── worker_inventario.py      ← actualiza stock
├── worker_notificaciones.py  ← consume email + sms + historial
└── monitor_dlq.py            ← vigila pagos fallidos
```

## Requisitos funcionales

| Componente | Requisitos técnicos obligatorios |
|------------|----------------------------------|
| `tienda_producer.py` | Publisher Confirms, mandatory=True, mensajes persistentes, message_id único |
| `worker_pagos.py` | Manual ACK, prefetch=1, idempotencia, DLQ configurada, rechazar total≤0 |
| `worker_inventario.py` | Manual ACK, prefetch=5, simular 2s de procesamiento |
| `worker_notificaciones.py` | Un proceso que consume las 3 colas del fanout |
| `monitor_dlq.py` | Registrar motivo del fallo, simular notificación a soporte |

## Checklist de entrega

- [ ] El sistema arranca sin errores con los 5 procesos en paralelo.
- [ ] Los pedidos con `total <= 0` llegan a `monitor_dlq.py`.
- [ ] Si se mata `worker_pagos.py` durante el procesamiento, el mensaje
      se reencola al reiniciarlo.
- [ ] Si se envía el mismo `message_id` dos veces, el segundo se ignora.
- [ ] Todos los workers usan `auto_ack=False`.
- [ ] El producer usa `confirm_delivery()`.
- [ ] Las colas y exchanges son durables; los mensajes persistentes.

## Cómo ejecutar el sistema completo

```bash
# Terminal 1
python practica8/monitor_dlq.py

# Terminal 2
python practica8/worker_pagos.py

# Terminal 3
python practica8/worker_inventario.py

# Terminal 4
python practica8/worker_notificaciones.py

# Terminal 5 — Panel web (observar colas)
# http://localhost:15672

# Terminal 6
python practica8/tienda_producer.py
```

## Pruebas de robustez

```bash
# Prueba 1: Crash recovery
# Envía 10 pedidos, mata worker_pagos con CTRL+C a mitad,
# reinícialo → debe continuar desde donde lo dejó.

# Prueba 2: TTL + DLQ
# Para worker_pagos, envía 5 pedidos, espera el TTL configurado
# → deben aparecer en monitor_dlq.py automáticamente.

# Prueba 3: Idempotencia
# Modifica producer para enviar el mismo message_id dos veces
# → el segundo debe ignorarse en worker_pagos.
```

## Ejercicio de ampliación (opcional)

Implementa un sistema de **reintentos con backoff**:

1. Si un pago falla, en lugar de ir directo a la DLQ, va a una
   `cola_espera_5s` con `x-message-ttl=5000`.
2. Al expirar, el DLX lo devuelve a `cola_pagos` (segundo intento).
3. En el tercer fallo consecutivo, va a la DLQ definitiva.

> **Pista:** usa el header `x-retry-count` para contar intentos
> y dos colas intermedias con TTL diferente (5s y 30s).
```