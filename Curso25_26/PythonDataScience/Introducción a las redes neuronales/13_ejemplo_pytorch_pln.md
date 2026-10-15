## Ejemplo práctico: Clasificador de sentimiento con PyTorch

### Objetivo del ejemplo

Vamos a construir una red que clasifique frases como POSITIVAS o NEGATIVAS. Veremos cada transformación:

```
Texto: "I love this book"
   ↓ (vocabulario)
Índices: [2, 5, 8, 12]
   ↓ (embedding layer)
Tensores: [[0.23, -0.45, ...], [0.12, 0.67, ...], ...]
   ↓ (red neuronal)
Tensor salida: [0.92, 0.08]
   ↓ (interpretación)
Predicción: POSITIVO (92% confianza)
```

### Preparación de datos

Primero creamos un dataset pequeño para entrenar:

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import Counter

# Dataset simple de entrenamiento
train_data = [
    ("I love this book", 1),           # 1 = positivo
    ("This is amazing", 1),
    ("Great story and characters", 1),
    ("Wonderful experience", 1),
    ("Best book ever", 1),
    ("I really enjoyed it", 1),
    ("Absolutely fantastic", 1),
    
    ("I hate this book", 0),           # 0 = negativo
    ("This is terrible", 0),
    ("Waste of time", 0),
    ("Very disappointing", 0),
    ("Awful and boring", 0),
    ("I did not like it", 0),
    ("Completely horrible", 0),
]

print("Dataset de entrenamiento:")
for text, label in train_data[:3]:
    sentiment = "POSITIVO" if label == 1 else "NEGATIVO"
    print(f"  '{text}' → {sentiment}")
```

### Paso 1: Construir el vocabulario (texto → índices)

Necesitamos un diccionario que mapee cada palabra a un número único:

```python
# Extraer todas las palabras
all_words = []
for text, _ in train_data:
    words = text.lower().split()
    all_words.extend(words)

# Crear vocabulario
vocab = {word: idx for idx, word in enumerate(set(all_words), start=2)}
vocab['<PAD>'] = 0  # Para padding
vocab['<UNK>'] = 1  # Para palabras desconocidas

print(f"\nVocabulario ({len(vocab)} palabras):")
for word, idx in list(vocab.items())[:10]:
    print(f"  '{word}' → {idx}")

# Vocabulario inverso (para convertir índices a palabras)
idx_to_word = {idx: word for word, idx in vocab.items()}
```

**Función para convertir texto a índices:**

```python
def text_to_indices(text, vocab):
    """Convierte texto en lista de índices"""
    words = text.lower().split()
    indices = [vocab.get(word, vocab['<UNK>']) for word in words]
    return indices

# Ejemplo de conversión
sample_text = "I love this book"
sample_indices = text_to_indices(sample_text, vocab)

print(f"\n--- Conversión texto → índices ---")
print(f"Texto: '{sample_text}'")
print(f"Palabras: {sample_text.lower().split()}")
print(f"Índices: {sample_indices}")

# Verificar conversión inversa
print(f"Verificación: {[idx_to_word[idx] for idx in sample_indices]}")
```

### Paso 2: Padding y creación de tensores

Las frases tienen diferente longitud, necesitamos igualarlas:

```python
def pad_sequence(indices, max_len, pad_value=0):
    """Añade padding hasta max_len"""
    if len(indices) < max_len:
        indices = indices + [pad_value] * (max_len - len(indices))
    else:
        indices = indices[:max_len]
    return indices

# Encontrar longitud máxima
max_length = max(len(text.split()) for text, _ in train_data)
print(f"\nLongitud máxima de frase: {max_length} palabras")

# Convertir todo el dataset
X_train = []
y_train = []

for text, label in train_data:
    indices = text_to_indices(text, vocab)
    padded = pad_sequence(indices, max_length)
    X_train.append(padded)
    y_train.append(label)

# Convertir a tensores de PyTorch
X_train = torch.LongTensor(X_train)
y_train = torch.FloatTensor(y_train)

