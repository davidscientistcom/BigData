# Guía Completa: Creación de Redes Neuronales en PyTorch para Clasificación

## Introducción

Esta guía te enseñará a construir redes neuronales en PyTorch desde cero, explicando cada decisión y concepto . Está diseñada para estudiantes que conocen la teoría pero realizan su primera implementación práctica.

## 1. Fundamentos: Arquitectura de una Red Neuronal de Clasificación

### 1.1 Componentes Esenciales

Antes de programar, debemos entender los componentes clave de una red neuronal para clasificación :

| Componente | Clasificación Binaria | Clasificación Multiclase |
|------------|----------------------|--------------------------|
| **Capa de entrada** | Número de características (ej: 2 para coordenadas X,Y) | Igual |
| **Capas ocultas** | Mínimo 1, máximo ilimitado (específico del problema) | Igual |
| **Neuronas por capa** | Generalmente 10-512 (hiperparámetro ajustable) | Igual |
| **Capa de salida** | 1 neurona (clase 0 o 1) | 1 neurona por clase |
| **Activación oculta** | ReLU (más común) | ReLU |
| **Activación salida** | Sigmoid | Softmax |
| **Función de pérdida** | BCEWithLogitsLoss | CrossEntropyLoss |
| **Optimizador** | SGD o Adam | SGD o Adam |

### 1.2 ¿Por qué esta arquitectura?

**Capa de entrada**: Debe coincidir exactamente con el número de características de tus datos. Si tienes 2 features, necesitas 2 neuronas de entrada .

**Capas ocultas**: Permiten al modelo aprender patrones complejos. Cada capa adicional aumenta la capacidad de aprendizaje .

**Neuronas por capa**: Más neuronas = mayor capacidad de aprendizaje, pero también mayor riesgo de sobreajuste. Es un equilibrio .

## 2. Preparación de Datos

### 2.1 Creación de Datos de Ejemplo

```python
from sklearn.datasets import make_circles
import torch

# Crear datos circulares (problema de clasificación binaria)
n_samples = 1000
X, y = make_circles(n_samples, 
                    noise=0.03,  # Ruido para realismo
                    random_state=42)  # Reproducibilidad
```

**¿Por qué estos parámetros?** 
- `n_samples=1000`: Suficientes datos para entrenar sin ser excesivo
- `noise=0.03`: Añade realismo; datos reales nunca son perfectos
- `random_state=42`: Garantiza que obtengas los mismos datos cada vez (reproducibilidad científica)

### 2.2 Conversión a Tensores

```python
# Convertir NumPy arrays a tensores de PyTorch
X = torch.from_numpy(X).type(torch.float)
y = torch.from_numpy(y).type(torch.float)
```

**¿Por qué convertir a float?** PyTorch requiere `torch.float` para operaciones de entrenamiento; usar otros tipos causa errores .

### 2.3 División Train/Test

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,  # 80% entrenamiento, 20% test
    random_state=42
)
```

**¿Por qué 80/20?** Es el estándar en ML: suficientes datos para entrenar y suficientes para validar .

## 3. Configuración del Dispositivo (CPU/GPU)

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {device}")

# Mover datos al dispositivo
X_train = X_train.to(device)
y_train = y_train.to(device)
X_test = X_test.to(device)
y_test = y_test.to(device)
```

**¿Por qué esto?** Las GPUs aceleran enormemente el entrenamiento. Este código detecta automáticamente si tienes GPU disponible .

## 4. Construcción del Modelo

### 4.1 Método 1: Subclasificando nn.Module

```python
import torch.nn as nn

class ModeloClasificacion(nn.Module):
    def __init__(self):
        super().__init__()
        # Definir capas
        self.layer_1 = nn.Linear(in_features=2, out_features=10)
        self.layer_2 = nn.Linear(in_features=10, out_features=10)
        self.layer_3 = nn.Linear(in_features=10, out_features=1)
    
    def forward(self, x):
        # Definir el flujo de datos
        return self.layer_3(self.layer_2(self.layer_1(x)))

# Crear instancia y mover a dispositivo
model = ModeloClasificacion().to(device)
```

**Explicación detallada** :

1. **`nn.Linear(in_features=2, out_features=10)`**:
   - `in_features=2`: Entrada de 2 características (nuestras coordenadas X,Y)
   - `out_features=10`: Salida de 10 valores (10 neuronas ocultas)
   - Internamente calcula: y = x · W^T + b

