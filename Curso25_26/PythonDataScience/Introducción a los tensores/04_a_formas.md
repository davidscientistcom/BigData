# Capítulo 3: Ejemplos Resueltos con Operaciones sobre Tensores en un Dataset Empresarial

## 3.1 Introducción

En este capítulo, aplicaremos las operaciones básicas sobre tensores vistas anteriormente a un conjunto de datos relacionado con el mundo empresarial. Crearemos un dataset ficticio que representa información de ventas y clientes de una empresa, incluyendo variables de distintos tipos: continuas, discretas y categóricas. A través de ejemplos resueltos, exploraremos cómo manipular y analizar este dataset utilizando las funcionalidades de PyTorch.

Este enfoque práctico te ayudará a consolidar los conceptos aprendidos y te preparará para abordar problemas más complejos en el ámbito del análisis de datos y el aprendizaje automático.

## 3.2 Creación del Dataset Empresarial

### 3.2.1 Descripción del Dataset

Nuestro dataset representará las ventas de una empresa que comercializa varios productos en diferentes regiones. Incluirá información sobre:

- **ID de Venta**: Identificador único de cada transacción (discreto).
- **ID de Producto**: Identificador del producto vendido (discreto).
- **Categoría del Producto**: Categoría a la que pertenece el producto (categórico nominal).
- **Cantidad Vendida**: Número de unidades vendidas (discreto).
- **Precio Unitario**: Precio por unidad del producto (continuo).
- **Ingresos Totales**: Ingresos generados por la venta (continuo).
- **Fecha de Venta**: Fecha en que se realizó la venta (categórico ordinal).
- **Edad del Cliente**: Edad del cliente que realizó la compra (continuo).
- **Género del Cliente**: Género del cliente (categórico nominal).
- **Región**: Región donde se realizó la venta (categórico nominal).
- **Puntaje de Satisfacción**: Calificación del cliente sobre su experiencia (ordinal).

### 3.2.2 Generación del Dataset

```python
import torch
import numpy as np
import pandas as pd

# Definir el número de registros
num_records = 1000

# Generar IDs de Venta
venta_id = torch.arange(1, num_records + 1)

# Generar IDs de Producto aleatorios entre 1 y 50
producto_id = torch.randint(1, 51, (num_records,))

# Categorías de Producto
categorias = ['Electrónica', 'Ropa', 'Hogar', 'Libros', 'Juguetes']
categoria_indices = torch.randint(0, len(categorias), (num_records,))
producto_categoria = [categorias[i] for i in categoria_indices]

# Cantidad Vendida entre 1 y 20
cantidad_vendida = torch.randint(1, 21, (num_records,))

# Precio Unitario entre $5 y $500
precio_unitario = torch.rand(num_records) * 495 + 5  # [5, 500]

# Ingresos Totales
ingresos_totales = cantidad_vendida * precio_unitario

# Fechas de Venta en 2022
fechas = pd.date_range(start='2022-01-01', end='2022-12-31', periods=num_records)
fecha_venta = torch.tensor(fechas.astype(np.int64) // 10**9)  # Convertir a timestamp

# Edad del Cliente entre 18 y 70
edad_cliente = torch.randint(18, 71, (num_records,))

# Género del Cliente
generos = ['Masculino', 'Femenino', 'No Especificado']
genero_indices = torch.randint(0, len(generos), (num_records,))
genero_cliente = [generos[i] for i in genero_indices]

# Regiones
regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
region_indices = torch.randint(0, len(regiones), (num_records,))
region = [regiones[i] for i in region_indices]

# Puntaje de Satisfacción entre 1 y 5
puntaje_satisfaccion = torch.randint(1, 6, (num_records,))
```

### 3.2.3 Creación del DataFrame

Para visualizar mejor el dataset y facilitar algunas operaciones, combinaremos los tensores en un DataFrame de Pandas.

```python
# Crear un diccionario con los datos
data = {
    'VentaID': venta_id.numpy(),
    'ProductoID': producto_id.numpy(),
    'ProductoCategoria': producto_categoria,
    'CantidadVendida': cantidad_vendida.numpy(),
    'PrecioUnitario': precio_unitario.numpy(),
    'IngresosTotales': ingresos_totales.numpy(),
    'FechaVenta': pd.to_datetime(fechas),
    'EdadCliente': edad_cliente.numpy(),
    'GeneroCliente': genero_cliente,
    'Region': region,
    'PuntajeSatisfaccion': puntaje_satisfaccion.numpy()
}

# Crear el DataFrame
df = pd.DataFrame(data)
```

