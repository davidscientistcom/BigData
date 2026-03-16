
# Módulo 0: El Lenguaje de los Datos (Tipología de Variables)

## 0.1. Por qué la Tipología es el Primer Paso

Antes de realizar cualquier análisis o visualización, es *imperativo* comprender la naturaleza de nuestros datos. Una **variable** es una característica, número o cantidad que puede ser medida o contada. Representa un atributo que puede variar entre diferentes individuos, elementos o puntos en el tiempo dentro de un conjunto de datos.

La **tipología de variables** clasifica estas características según sus propiedades matemáticas y cualitativas. ¿Por qué es esto tan crítico?

1.  **Determina las Operaciones Válidas:** No tiene sentido calcular la media de una variable como "Color de ojos" (categórica). La media es para variables numéricas. La moda (el valor más frecuente), en cambio, sí aplica a variables categóricas.
2.  **Guía la Elección de Visualizaciones:** Un *scatterplot* es ideal para explorar la relación entre dos variables numéricas continuas, mientras que un *diagrama de barras* o *countplot* es adecuado para visualizar la frecuencia de categorías. Un *boxplot* es excelente para comparar la distribución de una variable numérica entre diferentes grupos categóricos.
3.  **Condiciona las Pruebas Estadísticas:** Las pruebas estadísticas (que veremos superficialmente aquí y más a fondo en inferencia) tienen supuestos sobre los tipos de variables. Usar una prueba incorrecta (ej., una correlación de Pearson con datos puramente categóricos) invalida los resultados.
4.  **Impacta en el Preprocesamiento y Modelado:** Técnicas como la normalización (Z-score, Min-Max) solo aplican a variables numéricas. Los modelos de Machine Learning a menudo requieren que las variables categóricas se codifiquen numéricamente (ej., One-Hot Encoding).

Ignorar la tipología de variables es uno de los errores más comunes y graves en el análisis de datos. Este módulo establece las bases para evitarlo.

## 0.2. Variables Categóricas (Cualitativas)

Representan características o cualidades que **no pueden medirse numéricamente** en el sentido aritmético tradicional, aunque a veces se codifiquen con números. Se dividen en dos subtipos principales:

### Nominales

Son categorías que **no tienen un orden intrínseco o jerarquía**. Simplemente nombran o etiquetan distintas clases.

* **Ejemplos:**
    * `Color`: ['Rojo', 'Verde', 'Azul']
    * `País`: ['España', 'Francia', 'México']
    * `Estado Civil`: ['Soltero', 'Casado', 'Divorciado']
    * `ID de Sensor`: ['TEMP_A', 'HUM_B', 'PENG_C']
* **Operaciones Típicas:** Conteo de frecuencias (moda), proporciones.
* **Codificación Común:** *One-Hot Encoding* (crear columnas binarias para cada categoría) para muchos modelos de Machine Learning.
* **En Pandas:** A menudo se representan con `dtype` 'object' (si son strings) o 'category'.

### Ordinales

Son categorías que **sí tienen un orden o jerarquía intrínseca**, pero las diferencias entre categorías no son necesariamente iguales o cuantificables.

* **Ejemplos:**
    * `Nivel Educativo`: ['Primaria', 'Secundaria', 'Universidad', 'Doctorado']
    * `Calificación Servicio`: ['Malo', 'Regular', 'Bueno', 'Excelente']
    * `Talla Ropa`: ['S', 'M', 'L', 'XL']
    * `Condición del Hielo`: ['Estable', 'Agrietándose', 'Peligroso'] ('Stable', 'Cracking', 'Hazardous')
* **Operaciones Típicas:** Conteo de frecuencias (moda), mediana (si están codificadas numéricamente respetando el orden), comparaciones de orden (<, >).
* **Codificación Común:** *Label Encoding* o *Integer Encoding* (asignar enteros respetando el orden, ej: 'Malo'=0, 'Regular'=1, 'Bueno'=2) o mantenerlas como tipo 'category' ordenado en Pandas.
* **En Pandas:** Idealmente representadas con `dtype` 'category' especificando el orden.

## 0.3. Variables Numéricas (Cuantitativas)

Representan cantidades que **pueden medirse numéricamente** y con las que se pueden realizar operaciones aritméticas significativas (suma, resta, media, etc.). Se dividen en:

### Discretas

Toman valores numéricos **enteros** y a menudo resultan de **conteos**. No puede haber valores intermedios entre dos valores consecutivos.

* **Ejemplos:**
    * `Número de hijos`: 0, 1, 2, 3...
    * `Cantidad de errores`: 5, 10, 0...
    * `Pingüinos contados`: 150, 210...
* **Operaciones Típicas:** Todas las aritméticas, estadísticas descriptivas (media, mediana, desviación estándar, etc.).
* **En Pandas:** Usualmente `dtype` 'int64'.

### Continuas

