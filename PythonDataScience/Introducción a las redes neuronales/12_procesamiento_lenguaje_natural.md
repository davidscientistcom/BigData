# Curso de Procesamiento del Lenguaje Natural

## Introducción

El Procesamiento del Lenguaje Natural (PLN) es el área de la inteligencia artificial que permite a las máquinas entender, interpretar y generar lenguaje humano. En este curso trabajaremos con métodos clásicos que son la base fundamental para comprender cómo funcionan los sistemas modernos.

Utilizaremos principalmente Python con las librerías NLTK, gensim y scikit-learn. El corpus principal será el libro Drácula de Bram Stoker, disponible gratuitamente en Project Gutenberg.

***

## Bloque 1: Fundamentos y preprocesamiento de texto

### Instalación de librerías necesarias

Antes de comenzar, necesitamos instalar las librerías que vamos a utilizar:

```python
pip install nltk gensim scikit-learn matplotlib numpy
```

### Descarga de recursos NLTK

NLTK requiere descargar algunos recursos adicionales:

```python
import nltk

# Descargar recursos necesarios
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
```

### Obtención del corpus: Drácula

Vamos a descargar el libro Drácula desde Project Gutenberg:

```python
import urllib.request

# Descargar Drácula
url = 'https://www.gutenberg.org/files/345/345-0.txt'
response = urllib.request.urlopen(url)
dracula_raw = response.read().decode('utf-8')

# Ver las primeras líneas
print(dracula_raw[:500])
```

**Limpieza inicial del texto**

Los libros de Gutenberg tienen encabezados y pies con información legal. Vamos a limpiarlos:

```python
# Encontrar donde empieza y termina el contenido real
start = dracula_raw.find("CHAPTER I")
end = dracula_raw.find("*** END OF THE PROJECT GUTENBERG EBOOK")

dracula_text = dracula_raw[start:end]

print(f"Longitud del texto original: {len(dracula_raw)} caracteres")
print(f"Longitud del texto limpio: {len(dracula_text)} caracteres")
print("\nPrimeras líneas del libro:")
print(dracula_text[:300])
```

### Tokenización

La tokenización es el proceso de dividir el texto en unidades más pequeñas (tokens), que pueden ser palabras, frases o símbolos.

**Tokenización por palabras:**

```python
from nltk.tokenize import word_tokenize

# Tokenizar las primeras líneas
sample_text = "Jonathan Harker's Journal. 3 May. Bistritz.—Left Munich at 8:35 P.M."
tokens = word_tokenize(sample_text)

print("Texto original:")
print(sample_text)
print("\nTokens:")
print(tokens)
print(f"\nNúmero de tokens: {len(tokens)}")
```

**Tokenización por oraciones:**

```python
from nltk.tokenize import sent_tokenize

# Tokenizar en oraciones
sample_paragraph = """I read that every known superstition in the world is gathered into the horseshoe of the Carpathians, as if it were the centre of some sort of imaginative whirlpool. If so my stay may be very interesting."""

sentences = sent_tokenize(sample_paragraph)

print("Oraciones detectadas:")
for i, sentence in enumerate(sentences, 1):
    print(f"{i}. {sentence}")
```

**Práctica: Tokenizar todo Drácula**

```python
# Tokenizar todo el libro
dracula_tokens = word_tokenize(dracula_text.lower())

print(f"Total de tokens en Drácula: {len(dracula_tokens)}")
print(f"Primeros 50 tokens: {dracula_tokens[:50]}")
```

### Normalización del texto

La normalización incluye convertir el texto a minúsculas y eliminar elementos no deseados.

```python
import re
import string

def normalize_text(text):
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar números
    text = re.sub(r'\d+', '', text)
    # Eliminar puntuación
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Ejemplo
sample = "Jonathan Harker's Journal (1897): 3 May - Bistritz!!!"
normalized = normalize_text(sample)

print(f"Original: {sample}")
print(f"Normalizado: {normalized}")
```

### Stopwords (palabras vacías)

Las stopwords son palabras muy comunes que aportan poco significado (artículos, preposiciones, etc.).

```python
from nltk.corpus import stopwords

# Cargar stopwords en inglés
stop_words = set(stopwords.words('english'))

print(f"Total de stopwords en inglés: {len(stop_words)}")
print(f"Ejemplos: {list(stop_words)[:20]}")

# Filtrar stopwords de un texto
sample_tokens = ['the', 'count', 'stood', 'in', 'the', 'doorway']
filtered_tokens = [word for word in sample_tokens if word not in stop_words]

print(f"\nTokens originales: {sample_tokens}")
print(f"Tokens filtrados: {filtered_tokens}")
```