Ahora tenemos un dataset con 1000 registros y 11 columnas, que incluye variables de diferentes tipos.

## 3.3 Conversión de Datos Categóricos a Tensores

Para realizar operaciones con PyTorch, necesitamos convertir las variables categóricas a tensores numéricos. Esto se puede lograr mediante codificación de etiquetas (Label Encoding) o codificación one-hot.

### 3.3.1 Codificación de Etiquetas

Convertiremos las variables categóricas a números enteros.

```python
from sklearn.preprocessing import LabelEncoder

# Codificar ProductoCategoria
le_categoria = LabelEncoder()
producto_categoria_encoded = le_categoria.fit_transform(df['ProductoCategoria'])

# Codificar GeneroCliente
le_genero = LabelEncoder()
genero_cliente_encoded = le_genero.fit_transform(df['GeneroCliente'])

# Codificar Region
le_region = LabelEncoder()
region_encoded = le_region.fit_transform(df['Region'])
```

### 3.3.2 Creación de Tensores Finales

Creamos un tensor para cada variable, asegurándonos de que todas tengan el mismo tipo de datos cuando sea necesario.

```python
# Convertir a tensores
venta_id = torch.tensor(df['VentaID'].values)
producto_id = torch.tensor(df['ProductoID'].values)
producto_categoria = torch.tensor(producto_categoria_encoded)
cantidad_vendida = torch.tensor(df['CantidadVendida'].values)
precio_unitario = torch.tensor(df['PrecioUnitario'].values)
ingresos_totales = torch.tensor(df['IngresosTotales'].values)
fecha_venta = torch.tensor(df['FechaVenta'].astype(np.int64) // 10**9)  # Timestamp
edad_cliente = torch.tensor(df['EdadCliente'].values)
genero_cliente = torch.tensor(genero_cliente_encoded)
region = torch.tensor(region_encoded)
puntaje_satisfaccion = torch.tensor(df['PuntajeSatisfaccion'].values)
```

**Nota:** Al convertir `PrecioUnitario` e `IngresosTotales` a tensores, debemos asegurarnos de que sean de tipo `torch.float32` para operaciones precisas.

```python
precio_unitario = torch.tensor(df['PrecioUnitario'].values, dtype=torch.float32)
ingresos_totales = torch.tensor(df['IngresosTotales'].values, dtype=torch.float32)
```

## 3.4 Ejemplos Resueltos con Operaciones sobre Tensores

A continuación, realizaremos varias operaciones utilizando los tensores creados, aplicando las funciones y métodos aprendidos en el capítulo anterior.

### 3.4.1 Cálculo del Ingreso Total por Categoría de Producto

Queremos calcular el ingreso total generado por cada categoría de producto.

#### Pasos:

1. Obtener los ingresos totales y las categorías de producto.
2. Agrupar los ingresos por categoría.
3. Sumar los ingresos dentro de cada categoría.

#### Implementación:

```python
# Obtener el número de categorías
num_categorias = len(le_categoria.classes_)

# Crear un tensor para acumular los ingresos por categoría
ingresos_por_categoria = torch.zeros(num_categorias)

# Recorrer cada categoría y sumar los ingresos
for i in range(num_categorias):
    # Crear una máscara para la categoría actual
    mask = (producto_categoria == i)
    # Sumar los ingresos para esa categoría
    ingresos_por_categoria[i] = ingresos_totales[mask].sum()
```

#### Mostrar los resultados:

```python
for i in range(num_categorias):
    categoria = le_categoria.inverse_transform([i])[0]
    ingreso = ingresos_por_categoria[i].item()
    print(f"Ingreso total para {categoria}: ${ingreso:,.2f}")
```

#### Resultado (Ejemplo):

```
Ingreso total para Electrónica: $6,354,897.45
Ingreso total para Ropa: $4,256,123.67
Ingreso total para Hogar: $5,123,456.78
Ingreso total para Libros: $3,789,012.34
Ingreso total para Juguetes: $2,567,890.12
```

**Nota:** Los valores son ilustrativos.

### 3.4.2 Cálculo de la Cantidad Promedio Vendida por Región

Queremos calcular la cantidad promedio de productos vendidos en cada región.

#### Pasos:

1. Obtener la cantidad vendida y las regiones.
2. Agrupar la cantidad vendida por región.
3. Calcular la media dentro de cada grupo.

