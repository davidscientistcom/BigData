# Prometheus + Grafana: From Zero to Hero
## Guía completa para monitorización de infraestructura Big Data

---

## 📚 Índice

1. [Fundamentos conceptuales](#1-fundamentos-conceptuales)
2. [Lab 0: Setup inicial del stack](#lab-0-setup-inicial-del-stack)
3. [Lab 1: Primer servicio con métricas](#lab-1-primer-servicio-con-métricas)
4. [Lab 2: Entendiendo PromQL](#lab-2-entendiendo-promql)
5. [Lab 3: Dashboards en Grafana](#lab-3-dashboards-en-grafana)
6. [Lab 4: Métricas de sistema con Node Exporter](#lab-4-métricas-de-sistema-con-node-exporter)
7. [Lab 5: Load testing con k6](#lab-5-load-testing-con-k6)
8. [Lab 6: Monitorizando Redis y Nginx](#lab-6-monitorizando-redis-y-nginx)
9. [Lab 7: Alertas con Alertmanager](#lab-7-alertas-con-alertmanager)
10. [Lab 8: Casos avanzados y buenas prácticas](#lab-8-casos-avanzados-y-buenas-prácticas)

---

## 1. Fundamentos Conceptuales

### ¿Qué es Prometheus?

Prometheus es un sistema de monitorización y time-series database que funciona mediante **pull-based scraping**. A diferencia de sistemas push (donde los servicios envían métricas), Prometheus pregunta periódicamente a tus servicios "¿qué métricas tienes?" y almacena esas respuestas.

**Modelo mental clave:**
- Tus servicios exponen un endpoint `/metrics` en formato texto plano
- Prometheus hace `GET /metrics` cada X segundos (scrape_interval por defecto 15s)
- Almacena las métricas como series temporales con etiquetas (labels)
- Puedes consultarlas con PromQL (Prometheus Query Language)

### ¿Qué es Grafana?

Grafana es una herramienta de visualización que se conecta a Prometheus (y muchas otras fuentes de datos) para crear dashboards interactivos. No almacena datos, solo los consulta y presenta de forma visual.

### Tipos de métricas en Prometheus

| Tipo | Descripción | Ejemplo de uso | Operaciones comunes |
|------|-------------|----------------|---------------------|
| **Counter** | Solo sube, nunca baja. Se resetea al reiniciar | `http_requests_total`, `errors_total` | `rate()`, `increase()` |
| **Gauge** | Puede subir y bajar libremente | `cpu_usage_percent`, `memory_bytes`, `queue_size` | Directas, `avg()`, `max()` |
| **Histogram** | Distribución de valores en buckets predefinidos | `request_duration_seconds` | `histogram_quantile()` para p95/p99 |
| **Summary** | Similar a histogram, calcula percentiles en cliente | `api_latency` | Percentiles precalculados |

### Arquitectura del sistema

```
┌─────────────┐     scrape      ┌────────────────┐
│  Services   │ ◄───────────────┤  Prometheus    │
│ /metrics    │                 │  (TSDB)        │
└─────────────┘                 └────────┬───────┘
                                         │
                                         │ PromQL
                                         │ queries
                                         ▼
                                ┌────────────────┐
                                │   Grafana      │
                                │  (Dashboards)  │
                                └────────────────┘
```

---

## Lab 0: Setup Inicial del Stack

### Objetivo
Levantar el stack completo de monitorización con Docker Compose y verificar que todos los componentes se comunican correctamente.

### Estructura del proyecto

```
monitoring-lab/
├── docker-compose.yml
├── prometheus/
│   └── prometheus.yml
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── prometheus.yml
├── services/
│   └── fastapi_app/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── main.py
└── README.md
```

### Paso 1: docker-compose.yml

```yaml
version: '3.8'

services:
  # Prometheus: recolector y almacenamiento de métricas
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
      - '--web.enable-admin-api'
    ports:
      - "9090:9090"
    networks:
      - monitoring
    restart: unless-stopped

  # Grafana: visualización
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_SERVER_ROOT_URL=http://localhost:3000
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    ports:
      - "3000:3000"
    networks:
      - monitoring
    depends_on:
      - prometheus
    restart: unless-stopped

  # Node Exporter: métricas del sistema host
  node_exporter:
    image: prom/node-exporter:latest
    container_name: node_exporter
    command:
      - '--path.rootfs=/host'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    pid: host
    volumes:
      - '/:/host:ro,rslave'
    ports:
      - "9100:9100"
    networks:
      - monitoring
    restart: unless-stopped

  # cAdvisor: métricas de contenedores Docker
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    ports:
      - "8080:8080"
    networks:
      - monitoring
    privileged: true
    restart: unless-stopped

networks:
  monitoring:
    driver: bridge

volumes:
  prometheus_data:
  grafana_data:
```

### Paso 2: prometheus/prometheus.yml

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'lab-bigdata'
    environment: 'dev'

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node_exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

### Paso 3: grafana/provisioning/datasources/prometheus.yml

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
    jsonData:
      timeInterval: 15s
```

### Paso 4: Levantar el stack

```bash
# Crear directorios
mkdir -p monitoring-lab/{prometheus,grafana/provisioning/datasources,services/fastapi_app}
cd monitoring-lab

# Crear archivos de configuración (prometheus.yml, docker-compose.yml, etc.)

# Levantar servicios
docker-compose up -d

# Verificar estado
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f
```

### Paso 5: Verificación

**URLs de acceso:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (usuario: `admin`, password: `admin`)
- Node Exporter: http://localhost:9100/metrics
- cAdvisor: http://localhost:8080

**Verificar en Prometheus:**
1. Abre http://localhost:9090/targets
2. Deberías ver 3 targets en estado `UP`:
   - prometheus (1/1)
   - node_exporter (1/1)
   - cadvisor (1/1)

**Verificar en Grafana:**
1. Abre http://localhost:3000
2. Login con admin/admin
3. Ve a Configuration → Data Sources
4. Verifica que "Prometheus" aparece como datasource

---

## Lab 1: Primer Servicio con Métricas

### Objetivo
Crear un servicio FastAPI que exponga métricas Prometheus y monitorizarlo.

### Paso 1: Servicio FastAPI básico

`services/fastapi_app/requirements.txt`:
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
prometheus-client==0.19.0
```

`services/fastapi_app/main.py`:
```python
import asyncio
import random
import time
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app

app = FastAPI(title="BigData Lab API")

# Definir métricas personalizadas
request_count = Counter(
    'http_requests_total',
    'Total de peticiones HTTP',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'Duración de peticiones HTTP',
    ['method', 'endpoint']
)

active_requests = Gauge(
    'http_requests_active',
    'Número de peticiones activas'
)

work_duration = Histogram(
    'work_duration_seconds',
    'Duración del trabajo simulado',
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

errors_total = Counter(
    'errors_total',
    'Total de errores',
    ['type']
)

# Middleware para tracking automático
@app.middleware("http")
async def track_metrics(request, call_next):
    active_requests.inc()
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        request_count.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        request_duration.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response
    finally:
        active_requests.dec()

# Endpoints de negocio
@app.get("/")
async def root():
    return {"message": "BigData Lab API", "version": "1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/do_work")
async def do_work(delay_ms: int = 100, fail_rate: float = 0.0):
    """
    Simula trabajo con delay configurable y tasa de fallos.
    
    Args:
        delay_ms: Milisegundos de delay (simula latencia)
        fail_rate: Probabilidad de fallo (0.0 a 1.0)
    """
    start = time.time()
    
    # Simular fallo aleatorio
    if random.random() < fail_rate:
        errors_total.labels(type='simulated_error').inc()
        raise HTTPException(status_code=500, detail="Simulated error")
    
    # Simular trabajo
    await asyncio.sleep(delay_ms / 1000.0)
    
    duration = time.time() - start
    work_duration.observe(duration)
    
    return {
        "status": "completed",
        "delay_ms": delay_ms,
        "actual_duration_ms": round(duration * 1000, 2)
    }

@app.get("/cpu_intensive")
async def cpu_intensive(iterations: int = 1000000):
    """Simula carga CPU"""
    start = time.time()
    result = sum(i ** 2 for i in range(iterations))
    duration = time.time() - start
    work_duration.observe(duration)
    return {"result": result, "duration_ms": round(duration * 1000, 2)}

# Montar el endpoint /metrics de Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Paso 2: Dockerfile

`services/fastapi_app/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Paso 3: Añadir al docker-compose.yml

Agregar este servicio al `docker-compose.yml`:

```yaml
  # FastAPI service
  api:
    build: ./services/fastapi_app
    container_name: api
    ports:
      - "8000:8000"
    networks:
      - monitoring
    restart: unless-stopped
```

### Paso 4: Actualizar prometheus.yml

Añadir al final de `scrape_configs`:

```yaml
  - job_name: 'fastapi'
    static_configs:
      - targets: ['api:8000']
```

### Paso 5: Desplegar y probar

```bash
# Reconstruir y levantar
docker-compose up -d --build

# Probar el servicio
curl http://localhost:8000/
curl http://localhost:8000/do_work?delay_ms=200
curl http://localhost:8000/do_work?delay_ms=100&fail_rate=0.3

# Ver métricas raw
curl http://localhost:8000/metrics
```

### Paso 6: Verificar en Prometheus

1. Abre http://localhost:9090/targets
2. Verifica que el job `fastapi` está UP
3. Ve a Graph y ejecuta estas queries:
   - `http_requests_total` → deberías ver counters
   - `rate(http_requests_total[1m])` → requests por segundo
   - `http_requests_active` → peticiones concurrentes

---

## Lab 2: Entendiendo PromQL

### ¿Qué es PromQL?

PromQL (Prometheus Query Language) es el lenguaje para consultar métricas. Funciona con series temporales identificadas por nombre y labels.

### Conceptos básicos

**Selector básico:**
```promql
http_requests_total
```

**Selector con filtros (labels):**
```promql
http_requests_total{method="GET", status="200"}
```

**Tipos de resultados:**
- **Instant vector**: valor actual de cada serie
- **Range vector**: ventana temporal de valores `[5m]`
- **Scalar**: número único

### Funciones esenciales

#### 1. rate() - Tasa de crecimiento por segundo

Para counters que siempre suben:

```promql
# Requests por segundo en el último minuto
rate(http_requests_total[1m])

# Por endpoint
rate(http_requests_total{endpoint="/do_work"}[1m])
```

#### 2. irate() - Tasa instantánea

Más sensible a cambios rápidos:

```promql
irate(http_requests_total[5m])
```

#### 3. increase() - Incremento total

```promql
# Cuántas requests en los últimos 5 minutos
increase(http_requests_total[5m])
```

#### 4. histogram_quantile() - Percentiles

Para histogramas:

```promql
# Latencia p95 en los últimos 5 minutos
histogram_quantile(0.95, 
  rate(http_request_duration_seconds_bucket[5m])
)

# p99
histogram_quantile(0.99, 
  rate(http_request_duration_seconds_bucket[5m])
)
```

#### 5. Agregaciones

```promql
# Suma de requests por endpoint
sum by (endpoint) (rate(http_requests_total[1m]))

# Media de duración por método
avg by (method) (http_request_duration_seconds)

# Máximo de requests activas
max(http_requests_active)

# Número de instancias up
count(up == 1)
```

#### 6. Operaciones matemáticas

```promql
# Tasa de error (%)
sum(rate(http_requests_total{status=~"5.."}[1m]))
/
sum(rate(http_requests_total[1m]))
* 100

# Throughput total
sum(rate(http_requests_total[1m]))
```

### Ejercicios prácticos

Abre Prometheus (http://localhost:9090/graph) y ejecuta:

#### Ejercicio 1: Requests totales
```promql
http_requests_total
```

#### Ejercicio 2: RPS (requests por segundo)
```promql
rate(http_requests_total[1m])
```

#### Ejercicio 3: RPS por endpoint
```promql
sum by (endpoint) (rate(http_requests_total[1m]))
```

#### Ejercicio 4: Tasa de error
```promql
sum(rate(http_requests_total{status=~"5.."}[1m]))
/
sum(rate(http_requests_total[1m]))
```

#### Ejercicio 5: Latencia p95
```promql
histogram_quantile(0.95, 
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

#### Ejercicio 6: Peticiones activas
```promql
http_requests_active
```

### Generar carga para ver métricas

Instalar herramienta de carga:

```bash
# wrk (Linux/Mac)
# Ubuntu/Debian
sudo apt-get install wrk

# Mac
brew install wrk
```

Generar tráfico:

```bash
# 100 RPS durante 60 segundos
wrk -t4 -c50 -d60s http://localhost:8000/do_work?delay_ms=50

# Con fallos simulados
wrk -t4 -c100 -d30s "http://localhost:8000/do_work?delay_ms=100&fail_rate=0.1"
```

Ahora refresca las queries en Prometheus y verás los números crecer.

### Funciones de tiempo

```promql
# Valor hace 5 minutos
http_requests_total offset 5m

# Diferencia con hace 1 hora
http_requests_total - (http_requests_total offset 1h)

# Predicción lineal para las próximas 4 horas
predict_linear(http_requests_total[1h], 4*3600)
```

### Operadores de comparación

```promql
# Servicios con más de 100 RPS
sum by (job) (rate(http_requests_total[1m])) > 100

# Uso de memoria mayor al 80%
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.8
```

---

## Lab 3: Dashboards en Grafana

### Objetivo
Crear dashboards interactivos para visualizar las métricas del servicio FastAPI.

### Paso 1: Primer dashboard manual

1. Abre Grafana: http://localhost:3000
2. Click en `+` → `Dashboard` → `Add new panel`
3. En la query, escribe:
   ```promql
   rate(http_requests_total[1m])
   ```
4. En el lado derecho:
   - **Title**: "Requests por segundo"
   - **Panel type**: Time series
   - **Legend**: `{{method}} {{endpoint}}`
5. Click `Apply`

### Paso 2: Dashboard completo para FastAPI

Crear un dashboard con múltiples paneles:

#### Panel 1: Request Rate
```promql
sum(rate(http_requests_total[1m]))
```
- **Type**: Stat
- **Title**: "Total RPS"
- **Unit**: reqps (requests/sec)

#### Panel 2: Request Rate por Endpoint
```promql
sum by (endpoint) (rate(http_requests_total[1m]))
```
- **Type**: Time series
- **Title**: "RPS por Endpoint"
- **Legend**: `{{endpoint}}`

#### Panel 3: Latencia (percentiles)
```promql
# p50
histogram_quantile(0.50, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))

# p95
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))

# p99
histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
```
- **Type**: Time series
- **Title**: "Latencia (p50, p95, p99)"
- **Unit**: seconds (s)
- **Legend**: p50, p95, p99

#### Panel 4: Error Rate
```promql
(
  sum(rate(http_requests_total{status=~"5.."}[1m]))
  /
  sum(rate(http_requests_total[1m]))
) * 100
```
- **Type**: Stat
- **Title**: "Error Rate (%)"
- **Unit**: percent (0-100)
- **Thresholds**: 
  - Verde: 0-1
  - Amarillo: 1-5
  - Rojo: >5

#### Panel 5: Peticiones Activas
```promql
http_requests_active
```
- **Type**: Gauge
- **Title**: "Peticiones Activas"
- **Min**: 0
- **Max**: 100

#### Panel 6: Distribución de Status Codes
```promql
sum by (status) (rate(http_requests_total[5m]))
```
- **Type**: Pie chart
- **Title**: "Distribución de Status Codes"
- **Legend**: `{{status}}`

### Paso 3: Variables en dashboards

Las variables hacen los dashboards dinámicos y reutilizables.

**Crear variable para seleccionar endpoint:**

1. Settings (⚙️) → Variables → Add variable
2. Configurar:
   - **Name**: `endpoint`
   - **Type**: Query
   - **Data source**: Prometheus
   - **Query**: 
     ```promql
     label_values(http_requests_total, endpoint)
     ```
   - **Multi-value**: ✓
   - **Include All**: ✓

3. Ahora en tus panels usa `$endpoint`:
   ```promql
   sum(rate(http_requests_total{endpoint=~"$endpoint"}[1m]))
   ```

**Crear variable para intervalo:**

1. Variables → Add variable
2. Configurar:
   - **Name**: `interval`
   - **Type**: Interval
   - **Values**: `30s,1m,5m,15m,30m,1h`

3. Usar en queries:
   ```promql
   rate(http_requests_total[$interval])
   ```

### Paso 4: Importar dashboards públicos

Para no empezar de cero, importa dashboards públicos por ID:

**IDs recomendados:**
- **1860**: Node Exporter Full (métricas de sistema)
- **893**: Docker monitoring (cAdvisor)
- **3662**: Prometheus 2.0 Stats

**Cómo importar:**
1. `+` → Import
2. Introduce el ID (ej: 1860)
3. Load → Select Prometheus datasource → Import

### Paso 5: Anotaciones (Annotations)

Marcar eventos importantes en los gráficos:

1. Dashboard settings → Annotations → Add annotation query
2. Configurar:
   - **Name**: "Deploys"
   - **Data source**: Prometheus
   - **Query**: 
     ```promql
     changes(process_start_time_seconds[5m]) > 0
     ```
   - **Title**: "Service restarted"

Esto mostrará líneas verticales cuando el servicio se reinicie.

---

## Lab 4: Métricas de Sistema con Node Exporter

### Objetivo
Entender y visualizar métricas del sistema operativo: CPU, memoria, disco, red.

### Métricas clave de Node Exporter

#### CPU

```promql
# % de CPU usado (invertir idle)
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# % de CPU por modo (user, system, iowait)
sum by (mode) (rate(node_cpu_seconds_total[5m])) * 100

# Load average
node_load1   # 1 minuto
node_load5   # 5 minutos
node_load15  # 15 minutos

# Regla: load > núm_cpus indica saturación
node_load5 / count(node_cpu_seconds_total{mode="idle"}) > 1
```

#### Memoria

```promql
# Memoria disponible (GB)
node_memory_MemAvailable_bytes / 1024 / 1024 / 1024

# % de memoria usada
(
  (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
  /
  node_memory_MemTotal_bytes
) * 100

# Memoria por categoría
node_memory_MemTotal_bytes      # Total
node_memory_MemFree_bytes       # Libre
node_memory_Buffers_bytes       # Buffers
node_memory_Cached_bytes        # Cache

# Swap usado
node_memory_SwapTotal_bytes - node_memory_SwapFree_bytes
```

#### Disco

```promql
# % de disco usado (por mountpoint)
(
  (node_filesystem_size_bytes{fstype!="tmpfs"} - node_filesystem_avail_bytes)
  /
  node_filesystem_size_bytes
) * 100

# Espacio disponible (GB)
node_filesystem_avail_bytes{mountpoint="/"} / 1024 / 1024 / 1024

# Tasa de lectura (MB/s)
rate(node_disk_read_bytes_total[5m]) / 1024 / 1024

# Tasa de escritura (MB/s)
rate(node_disk_written_bytes_total[5m]) / 1024 / 1024

# IOPS de lectura
rate(node_disk_reads_completed_total[5m])

# IOPS de escritura
rate(node_disk_writes_completed_total[5m])

# Latencia promedio de I/O
rate(node_disk_read_time_seconds_total[5m]) / rate(node_disk_reads_completed_total[5m])
```

#### Red

```promql
# Tráfico recibido (Mbps)
rate(node_network_receive_bytes_total{device!="lo"}[5m]) * 8 / 1024 / 1024

# Tráfico enviado (Mbps)
rate(node_network_transmit_bytes_total{device!="lo"}[5m]) * 8 / 1024 / 1024

# Paquetes descartados
rate(node_network_receive_drop_total[5m])
rate(node_network_transmit_drop_total[5m])

# Errores de red
rate(node_network_receive_errs_total[5m])
rate(node_network_transmit_errs_total[5m])
```

### Dashboard de sistema completo

Crear un dashboard "System Overview" con estos paneles:

**Panel 1: CPU Usage**
```promql
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

**Panel 2: Load Average**
```promql
node_load1
node_load5
node_load15
```

**Panel 3: Memory Usage**
```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

**Panel 4: Disk Usage**
```promql
100 - ((node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100)
```

**Panel 5: Network Traffic**
```promql
rate(node_network_receive_bytes_total{device!="lo"}[5m]) * 8 / 1024 / 1024
rate(node_network_transmit_bytes_total{device!="lo"}[5m]) * 8 / 1024 / 1024
```

**Panel 6: Disk I/O**
```promql
rate(node_disk_read_bytes_total[5m]) / 1024 / 1024
rate(node_disk_written_bytes_total[5m]) / 1024 / 1024
```

---

## Lab 5: Load Testing con k6

### Objetivo
Integrar k6 con Prometheus para visualizar métricas de carga en tiempo real.

### Paso 1: Instalar k6

```bash
# Linux (Debian/Ubuntu)
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Mac
brew install k6

# Docker (alternativa)
docker pull grafana/k6:latest
```

### Paso 2: Script básico de k6

`load_tests/basic_test.js`:
```javascript
import http from 'k6/http';
import { sleep, check } from 'k6';
import { Rate } from 'k6/metrics';

// Métrica personalizada: tasa de errores
const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // Ramp-up a 20 usuarios
    { duration: '1m', target: 20 },    // Mantener 20 usuarios
    { duration: '30s', target: 50 },   // Ramp-up a 50 usuarios
    { duration: '1m', target: 50 },    // Mantener 50 usuarios
    { duration: '30s', target: 0 },    // Ramp-down a 0
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500'],  // 95% de requests < 500ms
    'errors': ['rate<0.1'],               // Tasa de error < 10%
  },
};

export default function () {
  const delay = Math.floor(Math.random() * 200) + 50;  // 50-250ms
  const res = http.get(`http://localhost:8000/do_work?delay_ms=${delay}`);
  
  const success = check(res, {
    'status is 200': (r) => r.status === 200,
    'duration < 500ms': (r) => r.timings.duration < 500,
  });
  
  errorRate.add(!success);
  
  sleep(1);  // Pausa de 1 segundo entre iteraciones
}
```

### Paso 3: Ejecutar test básico

```bash
cd load_tests
k6 run basic_test.js
```

Verás output en consola:

```
running (3m30s), 00/50 VUs, 4200 complete and 0 interrupted iterations
default ✓ [ 100% ] 00/50 VUs  3m30s

     ✓ status is 200
     ✓ duration < 500ms

     checks.........................: 100.00% ✓ 8400     ✗ 0   
     data_received..................: 1.4 MB  6.7 kB/s
     data_sent......................: 487 kB  2.3 kB/s
     errors.........................: 0.00%   ✓ 0        ✗ 4200
     http_req_duration..............: avg=145.23ms p(95)=287.45ms p(99)=412.33ms
     http_reqs......................: 4200    20.0/s
     iteration_duration.............: avg=1.14s    min=1.05s    max=1.41s
     vus............................: 0       min=0      max=50
     vus_max........................: 50      min=50     max=50
```

### Paso 4: Integración con Prometheus

k6 puede exportar métricas a Prometheus usando **Prometheus Remote Write**.

Añadir al `docker-compose.yml`:

```yaml
  k6:
    image: grafana/k6:latest
    container_name: k6
    networks:
      - monitoring
    volumes:
      - ./load_tests:/scripts
    command: tail -f /dev/null  # Mantener contenedor vivo
```

Script k6 con output a Prometheus:

`load_tests/prom_test.js`:
```javascript
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '5m',
};

export default function () {
  http.get('http://api:8000/do_work?delay_ms=100');
  sleep(1);
}
```

Ejecutar con output a Prometheus:

```bash
docker-compose exec k6 k6 run --out experimental-prometheus-rw /scripts/prom_test.js
```

O con variables de entorno:

```bash
docker-compose exec -e K6_PROMETHEUS_RW_SERVER_URL=http://prometheus:9090/api/v1/write \
  -e K6_PROMETHEUS_RW_TREND_STATS="p(95),p(99),avg,max" \
  k6 k6 run --out experimental-prometheus-rw /scripts/prom_test.js
```

### Paso 5: Queries para visualizar k6 en Grafana

```promql
# VUs activos
k6_vus

# Request rate de k6
rate(k6_http_reqs_total[1m])

# Duración p95
k6_http_req_duration_p95

# Tasa de error
rate(k6_http_reqs_total{status=~"5.."}[1m]) / rate(k6_http_reqs_total[1m])
```

### Paso 6: Escenarios avanzados

`load_tests/advanced_test.js`:
```javascript
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  scenarios: {
    // Escenario 1: Carga constante
    constant_load: {
      executor: 'constant-vus',
      vus: 20,
      duration: '2m',
      startTime: '0s',
    },
    // Escenario 2: Picos de carga
    spike_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 100 },  // Pico repentino
        { duration: '30s', target: 100 },  // Mantener
        { duration: '10s', target: 0 },    // Bajada
      ],
      startTime: '2m',  // Empieza después del constant_load
    },
    // Escenario 3: Tasa constante de requests
    constant_rate: {
      executor: 'constant-arrival-rate',
      rate: 100,  // 100 RPS
      timeUnit: '1s',
      duration: '1m',
      preAllocatedVUs: 50,
      maxVUs: 100,
      startTime: '4m',
    },
  },
};

export default function () {
  const endpoints = [
    '/do_work?delay_ms=50',
    '/do_work?delay_ms=100',
    '/cpu_intensive?iterations=100000',
  ];
  
  const endpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
  http.get(`http://api:8000${endpoint}`);
  sleep(0.1);
}
```

---

## Lab 6: Monitorizando Redis y Nginx

### Objetivo
Añadir Redis y Nginx al stack y monitorizar su rendimiento.

### Paso 1: Añadir Redis y Nginx al docker-compose

```yaml
  # Redis
  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    networks:
      - monitoring
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  # Redis Exporter para Prometheus
  redis_exporter:
    image: oliver006/redis_exporter:latest
    container_name: redis_exporter
    ports:
      - "9121:9121"
    environment:
      - REDIS_ADDR=redis:6379
    networks:
      - monitoring
    depends_on:
      - redis

  # Nginx como reverse proxy/balancer
  nginx:
    image: nginx:alpine
    container_name: nginx
    ports:
      - "80:80"
      - "9113:9113"  # nginx-exporter
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - monitoring
    depends_on:
      - api

  # Nginx Prometheus Exporter
  nginx_exporter:
    image: nginx/nginx-prometheus-exporter:latest
    container_name: nginx_exporter
    command:
      - '-nginx.scrape-uri=http://nginx:9113/stub_status'
    ports:
      - "9114:9114"
    networks:
      - monitoring
    depends_on:
      - nginx

volumes:
  redis_data:
```

### Paso 2: Configurar Nginx

`nginx/nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream api_backend {
        least_conn;  # Balanceo por menos conexiones
        server api:8000;
        # Aquí podrías añadir más réplicas: server api2:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://api_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # Endpoint para nginx-exporter
        location /stub_status {
            stub_status on;
            access_log off;
            allow 127.0.0.1;
            allow 172.0.0.0/8;  # Red de Docker
            deny all;
        }
    }
}
```

### Paso 3: Actualizar prometheus.yml

```yaml
  - job_name: 'redis'
    static_configs:
      - targets: ['redis_exporter:9121']

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx_exporter:9114']
```

### Paso 4: FastAPI con Redis cache

Actualizar `services/fastapi_app/main.py`:

```python
import redis
import json

# Conexión a Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Métrica de cache hits/misses
cache_hits = Counter('cache_hits_total', 'Total cache hits')
cache_misses = Counter('cache_misses_total', 'Total cache misses')

@app.get("/cached_work")
async def cached_work(key: str, delay_ms: int = 100):
    """Endpoint con cache Redis"""
    # Intentar obtener de cache
    cached = redis_client.get(f"work:{key}")
    
    if cached:
        cache_hits.inc()
        return {"status": "cached", "result": json.loads(cached)}
    
    # Cache miss: hacer el trabajo
    cache_misses.inc()
    await asyncio.sleep(delay_ms / 1000.0)
    result = {"key": key, "computed": True, "delay_ms": delay_ms}
    
    # Guardar en cache (TTL 60s)
    redis_client.setex(f"work:{key}", 60, json.dumps(result))
    
    return {"status": "computed", "result": result}
```

Actualizar `requirements.txt`:
```txt
redis==5.0.1
```

### Paso 5: Métricas de Redis

```promql
# Conexiones activas
redis_connected_clients

# Comandos por segundo
rate(redis_commands_processed_total[1m])

# Hit rate del cache (%)
rate(redis_keyspace_hits_total[5m]) 
/ 
(rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m]))
* 100

