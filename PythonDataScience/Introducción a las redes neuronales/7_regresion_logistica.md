# Regresión Logística: Un Análisis Detallado

## Introducción

La **regresión logística** es una técnica estadística utilizada para modelar la probabilidad de una variable de respuesta categórica, típicamente binaria (0 o 1). Es una herramienta fundamental en el aprendizaje automático para resolver problemas de clasificación.

En este capítulo, exploraremos en detalle:

- Por qué necesitamos la regresión logística.
- El modelo matemático de la regresión logística.
- La función de costo específica para la regresión logística.
- Derivación de las ecuaciones necesarias para entrenar el modelo.
- Implementación del algoritmo de descenso por gradiente.
- Un ejemplo numérico detallado para ilustrar el proceso.

---

## 1. Necesidad de la Regresión Logística

### 1.1. Limitaciones de la Regresión Lineal en Clasificación

La **regresión lineal** predice valores continuos y es adecuada para problemas de regresión. Sin embargo, cuando intentamos utilizarla para problemas de **clasificación binaria**, enfrenta varias limitaciones:

- **Salidas No Acotadas**: La regresión lineal puede producir predicciones fuera del rango [0,1], lo que no es interpretable como una probabilidad.
- **No Linealidad de la Frontera de Decisión**: En problemas donde la relación entre las características y la probabilidad de la clase es no lineal, la regresión lineal no es adecuada.

### 1.2. Solución: Regresión Logística

La **regresión logística** resuelve estos problemas al modelar la probabilidad de una clase utilizando la función sigmoide, que mapea cualquier valor real al rango (0,1).

---

## 2. Modelo de Regresión Logística

### 2.1. Función Sigmoide

La **función sigmoide** es una función matemática con forma de "S" definida como:

\[
\sigma(z) = \frac{1}{1 + e^{-z}}
\]

Características:

- Mapea cualquier valor real \( z \) al rango (0,1).
- Cuando \( z = 0 \), \( \sigma(0) = 0.5 \).
- A medida que \( z \rightarrow \infty \), \( \sigma(z) \rightarrow 1 \).
- A medida que \( z \rightarrow -\infty \), \( \sigma(z) \rightarrow 0 \).

### 2.2. Modelo Matemático

En la regresión logística, modelamos la **probabilidad** de que la variable de respuesta \( y \) sea 1 dado \( x \):

\[
P(y = 1 \mid x) = h_\theta(x) = \sigma(z) = \sigma(\theta^T x) = \frac{1}{1 + e^{-\theta^T x}}
\]

Donde:

- \( \theta \) es el vector de parámetros (incluyendo el término de sesgo).
- \( x \) es el vector de características (incluyendo un 1 para el término de sesgo).

### 2.3. Interpretación

La salida de \( h_\theta(x) \) es una probabilidad entre 0 y 1. Podemos clasificar una observación en:

- **Clase 1** si \( h_\theta(x) \geq 0.5 \).
- **Clase 0** si \( h_\theta(x) < 0.5 \).

---

## 3. Función de Costo en Regresión Logística

### 3.1. Necesidad de una Función de Costo Adecuada

La función de costo de **error cuadrático medio** utilizada en regresión lineal no es adecuada para la regresión logística debido a que la función sigmoide es no lineal y puede causar problemas de convergencia.

### 3.2. Función de Costo: Entropía Cruzada

Utilizamos la **entropía cruzada** o **función de costo logística**, definida como:

\[
J(\theta) = -\frac{1}{m} \sum_{i=1}^{m} \left[ y^{(i)} \log(h_\theta(x^{(i)})) + (1 - y^{(i)}) \log(1 - h_\theta(x^{(i)})) \right]
\]

Donde:

- \( m \) es el número de ejemplos en el conjunto de datos.
- \( y^{(i)} \) es el valor real de la variable de respuesta para el ejemplo \( i \).
- \( h_\theta(x^{(i)}) \) es la predicción del modelo para el ejemplo \( i \).

### 3.3. Interpretación de la Función de Costo

