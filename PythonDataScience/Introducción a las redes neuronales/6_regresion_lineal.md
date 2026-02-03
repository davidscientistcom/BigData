# Capítulo: Del Descenso por Gradiente a la Retropropagación en Redes Neuronales

## Introducción

En el aprendizaje automático, es fundamental comprender cómo los modelos aprenden de los datos ajustando sus parámetros para minimizar el error. Este proceso comienza con modelos simples como la **regresión lineal** y se extiende a técnicas más avanzadas como las **redes neuronales**. En este capítulo, exploraremos en detalle cómo se realiza el cálculo del gradiente en la regresión lineal y logística, y cómo estos conceptos se relacionan con el **perceptrón multicapa** y el algoritmo de **retropropagación**.

---

## 1. Regresión Lineal y Descenso por Gradiente

### 1.1. Modelo de Regresión Lineal

La regresión lineal busca modelar la relación entre una variable independiente \( x \) y una variable dependiente \( y \) mediante una línea recta:

\[
\hat{y} = \theta_0 + \theta_1 x
\]

Donde:

- \( \hat{y} \) es el valor predicho.
- \( \theta_0 \) es el intercepto (término independiente).
- \( \theta_1 \) es la pendiente (coeficiente de regresión).

### 1.2. Función de Costo: Error Cuadrático Medio (MSE)

Para evaluar qué tan bien nuestro modelo se ajusta a los datos, utilizamos una **función de costo** que mide el error entre las predicciones y los valores reales. En la regresión lineal, el **Error Cuadrático Medio** (MSE) es una elección común:

\[
J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=1}^{m} (\hat{y}_i - y_i)^2
\]

Donde:

- \( m \) es el número de ejemplos en el conjunto de datos.
- \( y_i \) es el valor real para el ejemplo \( i \).
- \( \hat{y}_i \) es el valor predicho para el ejemplo \( i \).

**Visualización de la Función de Costo:**

La función de costo \( J(\theta_0, \theta_1) \) es una función convexa en términos de \( \theta_0 \) y \( \theta_1 \), lo que significa que tiene un único mínimo global. Si graficamos el error cuadrático medio en función de los parámetros, obtenemos una superficie paraboloide.

 ![](images/mse_gradient.png)

### 1.3. Cálculo del Gradiente

Para encontrar el mínimo de la función de costo, necesitamos calcular sus derivadas parciales respecto a \( \theta_0 \) y \( \theta_1 \). Esto nos da la dirección del gradiente, que indica cómo ajustar los parámetros para reducir el error.

#### 1.3.1. Derivada Parcial Respecto a \( \theta_0 \)

Comenzamos con la función de costo:

\[
J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=1}^{m} \left( \theta_0 + \theta_1 x_i - y_i \right)^2
\]

Calculamos la derivada parcial de \( J \) respecto a \( \theta_0 \):

\[
\frac{\partial J}{\partial \theta_0} = \frac{\partial}{\partial \theta_0} \left( \frac{1}{2m} \sum_{i=1}^{m} \left( \theta_0 + \theta_1 x_i - y_i \right)^2 \right)
\]

Aplicamos la derivada al sumatorio:

\[
\frac{\partial J}{\partial \theta_0} = \frac{1}{2m} \sum_{i=1}^{m} \frac{\partial}{\partial \theta_0} \left( \left( \theta_0 + \theta_1 x_i - y_i \right)^2 \right)
\]

Usamos la regla de la cadena:

\[
\frac{\partial}{\partial \theta_0} \left( u^2 \right) = 2u \cdot \frac{\partial u}{\partial \theta_0}
\]

Donde \( u = \theta_0 + \theta_1 x_i - y_i \).

Entonces:

\[
\frac{\partial J}{\partial \theta_0} = \frac{1}{2m} \sum_{i=1}^{m} 2 \left( \theta_0 + \theta_1 x_i - y_i \right) \cdot 1
\]

El término \( \frac{\partial u}{\partial \theta_0} = 1 \) porque \( \theta_1 x_i \) y \( y_i \) son constantes respecto a \( \theta_0 \).

Simplificamos:

\[
\frac{\partial J}{\partial \theta_0} = \frac{1}{m} \sum_{i=1}^{m} \left( \theta_0 + \theta_1 x_i - y_i \right)
\]

#### 1.3.2. Derivada Parcial Respecto a \( \theta_1 \)

Similarmente, calculamos la derivada parcial respecto a \( \theta_1 \):

