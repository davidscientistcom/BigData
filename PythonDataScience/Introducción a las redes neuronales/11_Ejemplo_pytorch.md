# APUNTES: Redes Neuronales en PyTorch para Clasificación

## Introducción

Estos apuntes están diseñados para estudiantes que conocen la teoría básica de redes neuronales pero van a implementar su primera red en PyTorch. El objetivo es construir un modelo de clasificación binaria desde cero, entendiendo cada decisión técnica y cada línea de código. Vamos a seguir un proceso iterativo: empezaremos con modelos simples que fallan y los iremos mejorando hasta conseguir un modelo que funcione correctamente. Este enfoque refleja el proceso real de desarrollo en machine learning.

## Capítulo 1: Preparación del Entorno y Datos

### 1.1 ¿Qué es un Tensor?

Antes de empezar a construir redes neuronales, necesitamos entender qué es un tensor, porque es la estructura de datos fundamental en PyTorch. Un tensor es esencialmente un array multidimensional, similar a los arrays de NumPy, pero con dos ventajas cruciales: primero, PyTorch puede calcular automáticamente las derivadas de cualquier operación que hagamos con tensores (esto es fundamental para el entrenamiento), y segundo, los tensores pueden ejecutarse en GPU para acelerar los cálculos dramáticamente.

Cuando trabajamos con redes neuronales, todos nuestros datos (imágenes, texto, números) se representan como tensores. Por ejemplo, una imagen en color de 224x224 píxeles se representa como un tensor de forma (3, 224, 224), donde 3 representa los canales RGB. En nuestro caso, vamos a trabajar con datos más simples: puntos en un plano 2D, que se representarán como tensores de forma (número_de_muestras, 2).

### 1.2 Importando las Librerías Necesarias

Vamos a empezar importando todas las librerías que vamos a necesitar a lo largo de estos apuntes:

```python
import torch
import torch.nn as nn
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
```

La librería `torch` es el núcleo de PyTorch. El módulo `torch.nn` contiene todas las herramientas para construir redes neuronales: capas, funciones de activación, funciones de pérdida, etc. Usaremos scikit-learn para generar datos sintéticos y dividirlos en conjuntos de entrenamiento y test. Matplotlib nos servirá para visualizar nuestros datos y resultados.

### 1.3 Generación de Datos: El Problema de los Círculos Concéntricos

Para este tutorial vamos a usar un problema de clasificación binaria específico: clasificar puntos que pertenecen a dos círculos concéntricos. Este problema es perfecto para demostrar por qué las redes neuronales necesitan no-linealidades. Vamos a generar los datos usando la función `make_circles` de scikit-learn:

```python
torch.manual_seed(42)
torch.cuda.manual_seed(42)

n_samples = 1000
X, y = make_circles(n_samples=n_samples, noise=0.03, random_state=42)
```

Aquí hay varios detalles importantes que debemos entender. Primero, establecemos las semillas aleatorias usando `torch.manual_seed(42)` y `torch.cuda.manual_seed(42)`. ¿Por qué hacemos esto? Cuando entrenamos redes neuronales, hay muchos procesos aleatorios involucrados: la inicialización de los pesos, la selección de mini-batches, etc. Si no fijamos la semilla, cada vez que ejecutemos nuestro código obtendremos resultados ligeramente diferentes. Esto dificulta la reproducibilidad y el debugging. Al fijar la semilla en 42 (el número es arbitrario, puede ser cualquiera), garantizamos que nuestros resultados sean reproducibles.

La función `make_circles` genera 1000 puntos en 2D distribuidos en dos círculos concéntricos. El parámetro `noise=0.03` añade un pequeño ruido gaussiano a los puntos. Esto es importante porque en el mundo real los datos nunca son perfectos; siempre hay ruido. Entrenar con datos ruidosos hace que nuestro modelo sea más robusto. El `random_state=42` es similar al manual_seed: garantiza que scikit-learn genere siempre los mismos datos aleatorios.

El objeto `X` contiene las coordenadas (x, y) de cada punto, y el objeto `y` contiene las etiquetas: 0 para puntos del círculo interior, 1 para puntos del círculo exterior.

### 1.4 Conversión a Tensores de PyTorch

Los datos generados por scikit-learn están en formato NumPy array. Necesitamos convertirlos a tensores de PyTorch:

```python
X = torch.from_numpy(X).type(torch.float32)
y = torch.from_numpy(y).type(torch.float32)
```

La función `torch.from_numpy()` convierte un array de NumPy en un tensor de PyTorch. Pero hay un detalle crucial: usamos `.type(torch.float32)` para asegurar que los tensores sean de tipo float32. ¿Por qué es importante esto? PyTorch, por defecto, hace todos los cálculos de redes neuronales en precisión float32. Si nuestros datos están en otro formato (como int64 o float64), PyTorch dará errores o los convertirá automáticamente, lo cual puede causar problemas sutiles. Es una buena práctica siempre convertir explícitamente nuestros datos a float32.

Es importante notar que `X` tiene forma (1000, 2), es decir, 1000 muestras con 2 características cada una (las coordenadas x e y). El tensor `y` tiene forma (1000,), es decir, 1000 etiquetas, una por cada muestra.

### 1.5 División en Conjunto de Entrenamiento y Test

En machine learning, nunca evaluamos nuestro modelo con los mismos datos con los que entrenó. Si lo hiciéramos, no sabríamos si el modelo realmente aprendió patrones generalizables o simplemente memorizó los datos de entrenamiento. Por eso dividimos nuestros datos en dos conjuntos: entrenamiento (train) y test:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42
)
```

Estamos usando el 80% de los datos para entrenamiento y el 20% para test. Esta es una proporción estándar en machine learning. El modelo nunca verá los datos de test durante el entrenamiento; solo los usaremos al final para evaluar qué tan bien generaliza el modelo.

Después de esta división, tenemos:
- `X_train`: (800, 2) - 800 muestras para entrenar
- `X_test`: (200, 2) - 200 muestras para evaluar
- `y_train`: (800,) - etiquetas de entrenamiento
- `y_test`: (200,) - etiquetas de test

### 1.6 Configuración del Dispositivo: CPU vs GPU

Una de las ventajas de PyTorch es que puede ejecutar cálculos tanto en CPU como en GPU de manera transparente. Las GPUs son órdenes de magnitud más rápidas para operaciones matriciales, que son el núcleo de las redes neuronales. Vamos a configurar nuestro código para que use GPU si está disponible:

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {device}")
```

