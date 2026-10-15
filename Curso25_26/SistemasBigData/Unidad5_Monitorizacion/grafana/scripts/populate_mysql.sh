#!/usr/bin/env bash
set -euo pipefail

# Script que espera a que MySQL esté listo y ejecuta populate_clients.sql
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_FILE="$SCRIPT_DIR/populate_clients.sql"

echo "Esperando a MySQL..."
until docker exec grafana_mysql mysqladmin ping -uroot -prootpass --silent; do
  sleep 2
done

echo "MySQL listo, cargando datos desde $SQL_FILE"
docker exec -i grafana_mysql mysql -uroot -prootpass mydb < "$SQL_FILE"
echo "Datos cargados correctamente." 
