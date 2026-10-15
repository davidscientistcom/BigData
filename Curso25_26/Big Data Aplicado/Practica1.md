# Práctica de Laboratorio: Orquestación de Servicios Contenerizados para Gestión Temporal de Tareas

## 1. Introducción y Objetivos
El objetivo fundamental de esta práctica es diseñar, implementar y desplegar una arquitectura de microservicios desacoplada utilizando **Docker** y **Docker Compose**. Los estudiantes deberán demostrar competencia en la creación de APIs RESTful, la gestión de persistencia de datos relacional y la integración de interfaces de usuario, todo ello bajo un entorno aislado y reproducible.

## 2. Arquitectura del Sistema
El sistema, denominado *"ChronoTask"*, se compondrá de tres servicios independientes que se comunicarán a través de redes virtuales definidas por software (SDN) dentro del ecosistema Docker.

### Topología de la Infraestructura
Se requieren tres contenedores operando simultáneamente:

1.  **Capa de Persistencia (Database Service):** Motor de base de datos MariaDB.
2.  **Capa de Lógica de Negocio (Backend Service):** API REST desarrollada en Python con FastAPI.
3.  **Capa de Presentación (Frontend Service):** Interfaz de usuario (tecnología a elección del estudiante: React, Vue, HTML/JS vanilla, Streamlit, etc.).



## 3. Especificación Técnica de Componentes

### 3.1. Contenedor 1: Persistencia (MariaDB)
Este contenedor será responsable de almacenar la integridad de los datos.

* **Imagen Base:** `mariadb:latest` (o una versión LTS específica).
* **Requisitos de Configuración:**
    * Definición de variables de entorno para `ROOT_PASSWORD`, `DATABASE`, `USER` y `PASSWORD` mediante un archivo `.env` (no harcodeadas en el `docker-compose`).
* **Persistencia:** Es **imperativo** el uso de *Docker Volumes* (volúmenes nombrados) para mapear `/var/lib/mysql`. El ciclo de vida de los datos debe ser independiente del ciclo de vida del contenedor (si se destruye el contenedor, los datos deben subsistir).

### 3.2. Contenedor 2: Backend (FastAPI + SQLAlchemy)
Este microservicio actuará como la única puerta de enlace a los datos.

* **Tecnología:** Python 3.x, FastAPI, Uvicorn.
* **ORM (Object-Relational Mapping):** Se utilizará estrictamente **SQLAlchemy** para la abstracción de la base de datos. *Nota: Se proveerá un manual de referencia para la configuración de la sesión y los modelos.*
* **Documentación:** La API debe exponer automáticamente la documentación OpenAPI (Swagger UI) en la ruta `/docs`.
* **Lógica de Negocio (Endpoints):**
    * `POST /tasks`: Registro de una nueva tarea. Campos mínimos: `título`, `descripción`, `fecha_vencimiento`, `estado`.
    * `GET /tasks`: Recuperación de tareas. Este endpoint debe implementar la lógica de filtrado temporal (ver sección 4).
* **Conectividad:** Debe esperar a que el servicio de MariaDB esté saludable antes de iniciar (implementar lógica de *healthcheck* o scripts de *wait-for-it*).

### 3.3. Contenedor 3: Frontend (Cliente)
Interfaz gráfica que consumirá la API del Backend.

* **Requisito de Red:** Este contenedor **NO** debe tener acceso directo a la red del contenedor de base de datos. Toda comunicación debe pasar por el Backend.
* **Puerto:** Debe exponerse en un puerto estándar (ej. 80 o 3000) mapeado al `localhost` del anfitrión.



## 4. Requisitos de UX/UI y Lógica de Filtrado

Para mejorar la carga cognitiva del usuario, se implementará un patrón de diseño de interfaz basado en el **"Enfoque Temporal"**.

### Lógica de Visualización (Backend & Frontend)
El sistema debe comportarse de la siguiente manera para evitar la saturación de información:

1.  **Modo "Foco Inmediato" (Default):**
    * Al cargar la aplicación, el sistema **solo** debe mostrar las tareas cuya `fecha_vencimiento` esté comprendida entre `HOY` y `HOY + 14 días`.
    * El backend debe filtrar esto eficientemente (preferiblemente a nivel de consulta SQL, no recuperando todo y filtrando en memoria).

2.  **Modo "Planificación Extendida" (Flag):**
    * La interfaz debe incluir un mecanismo explícito (un *toggle*, *switch* o *checkbox*) etiquetado como "Mostrar Futuro / Backlog".
    * Al activar este flag, se realizará una nueva petición al backend que devolverá **todas** las tareas pendientes, independientemente de su fecha.



## 5. Requisitos de Orquestación (Docker Compose)

El entregable central es un archivo `docker-compose.yml` que orqueste el despliegue.

* **Redes (Networks):** Se deben definir al menos dos redes para garantizar el aislamiento y la seguridad:
    * `backend-network`: Conecta Backend y Database.
    * `frontend-network`: Conecta Frontend y Backend.
    * *El Frontend no debe poder hacer ping a la Database.*
* **Volúmenes:** Definición explícita del volumen para MariaDB.
* **Build Context:** Los servicios de Backend y Frontend deben construirse a partir de `Dockerfiles` personalizados incluidos en el repositorio del proyecto.



## 6. Criterios de Evaluación

La práctica se evaluará bajo los siguientes parámetros de rigor técnico:

1.  **Reproducibilidad:** El comando `docker-compose up --build` debe levantar todo el entorno sin intervención manual adicional.
2.  **Persistencia:** Tras detener y eliminar los contenedores (`docker-compose down`), al volver a levantarlos, las tareas creadas previamente deben existir.
3.  **Seguridad de Red:** Verificación del aislamiento entre el Frontend y la Base de Datos.
4.  **Calidad del Código:** Uso correcto de SQLAlchemy (definición de Modelos y Schemas Pydantic) y estructura limpia del proyecto FastAPI.
5.  **Funcionalidad UX:** Correcta implementación del filtro de 14 días vs. vista completa.