\[
\frac{\partial J}{\partial \theta_1} = \frac{\partial}{\partial \theta_1} \left( \frac{1}{2m} \sum_{i=1}^{m} \left( \theta_0 + \theta_1 x_i - y_i \right)^2 \right)
\]

Aplicamos la regla de la cadena:

\[
\frac{\partial J}{\partial \theta_1} = \frac{1}{2m} \sum_{i=1}^{m} 2 \left( \theta_0 + \theta_1 x_i - y_i \right) \cdot x_i
\]

Aquí, \( \frac{\partial u}{\partial \theta_1} = x_i \).

Simplificamos:

\[
\frac{\partial J}{\partial \theta_1} = \frac{1}{m} \sum_{i=1}^{m} \left( \theta_0 + \theta_1 x_i - y_i \right) x_i
\]

### 1.4. Descenso por Gradiente

El **descenso por gradiente** es un algoritmo iterativo que actualiza los parámetros en la dirección opuesta al gradiente de la función de costo:

\[
\theta_j := \theta_j - \alpha \frac{\partial J}{\partial \theta_j}
\]

Donde:

- \( \alpha \) es la tasa de aprendizaje.
- \( \theta_j \) representa \( \theta_0 \) o \( \theta_1 \).

**Pasos del Algoritmo:**

1. **Inicializar** \( \theta_0 \) y \( \theta_1 \) con valores aleatorios o ceros.
2. **Repetir** hasta la convergencia:
   - **Calcular** las derivadas parciales \( \frac{\partial J}{\partial \theta_0} \) y \( \frac{\partial J}{\partial \theta_1} \).
   - **Actualizar** los parámetros:
     \[
     \theta_0 := \theta_0 - \alpha \frac{\partial J}{\partial \theta_0}
     \]
     \[
     \theta_1 := \theta_1 - \alpha \frac{\partial J}{\partial \theta_1}
     \]
   - **Calcular** el nuevo costo \( J(\theta_0, \theta_1) \) para monitorear la convergencia.

### 1.5. Ejemplo Numérico

Supongamos que tenemos los siguientes datos:

| \( x \) | \( y \) |
|---------|---------|
| 1       | 2       |
| 2       | 2.5     |
| 3       | 3.5     |
| 4       | 5       |

**Inicialización:**

- \( \theta_0 = 0 \)
- \( \theta_1 = 0 \)
- \( \alpha = 0.01 \)
- \( m = 4 \)

**Iteración 1:**

1. **Calculamos las predicciones:**

   \[
   \hat{y}_i = \theta_0 + \theta_1 x_i = 0 + 0 \times x_i = 0
   \]

2. **Calculamos las derivadas:**

   - Para \( \theta_0 \):

     \[
     \frac{\partial J}{\partial \theta_0} = \frac{1}{4} \sum_{i=1}^{4} (\hat{y}_i - y_i) = \frac{1}{4} (0 - 2 + 0 - 2.5 + 0 - 3.5 + 0 - 5) = -3.25
     \]

   - Para \( \theta_1 \):

     \[
     \frac{\partial J}{\partial \theta_1} = \frac{1}{4} \sum_{i=1}^{4} (\hat{y}_i - y_i) x_i = \frac{1}{4} ((0 - 2) \times 1 + (0 - 2.5) \times 2 + (0 - 3.5) \times 3 + (0 - 5) \times 4) = -10.25
     \]

3. **Actualizamos los parámetros:**

   - \( \theta_0 := 0 - 0.01 \times (-3.25) = 0.0325 \)
   - \( \theta_1 := 0 - 0.01 \times (-10.25) = 0.1025 \)

¡Claro! Continuaremos con **Iteración 2** del algoritmo de descenso por gradiente para que entiendas cómo funciona el proceso paso a paso.

---

## **Iteración 2**

### **Paso 1: Calculamos las predicciones \(\hat{y}_i\)**

Usamos los nuevos valores de los parámetros:

- \( \theta_0 = 0.0325 \)
- \( \theta_1 = 0.1025 \)

Calculamos las predicciones para cada ejemplo:

1. Para \( x_1 = 1 \):

   \[
   \hat{y}_1 = \theta_0 + \theta_1 x_1 = 0.0325 + 0.1025 \times 1 = 0.135
   \]

2. Para \( x_2 = 2 \):

   \[
   \hat{y}_2 = \theta_0 + \theta_1 x_2 = 0.0325 + 0.1025 \times 2 = 0.2375
   \]

3. Para \( x_3 = 3 \):

   \[
   \hat{y}_3 = \theta_0 + \theta_1 x_3 = 0.0325 + 0.1025 \times 3 = 0.34
   \]

