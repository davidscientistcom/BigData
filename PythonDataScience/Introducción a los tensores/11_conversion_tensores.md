## 1. Transformación de Datos en Tensores

### 1.1 Datos Numéricos y Escalado

#### 1.1.1 Tensores Directos con PyTorch

Los datos numéricos suelen ser más fáciles de convertir directamente en tensores. En muchos casos, solo es necesario aplicar `torch.tensor()` sobre los datos en forma de listas o matrices de `NumPy`.

```python
import torch

# Ejemplo: datos numéricos en una lista
data = [1.0, 2.5, 3.1, 4.8]
tensor = torch.tensor(data)
print("Tensor a partir de lista numérica:\n", tensor)
```

#### 1.1.2 Transformación desde `NumPy` a Tensores

La función `torch.from_numpy()` convierte directamente un arreglo de `NumPy` en un tensor, lo cual es útil en ciencia de datos.

```python
import numpy as np

# Datos como arreglo NumPy
data_np = np.array([1.0, 2.5, 3.1, 4.8])
tensor_from_np = torch.from_numpy(data_np)
print("Tensor a partir de NumPy:\n", tensor_from_np)
```

#### 1.1.3 Escalado y Normalización

En muchas aplicaciones, es útil **escalar o normalizar los datos** para que estén en un rango específico, como entre 0 y 1 o con una media de 0 y desviación estándar de 1. Scikit-learn ofrece `StandardScaler` y `MinMaxScaler` para este propósito.

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Datos sin escalar
data = np.array([[1.0], [2.5], [3.1], [4.8]])

# Escalado usando StandardScaler (media = 0, desviación estándar = 1)
scaler = StandardScaler()
data_standardized = scaler.fit_transform(data)
tensor_standardized = torch.tensor(data_standardized)
print("Tensor con datos estandarizados:\n", tensor_standardized)

# Escalado usando MinMaxScaler (rango = [0, 1])
scaler_minmax = MinMaxScaler()
data_minmax_scaled = scaler_minmax.fit_transform(data)
tensor_minmax = torch.tensor(data_minmax_scaled)
print("Tensor con datos escalados en rango [0, 1]:\n", tensor_minmax)
```

### 1.2 Transformación de Variables Categóricas

Las variables categóricas suelen necesitar una codificación especial antes de ser utilizadas en modelos de aprendizaje profundo.

#### 1.2.1 Codificación One-Hot

La codificación **one-hot** convierte cada categoría en un vector binario. En Scikit-learn, podemos usar `OneHotEncoder` para esto, y luego convertir el resultado en un tensor.

```python
from sklearn.preprocessing import OneHotEncoder

# Ejemplo de variables categóricas
categories = np.array([['rojo'], ['azul'], ['verde'], ['azul']])

# Codificación One-Hot
encoder = OneHotEncoder(sparse=False)
encoded_data = encoder.fit_transform(categories)
tensor_one_hot = torch.tensor(encoded_data)
print("Tensor con codificación One-Hot:\n", tensor_one_hot)
```

#### 1.2.2 Codificación Ordinal

Para datos categóricos con un orden natural (como "bajo", "medio", "alto"), podemos usar **codificación ordinal**, asignando un número a cada categoría. En Scikit-learn, se puede hacer con `OrdinalEncoder`.

```python
from sklearn.preprocessing import OrdinalEncoder

# Ejemplo de categorías con orden
levels = np.array([['bajo'], ['medio'], ['alto'], ['medio']])

# Codificación Ordinal
ordinal_encoder = OrdinalEncoder()
encoded_levels = ordinal_encoder.fit_transform(levels)
tensor_ordinal = torch.tensor(encoded_levels)
print("Tensor con codificación ordinal:\n", tensor_ordinal)
```

### 1.3 Imágenes

Para trabajar con imágenes, PyTorch ofrece herramientas específicas para cargarlas y convertirlas en tensores.

#### 1.3.1 Transformación Directa usando `torchvision`

En PyTorch, el módulo `torchvision.transforms` proporciona varias transformaciones para imágenes, incluyendo la conversión a tensores.

```python
from PIL import Image
from torchvision import transforms

# Cargar una imagen y convertirla a escala de grises
img = Image.open("ruta_de_imagen.jpg").convert("L")  # Convertir a escala de grises