# Memoria usada
redis_memory_used_bytes / 1024 / 1024  # MB

# Latencia promedio (µs)
redis_latency_microseconds_sum / redis_latency_microseconds_count
```

### Paso 6: Métricas de Nginx

```promql
# Conexiones activas
nginx_connections_active

# Requests por segundo
rate(nginx_http_requests_total[1m])

# Conexiones aceptadas vs handled (detectar drops)
rate(nginx_connections_accepted[5m]) - rate(nginx_connections_handled[5m])

# Reading/Writing/Waiting
nginx_connections_reading
nginx_connections_writing
nginx_connections_waiting
```

### Paso 7: Test de cache

```bash
# Sin cache (lento)
time curl "http://localhost/cached_work?key=test1&delay_ms=1000"

# Con cache (rápido)
time curl "http://localhost/cached_work?key=test1&delay_ms=1000"

# Load test con k6
k6 run - <<EOF
import http from 'k6/http';
export const options = { vus: 50, duration: '30s' };
export default function () {
  const key = 'key_' + Math.floor(Math.random() * 100);
  http.get(\`http://localhost/cached_work?key=\${key}&delay_ms=500\`);
}
EOF
```

Observa en Grafana:
- Cache hit rate aumentando
- Latencia p95 disminuyendo
- Redis commands/sec aumentando

---

## Lab 7: Alertas con Alertmanager

### Objetivo
Configurar alertas automáticas cuando las métricas superen umbrales críticos.

### Paso 1: Añadir Alertmanager

Actualizar `docker-compose.yml`:

```yaml
  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    networks:
      - monitoring
    restart: unless-stopped

volumes:
  alertmanager_data:
```

### Paso 2: Configurar Alertmanager

`alertmanager/alertmanager.yml`:
```yaml
global:
  resolve_timeout: 5m
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alertmanager@example.com'
  smtp_auth_username: 'your-email@gmail.com'
  smtp_auth_password: 'your-app-password'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'email-notifications'
  
  routes:
    - match:
        severity: critical
      receiver: 'email-critical'
      continue: true
    
    - match:
        severity: warning
      receiver: 'email-warnings'

receivers:
  - name: 'email-notifications'
    email_configs:
      - to: 'team@example.com'
        headers:
          Subject: '[ALERT] {{ .GroupLabels.alertname }}'
  
  - name: 'email-critical'
    email_configs:
      - to: 'oncall@example.com'
        headers:
          Subject: '[CRITICAL] {{ .GroupLabels.alertname }}'
  
  - name: 'email-warnings'
    email_configs:
      - to: 'monitoring@example.com'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
```

### Paso 3: Definir reglas de alerta

`prometheus/alert_rules.yml`:
```yaml
groups:
  - name: fastapi_alerts
    interval: 30s
    rules:
      # Servicio caído
      - alert: ServiceDown
        expr: up{job="fastapi"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Servicio {{ $labels.job }} caído"
          description: "El servicio {{ $labels.job }} no responde desde hace más de 1 minuto"
      
      # Alta tasa de error
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > 0.05
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Tasa de error alta"
          description: "Tasa de error es {{ $value | humanizePercentage }} (>5%)"
      
      # Latencia p95 alta
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Latencia p95 alta"
          description: "Latencia p95 es {{ $value }}s (>1s)"
      
      # Peticiones activas saturando
      - alert: TooManyActiveRequests
        expr: http_requests_active > 100
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Demasiadas peticiones activas"
          description: "{{ $value }} peticiones activas (>100)"

  - name: system_alerts
    interval: 30s
    rules:
      # CPU alta
      - alert: HighCPUUsage
        expr: |
          100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Uso de CPU alto en {{ $labels.instance }}"
          description: "CPU al {{ $value }}% (>80%)"
      
      # Memoria alta
      - alert: HighMemoryUsage
        expr: |
          (
            (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
            /
            node_memory_MemTotal_bytes
          ) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Uso de memoria alto"
          description: "Memoria al {{ $value }}% (>85%)"
      
      # Disco casi lleno
      - alert: DiskSpaceLow
        expr: |
          (
            (node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_avail_bytes)
            /
            node_filesystem_size_bytes
          ) * 100 > 85
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Espacio en disco bajo"
          description: "Disco al {{ $value }}% (>85%)"

  - name: redis_alerts
    interval: 30s
    rules:
      # Redis caído
      - alert: RedisDown
        expr: up{job="redis"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Redis caído"
          description: "Redis no responde"
      
      # Memoria Redis alta
      - alert: RedisMemoryHigh
        expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Memoria de Redis alta"
          description: "Memoria al {{ $value | humanizePercentage }}"
```

### Paso 4: Actualizar prometheus.yml

Añadir referencia a las reglas de alerta y conectar con Alertmanager:

```yaml
# Añadir al principio
rule_files:
  - 'alert_rules.yml'

# Añadir al final
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
```

### Paso 5: Recargar configuración

```bash
# Recargar Prometheus sin reiniciar
curl -X POST http://localhost:9090/-/reload

# O reiniciar todo
docker-compose restart prometheus alertmanager
```

### Paso 6: Verificar alertas

1. Abre Prometheus: http://localhost:9090/alerts
2. Verás todas las reglas y su estado (Inactive, Pending, Firing)
3. Abre Alertmanager: http://localhost:9093

### Paso 7: Simular alertas

```bash
# Simular alta carga para disparar HighLatency
wrk -t8 -c200 -d5m "http://localhost:8000/do_work?delay_ms=2000"

# Simular errores para disparar HighErrorRate
wrk -t4 -c100 -d3m "http://localhost:8000/do_work?fail_rate=0.2"

# Parar servicio para disparar ServiceDown
docker-compose stop api
```

### Paso 8: Integración con Grafana

En Grafana puedes ver alertas y crear notificaciones:

1. Alerting → Notification channels → Add channel
2. Configurar tipo: Email, Slack, Webhook, PagerDuty, etc.
3. En cada panel puedes definir alertas visuales

**Alert en panel de Grafana:**
1. Editar panel → Alert tab
2. Configurar condición: `WHEN avg() OF query(A, 5m) IS ABOVE 0.05`
3. Asignar a notification channel

---

## Lab 8: Casos Avanzados y Buenas Prácticas

### Recording Rules para optimización

Las recording rules precalculan queries costosas y las guardan como nuevas métricas.

`prometheus/recording_rules.yml`:
```yaml
groups:
  - name: aggregate_metrics
    interval: 30s
    rules:
      # RPS total precalculado
      - record: job:http_requests_rate:sum
        expr: sum(rate(http_requests_total[1m]))
      
      # RPS por endpoint
      - record: job:http_requests_rate:sum_by_endpoint
        expr: sum by (endpoint) (rate(http_requests_total[1m]))
      
      # Latencia p95 precalculada
      - record: job:http_latency:p95
        expr: |
          histogram_quantile(0.95,
            sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
          )
      
      # Tasa de error precalculada
      - record: job:http_error_rate:ratio
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[1m]))
          /
          sum(rate(http_requests_total[1m]))
      
      # CPU por instancia
      - record: instance:node_cpu_usage:ratio
        expr: |
          100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

Añadir a `prometheus.yml`:
```yaml
rule_files:
  - 'alert_rules.yml'
  - 'recording_rules.yml'
```

Ahora puedes usar queries simplificadas:
```promql
# En vez de la query compleja
job:http_latency:p95

# En vez de
sum(rate(http_requests_total[1m]))
# Usar
job:http_requests_rate:sum
```

### Service Discovery con Docker

Para autodescubrir servicios en Docker:

`prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'docker_services'
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
    relabel_configs:
      # Solo contenedores con label prometheus.enable=true
      - source_labels: [__meta_docker_container_label_prometheus_enable]
        action: keep
        regex: true
      
      # Usar label prometheus.port
      - source_labels: [__meta_docker_container_label_prometheus_port]
        target_label: __address__
        regex: (.+)
        replacement: $1
      
      # Nombre del job desde label
      - source_labels: [__meta_docker_container_label_prometheus_job]
        target_label: job
```

Y en `docker-compose.yml`:
```yaml
  api:
    labels:
      - "prometheus.enable=true"
      - "prometheus.port=api:8000"
      - "prometheus.job=fastapi"
```

### Federated Prometheus (multi-cluster)

Para agregar métricas de múltiples Prometheus:

```yaml
# Prometheus central
scrape_configs:
  - job_name: 'federate'
    scrape_interval: 15s
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{job="fastapi"}'
        - '{__name__=~"job:.*"}'  # Recording rules
    static_configs:
      - targets:
        - 'prometheus-cluster-1:9090'
        - 'prometheus-cluster-2:9090'
```

### Buenas prácticas de naming

**Convenciones de nombres:**
```
# Counters: _total suffix
http_requests_total
errors_total

# Gauges: sin suffix especial
memory_usage_bytes
queue_size

# Histograms/Summaries: _seconds o unidad base
http_request_duration_seconds
payload_size_bytes

# Prefijo por componente
fastapi_http_requests_total
redis_commands_total
nginx_connections_active
```

### Exportar métricas de negocio

Más allá de infraestructura, exporta métricas de negocio:

```python
from prometheus_client import Counter, Histogram, Gauge

# Métricas de negocio
orders_total = Counter('orders_total', 'Total orders', ['status', 'payment_method'])
order_value = Histogram('order_value_euros', 'Order value in EUR',
                        buckets=)[7][8]
active_users = Gauge('active_users', 'Currently active users')
revenue_total = Counter('revenue_euros_total', 'Total revenue')

@app.post("/order")
async def create_order(order: Order):
    # Procesar orden...
    
    orders_total.labels(status='completed', payment_method=order.payment).inc()
    order_value.observe(order.total_amount)
    revenue_total.inc(order.total_amount)
    
    return {"order_id": order.id}
```

### Monitorizar batch jobs

Para jobs que no están siempre corriendo:

```python
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import time

def run_batch_job():
    registry = CollectorRegistry()
    
    duration = Gauge('job_duration_seconds', 'Job duration', registry=registry)
    last_success = Gauge('job_last_success_timestamp', 'Last success', registry=registry)
    records_processed = Gauge('job_records_processed', 'Records', registry=registry)
    
    start = time.time()
    try:
        # Hacer trabajo
        count = process_data()
        
        duration.set(time.time() - start)
        last_success.set(time.time())
        records_processed.set(count)
        
        push_to_gateway('localhost:9091', job='batch_processor', registry=registry)
    except Exception as e:
        # Registrar fallo
        pass
```

Añadir Pushgateway:
```yaml
  pushgateway:
    image: prom/pushgateway:latest
    ports:
      - "9091:9091"
    networks:
      - monitoring
```

### Retención y downsampling

Configurar retención en Prometheus:

```yaml
  prometheus:
    command:
      - '--storage.tsdb.retention.time=30d'
      - '--storage.tsdb.retention.size=50GB'
```

Para retención larga con downsampling, usar Thanos o VictoriaMetrics.

### Debugging de queries

Herramientas útiles:

1. **Explain query en Prometheus UI:**
   http://localhost:9090/graph → ejecuta query → pestaña "Table"

2. **Prometheus API:**
```bash
# Query instantánea
curl 'http://localhost:9090/api/v1/query?query=up'

# Query rango
curl 'http://localhost:9090/api/v1/query_range?query=rate(http_requests_total[5m])&start=2026-01-13T00:00:00Z&end=2026-01-13T23:59:59Z&step=15s'

# Metadata de métricas
curl 'http://localhost:9090/api/v1/metadata?metric=http_requests_total'
```

3. **promtool para validar configuración:**
```bash
# Validar prometheus.yml
docker-compose exec prometheus promtool check config /etc/prometheus/prometheus.yml

# Validar reglas
docker-compose exec prometheus promtool check rules /etc/prometheus/alert_rules.yml
```

### Dashboard de SLOs (Service Level Objectives)

Definir y monitorizar SLOs:

```promql
# Availability SLO: 99.9% uptime
(
  sum(rate(http_requests_total{status!~"5.."}[30d]))
  /
  sum(rate(http_requests_total[30d]))
) * 100

# Latency SLO: 95% requests < 500ms
(
  sum(rate(http_request_duration_seconds_bucket{le="0.5"}[30d]))
  /
  sum(rate(http_request_duration_seconds_count[30d]))
) * 100

# Error budget remaining (para SLO 99.9%)
1 - (
  (1 - (
    sum(rate(http_requests_total{status!~"5.."}[30d]))
    /
    sum(rate(http_requests_total[30d]))
  ))
  /
  0.001  # 0.1% error budget
)
```

---

## Ejercicios Finales

### Ejercicio 1: Dashboard completo
Crear un dashboard unificado que muestre:
- Golden signals (latency, traffic, errors, saturation)
- RED metrics (Rate, Errors, Duration)
- System resources
- Business metrics

### Ejercicio 2: Chaos engineering
1. Implementar endpoint `/chaos` que aleatoriamente:
   - Devuelve 500
   - Tarda más de 5 segundos
   - Consume mucha CPU
2. Configurar alertas que detecten el comportamiento anómalo
3. Ejecutar load test y verificar que las alertas se disparan

### Ejercicio 3: Multi-tier monitoring
1. Añadir PostgreSQL con postgres_exporter
2. Crear servicio que consulte DB
3. Monitorizar end-to-end: Nginx → API → Redis → PostgreSQL
4. Crear dashboard con correlación entre capas

### Ejercicio 4: Custom exporter
Crear un exporter en Python que:
1. Lee archivos de log
2. Extrae métricas (requests, errors, latencias)
3. Expone en formato Prometheus
4. Se integra en el stack

---

## Recursos Adicionales

### Documentación oficial
- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/
- k6: https://k6.io/docs/
- PromQL: https://prometheus.io/docs/prometheus/latest/querying/basics/

### Dashboards públicos
- Grafana Dashboards: https://grafana.com/grafana/dashboards/
- Node Exporter (1860): CPU, memoria, disco, red
- Docker monitoring (893): Contenedores
- Redis (763): Métricas de Redis
- Nginx (12708): Reverse proxy stats

### Librerías de cliente Prometheus
- Python: `prometheus-client`
- Go: `prometheus/client_golang`
- Java: `io.prometheus:simpleclient`
- Node.js: `prom-client`

### Herramientas complementarias
- **Thanos**: Almacenamiento a largo plazo, multi-cluster
- **VictoriaMetrics**: TSDB compatible con Prometheus, más eficiente
- **Loki**: Logs agregados (como Prometheus pero para logs)
- **Tempo**: Distributed tracing
- **Mimir**: Prometheus a escala (Grafana Labs)

---

## Conclusión

Este laboratorio te ha guiado desde cero hasta conceptos avanzados de observabilidad:

1. **Fundamentos**: Entender métricas y arquitectura pull-based
2. **Instrumentación**: Añadir métricas a aplicaciones
3. **PromQL**: Consultar y agregar métricas eficientemente
4. **Visualización**: Crear dashboards efectivos en Grafana
5. **Testing**: Integrar load testing con monitorización
6. **Alerting**: Detectar y notificar problemas automáticamente
7. **Best practices**: Naming, recording rules, SLOs

**Próximos pasos:**
- Implementa monitorización en tus proyectos reales
- Experimenta con Thanos para retención larga
- Integra con sistemas de logging (Loki)
- Añade distributed tracing (Jaeger/Tempo)
- Define SLOs y SLIs para tus servicios

---

**Autor**: Laboratorio Big Data e IA  
**Fecha**: Enero 2026  
**Versión**: 1.0


## Posibles fuentes de datos.

[1](https://www.cherryservers.com/blog/set-up-grafana-with-prometheus)
[2](https://betterstack.com/community/guides/monitoring/visualize-prometheus-metrics-grafana/)
[3](https://dev.to/rafi021/how-to-set-up-a-monitoring-stack-with-prometheus-grafana-and-node-exporter-using-docker-compose-17cc)
[4](https://prometheus.io/docs/prometheus/latest/querying/basics/)
[5](https://prometheus.io/docs/prometheus/latest/querying/examples/)
[6](https://last9.io/blog/promql-for-beginners-getting-started-with-prometheus-query-language/)
[7](https://codedamn.com/news/backend/benchmarking-redis-performance)
[8](https://stackoverflow.com/questions/56165506/create-a-variable-in-prometheus-grafana-with-all-values-selected-by-default)
[9](https://prometheus.io/docs/alerting/latest/configuration/)
[10](https://betterstack.com/community/guides/monitoring/prometheus-alertmanager/)