print(f"\nTensores creados:")
print(f"  X_train shape: {X_train.shape} (batch_size={len(train_data)}, seq_len={max_length})")
print(f"  y_train shape: {y_train.shape}")

print(f"\nEjemplo del primer dato:")
print(f"  Índices: {X_train[0]}")
print(f"  Palabras: {[idx_to_word[idx.item()] for idx in X_train[0]]}")
print(f"  Etiqueta: {y_train[0].item()} (POSITIVO)")
```

### Paso 3: Definir la red neuronal

Una arquitectura simple: **Embedding → Media → Fully Connected → Sigmoid**

```python
class SentimentClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(SentimentClassifier, self).__init__()
        
        # Capa de embedding: convierte índices en vectores densos
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        
        # Capas fully connected
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, 1)
        
        # Activaciones
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        # x shape: (batch_size, seq_length)
        
        # 1. Embedding: índices → vectores
        embedded = self.embedding(x)  # (batch_size, seq_length, embedding_dim)
        
        # 2. Pooling: promedio de todos los embeddings de la secuencia
        pooled = embedded.mean(dim=1)  # (batch_size, embedding_dim)
        
        # 3. Capas fully connected
        hidden = self.relu(self.fc1(pooled))  # (batch_size, hidden_dim)
        output = self.sigmoid(self.fc2(hidden))  # (batch_size, 1)
        
        return output

# Hiperparámetros
vocab_size = len(vocab)
embedding_dim = 10  # Dimensión de los embeddings
hidden_dim = 16     # Neuronas capa oculta

# Crear modelo
model = SentimentClassifier(vocab_size, embedding_dim, hidden_dim)

print("\n--- Arquitectura de la red ---")
print(model)
print(f"\nParámetros totales: {sum(p.numel() for p in model.parameters())}")
```

### Paso 4: Visualizar las transformaciones paso a paso

Vamos a ver qué pasa con UN ejemplo atravesando la red:

```python
# Tomar el primer ejemplo
sample_input = X_train[0:1]  # Shape: (1, seq_length)

print("\n" + "="*60)
print("TRANSFORMACIONES PASO A PASO")
print("="*60)

print(f"\n0. INPUT (texto original):")
print(f"   '{train_data[0][0]}'")

print(f"\n1. ÍNDICES (después de vocabulario):")
print(f"   Shape: {sample_input.shape}")
print(f"   Valores: {sample_input}")
print(f"   Palabras: {[idx_to_word[idx.item()] for idx in sample_input[0]]}")

# Pasar por embedding
with torch.no_grad():
    embedded = model.embedding(sample_input)
    
print(f"\n2. EMBEDDINGS (después de embedding layer):")
print(f"   Shape: {embedded.shape}")
print(f"   (batch=1, palabras={max_length}, dimensión_embedding={embedding_dim})")
print(f"\n   Embedding de la primera palabra ('{idx_to_word[sample_input[0][0].item()]}'):")
print(f"   {embedded[0][0]}")

# Pooling (promedio)
with torch.no_grad():
    pooled = embedded.mean(dim=1)
    
print(f"\n3. POOLING (promedio de embeddings):")
print(f"   Shape: {pooled.shape}")
print(f"   Valores: {pooled}")

# Capa oculta
with torch.no_grad():
    hidden = model.relu(model.fc1(pooled))
    
print(f"\n4. CAPA OCULTA (después de fc1 + ReLU):")
print(f"   Shape: {hidden.shape}")
print(f"   Valores: {hidden}")

# Salida final
with torch.no_grad():
    output = model(sample_input)
    