La función de costo penaliza fuertemente las predicciones incorrectas:

- Si \( y^{(i)} = 1 \) y \( h_\theta(x^{(i)}) \) es cercano a 0, el costo tiende a infinito.
- Si \( y^{(i)} = 0 \) y \( h_\theta(x^{(i)}) \) es cercano a 1, el costo tiende a infinito.

---

## 4. Derivación de las Ecuaciones para el Entrenamiento

### 4.1. Objetivo: Minimizar la Función de Costo

Queremos encontrar los valores óptimos de \( \theta \) que minimizan \( J(\theta) \).

### 4.2. Cálculo del Gradiente

Necesitamos calcular el **gradiente** de la función de costo respecto a \( \theta \):

\[
\frac{\partial J(\theta)}{\partial \theta_j}
\]

### 4.3. Derivación Paso a Paso

#### 4.3.1. Expandiendo la Función de Costo

Para un solo ejemplo, la función de costo es:

\[
J^{(i)}(\theta) = - \left[ y^{(i)} \log(h_\theta(x^{(i)})) + (1 - y^{(i)}) \log(1 - h_\theta(x^{(i)})) \right]
\]

Nuestro objetivo es calcular:

\[
\frac{\partial J^{(i)}(\theta)}{\partial \theta_j}
\]

#### 4.3.2. Aplicando la Regla de la Cadena

1. **Derivada de \( J^{(i)} \) respecto a \( h_\theta(x^{(i)}) \):**

\[
\frac{\partial J^{(i)}}{\partial h_\theta(x^{(i)})} = -\left( \frac{y^{(i)}}{h_\theta(x^{(i)})} - \frac{1 - y^{(i)}}{1 - h_\theta(x^{(i)})} \right)
\]

2. **Derivada de \( h_\theta(x^{(i)}) \) respecto a \( z^{(i)} \):**

Recordemos que:

\[
h_\theta(x^{(i)}) = \sigma(z^{(i)}) \quad \text{donde} \quad z^{(i)} = \theta^T x^{(i)}
\]

La derivada de la función sigmoide es:

\[
\frac{d\sigma(z)}{dz} = \sigma(z)(1 - \sigma(z))
\]

Por lo tanto:

\[
\frac{\partial h_\theta(x^{(i)})}{\partial z^{(i)}} = h_\theta(x^{(i)})(1 - h_\theta(x^{(i)}))
\]

3. **Derivada de \( z^{(i)} \) respecto a \( \theta_j \):**

\[
\frac{\partial z^{(i)}}{\partial \theta_j} = x_j^{(i)}
\]

#### 4.3.3. Combinando las Derivadas

Aplicamos la regla de la cadena:

\[
\frac{\partial J^{(i)}}{\partial \theta_j} = \frac{\partial J^{(i)}}{\partial h_\theta(x^{(i)})} \cdot \frac{\partial h_\theta(x^{(i)})}{\partial z^{(i)}} \cdot \frac{\partial z^{(i)}}{\partial \theta_j}
\]

Sustituyendo:

\[
\frac{\partial J^{(i)}}{\partial \theta_j} = \left( -\frac{y^{(i)}}{h_\theta(x^{(i)})} + \frac{1 - y^{(i)}}{1 - h_\theta(x^{(i)})} \right) \cdot h_\theta(x^{(i)})(1 - h_\theta(x^{(i)})) \cdot x_j^{(i)}
\]

Simplificando:

Observemos que:

\[
\left( -\frac{y}{h} + \frac{1 - y}{1 - h} \right) h (1 - h) = (h - y)
\]

Demostración:

\[
\begin{align*}
\left( -\frac{y}{h} + \frac{1 - y}{1 - h} \right) h (1 - h) &= \left( -\frac{y}{h} + \frac{1 - y}{1 - h} \right) h (1 - h) \\
&= \left( - y \frac{1 - h}{h} + (1 - y) \frac{h}{1 - h} \right) \\
&= \left( - y \left( \frac{1 - h}{h} \right) + (1 - y) \left( \frac{h}{1 - h} \right) \right) \\
&= - y \left( \frac{1 - h}{h} \right) + (1 - y) \left( \frac{h}{1 - h} \right) \\
\end{align*}
\]