Pueden tomar **cualquier valor numérico dentro de un rango** dado. Resultan típicamente de **mediciones**. Teóricamente, entre dos valores siempre puede existir otro.

* **Ejemplos:**
    * `Temperatura`: -10.5 °C, 25.3 °C
    * `Altura`: 1.75 m, 1.68 m
    * `Precio`: 19.99 €, 20.01 €
    * `Humedad`: 85.5 %
* **Operaciones Típicas:** Todas las aritméticas y estadísticas descriptivas.
* **En Pandas:** Usualmente `dtype` 'float64'.

Las variables continuas (y a veces las discretas con muchos valores) se pueden clasificar además según su **escala de medida**:

* **Escala de Intervalo:** El cero es **arbitrario** y no representa ausencia total de la cantidad. Las diferencias entre valores son significativas, pero los cocientes no lo son. (Ej: Temperatura en °C o °F. 0°C no es ausencia de temperatura, y 20°C no es "el doble de caliente" que 10°C).
* **Escala de Razón:** El cero es **absoluto** y representa ausencia total de la cantidad. Tanto las diferencias como los cocientes son significativos. (Ej: Peso, Altura, Precio, Temperatura en Kelvin. 0 Kg es ausencia de peso, y 10 Kg es el doble de peso que 5 Kg).

Esta distinción es más relevante en estadística inferencial y modelado, pero es bueno conocerla.

## 0.4. Tipos Especiales (Mención)

Existen otros tipos de datos comunes en análisis que tienen características particulares:

* **Datos de Texto (Text/NLP):** Cadenas de caracteres largas (ej., reseñas de clientes, artículos de noticias). Requieren técnicas específicas de Procesamiento del Lenguaje Natural (NLP).
* **Datos Temporales (Time Series):** Secuencias de observaciones ordenadas en el tiempo (ej., precios de acciones diarios, mediciones de sensores por hora). Tienen una estructura de dependencia temporal. Lo veremos en detalle en el Módulo 6.
* **Datos Geoespaciales:** Datos asociados a ubicaciones geográficas (ej., coordenadas GPS, polígonos de regiones). Requieren librerías espaciales (como GeoPandas).

## Ejemplos en Python con Pandas

Vamos a usar Pandas para ilustrar cómo trabajar con estos tipos. Primero, generemos un pequeño dataset artificial usando la función que hemos creado (ver `dataset_generator.py`).

```python
import pandas as pd
import numpy as np
# Asumimos que la función generate_antarctic_data está disponible
# from dataset_generator import generate_antarctic_data

# (Aquí iría el código de la función si no estuviera en otro archivo)
def generate_antarctic_data(n_records=100, missing_rate=0.05, outlier_rate=0.02, seed=None):
    """Genera un dataset simulado de una estación antártica."""
    if seed:
        np.random.seed(seed)

    # Sensor IDs (Nominal)
    sensor_ids = ['TEMP_A', 'TEMP_B', 'HUM_A', 'PENG_C', 'ICE_S']
    sensor_id = np.random.choice(sensor_ids, n_records)

    # Timestamp (para después)
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=n_records, freq='h')

    # Temperature (Continuous) - Simulación con paseo aleatorio
    temp_base = np.random.normal(-25, 10)
    temp_trend = np.linspace(0, np.random.choice([-5, 5]), n_records)
    temp_noise = np.random.normal(0, 2, n_records)
    temperature_c = temp_base + temp_trend + temp_noise + np.random.normal(0, 0.5, n_records).cumsum()

    # Humidity (Continuous, 0-100) - Simulación simple
    humidity_perc = np.random.uniform(30, 90, n_records) + np.random.normal(0, 5, n_records)
    humidity_perc = np.clip(humidity_perc, 0, 100) # Asegurar rango

    # Penguin Count (Discrete) - Simulación con Poisson
    avg_penguins = np.random.randint(50, 500)
    penguin_count = np.random.poisson(avg_penguins, n_records)

    # Ice Condition (Ordinal)
    ice_conditions = ['Stable', 'Cracking', 'Hazardous']
    # Probabilidades sesgadas: más estable, menos peligroso
    ice_condition = np.random.choice(ice_conditions, n_records, p=[0.7, 0.25, 0.05])
    ice_condition = pd.Categorical(ice_condition, categories=ice_conditions, ordered=True)


    # Sensor Status (Nominal)
    sensor_statuses = ['OK', 'ERROR', 'MAINTENANCE']
     # Probabilidades sesgadas: la mayoría OK
    sensor_status = np.random.choice(sensor_statuses, n_records, p=[0.9, 0.07, 0.03])

    df = pd.DataFrame({
        'timestamp': timestamps,
        'sensor_id': sensor_id,
        'temperature_c': temperature_c,
        'humidity_perc': humidity_perc,
        'penguin_count': penguin_count,
        'ice_condition': ice_condition,
        'sensor_status': sensor_status
    })

    # Introducir Outliers
    if outlier_rate > 0:
        n_outliers = int(n_records * outlier_rate)
        temp_outlier_indices = np.random.choice(df.index, n_outliers, replace=False)
        # Outliers extremos de temperatura
        df.loc[temp_outlier_indices, 'temperature_c'] += np.random.choice([-1, 1], n_outliers) * np.random.uniform(50, 100, n_outliers)

        count_outlier_indices = np.random.choice(df.index, n_outliers, replace=False)
         # Outliers altos de pingüinos
        df.loc[count_outlier_indices, 'penguin_count'] += np.random.randint(1000, 5000, n_outliers)


    # Introducir Missing Values (NaN)
    if missing_rate > 0:
        mask = np.random.choice([True, False], size=df.shape, p=[missing_rate, 1 - missing_rate])
        # No introducir NaNs en timestamp o sensor_id por simplicidad ahora
        mask[:, 0] = False
        mask[:, 1] = False
        df = df.mask(mask)
         # Asegurarse que ice_condition sigue siendo categórica después de mask
        if 'ice_condition' in df.columns:
             df['ice_condition'] = pd.Categorical(df['ice_condition'], categories=ice_conditions, ordered=True)


    # Mezclar un poco el orden de las filas
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    return df

# Generar un pequeño dataset de ejemplo
antarctic_df_sample = generate_antarctic_data(n_records=10, seed=42)

print("--- Sample Dataset Head ---")
print(antarctic_df_sample.head(10))
print("\n--- Dataset Info ---")
antarctic_df_sample.info()
print("\n--- Dataset dtypes ---")
print(antarctic_df_sample.dtypes)
```

