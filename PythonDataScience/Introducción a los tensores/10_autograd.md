
### Derivadas y Optimización: Concepto de Límite

La derivada de una función mide la **tasa de cambio** de una variable respecto a otra. Matemáticamente, la derivada \( f'(x) \) de una función \( f(x) \) se define como el **límite**:

\[
f'(x) = \lim_{\Delta x \to 0} \frac{f(x + \Delta x) - f(x)}{\Delta x}
\]

El concepto de límite en el cálculo de derivadas es esencial para entender cómo pequeñas variaciones en una variable afectan el valor de una función. En **optimización**, este cambio (o gradiente) indica cómo modificar las variables para **minimizar** (o maximizar) el valor de una función de costo, como el **Error Cuadrático Medio (MSE)** o la **Entropía Cruzada**.

Cuando optimizamos una función, queremos encontrar los valores de las variables que hacen que la función alcance su mínimo o máximo. Para ello, calculamos las **derivadas parciales** de la función respecto a cada variable y usamos el gradiente, un vector de todas estas derivadas parciales, para guiar el ajuste de las variables.

---

### Derivadas Parciales y Gradiente de Funciones de Costo Comunes

Veamos cómo calcular las derivadas parciales de las funciones **MSE** y **Entropía Cruzada** y cómo esto se relaciona con el gradiente.

#### 1. Error Cuadrático Medio (MSE)

El **Error Cuadrático Medio** mide la diferencia entre los valores predichos \( \hat{y} \) y los valores reales \( y \) y está definido como:

\[
\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (\hat{y}_i - y_i)^2
\]

Para optimizar MSE, calculamos la derivada parcial de MSE respecto a \( \hat{y}_i \):

\[
\frac{\partial \text{MSE}}{\partial \hat{y}_i} = \frac{2}{n} (\hat{y}_i - y_i)
\]

El gradiente de MSE respecto a las predicciones nos da la dirección en la que debemos ajustar las predicciones para minimizar el error. Este cálculo indica cómo cambiar cada \( \hat{y}_i \) para reducir el MSE.

#### 2. Entropía Cruzada

La **Entropía Cruzada** se usa típicamente en problemas de clasificación y está definida como:

\[
\text{Entropía Cruzada} = -\sum_{i=1}^{n} y_i \log(\hat{y}_i)
\]

La derivada parcial de la Entropía Cruzada respecto a \( \hat{y}_i \) (la predicción) es:

\[
\frac{\partial \text{Entropía Cruzada}}{\partial \hat{y}_i} = -\frac{y_i}{\hat{y}_i}
\]

Este gradiente muestra cómo ajustar cada \( \hat{y}_i \) para minimizar la Entropía Cruzada, guiándonos en la dirección de cambio que reduce el error de clasificación.

---

### El Rol del Gradiente y `autograd` en PyTorch

En PyTorch, el módulo `autograd` permite calcular automáticamente estos gradientes mediante **retropropagación** (backward propagation) al construir un **grafo computacional** de las operaciones realizadas. Esto significa que PyTorch registra todas las operaciones en tensores con `requires_grad=True`, y al llamar a `backward()` sobre la función objetivo, PyTorch calcula automáticamente las derivadas parciales de la función respecto a cada tensor involucrado.

#### Ejemplo Práctico: Cálculo Automático de Derivadas Parciales con `autograd`

Veamos cómo aplicar `autograd` para calcular el gradiente en ejemplos prácticos.

---

### Ejemplos Prácticos

#### Ejemplo 1: Derivada Parcial del Error Cuadrático Medio (MSE)

Supongamos que tenemos un conjunto de valores predichos \( \hat{y} \) y valores reales \( y \), y queremos calcular el gradiente de MSE respecto a cada valor en \( \hat{y} \) para ver cómo ajustar nuestras predicciones.

1. Definimos los valores reales y las predicciones.
2. Calculamos MSE.
3. Usamos `backward()` para obtener la derivada de MSE respecto a \( \hat{y} \).

```python
# Valores reales y predicciones
y = torch.tensor([3.0, -0.5, 2.0, 7.0])
y_pred = torch.tensor([2.5, 0.0, 2.0, 8.0], requires_grad=True)

# Cálculo de MSE
mse = torch.mean((y_pred - y) ** 2)

# Derivada de MSE respecto a y_pred
mse.backward()

# Gradiente
print("Gradiente de MSE respecto a las predicciones y_pred:", y_pred.grad)
```

En este caso, PyTorch calcula automáticamente el gradiente de MSE respecto a cada valor en `y_pred`, dándonos la dirección en que debemos ajustar las predicciones para reducir el error cuadrático.

#### Ejemplo 2: Derivada Parcial de la Entropía Cruzada

Supongamos que estamos trabajando en un problema de clasificación binaria. Tenemos valores reales \( y \) (0 o 1) y probabilidades predichas \( \hat{y} \) de la clase positiva. Usaremos la entropía cruzada y `autograd` para calcular el gradiente de esta función de costo.

1. Definimos \( y \) y \( \hat{y} \) para cada observación.
2. Calculamos la entropía cruzada.
3. Usamos `backward()` para obtener la derivada parcial de la entropía cruzada respecto a \( \hat{y} \).

```python
# Valores reales y predicciones (probabilidades)
y = torch.tensor([1.0, 0.0, 1.0])
y_pred = torch.tensor([0.8, 0.4, 0.6], requires_grad=True)

# Cálculo de Entropía Cruzada
cross_entropy = -torch.sum(y * torch.log(y_pred) + (1 - y) * torch.log(1 - y_pred))

# Derivada de la Entropía Cruzada respecto a y_pred
cross_entropy.backward()

# Gradiente
print("Gradiente de Entropía Cruzada respecto a las predicciones y_pred:", y_pred.grad)
```

PyTorch calcula el gradiente de la entropía cruzada respecto a las predicciones. Estos gradientes indican cómo ajustar cada valor de \( \hat{y} \) para reducir el error de clasificación.

---

### Aplicaciones del Cálculo Automático de Gradientes con `autograd`

Sin entrar en redes neuronales, podemos aplicar estos cálculos automáticos de gradientes en otros contextos donde necesitamos optimizar funciones. A continuación, algunos ejemplos de derivadas parciales en contextos reales:

#### Ejemplo Aplicado 1: Velocidad y Aceleración

En un automóvil que acelera, la velocidad en función del tiempo podría estar modelada como \( v(t) = 4t^2 \). Para optimizar su rendimiento, podríamos querer calcular la **aceleración**, que es la derivada de la velocidad respecto al tiempo.

```python
# Tiempo como tensor
t = torch.tensor(5.0, requires_grad=True)

# Velocidad en función del tiempo
v = 4 * t**2

# Derivada de la velocidad respecto al tiempo (aceleración)
v.backward()

print("Aceleración en t=5:", t.grad)  # Aceleración calculada automáticamente
```

#### Ejemplo Aplicado 2: Energía Potencial y Fuerza

Consideremos la **energía potencial** de un objeto en función de su altura \( h \), como \( U(h) = m \cdot g \cdot h \), donde \( m \) es la masa y \( g \) es la gravedad. La **fuerza** ejercida sobre el objeto es la derivada de la energía potencial respecto a la altura.

```python
# Constantes
mass = 5.0
gravity = 9.8

# Altura como tensor
h = torch.tensor(15.0, requires_grad=True)

# Energía potencial en función de la altura
U = mass * gravity * h

# Derivada de U respecto a h (fuerza)
U.backward()

print("Fuerza en h=15 m:", h.grad)
```

---
