### Ejercicios por Función Intermedia

#### 1. **Reshape y Manipulación de Dimensiones**
- **Ejercicio 1**: Crea un tensor de tamaño \(3 \times 3\), luego usa `torch.reshape()` para cambiar su forma a \(1 \times 9\).
- **Ejercicio 2**: Crea un tensor de tamaño \(5 \times 1 \times 5\), y utiliza `torch.squeeze()` para eliminar la dimensión de tamaño 1.

#### 2. **Concatenación y Combinación**
- **Ejercicio 3**: Crea dos tensores de tamaño \(3 \times 2\) y concaténalos a lo largo de la dimensión 0.
- **Ejercicio 4**: Divide un tensor de tamaño \(10 \times 3\) en 5 tensores de tamaño \(2 \times 3\) usando `torch.chunk()`.

#### 3. **Permutación y Transposición**
- **Ejercicio 5**: Crea un tensor de tamaño \(3 \times 4\) y obtén su transposición usando `torch.transpose()`.
- **Ejercicio 6**: Genera un tensor de tamaño \(2 \times 3 \times 4\) y permútalo para que su forma sea \(4 \times 2 \times 3\).

#### 4. **Reducciones Avanzadas**
- **Ejercicio 7**: Crea un tensor de tamaño \(2 \times 3\) y calcula el producto de todos sus elementos con `torch.prod()`.
- **Ejercicio 8**: Genera un tensor de tamaño \(4 \times 4\) y calcula la suma acumulativa de sus elementos en la dimensión 1.

#### 5. **Lógica Avanzada**
- **Ejercicio 9**: Crea dos tensores de tamaño \(3 \times 3\) con valores aleatorios y usa `torch.where()` para seleccionar los elementos mayores del primer tensor sobre el segundo.
- **Ejercicio 10**: Crea un tensor de tamaño \(5\) con valores aleatorios entre 0 y 1, y selecciona los valores mayores que 0.5 usando `torch.masked_select()`.

#### 6. **Broadcasting y Expansión**
- **Ejercicio 11**: Crea un tensor de tamaño \(5\) y expándelo para que sea de tamaño \(5 \times 3\) usando `torch.expand()`.
- **Ejercicio 12**: Genera un tensor de tamaño \(2 \times 1 \times 4\) y expándelo a \(2 \times 3 \times 4\) para aplicar una operación de broadcasting.

#### 7. **Aleatoriedad y Semillas**
- **Ejercicio 13**: Establece una semilla con `torch.manual_seed()` y genera un tensor aleatorio de tamaño \(3 \times 3\).
- **Ejercicio 14**: Crea un tensor de tamaño \(4\) con probabilidades y genera una muestra binaria usando `torch.bernoulli()`.

---

### Ejercicios Combinados

1. **Ejercicio 15**: Crea un tensor de tamaño \(3 \times 3\), expándelo a \(3 \times 3 \times 3\) y calcula el producto acumulativo de todos los elementos.
2. **Ejercicio 16**: Crea dos tensores de tamaño \(4 \times 4\) con valores aleatorios, concaténalos en la dimensión 0 y calcula el máximo de cada columna.
3. **Ejercicio 17**: Genera un tensor de tamaño \(3 \times 5\), transpónlo y calcula la suma acumulativa en la nueva dimensión 1.
4. **Ejercicio 18**: Establece una semilla para reproducibilidad y genera dos tensores de tamaño \(2 \times 2\). Usa `torch.where()` para comparar ambos y selecciona los valores mayores de uno sobre otro.
5. **Ejercicio 19**: Crea un tensor de tamaño \(4 \times 2\), usa `torch.unsqueeze()` para añadir una nueva dimensión y luego aplana el tensor usando `torch.view()`.
6. **Ejercicio 20**: Genera un tensor de tamaño \(6 \times 2\) con valores entre 0 y 1. Usa `torch.split()` para dividir el tensor en 3 partes iguales, calcula el promedio de cada parte, y expande el resultado para una comparación.
7. **Ejercicio 21**: Genera un tensor aleatorio de tamaño \(3 \times 4\), usa `torch.permute()` para reorganizarlo a tamaño \(4 \times 3\), y calcula la media de cada fila en la nueva disposición.
8. **Ejercicio 22**: Crea un tensor aleatorio de tamaño \(5 \times 5\), expándelo para agregar una dimensión adicional en el segundo eje y luego selecciona los valores mayores a 0.7 con `torch.masked_select()`.
9. **Ejercicio 23**: Usa `torch.manual_seed()` para fijar la aleatoriedad y genera un tensor aleatorio de tamaño \(3 \times 3\). Calcula la suma de los elementos de la diagonal principal.
10. **Ejercicio 24**: Crea un tensor de tamaño \(2 \times 3\), usa `torch.unsqueeze()` para agregar una dimensión en el segundo eje y luego calcula la suma acumulativa en la última dimensión.
