Recopilación Completa: Curso de Asalto Data ScienceArchivo: curso_data_science_acelerado.mdCurso de Asalto: Python para Data Science (Numpy y Pandas)Filosofía del Curso: "El Anti-Bucle"Objetivo: Abandonar la mentalidad de programador de software (con bucles for para todo) y adoptar la mentalidad de analista de datos (con operaciones vectorizadas).La Regla de Oro: Si estás escribiendo un for loop para iterar sobre filas de un DataFrame, probablemente lo estás haciendo mal. Te costará tiempo de cómputo y, lo que es peor, tiempo de desarrollo.Requisitos: Conocimientos básicos de Python (listas, diccionarios, funciones). Nada más.Módulo 0: La Caja de Herramientas de Python (Sin pandas)El objetivo es aprender las herramientas nativas de Python que nos permiten escribir código conciso y eficiente.Slicing (El Bisturí):lista[start:stop:step].El poder de lista[::-1] (invertir).lista[::2] (elementos alternos).Práctica: Coger los últimos 10 elementos de una lista, coger solo los pares.List Comprehensions (El Nuevo for):Sintaxis: [expresion for item in iterable if condicion].Por qué [x*2 for x in data] es superior a new_list = []; for x in data: new_list.append(x*2).Comprehensions anidadas (con moderación).Práctica: Filtrar una lista de números, convertir una lista de strings a mayúsculas, crear una matriz.Funciones Lambda (Funciones de usar y tirar):Sintaxis: lambda argumentos: expresion.Uso principal: como argumento key en sorted(), min(), max().Uso con map() y filter() (aunque las comprehensions suelen ser más legibles).Práctica: Ordenar una lista de tuplas por su segundo elemento. Ordenar una lista de diccionarios por una clave.Manejo de JSON Nativo (El Formato Universal):import jsonjson.load(f) y json.loads(s): De fichero/string a objeto Python (dict/list).json.dump(obj, f) y json.dumps(obj): De objeto Python a fichero/string.El parámetro indent para la legibilidad.Práctica: Leer un JSON, modificar un valor y volver a guardarlo "bonito" (indentado).Módulo 1: NumPy - Pensar en VectoresEl objetivo es entender el ndarray y cómo nos permite realizar operaciones matemáticas sobre conjuntos de datos enteros de golpe.El ndarray (El Fundamento):Creación: np.array(), np.zeros(), np.ones().El concepto de shape y dtype.reshape(): Cambiando la forma sin cambiar los datos.Aritmética Vectorizada (El "Anti-For"):Operaciones elemento a elemento: arr * 2, arr + 5, arr1 + arr2.Funciones universales (ufuncs): np.sin(), np.exp(), np.log().No se necesitan bucles.Generación de Datos (El Núcleo de tu idea):np.arange() y np.linspace(): Secuencias predecibles.np.random.rand(), np.random.randn(): Distribuciones uniforme y normal.Generación avanzada:np.random.normal(loc, scale, size): La base de la simulación.np.random.poisson(lam, size): Para conteos (ej. pingüinos).np.random.choice(a, size, p): Para datos categóricos (con probabilidades).Práctica: Generar 1000 muestras de una temperatura media de -15°C con desviación de 3°C.Creando el Caos (Datos del Mundo Real):Introduciendo np.nan (Not a Number) para valores faltantes.Generando outliers: Seleccionar índices aleatorios y sumar/restar un valor exagerado.Práctica: Coger el array de temperatura y sustituir un 5% aleatorio por np.nan.Indexación y Máscaras (El Super-Filtro):Slicing 2D: arr[fila, columna].Máscaras Booleanas: El concepto más importante.arr > 0 (devuelve un array de booleanos).arr[arr > 0] (selecciona solo los elementos que cumplen la condición).np.where(condicion, valor_si_true, valor_si_false): El if/else vectorizado.Práctica: En tu array de temperaturas, contar cuántas son bajo cero. Poner a cero todas las temperaturas superiores a 5°C.Módulo 2: Pandas - El Taller de DatosEl objetivo es usar pandas para estructurar, leer, limpiar y agregar datos tabulares. Aquí es donde NumPy y Python se unen.Estructuras Clave: Series y DataFrame:Series: Un ndarray con etiquetas (índice).DataFrame: Un diccionario de Series (columnas).El index: La columna vertebral de pandas.I/O: Leer y Escribir (El Pan de Cada Día):pd.read_csv(): Los parámetros clave (filepath_or_buffer, sep, header, usecols, dtype, parse_dates).pd.read_json(): El parámetro orient (común: 'records', 'columns').df.to_csv() y df.to_json(): Guardando el trabajo (index=False es tu amigo).Práctica: Leer un CSV, seleccionar 3 columnas, guardarlo como JSON.Selección de Datos (El Bisturí v2.0):Selección de columnas: df['columna'], df[['col1', 'col2']].loc (basado en etiqueta/índice): df.loc[etiqueta_fila, etiqueta_columna].iloc (basado en posición numérica): df.iloc[num_fila, num_columna].Selección Booleana (La más usada):df[df['temperature_c'] < -50].df[(df['sensor_id'] == 'TEMP_A') & (df['humidity_perc'] > 90)].Práctica: Seleccionar todas las lecturas del sensor 'PENG_C' donde el conteo sea 0.Diagnóstico y Limpieza (El 80% del Trabajo):El Chequeo Rápido: df.info(), df.describe(), df.dtypes.Valores Únicos: df['col'].unique(), df['col'].value_counts().Tratando con NaN:df.isnull().sum(): El diagnóstico de valores faltantes.df.dropna(subset=...): Eliminar filas/columnas.df.fillna(valor): Rellenar con un valor fijo, la media (df['col'].mean()) o la mediana.df.interpolate(): Relleno inteligente para series temporales.Práctica: Cargar datos con NaNs, contar cuántos hay, y rellenar los numéricos con la media y los categóricos con 'UNKNOWN'.Transformación y Agregación (El "BOOM"):apply(): Aplicar una función (¡o lambda!) a cada fila (axis=1) o columna (axis=0).map(): Sustituir valores en una Series (ideal para categóricos).groupby('col'): El concepto de "Split-Apply-Combine".Agregaciones: df.groupby('sensor_id').mean(), .sum(), .count().df.groupby('sensor_id')['temperature_c'].agg(['mean', 'std']).Práctica: Agrupar por 'sensor_id' y calcular la temperatura media, máxima y mínima de cada sensor.Módulo 3: Proyecto Final - "Estación Antártida"Objetivo: Aplicar todo lo aprendido usando tu función generate_antarctic_data como base.El Código de Nuestro Generadorimport pandas as pd
import numpy as np

def generate_antarctic_data(n_records=100, missing_rate=0.05, outlier_rate=0.02, seed=None):
    """Genera un dataset simulado de una estación antártica."""
    if seed:
        np.random.seed(seed)

    # Sensor IDs (Nominal)
    sensor_ids = ['TEMP_A', 'TEMP_B', 'HUM_A', 'PENG_C', 'ICE_S']
    sensor_id = np.random.choice(sensor_ids, n_records)

    # Timestamp
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=n_records, freq='h')

    # Temperature (Continuous) - Simulación con paseo aleatorio
    temp_base = np.random.normal(-25, 10)
    temp_trend = np.linspace(0, np.random.choice([-5, 5]), n_records)
    temp_noise = np.random.normal(0, 2, n_records)
    temperature_c = temp_base + temp_trend + temp_noise + np.random.normal(0, 0.5, n_records).cumsum()

    # Humidity (Continuous, 0-100)
    humidity_perc = np.random.uniform(30, 90, n_records) + np.random.normal(0, 5, n_records)
    humidity_perc = np.clip(humidity_perc, 0, 100) # Asegurar rango

    # Penguin Count (Discrete) - Simulación con Poisson
    avg_penguins = np.random.randint(50, 500)
    penguin_count = np.random.poisson(avg_penguins, n_records)

    # Ice Condition (Ordinal)
    ice_conditions = ['Stable', 'Cracking', 'Hazardous']
    ice_condition = np.random.choice(ice_conditions, n_records, p=[0.7, 0.25, 0.05])
    ice_condition = pd.Categorical(ice_condition, categories=ice_conditions, ordered=True)

    # Sensor Status (Nominal)
    sensor_statuses = ['OK', 'ERROR', 'MAINTENANCE']
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
        df.loc[temp_outlier_indices, 'temperature_c'] += np.random.choice([-1, 1], n_outliers) * np.random.uniform(50, 100, n_outliers)
        count_outlier_indices = np.random.choice(df.index, n_outliers, replace=False)
        df.loc[count_outlier_indices, 'penguin_count'] += np.random.randint(1000, 5000, n_outliers)

    # Introducir Missing Values (NaN)
    if missing_rate > 0:
        mask = np.random.choice([True, False], size=df.shape, p=[missing_rate, 1 - missing_rate])
        mask[:, 0] = False # No NaNs en timestamp
        mask[:, 1] = False # No NaNs en sensor_id
        df = df.mask(mask)
        if 'ice_condition' in df.columns:
             df['ice_condition'] = pd.Categorical(df['ice_condition'], categories=ice_conditions, ordered=True)

    # Mezclar
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    return df
Prácticas del ProyectoGenerar y Guardar:Genera un dataset de 10.000 filas con seed=42.Guarda este DataFrame "sucio" como antarctic_dirty.csv.Cargar y Diagnosticar:Carga antarctic_dirty.csv (¡cuidado con parse_dates=['timestamp']!).Usa df.info() y df.describe() para entender el desastre.Usa df.isnull().sum() para contar todos los NaN por columna.Limpieza de Faltantes (NaN):Rellena temperature_c y humidity_perc faltantes usando interpolate(method='time') (ya que tenemos timestamp).Rellena penguin_count faltante con 0 (asumimos que si no hay dato, no se contaron).Rellena ice_condition y sensor_status faltantes con el valor 'UNKNOWN'.Detección y Manejo de Outliers:Usando np.where: Crea una nueva columna temp_outlier que sea True si temperature_c es > 20°C o < -80°C (valores físicamente improbables).Usando loc: Filtra y muestra todos los penguin_count > 1500 (¡outliers claros!).Reemplaza estos outliers de penguin_count por np.nan y luego rellénalos con la mediana del sensor 'PENG_C'.Análisis y Agregación:Calcula la temperatura media y la humedad media por cada sensor_id.Encuentra el día (timestamp.dt.date) con el mayor número de pingüinos contados (¡después de limpiar outliers!).Calcula el porcentaje de tiempo que cada sensor estuvo en estado 'ERROR'.Exportación Final:Guarda el DataFrame limpio y analizado como antarctic_analysis_results.json con orient='records'.Archivo: modulo_0_python_avanzado.mdMódulo 0: Python Avanzado - La Caja de HerramientasFilosofía: Antes de correr con numpy y pandas, debemos caminar (muy rápido) con Python nativo. Este módulo asegura que todos dominan las herramientas base para manipular datos de forma eficiente.1. Slicing (El Bisturí)El "slicing" (rebanado) es la forma más rápida de seleccionar subconjuntos de secuencias (listas, tuplas, strings).Sintaxis: secuencia[start:stop:step]start: Índice de inicio (incluido). Si se omite, es 0.stop: Índice de fin (excluido). Si se omite, es hasta el final.step: El "paso". Si se omite, es 1.Ejemplos Básicosdata = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
print(f"Original: {data}")

# Coger los primeros 3 elementos
print(f"Primeros 3: {data[:3]}") # [10, 11, 12]

# Coger desde el índice 5 hasta el final
print(f"Desde índice 5: {data[5:]}") # [15, 16, 17, 18, 19, 20]

# Coger un rango en medio (índices 2, 3, 4)
print(f"De 2 a 5 (excl.): {data[2:5]}") # [12, 13, 14]
Ejemplos Avanzados (Indices Negativos y Step)Los índices negativos cuentan desde el final (-1 es el último elemento).data = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
print(f"Original: {data}")

# Coger los últimos 3 elementos
print(f"Últimos 3: {data[-3:]}") # [18, 19, 20]

# Coger todo EXCEPTO los últimos 2
print(f"Todo menos últimos 2: {data[:-2]}") # [10, ..., 18]

