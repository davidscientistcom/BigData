# Capítulo 4: Manipulación de la Forma de Tensores y Cálculo de Productos Matriciales en PyTorch

## 4.1 Introducción

La capacidad de manipular la forma y las dimensiones de los tensores es fundamental en PyTorch y en el aprendizaje profundo en general. Las redes neuronales a menudo requieren que los datos se ajusten a formas específicas, y comprender cómo transformar y operar con tensores es esencial para preparar datos, construir modelos y realizar cálculos eficientes.

En este capítulo, nos centraremos en las funciones de PyTorch relacionadas con la forma de los tensores. Utilizaremos el dataset empresarial creado en el capítulo anterior para ilustrar una amplia variedad de ejemplos. Exploraremos cómo cambiar las dimensiones de los tensores, realizar transposiciones, aplanar y expandir tensores, y cómo calcular productos de matrices y vectores para extraer información valiosa de los datos.

## 4.2 Repaso del Dataset Empresarial

Antes de comenzar, recordemos que nuestro dataset incluye información sobre ventas, productos, clientes y otras variables relevantes. Los tensores clave que utilizaremos son:

- `venta_id`: IDs de ventas.
- `producto_id`: IDs de productos.
- `producto_categoria`: Categorías de productos codificadas.
- `cantidad_vendida`: Cantidad de unidades vendidas.
- `precio_unitario`: Precio por unidad.
- `ingresos_totales`: Ingresos generados por cada venta.
- `edad_cliente`: Edad de los clientes.
- `genero_cliente`: Género de los clientes codificado.
- `region`: Regiones codificadas.
- `puntaje_satisfaccion`: Puntaje de satisfacción otorgado por los clientes.

## 4.3 Funciones de PyTorch para Manipular la Forma de Tensores

PyTorch ofrece varias funciones para manipular la forma y las dimensiones de los tensores. A continuación, exploraremos estas funciones en detalle, proporcionando ejemplos prácticos con nuestro dataset.

### 4.3.1 `view()` y `reshape()`

Ambas funciones se utilizan para cambiar la forma de un tensor sin alterar sus datos subyacentes.

- **`view()`**: Reorganiza los datos en un tensor existente, siempre que los elementos sean contiguos en memoria.
- **`reshape()`**: Intenta devolver una vista (`view`) si es posible, pero devuelve una copia (`clone`) si no es posible.

#### Ejemplo 1: Cambiar la Forma de `cantidad_vendida`

Supongamos que queremos reorganizar el tensor `cantidad_vendida`, que originalmente es un tensor de 1 dimensión con forma `(num_records,)`, y convertirlo en un tensor de forma `(num_records, 1)`.

```python
# Forma original
print(cantidad_vendida.shape)  # torch.Size([1000])

# Usando view()
cantidad_vendida_2d = cantidad_vendida.view(-1, 1)
print(cantidad_vendida_2d.shape)  # torch.Size([1000, 1])
```

- El `-1` en `view(-1, 1)` indica que PyTorch calculará automáticamente el tamaño de esa dimensión basándose en el número total de elementos y las otras dimensiones especificadas.

#### Ejemplo 2: Aplanar un Tensor

Si tenemos un tensor de múltiples dimensiones, podemos aplanarlo en una sola dimensión.

```python
# Crear un tensor de ejemplo de 3 dimensiones
tensor_3d = torch.rand(10, 5, 2)

# Aplanar el tensor a 1 dimensión
tensor_flat = tensor_3d.view(-1)
print(tensor_flat.shape)  # torch.Size([100])
```

### 4.3.2 `transpose()` y `permute()`

Estas funciones se utilizan para reordenar las dimensiones de un tensor.

- **`transpose(dim0, dim1)`**: Intercambia dos dimensiones específicas.
- **`permute(dims)`**: Reorganiza todas las dimensiones según el orden especificado.

#### Ejemplo 3: Transponer un Tensor 2D

Supongamos que tenemos un tensor de ingresos por región y categoría con forma `(num_regiones, num_categorias)`.

```python
# Simular ingresos por región y categoría
num_regiones = len(le_region.classes_)
num_categorias = len(le_categoria.classes_)
ingresos_region_categoria = torch.rand(num_regiones, num_categorias)

# Forma original
print(ingresos_region_categoria.shape)  # torch.Size([5, 5])

# Transponer el tensor
ingresos_categoria_region = ingresos_region_categoria.transpose(0, 1)
print(ingresos_categoria_region.shape)  # torch.Size([5, 5])
```

#### Ejemplo 4: Permutar Dimensiones en un Tensor 3D

Si tenemos un tensor 3D donde las dimensiones representan `(región, categoría, mes)`, podemos reorganizar las dimensiones.

```python
# Simular datos con dimensiones (región, categoría, mes)
num_meses = 12
datos_3d = torch.rand(num_regiones, num_categorias, num_meses)

# Forma original
print(datos_3d.shape)  # torch.Size([5, 5, 12])

# Permutar las dimensiones a (mes, región, categoría)
datos_permutados = datos_3d.permute(2, 0, 1)
print(datos_permutados.shape)  # torch.Size([12, 5, 5])
```

### 4.3.3 `unsqueeze()` y `squeeze()`

Estas funciones añaden o eliminan dimensiones de tamaño 1.