### Stemming y Lemmatization

**Stemming** reduce las palabras a su raíz mediante reglas heurísticas (puede no ser una palabra real).

```python
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

words = ['running', 'runs', 'ran', 'runner', 'easily', 'fairly']
stemmed = [stemmer.stem(word) for word in words]

print("Palabra original → Stem")
for original, stem in zip(words, stemmed):
    print(f"{original:15} → {stem}")
```

**Lemmatization** reduce las palabras a su forma base (lema) usando conocimiento lingüístico.

```python
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

words = ['running', 'runs', 'ran', 'better', 'are', 'was']
lemmatized = [lemmatizer.lemmatize(word, pos='v') for word in words]

print("\nPalabra original → Lema")
for original, lemma in zip(words, lemmatized):
    print(f"{original:15} → {lemma}")
```

**Diferencia entre stemming y lemmatization:**

```python
test_words = ['studies', 'studying', 'studied', 'studies']

print("Palabra\t\tStemming\tLemmatization")
print("-" * 50)
for word in test_words:
    stem = stemmer.stem(word)
    lemma = lemmatizer.lemmatize(word, pos='v')
    print(f"{word:15}\t{stem:15}\t{lemma}")
```

### Práctica completa: Preprocesar Drácula

Ahora vamos a aplicar todo el preprocesamiento al libro completo:

```python
def preprocess_text(text):
    """
    Preprocesa un texto completo:
    1. Tokenización
    2. Minúsculas
    3. Eliminar stopwords
    4. Eliminar puntuación y números
    5. Lemmatización
    """
    # Tokenizar
    tokens = word_tokenize(text.lower())
    
    # Cargar stopwords
    stop_words = set(stopwords.words('english'))
    
    # Lemmatizer
    lemmatizer = WordNetLemmatizer()
    
    # Filtrar y limpiar
    processed_tokens = []
    for token in tokens:
        # Solo palabras alfabéticas
        if token.isalpha():
            # Eliminar stopwords
            if token not in stop_words:
                # Lemmatizar
                lemma = lemmatizer.lemmatize(token, pos='v')
                processed_tokens.append(lemma)
    
    return processed_tokens

# Preprocesar Drácula
dracula_processed = preprocess_text(dracula_text)

print(f"Tokens originales: {len(dracula_tokens)}")
print(f"Tokens procesados: {len(dracula_processed)}")
print(f"\nPrimeros 50 tokens procesados:")
print(dracula_processed[:50])
```

### Análisis básico: Frecuencia de palabras

```python
from collections import Counter

# Contar frecuencias
word_freq = Counter(dracula_processed)

# Top 20 palabras más comunes
print("Las 20 palabras más frecuentes en Drácula:")
for word, count in word_freq.most_common(20):
    print(f"{word:15} → {count:5} veces")
```

**Visualización de frecuencias:**

```python
import matplotlib.pyplot as plt

# Top 15 palabras
top_words = word_freq.most_common(15)
words, counts = zip(*top_words)

plt.figure(figsize=(12, 6))
plt.bar(words, counts)
plt.xlabel('Palabras')
plt.ylabel('Frecuencia')
plt.title('15 palabras más frecuentes en Drácula')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

***

## Bloque 2: Representación vectorial de texto

### El problema de representar texto

Las máquinas no entienden palabras, necesitan números. Tenemos que convertir texto en vectores numéricos para poder procesarlo matemáticamente.

### Bag of Words (BoW)

El modelo de Bolsa de Palabras representa un documento contando cuántas veces aparece cada palabra, ignorando el orden.

**Ejemplo simple:**

```python
from sklearn.feature_extraction.text import CountVectorizer

# Corpus de ejemplo
corpus = [
    "El conde Drácula vive en un castillo",
    "El castillo está en Transilvania",
    "Drácula es un vampiro"
]

# Crear vectorizador
vectorizer = CountVectorizer()
bow_matrix = vectorizer.fit_transform(corpus)

# Ver el vocabulario
vocabulary = vectorizer.get_feature_names_out()
print("Vocabulario:")
print(vocabulary)

# Ver la matriz
print("\nMatriz BoW:")
print(bow_matrix.toarray())

