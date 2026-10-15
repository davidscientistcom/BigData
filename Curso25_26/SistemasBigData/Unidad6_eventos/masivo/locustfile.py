from locust import HttpUser, task, between

class MiPrimerUsuario(HttpUser):
    # Tiempo de espera entre tareas (segundos)
    wait_time = between(1, 3)

    # Host por defecto (podemos no ponerlo y usar --host en CLI)
    host = "http://localhost:8000"

    @task
    def hola(self):
        self.client.get("/hello")