- **`unsqueeze(dim)`**: Añade una dimensión de tamaño 1 en la posición especificada.
- **`squeeze(dim)`**: Elimina dimensiones de tamaño 1; si se especifica `dim`, solo elimina esa dimensión si es de tamaño 1.

#### Ejemplo 5: Añadir una Dimensión a `precio_unitario`

```python
# Forma original
print(precio_unitario.shape)  # torch.Size([1000])

# Añadir una dimensión en la posición 1
precio_unitario_unsqueezed = precio_unitario.unsqueeze(1)
print(precio_unitario_unsqueezed.shape)  # torch.Size([1000, 1])
```

#### Ejemplo 6: Eliminar Dimensiones de Tamaño 1

Supongamos que tenemos un tensor con dimensiones innecesarias de tamaño 1.

```python
# Crear un tensor con dimensiones adicionales
tensor_extra_dims = torch.rand(1, 1000, 1)

# Forma original
print(tensor_extra_dims.shape)  # torch.Size([1, 1000, 1])

# Eliminar dimensiones de tamaño 1
tensor_squeezed = tensor_extra_dims.squeeze()
print(tensor_squeezed.shape)  # torch.Size([1000])
```

### 4.3.4 `expand()` y `repeat()`

Estas funciones permiten ampliar un tensor a una forma más grande sin copiar los datos (`expand`) o copiando los datos (`repeat`).

#### Ejemplo 7: Expandir un Tensor para Operaciones por Lotes

Supongamos que queremos restar el valor medio de `edad_cliente` a cada registro, pero tenemos los valores medios para diferentes grupos.

```python
# Calcular la edad media por género
media_edad_por_genero = torch.zeros(num_generos)
for i in range(num_generos):
    mask = (genero_cliente == i)
    media_edad_por_genero[i] = edad_cliente[mask].float().mean()

# Forma de media_edad_por_genero
print(media_edad_por_genero.shape)  # torch.Size([3])

# Expandir media_edad_por_genero para que coincida con edad_cliente
media_edad_expandidas = media_edad_por_genero.expand(num_records, num_generos)

# Necesitamos seleccionar la media correspondiente a cada registro
indices_genero = genero_cliente.long()
media_edad_registros = media_edad_por_genero[indices_genero]

# Restar la media correspondiente
edad_centrada = edad_cliente.float() - media_edad_registros
```

#### Ejemplo 8: Repetir un Tensor

Si queremos crear una matriz donde cada fila es el tensor `cantidad_vendida`, podemos repetirlo.

```python
# Repetir el tensor para crear una matriz
cantidad_vendida_repetida = cantidad_vendida.unsqueeze(1).repeat(1, 5)
print(cantidad_vendida_repetida.shape)  # torch.Size([1000, 5])
```

### 4.3.5 `flatten()`

Aplana un tensor comenzando desde una dimensión inicial hasta una dimensión final.

#### Ejemplo 9: Aplanar un Tensor 3D a 2D

Si tenemos un tensor de forma `(batch_size, channels, height, width)` y queremos aplanar las dimensiones espaciales.

```python
# Simular un tensor de imágenes
batch_size = 10
channels = 3
height = 32
width = 32
tensor_imagenes = torch.rand(batch_size, channels, height, width)

# Aplanar las dimensiones de height y width
tensor_flat = tensor_imagenes.flatten(start_dim=1)
print(tensor_flat.shape)  # torch.Size([10, 3072])
```

### 4.3.6 Ejercicios Prácticos con el Dataset

Ahora aplicaremos estas funciones en ejemplos prácticos utilizando nuestro dataset empresarial.

## 4.4 Ejemplos Prácticos con el Dataset Empresarial

### 4.4.1 Preparación de Datos para Modelos de Aprendizaje Automático

Supongamos que queremos preparar nuestros datos para entrenar un modelo que prediga el puntaje de satisfacción del cliente basado en las características disponibles.

#### Paso 1: Crear una Matriz de Características (`X`) y un Vector de Objetivos (`y`)

Incluiremos las siguientes características:

- `cantidad_vendida` (reshape a 2D)
- `precio_unitario` (reshape a 2D)
- `edad_cliente` (reshape a 2D)
- `producto_categoria` (one-hot encoding)
- `genero_cliente` (one-hot encoding)
- `region` (one-hot encoding)

```python
# Convertir características continuas a 2D
cantidad_vendida_2d = cantidad_vendida.float().unsqueeze(1)
precio_unitario_2d = precio_unitario.unsqueeze(1)
edad_cliente_2d = edad_cliente.float().unsqueeze(1)
```

#### Paso 2: Codificación One-Hot de Variables Categóricas

Utilizaremos `torch.nn.functional.one_hot` para codificar las variables categóricas.

```python
import torch.nn.functional as F

# Producto Categoria
producto_categoria_onehot = F.one_hot(producto_categoria, num_classes=num_categorias).float()

# Genero Cliente
genero_cliente_onehot = F.one_hot(genero_cliente, num_classes=num_generos).float()

# Region
region_onehot = F.one_hot(region, num_classes=num_regiones).float()
```

#### Paso 3: Concatenar Todas las Características

Usamos `torch.cat` para combinar todas las características en una matriz.

```python
# Lista de características
caracteristicas = [
    cantidad_vendida_2d,
    precio_unitario_2d,
    edad_cliente_2d,
    producto_categoria_onehot,
    genero_cliente_onehot,
    region_onehot
]

# Concatenar a lo largo de la dimensión 1
X = torch.cat(caracteristicas, dim=1)
print(X.shape)  # torch.Size([1000, número_total_de_características])
```

