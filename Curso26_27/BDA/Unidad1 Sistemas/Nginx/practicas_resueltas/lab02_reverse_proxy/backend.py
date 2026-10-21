from fastapi import FastAPI, Request
import uvicorn

app = FastAPI(title="Servicio de Inferencia IA - Backend Privado")

@app.get("/api/info")
def get_client_info(request: Request):
    """
    Inspecciona las cabeceras HTTP que llegan al backend.
    Demuestra la diferencia entre la IP del socket TCP (que será NGINX)
    y las cabeceras X-Real-IP / X-Forwarded-For inyectadas por NGINX.
    """
    return {
        "socket_ip_directa": request.client.host,
        "x_real_ip": request.headers.get("x-real-ip", "NO_CONFIGURADO"),
        "x_forwarded_for": request.headers.get("x-forwarded-for", "NO_CONFIGURADO"),
        "host_header": request.headers.get("host", "NO_CONFIGURADO"),
        "scheme": request.headers.get("x-forwarded-proto", "http"),
        "status": "online"
    }

@app.get("/api/predict")
def predict():
    return {
        "modelo": "BERT-Sentiment-Analyzer",
        "prediccion": "POSITIVO",
        "confianza": 0.994
    }

if __name__ == "__main__":
    print("Iniciando backend FastAPI en puerto 8000 (Solo red local)...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
