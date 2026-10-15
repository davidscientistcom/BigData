# Backpropagation en el Perceptrón Multicapa (MLP)

El **backpropagation** es el proceso de ajuste de pesos que permite a una red neuronal multicapa aprender de los datos, minimizando el error en sus predicciones. Este algoritmo se basa en dos fases principales: la **propagación hacia adelante** de los datos de entrada hasta la salida y la **retropropagación del error** hacia atrás, que ajusta los pesos para reducir el error total.

Para entenderlo, vamos a usar una red simple con:
- Una capa de entrada con valores de entrada \( X = [x_1, x_2] \).
- Una capa oculta con dos neuronas \( h_1 \) y \( h_2 \) con función de activación sigmoide.
- Una capa de salida con una neurona \( y \), también con función de activación sigmoide.
- Una salida deseada \( t \) que la red quiere aproximar.

### Paso 1: Propagación Hacia Adelante

1. **Entrada en la Capa Oculta**:
   - Cada neurona en la capa oculta calcula una **combinación ponderada** de sus entradas \( x_1 \) y \( x_2 \) a través de los pesos. Por ejemplo, la entrada total \( z_1 \) para la neurona \( h_1 \) es:
     \[
     z_1 = w_{11} \cdot x_1 + w_{21} \cdot x_2 + b_1
     \]
   - La salida \( h_1 \) de esta neurona se calcula aplicando la función sigmoide a \( z_1 \):
     \[
     h_1 = \sigma(z_1) = \frac{1}{1 + e^{-z_1}}
     \]
   - Esto se repite para \( h_2 \), con sus pesos y sesgo correspondientes.

2. **Entrada en la Capa de Salida**:
   - La neurona de salida toma como entrada las salidas \( h_1 \) y \( h_2 \) de la capa oculta. Calcula una combinación ponderada de estas entradas, por ejemplo:
     \[
     z_y = v_1 \cdot h_1 + v_2 \cdot h_2 + b_y
     \]
   - La salida final \( y \) de la red se calcula aplicando la función sigmoide a \( z_y \):
     \[
     y = \sigma(z_y) = \frac{1}{1 + e^{-z_y}}
     \]

3. **Cálculo del Error Total**:
   - Con la salida \( y \) calculada, se mide el error en función de la diferencia entre \( y \) y el valor deseado \( t \). Una función común de error es el **Error Cuadrático Medio (MSE)**:
     \[
     \text{Error} = \frac{1}{2} (y - t)^2
     \]
   - Este error total es lo que la red tratará de minimizar mediante ajustes en los pesos.

---

### Paso 2: Retropropagación del Error

Para reducir el error, necesitamos ajustar los pesos en cada capa. La retropropagación funciona distribuyendo el error desde la capa de salida hacia atrás, capa por capa, usando gradientes de las funciones de activación.

1. **Error y Gradiente en la Capa de Salida**:
   - El error de la capa de salida es la diferencia entre la salida de la red y el valor deseado \( t \).
   - La **derivada de la función de activación sigmoide** en la capa de salida ayuda a calcular cuánto contribuye cada peso al error. La derivada de la sigmoide \( \sigma(y) \) se expresa como:
     \[
     \sigma'(y) = y \cdot (1 - y)
     \]
   - El gradiente del error en la salida se calcula como:
     \[
     \delta_y = (y - t) \cdot y \cdot (1 - y)
     \]
   - Este gradiente muestra en qué dirección y magnitud deben ajustarse los pesos que conectan las neuronas de la capa oculta con la neurona de salida.

2. **Ajuste de Pesos en la Capa de Salida**:
   - Usamos el gradiente calculado para ajustar cada peso en la capa de salida. Si \( v_1 \) es el peso que conecta \( h_1 \) con \( y \), el ajuste de \( v_1 \) es:
     \[
     v_1 := v_1 - \eta \cdot \delta_y \cdot h_1
     \]
   - Este ajuste se realiza para todos los pesos en la capa de salida.

3. **Propagación del Error hacia la Capa Oculta**:
   - Cada neurona en la capa oculta recibe una "parte" del error de la capa de salida, ajustada por los pesos que conectan cada neurona oculta con la salida.
   - Por ejemplo, el error retropropagado en la neurona \( h_1 \) es:
     \[
     \delta_{h_1} = \delta_y \cdot v_1 \cdot h_1 \cdot (1 - h_1)
     \]
   - Aquí, \( h_1 \cdot (1 - h_1) \) es la derivada de la función de activación sigmoide en \( h_1 \). Esto se calcula para cada neurona en la capa oculta, distribuyendo el error de acuerdo con los pesos en la capa de salida.

4. **Ajuste de Pesos en la Capa Oculta**:
   - Finalmente, ajustamos los pesos que conectan las neuronas de entrada con las neuronas ocultas usando los gradientes calculados. Si \( w_{11} \) es el peso que conecta \( x_1 \) con \( h_1 \), el ajuste de \( w_{11} \) es:
     \[
     w_{11} := w_{11} - \eta \cdot \delta_{h_1} \cdot x_1
     \]
   - Esto se aplica a todos los pesos en la capa de entrada.

---

### Resumen del Proceso Completo de Backpropagation

1. **Propagación hacia adelante**:
   - Las entradas se procesan capa por capa hasta llegar a la salida.
   - Se calcula el error total comparando la salida predicha con la salida deseada.

2. **Retropropagación del error**:
   - El error se retropropaga desde la capa de salida hacia las capas anteriores, ajustando los pesos de acuerdo con el gradiente calculado en cada capa.

3. **Ajuste de pesos**:
   - Los pesos en cada capa se ajustan en la dirección que minimiza el error, usando un **factor de aprendizaje** \( \eta \) para controlar la magnitud del ajuste.

Este ciclo de **propagación hacia adelante y retropropagación** se repite en cada **época de entrenamiento** hasta que el error se reduce a un nivel aceptable. Este ajuste continuo de pesos permite que la red aprenda patrones complejos en los datos y mejore en sus predicciones.