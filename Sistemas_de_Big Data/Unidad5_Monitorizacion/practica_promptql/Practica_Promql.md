# Práctica Autoguiada: Monitorización con Prometheus y PromQL

## Introducción

En esta práctica aprenderás a utilizar **PromQL** (Prometheus Query Language), el lenguaje de consultas de Prometheus, para analizar métricas de tu sistema. Asumimos que ya conoces Docker Compose y has instalado Prometheus en prácticas anteriores.[^1][^2]

## Configuración del Entorno

### Archivos en esta carpeta

- `docker-compose.yml` — definición del stack (se mantiene como copia de trabajo en esta práctica).
- `prometheus.yml` — configuración que Prometheus carga al arrancar (en este repo apunta a `localhost` cuando se usa `host` network mode).
- `check_stack.sh` — script de comprobación rápida desde el host (métricas, API targets, docker ps).
- `PromQL_Examples.md` — ejemplos adicionales y consultas sugeridas.
- `README.md` — diagnóstico y comandos útiles.

### Docker Compose (resumen)

El repositorio contiene un `docker-compose.yml` con dos servicios: `prometheus` y `node-exporter`. En entornos de laboratorio hemos ejecutado ambos servicios con `network_mode: "host"` para que los enlaces en la UI apunten a `localhost` y sean clicables desde el navegador del host. Esto facilita el uso en redes institucionales donde el tráfico entre la red bridge y el host puede estar restringido.

Si prefieres el modo recomendado para entornos aislados, elimina `network_mode: "host"` de los servicios y publica los puertos con `ports:`; en ese caso `prometheus.yml` puede usar los nombres de servicio (`prometheus:9090`, `node-exporter:9100`) como targets.

### Archivo de Configuración de Prometheus (actual)

El `prometheus.yml` que se usa en esta práctica está configurado para entornos donde Prometheus corre en `host` network mode y por eso apunta a `localhost`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']
```

Nota: para usar nombres de servicio en lugar de `localhost` (bridge network), reemplaza `localhost` por `prometheus` y `node-exporter` y asegúrate de que los servicios no usan `network_mode: "host"`.

### Verificación rápida (útil para alumnos)

Pasos básicos:
- Levanta el stack: `docker compose up -d`
- Comprueba contenedores: `docker compose ps` o `docker ps`
- Ejecuta el comprobador rápido: `./check_stack.sh` (muestra primeras líneas de métricas, código HTTP y estado de targets en la API de Prometheus)

Comandos manuales de verificación (si quieres entender qué hace `check_stack.sh`):

- Obtener las primeras líneas de métricas de Prometheus:
  - `curl -sS http://localhost:9090/metrics | sed -n '1,12p'`
- Obtener las primeras líneas de Node Exporter:
  - `curl -sS http://localhost:9100/metrics | sed -n '1,12p'`
- Ver el estado de scraping desde la API de Prometheus:
  - `curl -sS http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {scrapePool: .scrapePool, health: .health, scrapedUrl: .scrapeUrl}'`

Nota: algunas imágenes base no incluyen utilidades como `curl` o `nslookup`. Para pruebas dentro de la red bridge usa un contenedor efímero con `curlimages/curl` y la opción `--network`:

```bash
docker run --rm --network <compose_network_name> curlimages/curl:8.4.0 -sS -I http://node-exporter:9100/metrics
```

Este comando te permite probar resolución y conectividad desde dentro de la red de Compose.

### Explicación de los comandos de verificación

Los comandos que usamos para comprobar el estado y diagnosticar problemas son sencillos pero potentes. Aquí se explica cada uno:

- `curl -sS http://localhost:9090/metrics | sed -n '1,12p'`
  - `-sS`: silencio + mostrar errores. `sed -n '1,12p'` muestra solo las primeras líneas.