print(f"\n5. OUTPUT FINAL (después de fc2 + Sigmoid):")
print(f"   Shape: {output.shape}")
print(f"   Valor: {output.item():.4f}")
print(f"   Interpretación: {'POSITIVO' if output.item() > 0.5 else 'NEGATIVO'}")
print(f"   Confianza: {output.item()*100:.1f}%" if output.item() > 0.5 else f"   Confianza: {(1-output.item())*100:.1f}%")
```

### Paso 5: Entrenamiento

Ahora entrenamos la red para que aprenda a clasificar:

```python
# Configuración del entrenamiento
criterion = nn.BCELoss()  # Binary Cross Entropy
optimizer = optim.Adam(model.parameters(), lr=0.01)
epochs = 100

print("\n" + "="*60)
print("ENTRENAMIENTO")
print("="*60)

# Entrenamiento
losses = []

for epoch in range(epochs):
    # Forward pass
    outputs = model(X_train).squeeze()
    loss = criterion(outputs, y_train)
    
    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    losses.append(loss.item())
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

# Visualizar pérdida
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(losses)
plt.xlabel('Época')
plt.ylabel('Pérdida (Loss)')
plt.title('Evolución del entrenamiento')
plt.grid(True, alpha=0.3)
plt.show()
```

### Paso 6: Evaluación y predicción

Probamos con nuevas frases:

```python
def predict_sentiment(text, model, vocab, max_length):
    """
    Predice el sentimiento de un texto
    Muestra toda la pipeline de transformación
    """
    print(f"\n{'='*60}")
    print(f"PREDICCIÓN: '{text}'")
    print('='*60)
    
    # 1. Texto → índices
    indices = text_to_indices(text, vocab)
    print(f"\n1. Palabras: {text.lower().split()}")
    print(f"   Índices: {indices}")
    
    # 2. Padding
    padded = pad_sequence(indices, max_length)
    print(f"\n2. Con padding: {padded}")
    
    # 3. Convertir a tensor
    tensor_input = torch.LongTensor([padded])
    print(f"\n3. Tensor shape: {tensor_input.shape}")
    
    # 4. Predicción
    model.eval()
    with torch.no_grad():
        output = model(tensor_input)
        probability = output.item()
    
    print(f"\n4. Salida de la red:")
    print(f"   Tensor: {output}")
    print(f"   Probabilidad: {probability:.4f}")
    
    # 5. Interpretación
    sentiment = "POSITIVO" if probability > 0.5 else "NEGATIVO"
    confidence = probability if probability > 0.5 else 1 - probability
    
    print(f"\n5. RESULTADO FINAL:")
    print(f"   Sentimiento: {sentiment}")
    print(f"   Confianza: {confidence*100:.1f}%")
    
    return sentiment, confidence

# Probar con frases del entrenamiento
print("\n" + "="*70)
print("EVALUACIÓN EN DATOS DE ENTRENAMIENTO")
print("="*70)

test_texts = [
    "I love this book",
    "This is terrible",
]

for text in test_texts:
    predict_sentiment(text, model, vocab, max_length)
```

**Probar con frases completamente nuevas:**

```python
print("\n" + "="*70)
print("PREDICCIÓN EN DATOS NUEVOS")
print("="*70)

new_texts = [
    "amazing and wonderful",      # Positivo
    "awful and disappointing",    # Negativo  
    "great story",                # Positivo
    "waste of time",              # Negativo
    "love it",                    # Positivo
    "i hate it",                  # Negativo
]

for text in new_texts:
    predict_sentiment(text, model, vocab, max_length)
```

### Paso 7: Inspeccionar los embeddings aprendidos

Veamos qué ha aprendido la red sobre las palabras:

```python
print("\n" + "="*60)
print("EMBEDDINGS APRENDIDOS")
print("="*60)

# Obtener matriz de embeddings
embedding_matrix = model.embedding.weight.data

print(f"Matriz de embeddings shape: {embedding_matrix.shape}")
print(f"({vocab_size} palabras × {embedding_dim} dimensiones)")

# Ver embeddings de palabras específicas
interesting_words = ['love', 'hate', 'amazing', 'terrible', 'great', 'awful']

print("\nEmbeddings de palabras clave:")
for word in interesting_words:
    if word in vocab:
        idx = vocab[word]
        embedding_vec = embedding_matrix[idx]
        print(f"\n'{word}' (índice {idx}):")
        print(f"  {embedding_vec}")