# Crear DataFrame para visualizar mejor
import pandas as pd
bow_df = pd.DataFrame(bow_matrix.toarray(), columns=vocabulary)
print("\nRepresentación en tabla:")
print(bow_df)
```

**Interpretación:**
Cada fila es un documento, cada columna es una palabra del vocabulario, y cada celda indica cuántas veces aparece esa palabra en ese documento.

### TF-IDF (Term Frequency - Inverse Document Frequency)

TF-IDF mejora BoW dando más peso a palabras importantes y menos a palabras comunes.

**Fórmula conceptual:**
- **TF** (Term Frequency): frecuencia del término en el documento
- **IDF** (Inverse Document Frequency): logaritmo del inverso de la frecuencia del término en todos los documentos
- **TF-IDF** = TF × IDF

**Ejemplo:**

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Mismo corpus
corpus = [
    "El conde Drácula vive en un castillo",
    "El castillo está en Transilvania",
    "Drácula es un vampiro"
]

# Crear vectorizador TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

# Ver resultados
tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray(), 
    columns=tfidf_vectorizer.get_feature_names_out()
)

print("Matriz TF-IDF:")
print(tfidf_df)
```

**Comparación BoW vs TF-IDF:**

```python
print("\nComparación para el documento 1:")
print("\nBoW:")
print(bow_df.iloc[0])
print("\nTF-IDF:")
print(tfidf_df.iloc[0])
```

Observa cómo "el" y "en" (palabras comunes) tienen valores TF-IDF más bajos que "drácula" o "castillo".

### Práctica: Dividir Drácula en capítulos

Vamos a dividir el libro en capítulos para poder analizarlos como documentos separados:

```python
import re

# Dividir por capítulos
chapters = re.split(r'CHAPTER [IVXLC]+', dracula_text)

# Eliminar el primer elemento (texto antes del primer capítulo)
chapters = [ch.strip() for ch in chapters if len(ch.strip()) > 100]

print(f"Número de capítulos encontrados: {len(chapters)}")
print(f"\nLongitud del capítulo 1: {len(chapters[0])} caracteres")
print(f"\nPrimeras líneas del capítulo 1:")
print(chapters[0][:300])
```

### TF-IDF en Drácula por capítulos

```python
# Crear TF-IDF de los capítulos
tfidf_vectorizer = TfidfVectorizer(
    max_features=100,  # Top 100 palabras
    stop_words='english',
    lowercase=True
)

# Ajustar y transformar
tfidf_chapters = tfidf_vectorizer.fit_transform(chapters)

print(f"Forma de la matriz TF-IDF: {tfidf_chapters.shape}")
print(f"({tfidf_chapters.shape[0]} capítulos × {tfidf_chapters.shape[1]} palabras)")

# Ver vocabulario más importante
feature_names = tfidf_vectorizer.get_feature_names_out()
print(f"\nPrimeras 20 palabras del vocabulario:")
print(feature_names[:20])
```

### Encontrar palabras más importantes por capítulo

```python
def get_top_words_per_chapter(chapter_idx, n=10):
    """
    Obtiene las n palabras más importantes de un capítulo
    """
    # Obtener scores TF-IDF del capítulo
    chapter_vector = tfidf_chapters[chapter_idx].toarray()[0]
    
    # Obtener índices ordenados de mayor a menor
    top_indices = chapter_vector.argsort()[-n:][::-1]
    
    # Obtener palabras y scores
    top_words = [(feature_names[i], chapter_vector[i]) for i in top_indices]
    
    return top_words

# Analizar primeros 3 capítulos
for i in range(3):
    print(f"\n--- Capítulo {i+1} ---")
    print("Palabras más relevantes:")
    for word, score in get_top_words_per_chapter(i, n=10):
        print(f"  {word:15} → {score:.4f}")
```

### Similitud entre documentos

Podemos medir qué tan similares son dos documentos usando la similitud del coseno.

**Similitud del coseno:**

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Calcular matriz de similitud entre todos los capítulos
similarity_matrix = cosine_similarity(tfidf_chapters)

print(f"Forma de la matriz de similitud: {similarity_matrix.shape}")
print("\nSimilitud entre los primeros 5 capítulos:")
print(similarity_matrix[:5, :5])
```

**Encontrar capítulos más similares:**

```python
def find_most_similar_chapters(chapter_idx, n=5):
    """
    Encuentra los n capítulos más similares a uno dado
    """
    # Obtener similitudes con todos los capítulos
    similarities = similarity_matrix[chapter_idx]
    
    # Ordenar (excluyendo el mismo capítulo)
    similar_indices = similarities.argsort()[-n-1:-1][::-1]
    
    return [(idx, similarities[idx]) for idx in similar_indices]

# Ejemplo: Capítulo 1
print("\nCapítulos más similares al Capítulo 1:")
for idx, sim in find_most_similar_chapters(0):
    print(f"  Capítulo {idx+1} → similitud: {sim:.4f}")