# Coger los elementos en posiciones pares (::step)
print(f"Posiciones pares: {data[::2]}") # [10, 12, 14, 16, 18, 20]

# --- El truco maestro: Invertir una lista ---
print(f"Invertida: {data[::-1]}") # [20, 19, ..., 10]

# Invertir y coger elementos alternos
print(f"Invertida alterna: {data[::-2]}") # [20, 18, 16, 14, 12, 10]
2. List Comprehensions (El Nuevo for)Es la forma "Pythónica" de crear listas. Son más rápidas y legibles que usar un bucle for y .append().Sintaxis: [expresion for item in iterable if condicion]Ejemplo 1: Mapeo (Mapping)Queremos una nueva lista con el cuadrado de cada número.numeros = [1, 2, 3, 4, 5]

# --- Forma tradicional (Lenta y verbosa) ---
cuadrados_for = []
for n in numeros:
    cuadrados_for.append(n * n)
print(f"Con 'for': {cuadrados_for}")

# --- Con List Comprehension (Rápida y elegante) ---
cuadrados_comp = [n * n for n in numeros]
print(f"Con Comp.: {cuadrados_comp}")
Ejemplo 2: Filtrado (Filtering)Queremos solo los números pares de la lista, multiplicados por 10.numeros = [1, 2, 3, 4, 5, 6, 7, 8]

# --- Forma tradicional ---
pares_for = []
for n in numeros:
    if n % 2 == 0:
        pares_for.append(n * 10)
print(f"Con 'for': {pares_for}")

# --- Con List Comprehension ---
# La sintaxis completa: [expresion for item in iterable if condicion]
pares_comp = [n * 10 for n in numeros if n % 2 == 0]
print(f"Con Comp.: {pares_comp}")
Ejemplo 3: Aplanado de Listas (Anidado)Esto es muy común en datos. Tienes una lista de listas y la quieres "plana".matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# --- Forma tradicional ---
plana_for = []
for fila in matriz:
    for numero in fila:
        plana_for.append(numero)
print(f"Con 'for': {plana_for}")

# --- Con List Comprehension (OJO al orden) ---
# El orden es el mismo del 'for', pero "leído" de izquierda a derecha
plana_comp = [numero for fila in matriz for numero in fila]
print(f"Con Comp.: {plana_comp}")
3. Funciones Lambda (Funciones de usar y tirar)Una lambda es una pequeña función anónima. Se limita a una sola expresión. Son increíblemente útiles para pasarlas como argumento a otras funciones.Sintaxis: lambda argumentos: expresionEjemplo 1: sorted() (El uso más común)Tenemos una lista de diccionarios (logs) y queremos ordenarla por la clave 'temperatura'.logs = [
    {'id': 'a', 'temperatura': 25},
    {'id': 'b', 'temperatura': 12},
    {'id': 'c', 'temperatura': 30}
]

# --- Sin lambda (forma larga) ---
def obtener_temp(log):
    return log['temperatura']

ordenados_func = sorted(logs, key=obtener_temp)
# print(f"Ordenados (func): {ordenados_func}")

# --- Con lambda (directo y limpio) ---
# key=lambda log: log['temperatura']
# "Crea una función que, dado un 'log', devuelve log['temperatura']"
ordenados_lambda = sorted(logs, key=lambda log: log['temperatura'])
print(f"Ordenados (lambda): {ordenados_lambda}")

# Ordenar por 'temperatura' en orden descendente
desc_lambda = sorted(logs, key=lambda log: log['temperatura'], reverse=True)
print(f"Ordenados (desc): {desc_lambda}")
Ejemplo 2: map() y filter()map(funcion, iterable) aplica una función a cada elemento.filter(funcion, iterable) filtra elementos donde la función devuelve True.Nota: Las List Comprehensions suelen ser preferidas a map y filter.numeros = [1, 2, 3, 4, 5, 6]

# --- map() ---
# Duplicar cada número
duplicados_map = list(map(lambda x: x * 2, numeros))
print(f"Map (lambda): {duplicados_map}")

# (Equivalente con List Comprehension)
duplicados_comp = [x * 2 for x in numeros]
print(f"Map (comp):   {duplicados_comp}")


# --- filter() ---
# Coger solo los pares
pares_filter = list(filter(lambda x: x % 2 == 0, numeros))
print(f"\nFilter (lambda): {pares_filter}")

# (Equivalente con List Comprehension)
pares_comp = [x for x in numeros if x % 2 == 0]
print(f"Filter (comp):   {pares_comp}")
4. Manejo de JSON Nativo (El Formato Universal)JSON (JavaScript Object Notation) es el estándar de facto para el intercambio de datos. Python lo trata como una combinación de diccionarios y listas.Usamos el módulo json (viene con Python).Ejemplo 1: json.dumps() (De Objeto Python a String)dumps = "dump string" (volcar a cadena)import json

# Objeto Python (diccionario)
data_dict = {
    'estacion': 'Antártida-Base',
    'sensores': [
        {'id': 'TEMP_A', 'valor': -25.5},
        {'id': 'HUM_A', 'valor': 80}
    ],
    'activa': True
}

# Convertir a un string JSON
# `indent=2` lo formatea de forma legible ("pretty-print")
json_string = json.dumps(data_dict, indent=2)

print("--- String JSON (formateado) ---")
print(json_string)

# Convertir a un string JSON (minimizado, para enviar por red)
json_string_mini = json.dumps(data_dict)
print(f"\nString JSON (minimizado): {json_string_mini}")
Ejemplo 2: json.loads() (De String a Objeto Python)loads = "load string" (cargar desde cadena)import json

# Imaginemos que recibimos este string de una API
json_recibido = '{"id_log": 123, "tags": ["error", "sensor_TEMP_B"], "data": {"valor": null}}'

# Convertir de vuelta a un diccionario Python
data_recibida = json.loads(json_recibido)

print(f"\n--- Objeto Python (desde string) ---")
print(f"Diccionario: {data_recibida}")
print(f"Tipo de 'data': {type(data_recibida['data'])}")
# ¡JSON 'null' se convierte en Python 'None'!
print(f"Valor de 'data.valor': {data_recibida['data']['valor']}")
print(f"Segundo tag: {data_recibida['tags'][1]}")
Ejemplo 3: json.dump() y json.load() (De/A Fichero)dump (sin 's') = volcar a ficheroload (sin 's') = cargar desde ficheroimport json

# --- Escribir (dump) a un fichero ---
data_para_guardar = {
    'id_experimento': 'EXP-001',
    'parametros': {'learning_rate': 0.01, 'epochs': 100}
}

# 'w' = write (escribir)
with open('config.json', 'w') as f:
    json.dump(data_para_guardar, f, indent=4)
    
print("\n--- Fichero 'config.json' escrito. ---")

# --- Leer (load) desde un fichero ---
# 'r' = read (leer)
with open('config.json', 'r') as f:
    data_cargada = json.load(f)

print("\n--- Fichero 'config.json' leído: ---")
print(f"Datos cargados: {data_cargada}")
print(f"Epochs: {data_cargada['parametros']['epochs']}")

# (Opcional: limpiar el fichero creado)
# import os
# os.remove('config.json')
Archivo: modulo_0_ejemplos_avanzados.mdMódulo 0 (Avanzado): Ejemplos de TallerFilosofía: Estos ejemplos asumen que se entiende el Módulo 0 (list comprehensions, lambdas, slicing, json). El objetivo aquí es combinar estas técnicas para resolver problemas más realistas de limpieza y transformación de datos, usando solo Python nativo.1. Taller: Limpieza de Logs de ServidorEscenario: Tienes una lista de strings. Cada string es un log de un servidor, pero están "sucios". Algunos son logs de 'ERROR', otros de 'INFO'. Algunos tienen timestamps y otros no.El Reto:Filtrar solo los logs que contienen la palabra 'ERROR'.Extraer el timestamp (si existe) y el mensaje.Estructurar la salida como una lista de diccionarios.print("--- 1. Taller: Limpieza de Logs ---")

logs_sucios = [
    "INFO: [2024-01-01T12:00:00] Servicio iniciado",
    "ERROR: [2024-01-01T12:01:30] Fallo en conexión a DB",
    "DEBUG: Valor x=10",
    "ERROR: [2024-01-01T12:02:00] Sensor TEMP_A time-out",
    "INFO: [2024-01-01T12:03:00] Usuario 'admin' logueado",
    "ERROR: Pánico en el kernel (sin timestamp)"
]

# --- Solución (Combinando técnicas) ---

def parsear_log(log_str):
    """
    Intenta extraer el timestamp y el mensaje de un log.
    Usa Slicing y métodos de string.
    """
    # Suponemos formato: "TIPO: [TIMESTAMP] Mensaje" o "TIPO: Mensaje"
    
    # 1. Quitar el prefijo 'ERROR: ' (Slicing)
    #    (Asumimos que ya ha sido filtrado por 'ERROR')
    mensaje_bruto = log_str[len('ERROR: '):].strip() # .strip() quita espacios
    
    # 2. Comprobar si tiene timestamp
    if mensaje_bruto.startswith('['):
        # Encontrar el ']' que cierra
        end_ts_idx = mensaje_bruto.find(']')
        if end_ts_idx != -1:
            # Slicing para extraer las partes
            timestamp = mensaje_bruto[1:end_ts_idx]
            mensaje = mensaje_bruto[end_ts_idx + 1:].strip()
            return {'timestamp': timestamp, 'mensaje': mensaje, 'raw': log_str}
            
    # Si no tiene timestamp o el formato falla
    return {'timestamp': None, 'mensaje': mensaje_bruto, 'raw': log_str}

# --- La magia (List Comprehensions) ---

# 1. Filtrar los logs de 'ERROR'
logs_error_filtrados = [log for log in logs_sucios if log.startswith('ERROR')]
print(f"Logs filtrados: {logs_error_filtrados}")

# 2. Procesar (parsear) los logs filtrados
logs_limpios = [parsear_log(log) for log in logs_error_filtrados]

print("\n--- Logs Limpios (JSON) ---")
# Usamos json.dumps para ver la salida "bonita"
import json
print(json.dumps(logs_limpios, indent=2))

# Salida esperada:
# [
#   {
#     "timestamp": "2024-01-01T12:01:30",
#     "mensaje": "Fallo en conexión a DB",
#     "raw": "ERROR: [2024-01-01T12:01:30] Fallo en conexión a DB"
#   },
#   {
#     "timestamp": "2024-01-01T12:02:00",
#     "mensaje": "Sensor TEMP_A time-out",
#     "raw": "ERROR: [2024-01-01T12:02:00] Sensor TEMP_A time-out"
#   },
#   {
#     "timestamp": null,
#     "mensaje": "Pánico en el kernel (sin timestamp)",
#     "raw": "ERROR: Pánico en el kernel (sin timestamp)"
#   }
# ]
2. Taller: Desanidar JSON de una APIEscenario: Recibes datos de una API en un formato JSON complejo y anidado. Tu objetivo es "aplanarlo" para hacerlo más fácil de analizar (por ejemplo, para meterlo en un CSV).El Reto:Cargar el string JSON (simulando la respuesta de la API).Transformar la lista de sensores (anidada) en un diccionario "plano" donde la clave sea el sensor_id.Crear una lista final de registros "planos".print("\n--- 2. Taller: Desanidar JSON ---")
import json

api_respuesta_str = """
[
    {
        "id_estacion": "ANT-001",
        "timestamp": "2024-01-01T12:00:00",
        "ubicacion": {"lat": -77.84, "lon": 166.66},
        "lecturas": [
            {"sensor_id": "TEMP_A", "valor": -25.5, "unidad": "C"},
            {"sensor_id": "HUM_A", "valor": 80, "unidad": "%"}
        ]
    },
    {
        "id_estacion": "ANT-001",
        "timestamp": "2024-01-01T13:00:00",
        "ubicacion": {"lat": -77.84, "lon": 166.66},
        "lecturas": [
            {"sensor_id": "TEMP_A", "valor": -26.1, "unidad": "C"},
            {"sensor_id": "HUM_A", "valor": 81, "unidad": "%"},
            {"sensor_id": "PENG_C", "valor": 150, "unidad": "count"}
        ]
    }
]
"""

# 1. Cargar el JSON
data_anidada = json.loads(api_respuesta_str)