2. **Segunda capa `nn.Linear(in_features=10, out_features=10)`**:
   - Debe tomar las 10 salidas de la capa anterior
   - Produce otras 10 características
   - Aumenta capacidad de aprendizaje

3. **Capa de salida `nn.Linear(in_features=10, out_features=1)`**:
   - `out_features=1`: Una sola salida para clasificación binaria
   - El valor indica probabilidad de pertenecer a clase 1

4. **Método `forward()`**:
   - Define cómo fluyen los datos a través del modelo
   - Los datos pasan secuencialmente: capa_1 → capa_2 → capa_3

### 4.2 Método 2: Usando nn.Sequential (Más Simple)

```python
model = nn.Sequential(
    nn.Linear(in_features=2, out_features=10),
    nn.Linear(in_features=10, out_features=10),
    nn.Linear(in_features=10, out_features=1)
).to(device)
```

**¿Cuándo usar cada método?** 
- **nn.Sequential**: Para arquitecturas simples y secuenciales
- **Subclasificar nn.Module**: Para arquitecturas complejas con flujos no secuenciales, conexiones residuales, etc.

### 4.3 ¿Por qué 10 neuronas ocultas?

Es un hiperparámetro ajustable :
- Datos simples (como círculos): 5-20 neuronas suelen ser suficientes
- Datos complejos (imágenes): 128-512 neuronas o más
- Regla práctica: Empieza pequeño, incrementa si el modelo no aprende

## 5. Función de Pérdida (Loss Function)

```python
loss_fn = nn.BCEWithLogitsLoss()
```

### 5.1 ¿Por qué BCEWithLogitsLoss?

**BCE = Binary Cross Entropy** :
- Diseñada específicamente para clasificación binaria
- Mide qué tan incorrectas son las predicciones del modelo
- Valores más altos = predicciones peores

**¿Por qué "WithLogits"?** :
- Los "logits" son las salidas crudas del modelo (valores sin procesar)
- Esta función incluye la activación sigmoid internamente
- Es **numéricamente más estable** que aplicar sigmoid + BCELoss por separado
- Evita problemas de precisión numérica

### 5.2 Alternativa (NO recomendada)

```python
# NO USAR: Menos estable numéricamente
loss_fn = nn.BCELoss()  # Requiere aplicar sigmoid manualmente
```

### 5.3 Para Clasificación Multiclase

```python
# Si tienes 3+ clases, usa CrossEntropyLoss
loss_fn = nn.CrossEntropyLoss()
```

## 6. Optimizador

```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
```

### 6.1 ¿Qué hace el optimizador?

El optimizador **actualiza los pesos del modelo** para minimizar la pérdida :
- Lee los gradientes calculados por backpropagation
- Ajusta los pesos en la dirección que reduce el error
- Es el "motor" del aprendizaje

### 6.2 ¿Por qué SGD?

**SGD = Stochastic Gradient Descent** :
- Algoritmo clásico y confiable
- Funciona bien para problemas simples
- Menos memoria que optimizadores más avanzados

### 6.3 ¿Qué es el Learning Rate (lr)?

**Learning rate = 0.1** es la "velocidad de aprendizaje" :
- **Demasiado alto (ej: 10)**: El modelo salta el mínimo, nunca converge
- **Demasiado bajo (ej: 0.0001)**: Aprendizaje muy lento, puede quedarse atascado
- **0.1 es buen punto de partida** para problemas simples
- Valores típicos: 0.001 a 0.1

### 6.4 Alternativa: Adam (Más Avanzado)

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

**¿Cuándo usar Adam?** :
- Problemas más complejos
- Ajusta automáticamente el learning rate
- Generalmente converge más rápido
- Usa más memoria

## 7. Bucle de Entrenamiento

### 7.1 Estructura Completa

```python
torch.manual_seed(42)  # Reproducibilidad

epochs = 100  # Número de veces que verá todos los datos

for epoch in range(epochs):
    ### MODO ENTRENAMIENTO ###
    model.train()
    
    # 1. Forward pass (pasada hacia adelante)
    y_logits = model(X_train).squeeze()
    
    # 2. Calcular pérdida
    loss = loss_fn(y_logits, y_train)
    
    # 3. Resetear gradientes
    optimizer.zero_grad()
    
    # 4. Backpropagation (calcular gradientes)
    loss.backward()
    
    # 5. Actualizar pesos
    optimizer.step()
    
    ### MODO EVALUACIÓN ###
    model.eval()
    with torch.inference_mode():
        test_logits = model(X_test).squeeze()
        test_loss = loss_fn(test_logits, y_test)
    
    # Imprimir progreso
    if epoch % 10 == 0:
        print(f"Epoch: {epoch} | Loss: {loss:.4f} | Test Loss: {test_loss:.4f}")
```