```

**Visualización de la matriz de similitud:**

```python
plt.figure(figsize=(12, 10))
plt.imshow(similarity_matrix, cmap='YlOrRd', aspect='auto')
plt.colorbar(label='Similitud')
plt.xlabel('Capítulo')
plt.ylabel('Capítulo')
plt.title('Matriz de similitud entre capítulos de Drácula')
plt.tight_layout()
plt.show()
```

***

## Bloque 3: Análisis semántico con Word Embeddings

### Limitaciones de BoW y TF-IDF

Los métodos anteriores tienen un problema: no capturan el significado de las palabras. "Rey" y "reina" son igual de diferentes que "rey" y "tomate".

Los **word embeddings** representan palabras como vectores densos en un espacio donde palabras con significados similares están cerca.

### Word2Vec

Word2Vec es un algoritmo que aprende representaciones vectoriales de palabras basándose en su contexto.

**Dos arquitecturas:**
- **CBOW** (Continuous Bag of Words): predice una palabra dado su contexto
- **Skip-gram**: predice el contexto dada una palabra

**Entrenamiento de Word2Vec en Drácula:**

```python
from gensim.models import Word2Vec

# Preparar datos: lista de oraciones, cada oración es lista de palabras
sentences = sent_tokenize(dracula_text.lower())
tokenized_sentences = [word_tokenize(sent) for sent in sentences]

# Limpiar: solo palabras alfabéticas
cleaned_sentences = []
for sent in tokenized_sentences:
    cleaned_sent = [word for word in sent if word.isalpha()]
    if len(cleaned_sent) > 3:  # Solo oraciones con más de 3 palabras
        cleaned_sentences.append(cleaned_sent)

print(f"Total de oraciones para entrenar: {len(cleaned_sentences)}")
print(f"Ejemplo de oración tokenizada:")
print(cleaned_sentences[10])
```

**Entrenar el modelo:**

```python
# Entrenar Word2Vec
model = Word2Vec(
    sentences=cleaned_sentences,
    vector_size=100,      # Dimensión de los vectores
    window=5,             # Ventana de contexto
    min_count=5,          # Ignorar palabras con frecuencia < 5
    workers=4,            # Threads para entrenamiento
    sg=0                  # 0=CBOW, 1=Skip-gram
)

print(f"Vocabulario aprendido: {len(model.wv)} palabras")
print(f"Dimensión de los vectores: {model.wv.vector_size}")
```

### Explorar el modelo

**Ver el vector de una palabra:**

```python
# Vector de "dracula"
if 'dracula' in model.wv:
    vector = model.wv['dracula']
    print(f"Vector de 'dracula' (primeros 10 elementos):")
    print(vector[:10])
    print(f"\nDimensión completa: {len(vector)}")
```

**Palabras más similares:**

```python
# Palabras similares a "dracula"
if 'dracula' in model.wv:
    similar_words = model.wv.most_similar('dracula', topn=10)
    print("\nPalabras más similares a 'dracula':")
    for word, similarity in similar_words:
        print(f"  {word:15} → {similarity:.4f}")
```

**Más ejemplos:**

```python
test_words = ['vampire', 'blood', 'night', 'castle', 'jonathan', 'mina']

for word in test_words:
    if word in model.wv:
        print(f"\n--- Similares a '{word}' ---")
        similar = model.wv.most_similar(word, topn=5)
        for w, score in similar:
            print(f"  {w:15} → {score:.4f}")
```

### Analogías

Word2Vec puede resolver analogías: "rey es a reina como hombre es a ?"

```python
# Función para analogías
def analogy(word1, word2, word3, model):
    """
    word1 es a word2 como word3 es a ?
    Ejemplo: king - man + woman = queen
    """
    try:
        result = model.wv.most_similar(
            positive=[word2, word3],
            negative=[word1],
            topn=5
        )
        return result
    except KeyError as e:
        return f"Palabra no encontrada: {e}"

# Ejemplos con Drácula
print("\nAnalogia: jonathan - man + woman = ?")
result = analogy('man', 'jonathan', 'woman', model)
if isinstance(result, list):
    for word, score in result:
        print(f"  {word:15} → {score:.4f}")
```

### Similitud entre palabras

```python
# Calcular similitud entre dos palabras
def word_similarity(word1, word2, model):
    try:
        sim = model.wv.similarity(word1, word2)
        return sim
    except KeyError:
        return None

# Ejemplos
pairs = [
    ('dracula', 'vampire'),
    ('dracula', 'jonathan'),
    ('blood', 'night'),
    ('castle', 'house'),
    ('day', 'night')
]

