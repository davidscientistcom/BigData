import os
from fastapi import FastAPI, Request

app = FastAPI(title="Servicio Micro-Inferencia IA")

NODE_ID = os.getenv("NODE_ID", "Replica-Desconocida")
DEVICE = os.getenv("COMPUTE_DEVICE", "CPU")

@app.get("/api/info")
def info(request: Request):
    return {
        "replica_activa": NODE_ID,
        "dispositivo_computo": DEVICE,
        "ip_vista_por_fastapi": request.client.host,
        "x_real_ip_cliente": request.headers.get("x-real-ip", "No presente"),
        "x_forwarded_for": request.headers.get("x-forwarded-for", "No presente"),
        "host": request.headers.get("host", "No presente")
    }

@app.get("/api/predict")
def predict():
    return {
        "atendido_por": NODE_ID,
        "modelo": "ResNet-50-ONNX",
        "prediccion": "Vehiculo-Autonomo",
        "probabilidad": 0.998
    }