```

**Calcular similitud entre palabras aprendidas:**

```python
from torch.nn.functional import cosine_similarity

def word_similarity(word1, word2, model, vocab):
    """Calcula similitud coseno entre dos palabras"""
    if word1 not in vocab or word2 not in vocab:
        return None
    
    idx1 = vocab[word1]
    idx2 = vocab[word2]
    
    emb1 = model.embedding.weight[idx1].unsqueeze(0)
    emb2 = model.embedding.weight[idx2].unsqueeze(0)
    
    similarity = cosine_similarity(emb1, emb2).item()
    return similarity

# Comparar pares de palabras
print("\n" + "="*60)
print("SIMILITUD ENTRE PALABRAS (aprendida por la red)")
print("="*60)

word_pairs = [
    ('love', 'amazing'),
    ('hate', 'terrible'),
    ('love', 'hate'),
    ('great', 'wonderful'),
    ('awful', 'horrible'),
]

for w1, w2 in word_pairs:
    sim = word_similarity(w1, w2, model, vocab)
    if sim is not None:
        print(f"{w1:12} ↔ {w2:12} → similitud: {sim:+.4f}")
```

### Visualización de embeddings

```python
from sklearn.decomposition import PCA

# Seleccionar palabras para visualizar
words_to_plot = [w for w in interesting_words if w in vocab]
word_indices = [vocab[w] for w in words_to_plot]

# Obtener embeddings
word_embeddings = embedding_matrix[word_indices].numpy()

# Reducir a 2D con PCA
pca = PCA(n_components=2)
embeddings_2d = pca.fit_transform(word_embeddings)

# Plotear
plt.figure(figsize=(10, 8))
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], s=200)

for i, word in enumerate(words_to_plot):
    plt.annotate(word, 
                 xy=(embeddings_2d[i, 0], embeddings_2d[i, 1]),
                 fontsize=14,
                 ha='center')

plt.title('Embeddings aprendidos (proyección 2D)')
plt.xlabel('Componente 1')
plt.ylabel('Componente 2')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\nObserva cómo palabras positivas y negativas")
print("se agrupan en regiones diferentes del espacio!")
```

### Resumen de transformaciones

```python
print("\n" + "="*70)
print("RESUMEN: PIPELINE COMPLETA")
print("="*70)

example_text = "I love this"

print(f"\nTexto original:")
print(f'  "{example_text}"')
print(f"  Tipo: string de Python")

indices = text_to_indices(example_text, vocab)
print(f"\n↓ [Vocabulario]")
print(f"\nÍndices numéricos:")
print(f"  {indices}")
print(f"  Tipo: lista de integers")

padded = pad_sequence(indices, max_length)
tensor_in = torch.LongTensor([padded])
print(f"\n↓ [Padding + Tensor]")
print(f"\nTensor de entrada:")
print(f"  {tensor_in}")
print(f"  Shape: {tensor_in.shape}")
print(f"  Tipo: torch.LongTensor")

with torch.no_grad():
    embedded = model.embedding(tensor_in)
    
print(f"\n↓ [Embedding Layer]")
print(f"\nEmbeddings:")
print(f"  Shape: {embedded.shape}")
print(f"  Tipo: torch.FloatTensor")
print(f"  Ejemplo (primera palabra): {embedded[0][0][:5]}...")

with torch.no_grad():
    output_tensor = model(tensor_in)
    
print(f"\n↓ [Red Neuronal]")
print(f"\nTensor de salida:")
print(f"  {output_tensor}")
print(f"  Shape: {output_tensor.shape}")
print(f"  Valor: {output_tensor.item():.4f}")

sentiment = "POSITIVO" if output_tensor.item() > 0.5 else "NEGATIVO"
print(f"\n↓ [Interpretación]")
print(f"\nResultado final:")
print(f'  "{sentiment}"')
print(f"  Tipo: string de Python")
```