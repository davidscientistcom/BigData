### Desarrollo Teórico del Primer Capítulo

#### 1. Historia de las Redes Neuronales

El origen de las redes neuronales se remonta a los años 1940 y 1950, cuando Warren McCulloch y Walter Pitts propusieron el primer modelo matemático de neuronas artificiales, inspirado en el funcionamiento del cerebro humano. Este modelo, aunque muy simplificado, fue un primer intento de representar cómo las neuronas procesan la información. A medida que las investigaciones avanzaron, en 1958, Frank Rosenblatt desarrolló el concepto del **perceptrón**, que marcaría un hito importante en la evolución de las redes neuronales.

El perceptrón es un modelo de neurona artificial capaz de clasificar datos en dos categorías, ajustando sus parámetros a través del entrenamiento. Sin embargo, este modelo inicial tenía una limitación clave: solo podía resolver problemas donde los datos fueran **linealmente separables**. Esto significa que, si las categorías no podían ser separadas por una línea recta, el perceptrón fallaría.

#### 1.1 Los Primeros Modelos Neuronales (1940-1950)

En 1943, Warren McCulloch y Walter Pitts propusieron un modelo matemático para representar el funcionamiento de las neuronas biológicas. Este modelo estaba basado en la lógica y describía cómo las neuronas pueden conectarse para procesar información. Aunque este enfoque fue innovador, sus aplicaciones prácticas eran limitadas debido a la simplicidad del modelo.

#### 1.2 El Nacimiento del Perceptrón (1958)

En 1958, Frank Rosenblatt introdujo el **perceptrón**, una neurona artificial capaz de realizar tareas de clasificación. A diferencia de los modelos anteriores, el perceptrón podía aprender a través de un proceso de ajuste de sus pesos, lo que le permitía mejorar su desempeño con el tiempo. El perceptrón solo funcionaba correctamente cuando los datos eran **linealmente separables**.

Este concepto de linealidad es clave. Si los datos podían ser divididos por una línea (en el caso de dos dimensiones), el perceptrón podía clasificarlos de manera correcta. Sin embargo, si los datos no eran separables linealmente, como en el caso de problemas más complejos, el perceptrón no lograba encontrar una solución adecuada.

**Ventajas del Perceptrón:**
- Capacidad de aprender de los datos y ajustar sus parámetros.
- Resolución de problemas de clasificación simples, como la clasificación de datos linealmente separables.

**Limitaciones del Perceptrón:**
- Incapacidad de resolver problemas no linealmente separables, como el problema clásico de la puerta XOR.

#### 1.3 Dificultades y Críticas al Perceptrón (1970)

A finales de los años 60, Marvin Minsky y Seymour Papert publicaron un libro titulado *Perceptrons* (1969), donde demostraban que el perceptrón no podía resolver problemas complejos. Esto llevó a una pausa en la investigación sobre redes neuronales, conocida como el "invierno de las redes neuronales". Durante los años 70, el enfoque de la inteligencia artificial se desvió hacia otros métodos, como los sistemas basados en reglas.

#### 2. Inspiración Biológica

Las redes neuronales artificiales están inspiradas en el funcionamiento del cerebro humano. Una **neurona biológica** se compone de tres partes principales:
- **Dendritas**: reciben señales de otras neuronas.
- **Soma**: procesa las señales y, si son lo suficientemente fuertes, dispara un impulso.
- **Axón**: transmite el impulso a otras neuronas.

![](images/neurona.png)

En las redes neuronales artificiales, cada neurona recibe múltiples entradas, realiza una operación matemática sobre estas, y produce una salida, que se transmite a las siguientes neuronas. Las neuronas artificiales, aunque simplificadas, capturan la esencia del procesamiento de información en las neuronas biológicas.

#### 3. El Perceptrón: La Neurona Artificial

El **perceptrón** es el modelo básico de una neurona artificial. Consiste en un conjunto de entradas, cada una con un peso asociado. La neurona realiza una suma ponderada de estas entradas y las compara con un umbral para determinar la salida, que puede ser 0 o 1. Matemáticamente, el perceptrón se describe como:
![](images/estructura_perceptron.png)

$$
y = f\left(\sum_{i=1}^{n} w_i x_i + b\right)
$$

Donde:
- $x_i$ son las entradas,
- $w_i$ son los pesos,
- $b$ es el sesgo,
- $f$ es una función de activación.

El perceptrón es capaz de clasificar correctamente datos que sean **linealmente separables**, pero su limitación radica en su incapacidad para resolver problemas donde no se puede trazar una línea o un plano que separe las clases.

#### 4. Problemas Linealmente Separables y No Linealmente Separables

**Problemas linealmente separables** son aquellos en los que las clases de datos pueden ser divididas por una línea (en dos dimensiones) o un hiperplano (en dimensiones mayores). 

##### Ejemplo de problema linealmente separable:
Un conjunto de puntos en un plano donde los puntos de una clase están claramente separados de los de otra por una línea recta.

```
Clase 1 (◯) y Clase 2 (×)

◯ ◯ ◯ ◯
          
          ← Línea separadora →
          
× × × ×
```
![](images/separable_and.png)
**Problemas no linealmente separables** son aquellos en los que no es posible dividir las clases mediante una línea o un plano. Un ejemplo clásico de este tipo de problema es el XOR.


##### Ejemplo de problema no linealmente separable:
```
Clase 1 (◯) en el centro, Clase 2 (×) alrededor

    × × ×
   ×     ×
  ×   ◯   ×
   × ◯ ◯ ×
    × × ×
```
![](images/no_separable_xor.png)