Este código detecta automáticamente si tenemos una GPU CUDA disponible. Si la hay, `device` será "cuda"; si no, será "cpu". Ahora necesitamos mover nuestros datos y nuestro modelo (cuando lo creemos) a este dispositivo:

```python
X_train = X_train.to(device)
y_train = y_train.to(device)
X_test = X_test.to(device)
y_test = y_test.to(device)
```

El método `.to(device)` mueve un tensor al dispositivo especificado. Es fundamental que todos los tensores que participan en una operación estén en el mismo dispositivo. Si intentamos multiplicar un tensor en CPU con otro en GPU, PyTorch dará un error. Por eso movemos todos nuestros datos al mismo dispositivo desde el principio.

## Capítulo 2: Primer Intento - Modelo Lineal Simple

### 2.1 Construyendo el Modelo Más Simple Posible

Vamos a empezar con el modelo de red neuronal más simple que existe: una sola capa lineal, sin capas ocultas ni funciones de activación. Este modelo fallará, pero entender por qué falla es crucial para entender por qué necesitamos arquitecturas más complejas.

```python
class ModeloClasificacionV0(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=2, out_features=1)
    
    def forward(self, x):
        return self.layer_1(x)

model_0 = ModeloClasificacionV0().to(device)
```

Vamos a desglosar este código línea por línea porque es fundamental entenderlo. Cuando creamos un modelo en PyTorch, siempre creamos una clase que hereda de `nn.Module`. Esta es la clase base para todas las redes neuronales en PyTorch. 

En el método `__init__`, llamamos primero a `super().__init__()`, que inicializa la clase padre. Luego definimos las capas de nuestra red. En este caso, solo tenemos una capa: `self.layer_1 = nn.Linear(in_features=2, out_features=1)`.

¿Qué hace `nn.Linear`? Esta capa implementa una transformación lineal: y = xW^T + b, donde W es una matriz de pesos y b es un vector de bias. El parámetro `in_features=2` indica que esta capa recibe 2 características de entrada (nuestras coordenadas x e y). El parámetro `out_features=1` indica que produce una salida (un solo número, porque es clasificación binaria).

Cuando creamos esta capa, PyTorch automáticamente inicializa los pesos W y el bias b con valores aleatorios pequeños. Estos son los parámetros que la red aprenderá durante el entrenamiento. En este caso, W tendrá forma (1, 2) y b tendrá forma (1,).

El método `forward` define cómo fluyen los datos a través de la red. En este caso simple, los datos pasan directamente por la capa lineal y se devuelven. Cuando llamemos `model_0(X_train)`, PyTorch automáticamente llamará a este método `forward`.

Finalmente, usamos `.to(device)` para mover el modelo al dispositivo apropiado (GPU o CPU).

### 2.2 Función de Pérdida: BCEWithLogitsLoss

Ahora necesitamos definir cómo vamos a medir qué tan bien (o mal) está funcionando nuestro modelo. Para esto usamos una función de pérdida (loss function). Para clasificación binaria, la función de pérdida estándar es Binary Cross Entropy (BCE):

```python
loss_fn = nn.BCEWithLogitsLoss()
```

Vamos a entender en profundidad qué hace esta función. La entropía cruzada binaria mide la diferencia entre dos distribuciones de probabilidad: la distribución real (nuestras etiquetas, que son 0 o 1) y la distribución predicha por el modelo (que debería estar entre 0 y 1).

La fórmula de BCE es: Loss = -[y·log(p) + (1-y)·log(1-p)], donde y es la etiqueta real (0 o 1) y p es la probabilidad predicha (entre 0 y 1).

Pero hay un detalle importante: ¿por qué usamos `BCEWithLogitsLoss` en lugar de solo `BCELoss`? La diferencia está en los "logits". Un logit es la salida cruda de la red, que puede ser cualquier número real de -∞ a +∞. Para convertir logits en probabilidades (0 a 1), necesitamos aplicar la función sigmoid: p = 1/(1+e^(-logit)).

Podríamos aplicar sigmoid manualmente y luego usar `BCELoss`, pero `BCEWithLogitsLoss` hace ambas cosas internamente de una manera numéricamente más estable. Cuando los logits son muy grandes o muy pequeños, calcular sigmoid puede causar problemas de overflow o underflow. `BCEWithLogitsLoss` usa trucos matemáticos para evitar estos problemas, por eso es la opción recomendada.

### 2.3 Optimizador: Stochastic Gradient Descent

El optimizador es el algoritmo que actualiza los pesos de la red para minimizar la función de pérdida. Vamos a empezar con el optimizador más simple: Stochastic Gradient Descent (SGD):

```python
optimizer = torch.optim.SGD(model_0.parameters(), lr=0.1)
```

SGD implementa el algoritmo de descenso por gradiente: en cada paso, calcula el gradiente de la pérdida con respecto a cada parámetro (cada peso y bias de la red), y mueve los parámetros en la dirección opuesta al gradiente. La idea es que el gradiente apunta en la dirección de mayor crecimiento de la pérdida, así que movernos en dirección opuesta reduce la pérdida.

El parámetro `lr=0.1` es el learning rate (tasa de aprendizaje). Este es probablemente el hiperparámetro más importante en el entrenamiento de redes neuronales. Controla qué tan grande es cada paso que damos en la dirección del gradiente. Si el learning rate es demasiado grande, podemos "saltar" sobre el mínimo y el entrenamiento será inestable. Si es demasiado pequeño, el entrenamiento será muy lento y podemos quedarnos atascados en mínimos locales. Un valor de 0.1 es razonable para empezar con SGD, pero más adelante veremos que otros optimizadores funcionan mejor con valores más pequeños.