### 7.2 Explicación Paso a Paso

**1. Forward Pass** :
```python
y_logits = model(X_train).squeeze()
```
- El modelo procesa los datos de entrada
- Produce "logits" (valores crudos sin activación)
- `.squeeze()` elimina dimensiones extra para que coincida con y_train

**2. Calcular Pérdida** :
```python
loss = loss_fn(y_logits, y_train)
```
- Compara predicciones con valores reales
- Produce un número: qué tan mal lo está haciendo el modelo
- El objetivo es minimizar este número

**3. Zero Gradients** :
```python
optimizer.zero_grad()
```
- **MUY IMPORTANTE**: PyTorch acumula gradientes por defecto
- Debemos resetearlos a cero antes de cada iteración
- Olvidar esto causa errores de entrenamiento

**4. Backpropagation** :
```python
loss.backward()
```
- Calcula cómo cambiar cada peso para reducir la pérdida
- Usa la regla de la cadena del cálculo
- Almacena gradientes en cada parámetro

**5. Actualizar Pesos** :
```python
optimizer.step()
```
- Aplica los gradientes calculados
- Actualiza los pesos del modelo
- Aquí es donde realmente "aprende" el modelo

### 7.3 ¿Por qué model.train() y model.eval()?

```python
model.train()  # Modo entrenamiento
# ... entrenamiento ...
model.eval()   # Modo evaluación
```

**model.train()** :
- Activa capas como Dropout y BatchNorm en modo entrenamiento
- Calcula y almacena gradientes

**model.eval()** :
- Desactiva Dropout y BatchNorm
- Más rápido, no calcula gradientes innecesarios
- `torch.inference_mode()` optimiza aún más

### 7.4 ¿Cuántas Epochs?

```python
epochs = 100  # Puedes ajustar este valor
```

**¿Qué significa?** :
- El modelo verá todos los datos de entrenamiento 100 veces
- Más epochs = más oportunidades de aprender
- Demasiadas epochs = sobreajuste (memoriza en lugar de aprender)

**Valores típicos**:
- Problemas simples: 100-500 epochs
- Problemas complejos: 1000-10000 epochs
- Usa validación para detectar cuándo parar

## 8. Hacer Predicciones

### 8.1 De Logits a Predicciones Finales

El proceso es: **Logits → Probabilidades → Clases** 

```python
# 1. Obtener logits (salidas crudas)
y_logits = model(X_test)

# 2. Convertir a probabilidades con sigmoid
y_pred_probs = torch.sigmoid(y_logits)

# 3. Convertir a clases (0 o 1)
y_preds = torch.round(y_pred_probs)
```

**¿Por qué este proceso?** :

1. **Logits**: Valores sin restricción (-∞ a +∞)
2. **Sigmoid**: Convierte a rango , interpretable como probabilidad
3. **Round**: Umbral en 0.5:
   - Si prob ≥ 0.5 → clase 1
   - Si prob < 0.5 → clase 0

### 8.2 Función de Precisión (Accuracy)

```python
def accuracy_fn(y_true, y_pred):
    correct = torch.eq(y_true, y_pred).sum().item()
    acc = (correct / len(y_pred)) * 100
    return acc
```

**¿Qué hace?** :
- Cuenta cuántas predicciones son correctas
- Divide por el total de predicciones
- Multiplica por 100 para obtener porcentaje

## 9. Problema Común: Underfitting

### 9.1 ¿Qué es Underfitting?

Tu modelo puede mostrar síntomas de **underfitting** (subajuste) si :
- Precisión cercana al 50% en clasificación binaria balanceada
- La pérdida no disminuye significativamente
- El modelo dibuja límites de decisión demasiado simples

### 9.2 Causas y Soluciones

| Causa | Solución | Código |
|-------|----------|--------|
| Modelo demasiado simple | Añadir más capas | `nn.Linear(10, 20), nn.Linear(20, 10)` |
| Pocas neuronas | Aumentar `out_features` | `out_features=50` en lugar de `10` |
| Pocas epochs | Entrenar más tiempo | `epochs=1000` |
| Datos no lineales | **Añadir funciones de activación** | Ver siguiente sección |

