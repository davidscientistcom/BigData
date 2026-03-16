# Apuntes: Formatos de Datos en Big Data e IA

## Introducción: ¿Por qué necesitamos diferentes formatos?

En Big Data, el formato de almacenamiento de los datos impacta directamente en el **rendimiento**, el **coste** y la **escalabilidad** de nuestras soluciones. Los formatos tradicionales como CSV o JSON son legibles para humanos, pero ineficientes para grandes volúmenes. Los formatos especializados (Avro, Parquet, ORC, Protocol Buffers) optimizan aspectos como compresión, velocidad de lectura, y evolución del esquema. [datacamp](https://www.datacamp.com/es/blog/avro-vs-parquet)

## Formatos Basados en Texto

### CSV (Comma-Separated Values)

**Características:**
- Formato más simple: valores separados por delimitadores (comas, tabuladores)
- Legible por humanos, sin metadatos de esquema
- Ocupa mucho espacio sin compresión

**Ventajas:**
- Universal: compatible con cualquier herramienta
- Fácil de generar y leer
- Ideal para datos tabulares simples

**Desventajas:**
- Sin tipos de datos definidos (todo se interpreta como texto)
- Sin compresión nativa
- No soporta estructuras jerárquicas o anidadas
- Costoso en términos de almacenamiento y consulta [aitor-medrano.github](https://aitor-medrano.github.io/iabd2223/hadoop/04formatos.html)

**Ejemplo de uso:**
```csv
id,nombre,edad,ciudad
1,Ana,28,Valencia
2,Carlos,35,Madrid
```

**Caso de uso:** Exportaciones simples, intercambio con herramientas de ofimática, datasets pequeños para análisis exploratorio.

### JSON (JavaScript Object Notation)

**Características:**
- Formato de texto basado en pares clave-valor
- Soporta estructuras jerárquicas y anidadas
- Almacena datos y esquema juntos (autodescriptivo)

**Ventajas:**
- Legible por humanos
- Soporta datos complejos y anidados
- Ampliamente adoptado en APIs REST
- Compatible con la mayoría de lenguajes de programación

**Desventajas:**
- Muy verboso: repite nombres de campos en cada registro
- Sin compresión nativa (archivos muy grandes) [opensistemas](https://opensistemas.com/5-beneficios-de-avro-y-parquet/)
- Lento para parsear en grandes volúmenes
- No optimizado para consultas analíticas

**Ejemplo de uso:**
```json
{
  "id": 1,
  "nombre": "Ana",
  "edad": 28,
  "direccion": {
    "ciudad": "Valencia",
    "cp": "46001"
  }
}
```

**Caso de uso:** APIs REST, configuraciones, logs semi-estructurados, mensajes en colas de baja frecuencia.

### XML (eXtensible Markup Language)

**Características:**
- Lenguaje de marcado con etiquetas anidadas
- Muy verboso y con alta redundancia
- Soporta validación mediante DTD o XSD

**Ventajas:**
- Soporta estructuras complejas con metadatos ricos
- Estándar maduro con muchas herramientas
- Validación de esquema robusta

**Desventajas:**
- Extremadamente verboso (3-10 veces más grande que alternativas binarias) [ionos](https://www.ionos.es/digitalguide/paginas-web/desarrollo-web/protocol-buffers/)
- Lento de parsear (20-100 veces más lento que Protocol Buffers) [ionos](https://www.ionos.com/es-us/digitalguide/paginas-web/desarrollo-web/protocol-buffers/)
- Ineficiente para Big Data
- Poco usado en pipelines modernos

**Ejemplo de uso:**
```xml
<persona>
  <id>1</id>
  <nombre>Ana</nombre>
  <edad>28</edad>
  <direccion>
    <ciudad>Valencia</ciudad>
  </direccion>
</persona>
```

**Caso de uso:** Sistemas legacy, SOAP web services, configuraciones empresariales. En Big Data prácticamente obsoleto.

## Formatos Binarios Especializados

### Apache Avro

**Características:**
- Formato **orientado a filas** (row-based)
- Esquema definido en JSON, datos en binario compacto
- **Evolución de esquema** dinámica: soporta cambios sin romper pipelines [astera](https://www.astera.com/es/type/blog/avro-vs-parquet-is-one-better-than-the-other/)
- Formato **splittable** (divisible para procesamiento distribuido) [aitor-medrano.github](https://aitor-medrano.github.io/iabd/de/formatos.html)

**Ventajas:**
- Muy eficiente para **escrituras rápidas** e ingestión en streaming
- Evolución de esquema: permite añadir/quitar campos manteniendo compatibilidad
- Esquema y datos en el mismo archivo (autodescriptivo)
- Excelente para serialización en mensajería (Kafka)
- Menor tamaño que JSON o CSV

**Desventajas:**
- No optimizado para consultas analíticas columnar
- Mayor tamaño de archivo que Parquet o ORC
- Compresión menos eficiente que formatos columnares [datacamp](https://www.datacamp.com/es/blog/avro-vs-parquet)

**Ejemplo de esquema (.avsc):**
```json
{
  "type": "record",
  "name": "Usuario",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "nombre", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

**Herramientas:**
- **Apache Kafka:** formato preferido para serialización de mensajes [stackoverflow](https://stackoverflow.com/questions/57305078/can-kafka-brokers-store-data-not-only-in-binary-format-but-also-avro-json-and)
- **Apache NiFi:** procesadores nativos para Avro (ConvertRecord, ConvertAvroToJSON) [ibm](https://www.ibm.com/docs/es/tncm-p/1.4.6?topic=packs-setting-up-apache-nifi)
- Hadoop ecosystem: Hive, Pig, Spark

**Caso de uso ideal:**
- Ingestión de datos en streaming (IoT, logs, eventos en tiempo real) [datacamp](https://www.datacamp.com/es/blog/avro-vs-parquet)
- Pipelines ETL intermedios con esquemas cambiantes
- Serialización en Apache Kafka
- Cuando prima la **velocidad de escritura** sobre la lectura

### Apache Parquet

**Características:**
- Formato **orientado a columnas** (columnar storage)
- Compresión avanzada: codificación de diccionario, RLE (Run-Length Encoding), bit packing [datacamp](https://www.datacamp.com/es/blog/avro-vs-parquet)
- Optimizado para consultas analíticas que leen subconjuntos de columnas
- Metadatos ricos con estadísticas por columna

**Ventajas:**
- **Compresión superior:** reduce tamaño 80-90% vs CSV [aitor-medrano.github](https://aitor-medrano.github.io/iabd2223/hadoop/04formatos.html)
- Consultas analíticas muy rápidas (solo lee columnas necesarias)
- Reduce costes de I/O y almacenamiento en cloud (AWS Athena, Snowflake) [techsyncer](https://www.techsyncer.com/es/performance-and-cost-implications-parquet-avro-orc.html)
- Excelente con Spark, Hive, Presto, Impala
- Soporta tipos de datos complejos y anidados

**Desventajas:**
- Escrituras más lentas que Avro (optimiza para lectura)
- No ideal para acceso a registros completos (row-based)
- Evolución de esquema más limitada que Avro

**Ejemplo de uso en PySpark:**
```python
# Escribir Parquet
df.write.parquet("hdfs://ruta/datos.parquet", mode="overwrite", compression="snappy")

# Leer Parquet
df = spark.read.parquet("hdfs://ruta/datos.parquet")
df.select("columna1", "columna3").filter(df.edad > 25).show()
```

**Herramientas:**
- **Apache Spark:** formato predeterminado para análisis
- Data lakes: AWS S3 + Athena, Google BigQuery, Azure Synapse
- Apache NiFi: procesadores PutParquet, ConvertAvroToParquet

**Caso de uso ideal:**
- **Almacenamiento final** en Data Lakes para análisis [datacamp](https://www.datacamp.com/es/blog/avro-vs-parquet)
- Consultas BI y dashboards (solo se escanean columnas necesarias)
- Reducción de costes en cloud (menor escaneo = menor coste)
- Procesamiento batch con Spark

### Apache ORC (Optimized Row Columnar)

**Características:**
- Formato **columnar** similar a Parquet
- Diseñado originalmente para **Hive** en el ecosistema Hadoop
- Indexación avanzada y predicate pushdown
- Estadísticas integradas por bloque y stripe

**Ventajas:**
- Compresión aún más eficiente que Parquet en algunos casos [techsyncer](https://www.techsyncer.com/es/performance-and-cost-implications-parquet-avro-orc.html)
- Excelente rendimiento en consultas de agregación y joins [techsyncer](https://www.techsyncer.com/es/performance-and-cost-implications-parquet-avro-orc.html)
- Predicate pushdown: saltea bloques que no cumplen filtros
- Optimizado para cargas pesadas en Hive

**Desventajas:**
- Menor adopción fuera del ecosistema Hadoop
- Menos soporte en herramientas cloud vs Parquet
- Curva de aprendizaje similar a Parquet

**Ejemplo de uso en Hive:**
```sql
CREATE TABLE usuarios_orc (
  id INT,
  nombre STRING,
  edad INT
) STORED AS ORC;

INSERT INTO usuarios_orc SELECT * FROM usuarios_csv;
```

**Herramientas:**
- Apache Hive (formato nativo)
- Apache Spark
- Presto, Impala

**Caso de uso ideal:**
- Entornos Hadoop con Hive como motor principal [coffeeandtips](https://www.coffeeandtips.com/post/parquet-vs-avro-vs-orc-qual-formato-de-arquivo-escolher-no-seu-projeto-de-dados)
- Consultas complejas con joins y agregaciones [techsyncer](https://www.techsyncer.com/es/performance-and-cost-implications-parquet-avro-orc.html)
- Procesamiento batch de alto rendimiento

### Protocol Buffers (Protobuf)

**Características:**
- Sistema de serialización binaria desarrollado por **Google**
- Requiere definir esquema en archivos `.proto`
- Genera código automáticamente para múltiples lenguajes
- Formato muy compacto y extremadamente rápido [ionos](https://www.ionos.es/digitalguide/paginas-web/desarrollo-web/protocol-buffers/)

**Ventajas:**
- **3-10 veces más pequeño** que XML [ionos](https://www.ionos.com/es-us/digitalguide/paginas-web/desarrollo-web/protocol-buffers/)
- **20-100 veces más rápido** de parsear que XML [ionos](https://www.ionos.com/es-us/digitalguide/paginas-web/desarrollo-web/protocol-buffers/)
- Fuertemente tipado: contratos claros entre sistemas
- Compatibilidad hacia atrás y adelante (evolución controlada)
- Ideal para comunicación entre microservicios

**Desventajas:**
- No legible por humanos (binario puro)
- Requiere compilar archivos `.proto` para generar código
- Menos usado en Big Data analítico (más en sistemas distribuidos)
- No es splittable como Avro

**Ejemplo de definición (.proto):**
```protobuf
syntax = "proto3";

message Usuario {
  int32 id = 1;
  string nombre = 2;
  string email = 3;
  int32 edad = 4;
}
```

**Herramientas:**
- **gRPC:** comunicación eficiente entre microservicios [profile](https://profile.es/blog/grpc-protobuf-para-microservicios/)
- Apache Kafka: alternativa a Avro para serialización
- Sistemas de mensajería de baja latencia

**Caso de uso ideal:**
- Comunicación entre microservicios (gRPC)
- Sistemas de baja latencia donde cada byte y microsegundo cuenta
- APIs internas (no REST público)
- Streaming de alto rendimiento

## Tabla Comparativa

| **Formato** | **Tipo** | **Compresión** | **Velocidad Lectura** | **Velocidad Escritura** | **Evolución Esquema** | **Caso de Uso Principal** |
|-------------|----------|----------------|-----------------------|-------------------------|-----------------------|---------------------------|
| **CSV** | Texto | Baja | Lenta | Rápida | No | Intercambio simple, exports |
| **JSON** | Texto | Baja | Lenta | Media | Limitada | APIs, logs, configs |
| **XML** | Texto | Muy baja | Muy lenta | Media | Buena | Legacy, SOAP (obsoleto en BD) |
| **Avro** | Binario (filas) | Media | Media | **Muy rápida** | **Excelente** | Streaming, Kafka, ingestión |
| **Parquet** | Binario (columnar) | **Muy alta** | **Muy rápida** | Lenta | Limitada | Análisis, Data Lakes, BI |
| **ORC** | Binario (columnar) | **Muy alta** | **Muy rápida** | Lenta | Limitada | Hive, queries complejas |
| **Protobuf** | Binario | Alta | **Extremadamente rápida** | Rápida | Buena | gRPC, microservicios |

 [astera](https://www.astera.com/es/type/blog/avro-vs-parquet-is-one-better-than-the-other/)

## Integración con Apache Kafka y NiFi

### Apache Kafka

Kafka almacena mensajes como **byte arrays** (binario puro), pero los **serializadores/deserializadores** convierten objetos a bytes. [stackoverflow](https://stackoverflow.com/questions/57305078/can-kafka-brokers-store-data-not-only-in-binary-format-but-also-avro-json-and)

**Formatos más usados en Kafka:**
1. **Avro** (con Schema Registry): formato preferido para streaming [learn.microsoft](https://learn.microsoft.com/es-es/azure/databricks/structured-streaming/avro-dataframe)
   - Schema Registry centraliza esquemas y gestiona evolución
   - Eficiente, compacto, y con versionado de esquemas
   
2. **JSON:** fácil de debuggear, pero ineficiente en producción

3. **Protocol Buffers:** alternativa de alto rendimiento a Avro

4. **String:** solo para mensajes simples

**Ejemplo Kafka Producer con Avro:**
```python
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

value_schema = avro.loads('''
{
  "type": "record",
  "name": "Usuario",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "nombre", "type": "string"}
  ]
}
''')

avroProducer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
}, default_value_schema=value_schema)

avroProducer.produce(topic='usuarios', value={"id": 1, "nombre": "Ana"})
```

### Apache NiFi

NiFi soporta múltiples formatos mediante **procesadores** y **Record Readers/Writers**. [aprenderbigdata](https://aprenderbigdata.com/nifi-vs-kafka/)

**Procesadores clave:**
- **ConvertRecord:** conversión universal entre formatos (CSV → Avro, JSON → Parquet, etc.)
- **PublishKafkaRecord / ConsumeKafkaRecord:** integración directa con Kafka
- **ConvertAvroToJSON / ConvertJSONToAvro**
- **PutParquet:** escribir a formato Parquet

**Flujo típico NiFi + Kafka:**
1. NiFi ingesta datos desde múltiples fuentes (sensores, APIs, archivos)
2. Transforma y convierte a **Avro**
3. Publica mensajes Avro a **Kafka**
4. Consumidores (Spark, Flink, otro NiFi) procesan desde Kafka
5. Almacenamiento final en **Parquet** para análisis [ibm](https://www.ibm.com/docs/es/tncm-p/1.4.6?topic=packs-setting-up-apache-nifi)

**Ejemplo de flujo:**
```
GetFile → ConvertRecord (CSV → Avro) → PublishKafkaRecord_2_6 → [Kafka Topic]
```

## Pipeline Completo: Recomendaciones por Etapa

| **Etapa Pipeline** | **Formato Recomendado** | **Razón** |
|--------------------|-----------------------|-----------|
| **Ingestión inicial** (IoT, logs) | Avro, JSON | Escritura rápida, evolución esquema  [datacamp](https://www.datacamp.com/es/blog/avro-vs-parquet) |
| **Streaming** (Kafka) | Avro + Schema Registry | Serialización eficiente, versionado  [learn.microsoft](https://learn.microsoft.com/es-es/azure/databricks/structured-streaming/avro-dataframe) |
| **Procesamiento intermedio** (NiFi, Spark) | Avro | Flexibilidad, compatibilidad  [datacamp](https://www.datacamp.com/es/blog/avro-vs-parquet) |
| **Almacenamiento analítico** (Data Lake) | Parquet, ORC | Compresión máxima, queries rápidas  [datacamp](https://www.datacamp.com/es/blog/avro-vs-parquet) |
| **Comunicación microservicios** | Protocol Buffers | Mínima latencia, contratos fuertes  [profile](https://profile.es/blog/grpc-protobuf-para-microservicios/) |
| **Export/intercambio** | CSV, JSON | Interoperabilidad universal |

## Ejercicios Prácticos Propuestos

### Ejercicio 1: Conversión de formatos
Descarga un dataset CSV público y conviértelo a JSON, Avro y Parquet usando Python (pandas, pyarrow, fastavro). Compara tamaños de archivo y tiempos de lectura.

### Ejercicio 2: Kafka con Avro
Configura un Schema Registry local y crea un producer/consumer Kafka que use Avro. Practica la evolución de esquema añadiendo un campo opcional.

### Ejercicio 3: NiFi pipeline
Crea un flujo NiFi que lea archivos JSON, los convierta a Avro, y los publique en un topic Kafka. Configura un segundo flujo que consuma de Kafka y escriba a Parquet.

### Ejercicio 4: Análisis comparativo Spark
Carga el mismo dataset en formatos CSV, JSON, Parquet y ORC en Spark. Mide el tiempo de ejecución de consultas analíticas (filtros, agregaciones) sobre cada formato.

***

**Conclusión:** La elección del formato depende del **contexto de uso**. Para streaming y evolución de esquemas: **Avro**. Para análisis y almacenamiento: **Parquet/ORC**. Para microservicios: **Protocol Buffers**. Dominar estos formatos es esencial para diseñar pipelines eficientes en Big Data. [coffeeandtips](https://www.coffeeandtips.com/post/parquet-vs-avro-vs-orc-qual-formato-de-arquivo-escolher-no-seu-projeto-de-dados)