`model_0.parameters()` es un método que devuelve todos los parámetros entrenables del modelo. En nuestro caso, son los pesos W y el bias b de la capa lineal.

### 2.4 Función de Accuracy

Además de la pérdida, es útil tener una métrica más interpretable para evaluar nuestro modelo. Para clasificación, la métrica más común es accuracy (precisión): el porcentaje de predicciones correctas:

```python
def accuracy_fn(y_true, y_pred):
    correct = torch.eq(y_true, y_pred).sum().item()
    acc = (correct / len(y_pred)) * 100
    return acc
```

Esta función es simple: `torch.eq(y_true, y_pred)` crea un tensor de booleanos (True donde las predicciones son correctas, False donde no). `.sum()` cuenta cuántos True hay (cuántas predicciones correctas). `.item()` convierte el tensor de un elemento en un número Python normal. Finalmente, dividimos por el número total de predicciones y multiplicamos por 100 para obtener un porcentaje.

### 2.5 El Bucle de Entrenamiento

Ahora viene la parte más importante: el bucle de entrenamiento. Este es el proceso iterativo donde la red aprende. Vamos a verlo completo primero y luego lo desglosamos:

```python
torch.manual_seed(42)
torch.cuda.manual_seed(42)

epochs = 100

for epoch in range(epochs):
    ### Modo entrenamiento ###
    model_0.train()
    
    # 1. Forward pass
    y_logits = model_0(X_train).squeeze()
    y_pred = torch.round(torch.sigmoid(y_logits))
    
    # 2. Calcular pérdida
    loss = loss_fn(y_logits, y_train)
    
    # 3. Accuracy
    acc = accuracy_fn(y_train, y_pred)
    
    # 4. Zero gradients
    optimizer.zero_grad()
    
    # 5. Backpropagation
    loss.backward()
    
    # 6. Gradient descent
    optimizer.step()
    
    ### Modo evaluación ###
    model_0.eval()
    with torch.inference_mode():
        # Forward pass en test
        test_logits = model_0(X_test).squeeze()
        test_pred = torch.round(torch.sigmoid(test_logits))
        
        # Calcular pérdida y accuracy en test
        test_loss = loss_fn(test_logits, y_test)
        test_acc = accuracy_fn(y_test, test_pred)
    
    # Imprimir progreso cada 10 epochs
    if epoch % 10 == 0:
        print(f"Epoch: {epoch} | Loss: {loss:.5f}, Acc: {acc:.2f}% | Test Loss: {test_loss:.5f}, Test Acc: {test_acc:.2f}%")
```

Este es el corazón del entrenamiento de redes neuronales, así que vamos a entender cada paso en detalle.

**Epochs**: Una epoch es una pasada completa por todos los datos de entrenamiento. En este caso, entrenamos durante 100 epochs, lo que significa que la red verá todos los datos de entrenamiento 100 veces.

**model_0.train()**: Esta línea pone el modelo en modo entrenamiento. Algunas capas (como Dropout o BatchNorm, que veremos más adelante) se comportan diferente durante entrenamiento vs evaluación. Aunque nuestro modelo simple no tiene estas capas, es buena práctica siempre llamar a `.train()` antes de entrenar.

**Forward pass**: `y_logits = model_0(X_train).squeeze()` pasa todos los datos de entrenamiento por la red y obtiene las predicciones crudas (logits). `.squeeze()` elimina dimensiones de tamaño 1. La salida de nuestro modelo tiene forma (800, 1), pero queremos (800,) para que coincida con y_train.

**Conversión de logits a predicciones**: `y_pred = torch.round(torch.sigmoid(y_logits))` convierte los logits a predicciones finales. Primero, `torch.sigmoid()` convierte logits (-∞ a +∞) a probabilidades (0 a 1). Luego, `torch.round()` redondea: valores ≥0.5 se convierten en 1, valores <0.5 se convierten en 0.

**Calcular pérdida**: `loss = loss_fn(y_logits, y_train)` calcula qué tan mal están nuestras predicciones. Nota que pasamos los logits, no las predicciones redondeadas, porque `BCEWithLogitsLoss` espera logits.

**Zero gradients**: `optimizer.zero_grad()` es CRUCIAL. PyTorch acumula gradientes por defecto. Si no limpiamos los gradientes de la iteración anterior, se sumarán a los nuevos gradientes y obtendremos resultados incorrectos. Este es uno de los errores más comunes para principiantes.

**Backpropagation**: `loss.backward()` es donde ocurre la magia. Esta línea calcula automáticamente el gradiente de la pérdida con respecto a todos los parámetros del modelo usando la regla de la cadena. Después de esta línea, cada parámetro tendrá un atributo `.grad` que contiene su gradiente.

**Gradient descent**: `optimizer.step()` actualiza todos los parámetros del modelo usando los gradientes calculados. Específicamente, para cada parámetro, hace: parámetro = parámetro - learning_rate * gradiente.

**Evaluación en test**: Después de cada epoch de entrenamiento, evaluamos el modelo en el conjunto de test. Usamos `model_0.eval()` para poner el modelo en modo evaluación. `torch.inference_mode()` es un administrador de contexto que desactiva el cálculo de gradientes, lo que ahorra memoria y acelera la evaluación. Dentro de este bloque, hacemos un forward pass en los datos de test y calculamos la pérdida y accuracy.

### 2.6 Resultados del Modelo Lineal Simple

Si ejecutamos este código, veremos algo como:

```
Epoch: 0 | Loss: 0.69315, Acc: 50.50% | Test Loss: 0.69338, Test Acc: 49.50%
Epoch: 10 | Loss: 0.69298, Acc: 50.62% | Test Loss: 0.69319, Test Acc: 49.50%
Epoch: 20 | Loss: 0.69279, Acc: 50.75% | Test Loss: 0.69299, Test Acc: 49.50%
...
Epoch: 90 | Loss: 0.69140, Acc: 51.88% | Test Loss: 0.69155, Test Acc: 50.50%
```

La pérdida baja muy poco y la accuracy se queda alrededor del 50%. Para un problema de clasificación binaria balanceada, 50% de accuracy es lo que obtendríamos adivinando al azar. Claramente, ¡nuestro modelo no está aprendiendo!