Calculamos el número total de características:

```python
número_total_de_características = (
    1 +  # cantidad_vendida
    1 +  # precio_unitario
    1 +  # edad_cliente
    num_categorias +  # producto_categoria_onehot
    num_generos +  # genero_cliente_onehot
    num_regiones  # region_onehot
)
print(número_total_de_características)  # Debería coincidir con X.shape[1]
```

#### Paso 4: Vector de Objetivos (`y`)

Nuestro vector objetivo es `puntaje_satisfaccion`, que necesitamos convertir a tipo float y reshape a 2D.

```python
y = puntaje_satisfaccion.float().unsqueeze(1)
```

### 4.4.2 Normalización de Características

Es común centrar y escalar las características antes de entrenar un modelo.

#### Cálculo de la Media y Desviación Estándar

```python
# Calcular la media y desviación estándar de las características continuas
media = X[:, :3].mean(dim=0)
desviacion_estandar = X[:, :3].std(dim=0)

# Normalizar las características continuas
X[:, :3] = (X[:, :3] - media) / desviacion_estandar
```

### 4.4.3 Cálculo del Producto Matriz-Vector para Predicciones

Supongamos que queremos calcular una predicción lineal simple:

\[
\hat{y} = Xw + b
\]

Donde:

- \( X \) es nuestra matriz de características.
- \( w \) es un vector de pesos.
- \( b \) es el sesgo (bias).

#### Inicializar los Pesos y el Sesgo

```python
# Inicializar pesos y sesgo aleatorios
torch.manual_seed(0)  # Para reproducibilidad
w = torch.rand(número_total_de_características, 1, requires_grad=True)
b = torch.rand(1, requires_grad=True)
```

#### Calcular las Predicciones

Usamos `torch.mm` para el producto matriz-matriz.

```python
# Producto matriz-matriz
y_pred = torch.mm(X, w) + b  # y_pred tendrá forma (1000, 1)
```

### 4.4.4 Cálculo de la Pérdida y Retropropagación

Calculamos la pérdida utilizando el error cuadrático medio y realizamos retropropagación.

```python
# Calcular la pérdida MSE
loss = ((y_pred - y) ** 2).mean()

# Retropropagación
loss.backward()

# Verificar los gradientes
print(w.grad.shape)  # torch.Size([número_total_de_características, 1])
print(b.grad.shape)  # torch.Size([1])
```

### 4.4.5 Actualización de los Pesos (Un Paso de Entrenamiento)

Usando una tasa de aprendizaje simple.

```python
# Definir la tasa de aprendizaje
learning_rate = 0.01

# Actualizar los pesos y el sesgo (sin un optimizador)
with torch.no_grad():
    w -= learning_rate * w.grad
    b -= learning_rate * b.grad

# Reiniciar los gradientes
w.grad.zero_()
b.grad.zero_()
```

### 4.4.6 Cálculo de la Matriz de Correlación

Queremos calcular la matriz de correlación entre las características continuas.

#### Paso 1: Seleccionar las Características Continuas

```python
# Extraer las características continuas normalizadas
X_continuas = X[:, :3]  # cantidad_vendida, precio_unitario, edad_cliente
```

#### Paso 2: Calcular la Matriz de Covarianza

```python
# Calcular la matriz de covarianza
covarianza = torch.mm(X_continuas.t(), X_continuas) / (X_continuas.shape[0] - 1)
```

#### Paso 3: Calcular la Matriz de Correlación

```python
# Obtener las desviaciones estándar de cada característica
desviaciones_estandar = X_continuas.std(dim=0)

# Calcular la matriz de correlación
correlacion = covarianza / (desviaciones_estandar.unsqueeze(1) * desviaciones_estandar)
```

#### Mostrar la Matriz de Correlación

```python
import pandas as pd

# Convertir a DataFrame para mejor visualización
caracteristicas_nombres = ['CantidadVendida', 'PrecioUnitario', 'EdadCliente']
df_correlacion = pd.DataFrame(correlacion.detach().numpy(), index=caracteristicas_nombres, columns=caracteristicas_nombres)

print(df_correlacion)
```

### 4.4.7 Análisis de Componentes Principales (PCA)

Podemos reducir la dimensionalidad de nuestras características utilizando PCA.

#### Paso 1: Calcular la Media y Restarla

```python
# Calcular la media de X
X_mean = X.mean(dim=0)

# Centrar los datos
X_centered = X - X_mean
```

#### Paso 2: Calcular la Matriz de Covarianza

```python
# Calcular la matriz de covarianza
covariance_matrix = torch.mm(X_centered.t(), X_centered) / (X_centered.shape[0] - 1)
```

#### Paso 3: Calcular los Autovalores y Autovectores

```python
# Calcular autovalores y autovectores
eigenvalues, eigenvectors = torch.eig(covariance_matrix, eigenvectors=True)
```

#### Nota Importante

La función `torch.eig` devuelve valores complejos, y dado que nuestra matriz de covarianza es simétrica y positiva definida, podemos utilizar `torch.symeig` para obtener autovalores y autovectores reales.

```python
eigenvalues, eigenvectors = torch.symeig(covariance_matrix, eigenvectors=True)
```

#### Paso 4: Proyectar los Datos en los Componentes Principales

Seleccionamos los primeros `k` autovectores para reducir la dimensionalidad.

