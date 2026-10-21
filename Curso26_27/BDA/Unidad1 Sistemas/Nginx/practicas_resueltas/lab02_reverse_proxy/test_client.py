#!/usr/bin/env python3
"""
Cliente de prueba para verificar el Reverse Proxy de NGINX hacia FastAPI
"""
import urllib.request
import json

URL = "http://localhost:8080/api/info"

print(f"[*] Consultando endpoint a través de NGINX: {URL}")

try:
    with urllib.request.urlopen(URL) as response:
        status_code = response.getcode()
        body = json.loads(response.read().decode('utf-8'))
        
        print(f"[+] Estado HTTP: {status_code} OK")
        print("[+] Datos recibidos desde FastAPI:")
        print(json.dumps(body, indent=4))
        
        print("\n=== ANÁLISIS DE LAS CABECERAS ===")
        print(f"IP Directa del Socket (NGINX hacia FastAPI): {body.get('socket_ip_directa')}")
        print(f"IP Real Inyectada por NGINX (X-Real-IP):     {body.get('x_real_ip')}")
        print(f"Cadena de Proxies (X-Forwarded-For):        {body.get('x_forwarded_for')}")
        print(f"Host Original Preservado:                   {body.get('host_header')}")
        
        if body.get('x_real_ip') != "NO_CONFIGURADO":
            print("\n✅ ¡ÉXITO! NGINX está inyectando correctamente la IP real del cliente.")
        else:
            print("\n❌ ALERTA: La cabecera X-Real-IP no fue inyectada.")

except urllib.error.URLError as e:
    print(f"[-] Error de conexión: {e}")
    print("[-] Asegúrate de tener arrancados tanto FastAPI (puerto 8000) como NGINX (puerto 8080).")