# --- Solución (Combinando List Comprehensions y Dicts) ---

registros_planos = []
for registro in data_anidada:
    # 1. Crear la base del registro plano
    base = {
        'id_estacion': registro['id_estacion'],
        'timestamp': registro['timestamp'],
        'latitud': registro['ubicacion']['lat'], # Aplanar 'ubicacion'
        'longitud': registro['ubicacion']['lon']
    }
    
    # 2. Aplanar la lista de 'lecturas'
    #    Usamos una "Dict Comprehension"
    lecturas_planas = {
        lectura['sensor_id']: lectura['valor']
        for lectura in registro['lecturas']
    }
    # (Ej: {'TEMP_A': -25.5, 'HUM_A': 80})
    
    # 3. Combinar los dos diccionarios
    #    El truco (Python 3.9+): base | lecturas_planas
    #    Forma compatible (Python 3.5+): {**base, **lecturas_planas}
    registro_plano = {**base, **lecturas_planas}
    
    registros_planos.append(registro_plano)

print("\n--- Registros Aplanados (JSON) ---")
print(json.dumps(registros_planos, indent=2))

# Salida esperada:
# [
#   {
#     "id_estacion": "ANT-001",
#     "timestamp": "2024-01-01T12:00:00",
#     "latitud": -77.84,
#     "longitud": 166.66,
#     "TEMP_A": -25.5,
#     "HUM_A": 80
#   },
#   {
#     "id_estacion": "ANT-001",
#     "timestamp": "2024-01-01T13:00:00",
#     "latitud": -77.84,
#     "longitud": 166.66,
#     "TEMP_A": -26.1,
#     "HUM_A": 81,
#     "PENG_C": 150
#   }
# ]
# (Nota: Faltan PENG_C en el primero y TEMP_A/HUM_A en el segundo si no los tuviera,
#  esto es normal y se maneja en Pandas como 'NaN')
3. Taller: Agrupar Transacciones por CategoríaEscenario: Tienes una lista larga de transacciones. Cada una es un diccionario. Quieres agruparlas por la clave 'categoria' y calcular el total gastado en cada una.El Reto:Iterar la lista una sola vez.Construir un diccionario que acumule los totales por categoría.(Opcional) Encontrar la categoría con el gasto máximo usando lambda.print("\n--- 3. Taller: Agrupar Transacciones ---")

transacciones = [
    {'id': 1, 'categoria': 'Comida', 'monto': 15.50},
    {'id': 2, 'categoria': 'Transporte', 'monto': 8.00},
    {'id': 3, 'categoria': 'Comida', 'monto': 25.00},
    {'id': 4, 'categoria': 'Ocio', 'monto': 40.00},
    {'id': 5, 'categoria': 'Transporte', 'monto': 12.50},
    {'id': 6, 'categoria': 'Comida', 'monto': 7.25},
]

# --- Solución (Usando un diccionario para agrupar) ---

totales_por_categoria = {}
for t in transacciones:
    categoria = t['categoria']
    monto = t['monto']
    
    if categoria not in totales_por_categoria:
        # Si es la primera vez que vemos esta categoría, la inicializamos
        totales_por_categoria[categoria] = 0.0
        
    # Acumulamos el monto
    totales_por_categoria[categoria] += monto
    
    # (Forma avanzada y corta usando .get())
    # totales_por_categoria[categoria] = totales_por_categoria.get(categoria, 0.0) + monto

print(f"\n--- Totales por Categoría ---")
print(json.dumps(totales_por_categoria, indent=2))
# Salida:
# {
#   "Comida": 47.75,
#   "Transporte": 20.5,
#   "Ocio": 40.0
# }


# --- Reto Opcional: Categoría con Gasto Máximo (Lambda) ---

# .items() convierte {'Comida': 47.75, ...}
# en una lista de tuplas: [('Comida', 47.75), ...]

# Usamos max() con una lambda para decirle que mire el *segundo*
# elemento de la tupla (el monto, índice 1)
categoria_max_gasto = max(
    totales_por_categoria.items(), 
    key=lambda item: item[1]
)

print(f"\nCategoría con gasto máximo: {categoria_max_gasto}")
# Salida: ('Comida', 47.75)
Archivo: modulo_0_desafios_avanzados.mdMódulo 0 (Desafíos): Taller Avanzado IIFilosofía: Más difícil. Estos ejemplos requieren pensar más en la estructura de los datos. El objetivo sigue siendo usar solo herramientas nativas de Python (Módulo 0) para realizar transformaciones complejas.1. Desafío: Normalización de Registros HeterogéneosEscenario: Tienes una lista de registros de sensores. El problema es que vienen de dos sistemas diferentes:Sistema 'A' usa {"sensor_id": ..., "temp": ..., "unit": "C"}Sistema 'B' usa {"device": ..., "reading": ..., "scale": "Fahrenheit"}El Reto:Escribir una función "adaptadora" que normalice cualquier tipo de registro a un formato estándar: {"id": ..., "temperatura_c": ..., "origen": ...}.La función debe convertir Fahrenheit a Celsius: C = (F - 32) * 5/9.Usar una list comprehension para procesar toda la lista sucia.print("--- 1. Desafío: Normalización de Registros Heterogéneos ---")
import json

registros_sucios = [
    {"sensor_id": "T-100", "temp": 25.5, "unit": "C"},
    {"device": "DEV-A", "reading": 77.0, "scale": "Fahrenheit"},
    {"sensor_id": "T-101", "temp": -5.0, "unit": "C"},
    {"device": "DEV-B", "reading": 32.0, "scale": "Fahrenheit"},
    {"sensor_id": "T-100", "temp": 26.0, "unit": "C"},
    {"device": "DEV-A", "reading": 80.6, "scale": "Fahrenheit"}
]

def normalizar_registro(registro):
    """
    Normaliza un registro de sensor heterogéneo a un formato estándar.
    """
    if 'sensor_id' in registro:
        # Es Sistema 'A'
        id_sensor = registro['sensor_id']
        temp_c = registro['temp']
        origen = 'Sistema_A'
    
    elif 'device' in registro:
        # Es Sistema 'B'
        id_sensor = registro['device']
        temp_f = registro['reading']
        # Convertir F a C
        temp_c = (temp_f - 32) * 5 / 9
        origen = 'Sistema_B'
        
    else:
        # Formato desconocido, lo descartamos o marcamos
        return None 
        
    return {
        "id": id_sensor,
        "temperatura_c": round(temp_c, 2), # Redondear a 2 decimales
        "origen": origen
    }

# --- Solución (List Comprehension + filter) ---

# 1. Procesar todo con la list comprehension
registros_normalizados_con_nones = [normalizar_registro(r) for r in registros_sucios]
print(f"Procesados (con Nones): {registros_normalizados_con_nones}")

# 2. Filtrar los 'None' (si los hubiera) usando otra list comprehension
registros_finales = [r for r in registros_normalizados_con_nones if r is not None]

print("\n--- Registros Normalizados (JSON) ---")
print(json.dumps(registros_finales, indent=2))

# Salida esperada:
# [
#   { "id": "T-100", "temperatura_c": 25.5, "origen": "Sistema_A" },
#   { "id": "DEV-A", "temperatura_c": 25.0, "origen": "Sistema_B" },
#   { "id": "T-101", "temperatura_c": -5.0, "origen": "Sistema_A" },
#   { "id": "DEV-B", "temperatura_c": 0.0, "origen": "Sistema_B" },
#   { "id": "T-100", "temperatura_c": 26.0, "origen": "Sistema_A" },
#   { "id": "DEV-A", "temperatura_c": 27.0, "origen": "Sistema_B" }
# ]
2. Desafío: Aplanado de Datos de Series TemporalesEscenario: Tienes datos de sensores en un formato "largo" (long format), donde cada lectura es un registro separado.El Reto:Convertirlo a un formato "ancho" (wide format) agrupado por timestamp.El resultado debe ser un diccionario donde cada clave es un timestamp, y el valor es otro diccionario que contiene {sensor: valor}.Manejar el hecho de que no todos los sensores reportan en cada timestamp.print("\n--- 2. Desafío: Aplanado de Series Temporales (Pivote) ---")
import json

datos_formato_largo = [
    {"timestamp": "10:00", "sensor": "TEMP_A", "valor": 20},
    {"timestamp": "10:00", "sensor": "HUM", "valor": 60},
    {"timestamp": "10:01", "sensor": "TEMP_A", "valor": 21},
    {"timestamp": "10:01", "sensor": "HUM", "valor": 59},
    {"timestamp": "10:01", "sensor": "PRESION", "valor": 1012},
    {"timestamp": "10:02", "sensor": "TEMP_A", "valor": 22},
]

# --- Solución (Agrupación manual con diccionarios) ---

datos_formato_ancho = {}
for lectura in datos_formato_largo:
    ts = lectura['timestamp']
    sensor = lectura['sensor']
    valor = lectura['valor']
    
    if ts not in datos_formato_ancho:
        # Si es la primera vez que vemos este timestamp, creamos su dict
        datos_formato_ancho[ts] = {}
        
    # Añadimos la lectura del sensor a ese timestamp
    datos_formato_ancho[ts][sensor] = valor
    
    # Forma avanzada (setdefault)
    # datos_formato_ancho.setdefault(ts, {})[sensor] = valor

print("\n--- Datos en Formato Ancho (JSON) ---")
print(json.dumps(datos_formato_ancho, indent=2))

# Salida esperada:
# {
#   "10:00": {
#     "TEMP_A": 20,
#     "HUM": 60
#   },
#   "10:01": {
#     "TEMP_A": 21,
#     "HUM": 59,
#     "PRESION": 1012
#   },
#   "10:02": {
#     "TEMP_A": 22
#   }
# }
3. Desafío: "Hot-Swapping" de Claves en DiccionariosEscenario: Tienes una lista de diccionarios y un "mapa de traducción" (mapping). Quieres renombrar todas las claves de todos los diccionarios de la lista según el mapa.El Reto:Usar una List Comprehension para iterar la lista.Dentro, usar una Dict Comprehension para iterar los pares (clave, valor) de cada diccionario.Traducir la clave usando el mapa. Si una clave no está en el mapa, debe mantenerse la original (esto es importante).print("\n--- 3. Desafío: Renombrado ('Hot-Swapping') de Claves ---")
import json

datos_antiguos = [
    {'ts': 1678886400, 'dev_id': 1, 'val': 99.5, 'err_code': 0},
    {'ts': 1678886401, 'dev_id': 2, 'val': 101.2, 'err_code': 1},
    {'ts': 1678886402, 'dev_id': 1, 'val': 99.6, 'err_code': 0, 'extra': 'OK'}
]

# Mapa de traducción: 'antiguo' -> 'nuevo'
mapa_traduccion = {
    'ts': 'timestamp',
    'dev_id': 'device_id',
    'val': 'value',
    'err_code': 'error_code'
    # 'extra' no está, así que debe mantenerse
}

# --- Solución (List + Dict Comprehension anidadas) ---

# [ {traduccion} for d in datos_antiguos ]
datos_nuevos = [
    {mapa_traduccion.get(k, k): v for k, v in d.items()}
    for d in datos_antiguos
]
# Explicación de la Dict Comprehension:
# {mapa_traduccion.get(k, k): v for k, v in d.items()}
#
# Para cada par (k, v) en el diccionario 'd':
#   Crea un nuevo par donde:
#     - La clave es: mapa_traduccion.get(k, k)
#       (Intenta coger k del mapa. Si no existe, usa k (la original))
#     - El valor es: v (el original)


print("\n--- Datos con Claves Nuevas (JSON) ---")
print(json.dumps(datos_nuevos, indent=2))