```python
# Seleccionar los primeros k autovectores
k = 2
principal_components = eigenvectors[:, -k:]  # Tomamos los autovectores correspondientes a los mayores autovalores

# Proyectar los datos
X_reducido = torch.mm(X_centered, principal_components)
print(X_reducido.shape)  # torch.Size([1000, 2])
```

### 4.4.8 Uso de Tensores de Mayor Dimensión

Supongamos que queremos organizar nuestros datos en un tensor de 3 dimensiones, donde las dimensiones son `(batch_size, num_features, num_records_per_batch)`.

#### Paso 1: Definir el Tamaño del Lote

```python
batch_size = 10
num_records_per_batch = num_records // batch_size  # Debe ser un número entero
```

#### Paso 2: Reorganizar `X` en un Tensor 3D

```python
# Asegurarnos de que num_records es divisible por batch_size
num_records = batch_size * num_records_per_batch
X = X[:num_records]

# Reorganizar X
X_3d = X.view(batch_size, num_records_per_batch, -1)
print(X_3d.shape)  # torch.Size([10, 100, número_total_de_características])
```

#### Paso 3: Transponer Dimensiones si es Necesario

Si queremos que las dimensiones sean `(batch_size, num_features, num_records_per_batch)`.

```python
X_3d = X_3d.permute(0, 2, 1)
print(X_3d.shape)  # torch.Size([10, número_total_de_características, 100])
```

### 4.4.9 Cálculo de Productos Matriz-Matriz por Lotes

Supongamos que tenemos una matriz de pesos `W` para cada lote y queremos realizar un producto matriz-matriz para cada uno.

#### Paso 1: Crear una Matriz de Pesos para Cada Lote

```python
# Simular una matriz de pesos para cada lote
W = torch.rand(batch_size, número_total_de_características, número_total_de_características)
```

#### Paso 2: Realizar el Producto Matriz-Matriz por Lotes

Utilizamos `torch.bmm` para multiplicación de matrices por lotes.

```python
# Producto matriz-matriz por lotes
resultado = torch.bmm(W, X_3d)
print(resultado.shape)  # torch.Size([10, número_total_de_características, 100])
```

### 4.4.10 Uso de `einsum` para Operaciones Complejas

La función `torch.einsum` permite realizar operaciones matriciales complejas utilizando notación de Einstein.

#### Ejemplo: Cálculo de la Suma Ponderada de Características

Supongamos que queremos calcular una suma ponderada de las características para cada registro.

```python
# Simular un vector de pesos
pesos = torch.rand(número_total_de_características)

# Usar einsum para calcular la suma ponderada
suma_ponderada = torch.einsum('ij,j->i', X, pesos)
print(suma_ponderada.shape)  # torch.Size([1000])
```

## 4.5 Resumen de las Funciones de Forma en PyTorch

### Funciones Principales y sus Usos

- **`view(*shape)`**: Cambia la forma de un tensor sin alterar los datos.
- **`reshape(*shape)`**: Similar a `view`, pero puede devolver una copia si es necesario.
- **`transpose(dim0, dim1)`**: Intercambia dos dimensiones.
- **`permute(*dims)`**: Reorganiza todas las dimensiones.
- **`unsqueeze(dim)`**: Añade una dimensión de tamaño 1.
- **`squeeze(dim)`**: Elimina dimensiones de tamaño 1.
- **`expand(*sizes)`**: Expande un tensor para que parezca más grande sin copiar datos.
- **`repeat(*sizes)`**: Repite un tensor a lo largo de las dimensiones, copiando datos.
- **`flatten(start_dim, end_dim)`**: Aplana un tensor entre dos dimensiones.
- **`torch.mm(a, b)`**: Producto matriz-matriz.
- **`torch.mv(a, b)`**: Producto matriz-vector.
- **`torch.bmm(a, b)`**: Producto matriz-matriz por lotes.
- **`torch.einsum(equation, *operands)`**: Operaciones matriciales usando notación de Einstein.
  
## 4.6 Entendiendo el Broadcasting en PyTorch

### 4.6.1 ¿Qué es el Broadcasting?

El **broadcasting** es una técnica que permite realizar operaciones aritméticas en tensores de diferentes formas y tamaños sin necesidad de duplicar datos explícitamente. En esencia, PyTorch expande automáticamente los tensores más pequeños para que coincidan con las dimensiones de los tensores más grandes durante una operación, siguiendo reglas específicas.

El broadcasting es extremadamente útil porque simplifica el código y mejora la eficiencia al evitar la necesidad de expandir manualmente los tensores. Sin embargo, es importante entender cómo funciona para evitar errores sutiles y asegurar que las operaciones se realizan según lo esperado.

### 4.6.2 Reglas del Broadcasting

Las reglas de broadcasting en PyTorch son similares a las de NumPy y son las siguientes:

1. **Si los tensores no tienen el mismo número de dimensiones**, se agregan dimensiones de tamaño 1 al principio del tensor con menos dimensiones hasta que ambos tensores tengan el mismo número de dimensiones.

2. **Para cada dimensión**, los tamaños de los tensores deben ser iguales, o uno de ellos debe ser 1. En este último caso, el tensor con tamaño 1 en esa dimensión se "estira" o "repite" para coincidir con el tamaño del otro tensor en esa dimensión.

