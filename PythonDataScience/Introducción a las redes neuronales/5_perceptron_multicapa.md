# El Perceptrón Multicapa: Fundamentos, Implementación y Aplicaciones Avanzadas

## 1. De la Neurona Biológica al Perceptrón Multicapa

### 1.1 Evolución del Perceptrón

El **perceptrón multicapa (MLP, Multilayer Perceptron)** surge como una extensión directa del perceptrón simple para superar sus limitaciones. Mientras que el perceptrón simple solo es capaz de resolver problemas **linealmente separables**, la mayoría de los problemas del mundo real son **no lineales**. El MLP introduce una o más **capas ocultas** de neuronas entre la capa de entrada y la de salida, permitiendo que la red neuronal aprenda relaciones no lineales complejas.

### 1.2 Analogía con la Neurona Biológica

La estructura del MLP se inspira en la organización del cerebro humano:

- **Entrada (Dendritas)**: Las neuronas reciben señales de entrada.
- **Procesamiento (Soma y Axón)**: Las señales se integran y procesan a través de las capas ocultas.
- **Salida (Terminales Sinápticos)**: Se generan las respuestas o acciones en base al procesamiento.

Esta analogía biológica resalta cómo las redes neuronales artificiales buscan emular el procesamiento de información del cerebro.

## 2. Arquitectura y Componentes del MLP

### 2.1 Estructura de Capas

Un MLP se compone de:

1. **Capa de Entrada**:
   - Recibe los datos de entrada.
   - Cada nodo representa una característica del conjunto de datos.
2. **Capas Ocultas**:
   - Una o más capas entre la entrada y la salida.
   - Procesan y transforman los datos de manera no lineal.
   - Cada neurona en una capa está conectada con todas las neuronas de la siguiente capa (arquitectura totalmente conectada).
3. **Capa de Salida**:
   - Genera la predicción final.
   - El número de neuronas depende del problema (una para regresión, múltiples para clasificación multiclase).
  
  ![](images/mlp.png)

### 2.2 Funciones de Activación

Las **funciones de activación** introducen no linealidad en la red, permitiendo al MLP aprender relaciones complejas.

#### 2.2.1 Función Sigmoide

\[
\sigma(z) = \frac{1}{1 + e^{-z}}
\]

- **Ventajas**:
  - Salida en el rango (0, 1), útil para probabilidades.
- **Desventajas**:
  - Problema de **gradiente difuminado / Vanishing gradient** en capas profundas.
  - Salidas no centradas en cero.

#### 2.2.2 Tangente Hiperbólica (tanh)

\[
\tanh(z) = \frac{e^{z} - e^{-z}}{e^{z} + e^{-z}}
\]

- **Ventajas**:
  - Salida en el rango (-1, 1), centrada en cero.
  - Gradiente más fuerte que la sigmoide.
- **Desventajas**:
  - También sufre del problema de gradiente difuminado.

#### 2.2.3 ReLU (Rectified Linear Unit)

\[
\text{ReLU}(z) = \max(0, z)
\]

- **Ventajas**:
  - Simple y eficiente computacionalmente.
  - Mitiga el problema del gradiente difuminado.
- **Desventajas**:
  - Neuronas pueden "morir" si reciben siempre entradas negativas.

## 3. Propagación Hacia Adelante (Forward Propagation)

El proceso de **propagación hacia adelante** implica calcular las salidas de cada neurona, desde la capa de entrada hasta la de salida, pasando por las capas ocultas.

### 3.1 Proceso Detallado

Para cada capa \( l \):

1. **Cálculo de la Suma Ponderada**:

   \[
   z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}
   \]

   Donde:
   - \( W^{(l)} \) es la matriz de pesos de la capa \( l \).
   - \( a^{(l-1)} \) es el vector de activaciones de la capa anterior.
   - \( b^{(l)} \) es el vector de bias de la capa \( l \).

2. **Aplicación de la Función de Activación**:

   \[
   a^{(l)} = f(z^{(l)})
   \]

   Donde \( f \) es la función de activación escogida.

---

## 4. Ejemplo Numérico: Resolviendo el Problema XOR

### 4.1 ¿Por Qué el MLP Puede Resolver el Problema XOR?

El problema **XOR** (or exclusivo) no es linealmente separable, lo que significa que un perceptrón simple no puede resolverlo. Sin embargo, un MLP con una capa oculta y funciones de activación no lineales **sí puede** aprender esta relación no lineal.

La tabla de verdad del XOR es:

| Entrada \( x_1 \) | Entrada \( x_2 \) | Salida \( y \) |
|-------------------|-------------------|----------------|
| 0                 | 0                 | 0              |
| 0                 | 1                 | 1              |
| 1                 | 0                 | 1              |
| 1                 | 1                 | 0              |

