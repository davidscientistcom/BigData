#!/bin/bash
# ==============================================================================
# Generador de Certificado Autofirmado X.509 de 2048 bits para NGINX
# ==============================================================================
set -e

mkdir -p certs

echo "[*] Generando clave privada RSA y certificado digital autofirmado..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/server.key \
  -out certs/server.crt \
  -subj "/C=ES/ST=Alicante/L=SanVicente/O=IESSanVicente/CN=localhost"

chmod 600 certs/server.key
chmod 644 certs/server.crt

echo "[+] Certificado generado con éxito en certs/server.crt"
echo "[+] Clave privada guardada de forma segura en certs/server.key"
