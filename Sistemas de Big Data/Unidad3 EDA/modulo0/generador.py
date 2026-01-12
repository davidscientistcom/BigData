import pandas as pd
import numpy as np

def generate_antarctic_data(n_records=100, missing_rate=0.05, outlier_rate=0.02, seed=None):
    """
    Genera un DataFrame de Pandas simulando datos de una estación de investigación antártica.

    Args:
        n_records (int): Número de registros a generar.
        missing_rate (float): Proporción de valores faltantes (NaN) a introducir (0 a 1).
        outlier_rate (float): Proporción de outliers a introducir en columnas numéricas (0 a 1).
        seed (int, optional): Semilla para la generación aleatoria para reproducibilidad.

    Returns:
        pd.DataFrame: DataFrame con los datos simulados.
    """
    if seed:
        np.random.seed(seed)

    # --- Generación de Datos Base ---

    # IDs de Sensor (Categórica Nominal)
    sensor_ids_options = ['TEMP_A', 'TEMP_B', 'HUM_A', 'PENG_C', 'ICE_S']
    sensor_id = np.random.choice(sensor_ids_options, n_records)

    # Timestamp (Tipo Temporal - para uso posterior)
    # Genera timestamps horarios terminando ahora, hora local por defecto
    timestamps = pd.date_range(end=pd.Timestamp.now(tz='Europe/Madrid'), periods=n_records, freq='h')

    # Temperatura (°C) (Numérica Continua)
    # Simulación con un paseo aleatorio + tendencia + ruido estacional leve
    temp_base = np.random.normal(-25, 10) # Temperatura base media
    temp_trend = np.linspace(0, np.random.choice([-5, 5]), n_records) # Tendencia lineal aleatoria
    temp_seasonal = 3 * np.sin(np.linspace(0, 4 * np.pi, n_records)) # Ciclo diario simulado
    temp_noise = np.random.normal(0, 1.5, n_records) # Ruido aleatorio
    # Paseo aleatorio para simular cambios graduales
    temp_random_walk = np.random.normal(0, 0.8, n_records).cumsum()
    temperature_c = temp_base + temp_trend + temp_seasonal + temp_noise + temp_random_walk

    # Humedad (%) (Numérica Continua, rango 0-100)
    # Simulación simple con clipping para asegurar el rango
    humidity_perc = np.random.uniform(30, 90, n_records) + np.random.normal(0, 5, n_records)
    humidity_perc = np.clip(humidity_perc, 0, 100) # Asegurar que esté entre 0 y 100

    # Conteo de Pingüinos (Numérica Discreta)
    # Simulación usando distribución de Poisson
    avg_penguins = np.random.randint(50, 500) # Promedio variable de pingüinos
    penguin_count = np.random.poisson(avg_penguins, n_records).astype(float) # Convertir a float para permitir NaN luego

    # Condición del Hielo (Categórica Ordinal)
    ice_conditions_options = ['Stable', 'Cracking', 'Hazardous']
    # Probabilidades sesgadas: Mayoría estable, algo agrietándose, poco peligroso
    ice_condition_raw = np.random.choice(ice_conditions_options, n_records, p=[0.7, 0.25, 0.05])
    # Convertir a tipo categórico ordenado de Pandas
    ice_condition = pd.Categorical(ice_condition_raw, categories=ice_conditions_options, ordered=True)

    # Estado del Sensor (Categórica Nominal)
    sensor_statuses_options = ['OK', 'ERROR', 'MAINTENANCE']
     # Probabilidades sesgadas: La mayoría OK, pocos errores o mantenimiento
    sensor_status = np.random.choice(sensor_statuses_options, n_records, p=[0.9, 0.07, 0.03])

    # Crear DataFrame inicial
    df = pd.DataFrame({
        'timestamp': timestamps,
        'sensor_id': sensor_id,
        'temperature_c': temperature_c,
        'humidity_perc': humidity_perc,
        'penguin_count': penguin_count,
        'ice_condition': ice_condition,
        'sensor_status': sensor_status
    })

    # --- Introducción de Problemas (Stack de Modificaciones) ---

    # Introducir Outliers en columnas numéricas
    if outlier_rate > 0 and n_records > 0:
        n_outliers = max(1, int(n_records * outlier_rate)) # Asegurar al menos 1 si rate > 0

        # Outliers de Temperatura (valores muy altos o bajos)
        temp_outlier_indices = np.random.choice(df.index, n_outliers, replace=False)
        df.loc[temp_outlier_indices, 'temperature_c'] += np.random.choice([-1, 1], n_outliers) * np.random.uniform(50, 100, n_outliers)

        # Outliers de Humedad (cercanos a 0% o 100% donde no deberían)
        hum_outlier_indices = np.random.choice(df.index, n_outliers, replace=False)
        df.loc[hum_outlier_indices, 'humidity_perc'] = np.random.choice([np.random.uniform(0, 10), np.random.uniform(95, 100)], n_outliers)
        df['humidity_perc'] = np.clip(df['humidity_perc'], 0, 100) # Re-clip por si acaso

        # Outliers de Conteo de Pingüinos (valores exageradamente altos)
        count_outlier_indices = np.random.choice(df.index, n_outliers, replace=False)
        df.loc[count_outlier_indices, 'penguin_count'] += np.random.randint(1000, 5000, n_outliers)


    # Introducir Missing Values (NaN) en columnas seleccionadas
    if missing_rate > 0 and n_records > 0:
        cols_to_nan = ['temperature_c', 'humidity_perc', 'penguin_count', 'ice_condition', 'sensor_status']
        mask = np.random.choice([True, False], size=(n_records, len(cols_to_nan)),
                                p=[missing_rate, 1 - missing_rate])

        for i, col in enumerate(cols_to_nan):
             # Aplicar NaN donde la máscara es True para esta columna
             # Usar .loc para evitar SettingWithCopyWarning
            df.loc[mask[:, i], col] = np.nan

            # Importante: Si la columna era categórica, hay que reconvertirla
            # porque .loc[mask, col] = np.nan la convierte a 'object' o 'float'
            if col == 'ice_condition':
                 df[col] = pd.Categorical(df[col], categories=ice_conditions_options, ordered=True)
            # Podríamos hacer lo mismo para sensor_status si la hubiéramos hecho category antes

    # Mezclar el orden de las filas para que no esté ordenado por tiempo
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    return df

# --- Ejemplo de uso ---
if __name__ == '__main__':
    # Generar un dataset con algunos problemas
    df_example = generate_antarctic_data(n_records=150, missing_rate=0.1, outlier_rate=0.05, seed=123)

    print("--- Ejemplo de Dataset Generado ---")
    print(df_example.head())
    print("\n--- Información del Dataset ---")
    df_example.info()
    print("\n--- Descripción Estadística (Numéricas) ---")
    print(df_example.describe())
    print("\n--- Conteo de Nulos por Columna ---")
    print(df_example.isnull().sum())
    print("\n--- Conteo de Categorías (Estado Sensor) ---")
    print(df_example['sensor_status'].value_counts(dropna=False)) # Incluir NaNs en el conteo
    print("\n--- Conteo de Categorías (Condición Hielo) ---")
    print(df_example['ice_condition'].value_counts(dropna=False)) # Incluir NaNs en el conteo