## 10. Funciones de Activación: La Clave para No-Linealidad

### 10.1 El Problema de las Capas Lineales

**Sin activaciones, tu red es esencialmente lineal** :
```python
# Este modelo SOLO puede aprender líneas rectas
model = nn.Sequential(
    nn.Linear(2, 10),
    nn.Linear(10, 1)
)
```

¿Por qué? Matemáticamente:
- Capa 1: y₁ = x · W₁ + b₁
- Capa 2: y₂ = y₁ · W₂ + b₂
- Combinado: y₂ = (x · W₁ + b₁) · W₂ + b₂ = x · (W₁·W₂) + (b₁·W₂+b₂)
- ¡Sigue siendo una función lineal!

### 10.2 Solución: Función ReLU

```python
model = nn.Sequential(
    nn.Linear(2, 10),
    nn.ReLU(),          # ← ACTIVACIÓN NO LINEAL
    nn.Linear(10, 10),
    nn.ReLU(),          # ← OTRA ACTIVACIÓN
    nn.Linear(10, 1)
)
```

**¿Qué es ReLU?** :
- **Re**ctified **L**inear **U**nit
- Fórmula simple: f(x) = max(0, x)
- Si x > 0 → devuelve x
- Si x ≤ 0 → devuelve 0

**¿Por qué ReLU?** :
- Introduce no-linealidad (puede modelar curvas)
- Computacionalmente muy eficiente
- No sufre de "vanishing gradient" como sigmoid/tanh
- Es el estándar en deep learning moderno

### 10.3 Otras Activaciones

```python
# Alternativas a ReLU
nn.Tanh()        # Rango [-1, 1], útil para ciertos problemas
nn.LeakyReLU()   # Como ReLU pero no "mata" valores negativos
nn.Sigmoid()     # Solo para capa de salida en clasificación binaria
nn.Softmax()     # Solo para capa de salida multiclase
```

## 11. Modelo Completo y Funcional

```python
import torch
import torch.nn as nn
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split

# 1. PREPARAR DATOS
X, y = make_circles(1000, noise=0.03, random_state=42)
X = torch.from_numpy(X).type(torch.float)
y = torch.from_numpy(y).type(torch.float)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. CONFIGURAR DISPOSITIVO
device = "cuda" if torch.cuda.is_available() else "cpu"
X_train, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)

# 3. CREAR MODELO CON ACTIVACIONES
model = nn.Sequential(
    nn.Linear(in_features=2, out_features=16),
    nn.ReLU(),
    nn.Linear(in_features=16, out_features=16),
    nn.ReLU(),
    nn.Linear(in_features=16, out_features=1)
).to(device)

# 4. FUNCIÓN DE PÉRDIDA Y OPTIMIZADOR
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 5. FUNCIÓN DE ACCURACY
def accuracy_fn(y_true, y_pred):
    correct = torch.eq(y_true, y_pred).sum().item()
    return (correct / len(y_pred)) * 100

# 6. BUCLE DE ENTRENAMIENTO
epochs = 1000
for epoch in range(epochs):
    # Entrenamiento
    model.train()
    y_logits = model(X_train).squeeze()
    loss = loss_fn(y_logits, y_train)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    # Evaluación
    model.eval()
    with torch.inference_mode():
        test_logits = model(X_test).squeeze()
        test_pred = torch.round(torch.sigmoid(test_logits))
        test_loss = loss_fn(test_logits, y_test)
        test_acc = accuracy_fn(y_test, test_pred)
    
    if epoch % 100 == 0:
        print(f"Epoch: {epoch} | Loss: {loss:.4f} | Test Acc: {test_acc:.2f}%")

# 7. HACER PREDICCIONES
model.eval()
with torch.inference_mode():
    y_preds = torch.round(torch.sigmoid(model(X_test).squeeze()))
    final_acc = accuracy_fn(y_test, y_preds)
    print(f"\nAccuracy final: {final_acc:.2f}%")
```

## 12. Resumen de Decisiones Clave