print("\nSimilitud entre pares de palabras:")
for w1, w2 in pairs:
    sim = word_similarity(w1, w2, model)
    if sim:
        print(f"{w1:12} ↔ {w2:12} → {sim:.4f}")
```

### Visualización de embeddings (reducción dimensional)

Para visualizar vectores de 100 dimensiones, los reducimos a 2D usando t-SNE:

```python
from sklearn.manifold import TSNE
import numpy as np

# Seleccionar palabras interesantes
interesting_words = [
    'dracula', 'vampire', 'blood', 'count', 'castle',
    'jonathan', 'mina', 'lucy', 'van', 'helsing',
    'night', 'day', 'death', 'life', 'fear',
    'love', 'window', 'door', 'room', 'sleep'
]

# Filtrar palabras que existen en el vocabulario
existing_words = [w for w in interesting_words if w in model.wv]

# Obtener vectores
vectors = np.array([model.wv[w] for w in existing_words])

# Reducir a 2D con t-SNE
tsne = TSNE(n_components=2, random_state=42, perplexity=5)
vectors_2d = tsne.fit_transform(vectors)

# Visualizar
plt.figure(figsize=(14, 10))
plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1], s=100)

for i, word in enumerate(existing_words):
    plt.annotate(word, xy=(vectors_2d[i, 0], vectors_2d[i, 1]), 
                 fontsize=12, ha='center')

plt.title('Visualización de Word Embeddings de Drácula (t-SNE)')
plt.xlabel('Dimensión 1')
plt.ylabel('Dimensión 2')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### Operaciones con vectores

Los embeddings permiten operaciones algebraicas con significado semántico:

```python
# Ejemplo: vampire + night = ?
if all(w in model.wv for w in ['vampire', 'night']):
    result_vec = model.wv['vampire'] + model.wv['night']
    
    # Encontrar palabra más cercana al vector resultado
    similar = model.wv.similar_by_vector(result_vec, topn=5)
    
    print("\nvampire + night ≈")
    for word, score in similar:
        print(f"  {word:15} → {score:.4f}")
```

***

## Bloque 4: Aplicación práctica completa

### Proyecto: Análisis de personajes en Drácula

Vamos a crear un sistema que analice menciones de personajes y encuentre relaciones entre ellos.

**Paso 1: Identificar personajes principales**

```python
# Lista de personajes conocidos
characters = [
    'dracula', 'jonathan', 'mina', 'lucy', 
    'helsing', 'van', 'seward', 'arthur', 'quincey'
]

# Contar menciones en todo el libro
character_counts = {}

dracula_lower = dracula_text.lower()
for character in characters:
    count = dracula_lower.count(character)
    character_counts[character] = count

# Ordenar por frecuencia
sorted_characters = sorted(character_counts.items(), key=lambda x: x[1], reverse=True)

print("Frecuencia de menciones de personajes:")
for char, count in sorted_characters:
    print(f"{char:15} → {count:5} menciones")
```

**Paso 2: Co-ocurrencia de personajes**

Vamos a ver qué personajes aparecen juntos en los mismos capítulos:

```python
# Matriz de co-ocurrencia
cooccurrence = np.zeros((len(characters), len(characters)))

for i, char1 in enumerate(characters):
    for j, char2 in enumerate(characters):
        if i != j:
            # Contar capítulos donde ambos aparecen
            count = sum(1 for ch in chapters 
                       if char1 in ch.lower() and char2 in ch.lower())
            cooccurrence[i][j] = count

# Visualizar
cooccurrence_df = pd.DataFrame(
    cooccurrence, 
    index=characters, 
    columns=characters
)

print("\nMatriz de co-ocurrencia de personajes:")
print(cooccurrence_df)
```

**Visualización de la red de personajes:**

```python
plt.figure(figsize=(10, 8))
plt.imshow(cooccurrence, cmap='Blues', aspect='auto')
plt.colorbar(label='Co-apariciones')
plt.xticks(range(len(characters)), characters, rotation=45)
plt.yticks(range(len(characters)), characters)
plt.title('Co-ocurrencia de personajes en Drácula')
plt.tight_layout()
plt.show()
```

**Paso 3: Contexto de personajes usando Word2Vec**

```python
# Palabras asociadas con cada personaje
print("\n" + "="*50)
print("CONTEXTO SEMÁNTICO DE PERSONAJES")
print("="*50)

for character in ['dracula', 'jonathan', 'mina', 'lucy']:
    if character in model.wv:
        print(f"\n--- Palabras asociadas con '{character}' ---")
        similar = model.wv.most_similar(character, topn=8)
        for word, score in similar:
            print(f"  {word:15} → {score:.4f}")
```

### Proyecto: Detector de temas en capítulos