El objetivo es entrenar una red neuronal que reciba dos entradas binarias (0 o 1) y devuelva la salida correcta según la operación XOR.

### 4.2 Arquitectura del MLP

Para resolver XOR, necesitamos una red con la siguiente estructura:

- **Capa de Entrada**: 2 neuronas (una para cada valor de entrada).
- **Capa Oculta**: 2 neuronas. Aquí es donde se introduce la **no linealidad** mediante una función de activación sigmoide.
- **Capa de Salida**: 1 neurona, cuya salida será el resultado final (0 o 1), aplicando también la función sigmoide para obtener una probabilidad.

### 4.3 Inicialización de Pesos y Biases

Para simplificar el ejemplo, usaremos pesos y biases predefinidos que resuelven correctamente el problema XOR. En un escenario real, estos valores se obtendrían tras entrenar la red utilizando **backpropagation**.

- **Pesos de la Capa Oculta** (\( W^{(1)} \)): 
  Estos pesos conectan las dos neuronas de entrada con las dos neuronas de la capa oculta. Los representamos como una **matriz** de 2x2:

  \[
  W^{(1)} = \begin{pmatrix}
  20 & 20 \\
  -20 & -20
  \end{pmatrix}
  \]

- **Biases de la Capa Oculta** (\( b^{(1)} \)): 

  \[
  b^{(1)} = \begin{pmatrix} -10 \\ 30 \end{pmatrix}
  \]

- **Pesos de la Capa de Salida** (\( W^{(2)} \)): 

  \[
  W^{(2)} = \begin{pmatrix} 20 & 20 \end{pmatrix}
  \]

- **Bias de la Capa de Salida** (\( b^{(2)} \)): 

  \[
  b^{(2)} = \begin{pmatrix} -30 \end{pmatrix}
  \]

### 4.4 Cálculos Paso a Paso

Tomemos como ejemplo la entrada \( x = \begin{pmatrix} 0 \\ 1 \end{pmatrix} \).

#### Paso 1: Cálculo en la Capa Oculta

Para cada neurona en la capa oculta, calculamos el valor ponderado de la entrada más el bias:

1. **Primera Neurona de la Capa Oculta**:
   - Suma ponderada:

     \[
     z_1^{(1)} = (20 \times 0) + (20 \times 1) + (-10) = 0 + 20 - 10 = 10
     \]

2. **Segunda Neurona de la Capa Oculta**:
   - Suma ponderada:

     \[
     z_2^{(1)} = (-20 \times 0) + (-20 \times 1) + 30 = 0 - 20 + 30 = 10
     \]

Luego, aplicamos la función de activación **sigmoide** a los valores \( z_1^{(1)} \) y \( z_2^{(1)} \):

\[
\sigma(z) = \frac{1}{1 + e^{-z}}
\]

Aplicamos esta función a los valores calculados:

\[
a_1^{(1)} = \sigma(10) \approx 0.99995 \quad \text{y} \quad a_2^{(1)} = \sigma(10) \approx 0.99995
\]

Estas son las activaciones de las neuronas en la capa oculta.

#### Paso 2:

 Cálculo en la Capa de Salida

Usamos las activaciones \( a_1^{(1)} \) y \( a_2^{(1)} \) para calcular la suma ponderada en la **neurona de salida**:

\[
z^{(2)} = (20 \times 0.99995) + (20 \times 0.99995) + (-30) \approx 19.999 + 19.999 - 30 = 9.998
\]

Aplicamos la función sigmoide a este valor:

\[
a^{(2)} = \sigma(9.998) \approx 0.99995
\]

Interpretamos la salida como 1, lo cual es correcto para la entrada \( x = (0, 1) \).

### 4.5 Interpretación de los Resultados

Este ejemplo muestra cómo un MLP puede calcular correctamente la salida del problema XOR usando pesos y biases predefinidos. **En un proceso real**, los pesos y biases no son perfectos al inicio, sino que el MLP debe entrenarse para aprender estos valores a través de **backpropagation y descenso por gradiente**. Esto implica que el MLP ajusta iterativamente los pesos hasta que puede resolver el problema XOR de manera precisa.

---

## 5. Descenso por Gradiente: Fundamentos y Ejemplos

El siguiente paso importante es entender cómo los **pesos y biases** se ajustan automáticamente durante el entrenamiento de una red neuronal. El **descenso por gradiente** es el algoritmo clave para este ajuste, y el **backpropagation** es la técnica que permite calcular los gradientes de manera eficiente.

---

Esta es la explicación completa y ajustada, detallando el ejemplo del XOR y corrigiendo los malentendidos sobre el entrenamiento. Los pesos utilizados en el ejemplo son preajustados para ilustrar el cálculo, pero en la práctica, el MLP necesitaría ser entrenado para aprender estos valores.