| Decisión | Recomendación | Razón |
|----------|---------------|-------|
| **Función de pérdida binaria** | `BCEWithLogitsLoss` | Numéricamente estable, sigmoid incluido |
| **Función de pérdida multiclase** | `CrossEntropyLoss` | Diseñada para múltiples clases |
| **Optimizador simple** | `SGD` con lr=0.1 | Confiable, menos memoria |
| **Optimizador avanzado** | `Adam` con lr=0.001 | Converge más rápido |
| **Activación oculta** | `ReLU` | Estándar, eficiente, evita vanishing gradient |
| **Neuronas ocultas** | 10-512 (empezar pequeño) | Ajustar según complejidad del problema |
| **Epochs** | 100-1000+ | Monitorear hasta que converja |

## 13. Checklist de Errores Comunes

**Verificar siempre**:
- [ ] Convertir datos a tensores con `.type(torch.float)`
- [ ] Mover modelo y datos al mismo dispositivo (`.to(device)`)
- [ ] Usar `optimizer.zero_grad()` antes de cada backward
- [ ] Incluir activaciones no-lineales (ReLU) entre capas
- [ ] Usar `model.train()` para entrenar y `model.eval()` para evaluar
- [ ] Las dimensiones coinciden: `out_features` de capa N = `in_features` de capa N+1
- [ ] Aplicar sigmoid a logits solo para visualizar probabilidades, no para BCEWithLogitsLoss

Tienes razón, falta explicar los tensores y `requires_grad`. Voy a añadir esa sección importante y crear un segundo ejemplo completo de **regresión** para que tengan ambos casos. Te lo presento como complemento al documento anterior:



# COMPLEMENTO: Conceptos Fundamentales y Ejemplo de Regresión

## 14. Tensores y Gradientes: El Motor del Aprendizaje

### 14.1 ¿Qué es un Tensor?

Un tensor es la estructura de datos fundamental en PyTorch :

```python
import torch

# Diferentes tipos de tensores
escalar = torch.tensor(7)           # Tensor 0D (número)
vector = torch.tensor([1, 2, 3])    # Tensor 1D (lista)
matriz = torch.tensor([[1, 2],      # Tensor 2D (tabla)
                       [3, 4]])
```

**¿Por qué no usar NumPy?** PyTorch puede calcular gradientes automáticamente y usar GPU .

### 14.2 requires_grad: Activar el Cálculo de Gradientes

```python
# Crear tensor que necesita gradientes
x = torch.tensor([2.0], requires_grad=True)

# Realizar operación
y = x ** 2  # y = 4

# Calcular gradiente
y.backward()  # dy/dx = 2x = 2*2 = 4

print(f"Gradiente de y respecto a x: {x.grad}")  # Output: 4.0
```

**¿Qué significa `requires_grad=True`?** :
- Le dice a PyTorch: "necesito calcular derivadas para este tensor"
- PyTorch registra todas las operaciones en un "grafo computacional"
- Cuando llamas `.backward()`, calcula todas las derivadas automáticamente

### 14.3 ¿Cuándo Necesitas requires_grad?

| Situación | requires_grad | Razón |
|-----------|---------------|-------|
| **Parámetros del modelo** | ✅ Automático | `nn.Module` lo activa por defecto |
| **Datos de entrada (X)** | ❌ NO | No entrenamos los datos, solo el modelo |
| **Etiquetas (y)** | ❌ NO | Las etiquetas son fijas |
| **Crear modelo custom** | ✅ Sí, para parámetros | Solo si no usas `nn.Linear` |

**En la práctica con nn.Module**: No necesitas preocuparte porque PyTorch lo maneja automáticamente :

```python
model = nn.Linear(2, 1)

# Los parámetros YA tienen requires_grad=True
for name, param in model.named_parameters():
    print(f"{name}: requires_grad={param.requires_grad}")

# Output:
# weight: requires_grad=True
# bias: requires_grad=True
```

### 14.4 Ejemplo Manual (Para Entender el Concepto)

```python
# Si crearas parámetros manualmente (raro en la práctica)
W = torch.randn(10, 2, requires_grad=True)  # Pesos
b = torch.randn(10, requires_grad=True)     # Bias

# Forward pass
y = X @ W.T + b  # @ es multiplicación de matrices

# Backward pass
loss = some_loss_function(y, targets)
loss.backward()  # Calcula gradientes de W y b

# Ahora W.grad y b.grad contienen las derivadas
```

**Mensaje clave**: Cuando usas `nn.Linear`, `nn.Sequential`, etc., **PyTorch maneja requires_grad automáticamente**. Solo necesitas saberlo si construyes arquitecturas muy personalizadas .