¿Por qué falla este modelo? El problema fundamental es que una sola capa lineal solo puede aprender límites de decisión lineales. Matemáticamente, nuestro modelo está calculando: decisión = w1·x + w2·y + b. Esto define una línea recta en el espacio 2D. Los puntos de un lado de la línea se clasifican como 0, los del otro lado como 1.

Pero nuestros datos (círculos concéntricos) no son linealmente separables. No hay ninguna línea recta que pueda separar el círculo interior del exterior. Necesitamos un límite de decisión curvo, no lineal. Por eso el modelo falla.

Esta es una lección fundamental: para problemas no lineales (que son la mayoría en la práctica), necesitamos modelos no lineales.

## Capítulo 3: Segundo Intento - Añadiendo Capas Ocultas

### 3.1 Construyendo un Modelo con Capas Ocultas

El siguiente paso lógico es añadir capas ocultas. La idea es que cada capa adicional puede aprender representaciones más complejas de los datos. Vamos a crear un modelo con dos capas ocultas:

```python
class ModeloClasificacionV1(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=2, out_features=10)
        self.layer_2 = nn.Linear(in_features=10, out_features=10)
        self.layer_3 = nn.Linear(in_features=10, out_features=1)
    
    def forward(self, x):
        return self.layer_3(self.layer_2(self.layer_1(x)))

model_1 = ModeloClasificacionV1().to(device)
```

Este modelo tiene tres capas lineales. La primera capa toma las 2 características de entrada y produce 10 salidas. Estas 10 salidas son como "características intermedias" aprendidas por la red. La segunda capa toma estas 10 características y produce otras 10. La tercera capa toma esas 10 características y produce la salida final (1 número).

El número 10 para las capas ocultas es un hiperparámetro que elegimos. Podríamos usar 5, 20, 100, etc. Generalmente, más neuronas significan más capacidad de aprendizaje, pero también más riesgo de overfitting y más tiempo de entrenamiento. 10 es un número razonable para empezar con este problema simple.

En el método `forward`, las capas se aplican secuencialmente: `self.layer_3(self.layer_2(self.layer_1(x)))`. Los datos fluyen a través de la capa 1, luego la capa 2, luego la capa 3.

### 3.2 Entrenando el Modelo V1

Vamos a entrenar este modelo con el mismo proceso que antes. Usamos la misma función de pérdida, el mismo optimizador, el mismo bucle de entrenamiento:

```python
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.SGD(model_1.parameters(), lr=0.1)

torch.manual_seed(42)
torch.cuda.manual_seed(42)

epochs = 100

for epoch in range(epochs):
    model_1.train()
    y_logits = model_1(X_train).squeeze()
    y_pred = torch.round(torch.sigmoid(y_logits))
    loss = loss_fn(y_logits, y_train)
    acc = accuracy_fn(y_train, y_pred)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    model_1.eval()
    with torch.inference_mode():
        test_logits = model_1(X_test).squeeze()
        test_pred = torch.round(torch.sigmoid(test_logits))
        test_loss = loss_fn(test_logits, y_test)
        test_acc = accuracy_fn(y_test, test_pred)
    
    if epoch % 10 == 0:
        print(f"Epoch: {epoch} | Loss: {loss:.5f}, Acc: {acc:.2f}% | Test Loss: {test_loss:.5f}, Test Acc: {test_acc:.2f}%")
```

### 3.3 Resultados del Modelo V1

Si ejecutamos este código, veremos algo sorprendente: ¡los resultados son casi idénticos al modelo anterior!

```
Epoch: 0 | Loss: 0.69315, Acc: 50.38% | Test Loss: 0.69338, Test Acc: 49.50%
Epoch: 10 | Loss: 0.69279, Acc: 50.75% | Test Loss: 0.69299, Test Acc: 49.50%
...
Epoch: 90 | Loss: 0.69107, Acc: 52.25% | Test Loss: 0.69120, Test Acc: 51.00%
```

La accuracy sigue siendo alrededor del 50%. El modelo con múltiples capas no es significativamente mejor que el modelo de una sola capa. ¿Por qué?

La razón es profunda y matemática: una composición de funciones lineales es también una función lineal. Matemáticamente:
- Capa 1: z1 = x·W1 + b1
- Capa 2: z2 = z1·W2 + b2 = (x·W1 + b1)·W2 + b2 = x·(W1·W2) + (b1·W2 + b2)
- Capa 3: z3 = z2·W3 + b3 = ...

Si expandimos toda la expresión, podemos escribir z3 = x·W_total + b_total, donde W_total y b_total son combinaciones de todos los pesos y biases. Es decir, ¡la red multicapa es equivalente a una sola capa lineal! No importa cuántas capas lineales apilemos, el resultado siempre será lineal.

Esto es un problema fundamental: para aprender funciones no lineales (como nuestros círculos concéntricos), necesitamos introducir no-linealidad en la red. Aquí es donde entran las funciones de activación.

## Capítulo 4: La Solución - Funciones de Activación No Lineales

### 4.1 ¿Qué son las Funciones de Activación?

Una función de activación es una función no lineal que se aplica elemento a elemento a la salida de cada capa. Las funciones de activación rompen la linealidad de la red y permiten que aprenda funciones arbitrariamente complejas.

La función de activación más popular en deep learning moderno es ReLU (Rectified Linear Unit), definida como:

ReLU(x) = max(0, x)

Es decir, si x es positivo, ReLU devuelve x; si x es negativo o cero, ReLU devuelve 0. Aunque ReLU es matemáticamente simple, introduce no-linealidad de manera muy efectiva.

¿Por qué ReLU es tan popular? Tiene varias ventajas:
1. Es computacionalmente muy eficiente: solo requiere comparar con cero y elegir el máximo.
2. No sufre del problema del "gradiente desvaneciente" que afecta a funciones como sigmoid o tanh. En sigmoid/tanh, para valores de entrada muy grandes o muy pequeños, el gradiente se vuelve casi cero, lo que hace que el aprendizaje sea muy lento. ReLU no tiene este problema para valores positivos.
3. Promueve sparsity: muchas neuronas se "apagan" (producen 0), lo que puede hacer que la red sea más interpretable y eficiente.

