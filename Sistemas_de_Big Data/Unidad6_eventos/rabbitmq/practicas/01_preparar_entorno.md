
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
