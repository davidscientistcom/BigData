# NGINX: From Zero to Hero (IA & Big Data)

> Documento de referencia para pasar de exponer una API a desplegar una **plataforma de producción** robusta, segura y escalable para sistemas de IA.


## 1. Idea central

* **FastAPI/Uvicorn NO se exponen directamente a Internet**.
* **NGINX es la capa de infraestructura** que se enfrenta al mundo.
* FastAPI procesa lógica; NGINX protege, enruta, balancea, cachea y monitoriza.

> FastAPI = cerebro
> NGINX = sistema nervioso + piel



## 2. Por qué Uvicorn no es suficiente

Uvicorn es un **servidor de aplicaciones**, no de infraestructura:

* No gestiona TLS de forma robusta
* No tiene rate limiting
* No balancea múltiples réplicas
* Expone directamente Python

NGINX:

* Event loop no bloqueante (C)
* Miles de conexiones con pocos recursos
* Diseñado para tráfico real



## 3. Proxy vs Reverse Proxy

* **Forward Proxy**: protege al cliente (VPN)
* **Reverse Proxy**: protege al servidor (NGINX)

El cliente cree que habla con un único servidor, pero NGINX decide el backend real.



## 4. Jerarquía de configuración

text
http → server → location


* http: configuración global
* server: dominio / host virtual
* location: enrutado por URL

NGINX aplica siempre la regla **más específica**.



## 5. Aislamiento con Docker

FastAPI **no debe ser público**:

yaml
expose:
  - "8000"


* expose: solo red interna
* ports: Internet

Solo NGINX habla con FastAPI.



## 6. Headers críticos del Reverse Proxy

NGINX traduce la request real hacia FastAPI:

* X-Real-IP
* X-Forwarded-For
* X-Forwarded-Proto
* Host

Sin ellos, FastAPI pierde contexto real del cliente.



## 7. Load Balancing (escalado horizontal)

upstream define un **pool de backends**:

* round_robin (default)
* least_conn
* ip_hash
* weight (GPUs heterogéneas)

Permite:

* paralelismo
* tolerancia a fallos
* escalado real



## 8. HTTPS (obligatorio)

HTTPS ya no es opcional:

* Navegadores bloquean features sin TLS
* HTTP/2 y HTTP/3 lo requieren
* APIs modernas fallan sin HTTPS

**Let's Encrypt**:

* Gratis
* Automático
* Trusted



## 9. Cache para modelos de IA

Si un endpoint es:

* determinista
* idempotente

NGINX puede cachear respuestas:

* reduce latencia
* ahorra GPU
* no cambia código Python

NGINX cachea, FastAPI ni se entera.



## 10. Rate Limiting

Protección crítica:

* evita abusos
* controla costes
* protege GPU

Ejemplos:

* /predict: 10 req/s
* /train: 1 req/min

NGINX es el sitio correcto para esto.



## 11. Logging y observabilidad

NGINX ve **todo el flujo**:

* tiempos totales
* tiempos de backend
* cache HIT/MISS
* errores raros

Permite análisis:

* P50 / P95 / P99
* detección de outliers



## 12. Microservicios con un solo dominio

Path-based routing:

* /api → FastAPI
* /dashboard → Streamlit
* /mlflow → MLflow
* /jupyter → Jupyter

Un dominio, un SSL, una entrada.

NGINX = API Gateway.



## 13. Streaming y WebSockets

Por defecto NGINX **bufferiza** (rompe streaming).

Para streaming:

* proxy_buffering off
* timeouts largos

Esencial para:

* chat tipo GPT
* SSE
* WebSockets
* gRPC



## 14. Optimización de producción

Claves:

* worker_processes auto
* worker_connections altos
* epoll
* gzip
* open_file_cache

Ajustes de kernel Linux incluidos.



## 15. Checklist de arquitectura final

* HTTPS activo
* Reverse proxy
* Load balancing (≥3 réplicas)
* Rate limiting
* Cache de predicciones
* Logs con métricas
* Monitoring (Prometheus/Grafana)


