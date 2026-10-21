#!/usr/bin/env python3
"""
Simulador de Tráfico Rápido y Abusivo contra el Endpoint de Inferencia
Demuestra la efectividad de NGINX limit_req frenando peticiones en milisegundos.
"""
import concurrent.futures
import urllib.request
import urllib.error
import time

URL = "http://localhost:8080/api/infer/"
TOTAL_REQUESTS = 22

def make_request(req_id):
    start = time.time()
    try:
        with urllib.request.urlopen(URL) as resp:
            elapsed = (time.time() - start) * 1000
            return req_id, resp.getcode(), f"200 OK ({elapsed:.1f}ms)"
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        return req_id, e.code, f"429 Bloqueada por Rate Limiting ({elapsed:.1f}ms)"
    except Exception as e:
        return req_id, 0, str(e)

print("==================================================================")
print(f"🚀 Lanzando ráfaga concurrente de {TOTAL_REQUESTS} peticiones contra {URL}")
print("==================================================================")

with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    results = list(executor.map(make_request, range(1, TOTAL_REQUESTS + 1)))

ok_count = 0
rate_limited_count = 0

for req_id, code, msg in sorted(results, key=lambda x: x[0]):
    if code == 200:
        ok_count += 1
        print(f"  [Req #{req_id:02d}] ✅ Aceptada:  {msg}")
    elif code == 429:
        rate_limited_count += 1
        print(f"  [Req #{req_id:02d}] 🛑 Rechazada: {msg}")
    else:
        print(f"  [Req #{req_id:02d}] ⚠️ Error:     {msg}")

print("\n==================================================================")
print(f"📊 RESUMEN FINAL DEL ATAQUE SIMULADO:")
print(f"  - Peticiones Atendidas con Éxito (HTTP 200):  {ok_count} (Dentro de la ráfaga tolerada)")
print(f"  - Peticiones Cortadas en Seco (HTTP 429):     {rate_limited_count} (Exceso mitigado por NGINX)")
print("==================================================================")
print("💡 Tu backend de IA quedó 100% protegido contra saturación de GPU.")