Multiplicando y simplificando se llega a:

\[
(h - y)
\]

Por lo tanto:

\[
\frac{\partial J^{(i)}}{\partial \theta_j} = \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_j^{(i)}
\]

#### 4.3.4. Gradiente Total

Sumando sobre todos los ejemplos:

\[
\frac{\partial J(\theta)}{\partial \theta_j} = \frac{1}{m} \sum_{i=1}^{m} \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_j^{(i)}
\]

---

## 5. Algoritmo de Descenso por Gradiente

### 5.1. Regla de Actualización

Usamos el **descenso por gradiente** para actualizar los parámetros:

\[
\theta_j := \theta_j - \alpha \frac{\partial J(\theta)}{\partial \theta_j}
\]

Donde:

- \( \alpha \) es la tasa de aprendizaje.
- \( \theta_j \) es el \( j \)-ésimo parámetro.

### 5.2. Vectorización

Para eficiencia, especialmente con grandes conjuntos de datos y múltiples características, es útil utilizar la notación vectorial:

\[
\theta := \theta - \alpha \nabla J(\theta)
\]

Donde:

- \( \nabla J(\theta) \) es el gradiente vectorial de la función de costo.

---

## 6. Ejemplo Numérico Detallado

### 6.1. Conjunto de Datos

Supongamos que tenemos el siguiente conjunto de datos:

| \( x_0 \) | \( x_1 \) | \( y \) |
|-----------|-----------|---------|
| 1         | 0.5       | 0       |
| 1         | 2.0       | 0       |
| 1         | 1.0       | 0       |
| 1         | 3.0       | 1       |
| 1         | 4.0       | 1       |
| 1         | 5.0       | 1       |

Notas:

- Incluimos \( x_0 = 1 \) para el término de sesgo (\( \theta_0 \)).
- \( x_1 \) es la característica.
- \( y \) es la variable de respuesta (0 o 1).

### 6.2. Inicialización

- Parámetros iniciales:

  \[
  \theta_0 = 0, \quad \theta_1 = 0
  \]

- Tasa de aprendizaje:

  \[
  \alpha = 0.1
  \]

- Número de ejemplos:

  \[
  m = 6
  \]

### 6.3. Iteración 1

#### 6.3.1. Propagación Hacia Adelante

Calculamos \( z^{(i)} \) y \( h_\theta(x^{(i)}) \) para cada ejemplo:

Para cada ejemplo \( i \):

1. \( z^{(i)} = \theta_0 x_0^{(i)} + \theta_1 x_1^{(i)} \)
2. \( h_\theta(x^{(i)}) = \sigma(z^{(i)}) \)

Con \( \theta_0 = 0 \) y \( \theta_1 = 0 \):

- \( z^{(i)} = 0 \)
- \( h_\theta(x^{(i)}) = \sigma(0) = 0.5 \)

#### 6.3.2. Cálculo del Error

Para cada ejemplo \( i \):

\[
\text{Error}^{(i)} = h_\theta(x^{(i)}) - y^{(i)}
\]

Calculamos:

1. Para \( i = 1 \):

   \[
   \text{Error}^{(1)} = 0.5 - 0 = 0.5
   \]

2. Para \( i = 2 \):

   \[
   \text{Error}^{(2)} = 0.5 - 0 = 0.5
   \]

3. Para \( i = 3 \):

   \[
   \text{Error}^{(3)} = 0.5 - 0 = 0.5
   \]

4. Para \( i = 4 \):

   \[
   \text{Error}^{(4)} = 0.5 - 1 = -0.5
   \]

5. Para \( i = 5 \):

   \[
   \text{Error}^{(5)} = 0.5 - 1 = -0.5
   \]

6. Para \( i = 6 \):

   \[
   \text{Error}^{(6)} = 0.5 - 1 = -0.5
   \]