#### Implementación:

```python
# Obtener el número de regiones
num_regiones = len(le_region.classes_)

# Crear tensores para acumular las cantidades y contar los registros por región
suma_cantidad_por_region = torch.zeros(num_regiones)
conteo_por_region = torch.zeros(num_regiones)

# Recorrer cada región y acumular los datos
for i in range(num_regiones):
    # Crear una máscara para la región actual
    mask = (region == i)
    # Sumar la cantidad vendida
    suma_cantidad_por_region[i] = cantidad_vendida[mask].sum()
    # Contar el número de ventas
    conteo_por_region[i] = mask.sum()

# Calcular la cantidad promedio por región
promedio_cantidad_por_region = suma_cantidad_por_region / conteo_por_region
```

#### Mostrar los resultados:

```python
for i in range(num_regiones):
    region_nombre = le_region.inverse_transform([i])[0]
    promedio = promedio_cantidad_por_region[i].item()
    print(f"Cantidad promedio vendida en {region_nombre}: {promedio:.2f} unidades")
```

#### Resultado (Ejemplo):

```
Cantidad promedio vendida en Centro: 10.25 unidades
Cantidad promedio vendida en Este: 9.87 unidades
Cantidad promedio vendida en Norte: 11.02 unidades
Cantidad promedio vendida en Oeste: 8.76 unidades
Cantidad promedio vendida en Sur: 9.54 unidades
```

### 3.4.3 Análisis de la Distribución de Edades de los Clientes

Queremos analizar la distribución de edades de los clientes y calcular estadísticas básicas.

#### Pasos:

1. Obtener la edad de los clientes.
2. Calcular la edad mínima, máxima, media y desviación estándar.

#### Implementación:

```python
# Convertir a tipo float para precisión en cálculos estadísticos
edad_cliente_float = edad_cliente.float()

edad_min = edad_cliente_float.min()
edad_max = edad_cliente_float.max()
edad_media = edad_cliente_float.mean()
edad_std = edad_cliente_float.std()
```

#### Mostrar los resultados:

```python
print(f"Edad mínima: {edad_min.item()} años")
print(f"Edad máxima: {edad_max.item()} años")
print(f"Edad media: {edad_media.item():.2f} años")
print(f"Desviación estándar: {edad_std.item():.2f} años")
```

#### Resultado (Ejemplo):

```
Edad mínima: 18 años
Edad máxima: 70 años
Edad media: 44.35 años
Desviación estándar: 15.62 años
```

### 3.4.4 Filtrar Ventas con Puntaje de Satisfacción Máximo

Queremos obtener las ventas donde los clientes dieron el puntaje máximo de satisfacción (5).

#### Pasos:

1. Crear una máscara donde el puntaje de satisfacción es 5.
2. Filtrar los IDs de venta y los ingresos totales correspondientes.

#### Implementación:

```python
# Crear la máscara
mask_satisfaccion_max = (puntaje_satisfaccion == 5)

# Filtrar los datos
ventas_id_satisfechas = venta_id[mask_satisfaccion_max]
ingresos_satisfechos = ingresos_totales[mask_satisfaccion_max]
```

#### Mostrar los resultados:

```python
num_ventas_satisfechas = ventas_id_satisfechas.size(0)
ingreso_total_satisfechos = ingresos_satisfechos.sum().item()

print(f"Número de ventas con puntaje máximo: {num_ventas_satisfechas}")
print(f"Ingreso total de ventas con puntaje máximo: ${ingreso_total_satisfechos:,.2f}")
```

#### Resultado (Ejemplo):

```
Número de ventas con puntaje máximo: 200
Ingreso total de ventas con puntaje máximo: $1,234,567.89
```

### 3.4.5 Comparación de Ingresos entre Géneros

Queremos comparar los ingresos totales generados por clientes de diferentes géneros.

#### Pasos:

1. Identificar los índices correspondientes a cada género.
2. Calcular los ingresos totales para cada género.

#### Implementación:

```python
# Obtener el número de géneros
num_generos = len(le_genero.classes_)

# Crear un tensor para acumular los ingresos por género
ingresos_por_genero = torch.zeros(num_generos)

# Recorrer cada género y sumar los ingresos
for i in range(num_generos):
    mask = (genero_cliente == i)
    ingresos_por_genero[i] = ingresos_totales[mask].sum()
```

#### Mostrar los resultados:

```python
for i in range(num_generos):
    genero_nombre = le_genero.inverse_transform([i])[0]
    ingreso = ingresos_por_genero[i].item()
    print(f"Ingreso total para género {genero_nombre}: ${ingreso:,.2f}")
```

#### Resultado (Ejemplo):

```
Ingreso total para género Femenino: $4,567,890.12
Ingreso total para género Masculino: $5,678,901.23
Ingreso total para género No Especificado: $2,345,678.90
```

### 3.4.6 Análisis Temporal de Ventas

Queremos analizar cómo evolucionaron las ventas a lo largo del tiempo.

#### Pasos:

1. Convertir las fechas de venta a meses.
2. Agrupar los ingresos por mes.
3. Graficar los ingresos mensuales.

#### Implementación:

```python
import matplotlib.pyplot as plt

# Convertir timestamp a objeto datetime
fechas_datetime = pd.to_datetime(fecha_venta.numpy(), unit='s')

# Extraer el mes de la fecha
meses = torch.tensor(fechas_datetime.month)

# Crear un tensor para acumular los ingresos por mes
ingresos_por_mes = torch.zeros(12)

# Sumar los ingresos por mes
for i in range(1, 13):
    mask = (meses == i)
    ingresos_por_mes[i - 1] = ingresos_totales[mask].sum()
```

#### Graficar los resultados:

```python
meses_labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

plt.figure(figsize=(10, 6))
plt.bar(meses_labels, ingresos_por_mes.numpy())
plt.xlabel('Mes')
plt.ylabel('Ingresos Totales')
plt.title('Ingresos Mensuales en 2022')
plt.show()
```

#### Resultado:

El gráfico mostrará una barra para cada mes con los ingresos totales, permitiendo visualizar tendencias estacionales o picos de ventas.

### 3.4.7 Cálculo del Precio Promedio por Categoría de Producto

Queremos calcular el precio unitario promedio de los productos en cada categoría.

#### Pasos:

1. Obtener el precio unitario y las categorías de producto.
2. Agrupar los precios por categoría.
3. Calcular la media de los precios en cada grupo.

#### Implementación:

```python
# Crear tensores para acumular los precios y contar los productos por categoría
suma_precio_por_categoria = torch.zeros(num_categorias)
conteo_por_categoria = torch.zeros(num_categorias)

# Recorrer cada categoría y acumular los datos
for i in range(num_categorias):
    mask = (producto_categoria == i)
    suma_precio_por_categoria[i] = precio_unitario[mask].sum()
    conteo_por_categoria[i] = mask.sum()

# Calcular el precio promedio por categoría
promedio_precio_por_categoria = suma_precio_por_categoria / conteo_por_categoria
```

#### Mostrar los resultados:

```python
for i in range(num_categorias):
    categoria = le_categoria.inverse_transform([i])[0]
    promedio = promedio_precio_por_categoria[i].item()
    print(f"Precio unitario promedio para {categoria}: ${promedio:.2f}")
```

#### Resultado (Ejemplo):

```
Precio unitario promedio para Electrónica: $250.45
Precio unitario promedio para Ropa: $45.67
Precio unitario promedio para Hogar: $120.89
Precio unitario promedio para Libros: $30.12
Precio unitario promedio para Juguetes: $75.34
```

### 3.4.8 Identificación de las Ventas Más Altas

Queremos identificar las 5 ventas con mayores ingresos totales.

#### Pasos:

1. Ordenar los ingresos totales en orden descendente.
2. Obtener los índices de las 5 ventas más altas.
3. Recuperar la información correspondiente a esas ventas.

#### Implementación:

```python
# Obtener los índices ordenados en orden descendente
_, indices_ordenados = ingresos_totales.sort(descending=True)

# Obtener los índices de las 5 ventas más altas
top_5_indices = indices_ordenados[:5]

# Extraer la información de las ventas
top_5_ventas = {
    'VentaID': venta_id[top_5_indices],
    'IngresosTotales': ingresos_totales[top_5_indices],
    'ProductoID': producto_id[top_5_indices],
    'CantidadVendida': cantidad_vendida[top_5_indices],
    'PrecioUnitario': precio_unitario[top_5_indices]
}
```

#### Mostrar los resultados:

```python
print("Top 5 Ventas con Mayores Ingresos:")
for i in range(5):
    print(f"Venta ID: {top_5_ventas['VentaID'][i].item()}, "
          f"Ingresos: ${top_5_ventas['IngresosTotales'][i].item():,.2f}, "
          f"Producto ID: {top_5_ventas['ProductoID'][i].item()}, "
          f"Cantidad Vendida: {top_5_ventas['CantidadVendida'][i].item()}, "
          f"Precio Unitario: ${top_5_ventas['PrecioUnitario'][i].item():.2f}")
```