### 4.2 Otras Funciones de Activación

Aunque ReLU es la más común, hay otras funciones de activación que se usan en contextos específicos:

**Sigmoid**: σ(x) = 1 / (1 + e^(-x))
Transforma cualquier entrada a un valor entre 0 y 1. Útil para la capa de salida en clasificación binaria cuando queremos interpretar la salida como probabilidad. Sin embargo, sufre de gradiente desvaneciente, por eso ya no se usa en capas ocultas.

**Tanh**: tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))
Transforma cualquier entrada a un valor entre -1 y 1. Similar a sigmoid pero centrada en cero, lo que puede hacer el entrenamiento más estable en algunos casos. También sufre de gradiente desvaneciente.

**Leaky ReLU**: max(0.01x, x)
Una variante de ReLU que permite un pequeño gradiente negativo (0.01x) cuando x < 0. Esto evita el problema de "neuronas muertas" que puede ocurrir con ReLU: si una neurona siempre produce valores negativos, ReLU siempre producirá 0 y su gradiente será 0, así que la neurona nunca se actualizará.

**ELU (Exponential Linear Unit)**: x si x > 0, α(e^x - 1) si x ≤ 0
Otra variante que intenta combinar las ventajas de ReLU con una salida suave para valores negativos.

Para nuestro problema, vamos a usar ReLU, que es la opción estándar y funciona bien en la mayoría de los casos.

### 4.3 Construyendo el Modelo V2 con ReLU

Vamos a reconstruir nuestro modelo, ahora añadiendo ReLU después de cada capa oculta:

```python
class ModeloClasificacionV2(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=2, out_features=10)
        self.layer_2 = nn.Linear(in_features=10, out_features=10)
        self.layer_3 = nn.Linear(in_features=10, out_features=1)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        return self.layer_3(self.relu(self.layer_2(self.relu(self.layer_1(x)))))

model_2 = ModeloClasificacionV2().to(device)
```

Ahora, en el método `forward`, aplicamos ReLU después de la capa 1 y después de la capa 2. Nota que NO aplicamos ReLU después de la capa 3 (la capa de salida), porque queremos que la salida pueda ser cualquier número real (logit).

Alternativamente, podemos usar `nn.Sequential` para construir el modelo de manera más compacta:

```python
model_2 = nn.Sequential(
    nn.Linear(in_features=2, out_features=10),
    nn.ReLU(),
    nn.Linear(in_features=10, out_features=10),
    nn.ReLU(),
    nn.Linear(in_features=10, out_features=1)
).to(device)
```

Esta notación es más limpia y hace explícito el flujo de datos: Linear → ReLU → Linear → ReLU → Linear. Ambas formas son equivalentes; usa la que te resulte más clara.

### 4.4 Cambiando a Adam Optimizer

Hasta ahora hemos usado SGD, pero para este modelo vamos a cambiar a Adam, que es un optimizador más sofisticado:

```python
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model_2.parameters(), lr=0.01)
```

Adam (Adaptive Moment Estimation) es uno de los optimizadores más populares en deep learning. Combina ideas de dos optimizadores anteriores: Momentum y RMSprop.

**Momentum** es una técnica que acelera SGD en la dirección correcta y amortigua oscilaciones. La idea es que el optimizador acumula un "vector de velocidad" en la dirección de los gradientes anteriores. Esto ayuda a superar mínimos locales superficiales y a moverse más rápido por valles largos y estrechos en el paisaje de la función de pérdida.

**RMSprop** adapta el learning rate para cada parámetro basándose en la magnitud promedio de los gradientes recientes. Parámetros con gradientes grandes reciben un learning rate más pequeño, y viceversa.

**Adam** combina ambas ideas: mantiene promedios móviles exponenciales tanto del gradiente (primer momento) como del cuadrado del gradiente (segundo momento), y usa estos para adaptar el learning rate de cada parámetro.

En la práctica, Adam generalmente converge más rápido que SGD y es menos sensible a la elección del learning rate inicial. Por eso hemos elegido un learning rate más pequeño (0.01 en lugar de 0.1). Adam típicamente funciona bien con learning rates en el rango 0.001 - 0.01.

### 4.5 Entrenando el Modelo V2

Vamos a entrenar este modelo, pero esta vez durante más epochs porque ahora tenemos más capacidad de aprendizaje:

```python
torch.manual_seed(42)
torch.cuda.manual_seed(42)

epochs = 1000

for epoch in range(epochs):
    model_2.train()
    y_logits = model_2(X_train).squeeze()
    y_pred = torch.round(torch.sigmoid(y_logits))
    loss = loss_fn(y_logits, y_train)
    acc = accuracy_fn(y_train, y_pred)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    model_2.eval()
    with torch.inference_mode():
        test_logits = model_2(X_test).squeeze()
        test_pred = torch.round(torch.sigmoid(test_logits))
        test_loss = loss_fn(test_logits, y_test)
        test_acc = accuracy_fn(y_test, test_pred)
    
    if epoch % 100 == 0:
        print(f"Epoch: {epoch} | Loss: {loss:.5f}, Acc: {acc:.2f}% | Test Loss: {test_loss:.5f}, Test Acc: {test_acc:.2f}%")
```

### 4.6 Resultados del Modelo V2 - ¡Éxito!

Ahora sí, veremos resultados dramáticamente diferentes:

```
Epoch: 0 | Loss: 0.69536, Acc: 48.38% | Test Loss: 0.69629, Test Acc: 47.00%
Epoch: 100 | Loss: 0.04856, Acc: 99.75% | Test Loss: 0.04897, Test Acc: 99.50%
Epoch: 200 | Loss: 0.02156, Acc: 100.00% | Test Loss: 0.02212, Test Acc: 100.00%
Epoch: 300 | Loss: 0.01344, Acc: 100.00% | Test Loss: 0.01403, Test Acc: 100.00%
...
Epoch: 900 | Loss: 0.00501, Acc: 100.00% | Test Loss: 0.00563, Test Acc: 100.00%
```

