
El broadcasting es un mecanismo que permite realizar operaciones entre tensores de diferentes tamaños/formas automáticamente. PyTorch expandirá implícitamente los tensores más pequeños para que coincidan con los más grandes cuando sea posible.

Las reglas básicas son:

1. Si los tensores tienen diferente número de dimensiones, PyTorch añade dimensiones de tamaño 1 al principio del tensor más pequeño hasta igualar las dimensiones.

2. Si en una dimensión un tensor tiene tamaño 1 y el otro tiene tamaño N, el de tamaño 1 se expande para coincidir con N.

Veamos ejemplos prácticos:

```python
import torch

# Ejemplo 1: Broadcasting entre escalar y tensor
scalar = torch.tensor(2)
vector = torch.tensor([1, 2, 3])
result = scalar * vector  # El escalar se expande a [2, 2, 2]
# result = [2, 4, 6]

# Ejemplo 2: Broadcasting entre vectores de diferentes dimensiones
a = torch.tensor([1, 2, 3])               # Shape: (3,)
b = torch.tensor([[4], [5], [6]])         # Shape: (3, 1)
result = a + b  # b se expande para coincidir con a
# result shape: (3, 3)
# result = [[5, 6, 7],
#           [6, 7, 8],
#           [7, 8, 9]]

# Ejemplo 3: Broadcasting más complejo
x = torch.zeros(2, 1, 3)  # Shape: (2, 1, 3)
y = torch.ones(3)         # Shape: (3,)
z = x + y  # y se expande a shape (2, 1, 3)
```

Algunos casos prácticos donde el broadcasting es útil:

1. Normalización de datos:
```python
# Restar la media a cada característica
data = torch.randn(100, 20)  # 100 muestras, 20 características
mean = data.mean(dim=0)      # media de cada característica
normalized = data - mean     # broadcasting automático
```

2. Añadir bias a capas neuronales:
```python
features = torch.randn(32, 10)  # batch_size=32, feature_size=10
bias = torch.randn(10)          # un bias por característica
output = features + bias        # bias se expande automáticamente
```