3. **Si en alguna dimensión los tamaños son diferentes y ninguno es 1**, PyTorch lanzará un error, ya que no puede aplicar el broadcasting.

### 4.6.3 Ejemplos de Broadcasting

#### Ejemplo 1: Sumar un Escalar a un Tensor

Esta es la forma más básica de broadcasting. Si sumamos un escalar (un tensor de cero dimensiones) a un tensor de cualquier forma, el escalar se expande para que coincida con la forma del tensor.

- **Situación:** Tenemos un tensor `a` de forma `(3, 4)` y un escalar `b`.
- **Operación:** `c = a + b`
- **Broadcasting:** El escalar `b` se expande para que su forma sea `(3, 4)`.

#### Ejemplo 2: Sumar un Vector a una Matriz

- **Situación:** Tensor `a` de forma `(3, 4)` y vector `b` de forma `(4,)`.
- **Operación:** `c = a + b`
- **Broadcasting:**
  - Se agrega una dimensión al principio de `b` para obtener `(1, 4)`.
  - `b` se expande a `(3, 4)` al repetir sus valores a lo largo de la nueva dimensión.

#### Ejemplo 3: Multiplicar Tensores con Dimensiones Compatibles

- **Situación:** Tensor `a` de forma `(5, 1, 4)` y tensor `b` de forma `(1, 3, 1)`.
- **Operación:** `c = a * b`
- **Broadcasting:**
  - `a` se expande a `(5, 3, 4)`.
  - `b` se expande a `(5, 3, 4)`.
  - La operación se realiza elemento a elemento en el tensor resultante de forma `(5, 3, 4)`.

#### Ejemplo 4: Error de Broadcasting

- **Situación:** Tensor `a` de forma `(2, 3)` y tensor `b` de forma `(2, 2)`.
- **Operación:** `c = a + b`
- **Broadcasting:**
  - Las dimensiones no son compatibles en la segunda dimensión (3 y 2), y ninguno de los tamaños es 1.
  - **Resultado:** PyTorch lanzará un error.

### 4.6.4 Aplicaciones del Broadcasting en el Dataset Empresarial

Utilizaremos nuestro dataset empresarial para ilustrar cómo el broadcasting facilita operaciones comunes.

#### Ejemplo 5: Restar la Media de Cada Característica

Queremos centrar nuestras características continuas (`cantidad_vendida`, `precio_unitario`, `edad_cliente`) restando la media de cada una.

- **Paso 1:** Calcular la media de cada característica.

  ```python
  medias = X[:, :3].mean(dim=0)  # Forma: (3,)
  ```

- **Paso 2:** Restar las medias al tensor `X`.

  ```python
  X[:, :3] = X[:, :3] - medias  # Broadcasting de medias de forma (3,) a (num_records, 3)
  ```

- **Broadcasting:**
  - `medias` se expande de `(3,)` a `(num_records, 3)` para que coincida con `X[:, :3]`.

#### Ejemplo 6: Multiplicar Cada Característica por un Peso

Supongamos que tenemos un vector de pesos para cada característica y queremos multiplicar cada registro por estos pesos.

- **Paso 1:** Definir el vector de pesos.

  ```python
  pesos = torch.tensor([0.5, 1.5, -1.0])  # Forma: (3,)
  ```

- **Paso 2:** Multiplicar las características por los pesos.

  ```python
  X[:, :3] = X[:, :3] * pesos  # Broadcasting de pesos de forma (3,) a (num_records, 3)
  ```

- **Broadcasting:**
  - `pesos` se expande de `(3,)` a `(num_records, 3)`.

#### Ejemplo 7: Calcular el Ingreso Total Ajustado por Región

Queremos ajustar los ingresos totales por un factor específico para cada región.

- **Paso 1:** Definir los factores de ajuste por región.

  ```python
  factores_region = torch.tensor([1.0, 0.9, 1.1, 0.95, 1.05])  # Forma: (5,)
  ```

- **Paso 2:** Crear una máscara para cada registro que indique su región.

  ```python
  indices_region = region.long()  # Asumiendo que 'region' tiene valores de 0 a 4
  factores_ajuste = factores_region[indices_region]  # Forma: (num_records,)
  ```

- **Paso 3:** Ajustar los ingresos totales.

  ```python
  ingresos_ajustados = ingresos_totales * factores_ajuste  # Broadcasting automático
  ```

- **Broadcasting:**
  - `factores_ajuste` y `ingresos_totales` son de forma `(num_records,)`, no se requiere broadcasting adicional.

### 4.6.5 Consideraciones Importantes

#### Entender las Dimensiones

Es crucial comprender las dimensiones de los tensores involucrados en una operación para predecir cómo se aplicará el broadcasting.

- **Consejo:** Siempre imprime las formas de tus tensores antes de las operaciones para verificar su compatibilidad.

#### Evitar Errores Silenciosos

Aunque el broadcasting es conveniente, puede llevar a errores sutiles si las dimensiones no son las esperadas.

- **Ejemplo:** Si accidentalmente tienes un tensor de forma `(num_records, 1)` en lugar de `(num_records,)`, el broadcasting puede comportarse de manera diferente.

#### Uso de `unsqueeze` para Ajustar Formas

Puedes utilizar `unsqueeze` para agregar dimensiones de tamaño 1 y controlar cómo se aplica el broadcasting.