¡La pérdida baja drásticamente y la accuracy sube a casi 100%! El modelo ahora está aprendiendo correctamente. La diferencia es dramática: simplemente añadiendo funciones de activación no lineales (ReLU), transformamos un modelo que no podía aprender en uno que alcanza accuracy casi perfecta.

Esto demuestra una de las lecciones más importantes en redes neuronales: **las funciones de activación no lineales son esenciales**. Sin ellas, no importa cuántas capas añadas, tu red seguirá siendo equivalente a un modelo lineal simple.

## Capítulo 5: Haciendo Predicciones

### 5.1 Del Modelo a Predicciones Finales

Una vez que hemos entrenado nuestro modelo, queremos usarlo para hacer predicciones sobre nuevos datos. El proceso de convertir la salida cruda del modelo (logits) en predicciones finales (clases 0 o 1) implica varios pasos que debemos entender:

```python
model_2.eval()
with torch.inference_mode():
    y_logits = model_2(X_test).squeeze()
    y_pred_probs = torch.sigmoid(y_logits)
    y_preds = torch.round(y_pred_probs)
```

**Paso 1 - Logits**: `y_logits = model_2(X_test).squeeze()` obtiene las salidas crudas del modelo. Estos son números que pueden estar en cualquier rango (-∞ a +∞). Para clasificación binaria, un logit negativo generalmente indica clase 0, y un logit positivo indica clase 1, pero estos valores no son interpretables como probabilidades.

**Paso 2 - Probabilidades**: `y_pred_probs = torch.sigmoid(y_logits)` convierte los logits en probabilidades usando la función sigmoid. Después de este paso, todos los valores están en el rango  y pueden interpretarse como "probabilidad de que la muestra pertenezca a la clase 1".

**Paso 3 - Clases**: `y_preds = torch.round(y_pred_probs)` convierte probabilidades en clases concretas. `torch.round()` usa 0.5 como umbral: probabilidades ≥ 0.5 se convierten en 1, probabilidades < 0.5 se convierten en 0.

Es importante entender que este umbral de 0.5 es una convención, no una regla absoluta. En algunos problemas, podrías querer usar un umbral diferente. Por ejemplo, en detección de fraude, podrías usar un umbral más bajo (digamos 0.3) para ser más conservador y capturar más casos sospechosos, aceptando más falsos positivos.

### 5.2 Evaluación Final

Vamos a calcular la accuracy final en el conjunto de test:

```python
model_2.eval()
with torch.inference_mode():
    test_logits = model_2(X_test).squeeze()
    test_preds = torch.round(torch.sigmoid(test_logits))
    test_accuracy = accuracy_fn(y_test, test_preds)
    
print(f"Accuracy final en test: {test_accuracy:.2f}%")
```

Con nuestro modelo entrenado correctamente, deberíamos ver una accuracy superior al 95%, probablemente cercana al 100%. Esto significa que el modelo ha aprendido a separar correctamente los círculos concéntricos.

## Capítulo 6: De Clasificación a Regresión

### 6.1 ¿Qué es Regresión?

Hasta ahora hemos trabajado en un problema de clasificación: predecir categorías discretas (0 o 1). Pero muchos problemas en machine learning son de regresión: predecir valores continuos. Por ejemplo, predecir el precio de una casa, la temperatura de mañana, las ventas del próximo mes, etc.

La buena noticia es que la arquitectura básica de una red neuronal para regresión es muy similar a la de clasificación. Las principales diferencias están en la capa de salida, la función de pérdida y cómo interpretamos las predicciones.

### 6.2 Generando Datos para Regresión

Vamos a crear un problema de regresión simple: una relación lineal con ruido. Queremos que nuestro modelo aprenda a predecir y = 0.7x + 0.3 + ruido:

```python
torch.manual_seed(42)

X_regression = torch.arange(0, 1, 0.01).unsqueeze(dim=1)
y_regression = 0.7 * X_regression + 0.3 + 0.05 * torch.randn_like(X_regression)

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_regression, y_regression, test_size=0.2, random_state=42
)

X_train_reg = X_train_reg.to(device)
y_train_reg = y_train_reg.to(device)
X_test_reg = X_test_reg.to(device)
y_test_reg = y_test_reg.to(device)
```

`torch.arange(0, 1, 0.01)` crea 100 valores espaciados uniformemente entre 0 y 1. `.unsqueeze(dim=1)` añade una dimensión para que X tenga forma (100, 1) en lugar de (100,), porque nuestro modelo espera entrada 2D.

La ecuación `y = 0.7 * X + 0.3 + 0.05 * torch.randn_like(X)` crea valores y que siguen aproximadamente una línea recta (y = 0.7x + 0.3), pero con ruido gaussiano añadido (el término 0.05 * torch.randn_like(X)). El ruido simula la imperfección de datos del mundo real.

### 6.3 Construyendo un Modelo de Regresión

El modelo para regresión es casi idéntico al de clasificación, con una diferencia clave: la salida es un número real sin restricciones, no un logit que se convierte en probabilidad:

```python
class ModeloRegresion(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=1, out_features=10)
        self.layer_2 = nn.Linear(in_features=10, out_features=10)
        self.layer_3 = nn.Linear(in_features=10, out_features=1)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        return self.layer_3(self.relu(self.layer_2(self.relu(self.layer_1(x)))))

model_reg = ModeloRegresion().to(device)
```

Nota que la capa de entrada ahora toma 1 característica (solo x) en lugar de 2. La capa de salida produce 1 valor, que es nuestra predicción de y. Al igual que en clasificación, usamos ReLU entre las capas para introducir no-linealidad.

### 6.4 Función de Pérdida para Regresión: MSE

Para regresión, no usamos BCE. La función de pérdida estándar es Mean Squared Error (MSE):

```python
loss_fn_reg = nn.MSELoss()
```

MSE calcula el error cuadrático medio: MSE = (1/n) Σ(y_pred - y_true)². Esta función penaliza más los errores grandes que los pequeños (debido al cuadrado). Si nuestro modelo predice 5 cuando la verdad es 3, el error cuadrático es (5-3)² = 4. Si predice 10, el error es (10-3)² = 49, mucho mayor.