# Transformación a tensor
transform = transforms.ToTensor()
img_tensor = transform(img)
print("Tensor de imagen:\n", img_tensor.shape)
```

### 1.4 Texto

El texto necesita transformarse en números (tokens) antes de ser procesado. `TorchText` facilita este tipo de transformación.

#### 1.4.1 Tokenización y Codificación

Las palabras pueden convertirse en tokens, y estos en vectores. Para este propósito, se puede usar una **codificación de palabras** (Word Embeddings).

```python
# Ejemplo simple de tokenización en texto
from collections import Counter
from torchtext.vocab import Vocab

# Tokenizar una oración
sentence = "Me gusta aprender sobre redes neuronales"
tokens = sentence.lower().split()

# Crear vocabulario a partir de tokens
counter = Counter(tokens)
vocab = Vocab(counter, specials=['<unk>', '<pad>'])

# Convertir tokens en índices de vocabulario
indices = [vocab[token] for token in tokens]
tensor_text = torch.tensor(indices)
print("Tensor con índices de vocabulario:\n", tensor_text)
```

---

## 2. Transformación de Tensores en Datos

Al final del proceso, es común tener que transformar los tensores en formatos entendibles para humanos, especialmente para ver resultados de predicción, clasificaciones, o imágenes procesadas.

### 2.1 Transformación de Tensores a `NumPy`

Si necesitamos manipular o analizar los datos en `NumPy` después del procesamiento en PyTorch, podemos usar `.numpy()`.

```python
# Tensor a convertir
tensor_data = torch.tensor([1.0, 2.5, 3.1, 4.8])

# Conversión a NumPy
data_np = tensor_data.numpy()
print("Datos como arreglo NumPy:\n", data_np)
```

### 2.2 Transformación de Tensores a Datos Categóricos

Si tenemos datos categóricos codificados, como con One-Hot o índices ordinales, podemos revertir la transformación a etiquetas originales usando los encoders de Scikit-learn.

#### 2.2.1 Revertir Codificación One-Hot

```python
# Convertir de tensor a NumPy para decodificación
one_hot_tensor = torch.tensor([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
one_hot_np = one_hot_tensor.numpy()

# Revertir codificación One-Hot
decoded_categories = encoder.inverse_transform(one_hot_np)
print("Categorías originales:\n", decoded_categories)
```

#### 2.2.2 Revertir Codificación Ordinal

```python
# Convertir de tensor a NumPy para decodificación
ordinal_tensor = torch.tensor([0, 1, 2, 1])
ordinal_np = ordinal_tensor.numpy().reshape(-1, 1)

# Revertir codificación ordinal
decoded_levels = ordinal_encoder.inverse_transform(ordinal_np)
print("Categorías ordinales originales:\n", decoded_levels)
```

### 2.3 Visualización de Imágenes desde Tensores

Para visualizar imágenes, podemos usar `matplotlib` después de convertir el tensor en formato NumPy.

```python
import matplotlib.pyplot as plt

# Convertir tensor a NumPy y visualizar
img_np = img_tensor.numpy().squeeze()
plt.imshow(img_np, cmap="gray")
plt.title("Imagen desde tensor")
plt.show()
```

### 2.4 Decodificación de Texto

Para decodificar texto desde tensores de índices de vocabulario, revertimos la transformación original con el vocabulario.

```python
# Tensor con índices de palabras
tensor_text = torch.tensor([1, 2, 3, 4, 1])

# Revertir a palabras usando el vocabulario
tokens_decoded = [vocab.itos[idx] for idx in tensor_text]
decoded_sentence = " ".join(tokens_decoded)
print("Texto original decodificado:\n", decoded_sentence)
```

---

### Resumen de Métodos de Transformación

| Tipo de Datos           | Transformación a Tensor                                 | Ejemplo                               |
|-------------------------|---------------------------------------------------------|---------------------------------------|
| Numérico                | `torch.tensor(data)`, `torch.from_numpy(data)`           | Listas, NumPy arrays                  |
| Escalado               

 | `StandardScaler` y `MinMaxScaler` de Scikit-learn        | Normalización entre 0 y 1             |
| Categórico - One-Hot    | `OneHotEncoder` de Scikit-learn                          | Variables categóricas                 |
| Categórico - Ordinal    | `OrdinalEncoder` de Scikit-learn                         | Niveles ordenados                     |
| Imagen                  | `torchvision.transforms.ToTensor()`                      | Imágenes JPG, PNG                     |
| Texto                   | `Vocab`, tokenización                                   | Transformación de texto               |
| Transformación Inversa  | `.numpy()`, decodificación de Scikit-learn y vocabulario | Tensores a datos interpretables       |