- **Ejemplo:** Si necesitas sumar un vector columna a cada columna de una matriz.

  ```python
  vector_columna = torch.rand(num_features, 1)
  matriz = torch.rand(num_records, num_features)
  resultado = matriz + vector_columna.t()  # Transponer para ajustar las dimensiones
  ```

### 4.6.6 Visualización del Broadcasting

Para visualizar cómo se expanden los tensores durante el broadcasting, puedes pensar en repetir los elementos a lo largo de las dimensiones necesarias.

- **Ejemplo Visual:**

  - Tensor `a` de forma `(2, 3)`:
  
    ```
    [[a11, a12, a13],
     [a21, a22, a23]]
    ```

  - Tensor `b` de forma `(3,)` se expande a `(2, 3)`:

    ```
    [[b1, b2, b3],
     [b1, b2, b3]]
    ```

  - Operación `a + b` se realiza elemento a elemento.

### 4.6.7 Prácticas Recomendadas

#### Verificar la Compatibilidad de Dimensiones

Antes de realizar operaciones, asegúrate de que las dimensiones sean compatibles según las reglas de broadcasting.

#### Utilizar Operaciones Específicas

Cuando sea posible, utiliza funciones específicas que manejan las dimensiones internamente, como `torch.matmul` para multiplicaciones matriciales.

#### Controlar el Broadcasting

Si deseas evitar el broadcasting o hacerlo explícito, ajusta las formas de los tensores usando `unsqueeze`, `view` o `reshape`.

### 4.6.8 Ejercicios de Autoevaluación

#### Ejercicio 1: Sumar Matrices de Diferentes Formas

- **Situación:** Tensor `a` de forma `(4, 1)` y tensor `b` de forma `(1, 5)`.
- **Pregunta:** ¿Cuál será la forma del resultado de `a + b`?

  **Respuesta:**
  
  - `a` se expande a `(4, 5)`.
  - `b` se expande a `(4, 5)`.
  - Resultado: Tensor de forma `(4, 5)`.

#### Ejercicio 2: Multiplicar Tensores Incompatibles

- **Situación:** Tensor `a` de forma `(3, 2)` y tensor `b` de forma `(2, 3)`.
- **Pregunta:** ¿Por qué `a + b` genera un error?

  **Respuesta:**
  
  - Las dimensiones no son compatibles para el broadcasting, ya que en ninguna dimensión los tamaños son iguales o uno es 1.

#### Ejercicio 3: Uso de `unsqueeze` para Broadcasting

- **Situación:** Tensor `a` de forma `(100, 10)` y tensor `b` de forma `(10,)`.
- **Pregunta:** ¿Cómo puedes ajustar `b` para que se sume correctamente a cada fila de `a`?

  **Respuesta:**
  
  - Utilizar `b = b.unsqueeze(0)` para obtener forma `(1, 10)`.
  - El broadcasting expandirá `b` a `(100, 10)`.

### 4.6.9 Conexión con Otras Operaciones

El broadcasting está estrechamente relacionado con las funciones `squeeze`, `unsqueeze`, `reshape` y `expand`. Estas funciones te permiten preparar los tensores para que el broadcasting se realice según tus necesidades.

- **`unsqueeze`:** Añade dimensiones de tamaño 1 para habilitar el broadcasting en dimensiones específicas.
- **`expand`:** Expande un tensor de tamaño 1 en una dimensión a un tamaño mayor sin copiar datos, útil para el broadcasting.
- **`reshape` y `view`:** Ajustan las formas de los tensores para que sean compatibles en operaciones.

### 4.6.10 Resumen

El broadcasting es una característica poderosa de PyTorch que simplifica las operaciones entre tensores de diferentes formas. Al entender y aplicar las reglas de broadcasting, puedes escribir código más conciso y eficiente.

Es importante ser consciente de cómo PyTorch aplica el broadcasting para evitar errores y asegurarse de que las operaciones se realicen como se espera. Utiliza las funciones de manipulación de forma para controlar el broadcasting y adaptar tus tensores a las necesidades de tus cálculos.


## 4.7 Ejemplos Adicionales para Comprender `squeeze`, `unsqueeze`, `flatten` y `reshape`

En esta sección, profundizaremos en las funciones `squeeze`, `unsqueeze`, `flatten` y `reshape` de PyTorch mediante una serie de ejemplos detallados. El objetivo es brindar una comprensión más intuitiva de cómo y cuándo utilizar estas funciones al manipular tensores.

### 4.7.1 Comprendiendo `unsqueeze`

La función `unsqueeze(dim)` se utiliza para **añadir una nueva dimensión de tamaño 1** en la posición especificada. Esto es útil cuando necesitamos ajustar la forma de un tensor para operaciones que requieren una determinada dimensionalidad.

#### Ejemplo 1: Preparación de Datos para Operaciones de Broadcast

Supongamos que tenemos un tensor de características de tamaño `(1000, 10)` y un tensor de pesos de tamaño `(10,)`. Queremos multiplicar cada característica por su peso correspondiente para cada uno de los 1000 ejemplos.

- **Situación:** El tensor de pesos tiene una dimensión menos que el tensor de características.
- **Solución con `unsqueeze`:** Añadimos una dimensión al tensor de pesos para que su forma sea `(1, 10)`. Esto permite que la operación de multiplicación se realice correctamente a través del broadcast.

#### Ejemplo 2: Agregar una Dimensión para Operaciones de Reducción

Cuando utilizamos funciones de reducción como `mean` o `sum`, a veces queremos mantener la dimensión reducida para mantener la consistencia en la forma del tensor.