4. Para \( x_4 = 4 \):

   \[
   \hat{y}_4 = \theta_0 + \theta_1 x_4 = 0.0325 + 0.1025 \times 4 = 0.4425
   \]

### **Paso 2: Calculamos los errores \(\hat{y}_i - y_i\)**

1. Para \( i = 1 \):

   \[
   \hat{y}_1 - y_1 = 0.135 - 2 = -1.865
   \]

2. Para \( i = 2 \):

   \[
   \hat{y}_2 - y_2 = 0.2375 - 2.5 = -2.2625
   \]

3. Para \( i = 3 \):

   \[
   \hat{y}_3 - y_3 = 0.34 - 3.5 = -3.16
   \]

4. Para \( i = 4 \):

   \[
   \hat{y}_4 - y_4 = 0.4425 - 5 = -4.5575
   \]

### **Paso 3: Calculamos las derivadas parciales**

**Para \( \theta_0 \):**

\[
\frac{\partial J}{\partial \theta_0} = \frac{1}{m} \sum_{i=1}^{m} (\hat{y}_i - y_i)
\]

Calculamos la suma:

\[
\sum_{i=1}^{4} (\hat{y}_i - y_i) = (-1.865) + (-2.2625) + (-3.16) + (-4.5575) = -11.845
\]

Entonces:

\[
\frac{\partial J}{\partial \theta_0} = \frac{1}{4} (-11.845) = -2.96125
\]

**Para \( \theta_1 \):**

\[
\frac{\partial J}{\partial \theta_1} = \frac{1}{m} \sum_{i=1}^{m} (\hat{y}_i - y_i) x_i
\]

Calculamos cada término:

1. \( (\hat{y}_1 - y_1) x_1 = (-1.865) \times 1 = -1.865 \)
2. \( (\hat{y}_2 - y_2) x_2 = (-2.2625) \times 2 = -4.525 \)
3. \( (\hat{y}_3 - y_3) x_3 = (-3.16) \times 3 = -9.48 \)
4. \( (\hat{y}_4 - y_4) x_4 = (-4.5575) \times 4 = -18.23 \)

Sumamos los términos:

\[
\sum_{i=1}^{4} (\hat{y}_i - y_i) x_i = -1.865 - 4.525 - 9.48 - 18.23 = -34.1
\]

Entonces:

\[
\frac{\partial J}{\partial \theta_1} = \frac{1}{4} (-34.1) = -8.525
\]

### **Paso 4: Actualizamos los parámetros**

Usamos la regla de actualización:

\[
\theta_j := \theta_j - \alpha \frac{\partial J}{\partial \theta_j}
\]

- **Para \( \theta_0 \):**

  \[
  \theta_0 := 0.0325 - 0.01 \times (-2.96125) = 0.0325 + 0.0296125 = 0.0621125
  \]

- **Para \( \theta_1 \):**

  \[
  \theta_1 := 0.1025 - 0.01 \times (-8.525) = 0.1025 + 0.08525 = 0.18775
  \]

### **Paso 5: Calculamos el costo \( J(\theta_0, \theta_1) \)**

La función de costo es:

\[
J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=1}^{m} (\hat{y}_i - y_i)^2
\]

Calculamos cada término:

1. \( (\hat{y}_1 - y_1)^2 = (-1.865)^2 = 3.480225 \)
2. \( (\hat{y}_2 - y_2)^2 = (-2.2625)^2 = 5.12025625 \)
3. \( (\hat{y}_3 - y_3)^2 = (-3.16)^2 = 9.9856 \)
4. \( (\hat{y}_4 - y_4)^2 = (-4.5575)^2 = 20.76630625 \)

Sumamos:

\[
\sum_{i=1}^{4} (\hat{y}_i - y_i)^2 = 3.480225 + 5.12025625 + 9.9856 + 20.76630625 = 39.3523875
\]

Entonces:

\[
J(\theta_0, \theta_1) = \frac{1}{8} \times 39.3523875 = 4.9190484375
\]

---

## **Iteración 3**

### **Paso 1: Calculamos las predicciones \(\hat{y}_i\)**

Usamos los nuevos valores de los parámetros:

- \( \theta_0 = 0.0621125 \)
- \( \theta_1 = 0.18775 \)

Calculamos las predicciones para cada ejemplo:

1. Para \( x_1 = 1 \):

   \[
   \hat{y}_1 = 0.0621125 + 0.18775 \times 1 = 0.2498625
   \]

2. Para \( x_2 = 2 \):

   \[
   \hat{y}_2 = 0.0621125 + 0.18775 \times 2 = 0.4376125
   \]