# Salida esperada:
# [
#   {
#     "timestamp": 1678886400,
#     "device_id": 1,
#     "value": 99.5,
#     "error_code": 0
#   },
#   {
#     "timestamp": 1678886401,
#     "device_id": 2,
#     "value": 101.2,
#     "error_code": 1
#   },
#   {
#     "timestamp": 1678886402,
#     "device_id": 1,
#     "value": 99.6,
#     "error_code": 0,
#     "extra": "OK"
#   }
# ]
Archivo: modulo_0_desafios_fechas.mdMódulo 0 (Sección 5): El Dolor y la Gloria de las FechasFilosofía: El manejo de fechas y horas (timestamps) es, sin lugar a dudas, una de las tareas más frustrantes y comunes en la ciencia de datos. Antes de usar la maquinaria pesada de pandas, debemos dominar las herramientas nativas de Python: el módulo datetime.La Teoría: datetime, timedelta y el timestamp1. El Módulo datetimePython trae datetime en su librería estándar. Los objetos clave son:datetime.date: Un objeto que solo almacena Año, Mes, Día.datetime.time: Un objeto que solo almacena Hora, Minuto, Segundo, Microsegundo.datetime.datetime: El objeto completo. Almacena todo lo anterior. Este es el que usamos el 99% del tiempo.datetime.timedelta: Un lapso o duración de tiempo (ej. "3 días y 5 horas").import datetime

print("--- 1. Conceptos Básicos de datetime ---")

# --- Creando un objeto datetime ---
# (Año, Mes, Día, Hora, Minuto, Segundo)
dt_objeto = datetime.datetime(2024, 10, 27, 9, 30, 0)
print(f"Objeto datetime: {dt_objeto}")

# --- Obteniendo la fecha y hora ACTUAL ---
dt_ahora = datetime.datetime.now()
print(f"Ahora (local):   {dt_ahora}")

# --- Obteniendo la hora ACTUAL en UTC (¡La mejor práctica!) ---
dt_ahora_utc = datetime.datetime.now(datetime.timezone.utc)
print(f"Ahora (UTC):     {dt_ahora_utc}")

# --- Accediendo a las partes ---
print(f"Año: {dt_objeto.year}")
print(f"Mes: {dt_objeto.month}")
print(f"Día: {dt_objeto.day}")
print(f"Hora: {dt_objeto.hour}")
print(f"Día de la semana (Lunes=0, Domingo=6): {dt_objeto.weekday()}")
2. El "Timestamp" (La Medida Universal)¿Qué es un "timestamp"? Es la forma que tienen los ordenadores de representar el tiempo de forma universal, sin zonas horarias ni formatos.Es un número único (un float o int) que representa la cantidad de segundos que han pasado desde el "Epoch".El "Epoch" (o Época) es un punto de inicio universal: 1 de Enero de 1970 a las 00:00:00 UTC.Un timestamp 0 es el Epoch.Un timestamp 1729992600.0 (como ahora mismo) son 1.729.992.600 segundos desde el Epoch.La gran ventaja: Un timestamp es solo un número. No tiene zona horaria. Es inequívoco.import datetime

print("\n--- 2. El Timestamp (Epoch) ---")

dt_objeto = datetime.datetime(2024, 10, 27, 9, 30, 0, tzinfo=datetime.timezone.utc)
print(f"Objeto (UTC): {dt_objeto}")

# --- Convertir un datetime (UTC) a timestamp ---
ts = dt_objeto.timestamp()
print(f"Su Timestamp: {ts}")

# --- Convertir un timestamp de vuelta a un datetime (UTC) ---
# (OJO: fromtimestamp() usa la hora local, fromutcstamp() es la correcta)
dt_desde_ts = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
print(f"Desde TS (UTC): {dt_desde_ts}")

# El Epoch
epoch = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
print(f"El Epoch (TS=0): {epoch}")
3. Parseo (strptime) y Formateo (strftime)Este es el trabajo sucio: convertir un string (texto) a un objeto datetime (parseo) y viceversa (formateo).strptime: String Parse Time (De String -> a Datetime)strftime: String Format Time (De Datetime -> a String)Usamos "códigos de formato" (ej. %Y para año de 4 dígitos, %m para mes, %d para día).import datetime

print("\n--- 3. Parseo (strptime) y Formateo (strftime) ---")

# --- strptime (String -> Datetime) ---
fecha_string_a = "27/10/2024 09:30:15"
formato_a = "%d/%m/%Y %H:%M:%S" # El formato que COINCIDE con el string
dt_a = datetime.datetime.strptime(fecha_string_a, formato_a)
print(f"String A: '{fecha_string_a}'")
print(f"Objeto A: {dt_a}")
print(f"Año de A: {dt_a.year}")

fecha_string_b = "Monday, 28-Oct-2024"
formato_b = "%A, %d-%b-%Y"
dt_b = datetime.datetime.strptime(fecha_string_b, formato_b)
print(f"\nString B: '{fecha_string_b}'")
print(f"Objeto B: {dt_b}")

# --- strftime (Datetime -> String) ---
dt_objeto = datetime.datetime(2024, 10, 27, 9, 30, 0)

# Formatear a ISO 8601 (Formato estándar PREFERIDO)
# (Python tiene un atajo para esto: .isoformat())
iso_string = dt_objeto.isoformat()
print(f"\nFormato ISO (ideal): {iso_string}")

# Formatear a un formato "amigable"
amigable_string = dt_objeto.strftime("Domingo, %d de %B de %Y")
print(f"Formato amigable: {amigable_string}")
4. Aritmética (timedelta)No se pueden "restar" dos datetime y esperar un número. Se obtiene un timedelta.import datetime

print("\n--- 4. Aritmética (timedelta) ---")

dt_inicio = datetime.datetime(2024, 1, 1, 10, 0, 0)
dt_fin = datetime.datetime(2024, 1, 3, 12, 30, 0)

# --- Restar dos datetimes ---
duracion = dt_fin - dt_inicio
print(f"Duración: {duracion}")
print(f"Tipo: {type(duracion)}") # <class 'datetime.timedelta'>
print(f"Total segundos en duración: {duracion.total_seconds()}")

# --- Crear un timedelta ---
tres_dias = datetime.timedelta(days=3)
dos_horas_media = datetime.timedelta(hours=2, minutes=30)

# --- Sumar/Restar un timedelta a un datetime ---
hace_tres_dias = datetime.datetime.now() - tres_dias
print(f"\nHace 3 días: {hace_tres_dias}")

proxima_alarma = datetime.datetime.now() + dos_horas_media
print(f"Próxima alarma: {proxima_alarma}")
El Taller: Desafíos del Módulo 0 (Fechas)1. Desafío: Parseo de Logs con Fechas CaóticasEscenario: Tienes logs de diferentes sistemas. Cada uno usa un formato de fecha.El Reto: Escribir una función que intente múltiples formatos de parseo hasta que uno funcione. Debe devolver un objeto datetime (o None si falla).import datetime

print("\n--- Desafío 1: Parseo de Fechas Caóticas ---")

logs_fechas_sucias = [
    "2024-10-27T10:00:00.123Z", # ISO 8601 (con Z = Zulu/UTC)
    "27/10/2024 11:00:00",
    "Oct 27, 2024 - 12:00 PM",
    "ERROR: Sensor offline", # Sin fecha
    "2024-10-27T13:00:00+02:00" # ISO 8601 (con timezone)
]

# (Python 3.7+ puede parsear ISO 8601 con .fromisoformat())
# (Python < 3.7 necesita parsear la 'Z' y '+02:00' manualmente, es complejo)

# Lista de formatos que queremos probar
FORMATOS_CONOCIDOS = [
    "%d/%m/%Y %H:%M:%S",         # "27/10/2024 11:00:00"
    "%b %d, %Y - %I:%M %p"   # "Oct 27, 2024 - 12:00 PM"
]

def parsear_fecha_flexible(fecha_str):
    """
    Intenta parsear un string de fecha usando múltiples formatos.
    """
    
    # Intento 1: ISO 8601 (el mejor caso)
    # (Usamos try/except para capturar el error si no coincide)
    try:
        # (Versión simple para 3.7+)
        # (Ignoramos la 'Z' por simplicidad ahora)
        return datetime.datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        pass # Si falla, sigue intentando
        
    # Intento 2: Probar nuestra lista de formatos
    for fmt in FORMATOS_CONOCIDOS:
        try:
            return datetime.datetime.strptime(fecha_str, fmt)
        except (ValueError, TypeError):
            pass # Si falla, prueba el siguiente formato
            
    # Si todo falla
    return None

# --- Solución (List Comprehension) ---
datetimes_parseados = [parsear_fecha_flexible(log) for log in logs_fechas_sucias]

print("\nResultados del Parseo Flexible:")
for dt in datetimes_parseados:
    print(f"  -> {dt}")
    
# Salida esperada (depende de Python 3.7+ para ISO):
#   -> 2024-10-27 10:00:00.123000+00:00
#   -> 2024-10-27 11:00:00
#   -> 2024-10-27 12:00:00
#   -> None
#   -> 2024-10-27 13:00:00+02:00
2. Desafío: Calcular Tiempos de RespuestaEscenario: Tienes una lista de diccionarios (evento_id, timestamp_inicio, timestamp_fin). Los timestamps son strings en formato ISO 8601.El Reto:Parsear los timestamps.Calcular la duración (tiempo de respuesta) de cada evento en segundos totales.Crear una nueva lista de diccionarios que incluya {"id": ..., "duracion_seg": ...}.(Opcional) Encontrar el evento que más tardó (usando lambda).import datetime
import json

print("\n--- Desafío 2: Cálculo de Tiempos de Respuesta ---")

eventos = [
    {"id": "A", "inicio": "2024-01-01T12:00:00Z", "fin": "2024-01-01T12:00:30.5Z"},
    {"id": "B", "inicio": "2024-01-01T12:01:00Z", "fin": "2024-01-01T12:03:15.0Z"},
    {"id": "C", "inicio": "2024-01-01T12:02:00Z", "fin": "2024-01-01T12:02:05.2Z"}
]

# --- Solución (List Comprehension) ---

def calcular_duracion(evento):
    # 1. Parsear (Python 3.7+ simple)
    #    .replace('Z', '+00:00') es el truco para que fromisoformat()
    #    entienda 'Z' (Zulu/UTC)
    dt_inicio = datetime.datetime.fromisoformat(evento['inicio'].replace('Z', '+00:00'))
    dt_fin = datetime.datetime.fromisoformat(evento['fin'].replace('Z', '+00:00'))
    
    # 2. Calcular timedelta
    duracion = dt_fin - dt_inicio
    
    # 3. Extraer segundos totales
    return {
        "id": evento['id'],
        "duracion_seg": duracion.total_seconds()
    }

tiempos_respuesta = [calcular_duracion(e) for e in eventos]

print("\nTiempos de Respuesta (JSON):")
print(json.dumps(tiempos_respuesta, indent=2))
# Salida:
# [
#   { "id": "A", "duracion_seg": 30.5 },
#   { "id": "B", "duracion_seg": 135.0 },
#   { "id": "C", "duracion_seg": 5.2 }
# ]

# --- Opcional: Evento más lento (Lambda) ---
evento_mas_lento = max(tiempos_respuesta, key=lambda x: x['duracion_seg'])
print(f"\nEvento más lento: {evento_mas_lento}")
3. Desafío: Agregación por Ventanas de Tiempo (Time Bucketing)Escenario: Tienes una lista de ventas con timestamps exactos.El Reto: Agrupar las ventas por hora y contar cuántas ventas ocurrieron en cada hora. (Este es el "Group By" de Pandas, hecho a mano).import datetime
import json

print("\n--- Desafío 3: Agregación por Ventanas de Tiempo ---")

ventas_stream = [
    {"id": 1, "ts_iso": "2024-01-01T10:05:00Z", "monto": 10},
    {"id": 2, "ts_iso": "2024-01-01T10:15:00Z", "monto": 20},
    {"id": 3, "ts_iso": "2024-01-01T10:55:00Z", "monto": 15},
    {"id": 4, "ts_iso": "2024-01-01T11:02:00Z", "monto": 50},
    {"id": 5, "ts_iso": "2024-01-01T11:30:00Z", "monto": 5},
    {"id": 6, "ts_iso": "2024-01-01T12:01:00Z", "monto": 30},
]

# --- Solución (Agrupación manual con diccionarios) ---