- **Situación:** Después de calcular la media a lo largo de una dimensión, obtenemos un tensor de menor dimensionalidad.
- **Solución con `unsqueeze`:** Podemos utilizar `unsqueeze` para reintroducir la dimensión reducida, facilitando operaciones posteriores que requieren esa dimensión.

#### Ejemplo 3: Preparación de Imágenes para Modelos

En visión por computadora, las imágenes suelen tener la forma `(altura, anchura, canales)`. Los modelos de aprendizaje profundo generalmente esperan la forma `(batch_size, canales, altura, anchura)`.

- **Situación:** Tenemos una imagen individual de forma `(256, 256, 3)`.
- **Solución con `unsqueeze`:** Añadimos una dimensión al inicio para representar el tamaño del lote (batch size), obteniendo `(1, 256, 256, 3)`. Posteriormente, podemos permutar las dimensiones según sea necesario.

### 4.7.2 Comprendiendo `squeeze`

La función `squeeze(dim)` elimina dimensiones de tamaño 1 del tensor. Esto es útil para simplificar la forma de los tensores después de operaciones que introducen dimensiones adicionales innecesarias.

#### Ejemplo 4: Eliminación de Dimensiones Innecesarias

Después de una operación que devuelve un tensor con dimensiones de tamaño 1, queremos simplificar el tensor.

- **Situación:** Obtenemos un tensor con forma `(1, 1000, 1)`.
- **Solución con `squeeze`:** Aplicamos `squeeze` para eliminar las dimensiones de tamaño 1, obteniendo un tensor de forma `(1000)`.

#### Ejemplo 5: Extracción de Resultados Escalares

Al calcular la pérdida total en un modelo, el resultado es un tensor de tamaño `(1,)`. Para obtener un valor escalar que podamos imprimir o registrar, necesitamos eliminar la dimensión adicional.

- **Situación:** Pérdida calculada con forma `(1,)`.
- **Solución con `squeeze`:** Aplicamos `squeeze` para obtener un escalar.

### 4.7.3 Comprendiendo `flatten`

La función `flatten(start_dim, end_dim)` aplana (convierte en una sola dimensión) las dimensiones desde `start_dim` hasta `end_dim`. Es especialmente útil al preparar datos para capas totalmente conectadas en redes neuronales.

#### Ejemplo 6: Aplanamiento de Imágenes para Redes Neuronales

En redes neuronales, es común aplanar las características espaciales de una imagen antes de pasarlas a una capa totalmente conectada.

- **Situación:** Tenemos un lote de imágenes con forma `(batch_size, canales, altura, anchura)`, por ejemplo, `(32, 3, 28, 28)`.
- **Solución con `flatten`:** Aplicamos `flatten` desde la dimensión 1 en adelante para obtener un tensor de forma `(32, 2352)`, donde `2352 = 3 * 28 * 28`.

#### Ejemplo 7: Aplanamiento Selectivo de Dimensiones

Si tenemos datos de series temporales con forma `(batch_size, sequence_length, features)`, y queremos combinar el `sequence_length` y `features` en una sola dimensión.

- **Situación:** Tensor de forma `(64, 10, 50)`.
- **Solución con `flatten`:** Aplicamos `flatten` desde la dimensión 1 hasta la 2, obteniendo `(64, 500)`.

### 4.7.4 Comprendiendo `reshape`

La función `reshape(*shape)` cambia la forma de un tensor a la especificada, siempre que el número total de elementos permanezca igual. Es una herramienta versátil para reorganizar los datos.

#### Ejemplo 8: Reorganización de Datos para Modelos Recurrentes

Supongamos que tenemos un lote de secuencias concatenadas y queremos separarlas.

- **Situación:** Tensor de forma `(batch_size * sequence_length, features)`, por ejemplo, `(320, 50)`, donde `batch_size = 32` y `sequence_length = 10`.
- **Solución con `reshape`:** Cambiamos la forma a `(32, 10, 50)` para obtener el lote y las secuencias separadas.

#### Ejemplo 9: Preparación de Datos para Operaciones Matriciales

Si necesitamos preparar matrices para operaciones de multiplicación, podemos reorganizar los tensores.

- **Situación:** Dos tensores de forma `(batch_size, features1, features2)` y necesitamos multiplicarlos a lo largo de ciertas dimensiones.
- **Solución con `reshape`:** Ajustamos las formas para que las dimensiones sean compatibles para la operación.

### 4.7.5 Ejemplos Comparativos

#### Ejemplo 10: Diferencia entre `view` y `reshape`

Aunque `view` y `reshape` pueden parecer similares, hay diferencias en cómo manejan la memoria.

- **`view`:** Requiere que el tensor sea contiguo en memoria. Si no lo es, debemos llamar a `contiguous()` antes.
- **`reshape`:** Puede devolver un tensor que no es una vista del original, es más flexible pero puede implicar copias de datos.

**Situación:** Tenemos un tensor transpuesto que no es contiguo.

- **Solución con `view`:** No podemos usar `view` directamente, necesitamos llamar a `contiguous()` primero.
- **Solución con `reshape`:** Podemos usar `reshape` directamente, pero debemos ser conscientes de que puede crear una copia.

### 4.7.6 Visualización Conceptual

Para entender mejor estas funciones, es útil visualizarlas con analogías.