3. Para \( x_3 = 3 \):

   \[
   \hat{y}_3 = 0.0621125 + 0.18775 \times 3 = 0.6253625
   \]

4. Para \( x_4 = 4 \):

   \[
   \hat{y}_4 = 0.0621125 + 0.18775 \times 4 = 0.8131125
   \]

### **Paso 2: Calculamos los errores \(\hat{y}_i - y_i\)**

1. Para \( i = 1 \):

   \[
   \hat{y}_1 - y_1 = 0.2498625 - 2 = -1.7501375
   \]

2. Para \( i = 2 \):

   \[
   \hat{y}_2 - y_2 = 0.4376125 - 2.5 = -2.0623875
   \]

3. Para \( i = 3 \):

   \[
   \hat{y}_3 - y_3 = 0.6253625 - 3.5 = -2.8746375
   \]

4. Para \( i = 4 \):

   \[
   \hat{y}_4 - y_4 = 0.8131125 - 5 = -4.1868875
   \]

### **Paso 3: Calculamos las derivadas parciales**

**Para \( \theta_0 \):**

\[
\sum_{i=1}^{4} (\hat{y}_i - y_i) = (-1.7501375) + (-2.0623875) + (-2.8746375) + (-4.1868875) = -10.87305
\]

Entonces:

\[
\frac{\partial J}{\partial \theta_0} = \frac{1}{4} (-10.87305) = -2.7182625
\]

**Para \( \theta_1 \):**

Calculamos cada término:

1. \( (-1.7501375) \times 1 = -1.7501375 \)
2. \( (-2.0623875) \times 2 = -4.124775 \)
3. \( (-2.8746375) \times 3 = -8.6239125 \)
4. \( (-4.1868875) \times 4 = -16.74755 \)

Sumamos:

\[
\sum_{i=1}^{4} (\hat{y}_i - y_i) x_i = -1.7501375 - 4.124775 - 8.6239125 - 16.74755 = -31.246375
\]

Entonces:

\[
\frac{\partial J}{\partial \theta_1} = \frac{1}{4} (-31.246375) = -7.81159375
\]

### **Paso 4: Actualizamos los parámetros**

- **Para \( \theta_0 \):**

  \[
  \theta_0 := 0.0621125 - 0.01 \times (-2.7182625) = 0.0621125 + 0.027182625 = 0.089295125
  \]

- **Para \( \theta_1 \):**

  \[
  \theta_1 := 0.18775 - 0.01 \times (-7.81159375) = 0.18775 + 0.0781159375 = 0.2658659375
  \]

### **Paso 5: Calculamos el costo \( J(\theta_0, \theta_1) \)**

Calculamos cada término:

1. \( (\hat{y}_1 - y_1)^2 = (-1.7501375)^2 = 3.062981
2. \( (\hat{y}_2 - y_2)^2 = (-2.0623875)^2 = 4.256453
3. \( (\hat{y}_3 - y_3)^2 = (-2.8746375)^2 = 8.263549
4. \( (\hat{y}_4 - y_4)^2 = (-4.1868875)^2 = 17.534061

Sumamos:

\[
\sum_{i=1}^{4} (\hat{y}_i - y_i)^2 = 3.062981 + 4.256453 + 8.263549 + 17.534061 = 33.116995
\]

Entonces:

\[
J(\theta_0, \theta_1) = \frac{1}{8} \times 33.116995 = 4.139624375
\]

---

## **Observaciones**

- **Disminución del costo:** Notamos que el costo \( J \) disminuye en cada iteración:

  - Iteración 1: \( J = 5.9375 \) (calculado previamente)
  - Iteración 2: \( J = 4.9190484375 \)
  - Iteración 3: \( J = 4.139624375 \)

- **Actualización de parámetros:** Los valores de \( \theta_0 \) y \( \theta_1 \) se ajustan en cada iteración para reducir el error.

- **Convergencia:** Continuando con más iteraciones, los parámetros convergerán hacia los valores óptimos que minimizan el costo.


## 2. Importancia de la Regresión Lineal en el Contexto de las Redes Neuronales

La regresión lineal es fundamental por varias razones:

- **Comprensión de la Optimización**: Introduce el concepto de minimizar una función de costo ajustando los parámetros del modelo.
- **Aplicación de Derivadas**: Demuestra cómo calcular derivadas para encontrar la dirección de descenso más pronunciada en el espacio de parámetros.
- **Base para Modelos Más Complejos**: Los principios aprendidos se aplican directamente a modelos más avanzados, como las redes neuronales.
