
# Práctica 2 — Work Queue y Durabilidad

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

nombre = 'sys.argv if len(sys.argv) > 1 else 'Worker' 

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='pedidos_trabajo', durable=True)

# ③ PREFETCH = 1: no recibe el siguiente hasta confirmar el actual
channel.basic_qos(prefetch_count=1)

def procesar(ch, method, properties, body):
    mensaje = body.decode()
    print(f"[{nombre}] ▶ Procesando: {mensaje}")

    segundos = int(mensaje.split('tarda: ').replace('s)', ''))
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

