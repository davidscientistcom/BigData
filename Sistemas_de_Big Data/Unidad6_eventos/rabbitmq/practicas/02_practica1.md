
# Práctica 1 — Hello World

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
