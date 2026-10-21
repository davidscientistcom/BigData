#!/usr/bin/env python3
"""
Simulador de Microservicios para Clúster de Inferencia de IA
Permite arrancar 3 réplicas en puertos 8001, 8002 y 8003 en segundo plano o procesos independientes.
"""
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class ClusterNodeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            "node_port": self.server.server_port,
            "message": f"Respuesta generada por el backend en puerto {self.server.server_port}",
            "status": "healthy"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def log_message(self, format, *args):
        # Silenciar logs verbosos en consola
        pass

def run_server(port):
    server = HTTPServer(('127.0.0.1', port), ClusterNodeHandler)
    print(f"[*] Nodo escuchando en http://127.0.0.1:{port}")
    server.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] != "--all":
        port = int(sys.argv[1])
        run_server(port)
    else:
        # Iniciar los tres nodos simultáneamente en threads para pruebas inmediatas
        ports = [8001, 8002, 8003]
        print("=== Iniciando Clúster de 3 Nodos en Background ===")
        threads = []
        for p in ports:
            t = threading.Thread(target=run_server, args=(p,), daemon=True)
            t.start()
            threads.append(t)
        
        print("✅ Clúster activo. Pulsa Ctrl+C para detener todos los nodos.")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\nDeteniendo nodos del clúster...")
