# Guía rápida de Conda desde la terminal

Este fichero ofrece una recopilación de los comandos más importantes de **Conda**
y ejemplos concretos para que puedas trabajar con entornos y paquetes sin
problemas.

> **Requisito previo**: Tener [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
> o [Anaconda](https://www.anaconda.com/products/distribution) instalado en el
> sistema. Los comandos funcionan igual en Linux, macOS y Windows (PowerShell).

---

## Conceptos clave

* **Entorno (environment)**: espacio aislado con su propia versión de Python y
  paquetes.
* **Canal (channel)**: repositorio donde Conda busca paquetes (el predeterminado
  es `defaults`).
* **Paquete**: colección de archivos instalables (Python, C, bibliotecas, etc.).

Conda permite crear múltiples entornos para separar proyectos y evitar
conflictos de dependencias. Nunca instales paquetes directamente en el
entorno base si puedes evitarlo.



##  Comandos esenciales

### Listar entornos existentes

```bash
conda env list
# o equivalentes:
# conda info --envs
```

Salida típica:
```
# conda environments:
#
base                  *  /home/usuario/miniconda3
proyecto1                /home/usuario/miniconda3/envs/proyecto1
```
El asterisco indica el entorno activo.

### Crear un entorno nuevo

```bash
conda create -n mi_entorno python=3.11
```

Explicación:
* `-n mi_entorno` especifica el nombre.
* `python=3.11` fija la versión de Python (opcional: puedes instalar otros
  paquetes de paso).
* Si no pones versión de Python, Conda usa la que tenga configurada por
defecto.

Después de ejecutar el comando, Conda pedirá confirmación antes de
continuar.

### Activar / desactivar entornos

```bash
conda activate mi_entorno   # cambiar al entorno
conda deactivate            # volver al entorno base
```

> **Atajo**: al abrir una nueva terminal, el entorno `base` se activa
> automáticamente si así lo configuras en la instalación.

### Eliminar un entorno

```bash
conda remove -n mi_entorno --all
```

Este comando borra por completo el entorno y todos los paquetes instalados
(en caso de error, usa `--force` con precaución).

### Exportar / reproducir entornos

Para compartir un entorno con otros o volver a crearlo más tarde usa:

```bash
conda env export -n mi_entorno > environment.yml
```

El fichero `environment.yml` contendrá algo como:

```yaml
name: mi_entorno
channels:
  - defaults
dependencies:
  - python=3.11
  - fastapi
  - uvicorn
  - pip:
    - requests
```

Y para recrear el entorno en otra máquina:

```bash
conda env create -f environment.yml
```

### Listar paquetes instalados

```bash
conda list           # paquetes del entorno activo
conda list -n x      # listar otro entorno
```

La salida incluye nombre, versión y canal de cada paquete.

### Instalar paquetes

```bash
conda install requests numpy
```

Si el paquete no existe en los canales configurados puedes usar `-c` para
especificar uno distinto, por ejemplo:

```bash
conda install -c conda-forge pytorch
```

También puedes mezclar instalaciones con `pip`, aunque lo ideal es usar
Conda siempre que sea posible:

```bash
pip install somepackage
```

### Actualizar paquetes / Conda

```bash
conda update package_name   # actualizar un paquete en el entorno activo
conda update --all          # actualizar todos los paquetes
conda update conda          # actualizar el propio gestor Conda
```

### Buscar paquetes

```bash
conda search beautifulsoup4
```

El resultado muestra todas las versiones disponibles y el canal.

### Limpiar caché y liberar espacio

```bash
conda clean --all
```

Esto borra paquetes descargados y archivos temporales. Se puede combinar con
`--dry-run` para ver qué se eliminaría.



##  Ejemplos completos

1. **Crear un entorno con Python 3.10 y FastAPI**

    ```bash
    conda create -n api-demo python=3.10 fastapi uvicorn -y
    conda activate api-demo
    ```

2. **Exportar el entorno actual y compartirlo**

    ```bash
    conda env export > api-demo.yml
    # enviar api-demo.yml a otro desarrollador
    conda env create -f api-demo.yml  # en su máquina
    ```

3. **Actualizar todo antes de empezar un proyecto**

    ```bash
    conda activate api-demo
    conda update --all
    ```

4. **Instalar un paquete de conda-forge**

    ```bash
    conda activate api-demo
    conda install -c conda-forge geopandas
    ```

5. **Eliminar un entorno que ya no necesitas**

    ```bash
    conda deactivate
    conda remove -n api-demo --all
    ``