Vamos a clasificar capítulos según su tema principal usando clustering.

```python
from sklearn.cluster import KMeans

# Usar la matriz TF-IDF de capítulos que ya tenemos
n_clusters = 5  # 5 temas

# Clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(tfidf_chapters)

print(f"Capítulos asignados a cada cluster:")
for cluster_id in range(n_clusters):
    chapters_in_cluster = [i+1 for i, label in enumerate(cluster_labels) if label == cluster_id]
    print(f"\nCluster {cluster_id}: {len(chapters_in_cluster)} capítulos")
    print(f"  Capítulos: {chapters_in_cluster}")
```

**Identificar palabras clave de cada cluster:**

```python
# Obtener centroides
centroids = kmeans.cluster_centers_

print("\n" + "="*50)
print("PALABRAS CLAVE POR TEMA")
print("="*50)

for cluster_id in range(n_clusters):
    print(f"\n--- Tema {cluster_id} ---")
    
    # Obtener top palabras del centroide
    centroid = centroids[cluster_id]
    top_indices = centroid.argsort()[-10:][::-1]
    
    print("Palabras clave:")
    for idx in top_indices:
        word = feature_names[idx]
        score = centroid[idx]
        print(f"  {word:15} → {score:.4f}")
    
    # Mostrar qué capítulos pertenecen
    chapters_in_cluster = [i+1 for i, label in enumerate(cluster_labels) if label == cluster_id]
    print(f"Capítulos en este tema: {chapters_in_cluster[:5]}...")
```

### Proyecto: Análisis de sentimiento simple

Vamos a hacer un análisis básico de sentimiento usando palabras positivas y negativas:

```python
# Palabras positivas y negativas simples
positive_words = set(['good', 'happy', 'love', 'hope', 'peace', 'joy', 'sweet', 'kind', 'beautiful', 'wonderful'])
negative_words = set(['bad', 'fear', 'death', 'terrible', 'horrible', 'evil', 'dark', 'blood', 'dead', 'horror'])

def sentiment_score(text):
    """
    Calcula un score de sentimiento simple
    """
    tokens = word_tokenize(text.lower())
    
    positive_count = sum(1 for token in tokens if token in positive_words)
    negative_count = sum(1 for token in tokens if token in negative_words)
    
    # Score normalizado
    total = positive_count + negative_count
    if total == 0:
        return 0
    
    score = (positive_count - negative_count) / total
    return score

# Analizar sentimiento por capítulo
chapter_sentiments = []

for i, chapter in enumerate(chapters):
    score = sentiment_score(chapter)
    chapter_sentiments.append(score)
    
print("Sentimiento por capítulo:")
for i, score in enumerate(chapter_sentiments[:10]):  # Primeros 10
    sentiment_label = "POSITIVO" if score > 0 else "NEGATIVO" if score < 0 else "NEUTRAL"
    print(f"Capítulo {i+1:2d} → {score:+.3f} ({sentiment_label})")
```

**Visualizar evolución del sentimiento:**

```python
plt.figure(figsize=(14, 6))
plt.plot(range(1, len(chapter_sentiments)+1), chapter_sentiments, marker='o')
plt.axhline(y=0, color='r', linestyle='--', alpha=0.5)
plt.xlabel('Capítulo')
plt.ylabel('Score de sentimiento')
plt.title('Evolución del sentimiento a lo largo de Drácula')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### Proyecto: Búsqueda semántica

Sistema simple para buscar pasajes similares a una consulta:

```python
def semantic_search(query, chapters, tfidf_vectorizer, tfidf_matrix, top_n=3):
    """
    Busca capítulos más relevantes para una consulta
    """
    # Transformar query con el mismo vectorizador
    query_vector = tfidf_vectorizer.transform([query])
    
    # Calcular similitud con todos los capítulos
    similarities = cosine_similarity(query_vector, tfidf_matrix)[0]
    
    # Obtener top N
    top_indices = similarities.argsort()[-top_n:][::-1]
    
    results = []
    for idx in top_indices:
        results.append({
            'chapter': idx + 1,
            'similarity': similarities[idx],
            'preview': chapters[idx][:200]
        })
    
    return results

# Ejemplos de búsqueda
queries = [
    "vampire blood night",
    "journey castle mountains",
    "lucy mina friends"
]

for query in queries:
    print(f"\n{'='*60}")
    print(f"BÚSQUEDA: '{query}'")
    print('='*60)
    
    results = semantic_search(query, chapters, tfidf_vectorizer, tfidf_chapters)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Capítulo {result['chapter']} (similitud: {result['similarity']:.4f})")
        print(f"   Preview: {result['preview']}...")