**Alternativas a MSE**:

**MAE (Mean Absolute Error)**: `nn.L1Loss()`. Calcula MAE = (1/n) Σ|y_pred - y_true|. A diferencia de MSE, MAE penaliza todos los errores proporcionalmente. Es más robusto a outliers. Si tienes datos con valores extremos ocasionales, MAE puede ser mejor que MSE.

**Huber Loss**: Un híbrido que se comporta como MSE para errores pequeños y como MAE para errores grandes. Combina las ventajas de ambos.

Para nuestro problema, usamos MSE porque es estándar y funciona bien cuando los datos no tienen outliers extremos.

### 6.5 Entrenamiento del Modelo de Regresión

El bucle de entrenamiento es prácticamente idéntico al de clasificación, con dos diferencias: no aplicamos sigmoid ni round a las predicciones (porque queremos valores continuos), y usamos MAE como métrica en lugar de accuracy:

```python
optimizer_reg = torch.optim.Adam(model_reg.parameters(), lr=0.01)

def mae(y_true, y_pred):
    return torch.mean(torch.abs(y_true - y_pred)).item()

torch.manual_seed(42)
epochs = 1000

for epoch in range(epochs):
    model_reg.train()
    y_pred = model_reg(X_train_reg)
    loss = loss_fn_reg(y_pred, y_train_reg)
    optimizer_reg.zero_grad()
    loss.backward()
    optimizer_reg.step()
    
    model_reg.eval()
    with torch.inference_mode():
        test_pred = model_reg(X_test_reg)
        test_loss = loss_fn_reg(test_pred, y_test_reg)
        test_mae = mae(y_test_reg, test_pred)
    
    if epoch % 100 == 0:
        train_mae = mae(y_train_reg, y_pred)
        print(f"Epoch: {epoch} | Loss: {loss:.6f}, MAE: {train_mae:.6f} | Test Loss: {test_loss:.6f}, Test MAE: {test_mae:.6f}")
```

MAE (Mean Absolute Error) es más interpretable que MSE para regresión porque está en las mismas unidades que la variable objetivo. Si estamos prediciendo precios en euros y MAE es 5, significa que en promedio nos equivocamos por 5 euros.

### 6.6 Resultados y Predicciones

Después de entrenar, deberíamos ver que la pérdida y MAE bajan significativamente:

```
Epoch: 0 | Loss: 0.315626, MAE: 0.519845 | Test Loss: 0.318426, Test MAE: 0.519012
Epoch: 100 | Loss: 0.001892, MAE: 0.037721 | Test Loss: 0.002156, Test MAE: 0.040789
Epoch: 200 | Loss: 0.001823, MAE: 0.037102 | Test Loss: 0.002084, Test MAE: 0.040206
...
Epoch: 900 | Loss: 0.001823, MAE: 0.037101 | Test Loss: 0.002084, Test MAE: 0.040205
```

Un MAE de ~0.04 significa que nuestras predicciones están, en promedio, a una distancia de 0.04 del valor real. Dado que nuestros valores y están en el rango [0.3, 1.0], este es un error muy pequeño.

Podemos visualizar algunas predicciones:

```python
model_reg.eval()
with torch.inference_mode():
    ejemplos = torch.tensor([[0.0], [0.25], [0.5], [0.75], [1.0]]).to(device)
    preds = model_reg(ejemplos)
    
for x_val, pred_val in zip(ejemplos.cpu().numpy(), preds.cpu().numpy()):
    y_real = 0.7 * x_val[0] + 0.3
    print(f"X = {x_val[0]:.2f} -> Predicción: {pred_val[0]:.4f}, Real: {y_real:.4f}")
```

Esto mostrará que las predicciones están muy cerca de los valores reales de la función subyacente y = 0.7x + 0.3.

## Capítulo 7: Problemas Comunes y Debugging

### 7.1 Underfitting vs Overfitting

Cuando entrenas una red neuronal, hay dos problemas opuestos que pueden ocurrir:

**Underfitting** ocurre cuando el modelo es demasiado simple para capturar los patrones en los datos. Los síntomas son:
- Pérdida alta tanto en entrenamiento como en test
- Accuracy baja en ambos conjuntos
- El modelo no mejora significativamente con más entrenamiento

Vimos underfitting en nuestros primeros modelos (sin ReLU). Las soluciones incluyen:
- Añadir más capas o más neuronas por capa
- Entrenar durante más epochs
- Añadir funciones de activación no lineales
- Usar un optimizador más sofisticado (Adam en lugar de SGD)
- Aumentar el learning rate (con cuidado)

**Overfitting** ocurre cuando el modelo memoriza los datos de entrenamiento en lugar de aprender patrones generalizables. Los síntomas son:
- Pérdida muy baja en entrenamiento pero alta en test
- Gran diferencia entre accuracy de train y test
- El test loss empieza a subir mientras el train loss sigue bajando

Las soluciones para overfitting incluyen:
- Obtener más datos de entrenamiento
- Simplificar el modelo (menos capas/neuronas)
- Usar técnicas de regularización (Dropout, L2 regularization)
- Data augmentation (para imágenes)
- Early stopping (parar el entrenamiento cuando test loss empieza a subir)

### 7.2 Dropout: Regularización contra Overfitting

Dropout es una técnica de regularización muy efectiva. Durante el entrenamiento, Dropout "apaga" aleatoriamente un porcentaje de neuronas en cada forward pass. Esto fuerza a la red a ser robusta y no depender demasiado de neuronas específicas.

```python
model_with_dropout = nn.Sequential(
    nn.Linear(2, 10),
    nn.ReLU(),
    nn.Dropout(p=0.2),  # Apaga 20% de neuronas
    nn.Linear(10, 10),
    nn.ReLU(),
    nn.Dropout(p=0.2),
    nn.Linear(10, 1)
)
```

El parámetro `p=0.2` significa que cada neurona tiene 20% de probabilidad de ser apagada (su salida se pone a 0) en cada forward pass durante el entrenamiento. Durante la evaluación (cuando llamamos `model.eval()`), Dropout se desactiva automáticamente y todas las neuronas se usan, pero sus salidas se escalan para compensar.

