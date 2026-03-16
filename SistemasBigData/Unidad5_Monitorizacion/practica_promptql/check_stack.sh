#!/usr/bin/env bash
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"

echo "== Comprobación rápida del stack (host) =="

echo "URL Prometheus en el host: http://localhost:9090"

echo "\n-- Prometheus /metrics (primeras líneas) --"
if command -v curl >/dev/null 2>&1; then
  curl -sS http://localhost:9090/metrics | sed -n '1,10p'
  echo "HTTP status:" $(curl -sS -o /dev/null -w '%{http_code}\n' http://localhost:9090/metrics)
else
  echo "curl no está instalado en el host. Instala curl para ejecutar estas comprobaciones." >&2
fi

echo "\n-- Node Exporter /metrics (primeras líneas) --"
if command -v curl >/dev/null 2>&1; then
  curl -sS http://localhost:9100/metrics | sed -n '1,10p'
  echo "HTTP status:" $(curl -sS -o /dev/null -w '%{http_code}\n' http://localhost:9100/metrics)
fi

echo "\n-- Estado de targets desde API de Prometheus --"
if command -v jq >/dev/null 2>&1; then
  curl -sS http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {scrapePool: .scrapePool, health: .health, lastScrape: .lastScrape, scrapedUrl: .scrapeUrl}'
else
  echo "jq no está instalado; muestro la API cruda:" 
  curl -sS http://localhost:9090/api/v1/targets | sed -n '1,120p'
fi

echo "\n-- Contenedores Docker actuales (docker ps) --"
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

cat <<'EOF'

Notas/explicación rápida:
- Después de configurar los servicios en `network_mode: host`, los contenedores no tendrán la IP de red bridge (p.ej. 172.19.x.x). Para acceder a Prometheus desde tu navegador usa:
    http://localhost:9090
  y para Node Exporter:
    http://localhost:9100

- Si la configuración fuera bridge y quisieras comprobar accesibilidad desde dentro de la red de Docker, ejecutarías un contenedor temporal con curl conectado a la red (ejemplo):
    docker run --rm --network nosubir_monitoring curlimages/curl:8.4.0 -sS -I http://node-exporter:9100/metrics
  (esto prueba resolución por nombre de servicio `node-exporter`).

- `curl -sS` silencia la barra de progreso pero muestra errores; `-I` solicita HEAD (algunos endpoints devuelven 405 para HEAD), y `-o /dev/null -w '%{http_code}'` es útil para comprobar solo el código HTTP.
EOF

exit 0
