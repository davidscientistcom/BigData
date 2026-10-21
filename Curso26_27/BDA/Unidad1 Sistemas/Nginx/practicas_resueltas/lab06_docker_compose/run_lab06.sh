#!/bin/bash
# ==============================================================================
# Script de Despliegue Rápido para Lab 06 Multi-Contenedor Docker Compose
# ==============================================================================
set -e

echo "[*] Construyendo y arrancando clúster con Docker Compose..."
docker compose up -d --build

echo -e "\n[+] Clúster levantado. Comprobando estado de contenedores:"
docker compose ps

echo -e "\n[+] Realizando 4 peticiones de prueba a http://localhost/api/info para verificar balanceo:"
for i in {1..4}; do
  echo "--- Petición #$i ---"
  curl -s http://localhost/api/info | grep -o '"replica_activa":"[^"]*"' || true
  sleep 0.5
done

echo -e "\n✅ ¡Listo! Abre http://localhost en tu navegador para ver el dashboard interactivo."
echo "Para detener el clúster: docker compose down"