#### 6.3.3. Cálculo del Gradiente

Calculamos las derivadas parciales:

1. **Para \( \theta_0 \):**

   \[
   \frac{\partial J}{\partial \theta_0} = \frac{1}{m} \sum_{i=1}^{m} \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_0^{(i)}
   \]

   Dado que \( x_0^{(i)} = 1 \) para todos los \( i \):

   \[
   \frac{\partial J}{\partial \theta_0} = \frac{1}{6} \left( 0.5 + 0.5 + 0.5 - 0.5 - 0.5 - 0.5 \right) = \frac{1}{6} (0) = 0
   \]

2. **Para \( \theta_1 \):**

   \[
   \frac{\partial J}{\partial \theta_1} = \frac{1}{m} \sum_{i=1}^{m} \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_1^{(i)}
   \]

   Calculamos cada término:

   - \( (0.5 - 0) \times 0.5 = 0.25 \)
   - \( (0.5 - 0) \times 2.0 = 1.0 \)
   - \( (0.5 - 0) \times 1.0 = 0.5 \)
   - \( (-0.5) \times 3.0 = -1.5 \)
   - \( (-0.5) \times 4.0 = -2.0 \)
   - \( (-0.5) \times 5.0 = -2.5 \)

   Sumamos:

   \[
   \sum_{i=1}^{6} \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_1^{(i)} = 0.25 + 1.0 + 0.5 -1.5 -2.0 -2.5 = -4.25
   \]

   Entonces:

   \[
   \frac{\partial J}{\partial \theta_1} = \frac{1}{6} (-4.25) \approx -0.7083
   \]

#### 6.3.4. Actualización de Parámetros

1. **Para \( \theta_0 \):**

   \[
   \theta_0 := \theta_0 - \alpha \frac{\partial J}{\partial \theta_0} = 0 - 0.1 \times 0 = 0
   \]

2. **Para \( \theta_1 \):**

   \[
   \theta_1 := \theta_1 - \alpha \frac{\partial J}{\partial \theta_1} = 0 - 0.1 \times (-0.7083) = 0.07083
   \]

### 6.4. Iteración 2

#### 6.4.1. Propagación Hacia Adelante

Con los nuevos parámetros:

- \( \theta_0 = 0 \)
- \( \theta_1 = 0.07083 \)

Calculamos \( z^{(i)} \) y \( h_\theta(x^{(i)}) \):

1. \( z^{(1)} = 0 + 0.07083 \times 0.5 = 0.035415 \)
2. \( z^{(2)} = 0 + 0.07083 \times 2.0 = 0.14166 \)
3. \( z^{(3)} = 0 + 0.07083 \times 1.0 = 0.07083 \)
4. \( z^{(4)} = 0 + 0.07083 \times 3.0 = 0.21249 \)
5. \( z^{(5)} = 0 + 0.07083 \times 4.0 = 0.28332 \)
6. \( z^{(6)} = 0 + 0.07083 \times 5.0 = 0.35415 \)

Calculamos \( h_\theta(x^{(i)}) = \sigma(z^{(i)}) \):

1. \( h_\theta(x^{(1)}) = \sigma(0.035415) \approx 0.508853 \)
2. \( h_\theta(x^{(2)}) = \sigma(0.14166) \approx 0.535356 \)
3. \( h_\theta(x^{(3)}) = \sigma(0.07083) \approx 0.517700 \)
4. \( h_\theta(x^{(4)}) = \sigma(0.21249) \approx 0.552928 \)
5. \( h_\theta(x^{(5)}) = \sigma(0.28332) \approx 0.570364 \)
6. \( h_\theta(x^{(6)}) = \sigma(0.35415) \approx 0.587658 \)

#### 6.4.2. Cálculo del Error

Calculamos \( h_\theta(x^{(i)}) - y^{(i)} \):

