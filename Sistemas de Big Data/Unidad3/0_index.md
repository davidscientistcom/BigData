Temario del Curso: Análisis Descriptivo Experto con Python (Versión Rigurosa)

**Módulo 0: El Lenguaje de los Datos (Tipología de Variables)**
0.1. Por qué la Tipología es el Primer Paso
0.2. Variables Categóricas (Cualitativas): Nominales, Ordinales
0.3. Variables Numéricas (Cuantitativas): Discretas, Continuas (Intervalo, Razón)
0.4. Tipos Especiales (Mención)

**Módulo 1: Recolección, Carga y Calidad del Dato (Paso Clave)**
1.1. Recolección y Carga:
    * Fuentes de datos (CSV, JSON, SQL, APIs).
    * Práctica: `pandas.read_...`, manejo de `dtypes` y parseo.
1.2. Inspección Inicial (Data Quality):
    * El "primer vistazo": `df.head()`, `df.info()`.
    * Identificación de duplicados: `df.duplicated()`.
    * Identificación de cardinalidad (ruido): `df.nunique()`.
    * Identificación de datos corruptos o "valores que no sirven".

**Módulo 2: Fundamentos y Preparación del Entorno**
2.1. El Ecosistema: NumPy, Pandas, Matplotlib, Seaborn
2.2. Fundamentos de Probabilidad para el EDA (PDF, CDF, Distribuciones)
2.3. El Proceso de EDA vs. Preprocesamiento

**Módulo 3: Análisis Univariable (Entendiendo cada variable)**
3.1. Análisis de Variables Categóricas
3.2. Análisis de Variables Numéricas (Tendencia, Dispersión, Forma)
3.3. Análisis de Normalidad (Q-Q Plot)
3.4. Análisis de Outliers (Detección):
    * Teoría: Regla 1.5*IQR vs. Z-Score.
    * (El *tratamiento* se verá en el Módulo 7).

**Módulo 4: Análisis Bivariable Sistemático (Matriz de Cruce)**
4.1. Caso 1: Numérica vs. Numérica (Pearson, Spearman)
4.2. Caso 2: Categórica (Nominal) vs. Numérica
4.3. Caso 3: Categórica (Ordinal) vs. Numérica
4.4. Caso 4: Categórica vs. Categórica (Crosstabs)
4.5. Caso 5: Ordinal vs. Ordinal (Kendall, Spearman)

**Módulo 5: Análisis Multivariable y Patrones**
5.1. Visualización de 3 o más variables (`hue`, `size`, `style`)
5.2. La "Navaja Suiza" del EDA (`seaborn.pairplot`)
5.3. Análisis de Datos Faltantes (Missing Data):
    * Teoría: Tipos (MCAR, MAR, MNAR).
    * Visualización: `seaborn.heatmap(df.isnull())`.
    * (El *tratamiento* se verá en el Módulo 7).
5.4. PCA como Herramienta Descriptiva

**Módulo 6: Análisis Descriptivo de Series Temporales (Nivel Kaggle)**
6.1. Preparación de Datos Temporales
6.2. Análisis de Tendencia y Estacionalidad (Descomposición)
6.3. Análisis de Autocorrelación (ACF, PACF)

**Módulo 7: Accionables del EDA: Limpieza y Transformación (¡NUEVO!)**
7.1. Tratamiento de Datos Faltantes (NaNs)
    * Teoría: *Eliminación vs. Imputación*.
    * Práctica (Eliminación): `df.dropna()`. Pros y contras.
    * Práctica (Imputación Numérica): Media, Mediana. `SimpleImputer`.
    * Práctica (Imputación Categórica): Moda. `SimpleImputer`.
    * Práctica (Avanzada): `KNNImputer`, Imputación por regresión.
7.2. Tratamiento de Outliers
    * Teoría: *Eliminación vs. Transformación vs. Clipping (Winsorizing)*.
    * Práctica (Clipping): `df['col'].clip(lower=q1, upper=q3)`.
7.3. Transformación de Variables (Manejo de Asimetría)
    * Teoría: ¿Por qué transformar? (Manejo de Skewness, supuestos de modelos).
    * Práctica: Transformación Logarítmica (`np.log1p`), Raíz Cuadrada (`np.sqrt`), Box-Cox.
7.4. Escalado y Normalización de Datos (Tu petición)
    * Teoría: ¿Por qué escalar? (Modelos sensibles a la escala: KNN, SVM, PCA, Redes Neuronales).
    * Técnica 1: Estandarización (Z-Score)
        * Matemática: `$z = (x - \mu) / \sigma$`
        * Práctica: `sklearn.preprocessing.StandardScaler`.
        * Cuándo usar: Default. Cuando los datos son (aprox) normales y/o quieres media 0 y std 1.
    * Técnica 2: Normalización (Min-Max)
        * Matemática: `$x' = (x - min) / (max - min)$`
        * Práctica: `sklearn.preprocessing.MinMaxScaler`.
        * Cuándo usar: Cuando se requiere un rango fijo [0, 1] (ej. Redes Neuronales, procesamiento de imágenes). Muy sensible a outliers.
    * Técnica 3: Escalado Robusto (Robust Scaler)
        * Matemática: `$x' = (x - mediana) / IQR$`
        * Práctica: `sklearn.preprocessing.RobustScaler`.
        * Cuándo usar: Cuando el dataset tiene *muchos outliers*, ya que usa la mediana y el IQR, que son robustos a ellos.

**Módulo 8: El Reporte de EDA Experto (Poniéndolo todo junto)**
(Anterior Módulo 6)
8.1. Estructura de un Notebook de EDA Profesional
8.2. EDA para Feature Engineering
8.3. Resumen de *Insights* e Hipótesis para Inferencia.
8.4. Estudio de Caso (Case Study)