ventas_por_hora = {}
for venta in ventas_stream:
    # 1. Parsear
    dt = datetime.datetime.fromisoformat(venta['ts_iso'].replace('Z', '+00:00'))
    
    # 2. Crear la "Ventana" (Time Bucket)
    #    Queremos truncar la fecha a su hora.
    #    Ej: 10:05, 10:15, 10:55 -> todas van a la "ventana" de las 10:00
    
    # El truco: .replace() para poner minutos, segundos y micros a 0
    ventana_dt = dt.replace(minute=0, second=0, microsecond=0)
    
    # Convertimos a string para usarla como clave del diccionario
    ventana_str = ventana_dt.isoformat()
    
    # 3. Agrupar (Contar)
    ventas_por_hora[ventana_str] = ventas_por_hora.get(ventana_str, 0) + 1
    
    # (Si quisiéramos sumar el monto:)
    # ventas_por_hora[ventana_str] = ventas_por_hora.get(ventana_str, 0.0) + venta['monto']

print("\nConteo de Ventas por Hora (JSON):")
print(json.dumps(ventas_por_hora, indent=2))

# Salida esperada:
# {
#   "2024-01-01T10:00:00+00:00": 3,
#   "2024-01-01T11:00:00+00:00": 2,
#   "2024-01-01T12:00:00+00:00": 1
# }
Archivo: modulo_1_numpy.mdMódulo 1: NumPy - El Poder de la VectorizaciónFilosofía: NumPy (Numerical Python) es la librería sobre la que se construye todo el ecosistema de Data Science en Python (incluyendo Pandas, Scikit-learn y TensorFlow). Su poder reside en una nueva estructura de datos: el ndarray (N-dimensional array).El Cambio de Mentalidad: Dejamos de pensar en bucles for (iterar elemento por elemento). Empezamos a pensar en operaciones vectorizadas (aplicar una operación a todo el array a la vez).1. El ndarray (El Fundamento)Un ndarray es como una lista de Python, pero con dos diferencias cruciales:Homogéneo: Todos los elementos deben ser del mismo tipo (int, float64, bool).Eficiente: Ocupa un bloque de memoria contiguo, lo que permite que las operaciones se ejecuten en C (mucho más rápido que Python).Creación de Arraysimport numpy as np

print("--- 1. Creación de Arrays ---")

# --- Desde una lista de Python ---
lista_py = [1, 2, 3, 4, 5]
arr = np.array(lista_py)
print(f"Array: {arr}")
print(f"Tipo (Python): {type(arr)}") # <class 'numpy.ndarray'>
print(f"Tipo (NumPy): {arr.dtype}") # int64 (depende del S.O.)

# --- Arrays 2D (Matrices) ---
matriz_py = [[1, 2], [3, 4], [5, 6]]
matriz_np = np.array(matriz_py)
print(f"\nMatriz:\n{matriz_np}")
print(f"Shape (Forma): {matriz_np.shape}") # (3 filas, 2 columnas)

# --- Arrays pre-rellenados ---
zeros_arr = np.zeros((2, 3)) # (filas, columnas)
print(f"\nCeros (float por defecto):\n{zeros_arr}")

ones_arr = np.ones((3, 2), dtype=np.int32) # Especificar tipo
print(f"\nUnos (int32):\n{ones_arr}")

# --- Secuencias ---
# Como 'range()' pero para NumPy (y mejor)
rango_arr = np.arange(0, 10, 2) # (inicio, fin_excl, paso)
print(f"\nArange: {rango_arr}")

# 'linspace' (espaciado lineal) - Muy útil
# Genera 5 números equidistantes entre 0 y 10 (ambos incluidos)
linspace_arr = np.linspace(0, 10, 5)
print(f"\nLinspace: {linspace_arr}") # [ 0. ,  2.5,  5. ,  7.5, 10. ]
2. Aritmética Vectorizada (El "Anti-For")Aquí es donde NumPy brilla. Las operaciones se aplican a cada elemento simultáneamente (en la práctica).import numpy as np

print("\n--- 2. Aritmética Vectorizada ---")
arr = np.array([10, 20, 30, 40, 50])
print(f"Original: {arr}")

# --- Operaciones Escalares ---
# NO NECESITAMOS BUCLES
print(f"arr * 2:  {arr * 2}")
print(f"arr + 5:  {arr + 5}")
print(f"arr / 10: {arr / 10}") # ¡La división siempre produce float!
print(f"arr ** 2: {arr ** 2}") # Cuadrado

# --- Funciones Universales (ufuncs) ---
# Funciones matemáticas que operan elemento a elemento
print(f"np.sqrt(arr): {np.sqrt(arr)}")
print(f"np.exp(arr):  {np.exp(arr)}") # e^x
print(f"np.sin(arr):  {np.sin(arr)}")

# --- Operaciones entre Arrays ---
# Deben tener el mismo 'shape'
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(f"\nA: {a}")
print(f"B: {b}")
print(f"A + B: {a + b}") # [11, 22, 33]
print(f"A * B: {a * b}") # [10, 40, 90] (¡Esto NO es producto de matrices!)
¡El Producto Matricial (Álgebra Lineal)!Para el producto de matrices real (dot product), usamos el operador @ (Python 3.5+) o np.dot().mat_a = np.array([[1, 2], [3, 4]]) # (2, 2)
mat_b = np.array([[10], [20]])      # (2, 1)

# Producto Matricial: (2, 2) @ (2, 1) -> (2, 1)
producto_mat = mat_a @ mat_b
print(f"\nProducto Matricial (A @ B):\n{producto_mat}")
3. Generación de Datos (El Núcleo de tu idea)NumPy es la herramienta estándar para simular datos. Usamos el submódulo np.random.import numpy as np
np.random.seed(42) # ¡Fijar la semilla para reproducibilidad!

print("\n--- 3. Generación de Datos (np.random) ---")

# --- Distribución Uniforme ---
# 'rand' -> Números entre 0.0 y 1.0
uni_arr = np.random.rand(5) # 5 números
print(f"Uniforme (0 a 1): {uni_arr}")
uni_mat = np.random.rand(2, 3) # Matriz 2x3
print(f"Matriz Uniforme:\n{uni_mat}")

# 'randint' -> Enteros
# (low, high_excl, size)
enteros = np.random.randint(10, 20, size=5)
print(f"\nEnteros (10 a 19): {enteros}")

# --- Distribución Normal (Gaussiana) ---
# La más importante. La base de la simulación.
# 'randn' -> Normal estándar (Media=0, Desv.Est=1)
normal_std = np.random.randn(5)
print(f"\nNormal Estándar (Media 0, Desv 1): {normal_std}")

# 'normal' -> Especificar Media (loc) y Desv.Est (scale)
# Simular 1000 temperaturas de la Antártida
media_temp = -25
desv_temp = 5
size = 1000
temperaturas = np.random.normal(loc=media_temp, scale=desv_temp, size=size)
print(f"\nSimulación de Temperaturas (1000 muestras):")
print(f"  Media (calculada): {temperaturas.mean():.2f}")
print(f"  Desv.Est (calculada): {temperaturas.std():.2f}")

# --- Distribución de Poisson ---
# Para conteos (ej. "pingüinos por hora")
# 'lam' (lambda) es el promedio de eventos
avg_pinguinos = 50
conteo_pinguinos = np.random.poisson(lam=avg_pinguinos, size=10)
print(f"\nConteo Poisson (media 50): {conteo_pinguinos}")

# --- Elección (Choice) ---
# Para datos categóricos
opciones = ['Estable', 'Grietas', 'Peligroso']
# Elegir 10 veces, con probabilidades (p)
condicion_hielo = np.random.choice(
    opciones, 
    size=10, 
    p=[0.7, 0.2, 0.1] # 70% Estable, 20% Grietas, 10% Peligroso
)
print(f"\nCondición Hielo (Categórico): {condicion_hielo}")
4. Creando el Caos (Datos del Mundo Real)Los datos reales tienen valores faltantes (NaN) y outliers (atípicos).np.nan (Not a Number)np.nan es la forma de NumPy de representar un valor faltante. Es un float.Propiedad clave: np.nan se "propaga". Cualquier operación matemática con nan da como resultado nan.import numpy as np

print("\n--- 4. Creando el Caos (NaN y Outliers) ---")
arr = np.array([1.0, 2.0, np.nan, 4.0])
print(f"\nArray con NaN: {arr}")

# ¡Las operaciones estándar fallan!
print(f"Suma (falla): {arr.sum()}") # nan
print(f"Media (falla): {arr.mean()}") # nan

# ¡Hay que usar las versiones "nan-safe"!
print(f"Suma (segura): {np.nansum(arr)}") # 7.0
print(f"Media (segura): {np.nanmean(arr)}") # 2.333

# --- Introduciendo NaN en datos ---
print("\nIntroduciendo 50% de NaNs en un array:")
datos = np.linspace(0, 10, 10)
print(f"Datos originales: {datos}")

# 1. Crear una máscara booleana aleatoria
mask_nan = np.random.choice([True, False], size=datos.shape, p=[0.5, 0.5])
print(f"Máscara de NaNs:  {mask_nan}")

# 2. Aplicar la máscara
# (Necesitamos que 'datos' sea float para aceptar 'np.nan')
datos = datos.astype(np.float32)
datos[mask_nan] = np.nan
print(f"Datos con NaNs:   {datos}")
Outliers (Atípicos)import numpy as np
np.random.seed(42)

# Simular 10 lecturas de temperatura
temps = np.random.normal(loc=-15, scale=3, size=10)
print(f"\nTemperaturas (limpias):\n{np.round(temps, 1)}")

# Introducir 2 outliers
# 1. Elegir 2 índices al azar (sin reemplazo)
n_outliers = 2
indices_outlier = np.random.choice(temps.size, n_outliers, replace=False)
print(f"Índices de outliers: {indices_outlier}") # Ej: [1 7]

# 2. Añadir/Restar un valor extremo en esos índices
valor_extremo = 100.0
temps[indices_outlier] += np.random.choice([-1, 1], n_outliers) * valor_extremo

print(f"Temperaturas (sucias):\n{np.round(temps, 1)}")
# (Verás valores como -112.9 o 87.1)
5. Indexación y Máscaras (El Super-Filtro)Esta es la habilidad esencial de NumPy. Cómo seleccionar los datos que quieres.Slicing 2D (Matrices)arr[filas, columnas]import numpy as np

print("\n--- 5. Indexación y Máscaras ---")
mat = np.arange(1, 10).reshape((3, 3))
print(f"Matriz 3x3:\n{mat}")
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]

# Fila 0, Columna 1
print(f"\nElemento (0, 1): {mat[0, 1]}") # 2

# Fila 1 (completa)
print(f"Fila 1: {mat[1, :]}") # [4 5 6]  (el ':' significa "todo")

# Columna 2 (completa)
print(f"Columna 2: {mat[:, 2]}") # [3 6 9]

# Sub-matriz (Filas 0 y 1, Columnas 1 y 2)
print(f"Sub-matriz (0:2, 1:3):\n{mat[0:2, 1:3]}")
# [[2 3]
#  [5 6]]
Máscaras Booleanas (El concepto más importante)Una máscara booleana es un array de True/False con el mismo shape que tu array de datos. Se usa para filtrar.import numpy as np
np.random.seed(42)
temps = np.random.normal(-10, 5, size=10)
print(f"\nTemperaturas (10 muestras):\n{np.round(temps, 1)}")

# 1. Crear la Máscara: ¿Qué temperaturas están bajo cero?
mask_bajo_cero = temps < 0
print(f"\nMáscara (temps < 0): {mask_bajo_cero}")
# [ True  True False  True False  True  True  True False  True]

# 2. Aplicar la Máscara
# "Dame solo los elementos de 'temps' donde la máscara es 'True'"
temps_frias = temps[mask_bajo_cero]
print(f"Temperaturas frías:\n{np.round(temps_frias, 1)}")

# --- Directamente (sin variable 'mask') ---
print(f"Directo (temps > -10):\n{np.round(temps[temps > -10], 1)}")

# --- Combinando condiciones ---
# & (AND), | (OR), ~ (NOT)
# ¡LOS PARÉNTESIS SON OBLIGATORIOS!
mask_combinada = (temps < -10) & (temps > -15)
print(f"Temps entre -15 y -10:\n{np.round(temps[mask_combinada], 1)}")

# --- Modificar datos con una máscara ---
# "Poner a 0 todas las temperaturas positivas"
print(f"\nTemps (antes de modificar): {np.round(temps, 1)}")
temps[temps > 0] = 0.0
print(f"Temps (modificadas):        {np.round(temps, 1)}")
np.where() (El if/else vectorizado)np.where(condicion, valor_si_true, valor_si_false)import numpy as np