## 15. EJEMPLO COMPLETO 2: Red Neuronal para REGRESIÓN

### 15.1 Diferencias entre Clasificación y Regresión

| Aspecto | Clasificación | Regresión |
|---------|---------------|-----------|
| **Objetivo** | Predecir categorías (0, 1, 2...) | Predecir valores continuos (3.14, 100.5...) |
| **Ejemplos** | ¿Es spam? ¿Qué dígito es? | Precio de casa, temperatura, ventas |
| **Capa de salida** | 1 neurona (binaria) o N (multiclase) | 1 neurona (valor continuo) |
| **Activación salida** | Sigmoid o Softmax | **Ninguna** (valores sin restricción) |
| **Función de pérdida** | BCEWithLogitsLoss, CrossEntropyLoss | **MSELoss** o **L1Loss** |
| **Métricas** | Accuracy, Precision, Recall | MAE, RMSE, R² |

### 15.2 Preparación de Datos para Regresión

```python
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Crear datos: y = 0.7 * X + 0.3 + ruido
torch.manual_seed(42)
X = torch.arange(0, 1, 0.01).unsqueeze(1)  # 100 puntos de 0 a 1
y = 0.7 * X + 0.3 + 0.05 * torch.randn(X.shape)  # Línea con ruido

# Dividir en train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"X_train shape: {X_train.shape}")  # (80, 1)
print(f"y_train shape: {y_train.shape}")  # (80, 1)
```

**¿Por qué estos datos?** :
- `X.unsqueeze(1)`: Convierte  en  (necesario para nn.Linear)
- `0.05 * torch.randn()`: Añade ruido gaussiano realista
- Relación lineal simple para verificar que el modelo aprende

### 15.3 Arquitectura del Modelo de Regresión

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
X_train, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)

# Modelo simple para regresión lineal
class ModeloRegresion(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=1, out_features=10)
        self.layer_2 = nn.Linear(in_features=10, out_features=10)
        self.layer_3 = nn.Linear(in_features=10, out_features=1)
    
    def forward(self, x):
        # Añadimos ReLU para no-linealidad
        x = torch.relu(self.layer_1(x))
        x = torch.relu(self.layer_2(x))
        return self.layer_3(x)  # ¡SIN ACTIVACIÓN en la salida!

model = ModeloRegresion().to(device)
print(model)
```

**⚠️ IMPORTANTE**: La capa de salida NO tiene activación (ni sigmoid ni ReLU) porque necesitamos predecir cualquier valor real .

### 15.4 Función de Pérdida para Regresión: MSELoss

```python
loss_fn = nn.MSELoss()  # Mean Squared Error
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
```

**¿Qué es MSELoss?** :
- **MSE = Mean Squared Error** (Error Cuadrático Medio)
- Fórmula: MSE = (1/N) × Σ(y_pred - y_true)²
- Penaliza errores grandes más que errores pequeños
- Estándar para regresión

**Alternativa: L1Loss (MAE)** :
```python
loss_fn = nn.L1Loss()  # Mean Absolute Error
```
- Fórmula: MAE = (1/N) × Σ|y_pred - y_true|
- Más robusta a outliers
- Penaliza todos los errores por igual

### 15.5 Bucle de Entrenamiento para Regresión

```python
torch.manual_seed(42)
epochs = 1000

print("=== ENTRENAMIENTO DE REGRESIÓN ===\n")

for epoch in range(epochs):
    ### MODO ENTRENAMIENTO ###
    model.train()
    
    # 1. Forward pass
    y_pred = model(X_train)
    
    # 2. Calcular pérdida
    loss = loss_fn(y_pred, y_train)
    
    # 3. Resetear gradientes
    optimizer.zero_grad()
    
    # 4. Backpropagation
    loss.backward()
    
    # 5. Actualizar pesos
    optimizer.step()
    
    ### MODO EVALUACIÓN ###
    model.eval()
    with torch.inference_mode():
        test_pred = model(X_test)
        test_loss = loss_fn(test_pred, y_test)
    
    # Imprimir progreso
    if epoch % 100 == 0:
        print(f"Epoch: {epoch:4d} | Train Loss: {loss:.6f} | Test Loss: {test_loss:.6f}")