Dropout es especialmente útil cuando tienes un modelo grande entrenando en relativamente pocos datos. Para nuestro problema simple de círculos con 1000 muestras, no necesitamos Dropout, pero es una herramienta importante a conocer.

### 7.3 Errores Comunes

**Error 1: Olvidar optimizer.zero_grad()**
Sin esta línea, los gradientes se acumulan de una iteración a otra, causando actualizaciones incorrectas. El síntoma es que la pérdida no baja o incluso aumenta erraticamente.

**Error 2: Usar los datos de test para entrenar**
Nunca uses el conjunto de test para tomar decisiones sobre el modelo (elegir hiperparámetros, decidir cuándo parar, etc.). Esto causa "information leakage" y sobrestima el rendimiento real del modelo.

**Error 3: No mover modelo y datos al mismo dispositivo**
Si el modelo está en GPU pero los datos en CPU (o viceversa), obtendrás un error. Siempre verifica que todo esté en el mismo dispositivo con `.to(device)`.

**Error 4: Shape mismatches**
Las dimensiones de los tensores deben coincidir. Por ejemplo, si `y_train` tiene forma (800,) pero `y_logits` tiene forma (800, 1), la función de pérdida puede dar error. Usa `.squeeze()` o `.unsqueeze()` para ajustar las dimensiones.

**Error 5: No normalizar los datos**
Para algunos problemas (especialmente con features en diferentes escalas), normalizar los datos puede mejorar dramáticamente el entrenamiento. Sin embargo, para nuestro problema simple los datos ya están en un rango razonable.

## Capítulo 8: Comparación Final - Clasificación vs Regresión

### 8.1 Tabla Comparativa

Vamos a resumir las diferencias clave entre clasificación y regresión:

**Objetivo**:
- Clasificación: Predecir categorías discretas (0, 1, "perro", "gato")
- Regresión: Predecir valores continuos (precios, temperaturas, etc.)

**Capa de salida**:
- Clasificación binaria: 1 neurona (logit)
- Clasificación multiclase: N neuronas (una por clase)
- Regresión: 1 neurona (valor continuo) o N (regresión multivariada)

**Función de pérdida**:
- Clasificación binaria: BCEWithLogitsLoss
- Clasificación multiclase: CrossEntropyLoss
- Regresión: MSELoss o L1Loss

**Activación de salida**:
- Clasificación binaria: Sigmoid (implícito en BCEWithLogitsLoss)
- Clasificación multiclase: Softmax (implícito en CrossEntropyLoss)
- Regresión: Ninguna (salida sin restricciones)

**Predicciones finales**:
- Clasificación: sigmoid(logits) → round() → clases
- Regresión: usar salida directamente

**Métricas**:
- Clasificación: Accuracy, Precision, Recall, F1-Score
- Regresión: MSE, MAE, RMSE, R²

### 8.2 Código Completo - Clasificación

Aquí está el código completo para clasificación, desde datos hasta evaluación:

```python
import torch
import torch.nn as nn
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split

# Datos
torch.manual_seed(42)
X, y = make_circles(1000, noise=0.03, random_state=42)
X = torch.from_numpy(X).float()
y = torch.from_numpy(y).float()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

device = "cuda" if torch.cuda.is_available() else "cpu"
X_train, y_train, X_test, y_test = X_train.to(device), y_train.to(device), X_test.to(device), y_test.to(device)

# Modelo
model = nn.Sequential(
    nn.Linear(2, 16), nn.ReLU(),
    nn.Linear(16, 16), nn.ReLU(),
    nn.Linear(16, 1)
).to(device)

# Loss y optimizer
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Función accuracy
def accuracy_fn(y_true, y_pred):
    return (torch.eq(y_true, y_pred).sum().item() / len(y_pred)) * 100

# Entrenamiento
epochs = 1000
for epoch in range(epochs):
    model.train()
    y_logits = model(X_train).squeeze()
    loss = loss_fn(y_logits, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 200 == 0:
        model.eval()
        with torch.inference_mode():
            test_logits = model(X_test).squeeze()
            test_pred = torch.sigmoid(test_logits).round()
            test_acc = accuracy_fn(y_test, test_pred)
            print(f"Epoch {epoch}: Loss {loss:.4f}, Test Acc {test_acc:.1f}%")

# Evaluación final
model.eval()
with torch.inference_mode():
    test_logits = model(X_test).squeeze()
    test_pred = torch.sigmoid(test_logits).round()
    final_acc = accuracy_fn(y_test, test_pred)
    print(f"\nAccuracy final: {final_acc:.2f}%")
```

### 8.3 Código Completo - Regresión

Y aquí el código completo para regresión:

```python
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split

# Datos
torch.manual_seed(42)
X = torch.linspace(0, 1, 100).unsqueeze(1)
y = 0.7 * X + 0.3 + 0.05 * torch.randn_like(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

device = "cuda" if torch.cuda.is_available() else "cpu"
X_train, y_train, X_test, y_test = X_train.to(device), y_train.to(device), X_test.to(device), y_test.to(device)

# Modelo
model = nn.Sequential(
    nn.Linear(1, 16), nn.ReLU(),
    nn.Linear(16, 16), nn.ReLU(),
    nn.Linear(16, 1)
).to(device)

# Loss y optimizer
loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Función MAE
def mae(y_true, y_pred):
    return torch.mean(torch.abs(y_true - y_pred)).item()

# Entrenamiento
epochs = 1000
for epoch in range(epochs):
    model.train()
    y_pred = model(X_train)
    loss = loss_fn(y_pred, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 200 == 0:
        model.eval()
        with torch.inference_mode():
            test_pred = model(X_test)
            test_mae = mae(y_test, test_pred)
            print(f"Epoch {epoch}: Loss {loss:.6f}, Test MAE {test_mae:.6f}")

# Evaluación final
model.eval()
with torch.inference_mode():
    test_pred = model(X_test)
    final_mae = mae(y_test, test_pred)
    print(f"\nMAE final: {final_mae:.6f}")
```
