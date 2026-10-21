# Nginx desde CERO 

## 0. Idea mental clave (qué es Nginx)

**Nginx NO es tu aplicación**.
Es el **intermediario** entre Internet y tus apps.



## 1. Primer contacto: servir UNA página estática

### Objetivo

Que Nginx sirva un `index.html`. 

### 1.1 Instalar Nginx

En Ubuntu / Debian:

```bash
sudo apt update
sudo apt install nginx
```

Comprueba:

```bash
nginx -v
```

Arranca:

```bash
sudo systemctl start nginx
```

Abre el navegador:

```
http://localhost
```

Si ves “Welcome to nginx” → **todo bien**.



### 1.2 Dónde está la configuración

Archivo principal:

```
/etc/nginx/nginx.conf
```

Pero NO vamos a tocarlo aún.

Nginx carga esto automáticamente:

```
/etc/nginx/conf.d/*.conf
```

Aquí es donde vamos a trabajar.

### 1.3 Nuestra primera config mínima

Crea un archivo:

```bash
sudo nano /etc/nginx/conf.d/01-basic.conf
```

Contenido **mínimo absoluto**:

```nginx
server {
    listen 80;

    location / {
        root /var/www/html;
        index index.html;
    }
}
```

Guarda y prueba:

```bash
sudo nginx -t
sudo nginx -s reload
```

**Explicación**:

* server → un sitio web
* listen 80 → escucha HTTP
* location / → cualquier URL
* root → carpeta física
* index → archivo por defecto

👉 **Eso es Nginx en su forma más pura.**



## 2. Entender los bloques

Piensa así:

```
server = un dominio
location = una regla dentro del dominio
```

Ejemplo:

```
example.com/          → location /
example.com/api       → location /api/
example.com/static    → location /static/
```



## 3. Añadir una segunda ruta

Vamos a crear dos comportamientos distintos.

Config:

```nginx
server {
    listen 80;

    location / {
        root /var/www/html;
        index index.html;
    }

    location /hello {
        return 200 "Hola desde Nginx";
    }
}
```

Reload:

```bash
sudo nginx -s reload
```

Prueba:

```
http://localhost/hello
```

 **Algo Interesante**:

 Nginx decide qué hacer SOLO mirando la URL.



## 4. Introducir el backend (FastAPI)


### Idea clave

* FastAPI escucha en `localhost:8000`
* Nginx escucha en `:80`
* Nginx reenvía las requests


### 4.1 FastAPI mínimo

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/users")
def users():
    return {"users": ["Ana", "Luis"]}
```

Arranca:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```



### 4.2 Primer proxy_pass (sin upstream)

Config:

```nginx
server {
    listen 80;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Reload:

```bash
sudo nginx -s reload
```

Prueba:

```
http://localhost/api/users
```

 Nginx ya habla con FastAPI.



## 5. Qué hace realmente `proxy_pass`

Mentalmente:

```
Cliente → Nginx → FastAPI → Nginx → Cliente
```

Nginx:

1. Recibe la request
2. La copia
3. La manda al backend
4. Espera respuesta
5. La devuelve

Nginx **NO procesa la lógica**, solo transporta.



## 6. Problema real: IP del cliente perdida

FastAPI ve esto:

```
request.client.host = 127.0.0.1
```

Porque **la request viene de Nginx**.

### Solución (headers básicos)

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

👉 Esto es **OBLIGATORIO en producción**.



## 7. Ahora sí: introducir `upstream`

Hasta ahora:

```nginx
proxy_pass http://127.0.0.1:8000;
```

Problema:

* No escala
* No balancea
* No reutiliza conexiones



### 7.1 Upstream mínimo

```nginx
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;

    location /api/ {
        proxy_pass http://backend;
    }
}
```

👉 **Funciona igual**, pero ahora tienes una abstracción.



## 8. Escalar sin tocar el código

```nginx
upstream backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

Para conseguir ésto deberíamos de tener al menos...    

uvicorn app:app --port 8000
uvicorn app:app --port 8001
uvicorn app:app --port 8002
```

Sin cambiar FastAPI.
Sin cambiar frontend.

## 9. Keepalive (optimización real)

Sin keepalive:

* Abrir TCP
* Cerrar TCP
* Abrir TCP
  
Request 1 → abrir TCP → cerrar TCP
Request 2 → abrir TCP → cerrar TCP
Request 3 → abrir TCP → cerrar TCP

Con keepalive:

* Reutilizar conexiones

```nginx
upstream backend {
    server 127.0.0.1:8000;
    keepalive 16;
}

El 16 le dice, Ok! voy a mantener 16 conexiones abiertas con este backend

location /api/ {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
}
```

👉 Menos latencia, menos CPU.