1. \( \text{Error}^{(1)} = 0.508853 - 0 = 0.508853 \)
2. \( \text{Error}^{(2)} = 0.535356 - 0 = 0.535356 \)
3. \( \text{Error}^{(3)} = 0.517700 - 0 = 0.517700 \)
4. \( \text{Error}^{(4)} = 0.552928 - 1 = -0.447072 \)
5. \( \text{Error}^{(5)} = 0.570364 - 1 = -0.429636 \)
6. \( \text{Error}^{(6)} = 0.587658 - 1 = -0.412342 \)

#### 6.4.3. Cálculo del Gradiente

**Para \( \theta_0 \):**

\[
\frac{\partial J}{\partial \theta_0} = \frac{1}{6} \left( 0.508853 + 0.535356 + 0.517700 - 0.447072 - 0.429636 - 0.412342 \right)
\]

Sumamos:

\[
\text{Suma} = 0.508853 + 0.535356 + 0.517700 - 0.447072 - 0.429636 - 0.412342 = 0.273859
\]

Entonces:

\[
\frac{\partial J}{\partial \theta_0} = \frac{1}{6} (0.273859) \approx 0.045643
\]

**Para \( \theta_1 \):**

Calculamos cada término:

1. \( 0.508853 \times 0.5 = 0.254427 \)
2. \( 0.535356 \times 2.0 = 1.070712 \)
3. \( 0.517700 \times 1.0 = 0.517700 \)
4. \( (-0.447072) \times 3.0 = -1.341216 \)
5. \( (-0.429636) \times 4.0 = -1.718544 \)
6. \( (-0.412342) \times 5.0 = -2.061710 \)

Sumamos:

\[
\text{Suma} = 0.254427 + 1.070712 + 0.517700 - 1.341216 - 1.718544 - 2.061710 = -3.278631
\]

Entonces:

\[
\frac{\partial J}{\partial \theta_1} = \frac{1}{6} (-3.278631) \approx -0.546438
\]

#### 6.4.4. Actualización de Parámetros

1. **Para \( \theta_0 \):**

   \[
   \theta_0 := \theta_0 - \alpha \frac{\partial J}{\partial \theta_0} = 0 - 0.1 \times 0.045643 = -0.0045643
   \]

2. **Para \( \theta_1 \):**

   \[
   \theta_1 := \theta_1 - \alpha \frac{\partial J}{\partial \theta_1} = 0.07083 - 0.1 \times (-0.546438) = 0.07083 + 0.0546438 = 0.1254738
   \]

### 6.5. Observaciones

- Vemos que los parámetros se actualizan en cada iteración para minimizar el costo.
- Podemos continuar con más iteraciones hasta que los parámetros converjan.

---

## 7. Implementación General del Algoritmo

### 7.1. Pseudocódigo

```
Inicializar θ con valores ceros o aleatorios pequeños
Repetir hasta la convergencia:
    Para cada ejemplo i:
        Calcular z^{(i)} = θ^T x^{(i)}
        Calcular h_θ(x^{(i)}) = σ(z^{(i)})
        Calcular error^{(i)} = h_θ(x^{(i)}) - y^{(i)}
    Calcular gradiente:
        Para cada θ_j:
            θ_j := θ_j - α * (1/m) * Σ_{i=1}^m error^{(i)} * x_j^{(i)}
```

### 7.2. Consideraciones Prácticas

- **Tasa de Aprendizaje (\( \alpha \))**: Elegir un valor adecuado es crucial. Si es demasiado grande, el algoritmo puede divergir; si es demasiado pequeño, la convergencia será lenta.
- **Número de Iteraciones**: Determinado por la convergencia del costo o un número máximo predefinido.
- **Regularización**: Puede ser necesario para evitar el sobreajuste, especialmente con muchas características.

---

## 8. Conclusión

La regresión logística es una herramienta esencial para problemas de clasificación binaria. A través de la función sigmoide y la función de costo de entropía cruzada, podemos modelar y predecir probabilidades de clase. El descenso por gradiente nos permite ajustar los parámetros del modelo para minimizar el error y mejorar las predicciones.