**Salida Esperada (aproximada, los valores aleatorios cambiarán):**

```
--- Sample Dataset Head ---
                  timestamp sensor_id  temperature_c  humidity_perc  penguin_count ice_condition sensor_status
0 2025-10-26 10:01:00+01:00     TEMP_A     -26.680072      65.733076          262.0        Stable            OK
1 2025-10-26 18:01:00+01:00      HUM_A     -29.072524      79.997818            NaN        Stable            OK
2 2025-10-26 11:01:00+01:00      ICE_S     -26.042502      64.032185          278.0           NaN            OK
3 2025-10-26 17:01:00+01:00     TEMP_A     -24.629676      44.757077          250.0        Stable            OK
4 2025-10-26 12:01:00+01:00      HUM_A     -22.956041      70.720880          252.0        Stable            OK
5 2025-10-26 15:01:00+01:00     TEMP_B     -24.965747      49.560771          288.0        Stable            OK
6 2025-10-26 19:01:00+01:00     TEMP_B     -32.990422      69.096756          244.0      Cracking            OK
7 2025-10-26 16:01:00+01:00     TEMP_A     -25.040183      82.463319          247.0           NaN            OK
8 2025-10-26 14:01:00+01:00     TEMP_A     -24.156644      70.198357          263.0        Stable            OK
9 2025-10-26 13:01:00+01:00     PENG_C      -8.107058      57.733830         1281.0        Stable            OK

--- Dataset Info ---
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10 entries, 0 to 9
Data columns (total 7 columns):
 #   Column         Non-Null Count  Dtype
---  ------         --------------  -----
 0   timestamp      10 non-null     datetime64[ns, Europe/Madrid]
 1   sensor_id      10 non-null     object
 2   temperature_c  10 non-null     float64
 3   humidity_perc  10 non-null     float64
 4   penguin_count  9 non-null      float64
 5   ice_condition  8 non-null      category
 6   sensor_status  10 non-null     object
dtypes: category(1), datetime64[ns, Europe/Madrid](1), float64(3), object(2)
memory usage: 926.0+ bytes

--- Dataset dtypes ---
timestamp        datetime64[ns, Europe/Madrid]
sensor_id                              object
temperature_c                         float64
humidity_perc                         float64
penguin_count                         float64
ice_condition                        category
sensor_status                          object
dtype: object
```

**Observaciones de la Salida:**

* `df.info()` y `df.dtypes` nos muestran los tipos de datos inferidos o establecidos por Pandas.
* `timestamp` es reconocido como fecha/hora (`datetime64`).
* `sensor_id` y `sensor_status` son `object`, indicando cadenas de texto (Categóricas Nominales). Podríamos convertirlas a tipo `category` para optimizar memoria si fueran muchas.
* `temperature_c` y `humidity_perc` son `float64` (Numéricas Continuas).
* `penguin_count` es `float64` *debido a la introducción de NaN*. Si no hubiera NaNs, sería `int64` (Numérica Discreta). Pandas a menudo convierte enteros a flotantes para poder usar `NaN`.
* `ice_condition` es `category` (Categórica Ordinal). `info()` nos dice cuánta memoria usa.
* Vemos valores `NaN` (Not a Number) donde introdujimos valores faltantes.