- **`unsqueeze`:** Imagínate que tienes una fila de elementos y quieres convertirla en una columna; estás añadiendo una nueva dimensión para acomodar la estructura.
- **`squeeze`:** Tienes una caja con una sola fila o columna vacía; la eliminas para simplificar.
- **`flatten`:** Aplanas una caja multidimensional en una sola fila larga; estás combinando dimensiones.
- **`reshape`:** Reorganizas los elementos en una nueva estructura sin cambiar la cantidad total; como reorganizar libros en estantes de diferente tamaño.

### 4.7.7 Aplicaciones Prácticas en el Dataset Empresarial

#### Ejemplo 11: Aplanar Datos para Análisis Estadístico

Queremos analizar todos los ingresos totales como una sola lista sin importar su agrupación original.

- **Situación:** `ingresos_totales` está organizado por regiones y categorías en un tensor 2D de forma `(num_regiones, num_categorias)`.
- **Solución con `flatten`:** Aplanamos el tensor a una dimensión `(num_regiones * num_categorias)` para calcular estadísticas globales.

#### Ejemplo 12: Añadir una Dimensión para Compatibilidad en Operaciones

Necesitamos restar un vector de medias de cada fila de una matriz de datos.

- **Situación:** Matriz de datos de forma `(1000, 10)` y vector de medias de forma `(10,)`.
- **Solución con `unsqueeze`:** Añadimos una dimensión al vector de medias para obtener `(1, 10)` y permitir la operación de resta con broadcast.

#### Ejemplo 13: Eliminar Dimensiones Después de Operaciones de Agregación

Tras sumar los ingresos a lo largo de todas las regiones y categorías, obtenemos un tensor de forma `(1, 1)`.

- **Situación:** Resultado con dimensiones innecesarias.
- **Solución con `squeeze`:** Eliminamos las dimensiones de tamaño 1 para obtener un escalar.

#### Ejemplo 14: Reorganización de Datos para Visualización

Queremos visualizar los ingresos mensuales en una cuadrícula de meses por regiones.

- **Situación:** Tensor de ingresos con forma `(num_meses * num_regiones,)`.
- **Solución con `reshape`:** Cambiamos la forma a `(num_meses, num_regiones)` para facilitar la creación de un mapa de calor.

### 4.7.8 Resumen de Casos de Uso

- **Cuando usar `unsqueeze`:** Al preparar datos para modelos que requieren una dimensión adicional, o para ajustar las formas de tensores para operaciones de broadcast.
- **Cuando usar `squeeze`:** Después de operaciones que resultan en dimensiones de tamaño 1 que no son necesarias, para simplificar la forma del tensor.
- **Cuando usar `flatten`:** Al convertir datos multidimensionales en una sola dimensión, comúnmente antes de capas totalmente conectadas en redes neuronales.
- **Cuando usar `reshape`:** Al reorganizar los datos para cambiar su estructura, siempre que el número total de elementos permanezca igual.

### 4.7.9 Preguntas de Autoevaluación

Para reforzar la comprensión, considera las siguientes preguntas:

1. **¿Qué ocurre si aplicas `squeeze` a un tensor que no tiene dimensiones de tamaño 1?**

   No se producirá ningún cambio en la forma del tensor, ya que `squeeze` solo elimina dimensiones de tamaño 1.

2. **¿Puedes utilizar `unsqueeze` para cambiar un tensor de forma `(1000,)` a `(1000, 1, 1)`?**

   Sí, aplicando `unsqueeze` dos veces en las dimensiones 1 y 2.

3. **Si tienes un tensor de forma `(32, 3, 28, 28)`, ¿cómo lo aplanarías para prepararlo para una capa totalmente conectada?**

   Utilizando `flatten` desde la dimensión 1 en adelante para obtener `(32, 2352)`.

4. **¿Es posible cambiar la forma de un tensor de `(2, 3, 4)` a `(8, 3)` utilizando `reshape`?**

   No, porque el número total de elementos debe permanecer igual. `2 * 3 * 4 = 24`, pero `8 * 3 = 24`, así que es posible.

### 4.7.10 Buenas Prácticas

- **Verificar las Formas:** Siempre comprueba las formas de tus tensores antes y después de aplicar transformaciones para asegurarte de que son las esperadas.
- **Entender el Broadcast:** Al manipular dimensiones, es importante comprender cómo funciona el broadcast en PyTorch para evitar errores en las operaciones.
- **Mantener la Contigüidad:** Algunas operaciones requieren que los tensores sean contiguos en memoria. Si encuentras errores, considera usar `contiguous()` antes de `view`.

## 4.8 Conclusión 

Las funciones `squeeze`, `unsqueeze`, `flatten` y `reshape` son herramientas esenciales en PyTorch para la manipulación de tensores. A través de numerosos ejemplos, hemos explorado cómo estas funciones permiten ajustar las formas de los datos para adaptarse a diferentes necesidades, ya sea para operaciones matemáticas, preparación de datos para modelos o simplificación de resultados.

Una comprensión profunda de estas funciones facilita el trabajo eficiente con tensores y ayuda a evitar errores comunes relacionados con incompatibilidades de formas. A medida que avances en el uso de PyTorch y construyas modelos más complejos, estas habilidades serán cada vez más valiosas.

Recuerda que la práctica es clave. Experimenta con diferentes tensores y operaciones para solidificar tu comprensión y ganar confianza en la manipulación de datos en PyTorch.