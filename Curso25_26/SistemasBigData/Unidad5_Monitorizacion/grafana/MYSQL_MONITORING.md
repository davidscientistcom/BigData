# Monitorización de MySQL con Prometheus y Grafana (Stack independiente)

## Objetivo
Este directorio contiene una práctica autocontenida para monitorizar un MySQL con Prometheus y visualizar en Grafana, **separada** del `monitoring-lab`.

## Contenido
- `docker-compose.yml` — stack con Prometheus, Grafana, MySQL, mysqld_exporter, node_exporter y cAdvisor.
- `prometheus/prometheus.yml` — configuración de scrape para mysqld_exporter.
- `mysql/init.sql` — inicialización de la base de datos y creación del usuario `exporter`.
- `scripts/` — script para añadir datos en caliente.

## Notas
- Este stack es independiente: si ejecutas ambos (monitoring-lab y este) en la misma host, puedes tener **conflictos de puertos** (9090, 3000, 3306...). Ejecuta uno a la vez o ajusta los puertos en `docker-compose.yml`.
- Para inicializar datos adicionales:
  ```bash
  chmod +x scripts/populate_mysql.sh
  ./scripts/populate_mysql.sh
  ```

Fecha: 20-01-2026
