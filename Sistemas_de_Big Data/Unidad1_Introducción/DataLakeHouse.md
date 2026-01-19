## Qué es un **Data Lakehouse**

Un **Data Lakehouse** es una **arquitectura híbrida** que une lo mejor de los dos mundos:

| Característica | Data Warehouse                                | Data Lake                            | **Data Lakehouse**                 |
| -------------- | --------------------------------------------- | ------------------------------------ | ---------------------------------- |
| Tipo de datos  | Estructurados (tablas, SQL)                   | Todos (crudos, JSON, imágenes, logs) | Todos                              |
| Modelo         | Schema-on-write (transformo antes de guardar) | Schema-on-read (transformo al leer)  | Híbrido                            |
| Procesamiento  | ETL                                           | ELT                                  | ETL y ELT                          |
| Coste          | Alto                                          | Bajo                                 | Moderado                           |
| Rendimiento    | Muy alto (consultas SQL optimizadas)          | Bajo (archivos crudos)               | Alto (usa índices y formatos ACID) |
| Casos de uso   | BI, reporting                                 | Machine Learning, análisis libre     | Ambos                              |

En resumen:

> El Data Lakehouse **mantiene la flexibilidad** y bajo coste del *Data Lake*, pero **añade estructura, transacciones ACID y rendimiento tipo Data Warehouse.**

---

## Cómo funciona internamente

Imagina que tienes un **Data Lake** en la nube (por ejemplo, **Amazon S3**, **Azure Data Lake Storage** o **Google Cloud Storage**) donde guardas todos tus datos crudos.

El *Lakehouse* añade tres capas encima de ese almacenamiento:

### 1️⃣ **Capa de almacenamiento base**

* Guarda los datos en bruto (archivos Parquet, ORC, Avro, etc.).
* Es escalable y barata (almacenamiento de objetos).
* Ejemplo: `/raw/sensores/2025-10-06/temperatura.parquet`.

### 2️⃣ **Capa de metadatos y transacciones (ACID)**

* Añade un **catálogo de tablas** (como en un Data Warehouse) sobre esos archivos.
* Permite hacer **consultas SQL** como si fuera una base de datos.
* Gestiona **transacciones ACID**, control de versiones y *time travel* (puedes consultar los datos “como estaban” ayer).
* Ejemplos de formatos que añaden esta magia:

  * **Delta Lake** (Databricks)
  * **Apache Iceberg** (Netflix, Snowflake)
  * **Apache Hudi** (Uber)

### 3️⃣ **Capa de acceso unificado**

* Herramientas como **Spark SQL**, **Power BI**, **Tableau**, **Presto**, **Trino** o **Databricks SQL** pueden leer directamente las “tablas del lago”.
* Puedes correr *Machine Learning* y *BI* sobre el mismo dataset, sin duplicar datos.


## 🔍 Ejemplo real

### Caso: **Netflix**

* Tiene un **Data Lake** gigante en Amazon S3 con logs, clics, vídeos, etc.
* Usa **Apache Iceberg** como formato de tabla sobre S3.
* Esto convierte esos archivos en **tablas transaccionales**, consultables por Spark, Presto, Trino o Snowflake.
* Así pueden:

  * Hacer *reporting* (BI clásico).
  * Entrenar modelos de recomendación con *Machine Learning*.
  * Todo sin mover ni duplicar los datos.


## 🌟 Ejemplos de **Data Lakehouse famosos**

| Plataforma                             | Tecnología             | Descripción                                                                          |
| -------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------ |
| **Databricks Lakehouse**               | **Delta Lake**         | El más famoso. Mezcla Spark, ML, BI y streaming sobre un mismo lago (S3, ADLS, GCS). |
| **Snowflake Arctic / Polaris Catalog** | **Iceberg**            | Ha adoptado formato abierto y lo combina con motor SQL propietario.                  |
| **Google BigLake**                     | **Iceberg + BigQuery** | Fusiona BigQuery con Data Lake abierto en GCS.                                       |
| **AWS Athena + Glue + S3**             | **Iceberg o Hudi**     | Crea un Lakehouse barato con herramientas nativas de AWS.                            |
| **Apache Hudi (Uber)**                 | **Hudi Tables**        | Permite *upserts* y *time travel* en lagos de datos a gran escala.                   |

