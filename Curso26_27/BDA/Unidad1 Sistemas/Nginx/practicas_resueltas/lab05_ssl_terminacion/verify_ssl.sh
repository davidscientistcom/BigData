#!/bin/bash
# ==============================================================================
# Script de Verificación de Redirección HTTP 301 y Cifrado HTTPS
# ==============================================================================
echo "=== TEST 1: Comprobando Redirección en Puerto HTTP 8080 ==="
curl -s -I http://localhost:8080/dashboard | grep -E "HTTP|Location"

echo -e "\n=== TEST 2: Comprobando Cifrado HTTPS en Puerto 8443 ==="
# -k omite el error por ser certificado autofirmado (Self-Signed)
curl -s -k -I https://localhost:8443/ | grep -E "HTTP|Strict-Transport-Security|Server"

echo -e "\n=== TEST 3: Inspeccionando Datos de la Conexión SSL con OpenSSL ==="
echo | openssl s_client -connect localhost:8443 -servername localhost 2>/dev/null | grep -E "Protocol|Cipher"