- `curl -I http://localhost:9090/metrics`
  - Solicita solo las cabeceras (HEAD). Atención: algunos endpoints devuelven `405` si no soportan HEAD; siempre puedes usar GET si quieres el cuerpo.

- `curl -sS -o /dev/null -w '%{http_code}\n' http://localhost:9090/metrics`
  - Descarta el cuerpo y devuelve solo el código HTTP. Ídeal para scripts que comprueban disponibilidad.

- `curl -sS http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {scrapePool: .scrapePool, health: .health, scrapedUrl: .scrapeUrl}'`
  - Utiliza la API de Prometheus y `jq` para extraer solo lo relevante: qué `scrapeUrl` usa y si el objetivo está `up`.

- `docker run --rm --network nosubir_monitoring curlimages/curl:8.4.0 -sS -I http://node-exporter:9100/metrics`
  - Levanta un contenedor temporal en la red `nosubir_monitoring` para probar resolución y acceso desde dentro de la red. `--rm` borra el contenedor al terminar.

Recomiendo practicar estos comandos para aprender a distinguir problemas de DNS (resolución de nombres), problemas de conectividad (puertos cerrados/firewall) y errores de aplicación (500, 404, etc.).

Si quieres, dejo el `prometheus.yml` original con IPs comentado como ejemplo para estudio, pero en entornos reales evita IPs fijas.
```

### Desplegar el Stack

Ejecuta el siguiente comando para iniciar los servicios:

```bash
docker compose up -d
```

Verifica que los contenedores están funcionando:

```bash
docker compose ps
```

Deberías ver ambos servicios `prometheus` y `node-exporter` en estado `Up` y conectados a la red `monitoring`.

## Acceso a Prometheus

Abre tu navegador y accede a `http://localhost:9090`. Esta es la interfaz web de Prometheus donde ejecutarás las consultas PromQL.[^6]

Para verificar que Node Exporter está enviando métricas correctamente:

- Ve a **Status → Targets** en el menú superior
- Deberías ver ambos jobs (`prometheus` y `node-exporter`) en estado `UP`


## Introducción a PromQL

PromQL es el lenguaje de consultas de Prometheus que permite extraer y analizar métricas almacenadas. Las métricas del Node Exporter tienen el prefijo `node_`.[^7][^8][^1][^6]

### Estructura Básica de una Query

Una consulta PromQL tiene tres componentes principales:[^1]

1. **Nombre de la métrica**: `node_cpu_seconds_total`
2. **Selectores de etiquetas**: `{mode="idle", cpu="0"}`
3. **Rango temporal** (opcional): `[5m]`

## Ejercicios Autoguiados con PromQL

### Nivel 1: Consultas Básicas

#### Ejercicio 1.1: Primera Query Simple

Ejecuta la siguiente consulta en Prometheus para verificar qué targets están activos:[^1]

```promql
up
```

**Pregunta**: ¿Qué valor devuelve esta métrica? ¿Qué significa un valor de 1 vs 0?

#### Ejercicio 1.2: Filtrar por Job

Ahora filtra solo el node-exporter:[^1]

```promql
up{job="node-exporter"}
```


#### Ejercicio 1.3: Explorar Métricas de CPU

Lista todas las series temporales de CPU:[^8]

```promql
node_cpu_seconds_total
```

**Observa**: ¿Cuántas series temporales aparecen? ¿Qué etiquetas (labels) tienen?

#### Ejercicio 1.4: Filtrar por Modo de CPU

Consulta solo el tiempo en modo "idle":[^8]

```promql
node_cpu_seconds_total{mode="idle"}
```


### Nivel 2: Trabajando con Rangos Temporales

#### Ejercicio 2.1: Rango Temporal

Obtén los valores de los últimos 5 minutos:[^2]

```promql
node_cpu_seconds_total{mode="system"}[5m]
```

**Nota**: Este tipo de consulta devuelve un "range vector" y no puede graficarse directamente.[^2]