print(f"\n✅ Entrenamiento completado!")
```

**Diferencias con clasificación** :
1. No usamos `.squeeze()` porque y_train ya tiene shape correcto
2. No aplicamos sigmoid/softmax a las predicciones
3. No calculamos accuracy (usamos pérdida directamente)

### 15.6 Evaluación: Métricas para Regresión

```python
def mae_metric(y_true, y_pred):
    """Mean Absolute Error"""
    return torch.mean(torch.abs(y_true - y_pred)).item()

def rmse_metric(y_true, y_pred):
    """Root Mean Squared Error"""
    return torch.sqrt(torch.mean((y_true - y_pred)**2)).item()

# Evaluar modelo
model.eval()
with torch.inference_mode():
    y_pred_test = model(X_test)
    
    mae = mae_metric(y_test, y_pred_test)
    rmse = rmse_metric(y_test, y_pred_test)
    
    print(f"\n=== MÉTRICAS FINALES ===")
    print(f"MAE (Error Absoluto Medio):  {mae:.4f}")
    print(f"RMSE (Raíz Error Cuadrático): {rmse:.4f}")
```

**¿Qué significan estas métricas?** :
- **MAE**: Error promedio en las mismas unidades que y
  - Si predices precios en €, MAE=5 significa error promedio de 5€
- **RMSE**: Penaliza más los errores grandes
  - Más sensible a outliers que MAE

### 15.7 Visualización de Resultados

```python
# Hacer predicciones para todo el rango
model.eval()
with torch.inference_mode():
    y_pred_all = model(X.to(device)).cpu()

# Los valores reales que el modelo debería aprender
X_numpy = X.cpu().numpy()
y_numpy = y.cpu().numpy()
y_pred_numpy = y_pred_all.numpy()

print("\n=== Visualización ===")
print(f"El modelo aprendió una función que aproxima: y = 0.7*X + 0.3")
print(f"Primeros 5 ejemplos:")
for i in range(5):
    print(f"  X={X_numpy[i,0]:.2f} -> y_real={y_numpy[i,0]:.4f}, y_pred={y_pred_numpy[i,0]:.4f}")
```



## 16. CÓDIGO COMPLETO Y FUNCIONAL: REGRESIÓN

```python
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split