```

***

## Bloque 5: Visión moderna del PLN

### Del PLN clásico al PLN moderno

Todo lo que hemos visto hasta ahora son los fundamentos del procesamiento del lenguaje natural. Estos métodos fueron el estado del arte durante muchos años y siguen siendo útiles para entender cómo funcionan los sistemas modernos.

**Línea temporal:**
- **2000s**: BoW, TF-IDF, algoritmos estadísticos
- **2013**: Word2Vec revoluciona la representación de palabras
- **2017**: Aparece la arquitectura Transformer ("Attention is All You Need")
- **2018**: BERT introduce embeddings contextuales
- **2019**: GPT-2 muestra capacidades de generación
- **2020-2023**: Explosión de LLMs (GPT-3, GPT-4, LLaMA, etc.)
- **2024-2026**: LLMs multimodales y especializados

### Limitaciones de los métodos clásicos

**Word2Vec y limitaciones:**
```
Problema: "banco" tiene el mismo vector siempre
- "Me senté en el banco del parque" → vector de "banco"
- "Fui al banco a sacar dinero" → mismo vector de "banco"

Pero los significados son diferentes (mueble vs institución)
```

Los métodos clásicos no capturan el **contexto**.

### Embeddings contextuales: BERT

BERT (Bidirectional Encoder Representations from Transformers) resuelve esto generando vectores diferentes según el contexto.

**Diferencia fundamental:**

```
Word2Vec:
  banco → [0.23, -0.45, 0.12, ...]  (siempre igual)

BERT:
  "sentarse en el banco" → banco → [0.15, -0.23, 0.45, ...]
  "ir al banco"          → banco → [0.67, 0.12, -0.34, ...]
                                    (vectores diferentes)
```

**Arquitectura Transformer:**

La clave es el mecanismo de **atención** (attention):
- Cada palabra "mira" a todas las demás palabras de la oración
- Decide cuáles son importantes para entender su significado
- Genera un vector considerando todo el contexto

**Ejemplo de atención:**

```
Oración: "El animal no cruzó la calle porque estaba cansado"

Cuando procesa "estaba cansado", el modelo debe determinar:
¿A qué se refiere "estaba"? → presta atención a "animal"

Pesos de atención (simplificado):
  estaba → animal: 0.8
  estaba → calle: 0.1
  estaba → cruzó: 0.1
```

### Modelos de lenguaje grandes (LLMs)

**GPT (Generative Pre-trained Transformer):**

GPT y sus sucesores (GPT-2, GPT-3, GPT-4) son modelos autoregresivos que predicen la siguiente palabra.

```
Entrenamiento:
Input:  "El conde Drácula abrió la"
Output: "puerta"

Input:  "El conde Drácula abrió la puerta"
Output: "y"
```

Con billones de ejemplos, el modelo aprende:
- Gramática
- Conocimiento del mundo
- Razonamiento
- Patrones de escritura

**Escala de parámetros:**

```
Word2Vec (Drácula):     ~100K parámetros
BERT base:              110M parámetros
GPT-2:                  1.5B parámetros
GPT-3:                  175B parámetros
GPT-4:                  ~1.7T parámetros (estimado)
```

Más parámetros = más capacidad de aprender patrones complejos.

### Pre-entrenamiento y fine-tuning

**Estrategia moderna:**

1. **Pre-entrenamiento**: Entrenar en millones de textos de internet
   - El modelo aprende lenguaje general
   - Costoso computacionalmente (millones de dólares)

2. **Fine-tuning**: Ajustar en tarea específica
   - Usar el modelo pre-entrenado
   - Entrenar con menos datos para tu tarea específica
   - Mucho más barato y rápido

**Ejemplo:**
```
Base: GPT-4 pre-entrenado en internet
↓
Fine-tune: Ajustar con conversaciones médicas
↓
Resultado: Asistente médico especializado
```

### Capacidades de los LLMs modernos

**Tareas sin entrenamiento adicional (zero-shot):**

```
Tú: "Traduce al francés: The count lives in a castle"
LLM: "Le comte vit dans un château"

Tú: "Resume este texto: [texto largo]"
LLM: [genera resumen]

Tú: "Clasifica el sentimiento: I hate Mondays"
LLM: "Negativo"
```

**Few-shot learning:**

```
Tú: "Clasifica como ficción o no-ficción:
     
     Harry Potter → Ficción
     Historia de Roma → No-ficción
     El Quijote → Ficción
     Drácula → ?"
     