print("\n--- np.where (if/else vectorizado) ---")
temps = np.array([-5, 10, -1, 0, 8])

# Crear un array categórico:
# Si temp < 0 -> "Frio"
# Si temp >= 0 -> "Calido"
categorias_temp = np.where(temps < 0, "Frio", "Calido")
print(f"Categorías: {categorias_temp}")
# ['Frio' 'Calido' 'Frio' 'Calido' 'Calido']
Archivo: modulo_1_desafios_avanzados.mdMódulo 1 (Desafíos): Taller Avanzado NumPyFilosofía: Estos desafíos requieren combinar la lógica de Python (Módulo 0, como datetime) con el poder de NumPy (Módulo 1). El objetivo es resolver problemas que simulan el día a día de un analista de datos.1. Desafío: Simulación Monte Carlo (Básica)Escenario: Queremos estimar el valor de Pi ($\pi$) usando una simulación de Monte Carlo.La idea:Imagina un cuadrado de 1x1 (de (0,0) a (1,1)).Imagina un cuarto de círculo de radio 1 dentro de él.Lanza 1,000,000 de "dardos" (puntos aleatorios (x, y)) dentro del cuadrado.Calcula la distancia de cada punto al origen ((0,0)): $dist = \sqrt{x^2 + y^2}$.Si $dist \le 1.0$, el dardo cayó dentro del círculo.La proporción $Area_{círculo} / Area_{cuadrado}$ es $\pi r^2 / (2r)^2$ (para un círculo completo) o $(\pi/4) / 1$ (para nuestro cuarto de círculo).Por tanto: $\pi \approx 4 \times (\text{puntos_dentro} / \text{puntos_totales})$.El Reto: Implementar esto usando NumPy. No usar bucles for.import numpy as np

print("--- 1. Desafío: Simulación Monte Carlo (Estimar Pi) ---")
np.random.seed(42)

N_PUNTOS = 1_000_000 # 1 millón

# 1. Lanzar todos los dardos (coordenadas X e Y)
#    Generar 2 millones de números uniformes (0 a 1)
#    y reordenarlos en (1M, 2)
puntos = np.random.rand(N_PUNTOS, 2) # (x, y)
print(f"Shape de 'puntos': {puntos.shape}")

# 2. Calcular las distancias al origen (Vectorizado)
#    (x^2 + y^2) para cada punto
distancias_sq = np.sum(puntos**2, axis=1) # Sumar en el eje de las columnas
print(f"Shape de 'distancias_sq': {distancias_sq.shape}")

# (No necesitamos la raíz (sqrt) porque 1^2 = 1.
#  Podemos comparar las distancias al cuadrado con 1)

# 3. Crear la máscara booleana
mask_dentro_circulo = distancias_sq <= 1.0
print(f"Shape de 'mask_dentro': {mask_dentro_circulo.shape}")

# 4. Contar cuántos cayeron dentro
#    En NumPy, True=1 y False=0.
#    Podemos sumar la máscara.
puntos_dentro = np.sum(mask_dentro_circulo)
print(f"\nPuntos Totales: {N_PUNTOS}")
print(f"Puntos Dentro:  {puntos_dentro}")

# 5. Estimar Pi
pi_estimado = 4 * (puntos_dentro / N_PUNTOS)
print(f"\nPi (Real):     {np.pi:.6f}")
print(f"Pi (Estimado): {pi_estimado:.6f}")
2. Desafío: Limpieza de Datos de Sensor (Fechas y NaN)Escenario: Tienes un array de timestamps (en segundos desde Epoch, formato float) y un array de lecturas de temperatura. Las lecturas tienen NaNs y outliers.El Reto:Filtrar outliers: Reemplazar todos los valores > 50°C y < -80°C por np.nan.Rellenar NaNs: Rellenar todos los np.nan (los originales y los nuevos) con la media de los datos limpios (no-outlier, no-nan).Filtrar por fecha: Seleccionar solo las lecturas que ocurrieron un "Lunes".Nota: Usaremos datetime (Módulo 0) para la parte de las fechas, pero NumPy para el procesamiento.import numpy as np
import datetime

print("\n--- 2. Desafío: Limpieza (Fechas, NaN, Outliers) ---")
np.random.seed(42)

# 1. Generar datos "sucios"
base_time = 1704067200 # 1 Enero 2024 (Lunes)
N = 1000

# Timestamps: 1000 lecturas, cada 30 minutos (1800 seg)
timestamps_epoch = base_time + np.arange(N) * 1800

# Temperaturas: media -10, desv 5, con NaNs y Outliers
temps = np.random.normal(-10, 5, N)
# Introducir NaNs
temps[np.random.choice(N, 100, replace=False)] = np.nan
# Introducir Outliers
temps[np.random.choice(N, 20, replace=False)] += np.random.choice([-1, 1], 20) * 100

print(f"Datos generados: {N} lecturas")
print(f"Media (sucia):   {np.nanmean(temps):.2f}")
print(f"Max (sucia):     {np.nanmax(temps):.2f}")
print(f"Min (sucia):     {np.nanmin(temps):.2f}")
print(f"NaNs (inicio):   {np.sum(np.isnan(temps))}")

# --- Solución ---

# 1. Filtrar outliers (Máscara booleana)
mask_outliers = (temps > 50) | (temps < -80)
print(f"Outliers detectados: {np.sum(mask_outliers)}")

# 2. Crear una copia y reemplazarlos por NaN
temps_limpias = np.copy(temps)
temps_limpias[mask_outliers] = np.nan

# 3. Calcular la media de los datos válidos
media_valida = np.nanmean(temps_limpias)
print(f"Media (válida):  {media_valida:.2f}")

# 4. Rellenar TODOS los NaNs con la media válida
temps_rellenas = np.nan_to_num(temps_limpias, nan=media_valida)
print(f"NaNs (final):    {np.sum(np.isnan(temps_rellenas))}")

# 5. Filtrar por fecha (Lunes)
#    (Aquí combinamos con Módulo 0)

#    Convertir timestamps (números) a objetos datetime
#    (Usamos una list comprehension, esto puede ser lento en datos masivos)
datetimes = [datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc) 
             for ts in timestamps_epoch]

#    Obtener el día de la semana (Lunes=0)
dias_semana = np.array([dt.weekday() for dt in datetimes])
print(f"\nDías semana (0=Lunes): {dias_semana[:10]}...")

#    Crear la máscara booleana para los Lunes
mask_lunes = (dias_semana == 0) # 0 es Lunes
print(f"Total registros: {N}")
print(f"Registros en Lunes: {np.sum(mask_lunes)}")

# 6. Selección final
lecturas_lunes = temps_rellenas[mask_lunes]
print(f"Media de los Lunes (limpia): {lecturas_lunes.mean():.2f}")
3. Desafío: Normalización de Features (Min-Max Scaler)Escenario: En Machine Learning, muchos algoritmos requieren que las "features" (columnas) estén en la misma escala (ej. de 0 a 1).El Reto: Tienes una matriz de (100, 3) (100 muestras, 3 features).Implementar la "Normalización Min-Max" para cada columna por separado.Fórmula: $X_{scaled} = \frac{X - X_{min}}{X_{max} - X_{min}}$Hacerlo de forma vectorizada (sin bucles for sobre las columnas).Pista: Los ejes (axis=...) son la clave.import numpy as np

print("\n--- 3. Desafío: Normalización Min-Max (Vectorizada) ---")
np.random.seed(42)

# Generar 100 muestras, 3 features (columnas) con escalas diferentes
F1 = np.random.normal(100, 10, (100, 1)) # Temp (media 100)
F2 = np.random.normal(5, 1, (100, 1))   # Humedad (media 5)
F3 = np.random.normal(1000, 50, (100, 1)) # Presión (media 1000)

# np.hstack apila arrays horizontalmente
features = np.hstack((F1, F2, F3))
print(f"Shape de Features: {features.shape}")

print("\n--- Antes de Escalar ---")
print(f"Medias: {np.mean(features, axis=0)}")
print(f"Mins:   {np.min(features, axis=0)}")
print(f"Maxs:   {np.max(features, axis=0)}")

# --- Solución (Broadcasting y Ejes) ---

# 1. Calcular Mins y Maxs POR COLUMNA (axis=0)
X_min = np.min(features, axis=0)
X_max = np.max(features, axis=0)

print(f"\nShape de X_min: {X_min.shape}") # (3,)
print(f"Shape de X_max: {X_max.shape}") # (3,)

# 2. Aplicar la fórmula
#    features (100, 3)
#    X_min    (3,)
#
#    NumPy usa "Broadcasting"
#    "Resta el array (3,) de cada una de las 100 filas de (100, 3)"
numerador = features - X_min
denominador = X_max - X_min

features_scaled = numerador / denominador

print("\n--- Después de Escalar ---")
print(f"Medias: {np.mean(features_scaled, axis=0)}")
print(f"Mins:   {np.min(features_scaled, axis=0)}") # Deberían ser [0. 0. 0.]
print(f"Maxs:   {np.max(features_scaled, axis=0)}") # Deberían ser [1. 1. 1.]