# ====================
# 1. PREPARAR DATOS
# ====================
torch.manual_seed(42)
X = torch.arange(0, 1, 0.01).unsqueeze(1)
y = 0.7 * X + 0.3 + 0.05 * torch.randn(X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ====================
# 2. CONFIGURAR DISPOSITIVO
# ====================
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {device}\n")
X_train = X_train.to(device)
y_train = y_train.to(device)
X_test = X_test.to(device)
y_test = y_test.to(device)

# ====================
# 3. CREAR MODELO
# ====================
class ModeloRegresion(nn.Module):
    def __init__(self):
        super().__init__()
        self.capas = nn.Sequential(
            nn.Linear(1, 10),
            nn.ReLU(),
            nn.Linear(10, 10),
            nn.ReLU(),
            nn.Linear(10, 1)  # Sin activación en la salida
        )
    
    def forward(self, x):
        return self.capas(x)

model = ModeloRegresion().to(device)

# ====================
# 4. PÉRDIDA Y OPTIMIZADOR
# ====================
loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# ====================
# 5. MÉTRICAS
# ====================
def mae_metric(y_true, y_pred):
    return torch.mean(torch.abs(y_true - y_pred)).item()

# ====================
# 6. ENTRENAMIENTO
# ====================
epochs = 1000
print("=== ENTRENAMIENTO ===")

for epoch in range(epochs):
    # Entrenar
    model.train()
    y_pred = model(X_train)
    loss = loss_fn(y_pred, y_train)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    # Evaluar
    model.eval()
    with torch.inference_mode():
        test_pred = model(X_test)
        test_loss = loss_fn(test_pred, y_test)
        test_mae = mae_metric(y_test, test_pred)
    
    if epoch % 200 == 0:
        print(f"Epoch {epoch:4d} | Loss: {loss:.6f} | Test Loss: {test_loss:.6f} | MAE: {test_mae:.6f}")

# ====================
# 7. EVALUACIÓN FINAL
# ====================
model.eval()
with torch.inference_mode():
    final_pred = model(X_test)
    final_mae = mae_metric(y_test, final_pred)
    final_loss = loss_fn(final_pred, y_test)

print(f"\n=== RESULTADOS FINALES ===")
print(f"Test Loss (MSE): {final_loss:.6f}")
print(f"MAE: {final_mae:.6f}")

# Mostrar predicciones ejemplo
print(f"\n=== EJEMPLOS DE PREDICCIÓN ===")
with torch.inference_mode():
    ejemplos = torch.tensor([[0.0], [0.25], [0.5], [0.75], [1.0]]).to(device)
    predicciones = model(ejemplos)
    for x_val, y_val in zip(ejemplos.cpu().numpy(), predicciones.cpu().numpy()):
        y_real = 0.7 * x_val[0] + 0.3
        print(f"X={x_val[0]:.2f} -> Predicción: {y_val[0]:.4f} | Real teórico: {y_real:.4f}")
```



## 17. Comparación Lado a Lado: Clasificación vs Regresión

### 17.1 Tabla Resumen Código

| Componente | Clasificación (Binaria) | Regresión |
|------------|-------------------------|-----------|
| **Datos de salida** | `y = torch.tensor([0, 1, 1, 0])` | `y = torch.tensor([1.5, 2.3, 0.7])` |
| **Capa de salida** | `nn.Linear(hidden, 1)` | `nn.Linear(hidden, 1)` |
| **Activación salida** | **Ninguna** (BCEWithLogits la incluye) | **Ninguna** |
| **Loss function** | `nn.BCEWithLogitsLoss()` | `nn.MSELoss()` |
| **Predicción final** | `torch.round(torch.sigmoid(logits))` | `model(X)` directamente |
| **Métricas** | Accuracy, F1-Score | MAE, RMSE, R² |

### 17.2 Cuándo Usar Cada Una

**USA CLASIFICACIÓN cuando** :
- La respuesta es una categoría: Sí/No, Perro/Gato/Pájaro
- Ejemplos: Detección spam, diagnóstico médico, reconocimiento dígitos

**USA REGRESIÓN cuando** :
- La respuesta es un número continuo
- Ejemplos: Precio vivienda, temperatura, ventas futuras, edad



## 18. Checklist Final Expandido

 **Antes de entrenar**:
- [ ] Datos convertidos a tensores con `.type(torch.float)`
- [ ] Datos divididos en train/test (80/20 típico)
- [ ] Modelo y datos en el mismo dispositivo (`.to(device)`)
- [ ] Para clasificación: etiquetas son 0, 1, 2... (enteros)
- [ ] Para regresión: etiquetas son valores continuos

 **Arquitectura del modelo**:
- [ ] Capas de entrada coinciden con número de features
- [ ] Activaciones ReLU entre capas ocultas
- [ ] Clasificación: Salida sin activación + BCEWithLogitsLoss
- [ ] Regresión: Salida sin activación + MSELoss

**Durante entrenamiento**:
- [ ] `model.train()` antes de entrenar
- [ ] `optimizer.zero_grad()` antes de backward
- [ ] `loss.backward()` para calcular gradientes
- [ ] `optimizer.step()` para actualizar pesos
- [ ] `model.eval()` y `torch.inference_mode()` para evaluar

**Predicciones**:
- [ ] Clasificación: Aplicar sigmoid → round para clases finales
- [ ] Regresión: Usar predicciones directamente

**Concepto `requires_grad`** :
- [ ] Entiendes que los parámetros del modelo lo tienen activado automáticamente
- [ ] Los datos de entrada (X, y) NO necesitan requires_grad
- [ ] Solo lo configuras manualmente si creas parámetros custom (raro)



## 19. Ejercicios Propuestos para Estudiantes

### Ejercicio 1: Modificar el Modelo de Clasificación
- Cambia el número de neuronas ocultas de 16 a 32
- Añade una tercera capa oculta
- Observa cómo cambia la precisión

### Ejercicio 2: Experimentar con Learning Rate
- Prueba `lr=0.001`, `lr=0.1`, `lr=1.0`
- ¿Cuál converge mejor?
- Documenta tus observaciones

### Ejercicio 3: Cambiar Optimizador
- Reemplaza Adam por SGD
- Compara velocidad de convergencia
- ¿Cuál alcanza mejor accuracy final?

### Ejercicio 4: Crear Regresión No-Lineal
- Modifica los datos de regresión: `y = X**2 + ruido`
- Entrena el modelo
- ¿Puede aprender funciones cuadráticas?

### Ejercicio 5: Clasificación Multiclase
- Usa `make_blobs(n_samples=1000, centers=3)` para 3 clases
- Cambia la salida a `out_features=3`
- Usa `nn.CrossEntropyLoss()`
- ¿Cómo cambian las predicciones?