#### Ejercicio 2.2: Métricas de Memoria

Consulta la memoria disponible:

```promql
node_memory_MemAvailable_bytes
```

Para verlo en GB, divide entre 1024³:

```promql
node_memory_MemAvailable_bytes / 1024 / 1024 / 1024
```


### Nivel 3: Funciones de Agregación

#### Ejercicio 3.1: La Función `rate()`

La función `rate()` calcula la tasa de cambio por segundo de una métrica counter:[^9][^8]

```promql
rate(node_cpu_seconds_total{mode="system"}[1m])
```

**Explicación**: Esta query muestra cuántos segundos de CPU por segundo se están usando en modo sistema, promediados en el último minuto.[^8]

#### Ejercicio 3.2: CPU Total por Core

Para ver el uso total de CPU (todos los modos excepto idle):

```promql
rate(node_cpu_seconds_total{mode!="idle"}[5m])
```


#### Ejercicio 3.3: Agregación con `sum()`

Suma el uso de CPU de todos los cores:

```promql
sum(rate(node_cpu_seconds_total{mode!="idle"}[5m]))
```


#### Ejercicio 3.4: Agregación por Etiqueta

Usa `sum by` para mantener la etiqueta `mode`:

```promql
sum by(mode) (rate(node_cpu_seconds_total[5m]))
```

**Pregunta**: ¿Cómo cambia el resultado comparado con la query anterior?

### Nivel 4: Métricas de Red y Disco

#### Ejercicio 4.1: Tráfico de Red

Consulta los bytes recibidos por segundo en la red:[^8]

```promql
rate(node_network_receive_bytes_total[1m])
```


#### Ejercicio 4.2: Tráfico Total de Red

Suma todas las interfaces de red:

```promql
sum(rate(node_network_receive_bytes_total[1m]))
```

Para convertir a MB/s:

```promql
sum(rate(node_network_receive_bytes_total[1m])) / 1024 / 1024
```


#### Ejercicio 4.3: Espacio en Disco

Consulta el espacio disponible en filesystems:[^8]

```promql
node_filesystem_avail_bytes
```

Para ver el porcentaje usado:

```promql
100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)
```


### Nivel 5: Funciones Avanzadas

#### Ejercicio 5.1: La Función `increase()`

La función `increase()` muestra el incremento total en un rango temporal:[^10][^9]

```promql
increase(node_network_transmit_bytes_total[5m])
```

**Diferencia con `rate()`**: `increase()` devuelve el incremento total, mientras que `rate()` devuelve la tasa por segundo.[^9][^10]

#### Ejercicio 5.2: La Función `irate()`

`irate()` calcula una tasa instantánea usando solo las dos últimas muestras:[^9]

```promql
irate(node_cpu_seconds_total{mode="system"}[5m])
```

**Cuándo usar cada función**:

- `rate()`: Para gráficas suavizadas y alertas[^9]
- `irate()`: Para detectar picos de actividad[^9]
- `increase()`: Para valores acumulados totales[^10]


#### Ejercicio 5.3: Predicción Simple

Usa operadores aritméticos para cálculos:

```promql
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100
```

Esto calcula el porcentaje de memoria disponible.

### Nivel 6: Consultas Complejas

#### Ejercicio 6.1: Top 3 CPUs más Utilizadas

```promql
topk(3, rate(node_cpu_seconds_total{mode="system"}[5m]))
```


#### Ejercicio 6.2: Carga del Sistema

```promql
node_load1
```

Compara con el número de CPUs:

```promql
node_load1 / count(count by(cpu) (node_cpu_seconds_total))
```

**Interpretación**: Un valor > 1 indica que el sistema está sobrecargado.

#### Ejercicio 6.3: Interfaces de Red Activas

Filtra interfaces que hayan transmitido datos:

```promql
rate(node_network_transmit_bytes_total[5m]) > 0
```


## Ejercicios de Práctica Autónoma

