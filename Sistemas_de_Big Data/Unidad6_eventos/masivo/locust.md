# Locust: guía completa paso a paso

## 1. Objetivo y modelo mental

Locust es una herramienta de pruebas de carga escrita en Python que te permite simular muchos usuarios concurrentes ejecutando peticiones HTTP (o cualquier otra cosa que programes) de forma controlada. [frugaltesting](https://www.frugaltesting.com/blog/locust-for-load-testing-a-beginners-guide)
La unidad básica es un “usuario” (User/HttpUser) que ejecuta tareas (`@task`) en bucle, con una pausa entre tareas controlada por `wait_time`. [docs.locust](https://docs.locust.io/en/stable/writing-a-locustfile.html)

En esta guía vamos a:

1. Instalar Locust y ejecutar el primer test mínimo. [youtube](https://www.youtube.com/watch?v=a28HBCfDtvM)
2. Añadir autenticación y diferentes tipos de tareas. [docs.locust](https://docs.locust.io/en/2.19.1/api.html)
3. Controlar el ritmo con `wait_time` y pesos de tareas. [linode](https://www.linode.com/docs/guides/load-testing-with-locust/)
4. Manejar errores y resultados de forma explícita (`catch_response`). [docs.locust](https://docs.locust.io/en/stable/api.html)
5. Ejecutar en modo headless exportando CSV/HTML. [frugaltesting](https://www.frugaltesting.com/blog/locust-for-load-testing-a-beginners-guide)
6. Usar eventos y modo distribuido (master/worker). [docs.locust](https://docs.locust.io/en/stable/running-distributed.html)



## 2. Instalación y primer test mínimo

### 2.1. Instalación recomendada (entorno aislado)

```bash
# Crear entorno
conda create -n locust python=3.11
conda activate locust

# Instalar Locust
pip install locust

# Verificar
locust --version
```

Locust instala un comando `locust` que arrancará un proceso con una pequeña web en el puerto 8089 por defecto. [docs.locust](https://docs.locust.io)

### 2.2. Primer `locustfile.py` (mínimo)

Creamos un archivo `locustfile.py` en un directorio vacío:

```python
from locust import HttpUser, task, between

class MiPrimerUsuario(HttpUser):
    # Tiempo de espera entre tareas (segundos)
    wait_time = between(1, 3)

    # Host por defecto (podemos no ponerlo y usar --host en CLI)
    host = "http://localhost:8000"

    @task
    def hola(self):
        self.client.get("/hello")
```

Puntos clave:

- `HttpUser` ya trae un `self.client` HTTP para hacer `get`, `post`, etc. [docs.locust](https://docs.locust.io/en/2.19.1/api.html)
- `@task` marca los métodos que se ejecutarán en bucle por cada usuario. [docs.locust](https://docs.locust.io/en/2.19.1/api.html)
- `wait_time = between(1, 3)` simula “piensa entre 1 y 3 segundos entre acciones”. [linode](https://www.linode.com/docs/guides/load-testing-with-locust/)

### 2.3. Ejecutar y entender la UI

Lanzamos Locust:

```bash
locust -f locustfile.py
```

Después abrimos en el navegador:

```text
http://localhost:8089
```

En la pantalla inicial configuramos:

- Número de usuarios (Users).  
- Tasa de arranque (Spawn rate) = cuántos usuarios por segundo se añaden. [youtube](https://www.youtube.com/watch?v=u6VW-HqxOjg)

Al darle a “Start swarming”, veremos:

- RPS (requests per second).  
- Tiempo medio, p95, p99.  
- Número de fallos. [youtube](https://www.youtube.com/watch?v=u6VW-HqxOjg)

Ahora ya podemos  “jugar” cambiando número de usuarios y ver cómo sufren los endpoints.

## 3. Segundo paso: varias tareas y nombres

Ahora complicamos un poco: un mismo usuario hará lecturas frecuentes y escrituras ocasionales.

```python
from locust import HttpUser, task, between

class UsuarioCatalogo(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8000"

    @task(3)  # peso 3: se ejecuta ~3 veces más que las de peso 1
    def listar_productos(self):
        self.client.get("/productos", name="GET /productos")

    @task(1)
    def crear_producto(self):
        payload = {"nombre": "producto_test", "precio": 9.99}
        self.client.post("/productos", json=payload, name="POST /productos")
```

Notas:

- El entero de `@task(n)` indica el **peso** relativo: aproximadamente 75% lecturas, 25% escrituras. [docs.locust](https://docs.locust.io/en/stable/writing-a-locustfile.html)
- El parámetro `name="..."` agrupa las métricas en la UI con un nombre amigable, independientemente de la URL exacta. [docs.locust](https://docs.locust.io/en/2.19.1/api.html)

Ejercicio típico: pedir a los alumnos que cambien a `@task(10)` en lecturas y vean cómo bajan los RPS de escrituras manteniendo el número de usuarios.



## 4. Añadiendo autenticación (on_start / on_stop)

Ahora vamos a añadir un login al principio de la vida del usuario, y opcionalmente un logout al final.

```python
from locust import HttpUser, task, between

class UsuarioAutenticado(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8000"

    def on_start(self):
        # Se ejecuta una vez por usuario virtual, al empezar
        res = self.client.post(
            "/auth/token",
            data={"username": "test", "password": "test123"},
        )
        if res.status_code != 200:
            # Si falla el login, podemos abortar este usuario
            res.failure(f"Login fallo con {res.status_code}")
            self.environment.runner.quit()
            return
        self.token = res.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def on_stop(self):
        # Se ejecuta al morir el usuario
        self.client.post("/auth/logout", headers=self.headers)

    @task(3)
    def listar(self):
        self.client.get("/items", headers=self.headers, name="GET /items")

    @task(1)
    def insertar(self):
        payload = {"value": "test"}
        self.client.post("/items", json=payload, headers=self.headers, name="POST /items")
```

`on_start` y `on_stop` son la forma recomendada de inicializar y liberar recursos por usuario (login, abrir conexiones, etc.). [docs.locust](https://docs.locust.io/en/stable/writing-a-locustfile.html)



## 5. Controlando el ritmo: `wait_time` a fondo

Hasta ahora hemos usado `between`, pero hay más opciones muy útiles.

### 5.1. Tipos de `wait_time`

En la clase `User`/`HttpUser` podemos usar: [stackoverflow](https://stackoverflow.com/questions/27713104/locust-io-controlling-the-request-per-second-parameter)

```python
from locust import between, constant, constant_pacing, constant_throughput

# 1) between(min, max): aleatorio uniforme
wait_time = between(1, 3)

# 2) constant(n): siempre n segundos
wait_time = constant(2)

# 3) constant_pacing(n): cada iteración completa dura al menos n segundos
#   (si la tarea tarda 1s y n=5, esperará 4s)
wait_time = constant_pacing(5)

# 4) constant_throughput(tps): intenta ejecutar tps tareas por segundo
#    Ej: 2 tareas/s por usuario
wait_time = constant_throughput(2)
```

`constant_pacing` y `constant_throughput` son muy útiles cuando quieres acercarte a un RPS concreto con un número determinado de usuarios. [stackoverflow](https://stackoverflow.com/questions/27713104/locust-io-controlling-the-request-per-second-parameter)

Ejemplo: si quieres aproximadamente 50 RPS de un único endpoint, puedes usar `constant_pacing(1)` y lanzar 50 usuarios (cada usuario ejecuta la tarea ~1 vez por segundo, aproximando 50 RPS). [stackoverflow](https://stackoverflow.com/questions/27713104/locust-io-controlling-the-request-per-second-parameter)

### 5.2. Función personalizada

También puedes definir tu propia función:

```python
import random

class UsuarioRandom(HttpUser):
    def wait_time(self):
        # Distribución exponencial; la mayoría de esperas cortas, algunas largas
        return random.expovariate(1.0) * 0.5
```

Esto te permite simular patrones de “piensa-tiempo” más realistas.



## 6. Modelando escenarios: varias tareas, TaskSet y SequentialTaskSet

Hasta ahora todo estaba en una sola clase de usuario. Ahora añadimos estructura para flujos más complejos.

### 6.1. Varios tipos de usuarios

Una opción es crear varias clases `HttpUser` según el rol:

```python
from locust import HttpUser, task, between

class UsuarioSoloLectura(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8000"

    @task
    def listar(self):
        self.client.get("/items", name="GET /items")


class UsuarioEscritor(HttpUser):
    wait_time = between(2, 4)
    host = "http://localhost:8000"

    @task
    def insertar(self):
        payload = {"value": "heavy_insert"}
        self.client.post("/bulk-insert", json=payload, name="POST /bulk-insert")
```

En la UI podrás ver métricas separadas por tipo de usuario (clase). [docs.locust](https://docs.locust.io/en/2.19.1/api.html)

### 6.2. TaskSet y SequentialTaskSet

Cuando quieres un flujo ordenado (por ejemplo: crear carrito → añadir items → pagar → comprobar estado), usas `SequentialTaskSet`. [github](https://github.com/locustio/locust/blob/master/docs/tasksets.rst)

```python
from locust import HttpUser, SequentialTaskSet, TaskSet, task, between

class FlujoCompra(SequentialTaskSet):

    @task
    def paso1_crear_carrito(self):
        res = self.client.post("/cart")
        self.cart_id = res.json()["id"]

    @task
    def paso2_add_item(self):
        self.client.post(f"/cart/{self.cart_id}/items", json={"sku": "X", "qty": 3})

    @task
    def paso3_pagar(self):
        self.client.post(f"/cart/{self.cart_id}/checkout")

    @task
    def paso4_verificar(self):
        res = self.client.get(f"/cart/{self.cart_id}")
        if res.json().get("status") == "paid":
            # Terminamos el flujo y volvemos al HttpUser
            self.interrupt(reschedule=True)


class UsuarioEcommerce(HttpUser):
    wait_time = between(1, 3)
    tasks = [FlujoCompra]
```

La diferencia principal:

- `SequentialTaskSet` ejecuta las tareas en orden (métodos `@task` en orden de definición). [github](https://github.com/locustio/locust/blob/master/docs/tasksets.rst)
- `TaskSet` elige tareas según pesos, sin orden fijo (salvo que llames a `self.interrupt()`). [stackoverflow](https://stackoverflow.com/questions/46022068/locust-taskset-class-vs-function-task)



## 7. Manejo detallado de errores: `catch_response`

Por defecto, cualquier código HTTP 4xx/5xx se cuenta como fallo, pero a veces quieres control fino.

```python
from locust import HttpUser, task, between

class UsuarioConControl(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8000"

    @task
    def bulk_insert(self):
        docs = [{"v": i} for i in range(500)]
        with self.client.post(
            "/bulk-insert",
            json={"documents": docs},
            catch_response=True,
            name="bulk-insert-500"
        ) as res:
            if res.status_code != 201:
                res.failure(f"HTTP {res.status_code}")
                return

            inserted = res.json().get("inserted", 0)
            if inserted < 500:
                res.failure(f"Insertados {inserted}/500")
            else:
                res.success()
```

Claves:

- `catch_response=True` hace que la respuesta no se marque automáticamente como éxito o fracaso. [docs.locust](https://docs.locust.io/en/stable/api.html)
- Usas `res.success()` y `res.failure(msg)` para decidir. [docs.locust](https://docs.locust.io/en/stable/api.html)

Esto es útil cuando, por ejemplo, aceptas un 404 como “correcto” en cierto contexto o quieres registrar mensajes ricos.



## 8. Modo headless, CSV y HTML

Una vez que el escenario está estable, suele interesar integrarlo en pipelines y guardar resultados.

### 8.1. Modo headless

Ejemplo:

```bash
locust -f locustfile.py \
  --headless \
  --users 100 \
  --spawn-rate 10 \
  --run-time 5m \
  --host http://localhost:8000
```

- `--headless` desactiva la UI y permite ejecutar en scripts/CI. [youtube](https://www.youtube.com/watch?v=a28HBCfDtvM)
- `--run-time` limita la duración total del test. [frugaltesting](https://www.frugaltesting.com/blog/locust-for-load-testing-a-beginners-guide)

### 8.2. Exportar CSV y HTML

```bash
locust -f locustfile.py \
  --headless \
  -u 100 -r 10 -t 5m \
  --csv=resultados \
  --html=reporte.html \
  --host http://localhost:8000
```

Esto genera varios ficheros `resultados_*.csv` y un HTML con estadísticas agregadas. [github](https://github.com/benc-uk/locust-reporter)

Si quieres reportes HTML más avanzados a partir de los CSV, existe `locust-reporter`. [github](https://github.com/benc-uk/locust-reporter)



## 9. Eventos y “pseudo-thresholds” en Locust

Locust no tiene thresholds declarativos como k6, pero su sistema de eventos permite implementar lógica similar. [docs.locust](https://docs.locust.io/en/2.17.0/extending-locust.html)

### 9.1. Ejemplo: watchdog que aborta si error > 10%

```python
from locust import events
import logging

MAX_FAIL_RATIO = 0.10  # 10 %

@events.init.add_listener
def setup_watchdog(environment, **kwargs):
    import gevent

    def check():
        while True:
            gevent.sleep(5)
            runner = environment.runner
            if not runner:
                continue

            stats = runner.stats.total
            if stats.num_requests < 100:
                continue  # esperar a tener datos

            if stats.fail_ratio > MAX_FAIL_RATIO:
                logging.error(f"Abortando: fail_ratio={stats.fail_ratio:.2%}")
                runner.quit()

    gevent.spawn(check)
```

- `events.init` se dispara al inicio de Locust. [docs.locust](https://docs.locust.io/en/2.17.0/extending-locust.html)
- `environment.runner.stats.total` da acceso a métricas globales (fallos, RPS, etc.). [docs.locust](https://docs.locust.io/en/stable/api.html)
- `runner.quit()` detiene el test. [docs.locust](https://docs.locust.io/en/2.17.0/extending-locust.html)

### 9.2. Evento por request

```python
from locust import events

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kw):
    if exception:
        print(f"Fallo en {name}: {exception} ({response_time} ms)")
```

Esto te permite loguear o enviar métricas a otro sistema.



## 10. Modo distribuido: master y workers

Cuando una sola máquina no basta para simular suficientes usuarios, Locust soporta un modo distribuido sencillo. [courses.parottasalna](https://courses.parottasalna.com/locust/running-locust-in-distributed-mode-with-master-and-workers)

### 10.1. Arrancar master y workers

En la máquina master:

```bash
locust -f locustfile.py --master --host http://api:8000
```

En cada worker:

```bash
locust -f locustfile.py --worker --master-host 192.168.1.10
```

- El master expone la UI web y no ejecuta usuarios por sí mismo. [docs.locust](https://docs.locust.io/en/stable/running-distributed.html)
- Cada worker ejecuta usuarios y envía estadísticas agregadas al master. [docs.locust](https://docs.locust.io/en/stable/running-distributed.html)

### 10.2. Master sirviendo el locustfile (versión reciente)

Desde Locust 2.23.0 se puede lanzar workers sin copiar el locustfile, usando `-f -` para que se descargue desde el master. [docs.locust](https://docs.locust.io/en/stable/running-distributed.html)

```bash
locust -f - --worker --master-host 192.168.1.10
```

Esto simplifica despliegues en clúster donde quieres un único origen de verdad para el script.



## 11. Ejemplo final: escenario Big Data de inserciones masivas

Por último, un ejemplo completo que podrías usar casi tal cual en tu curso: un único `locustfile.py` que:

- Hace login al iniciar cada usuario.  
- Ejecuta tareas de inserción masiva (`/bulk-insert`) y lectura (`/items`).  
- Marca errores detallados.  
- Usa un watchdog para abortar si la tasa de fallos supera un umbral.  

```python
from locust import HttpUser, task, between, events
from locust.exception import RescheduleTask
import random
import logging
import gevent

DOCS_PER_BATCH = 500
MAX_FAIL_RATIO = 0.1  # 10 %

# Watchdog global
@events.init.add_listener
def setup_watchdog(environment, **kw):
    def check():
        while True:
            gevent.sleep(10)
            runner = environment.runner
            if not runner:
                continue
            stats = runner.stats.total
            if stats.num_requests < 200:
                continue
            if stats.fail_ratio > MAX_FAIL_RATIO:
                logging.error(f"Abortando: fail_ratio={stats.fail_ratio:.2%}")
                runner.quit()
    gevent.spawn(check)


class BigDataUser(HttpUser):
    wait_time = between(0.5, 1.5)
    host = "http://localhost:8000"

    def on_start(self):
        res = self.client.post(
            "/auth/token",
            data={"username": "admin", "password": "secret"},
            name="POST /auth/token",
        )
        if res.status_code != 200:
            # No tiene sentido que este usuario siga si no puede autenticarse
            raise RescheduleTask()
        self.token = res.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(1)
    def bulk_insert(self):
        docs = [
            {"id": f"d_{i}", "value": random.random()}
            for i in range(DOCS_PER_BATCH)
        ]
        with self.client.post(
            "/bulk-insert",
            json={"documents": docs},
            headers=self.headers,
            catch_response=True,
            name="POST /bulk-insert (500)"
        ) as res:
            if res.status_code != 201:
                res.failure(f"HTTP {res.status_code}")
                return
            inserted = res.json().get("inserted", 0)
            if inserted < DOCS_PER_BATCH:
                res.failure(f"Insertados {inserted}/{DOCS_PER_BATCH}")
            else:
                res.success()

    @task(3)
    def read_recent(self):
        self.client.get(
            "/items?limit=100&sort=-ts",
            headers=self.headers,
            name="GET /items?recent",
        )
```

Puedes ejecutar esto en modo UI o headless:

```bash
# UI
locust -f locustfile.py

# Headless con CSV y HTML
locust -f locustfile.py \
  --headless \
  -u 100 -r 10 -t 10m \
  --csv=bigdata \
  --html=bigdata.html \
  --host http://localhost:8000
```

- Levantar Locust, escribir sus propios `HttpUser` básicos y avanzados. [frugaltesting](https://www.frugaltesting.com/blog/locust-for-load-testing-a-beginners-guide)
- Controlar ritmo (`wait_time`), pesos, y flujos secuenciales. [linode](https://www.linode.com/docs/guides/load-testing-with-locust/)
- Entender y manejar errores con `catch_response` y eventos. [docs.locust](https://docs.locust.io/en/2.17.0/extending-locust.html)
- Ejecutar en local, headless, y en modo distribuido. [docs.locust](https://docs.locust.io/en/stable/running-distributed.html)