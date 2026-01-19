# Ejemplos de Consultas PromQL

Este documento contiene ejemplos de consultas útiles en PromQL para demostrar las capacidades del lenguaje y cómo se puede utilizar para analizar métricas en Prometheus.

## Ejemplos de Consultas

### 1. **Tasa de cambio de una métrica**
Calcular la tasa de cambio por segundo de una métrica de contador, como el número de solicitudes HTTP:
```promql
rate(http_requests_total[5m])
```
Esto calcula la tasa de cambio promedio de `http_requests_total` en los últimos 5 minutos.



### 2. **Suma de valores por etiqueta**
Sumar los valores de una métrica agrupados por una etiqueta específica, como el método HTTP:
```promql
sum(rate(http_requests_total[5m])) by (method)
```
Esto muestra la tasa de solicitudes HTTP por cada método (GET, POST, etc.).



### 3. **Promedio de uso de CPU por instancia**
Calcular el promedio de uso de CPU por cada instancia:
```promql
avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)
```
Esto muestra el promedio de tiempo de inactividad de la CPU por instancia en los últimos 5 minutos.



### 4. **Porcentaje de errores HTTP 500**
Calcular el porcentaje de solicitudes HTTP que resultaron en errores 500:
```promql
(sum(rate(http_requests_total{status="500"}[5m])) / sum(rate(http_requests_total[5m]))) * 100
```
Esto calcula el porcentaje de errores 500 en las solicitudes HTTP totales en los últimos 5 minutos.



### 5. **Uso de memoria total**
Obtener el uso total de memoria en todos los nodos:
```promql
sum(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
```
Esto calcula la memoria utilizada sumando la memoria total menos la memoria disponible.



### 6. **Número de procesos en ejecución**
Contar el número de procesos en ejecución en cada instancia:
```promql
node_procs_running{instance="<instance_name>"}
```
Esto muestra el número de procesos en ejecución en una instancia específica.



### 7. **Latencia promedio de solicitudes HTTP**
Calcular la latencia promedio de las solicitudes HTTP:
```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```
Esto calcula el percentil 95 de la duración de las solicitudes HTTP en los últimos 5 minutos.



### 8. **Uso de disco por nodo**
Obtener el uso de disco por nodo:
```promql
node_filesystem_size_bytes - node_filesystem_free_bytes
```
Esto calcula el espacio utilizado en el sistema de archivos restando el espacio libre del tamaño total.



### 9. **Número de conexiones activas**
Contar el número de conexiones activas en cada instancia:
```promql
sum(node_netstat_Tcp_CurrEstab) by (instance)
```
Esto muestra el número de conexiones TCP activas por instancia.



### 10. **Carga promedio del sistema**
Obtener la carga promedio del sistema en los últimos 5 minutos:
```promql
avg(node_load1{instance="<instance_name>"})
```
Esto muestra la carga promedio del sistema en una instancia específica.



## Visualización de Gráficas sin Grafana

Aunque Grafana es la herramienta más común para visualizar métricas de Prometheus, también puedes usar la interfaz web de Prometheus para generar gráficas básicas.

### Pasos para ver gráficas en Prometheus
1. Accede a la interfaz web de Prometheus en [http://localhost:9090](http://localhost:9090).
2. Ve a la pestaña **Graph**.
3. Escribe una consulta PromQL en el cuadro de texto (por ejemplo, `rate(http_requests_total[5m])`).
4. Haz clic en el botón **Execute**.
5. Cambia a la vista **Graph** para ver la gráfica generada.



## ¿Qué podemos medir con Prometheus en un entorno Docker Compose?

En un entorno configurado con Docker Compose, Prometheus puede recopilar métricas de los servicios que están siendo monitoreados. A continuación, se describen algunas de las métricas más comunes que se pueden medir y que son de interés en un sistema basado en Linux:

### Métricas del sistema operativo

1. **Uso de CPU**
   - **Métrica**: `node_cpu_seconds_total`
   - **Descripción**: Tiempo total que la CPU ha pasado en diferentes estados (idle, user, system, etc.).
   - **Ejemplo de consulta**:
     ```promql
     rate(node_cpu_seconds_total{mode="user"}[5m])
     ```
     Esto muestra la tasa de uso de CPU en modo usuario en los últimos 5 minutos.

2. **Uso de memoria**
   - **Métrica**: `node_memory_MemAvailable_bytes`, `node_memory_MemTotal_bytes`
   - **Descripción**: Memoria disponible y total en el sistema.
   - **Ejemplo de consulta**:
     ```promql
     (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100
     ```
     Esto calcula el porcentaje de memoria utilizada en el sistema.

3. **Uso de disco**
   - **Métrica**: `node_filesystem_size_bytes`, `node_filesystem_free_bytes`
   - **Descripción**: Tamaño total y espacio libre en los sistemas de archivos.
   - **Ejemplo de consulta**:
     ```promql
     (node_filesystem_size_bytes{fstype!="tmpfs"} - node_filesystem_free_bytes{fstype!="tmpfs"}) / node_filesystem_size_bytes{fstype!="tmpfs"} * 100
     ```
     Esto calcula el porcentaje de uso del sistema de archivos, excluyendo los sistemas de archivos temporales.

4. **Carga del sistema**
   - **Métrica**: `node_load1`, `node_load5`, `node_load15`
   - **Descripción**: Carga promedio del sistema en 1, 5 y 15 minutos.
   - **Ejemplo de consulta**:
     ```promql
     node_load1
     ```
     Esto muestra la carga promedio del sistema en el último minuto.

5. **Número de procesos en ejecución**
   - **Métrica**: `node_procs_running`
   - **Descripción**: Número de procesos que están actualmente en ejecución.
   - **Ejemplo de consulta**:
     ```promql
     node_procs_running
     ```
     Esto muestra el número de procesos en ejecución en el sistema.

### Métricas de red

1. **Conexiones activas**
   - **Métrica**: `node_netstat_Tcp_CurrEstab`
   - **Descripción**: Número de conexiones TCP activas.
   - **Ejemplo de consulta**:
     ```promql
     sum(node_netstat_Tcp_CurrEstab) by (instance)
     ```
     Esto muestra el número de conexiones TCP activas por instancia.

2. **Tráfico de red**
   - **Métrica**: `node_network_receive_bytes_total`, `node_network_transmit_bytes_total`
   - **Descripción**: Bytes recibidos y transmitidos por las interfaces de red.
   - **Ejemplo de consulta**:
     ```promql
     rate(node_network_receive_bytes_total[5m])
     ```
     Esto calcula la tasa de recepción de datos en las interfaces de red en los últimos 5 minutos.

### Métricas de servicios

1. **Solicitudes HTTP**
   - **Métrica**: `http_requests_total`
   - **Descripción**: Número total de solicitudes HTTP recibidas por el servicio.
   - **Ejemplo de consulta**:
     ```promql
     rate(http_requests_total[5m])
     ```
     Esto calcula la tasa de solicitudes HTTP en los últimos 5 minutos.

2. **Errores HTTP**
   - **Métrica**: `http_requests_total{status="500"}`
   - **Descripción**: Número de solicitudes HTTP que resultaron en errores 500.
   - **Ejemplo de consulta**:
     ```promql
     sum(rate(http_requests_total{status="500"}[5m]))
     ```
     Esto muestra la tasa de errores HTTP 500 en los últimos 5 minutos.

Estas métricas son solo algunos ejemplos de lo que se puede medir con Prometheus en un entorno Docker Compose. Dependiendo de los servicios configurados y las métricas que expongan, se pueden realizar consultas más específicas y adaptadas a las necesidades del sistema.