#### Resultado (Ejemplo):

```
Top 5 Ventas con Mayores Ingresos:
Venta ID: 123, Ingresos: $9,876.54, Producto ID: 45, Cantidad Vendida: 20, Precio Unitario: $493.83
Venta ID: 456, Ingresos: $9,765.43, Producto ID: 12, Cantidad Vendida: 19, Precio Unitario: $513.44
Venta ID: 789, Ingresos: $9,654.32, Producto ID: 37, Cantidad Vendida: 18, Precio Unitario: $536.35
Venta ID: 234, Ingresos: $9,543.21, Producto ID: 25, Cantidad Vendida: 17, Precio Unitario: $561.37
Venta ID: 567, Ingresos: $9,432.10, Producto ID: 8, Cantidad Vendida: 16, Precio Unitario: $589.51
```

### 3.4.9 Cálculo del Puntaje de Satisfacción Promedio por Categoría

Queremos saber cuál es el puntaje de satisfacción promedio por categoría de producto.

#### Pasos:

1. Obtener el puntaje de satisfacción y las categorías de producto.
2. Agrupar los puntajes por categoría.
3. Calcular la media dentro de cada grupo.

#### Implementación:

```python
# Crear tensores para acumular los puntajes y contar los registros por categoría
suma_puntaje_por_categoria = torch.zeros(num_categorias)
conteo_por_categoria = torch.zeros(num_categorias)

# Recorrer cada categoría y acumular los datos
for i in range(num_categorias):
    mask = (producto_categoria == i)
    suma_puntaje_por_categoria[i] = puntaje_satisfaccion[mask].sum()
    conteo_por_categoria[i] = mask.sum()

# Calcular el puntaje promedio por categoría
promedio_puntaje_por_categoria = suma_puntaje_por_categoria / conteo_por_categoria
```

#### Mostrar los resultados:

```python
for i in range(num_categorias):
    categoria = le_categoria.inverse_transform([i])[0]
    promedio = promedio_puntaje_por_categoria[i].item()
    print(f"Puntaje de satisfacción promedio para {categoria}: {promedio:.2f}")
```

#### Resultado (Ejemplo):

```
Puntaje de satisfacción promedio para Electrónica: 4.25
Puntaje de satisfacción promedio para Ropa: 3.87
Puntaje de satisfacción promedio para Hogar: 4.12
Puntaje de satisfacción promedio para Libros: 4.05
Puntaje de satisfacción promedio para Juguetes: 3.95
```

### 3.4.10 Análisis de Correlación entre Edad y Puntaje de Satisfacción

Queremos analizar si existe alguna correlación entre la edad de los clientes y el puntaje de satisfacción otorgado.

#### Pasos:

1. Obtener la edad y el puntaje de satisfacción.
2. Calcular la correlación entre ambas variables.

#### Implementación:

```python
# Convertir a tipo float
edad_cliente_float = edad_cliente.float()
puntaje_satisfaccion_float = puntaje_satisfaccion.float()

# Calcular la media de cada variable
media_edad = edad_cliente_float.mean()
media_puntaje = puntaje_satisfaccion_float.mean()

# Calcular las desviaciones de la media
diff_edad = edad_cliente_float - media_edad
diff_puntaje = puntaje_satisfaccion_float - media_puntaje

# Calcular la correlación de Pearson
numerador = (diff_edad * diff_puntaje).sum()
denominador = torch.sqrt((diff_edad ** 2).sum() * (diff_puntaje ** 2).sum())

correlacion = numerador / denominador
```

#### Mostrar el resultado:

```python
print(f"Correlación entre edad y puntaje de satisfacción: {correlacion.item():.4f}")
```

#### Resultado (Ejemplo):

```
Correlación entre edad y puntaje de satisfacción: 0.0523
```

**Interpretación:** Un valor cercano a 0 indica poca o ninguna correlación lineal entre las variables.

## 3.5 Conclusión

A través de estos ejemplos, hemos aplicado operaciones básicas sobre tensores en PyTorch para manipular y analizar un dataset empresarial con variables de distintos tipos. Hemos explorado cómo realizar agregaciones, filtrados, cálculos estadísticos y análisis más complejos, utilizando únicamente las funcionalidades de PyTorch.