print("\nHead de datos escalados (5 primeras filas):")
print(np.round(features_scaled[:5], 3))
4. Desafío: Vectorización de Texto (Bag-of-Words) y SimilaridadEscenario: Tienes un "corpus" de 3 frases. Quieres saber cómo de "similares" son. La base del NLP (Procesamiento de Lenguaje Natural) es convertir texto en números.El Reto:Tokenizar: Convertir las frases en listas de palabras (Python).Crear Vocabulario: Encontrar todas las palabras únicas (Python).Vectorizar (Bag-of-Words): Crear una matriz (3, N_palabras) donde matriz[i, j] es el conteo de la palabra j en la frase i.Calcular Similaridad de Coseno: Calcular cómo de "parecidas" son las frases 1 y 2.Fórmula: $Sim(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$ (Producto punto / (Norma A * Norma B))import numpy as np

print("\n--- 4. Desafío: Vectorización de Texto (Bag-of-Words) ---")

corpus = [
    "el gato come pescado",
    "el perro come pienso",
    "el gato y el perro juegan"
]

# --- 1 y 2. Tokenizar y Crear Vocabulario (Python) ---
vocabulario = set()
corpus_tokenizado = []
for frase in corpus:
    tokens = frase.split(' ') # Tokenización simple
    corpus_tokenizado.append(tokens)
    vocabulario.update(tokens) # .update() añade todos los items a un set

# Convertir a lista ordenada y crear un mapa de "palabra -> índice"
vocab_list = sorted(list(vocabulario))
word_to_index = {palabra: i for i, palabra in enumerate(vocab_list)}

N_FRASES = len(corpus)
N_PALABRAS = len(vocab_list)

print(f"Corpus de {N_FRASES} frases.")
print(f"Vocabulario de {N_PALABRAS} palabras: {vocab_list}")
print(f"Mapa: {word_to_index}")

# --- 3. Vectorizar (NumPy) ---
#    (Usamos np.zeros para crear la matriz vacía)
bow_matrix = np.zeros((N_FRASES, N_PALABRAS), dtype=np.int32)

# (Este es el único bucle 'for' que permitimos,
#  para iterar las frases, no las palabras)
for i_frase, tokens in enumerate(corpus_tokenizado):
    for token in tokens:
        i_palabra = word_to_index[token]
        # Incrementar el conteo
        bow_matrix[i_frase, i_palabra] += 1

print("\n--- Matriz Bag-of-Words (Frases x Palabras) ---")
print(bow_matrix)

# --- 4. Calcular Similaridad de Coseno (Frase 0 vs Frase 1) ---
#    (el gato come pescado) vs (el perro come pienso)

vec_0 = bow_matrix[0, :] # Fila 0
vec_1 = bow_matrix[1, :] # Fila 1

print(f"\nVector 0: {vec_0}")
print(f"Vector 1: {vec_1}")

# 4a. Producto Punto (A · B)
producto_punto = np.dot(vec_0, vec_1)
# (Forma alternativa: (vec_0 * vec_1).sum())
print(f"\nProducto Punto: {producto_punto}") # (el=1*1, come=1*1) -> 2

# 4b. Normas (||A|| y ||B||)
#    Norma (L2) = sqrt(sum(x^2))
norma_0 = np.sqrt(np.sum(vec_0**2))
norma_1 = np.sqrt(np.sum(vec_1**2))
# (Forma alternativa: np.linalg.norm(vec_0))
print(f"Norma 0: {norma_0:.3f}")
print(f"Norma 1: {norma_1:.3f}")

# 4c. Similaridad de Coseno
#    (Manejar división por cero si una norma es 0)
denominador = (norma_0 * norma_1)
if denominador == 0:
    similitud = 0.0
else:
    similitud = producto_punto / denominador
    
print(f"\nSimilaridad Coseno (Frase 0 vs 1): {similitud:.3f}")
# (Debería ser ~0.447)

# --- (Opcional) Similaridad (Frase 0 vs Frase 2) ---
vec_2 = bow_matrix[2, :]
producto_punto_02 = np.dot(vec_0, vec_2)
norma_2 = np.linalg.norm(vec_2)
similitud_02 = producto_punto_02 / (norma_0 * norma_2)
print(f"Similaridad Coseno (Frase 0 vs 2): {similitud_02:.3f}")
# (Debería ser ~0.408)
Archivo: modulo_1_final_desafios.mdMódulo 1 (Final): Broadcasting y Arrays EstructuradosFilosofía: Este es el último escalón de NumPy "puro". Si dominas esto, dominas NumPy.Broadcasting (La Magia): Es el conjunto de reglas por las que NumPy permite operaciones entre arrays de diferente forma. Es la característica más potente (y a veces confusa) de NumPy.Fancy Indexing (Indexación Avanzada): Usar arrays de enteros o arrays booleanos para seleccionar datos, no solo slices.Structured Arrays (Arrays Estructurados): El "eslabón perdido". Un array de NumPy que se comporta como una tabla, con columnas de diferentes tipos (dtype).1. Desafío: Broadcasting Avanzado (Matriz de Distancias)Escenario: Tienes un array A de 5 puntos en 2D (shape (5, 2)) y un array B de 3 "centroides" (shape (3, 2)).El Reto: Calcular la distancia euclidiana entre cada punto de A y cada punto de B, generando una matriz de distancias final de shape (5, 3). Todo esto sin un solo bucle for.Pista: $Dist = \sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$.Pista 2: Necesitarás np.newaxis para "alinear" las dimensiones.import numpy as np

print("--- 1. Desafío: Broadcasting (Matriz de Distancias) ---")
np.random.seed(42)

puntos = np.random.randint(0, 10, size=(5, 2))
centroides = np.random.randint(0, 5, size=(3, 2))

print(f"Puntos (shape {puntos.shape}):\n{puntos}")
print(f"\nCentroides (shape {centroides.shape}):\n{centroides}")

# --- Solución (Broadcasting) ---

# Queremos restar (5, 2) de (3, 2) de forma "cruzada".
# Para ello, expandimos sus dimensiones para que NumPy las "estire".

# 1. Expandir 'puntos' a (5, 1, 2)
#    (5 filas, 1 "profundidad", 2 columnas)
puntos_exp = puntos[:, np.newaxis, :]
# (Alternativa: puntos[:, None, :])

# 2. Expandir 'centroides' a (1, 3, 2)
#    (1 fila, 3 "profundidad", 2 columnas)
centroides_exp = centroides[np.newaxis, :, :]
# (Alternativa: centroides[None, :, :])

print(f"\nPuntos expandidos (shape {puntos_exp.shape})")
print(f"Centroides expandidos (shape {centroides_exp.shape})")

# 3. Restar (Aquí ocurre la magia)
#    NumPy ve: (5, 1, 2) - (1, 3, 2)
#    Y "estira" ambos para que coincidan en un shape (5, 3, 2)
#    El resultado es una matriz 5x3, donde cada celda
#    contiene el vector (dx, dy) entre el punto i y el centroide j.
vectores_distancia = puntos_exp - centroides_exp
print(f"\nVectores Distancia (shape {vectores_distancia.shape}):\n{vectores_distancia}")

# 4. Calcular la distancia (vectorizado)
#    (dx^2 + dy^2)
dist_sq = np.sum(vectores_distancia**2, axis=2) # Sumar en el eje 2 (las coords x,y)
distancias = np.sqrt(dist_sq)

print(f"\n--- Matriz de Distancias Final (shape {distancias.shape}) ---")
print(np.round(distancias, 2))

# Salida:
# [[2.   5.   3.  ]
#  [8.06 6.32 7.07]
#  [8.   5.   7.  ]
#  [5.39 3.   4.  ]
#  [6.   3.   5.  ]]
#
# (distancias[0, 0] es la distancia entre punto 0 [2, 7] y centroide 0 [0, 7] = 2.0)
2. Desafío: Fancy Indexing (Reordenar y Muestrear)Escenario: Tienes un array de datos (10, 2) (10 muestras, 2 features).El Reto:Selección Aleatoria: Crear un nuevo array (5, 2) seleccionando 5 filas aleatorias de las 10 originales (muestreo con reemplazo).Reordenado: Tienes un array de índices [9, 0, 3]. Crear un nuevo array (3, 2) seleccionando exactamente esas filas en ese orden.Selección Condicional (np.where): Obtener los índices (no los valores) de todas las filas donde la feature 0 (columna 0) sea mayor que 0.5.import numpy as np

print("\n--- 2. Desafío: Fancy Indexing ---")
np.random.seed(42)

datos = np.random.rand(10, 2)
print(f"Datos originales (shape {datos.shape}):\n{np.round(datos, 2)}")

# --- 1. Selección Aleatoria ---
indices_aleatorios = np.random.randint(0, 10, size=5) # 5 índices de 0 a 9
print(f"\nÍndices Aleatorios: {indices_aleatorios}") # [6 3 7 4 6]

# "Dame las filas de 'datos' en estos índices"
muestreo = datos[indices_aleatorios, :]
print(f"Muestreo (shape {muestreo.shape}):\n{np.round(muestreo, 2)}")
# (Nota: la fila 6 aparece dos veces)

# --- 2. Reordenado ---
indices_reorden = np.array([9, 0, 3])
print(f"\nÍndices Reorden: {indices_reorden}")

reordenado = datos[indices_reorden, :]
print(f"Reordenado (shape {reordenado.shape}):\n{np.round(reordenado, 2)}")
# (Fila 9, luego Fila 0, luego Fila 3)

# --- 3. Selección Condicional (np.where) ---
# np.where(condicion) (CON UN SOLO ARGUMENTO)
# devuelve una tupla de arrays de índices.
# (Es raro, pero así funciona)
indices_condicion = np.where(datos[:, 0] > 0.5)
print(f"\nÍndices donde col 0 > 0.5: {indices_condicion}")
# (array([0, 1, 2, 5, 6, 7]),)  <- ¡Es una tupla!

# Para usarlo, cogemos el primer elemento de la tupla:
indices = indices_condicion[0]
seleccion_condicional = datos[indices, :]
print(f"Selección condicional (shape {seleccion_condicional.shape}):\n{np.round(seleccion_condicional, 2)}")
3. Desafío: Structured Arrays (El Eslabón Perdido)Escenario: Tienes datos "sucios" en una lista de tuplas. Cada tupla tiene (id_sensor (str), timestamp (int), valor (float)). Esto no cabe en un array normal (tipos mixtos).El Reto:Definir un dtype estructurado para NumPy.Crear un array estructurado a partir de los datos.Filtrar (como en Pandas): Seleccionar todos los registros donde id_sensor sea 'TEMP_A'.Calcular (como en NumPy): Calcular la media de valor solo para 'TEMP_A'.import numpy as np

print("\n--- 3. Desafío: Structured Arrays ---")

# Datos "sucios" de Python
datos_tuplas = [
    ('TEMP_A', 1704067200, -25.5),
    ('HUM_B', 1704067200, 80.1),
    ('TEMP_A', 1704067300, -26.0),
    ('TEMP_B', 1704067300, -30.0),
    ('HUM_B', 1704067400, 81.5),
    ('TEMP_A', 1704067500, -25.8)
]

# 1. Definir el 'dtype' estructurado
#    (nombre_columna, tipo_dato)
#    'U10' = String Unicode de max 10 chars
#    'i8' = int64 (para el timestamp)
#    'f8' = float64 (para el valor)
dtype_estructurado = [
    ('id_sensor', 'U10'), 
    ('timestamp', 'i8'), 
    ('valor', 'f8')
]

# 2. Crear el array
datos = np.array(datos_tuplas, dtype=dtype_estructurado)

print(f"Array Estructurado:\n{datos}")
print(f"\nShape: {datos.shape}") # (6,) -> Es un array 1D de "estructuras"
print(f"DType: {datos.dtype}")

# 3. Filtrar (¡Como en Pandas!)
#    Podemos acceder a una "columna" por su nombre
print(f"\nColumna 'id_sensor': {datos['id_sensor']}")

#    Crear una máscara booleana sobre esa columna
mask_temp_a = (datos['id_sensor'] == 'TEMP_A')
print(f"Máscara 'TEMP_A': {mask_temp_a}")

#    Aplicar la máscara al array completo
registros_temp_a = datos[mask_temp_a]
print(f"Registros 'TEMP_A':\n{registros_temp_a}")

# 4. Calcular (¡Como en NumPy!)
#    Coger la columna 'valor' DE LOS REGISTROS FILTRADOS
#    y calcular la media.
valores_temp_a = registros_temp_a['valor']
media_temp_a = np.mean(valores_temp_a)

print(f"\nValores de 'TEMP_A': {valores_temp_a}")
print(f"Media de 'TEMP_A': {media_temp_a:.2f}") # (-25.5 - 26.0 - 25.8) / 3
Archivo: modulo_1_gran_final.mdMódulo 1 (Gran Final): NumPy CapstoneFilosofía: Esta es la prueba final. Aquí no se trata de aprender una función, sino de diseñar una solución combinando todo lo aprendido (Módulo 0 y Módulo 1) para resolver problemas de data science del mundo real.1. Desafío: Broadcasting Avanzado (K-Means "desde cero")Escenario: Tienes 100 puntos de datos en 2D (shape (100, 2)) y 3 "centroides" de clusters (shape (3, 2)).El Reto: Calcular una matriz de distancias de (100, 3) donde dist[i, j] sea la distancia euclidiana entre el punto i y el centroide j. Luego, asignar cada punto a su centroide más cercano. Todo esto sin un solo bucle for.import numpy as np

print("--- 1. Desafío: Broadcasting Avanzado (K-Means) ---")
np.random.seed(42)

# 1. Generar datos
n_puntos = 100
n_features = 2 # 2D
n_clusters = 3

puntos = np.random.rand(n_puntos, n_features) * 10
centroides = np.random.rand(n_clusters, n_features) * 10

print(f"Shape Puntos: {puntos.shape}")
print(f"Shape Centroides: {centroides.shape}")

# 2. El truco: Expandir dimensiones para el Broadcasting
#    Queremos restar (100, 2) de (3, 2) de forma "cruzada".
#    puntos -> (100, 1, 2)
#    centroides -> (1, 3, 2)
puntos_exp = puntos[:, np.newaxis, :]
centroides_exp = centroides[np.newaxis, :, :]

print(f"\nShape Puntos (expandido): {puntos_exp.shape}")
print(f"Shape Centroides (expandido): {centroides_exp.shape}")

# 3. Restar (Broadcasting mágico)
#    NumPy "estira" ambos arrays para que coincidan
#    El resultado es (100, 3, 2)
#    Donde [i, j, :] es el vector de diferencia entre punto i y centroide j
vectores_distancia = puntos_exp - centroides_exp
print(f"\nShape Vectores Distancia: {vectores_distancia.shape}")

# 4. Calcular distancias euclidianas
#    Dist = sqrt(sum(diff^2))
dist_sq = np.sum(vectores_distancia**2, axis=2) # Sumar en el eje de features (axis=2)
distancias = np.sqrt(dist_sq)
print(f"Shape Matriz de Distancias: {distancias.shape}") # (100, 3)

# 5. Asignar cada punto al cluster más cercano
#    `np.argmin` sobre el eje 1 (los clusters)
asignacion_clusters = np.argmin(distancias, axis=1)

print(f"\nShape Asignaciones: {asignacion_clusters.shape}")
print("\nAsignación de los primeros 10 puntos:")
print(asignacion_clusters[:10]) # [2, 0, 1, 0, 0, 2, 2, 0, 1, 0]

# 6. (Extra) Calcular la media de los puntos por cluster (Módulo 0)
for k in range(n_clusters):
    mask_cluster = (asignacion_clusters == k)
    puntos_en_cluster = puntos[mask_cluster]
    print(f"\nCluster {k}: {len(puntos_en_cluster)} puntos")
    if len(puntos_en_cluster) > 0:
        print(f"  Centroide original: {centroides[k]}")
        print(f"  Centroide (calculado): {np.mean(puntos_en_cluster, axis=0)}")
2. Desafío: Apilado hstack (One-Hot Encoding Manual)Escenario: Tienes un dataset mixto. Una matriz numérica de (10, 3) (edad, altura, peso) y un array categórico (10,) (país: 'ES', 'MX', 'AR').El Reto: Convertir el array categórico a One-Hot Encoding (OHE) y "pegarlo" (apilarlo horizontalmente) a la matriz numérica para crear una matriz de features final (10, 6).import numpy as np

print("\n--- 2. Desafío: Apilado `hstack` (One-Hot Encoding) ---")
np.random.seed(42)

# 1. Datos de entrada
datos_numericos = np.random.randint(18, 60, size=(10, 3))
datos_categoricos = np.random.choice(['ES', 'MX', 'AR'], size=10)

print("Datos Numéricos:\n", datos_numericos[:5])
print("\nDatos Categóricos:\n", datos_categoricos[:5])

# 2. Identificar categorías únicas (Módulo 0)
categorias = np.unique(datos_categoricos)
n_categorias = len(categorias)
print(f"\nCategorías: {categorias}") # ['AR', 'ES', 'MX']

# 3. Crear el mapeo (Módulo 0)
cat_to_index = {cat: i for i, cat in enumerate(categorias)}

# 4. Crear la matriz OHE (Fancy Indexing)
indices = np.array([cat_to_index[cat] for cat in datos_categoricos])
matriz_ohe = np.zeros((len(datos_categoricos), n_categorias), dtype=int)
matriz_ohe[np.arange(len(datos_categoricos)), indices] = 1

print("\nMatriz OHE:\n", matriz_ohe[:5])

# 5. La operación "zip" (hstack)
#    np.hstack apila arrays horizontalmente (por columnas)
#    Tienen que tener el mismo número de filas
matriz_final = np.hstack((datos_numericos, matriz_ohe))

print(f"\nShape Matriz Final: {matriz_final.shape}")
print("Matriz Final (head 5):\n", matriz_final[:5])
# (Col 0,1,2 = numéricas; Col 3,4,5 = OHE de AR, ES, MX)
3. Desafío: Apilado column_stack (Feature Engineering en TimeSeries)Escenario: Tienes un array de timestamps (N,) y un array de valores de sensor (N,).El Reto: Crear una matriz de features (N, 4) donde las columnas sean: [valor, hora_del_dia, dia_de_semana, es_finde]. Esta es la operación "zip" más común en Data Science.import numpy as np

print("\n--- 3. Desafío: Apilado `column_stack` (TimeSeries FE) ---")
np.random.seed(42)

# 1. Generar datos base
timestamps = np.arange('2024-01-01', '2024-01-04', dtype='datetime64[h]')
N = len(timestamps)
valores = np.random.normal(100, 5, N) + (np.arange(N) * 0.1) # Tendencia

print(f"Generados {N} registros.")
print(f"Valores (head): {valores[:5]}")

# 2. Feature Engineering (Módulo 1)
#    Extraer features temporales
dias_desde_epoch = timestamps.astype('datetime64[D]').astype(int)
dia_semana = (dias_desde_epoch + 3) % 7 # 0=Lunes
hora_dia = timestamps.astype('datetime64[h]').astype(int) % 24
es_finde = (dia_semana >= 5).astype(int) # 1 si finde, 0 si no

# 3. La operación "zip" (column_stack)
#    np.column_stack toma una lista de arrays 1D (N,) y los
#    convierte en columnas de una matriz 2D (N, k)
matriz_features = np.column_stack((
    valores, 
    hora_dia, 
    dia_semana, 
    es_finde
))

print(f"\nShape Matriz Features: {matriz_features.shape}")
print("\nMatriz de Features (head 5):")
print("[Valor, Hora, DiaSem, EsFinde]")
print(matriz_features[:5])
4. Desafío: La "Operación Secreta" (np.einsum)Escenario: Tienes un "batch" de 10 matrices (10, 5, 4) y un "batch" de 10 vectores (10, 4). Quieres hacer 10 productos "matriz-vector" independientes.El Reto: Hacerlo en una sola línea de código usando np.einsum (Suma de Einstein), la herramienta más densa pero potente de NumPy para álgebra tensorial.import numpy as np

print("\n--- 4. Desafío: `np.einsum` (Batch Matrix-Vector) ---")
np.random.seed(42)

B = 10 # Tamaño del Batch
N = 5
M = 4

# 1. Datos
batch_matrices = np.random.rand(B, N, M) # (10, 5, 4)
batch_vectores = np.random.rand(B, M)    # (10, 4)

# 2. La solución con `np.einsum`
#    'bnm,bm->bn'
#    b = eje de batch, n = eje de filas, m = eje de columnas
#    Le decimos:
#    1. Coge el array 'bnm' (matrices)
#    2. Coge el array 'bm' (vectores)
#    3. Multiplica y suma sobre el eje 'm' (el eje común)
#    4. Devuélveme un array 'bn'
resultado_einsum = np.einsum('bnm,bm->bn', batch_matrices, batch_vectores)

print(f"Shape Resultado (einsum): {resultado_einsum.shape}") # (10, 5)

# 3. Verificación (con bucle de Python)
#    Así es como lo haríamos "a mano"
resultado_check = np.zeros((B, N))
for i in range(B):
    # (5, 4) @ (4,) -> (5,)
    resultado_check[i] = np.dot(batch_matrices[i], batch_vectores[i])

print(f"Shape Resultado (check): {resultado_check.shape}")

# 4. Comprobar que son idénticos
print(f"\n¿Son idénticos los resultados? {np.allclose(resultado_einsum, resultado_check)}")

# ---
print("\nEjemplo 2 `einsum`: Traza de un batch (suma de diagonales)")
# 'bnn->b' -> Coge un batch de matrices (b,n,n) y suma por la diagonal (n=n)
matrices_cuadradas = np.random.rand(B, 3, 3)
trazas = np.einsum('bnn->b', matrices_cuadradas)
print(f"Trazas (shape {trazas.shape}):\n {trazas}")

# Verificación
trazas_check = np.trace(matrices_cuadradas, axis1=1, axis2=2)
print(f"¿Son idénticas las trazas? {np.allclose(trazas, trazas_check)}")
Archivo: modulo_1_desafio_imagenes.mdMódulo 1 (Desafío Final): Procesamiento de ImágenesFilosofía: Este es un desafío "capstone". El campo de batalla donde todo lo visto (slicing, dtypes, broadcasting, operaciones de ejes) se une de la forma más visual e intuitiva es el procesamiento de imágenes.Para un data scientist, una imagen no es una foto, es un tensor de uint8 (0-255).Una imagen en escala de grises: (altura, ancho)Una imagen a color: (altura, ancho, 3) (Canales R,G,B)Un "batch" de imágenes (para una red neuronal): (n_imagenes, altura, ancho, 3)Desafío: Procesamiento de Imágenes (Batch Masking)Escenario: Eres un Data Scientist de IA. Tienes un "batch" de 10 imágenes a color de 128x128 píxeles. Quieres aplicar una máscara (un "filtro" circular) a todo el batch de golpe para aumentar tu dataset.El Reto: Crear un batch 4D (10, 128, 128, 3) de imágenes sintéticas. Luego, crear una sola máscara 2D (128, 128) y usar la magia del broadcasting para aplicarla a las 10 imágenes (y sus 3 canales) de una sola vez.import numpy as np
# (matplotlib es solo para la verificación visual, no es parte del reto)
# import matplotlib.pyplot as plt 

print("--- Desafío Final: Batch de Imágenes y Broadcasting ---")
np.random.seed(42)

# 1. Definir dimensiones
B = 10  # n_imagenes (Batch size)
H = 128 # Altura (Height)
W = 128 # Ancho (Width)
C = 3   # Canales (R, G, B)

# 2. Generar el batch de imágenes sintéticas
#    `uint8` es el tipo de dato ESTÁNDAR para imágenes
#    Crearemos un fondo azul con un cuadrado verde en el centro
images_batch = np.zeros((B, H, W, C), dtype=np.uint8)

# Fondo azul (R=0, G=0, B=255)
images_batch[..., 2] = 255 

# Cuadrado verde (R=0, G=255, B=0)
# Usamos slicing para seleccionar el centro de TODAS las imágenes del batch
images_batch[:, 32:96, 32:96, 1] = 255 

print(f"Shape del Batch de Imágenes: {images_batch.shape}")
print(f"Tipo de dato: {images_batch.dtype}")

# 3. Crear UNA máscara 2D (la operación "chula")
#    Usamos `np.meshgrid` para crear un "mapa de coordenadas"
x = np.linspace(-1, 1, W) # Coordenadas X de -1 a 1
y = np.linspace(-1, 1, H) # Coordenadas Y de -1 a 1
xx, yy = np.meshgrid(x, y)

# Calcular la distancia al centro (Teorema de Pitágoras)
# dist = sqrt(x^2 + y^2)
distancia_centro = np.sqrt(xx**2 + yy**2)

# Crear una máscara circular (todo lo que esté a > 1 de radio, es 0)
# (Lo escalamos a float 0.0-1.0 para que sea un "filtro")
mascara_2d = 1.0 - distancia_centro
mascara_2d[mascara_2d < 0] = 0.0 # Clip

print(f"\nShape de la Máscara 2D: {mascara_2d.shape}")
print(f"Tipo de dato: {mascara_2d.dtype}")

# 4. El "Ostión": Aplicar la máscara 2D al Batch 4D
#    Shape de Imágenes: (10, 128, 128, 3)
#    Shape de Máscara:   (128, 128)
#
#    ¡No son compatibles! Necesitamos "alinear los ejes".
#    Queremos que la máscara se aplique a cada canal (C)
#    y a cada imagen (B) por igual.

#    Expandimos la máscara a (1, 128, 128, 1)
mascara_expandida = mascara_2d[np.newaxis, :, :, np.newaxis]
print(f"\nShape Máscara Expandida: {mascara_expandida.shape}")

# 5. La operación de Broadcasting
#    NumPy ve: (10, 128, 128, 3) * (1, 128, 128, 1)
#    "Estira" el eje 0 (batch) de 1 a 10
#    "Estira" el eje 3 (canal) de 1 a 3
#    ...y realiza 10*128*128*3 multiplicaciones.
#    (Convertimos a float para la multiplicación y luego a uint8)

imagenes_filtradas = images_batch.astype(np.float32) * mascara_expandida
imagenes_filtradas = imagenes_filtradas.astype(np.uint8)

print("\n¡Operación de broadcasting completada!")
print(f"Shape final: {imagenes_filtradas.shape}")

# 6. Verificación
#    Comprobamos que las esquinas de la primera imagen están a 0
print("\nVerificación de la Imagen 0:")
print("Esquina Superior Izq (R,G,B):", imagenes_filtradas[0, 0, 0, :])
print("Esquina Inferior Der (R,G,B):", imagenes_filtradas[0, -1, -1, :])
print("Centro de la Imagen (R,G,B):", imagenes_filtradas[0, 64, 64, :]) # Debe ser (0, 255, 0)
                                                                 # (porque máscara=1 en el centro)

# --- Visualización (Opcional, si tienes matplotlib) ---
# import matplotlib.pyplot as plts
# fig, ax = plt.subplots(1, 2)
# ax[0].imshow(images_batch[0])
# ax[0].set_title("Imagen Original [0]")
# ax[1].imshow(imagenes_filtradas[0])
# ax[1].set_title("Imagen Filtrada [0]")
# plt.show()