LLM: "Ficción"
```

El modelo aprende la tarea con solo algunos ejemplos.

### Prompting: La nueva forma de programar

Con LLMs, "programar" se convierte en escribir instrucciones en lenguaje natural.

**Ejemplo clásico vs moderno:**

```python
# Enfoque clásico (lo que hemos hecho)
def extract_characters(text):
    # 1. Tokenizar
    tokens = word_tokenize(text)
    # 2. POS tagging
    tagged = pos_tag(tokens)
    # 3. NER (Named Entity Recognition)
    entities = ne_chunk(tagged)
    # 4. Filtrar personas
    characters = [...]
    return characters
```

```
# Enfoque moderno
prompt = """
Extrae todos los personajes del siguiente texto:

[texto]

Lista de personajes:
"""

response = llm.generate(prompt)
```

### Herramientas modernas disponibles

**APIs comerciales:**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
- Cohere

**Modelos open source:**
- Meta LLaMA
- Mistral
- Falcon
- Vicuna

**Plataformas:**
- Hugging Face: repositorio de modelos pre-entrenados
- Ollama: ejecutar LLMs localmente
- LangChain: framework para aplicaciones con LLMs

### Aplicaciones del PLN moderno

**Generación de texto:**
- Asistentes de escritura
- Generación de código
- Creación de contenido

**Comprensión:**
- Chatbots conversacionales
- Análisis de documentos
- Extracción de información

**Traducción:**
- DeepL, Google Translate (usan transformers)
- Traducción multimodal

**Multimodal:**
- Modelos que entienden texto + imágenes
- GPT-4V, Claude 3, Gemini

### Limitaciones y retos actuales

**Alucinaciones:**
Los LLMs pueden generar información falsa con confianza:
```
Usuario: "¿Cuándo murió Drácula histórico?"
LLM: "El verdadero Vlad III murió en 1476" ✓
LLM: "Su castillo en Bran fue construido en 1450" ✗ (incorrecto)
```

**Sesgo:**
Los modelos aprenden sesgos de los datos de entrenamiento.

**Falta de razonamiento real:**
Los LLMs no "entienden" en el sentido humano, solo predicen patrones.

**Costo computacional:**
Entrenar y ejecutar LLMs grandes es muy costoso.

### El futuro del PLN

**Tendencias:**
- Modelos más eficientes (menos parámetros, mejor rendimiento)
- Especialización (modelos para dominios específicos)
- Multimodalidad (texto + imagen + audio + video)
- Razonamiento mejorado
- Agentes autónomos con LLMs

**RAG (Retrieval-Augmented Generation):**
Combinar búsqueda con generación:
```
1. Usuario hace pregunta
2. Sistema busca documentos relevantes (como hicimos con TF-IDF)
3. LLM genera respuesta usando esos documentos
4. Reduce alucinaciones, respuestas más precisas
```

### Relación con lo aprendido

Todo lo que hemos practicado son los fundamentos:

```
Tokenización → Sigue siendo necesaria en LLMs
TF-IDF → Base de sistemas de búsqueda que alimentan RAG
Word2Vec → Precursor de embeddings modernos
Similitud → Se usa para encontrar documentos relevantes
```

Los LLMs no reemplazan estos conceptos, los incorporan y amplían.

### Cómo seguir aprendando

**Próximos pasos:**

1. **Experimentar con Hugging Face:**
   - Probar modelos pre-entrenados
   - Fine-tuning en datos propios

2. **Prompt engineering:**
   - Aprender a diseñar buenos prompts
   - Técnicas como Chain-of-Thought

3. **LangChain:**
   - Construir aplicaciones con LLMs
   - Combinar múltiples herramientas

4. **Ollama (local):**
   - Ejecutar modelos localmente
   - Sin costes de API

5. **Especializarse:**
   - NER (Named Entity Recognition)
   - Question Answering
   - Summarization
   - Machine Translation

***

## Recursos adicionales

**Librerías principales:**
- NLTK: https://www.nltk.org/
- spaCy: https://spacy.io/
- Gensim: https://radimrehurek.com/gensim/
- Hugging Face: https://huggingface.co/

**Datasets:**
- Project Gutenberg: https://www.gutenberg.org/
- Common Crawl: https://commoncrawl.org/
- Wikipedia dumps: https://dumps.wikimedia.org/

**Cursos y tutoriales:**
- CS224N (Stanford): NLP with Deep Learning
- Fast.ai: Practical Deep Learning for Coders
- Hugging Face Course: https://huggingface.co/course

**Papers fundamentales:**
- "Attention Is All You Need" (Transformer)
- "BERT: Pre-training of Deep Bidirectional Transformers"
- "Language Models are Few-Shot Learners" (GPT-3)