Ahora que conoces las funciones básicas, intenta responder estas preguntas usando PromQL:

1. **¿Cuánta memoria swap está en uso?**
*Pista: Busca métricas con `node_memory_Swap`*
2. **¿Cuál es la tasa de escritura en disco en bytes/segundo?**
*Pista: Busca métricas `node_disk_written_bytes_total`*
3. **¿Cuántos procesos hay en ejecución?**
*Pista: Busca la métrica `node_procs_running`*
4. **¿Cuál es el porcentaje de uso de CPU en modo "user"?**
*Pista: Usa `rate()` y operaciones aritméticas*
5. **¿Cuántos errores de transmisión de red ha habido en la última hora?**
*Pista: Usa `increase()` con `node_network_transmit_errs_total`*

## Visualización en Gráficas

En la interfaz de Prometheus, puedes cambiar entre las pestañas **Table** y **Graph**:

- **Table**: Muestra valores actuales
- **Graph**: Muestra la evolución temporal (útil para queries con `rate()`, `increase()`, etc.)

Experimenta graficando algunas de las queries anteriores para ver cómo evoluciona el uso de recursos en el tiempo.

## Recursos Adicionales

Para explorar todas las métricas disponibles:

1. Accede a `http://localhost:9100/metrics` (endpoint del Node Exporter)[^11]
2. Ve a **Graph → Metrics Explorer** en Prometheus para buscar métricas por prefijo

## Entrega de la Práctica

Documenta las siguientes consultas PromQL y sus resultados:

1. Cinco consultas básicas de tu elección
2. Tres consultas usando funciones de agregación
3. Dos consultas complejas que combinen múltiples operadores
4. Capturas de pantalla de al menos dos gráficas relevantes

***

**Nota**: Esta práctica te ha permitido trabajar con métricas reales del host y aprender PromQL de forma progresiva. PromQL es fundamental para crear dashboards en Grafana y configurar alertas en Prometheus, temas que se verán en prácticas futuras.[^7]
<span style="display:none">[^12][^13][^14][^15][^16][^17][^18]</span>

<div align="center">⁂</div>

[^1]: https://last9.io/blog/promql-for-beginners-getting-started-with-prometheus-query-language/

[^2]: https://logz.io/blog/promql-examples-introduction/

[^3]: https://grafana.com/docs/grafana-cloud/send-data/metrics/metrics-prometheus/prometheus-config-examples/docker-compose-linux/

[^4]: https://svenvg.com/posts/host-container-monitoring-with-prometheus/

[^5]: https://prometheus.io/docs/guides/node-exporter/

[^6]: https://www.opsramp.com/guides/prometheus-monitoring/prometheus-node-exporter/

[^7]: https://betterstack.com/community/guides/monitoring/promql/

[^8]: https://www.devopsschool.com/blog/prometheus-promql-example-query-node-exporter/

[^9]: https://www.youtube.com/watch?v=7uy_yovtyqw

[^10]: https://dohost.us/index.php/2025/09/28/understanding-rate-vs-increase-in-promql/

[^11]: https://github.com/prometheus/node_exporter

[^12]: https://hub.docker.com/r/prom/node-exporter

[^13]: https://dev.to/rafi021/how-to-set-up-a-monitoring-stack-with-prometheus-grafana-and-node-exporter-using-docker-compose-17cc

[^14]: https://stackoverflow.com/questions/70300286/where-can-i-get-node-exporter-metrics-description

[^15]: https://www.youtube.com/watch?v=RC1ivt-ZN_U

[^16]: https://nsrc.org/workshops/2025/apricot/virt/netmgmt/en/prometheus/ex-promql-basic.html

[^17]: https://docs.giantswarm.io/overview/observability/data-management/data-exploration/advanced-promql-tutorial/

[^18]: https://grafana.com/blog/basics-and-best-practices-for-getting-started-with-promql/

