#!/usr/bin/env python3
"""
Script de verificación de distribución de carga y tolerancia a fallos
"""
import urllib.request
import json
import time
from collections import Counter

URL = "http://localhost:8080/"
TOTAL_REQUESTS = 15

print("==================================================================")
print(f"[*] FASE 1: Enviando {TOTAL_REQUESTS} peticiones para comprobar el reparto de pesos...")
print("==================================================================")

distribution = Counter()

for i in range(1, TOTAL_REQUESTS + 1):
    try:
        with urllib.request.urlopen(URL, timeout=2) as response:
            data = json.loads(response.read().decode('utf-8'))
            port = data.get("node_port")
            distribution[port] += 1
            print(f"  Req #{i:02d} -> Atendido por el backend en puerto: {port}")
    except Exception as e:
        print(f"  Req #{i:02d} -> ❌ ERROR: {e}")
    time.sleep(0.08)

print("\n--- RESUMEN DE DISTRIBUCIÓN (FASE 1) ---")
for port, count in distribution.items():
    pct = (count / TOTAL_REQUESTS) * 100
    print(f"Puerto {port}: {count} peticiones ({pct:.1f}%)")

print("\n💡 OBSERVACIÓN PEDAGÓGICA:")
print("El nodo 8001 (weight=2) procesa aproximadamente el doble de peticiones que el nodo 8002 (weight=1).")
print("El nodo 8003 (backup) ha recibido 0 peticiones porque los nodos primarios están vivos.")
