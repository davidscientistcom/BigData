
## 📚 Índice de Contenidos

1. [Introducción al PLN](#1-introducción-al-pln)
2. [Terminología Fundamental](#2-terminología-fundamental)
3. [Tokenización](#3-tokenización)
4. [Limpieza y Preprocesamiento](#4-limpieza-y-preprocesamiento)
5. [Normalización de Texto](#5-normalización-de-texto)
6. [Visualización de Datos de Texto](#6-visualización-de-datos-de-texto)
7. [Part-of-Speech (POS) Tagging](#7-part-of-speech-pos-tagging)
8. [Ejercicios Prácticos](#8-ejercicios-prácticos)



## 1. Introducción al PLN

### ¿Qué es el Procesamiento del Lenguaje Natural?

El Procesamiento del Lenguaje Natural (PLN o NLP en inglés) es una rama de la inteligencia artificial que se centra en la **interacción entre computadoras y lenguaje humano**. El objetivo es permitir que las máquinas entiendan, interpreten y generen lenguaje humano de manera útil.

### ¿Por qué es difícil procesar el lenguaje natural?

El lenguaje humano presenta varios desafíos únicos:

1. **Ambigüedad**: Las palabras pueden tener múltiples significados
   - "Voy al **banco** a depositar dinero" (institución financiera)
   - "Me senté en el **banco** del parque" (asiento)

2. **Contexto**: El significado depende del contexto
   - "Hace **frío**" (temperatura baja)
   - "Me dejó **frío** su respuesta" (indiferencia)

3. **Variabilidad**: Existen múltiples formas de expresar la misma idea
   - "El perro persigue al gato"
   - "El gato es perseguido por el perro"
   - "Al gato lo persigue el perro"

4. **Errores y variaciones**: Errores ortográficos, jerga, dialectos
   - "Ke onda we" vs "¿Qué pasa, amigo?"

5. **Conocimiento del mundo**: Requiere información contextual
   - "El trofeo no cabe en la maleta porque es muy grande"
   - ¿Qué es muy grande? ¿El trofeo o la maleta?

### Aplicaciones del PLN en la vida real

- **Asistentes virtuales**: Siri, Alexa, Google Assistant
- **Traducción automática**: Google Translate, DeepL
- **Análisis de sentimientos**: Análisis de opiniones en redes sociales
- **Chatbots**: Atención al cliente automatizada
- **Resumen automático**: Generación de resúmenes de documentos
- **Corrección ortográfica y gramatical**: Microsoft Word, Grammarly
- **Motores de búsqueda**: Google, Bing
- **Clasificación de emails**: Spam vs No Spam



## 2. Terminología Fundamental

Antes de sumergirnos en el código, es crucial entender los términos básicos del PLN.

### Corpus (plural: Corpora)

Un **corpus** es una colección de documentos de texto. Es el conjunto de datos con el que trabajamos.

**Ejemplos:**
- Una colección de artículos de noticias
- Todos los tweets sobre un tema específico
- Conjunto de reseñas de productos
- Documentos legales de una empresa

```python
# Ejemplo de corpus simple
corpus = [
    "Me encanta el procesamiento del lenguaje natural",
    "Python es un lenguaje de programación excelente para PLN",
    "Los modelos de lenguaje están revolucionando la IA"
]
```

### Documento

Un **documento** es una unidad individual dentro del corpus. Puede ser:
- Un artículo completo
- Un tweet
- Una reseña
- Un párrafo

### Token

Un **token** es la unidad mínima de procesamiento. Generalmente es una palabra, pero también puede ser:
- Un número
- Un signo de puntuación
- Un símbolo especial

**Ejemplo:**
```
Texto original: "¡Hola, mundo!"
Tokens: ["¡", "Hola", ",", "mundo", "!"]
```

### Tokenización

Es el **proceso de dividir un texto en tokens**. Es el primer paso fundamental en casi cualquier tarea de PLN.

### N-gramas

Los **n-gramas** son secuencias continuas de n elementos (palabras) del texto.

**Ejemplo con la frase: "Me gusta programar en Python"**

- **Unigramas (n=1)**: "Me", "gusta", "programar", "en", "Python"
- **Bigramas (n=2)**: "Me gusta", "gusta programar", "programar en", "en Python"
- **Trigramas (n=3)**: "Me gusta programar", "gusta programar en", "programar en Python"

Los n-gramas son útiles para:
- Capturar contexto local
- Modelado de lenguaje
- Extracción de frases clave

### Morfema

El **morfema** es la forma base de una palabra, sin flexiones ni derivaciones.

**Ejemplo:**
```
Palabra: "antinacionalista"
├── Prefijo: "anti-" (morfema)
├── Raíz: "nacional" (morfema base)
└── Sufijo: "-ista" (morfema)
```

### Léxico

El **léxico** es el conjunto completo de palabras y frases utilizadas en un idioma o dominio específico.



## 3. Tokenización

La tokenización es el proceso de **dividir el texto en unidades más pequeñas** (tokens). Es el primer paso en casi cualquier pipeline de PLN.

### 3.1 Instalación de bibliotecas necesarias

Primero, instalamos las bibliotecas que vamos a usar:

```python
# En la terminal o celda de Jupyter
!pip install nltk
!pip install gensim
!pip install wordcloud
!pip install matplotlib
!pip install spacy
```

### 3.2 Configuración inicial de NLTK

```python
import nltk

# Descargar recursos necesarios
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

print("¡Recursos descargados exitosamente!")
```

### 3.3 Tokenización por espacios en blanco

La forma más simple de tokenización es dividir el texto por espacios.

```python
texto = "El procesamiento del lenguaje natural es fascinante"

# Tokenización simple con split()
tokens_simple = texto.split()
print("Tokens:", tokens_simple)
# Output: ['El', 'procesamiento', 'del', 'lenguaje', 'natural', 'es', 'fascinante']

# Contar tokens
print(f"Número de tokens: {len(tokens_simple)}")
```

**Problema con este enfoque:**

```python
texto_problematico = "¡Hola! ¿Cómo estás? Me llamo Juan."
tokens = texto_problematico.split()
print("Tokens:", tokens)
# Output: ['¡Hola!', '¿Cómo', 'estás?', 'Me', 'llamo', 'Juan.']
# Nota: La puntuación queda pegada a las palabras
```

### 3.4 Tokenización con expresiones regulares

Podemos usar expresiones regulares para tokenizar de forma más sofisticada.

```python
import re

texto = "El correo es: juan@email.com, y el teléfono: 555-1234"

# Tokenizar separando por espacios y signos de puntuación
tokens_re = re.findall(r'\w+', texto)
print("Tokens:", tokens_re)
# Output: ['El', 'correo', 'es', 'juan', 'email', 'com', 'y', 'el', 'teléfono', '555', '1234']

# Tokenizar conservando la puntuación
tokens_re2 = re.findall(r'\w+|[^\w\s]', texto)
print("Tokens con puntuación:", tokens_re2)
```

**Ejercicio 1:** Modifica la expresión regular para que también capture emails completos.

### 3.5 Tokenización de palabras con NLTK

NLTK ofrece tokenizadores más robustos que manejan mejor la puntuación.

```python
from nltk.tokenize import word_tokenize

texto = "Dr. Smith llegó a las 9:30 a.m. ¡Qué puntualidad!"

tokens = word_tokenize(texto, language='spanish')
print("Tokens NLTK:", tokens)
# Output: ['Dr.', 'Smith', 'llegó', 'a', 'las', '9:30', 'a.m.', '¡', 'Qué', 'puntualidad', '!']
```

**Ventajas de word_tokenize:**
- Maneja bien las abreviaciones (Dr., a.m.)
- Separa correctamente la puntuación
- Soporta múltiples idiomas

### 3.6 Tokenización de oraciones

A veces necesitamos dividir un texto en oraciones en lugar de palabras.

```python
from nltk.tokenize import sent_tokenize

texto_largo = """
El procesamiento del lenguaje natural es fascinante. 
Permite a las computadoras entender el texto humano. 
¿No es increíble? ¡Definitivamente lo es!
"""

oraciones = sent_tokenize(texto_largo, language='spanish')

print("Número de oraciones:", len(oraciones))
for i, oracion in enumerate(oraciones, 1):
    print(f"{i}. {oracion.strip()}")

# Output:
# Número de oraciones: 4
# 1. El procesamiento del lenguaje natural es fascinante.
# 2. Permite a las computadoras entender el texto humano.
# 3. ¿No es increíble?
# 4. ¡Definitivamente lo es!
```

### 3.7 Ejemplo completo: Tokenización de un texto real

```python
from nltk.tokenize import word_tokenize, sent_tokenize

# Texto de ejemplo sobre IA
texto_ia = """
La inteligencia artificial está transformando el mundo. Los algoritmos de 
aprendizaje automático procesan millones de datos diariamente. ¿Qué nos 
depara el futuro? Según expertos, la IA revolucionará industrias como la 
medicina, transporte y educación. Sin embargo, también plantea desafíos éticos 
importantes. ¡El futuro es ahora!
"""

# Tokenización de oraciones
oraciones = sent_tokenize(texto_ia, language='spanish')
print(f"El texto tiene {len(oraciones)} oraciones\n")

# Tokenización de palabras para cada oración
for i, oracion in enumerate(oraciones, 1):
    palabras = word_tokenize(oracion, language='spanish')
    print(f"Oración {i}: {len(palabras)} tokens")
    print(f"Tokens: {palabras[:10]}...")  # Mostrar solo los primeros 10
    print()

# Tokenización de todas las palabras del texto
todas_las_palabras = word_tokenize(texto_ia, language='spanish')
print(f"Total de tokens en el texto: {len(todas_las_palabras)}")
```

### 3.8 Ejercicio práctico: Análisis básico de un texto

```python
def analizar_texto(texto):
    """
    Función que analiza un texto y devuelve estadísticas básicas
    """
    # Tokenizar oraciones
    oraciones = sent_tokenize(texto, language='spanish')
    
    # Tokenizar palabras
    palabras = word_tokenize(texto, language='spanish')
    
    # Filtrar solo palabras (sin puntuación)
    palabras_solo = [p for p in palabras if p.isalnum()]
    
    # Calcular estadísticas
    stats = {
        'num_caracteres': len(texto),
        'num_oraciones': len(oraciones),
        'num_tokens': len(palabras),
        'num_palabras': len(palabras_solo),
        'promedio_palabras_por_oracion': len(palabras_solo) / len(oraciones) if oraciones else 0,
        'longitud_promedio_palabra': sum(len(p) for p in palabras_solo) / len(palabras_solo) if palabras_solo else 0
    }
    
    return stats

# Probar la función
texto_prueba = """
Python es un lenguaje de programación versátil y poderoso. 
Se usa en ciencia de datos, desarrollo web, automatización y más. 
Su sintaxis clara lo hace ideal para principiantes.
"""

resultados = analizar_texto(texto_prueba)
for clave, valor in resultados.items():
    print(f"{clave}: {valor:.2f}")
```

**Ejercicio 2:** Modifica la función `analizar_texto` para que también devuelva:
- La oración más larga
- La palabra más larga
- Frecuencia de cada palabra



## 4. Limpieza y Preprocesamiento

El texto real es "sucio": contiene ruido, inconsistencias y elementos innecesarios. La limpieza es crucial para obtener buenos resultados.

### 4.1 Problemas comunes en texto real

```python
texto_sucio = """
   ¡¡OFERTA ESPECIAL!! Compra AHORA... solo por $99.99!!!
   
   Visita: https://www.ejemplo.com para más info 📱💻
   
   Email: contacto@empresa.com
   Teléfono: +34-555-1234
   
   #OfertaDelDía #Tecnología @usuario123
"""

print("Texto original:")
print(texto_sucio)
```

### 4.2 Convertir a minúsculas

Convertir todo el texto a minúsculas ayuda a reducir la dimensionalidad del vocabulario.

```python
texto_lower = texto_sucio.lower()
print("Texto en minúsculas:")
print(texto_lower)

# Ejemplo de por qué es importante
palabras = ["Python", "python", "PYTHON", "PyThOn"]
palabras_lower = [p.lower() for p in palabras]
print(f"\nPalabras originales: {len(set(palabras))} únicas")
print(f"Palabras en minúsculas: {len(set(palabras_lower))} únicas")
```

**Cuándo NO convertir a minúsculas:**
- En análisis de sentimientos (mayúsculas pueden indicar emoción)
- En NER (Named Entity Recognition) - los nombres propios son importantes
- Cuando las mayúsculas tienen significado (USA vs usa)

### 4.3 Eliminación de URLs

```python
import re

texto_con_urls = """
Visita mi blog en https://www.miblog.com/articulo o 
mi perfil en http://twitter.com/usuario. 
También tengo un canal: www.youtube.com/canal
"""

# Patrón para URLs
patron_url = r'https?://\S+|www\.\S+'
texto_sin_urls = re.sub(patron_url, '', texto_con_urls)

print("Texto sin URLs:")
print(texto_sin_urls)
```

### 4.4 Eliminación de emails

```python
texto_con_emails = """
Contacta con soporte@empresa.com o ventas@empresa.co.uk 
para más información. También puedes escribir a juan.perez@mail.com
"""

# Patrón para emails
patron_email = r'\S+@\S+'
texto_sin_emails = re.sub(patron_email, '', texto_con_emails)

print("Texto sin emails:")
print(texto_sin_emails)
```

### 4.5 Eliminación de menciones y hashtags

```python
texto_social = """
@usuario1 mira esto! #PLN #MachineLearning 
cc: @usuario2 @usuario3 
#InteligenciaArtificial #Python
"""

# Eliminar menciones (@usuario)
texto_sin_menciones = re.sub(r'@\w+', '', texto_social)
print("Sin menciones:", texto_sin_menciones)

# Eliminar hashtags (#tag)
texto_sin_hashtags = re.sub(r'#\w+', '', texto_social)
print("Sin hashtags:", texto_sin_hashtags)

# Eliminar ambos
texto_limpio = re.sub(r'[@#]\w+', '', texto_social)
print("Sin menciones ni hashtags:", texto_limpio)
```

### 4.6 Eliminación de números

```python
texto_con_numeros = """
En 2024, el PIB creció un 3.5%. La empresa tiene 150 empleados 
y facturó $2,500,000. El teléfono es 555-1234.
"""

# Eliminar todos los números
texto_sin_numeros = re.sub(r'\d+', '', texto_con_numeros)
print("Sin números:")
print(texto_sin_numeros)

# Eliminar números pero mantener decimales y separadores
texto_sin_numeros2 = re.sub(r'[0-9]+', '[NUM]', texto_con_numeros)
print("\nNúmeros reemplazados por [NUM]:")
print(texto_sin_numeros2)
```

### 4.7 Eliminación de puntuación

```python
import string

texto_con_puntuacion = "¡Hola! ¿Cómo estás? Espero que bien... (muy bien)"

# Método 1: Usando string.punctuation
print("Puntuación estándar:", string.punctuation)

texto_sin_puntuacion = texto_con_puntuacion.translate(
    str.maketrans('', '', string.punctuation)
)
print("Sin puntuación:", texto_sin_puntuacion)

# Método 2: Usando expresiones regulares (más flexible)
texto_sin_puntuacion2 = re.sub(r'[^\w\s]', '', texto_con_puntuacion)
print("Sin puntuación (regex):", texto_sin_puntuacion2)

# Método 3: Mantener puntuación importante (., !, ?)
puntuacion_a_eliminar = string.punctuation.replace('.', '').replace('!', '').replace('?', '')
texto_parcial = texto_con_puntuacion.translate(
    str.maketrans('', '', puntuacion_a_eliminar)
)
print("Manteniendo ., !, ?:", texto_parcial)
```

### 4.8 Eliminación de espacios extras

```python
texto_espacios = "Este    texto   tiene     muchos espacios      extras"

# Eliminar espacios extras
texto_limpio = ' '.join(texto_espacios.split())
print("Texto limpio:", texto_limpio)

# Eliminar espacios al inicio y final
texto_con_espacios_extremos = "   texto con espacios   "
texto_sin_espacios = texto_con_espacios_extremos.strip()
print(f"Original: '{texto_con_espacios_extremos}'")
print(f"Limpio: '{texto_sin_espacios}'")
```

### 4.9 Eliminación de caracteres especiales y emojis

```python
texto_emojis = "Me encanta Python 🐍💻! Es increíble 😍🔥"

# Eliminar emojis y caracteres no ASCII
texto_sin_emojis = texto_emojis.encode('ascii', 'ignore').decode('ascii')
print("Sin emojis:", texto_sin_emojis)

# Mantener solo letras, números y espacios
texto_solo_alfanumerico = re.sub(r'[^a-zA-Z0-9\s]', '', texto_emojis)
print("Solo alfanumérico:", texto_solo_alfanumerico)
```

### 4.10 Función de limpieza completa

```python
def limpiar_texto(texto, 
                  minusculas=True,
                  eliminar_urls=True,
                  eliminar_emails=True,
                  eliminar_menciones=True,
                  eliminar_hashtags=False,  # A veces los hashtags son útiles
                  eliminar_numeros=False,
                  eliminar_puntuacion=True,
                  eliminar_espacios_extras=True):
    """
    Función completa para limpiar texto
    
    Parámetros:
    --
    texto : str
        Texto a limpiar
    minusculas : bool
        Convertir a minúsculas
    eliminar_urls : bool
        Eliminar URLs
    eliminar_emails : bool
        Eliminar direcciones de email
    eliminar_menciones : bool
        Eliminar menciones (@usuario)
    eliminar_hashtags : bool
        Eliminar hashtags (#tag)
    eliminar_numeros : bool
        Eliminar números
    eliminar_puntuacion : bool
        Eliminar signos de puntuación
    eliminar_espacios_extras : bool
        Eliminar espacios múltiples
        
    Retorna:
    --
    str
        Texto limpio
    """
    
    # Convertir a minúsculas
    if minusculas:
        texto = texto.lower()
    
    # Eliminar URLs
    if eliminar_urls:
        texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    
    # Eliminar emails
    if eliminar_emails:
        texto = re.sub(r'\S+@\S+', '', texto)
    
    # Eliminar menciones
    if eliminar_menciones:
        texto = re.sub(r'@\w+', '', texto)
    
    # Eliminar hashtags
    if eliminar_hashtags:
        texto = re.sub(r'#\w+', '', texto)
    
    # Eliminar números
    if eliminar_numeros:
        texto = re.sub(r'\d+', '', texto)
    
    # Eliminar puntuación
    if eliminar_puntuacion:
        texto = texto.translate(str.maketrans('', '', string.punctuation))
    
    # Eliminar espacios extras
    if eliminar_espacios_extras:
        texto = ' '.join(texto.split())
    
    return texto


# Ejemplo de uso
texto_original = """
¡SÚPER OFERTA! 🎉 Visita https://www.tienda.com 
Contacto: ventas@tienda.com o @TiendaOficial
#Descuento #Ahorra 50% ¡Solo HOY!
Llama al 555-1234
"""

print("=" * 50)
print("TEXTO ORIGINAL:")
print("=" * 50)
print(texto_original)

print("\n" + "=" * 50)
print("TEXTO LIMPIO:")
print("=" * 50)
texto_limpio = limpiar_texto(texto_original)
print(texto_limpio)

# Ejemplo con diferentes configuraciones
print("\n" + "=" * 50)
print("TEXTO LIMPIO (conservando hashtags):")
print("=" * 50)
texto_limpio2 = limpiar_texto(texto_original, eliminar_hashtags=False)
print(texto_limpio2)
```

### 4.11 Eliminación de stopwords

Las **stopwords** son palabras muy comunes que generalmente no aportan mucho significado (artículos, preposiciones, etc.).

```python
from nltk.corpus import stopwords

# Cargar stopwords en español
stop_words_es = set(stopwords.words('spanish'))

print("Primeras 20 stopwords en español:")
print(list(stop_words_es)[:20])

# Ejemplo de uso
texto = "El procesamiento del lenguaje natural es una rama de la inteligencia artificial"

# Tokenizar
tokens = word_tokenize(texto, language='spanish')
print(f"\nTokens originales ({len(tokens)}):", tokens)

# Filtrar stopwords
tokens_filtrados = [palabra for palabra in tokens if palabra.lower() not in stop_words_es]
print(f"\nTokens sin stopwords ({len(tokens_filtrados)}):", tokens_filtrados)

# Ver qué palabras se eliminaron
palabras_eliminadas = [p for p in tokens if p.lower() in stop_words_es]
print(f"\nPalabras eliminadas: {palabras_eliminadas}")
```

**Cuándo NO eliminar stopwords:**
- Análisis de sentimientos (negaciones son importantes: "no me gusta")
- Traducción automática
- Generación de texto
- Preguntas y respuestas

### 4.12 Personalizar lista de stopwords

```python
# Agregar stopwords personalizadas
stop_words_custom = stop_words_es.copy()
stop_words_custom.update(['señor', 'señora', 'favor', 'etc'])

# O crear una lista completamente personalizada
mi_lista_stopwords = {'el', 'la', 'de', 'y', 'a', 'en'}

texto = "El señor García vive en Madrid y trabaja en Barcelona"
tokens = word_tokenize(texto.lower(), language='spanish')

tokens_sin_custom = [p for p in tokens if p not in stop_words_custom]
print("Con stopwords personalizadas:", tokens_sin_custom)
```

### 4.13 Ejercicio: Pipeline completo de limpieza

```python
def pipeline_limpieza_completo(texto):
    """
    Pipeline completo de limpieza de texto
    """
    print("PASO 1: Texto original")
    print(f"Longitud: {len(texto)} caracteres")
    print(texto[:200] + "...")
    
    print("\nPASO 2: Convertir a minúsculas")
    texto = texto.lower()
    print(texto[:200] + "...")
    
    print("\nPASO 3: Eliminar URLs, emails y menciones")
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    texto = re.sub(r'\S+@\S+', '', texto)
    texto = re.sub(r'@\w+', '', texto)
    print(texto[:200] + "...")
    
    print("\nPASO 4: Eliminar puntuación")
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    print(texto[:200] + "...")
    
    print("\nPASO 5: Tokenizar")
    tokens = word_tokenize(texto, language='spanish')
    print(f"Número de tokens: {len(tokens)}")
    print(f"Primeros 20 tokens: {tokens[:20]}")
    
    print("\nPASO 6: Eliminar stopwords")
    stop_words = set(stopwords.words('spanish'))
    tokens_filtrados = [t for t in tokens if t not in stop_words]
    print(f"Tokens después de eliminar stopwords: {len(tokens_filtrados)}")
    print(f"Primeros 20 tokens: {tokens_filtrados[:20]}")
    
    print("\nPASO 7: Filtrar palabras muy cortas")
    tokens_finales = [t for t in tokens_filtrados if len(t) > 2]
    print(f"Tokens finales: {len(tokens_finales)}")
    print(f"Primeros 20 tokens: {tokens_finales[:20]}")
    
    return tokens_finales

# Probar con un texto real
texto_ejemplo = """
La inteligencia artificial (IA) está revolucionando múltiples sectores. 
Según expertos, para 2025 el 80% de las empresas habrán adoptado alguna 
forma de IA. ¿Qué significa esto para el futuro del trabajo?

Visita https://www.ejemplo.com para más información o escribe a info@ia.com

#InteligenciaArtificial #Tecnología @ExpertoIA
"""

tokens_limpios = pipeline_limpieza_completo(texto_ejemplo)
```

**Ejercicio 3:** Crea una versión de `pipeline_limpieza_completo` que:
- Reciba parámetros para activar/desactivar cada paso
- Devuelva tanto los tokens como estadísticas del proceso
- Guarde un log de las transformaciones



## 5. Normalización de Texto

La normalización busca reducir las palabras a su forma canónica o base. Hay dos técnicas principales: **stemming** y **lemmatization**.

### 5.1 ¿Qué es el Stemming?

El **stemming** es el proceso de reducir palabras a su raíz o "stem" mediante reglas heurísticas (eliminando sufijos y prefijos).

**Ventajas:**
- Muy rápido
- Simple de implementar
- No requiere diccionario

**Desventajas:**
- Puede generar stems que no son palabras reales
- Menos preciso que lemmatization
- Puede sobre-reducir o sub-reducir

```python
from nltk.stem import SnowballStemmer

# Crear stemmer para español
stemmer_es = SnowballStemmer('spanish')

# Ejemplos de stemming
palabras = [
    'programar', 'programación', 'programador', 'programadores', 'programa',
    'correr', 'corriendo', 'corrió', 'correrá', 'corredor',
    'estudiar', 'estudiante', 'estudiantes', 'estudió', 'estudioso'
]

print("Palabra Original → Stem")
print("-" * 40)
for palabra in palabras:
    stem = stemmer_es.stem(palabra)
    print(f"{palabra:20} → {stem}")
```

### 5.2 Problemas del Stemming

```python
# Caso 1: Sobre-reducción (palabras diferentes con el mismo stem)
palabras_diferentes = ['organizar', 'organismo', 'órgano']
print("\nSOBRE-REDUCCIÓN:")
for palabra in palabras_diferentes:
    print(f"{palabra} → {stemmer_es.stem(palabra)}")

# Caso 2: Sub-reducción (misma palabra con stems diferentes)
palabras_iguales = ['mejor', 'mejorar', 'mejora', 'mejoramiento']
print("\nSUB-REDUCCIÓN:")
for palabra in palabras_iguales:
    print(f"{palabra} → {stemmer_es.stem(palabra)}")

# Caso 3: Stems que no son palabras reales
palabras_normales = ['análisis', 'analizar', 'analítico']
print("\nSTEMS NO REALES:")
for palabra in palabras_normales:
    stem = stemmer_es.stem(palabra)
    print(f"{palabra} → {stem}")
```

### 5.3 ¿Qué es la Lematización?

La **lematización** reduce las palabras a su forma base (lema) usando un diccionario y análisis morfológico.

**Ventajas:**
- Produce palabras reales
- Más preciso
- Considera el contexto

**Desventajas:**
- Más lento que stemming
- Requiere diccionario
- Más complejo

```python
# Para español, usamos spaCy que tiene mejor soporte
# !python -m spacy download es_core_news_sm

import spacy

# Cargar modelo en español
nlp = spacy.load('es_core_news_sm')

# Ejemplos de lematización
palabras = [
    'programar', 'programación', 'programador', 'programadores',
    'corriendo', 'corrió', 'correrá', 'corredor',
    'mejor', 'mejores', 'mejorar', 'mejoramiento'
]

print("Palabra Original → Lema")
print("-" * 40)
for palabra in palabras:
    doc = nlp(palabra)
    for token in doc:
        print(f"{token.text:20} → {token.lemma_}")
```

### 5.4 Comparación Stemming vs Lematización

```python
# Crear función de comparación
def comparar_normalizacion(palabras):
    """
    Compara stemming y lematización en una lista de palabras
    """
    print(f"{'Palabra':<20} {'Stem':<20} {'Lema':<20}")
    print("-" * 60)
    
    for palabra in palabras:
        # Stemming
        stem = stemmer_es.stem(palabra)
        
        # Lematización
        doc = nlp(palabra)
        lema = doc[0].lemma_ if doc else palabra
        
        print(f"{palabra:<20} {stem:<20} {lema:<20}")

# Probar con diferentes palabras
palabras_prueba = [
    'corriendo', 'mejor', 'organización', 'análisis',
    'estudiar', 'programadores', 'desarrollando',
    'fui', 'fuiste', 'fue', 'fuimos', 'fueron'
]

comparar_normalizacion(palabras_prueba)
```

### 5.5 Aplicación en texto real

```python
texto = """
Los científicos están desarrollando nuevos algoritmos de aprendizaje automático.
Estos algoritmos pueden analizar grandes cantidades de datos y encontrar patrones
complejos. Las aplicaciones son infinitas: desde diagnósticos médicos hasta
predicciones financieras. Los investigadores creen que estos avances revolucionarán
múltiples industrias en los próximos años.
"""

print("TEXTO ORIGINAL:")
print(texto)

# Tokenizar
tokens = word_tokenize(texto.lower(), language='spanish')
print(f"\nNúmero de tokens: {len(tokens)}")

# Aplicar stemming
tokens_stem = [stemmer_es.stem(token) for token in tokens if token.isalnum()]
print(f"\nTokens con stemming ({len(set(tokens_stem))} únicos):")
print(tokens_stem)

# Aplicar lematización
doc = nlp(texto.lower())
tokens_lema = [token.lemma_ for token in doc if token.is_alpha]
print(f"\nTokens con lematización ({len(set(tokens_lema))} únicos):")
print(tokens_lema)

# Comparar reducción de vocabulario
print(f"\nVocabulario original: {len(set([t for t in tokens if t.isalnum()]))} palabras únicas")
print(f"Vocabulario con stemming: {len(set(tokens_stem))} palabras únicas")
print(f"Vocabulario con lematización: {len(set(tokens_lema))} palabras únicas")
```

### 5.6 ¿Cuándo usar cada uno?

**Usar STEMMING cuando:**
- La velocidad es crítica
- Trabajas con grandes volúmenes de texto
- La precisión exacta no es crucial
- Trabajas en sistemas de búsqueda/recuperación de información

**Usar LEMATIZACIÓN cuando:**
- Necesitas preservar el significado exacto
- Trabajas con análisis de sentimientos
- La interpretabilidad es importante
- Tienes suficientes recursos computacionales

```python
# Ejemplo: Sistema de búsqueda vs Análisis de sentimientos

# BÚSQUEDA (stemming es suficiente)
consulta_busqueda = "programando en Python"
terminos_busqueda = [stemmer_es.stem(t) for t in consulta_busqueda.lower().split()]
print("Términos de búsqueda (stemming):", terminos_busqueda)
# Output: ['program', 'en', 'python']
# Encontrará: "programar", "programador", "programa", etc.

# ANÁLISIS DE SENTIMIENTOS (lematización es mejor)
comentario = "Los mejores programadores son autodidactas"
doc = nlp(comentario.lower())
tokens_analisis = [token.lemma_ for token in doc if token.is_alpha]
print("Análisis de sentimientos (lematización):", tokens_analisis)
# Output: ['bueno', 'programador', 'ser', 'autodidacta']
# Preserva "bueno" en lugar de reducirlo a "buen"
```

### 5.7 Ejercicio: Análisis de frecuencias con normalización

```python
from collections import Counter

def analizar_frecuencias(texto, metodo='lema'):
    """
    Analiza las frecuencias de palabras en un texto
    
    Parámetros:
    --
    texto : str
        Texto a analizar
    metodo : str
        'stem' para stemming, 'lema' para lematización, 'original' para tokens sin normalizar
    
    Retorna:
    --
    Counter
        Contador de frecuencias
    """
    # Limpiar texto
    texto_limpio = limpiar_texto(texto)
    
    # Tokenizar
    tokens = word_tokenize(texto_limpio, language='spanish')
    
    # Filtrar stopwords
    stop_words = set(stopwords.words('spanish'))
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    
    # Normalizar según método
    if metodo == 'stem':
        tokens_normalizados = [stemmer_es.stem(t) for t in tokens]
    elif metodo == 'lema':
        doc = nlp(' '.join(tokens))
        tokens_normalizados = [token.lemma_ for token in doc if token.is_alpha]
    else:
        tokens_normalizados = tokens
    
    # Contar frecuencias
    frecuencias = Counter(tokens_normalizados)
    
    return frecuencias

# Texto de ejemplo
texto_largo = """
La inteligencia artificial está revolucionando la forma en que vivimos y trabajamos.
Los desarrolladores están creando nuevas aplicaciones cada día. Estas aplicaciones
utilizan algoritmos avanzados de aprendizaje automático. El aprendizaje profundo,
una rama del aprendizaje automático, ha demostrado resultados impresionantes en
múltiples áreas. Los investigadores continúan desarrollando mejores algoritmos y
las empresas continúan invirtiendo en esta tecnología revolucionaria.
"""

# Comparar métodos
for metodo in ['original', 'stem', 'lema']:
    print(f"\n{'='*50}")
    print(f"MÉTODO: {metodo.upper()}")
    print(f"{'='*50}")
    
    freq = analizar_frecuencias(texto_largo, metodo)
    print(f"Vocabulario único: {len(freq)} palabras")
    print("\nTop 10 palabras más frecuentes:")
    for palabra, count in freq.most_common(10):
        print(f"  {palabra:20} → {count}")
```

**Ejercicio 4:** Modifica `analizar_frecuencias` para que:
- Genere un gráfico de barras con las 20 palabras más frecuentes
- Calcule el ratio de reducción de vocabulario para cada método
- Identifique bigramas frecuentes



## 6. Visualización de Datos de Texto

La visualización nos ayuda a entender rápidamente patrones en los datos de texto.

### 6.1 Nubes de palabras (Word Clouds)

Las nubes de palabras muestran visualmente las palabras más frecuentes, donde el tamaño indica la frecuencia.

```python
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Texto de ejemplo
texto_visualizar = """
Python es un lenguaje de programación interpretado de alto nivel. Python es 
conocido por su sintaxis clara y legible. Muchos desarrolladores eligen Python
para ciencia de datos, desarrollo web y automatización. La comunidad de Python
es grande y activa. Python tiene excelentes bibliotecas para machine learning,
análisis de datos y visualización. Python es versátil y poderoso.
"""

# Crear nube de palabras básica
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto_visualizar)

# Visualizar
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Nube de Palabras - Básica')
plt.tight_layout(pad=0)
plt.show()
```

### 6.2 Nube de palabras personalizada

```python
# Limpiar y preparar el texto
texto_limpio = limpiar_texto(texto_visualizar)
tokens = word_tokenize(texto_limpio, language='spanish')

# Eliminar stopwords
stop_words = set(stopwords.words('spanish'))
tokens_filtrados = [t for t in tokens if t not in stop_words]

# Unir tokens de nuevo
texto_para_wordcloud = ' '.join(tokens_filtrados)

# Crear nube de palabras personalizada
wordcloud_custom = WordCloud(
    width=1200,
    height=600,
    background_color='white',
    colormap='viridis',  # Esquema de colores
    max_words=50,        # Número máximo de palabras
    relative_scaling=0.5,
    min_font_size=10
).generate(texto_para_wordcloud)

# Visualizar
plt.figure(figsize=(15, 7))
plt.imshow(wordcloud_custom, interpolation='bilinear')
plt.axis('off')
plt.title('Nube de Palabras - Personalizada (sin stopwords)', fontsize=16)
plt.tight_layout(pad=0)
plt.show()
```

### 6.3 Nube de palabras con frecuencias específicas

```python
from collections import Counter

# Calcular frecuencias
frecuencias = Counter(tokens_filtrados)

# Crear nube desde frecuencias
wordcloud_freq = WordCloud(
    width=1200,
    height=600,
    background_color='black',
    colormap='plasma'
).generate_from_frequencies(frecuencias)

# Visualizar
plt.figure(figsize=(15, 7))
plt.imshow(wordcloud_freq, interpolation='bilinear')
plt.axis('off')
plt.title('Nube de Palabras - Desde Frecuencias', fontsize=16, color='white')
plt.tight_layout(pad=0)
plt.show()

# Mostrar top 10 palabras
print("\nTop 10 palabras más frecuentes:")
for palabra, freq in frecuencias.most_common(10):
    print(f"{palabra:15} → {freq}")
```

### 6.4 Gráfico de barras de frecuencias

```python
# Preparar datos
top_n = 15
palabras_top = frecuencias.most_common(top_n)
palabras = [p[0] for p in palabras_top]
counts = [p[1] for p in palabras_top]

# Crear gráfico
plt.figure(figsize=(12, 6))
plt.barh(palabras, counts, color='skyblue', edgecolor='navy')
plt.xlabel('Frecuencia', fontsize=12)
plt.ylabel('Palabra', fontsize=12)
plt.title(f'Top {top_n} Palabras Más Frecuentes', fontsize=14)
plt.gca().invert_yaxis()  # Invertir para que la más frecuente esté arriba
plt.tight_layout()
plt.show()
```

### 6.5 Distribución de longitudes de palabras

```python
# Calcular longitudes
longitudes = [len(token) for token in tokens_filtrados]

# Crear histograma
plt.figure(figsize=(10, 6))
plt.hist(longitudes, bins=range(1, max(longitudes)+2), color='coral', edgecolor='black', alpha=0.7)
plt.xlabel('Longitud de la palabra (caracteres)', fontsize=12)
plt.ylabel('Frecuencia', fontsize=12)
plt.title('Distribución de Longitudes de Palabras', fontsize=14)
plt.xticks(range(1, max(longitudes)+1))
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# Estadísticas
print(f"Longitud promedio: {sum(longitudes)/len(longitudes):.2f} caracteres")
print(f"Longitud mínima: {min(longitudes)} caracteres")
print(f"Longitud máxima: {max(longitudes)} caracteres")
```

### 6.6 Visualización de n-gramas

```python
from nltk import ngrams

def obtener_ngramas(tokens, n=2):
    """
    Obtiene n-gramas de una lista de tokens
    """
    ngramas = list(ngrams(tokens, n))
    ngramas_texto = [' '.join(ngrama) for ngrama in ngramas]
    return Counter(ngramas_texto)

# Obtener bigramas
bigramas = obtener_ngramas(tokens_filtrados, 2)

# Visualizar top bigramas
top_bigramas = bigramas.most_common(10)
bigramas_labels = [b[0] for b in top_bigramas]
bigramas_counts = [b[1] for b in top_bigramas]

plt.figure(figsize=(12, 6))
plt.barh(bigramas_labels, bigramas_counts, color='lightgreen', edgecolor='darkgreen')
plt.xlabel('Frecuencia', fontsize=12)
plt.ylabel('Bigrama', fontsize=12)
plt.title('Top 10 Bigramas Más Frecuentes', fontsize=14)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Obtener trigramas
print("\nTop 5 Trigramas:")
trigramas = obtener_ngramas(tokens_filtrados, 3)
for trigrama, freq in trigramas.most_common(5):
    print(f"{trigrama:40} → {freq}")
```

### 6.7 Ejercicio: Dashboard de análisis de texto

```python
def crear_dashboard_texto(texto):
    """
    Crea un dashboard completo con múltiples visualizaciones
    """
    # Limpiar y preparar
    texto_limpio = limpiar_texto(texto)
    tokens = word_tokenize(texto_limpio, language='spanish')
    stop_words = set(stopwords.words('spanish'))
    tokens_filtrados = [t for t in tokens if t not in stop_words and len(t) > 2]
    
    # Calcular métricas
    frecuencias = Counter(tokens_filtrados)
    bigramas = obtener_ngramas(tokens_filtrados, 2)
    longitudes = [len(t) for t in tokens_filtrados]
    
    # Crear figura con subplots
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. Nube de palabras
    ax1 = fig.add_subplot(gs[0, :])
    wordcloud = WordCloud(
        width=1200, height=300,
        background_color='white',
        colormap='viridis'
    ).generate(' '.join(tokens_filtrados))
    ax1.imshow(wordcloud, interpolation='bilinear')
    ax1.axis('off')
    ax1.set_title('Nube de Palabras', fontsize=14, fontweight='bold')
    
    # 2. Top palabras
    ax2 = fig.add_subplot(gs[1, 0])
    top_palabras = frecuencias.most_common(10)
    palabras = [p[0] for p in top_palabras]
    counts = [p[1] for p in top_palabras]
    ax2.barh(palabras, counts, color='skyblue', edgecolor='navy')
    ax2.set_xlabel('Frecuencia')
    ax2.set_title('Top 10 Palabras', fontsize=12, fontweight='bold')
    ax2.invert_yaxis()
    
    # 3. Top bigramas
    ax3 = fig.add_subplot(gs[1, 1])
    top_bi = bigramas.most_common(10)
    bi_labels = [b[0] for b in top_bi]
    bi_counts = [b[1] for b in top_bi]
    ax3.barh(bi_labels, bi_counts, color='lightgreen', edgecolor='darkgreen')
    ax3.set_xlabel('Frecuencia')
    ax3.set_title('Top 10 Bigramas', fontsize=12, fontweight='bold')
    ax3.invert_yaxis()
    
    # 4. Distribución de longitudes
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.hist(longitudes, bins=range(1, max(longitudes)+2), 
             color='coral', edgecolor='black', alpha=0.7)
    ax4.set_xlabel('Longitud (caracteres)')
    ax4.set_ylabel('Frecuencia')
    ax4.set_title('Distribución de Longitudes', fontsize=12, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    # 5. Estadísticas textuales
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.axis('off')
    
    stats_text = f"""
    ESTADÍSTICAS DEL TEXTO
    
    Tokens totales: {len(tokens)}
    Tokens únicos: {len(set(tokens))}
    Tokens filtrados: {len(tokens_filtrados)}
    Vocabulario único: {len(frecuencias)}
    
    Longitud promedio: {sum(longitudes)/len(longitudes):.2f} caracteres
    Palabra más larga: {max(tokens_filtrados, key=len)} ({len(max(tokens_filtrados, key=len))} chars)
    Palabra más corta: {min(tokens_filtrados, key=len)} ({len(min(tokens_filtrados, key=len))} chars)
    
    Palabra más frecuente: {frecuencias.most_common(1)[0][0]} ({frecuencias.most_common(1)[0][1]} veces)
    """
    
    ax5.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
             verticalalignment='center')
    
    plt.suptitle('Dashboard de Análisis de Texto', fontsize=16, fontweight='bold', y=0.995)
    plt.show()

# Probar con un texto extenso
texto_dashboard = """
La inteligencia artificial y el aprendizaje automático están transformando radicalmente 
nuestra sociedad. Los algoritmos de aprendizaje profundo pueden procesar cantidades 
masivas de datos y encontrar patrones que serían imposibles de detectar para los humanos.

Las aplicaciones son infinitas: desde vehículos autónomos hasta diagnósticos médicos 
avanzados, pasando por sistemas de recomendación y asistentes virtuales. El procesamiento 
del lenguaje natural permite que las máquinas entiendan y generen texto humano con 
una precisión cada vez mayor.

Los desafíos éticos son importantes. Debemos asegurarnos de que estos sistemas sean 
justos, transparentes y beneficiosos para toda la humanidad. El futuro de la IA depende 
de nuestra capacidad para desarrollar tecnología responsable y centrada en las personas.

Python se ha convertido en el lenguaje preferido para desarrollar soluciones de IA y 
aprendizaje automático, gracias a su sintaxis clara y sus poderosas bibliotecas como 
TensorFlow, PyTorch y scikit-learn. La comunidad de desarrolladores continúa creando 
herramientas innovadoras que democratizan el acceso a estas tecnologías.
"""

crear_dashboard_texto(texto_dashboard)
```

**Ejercicio 5:** Extiende `crear_dashboard_texto` para incluir:
- Un gráfico de línea mostrando la frecuencia acumulada de palabras
- Comparación de frecuencias antes y después de normalización
- Identificación de palabras clave usando TF-IDF



## 7. Part-of-Speech (POS) Tagging

El etiquetado gramatical (POS tagging) asigna a cada palabra su categoría gramatical (sustantivo, verbo, adjetivo, etc.).

### 7.1 ¿Qué es POS Tagging?

POS Tagging es el proceso de etiquetar cada palabra de un texto con su parte de la oración correspondiente.

**Categorías principales:**
- **Sustantivos (N)**: Nombran personas, lugares, cosas
- **Verbos (V)**: Indican acciones o estados
- **Adjetivos (A)**: Describen o modifican sustantivos
- **Adverbios (R)**: Modifican verbos, adjetivos u otros adverbios
- **Pronombres (P)**: Sustituyen a sustantivos
- **Preposiciones (ADP)**: Relacionan palabras
- **Conjunciones (C)**: Conectan palabras o frases
- **Determinantes (D)**: Preceden a sustantivos

### 7.2 POS Tagging con NLTK (inglés)

```python
from nltk import pos_tag
from nltk.tokenize import word_tokenize

# Texto en inglés
texto_en = "The quick brown fox jumps over the lazy dog"

# Tokenizar
tokens = word_tokenize(texto_en)

# Etiquetar
tags = pos_tag(tokens)

print("Token        → POS Tag")
print("-" * 30)
for token, tag in tags:
    print(f"{token:12} → {tag}")

"""
Explicación de tags comunes en inglés:
DT  - Determiner (el, la, un, una)
JJ  - Adjective (adjetivo)
NN  - Noun, singular (sustantivo singular)
NNS - Noun, plural (sustantivo plural)
VB  - Verb, base form (verbo en infinitivo)
VBZ - Verb, 3rd person singular present (verbo 3ra persona)
IN  - Preposition (preposición)
"""
```

### 7.3 POS Tagging con spaCy (español)

spaCy proporciona mejor soporte para español y es más preciso.

```python
import spacy

# Cargar modelo de español
nlp = spacy.load('es_core_news_sm')

# Texto de ejemplo
texto_es = "Los científicos desarrollan nuevos algoritmos de aprendizaje automático"

# Procesar
doc = nlp(texto_es)

# Mostrar etiquetas
print("Token           → POS    → Tag Detallado → Explicación")
print("-" * 80)
for token in doc:
    print(f"{token.text:15} → {token.pos_:7} → {token.tag_:15} → {spacy.explain(token.tag_)}")

"""
Principales tags de spaCy en español:
NOUN  - Sustantivo
VERB  - Verbo
ADJ   - Adjetivo
ADV   - Adverbio
DET   - Determinante
ADP   - Adposición (preposición)
PRON  - Pronombre
CONJ  - Conjunción
NUM   - Número
"""
```

### 7.4 Extracción de sustantivos

```python
def extraer_sustantivos(texto):
    """
    Extrae todos los sustantivos de un texto
    """
    doc = nlp(texto)
    sustantivos = [token.text for token in doc if token.pos_ == 'NOUN']
    return sustantivos

texto = """
El procesamiento del lenguaje natural es una rama fascinante de la inteligencia 
artificial. Los investigadores trabajan constantemente en mejorar los algoritmos 
y modelos que permiten a las computadoras entender el lenguaje humano.
"""

sustantivos = extraer_sustantivos(texto)
print("Sustantivos encontrados:")
print(sustantivos)
```

### 7.5 Extracción de verbos

```python
def extraer_verbos(texto):
    """
    Extrae todos los verbos de un texto
    """
    doc = nlp(texto)
    verbos = [token.lemma_ for token in doc if token.pos_ == 'VERB']
    return verbos

verbos = extraer_verbos(texto)
print("\nVerbos encontrados (forma base):")
print(verbos)
```

### 7.6 Análisis morfológico completo

```python
def analisis_morfologico(texto):
    """
    Realiza un análisis morfológico completo
    """
    doc = nlp(texto)
    
    # Contar por categoría
    pos_counts = {}
    for token in doc:
        if token.pos_ not in pos_counts:
            pos_counts[token.pos_] = []
        pos_counts[token.pos_].append(token.text)
    
    # Mostrar resultados
    print("ANÁLISIS MORFOLÓGICO")
    print("=" * 60)
    
    for pos, palabras in sorted(pos_counts.items()):
        print(f"\n{pos} ({len(palabras)} palabras):")
        print(f"  {', '.join(set(palabras))}")
    
    # Mostrar detalles palabra por palabra
    print("\n" + "=" * 60)
    print("DETALLE POR PALABRA")
    print("=" * 60)
    print(f"{'Token':<20} {'Lema':<15} {'POS':<10} {'Morfología'}")
    print("-" * 70)
    
    for token in doc:
        if token.is_alpha:  # Solo palabras, no puntuación
            print(f"{token.text:<20} {token.lemma_:<15} {token.pos_:<10} {token.morph}")

# Probar
texto_complejo = """
Los desarrolladores están creando aplicaciones innovadoras usando inteligencia 
artificial. Estas aplicaciones procesan datos complejos y generan resultados 
sorprendentes. El futuro de la tecnología será revolucionario.
"""

analisis_morfologico(texto_complejo)
```

### 7.7 Identificación de patrones gramaticales

```python
def encontrar_patron(texto, patron):
    """
    Encuentra patrones gramaticales específicos
    
    Parámetros:
    --
    texto : str
        Texto a analizar
    patron : list
        Lista de tags POS a buscar en secuencia
        Ejemplo: ['DET', 'NOUN'] para determinante + sustantivo
    """
    doc = nlp(texto)
    resultados = []
    
    for i in range(len(doc) - len(patron) + 1):
        secuencia = doc[i:i+len(patron)]
        tags = [token.pos_ for token in secuencia]
        
        if tags == patron:
            texto_patron = ' '.join([token.text for token in secuencia])
            resultados.append(texto_patron)
    
    return resultados

# Buscar patrones específicos
texto_patrones = """
El gato negro duerme en el sofá cómodo. 
La casa grande tiene un jardín hermoso. 
Los estudiantes inteligentes aprenden rápido.
"""

# Patrón: Determinante + Sustantivo + Adjetivo (el gato negro)
patron_det_noun_adj = ['DET', 'NOUN', 'ADJ']
resultados = encontrar_patron(texto_patrones, patron_det_noun_adj)

print("Patrón: DET + NOUN + ADJ")
print("Resultados:")
for r in resultados:
    print(f"  - {r}")

# Patrón: Sustantivo + Verbo (estudiantes aprenden)
patron_noun_verb = ['NOUN', 'VERB']
resultados2 = encontrar_patron(texto_patrones, patron_noun_verb)

print("\nPatrón: NOUN + VERB")
print("Resultados:")
for r in resultados2:
    print(f"  - {r}")
```

### 7.8 Desambiguación de palabras

POS tagging ayuda a resolver ambigüedades.

```python
# Palabra "bajo" puede ser adjetivo, sustantivo o verbo
frases_bajo = [
    "El techo es muy bajo",           # Adjetivo
    "Toco el bajo en la banda",       # Sustantivo
    "Yo bajo por las escaleras"       # Verbo
]

print("Desambiguación de 'bajo':")
print("-" * 50)

for frase in frases_bajo:
    doc = nlp(frase)
    for token in doc:
        if 'bajo' in token.text.lower():
            print(f"Frase: {frase}")
            print(f"  → POS: {token.pos_} ({token.tag_})")
            print(f"  → Lema: {token.lemma_}")
            print()
```

### 7.9 Extracción de frases nominales

```python
def extraer_frases_nominales(texto):
    """
    Extrae frases nominales (sustantivo con sus modificadores)
    """
    doc = nlp(texto)
    frases = []
    
    for chunk in doc.noun_chunks:
        frases.append({
            'texto': chunk.text,
            'raiz': chunk.root.text,
            'raiz_pos': chunk.root.pos_
        })
    
    return frases

texto_frases = """
La inteligencia artificial moderna utiliza redes neuronales profundas. 
Los algoritmos avanzados de aprendizaje automático procesan grandes 
cantidades de datos complejos en tiempo real.
"""

frases_nominales = extraer_frases_nominales(texto_frases)

print("FRASES NOMINALES:")
print("-" * 50)
for i, frase in enumerate(frases_nominales, 1):
    print(f"{i}. {frase['texto']}")
    print(f"   Raíz: {frase['raiz']} ({frase['raiz_pos']})")
    print()
```

### 7.10 Aplicación: Generador de resúmenes extractivos

```python
def generar_resumen_extractivo(texto, num_oraciones=3):
    """
    Genera un resumen extractivo basado en frecuencia de sustantivos
    """
    # Dividir en oraciones
    oraciones = sent_tokenize(texto, language='spanish')
    
    # Procesar todo el texto
    doc = nlp(texto)
    
    # Contar frecuencia de sustantivos
    sustantivos = [token.lemma_.lower() for token in doc 
                   if token.pos_ == 'NOUN' and not token.is_stop]
    freq_sustantivos = Counter(sustantivos)
    
    # Puntuar oraciones
    scores = []
    for oracion in oraciones:
        doc_oracion = nlp(oracion)
        score = sum(freq_sustantivos.get(token.lemma_.lower(), 0) 
                   for token in doc_oracion if token.pos_ == 'NOUN')
        scores.append((oracion, score))
    
    # Ordenar por puntuación y tomar las mejores
    scores.sort(key=lambda x: x[1], reverse=True)
    resumen = ' '.join([oracion for oracion, score in scores[:num_oraciones]])
    
    return resumen, freq_sustantivos.most_common(5)

# Texto largo para resumir
texto_largo = """
La inteligencia artificial está revolucionando múltiples industrias en todo el mundo.
Los sistemas de aprendizaje automático pueden analizar patrones complejos en grandes
conjuntos de datos. Las empresas utilizan estos sistemas para mejorar sus operaciones
y tomar decisiones más informadas. Los investigadores continúan desarrollando nuevos
algoritmos más eficientes y precisos. El procesamiento del lenguaje natural permite
que las máquinas entiendan el texto humano. Las aplicaciones incluyen traducción
automática, análisis de sentimientos y generación de texto. Los chatbots utilizan
PLN para mantener conversaciones naturales con usuarios. El futuro de la IA promete
avances aún más impresionantes en los próximos años.
"""

resumen, palabras_clave = generar_resumen_extractivo(texto_largo, 3)

print("RESUMEN:")
print("=" * 60)
print(resumen)
print("\n" + "=" * 60)
print("PALABRAS CLAVE:")
for palabra, freq in palabras_clave:
    print(f"  - {palabra}: {freq} veces")
```



## 8. Ejercicios Prácticos

### Ejercicio 1: Análisis de Tweets

```python
# Dataset de tweets simulados
tweets = [
    "Me encanta #Python! Es el mejor lenguaje para #DataScience 😍",
    "Odio cuando el código no funciona 😤 @desarrollador ayuda!",
    "Nuevo tutorial de #MachineLearning en mi blog: https://example.com/ml",
    "¿Alguien sabe resolver este error? TypeError en línea 42...",
    "¡Conseguí mi certificación en #AI! 🎉🎓 Gracias @mentor"
]

# Tareas:
# 1. Limpiar tweets (eliminar URLs, menciones, hashtags)
# 2. Tokenizar
# 3. Eliminar stopwords
# 4. Calcular frecuencias
# 5. Identificar sentimiento (positivo/negativo) basado en palabras clave

# TU CÓDIGO AQUÍ
```

### Ejercicio 2: Comparador de Documentos

```python
# Dos artículos sobre el mismo tema
doc1 = """
El cambio climático es uno de los mayores desafíos de nuestra era. 
Las temperaturas globales continúan aumentando debido a las emisiones 
de gases de efecto invernadero.
"""

doc2 = """
El calentamiento global representa una amenaza seria para el planeta. 
El aumento de las temperaturas es causado principalmente por la actividad 
humana y las emisiones de CO2.
"""

# Tareas:
# 1. Procesar ambos documentos (limpiar, tokenizar, normalizar)
# 2. Calcular vocabulario común
# 3. Identificar palabras únicas de cada documento
# 4. Calcular similitud basada en palabras compartidas

# TU CÓDIGO AQUÍ
```

### Ejercicio 3: Extractor de Información

```python
texto_noticia = """
Madrid, 15 de marzo de 2024. El presidente del gobierno, Pedro Sánchez,
anunció ayer un nuevo plan de inversión en tecnología por valor de 
1.500 millones de euros. La ministra de Ciencia, Diana Morant, 
explicó que el 60% se destinará a inteligencia artificial y el 40% 
restante a computación cuántica. El plan se implementará entre 2024 y 2027.
"""

# Tareas:
# 1. Extraer todas las fechas
# 2. Extraer todos los nombres propios (usando POS tagging)
# 3. Extraer todas las cantidades numéricas
# 4. Identificar las organizaciones mencionadas

# TU CÓDIGO AQUÍ
```

### Ejercicio 4: Generador de Estadísticas

```python
def analisis_completo_texto(archivo_texto):
    """
    Lee un archivo de texto y genera un informe completo
    
    El informe debe incluir:
    - Número total de palabras
    - Número de palabras únicas
    - Top 20 palabras más frecuentes (sin stopwords)
    - Top 10 bigramas
    - Distribución de partes de la oración
    - Longitud promedio de palabras
    - Longitud promedio de oraciones
    - Lista de palabras más largas
    - Palabras que solo aparecen una vez (hapax legomena)
    """
    # TU CÓDIGO AQUÍ
    pass
```

### Ejercicio 5: Clasificador de Sentimientos Básico

```python
# Listas de palabras positivas y negativas
palabras_positivas = {'excelente', 'bueno', 'genial', 'fantástico', 'increíble', 
                      'maravilloso', 'perfecto', 'amor', 'feliz', 'éxito'}

palabras_negativas = {'malo', 'terrible', 'horrible', 'pésimo', 'odio', 
                      'fracaso', 'triste', 'error', 'problema', 'difícil'}

def clasificar_sentimiento(texto):
    """
    Clasifica un texto como positivo, negativo o neutro
    basándose en las palabras que contiene
    
    Retorna:
    --
    tuple
        (clasificación, score_positivo, score_negativo)
    """
    # TU CÓDIGO AQUÍ
    pass

# Probar con diferentes textos
textos_prueba = [
    "Este producto es excelente, me encanta!",
    "Terrible experiencia, muy malo",
    "El servicio es normal, nada especial"
]

# TU CÓDIGO AQUÍ
```



## 9. Resumen y Mejores Prácticas

### 9.1 Pipeline típico de preprocesamiento

```python
def pipeline_completo(texto):
    """
    Pipeline completo de preprocesamiento de texto
    """
    # 1. Limpieza básica
    texto = texto.lower()
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)  # URLs
    texto = re.sub(r'\S+@\S+', '', texto)  # Emails
    texto = re.sub(r'[@#]\w+', '', texto)  # Menciones y hashtags
    
    # 2. Tokenización
    tokens = word_tokenize(texto, language='spanish')
    
    # 3. Filtrar puntuación y números
    tokens = [t for t in tokens if t.isalpha()]
    
    # 4. Eliminar stopwords
    stop_words = set(stopwords.words('spanish'))
    tokens = [t for t in tokens if t not in stop_words]
    
    # 5. Filtrar palabras muy cortas
    tokens = [t for t in tokens if len(t) > 2]
    
    # 6. Lematización
    doc = nlp(' '.join(tokens))
    tokens_finales = [token.lemma_ for token in doc if token.is_alpha]
    
    return tokens_finales
```

### 9.2 Cuándo aplicar cada técnica

| Técnica | Usar cuando... | No usar cuando... |
||-|-|
| Conversión a minúsculas | Búsqueda, clasificación | NER, análisis de sentimientos |
| Eliminación de stopwords | Búsqueda, topic modeling | Traducción, generación de texto |
| Stemming | Búsqueda rápida, grandes volúmenes | Necesitas precisión exacta |
| Lematización | Análisis semántico, precisión | Procesamiento en tiempo real |
| Eliminación de puntuación | Análisis de palabras | Análisis sintáctico |
| Eliminación de números | Análisis de opiniones | Análisis cuantitativo |

### 9.3 Errores comunes a evitar

```python
# ❌ ERROR: No normalizar antes de comparar
texto1 = "Python es genial"
texto2 = "PYTHON ES GENIAL"
print(texto1 == texto2)  # False

# ✅ CORRECTO:
print(texto1.lower() == texto2.lower())  # True

# ❌ ERROR: No manejar caracteres especiales
texto = "Hola cómo estás"
tokens = texto.split()  # Mantiene tildes

# ✅ CORRECTO (si quieres normalizar):
from unicodedata import normalize
texto_normalizado = normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

# ❌ ERROR: No verificar el idioma
# Usar stopwords en inglés para texto en español

# ✅ CORRECTO:
stop_words_es = set(stopwords.words('spanish'))

# ❌ ERROR: Aplicar todas las técnicas sin pensar
# No siempre necesitas aplicar todo el pipeline

# ✅ CORRECTO:
# Adapta el pipeline a tu tarea específica
```

### 9.4 Optimización de rendimiento

```python
# Para grandes volúmenes de texto:

# 1. Compilar regex una sola vez
import re

PATRON_URL = re.compile(r'https?://\S+|www\.\S+')
PATRON_EMAIL = re.compile(r'\S+@\S+')

def limpiar_rapido(texto):
    texto = PATRON_URL.sub('', texto)
    texto = PATRON_EMAIL.sub('', texto)
    return texto

# 2. Usar sets para stopwords (búsqueda O(1))
stop_words = set(stopwords.words('spanish'))  # ✅ Rápido
# vs
stop_words = stopwords.words('spanish')  # ❌ Lento (lista)

# 3. Procesar por lotes con spaCy
textos = ["texto1", "texto2", "texto3", ...]
for doc in nlp.pipe(textos, batch_size=50):
    # Procesar doc
    pass

# 4. Cachear resultados frecuentes
from functools import lru_cache

@lru_cache(maxsize=10000)
def normalizar_palabra(palabra):
    return stemmer_es.stem(palabra.lower())
```



## 10. Recursos Adicionales y Próximos Pasos

### Bibliotecas importantes:
- **NLTK**: Fundamentos y educación
- **spaCy**: Producción y alto rendimiento
- **Gensim**: Topic modeling y word embeddings
- **TextBlob**: Análisis de sentimientos simple
- **Transformers**: Modelos estado del arte (Hugging Face)

### Conceptos avanzados para estudiar después:
1. **Word Embeddings**: Word2Vec, GloVe, FastText
2. **Topic Modeling**: LDA, NMF
3. **Named Entity Recognition (NER)**
4. **Análisis de Sentimientos avanzado**
5. **Modelos de lenguaje**: BERT, GPT
6. **Secuencia a secuencia**: Traducción, resumen

### Datasets para practicar:
- Reviews de productos (Amazon, Yelp)
- Tweets en español
- Noticias (BBC, El País)
- Libros del Proyecto Gutenberg
- Corpus de la RAE



## Conclusión

El preprocesamiento de texto es fundamental en PLN. Los pasos que hemos visto:

1. **Tokenización**: Dividir texto en unidades
2. **Limpieza**: Eliminar ruido
3. **Normalización**: Reducir variabilidad
4. **Visualización**: Entender los datos
5. **POS Tagging**: Análisis gramatical
