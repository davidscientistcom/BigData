## INTRODUCCIÓN
Hadoop es un framework de Big Data, que está mantenido por la fundación Apache. Es un software Open-Source que permite conectar en forma de cluster máquinas de "bajo coste" con el objetivo de realizar trabajos en paralelo.

Google publicó un paper MapReduce en 2004 que inspiró la creación de Hadoop.

Problema: Imaginemos que tenemos un log con cientos de ficheros y de líneas que tienen datos que tengo que procesar. Si tuviéramos que procesar toda la información desde una máquina tendríamos que ir procesando todos los ficheros, lo que es una tarea muy pasada. 

Definamos unos conceptos:

- Problema del camino crítico: Es la cantidad de tiempo que se necesita para terminar el trabajo sin retrasar el siguiente hito o la fecha de finalización. Por lo tanto si alguna máquina se retrasa se retrasa todo el trabajo.


- Problema de fiabilidad:  Si alguna de la máquina que está trabajando se para por algún motivo ¿Qué pasa con el trabajo que se está realizando o los datos que contenía?

- Problema de división equitativa. Las máquinas deberían de tener la misma carga de trabajo, para no tener computadores ociosos o computadores agobiados.

- La división única puede fallar. Se debe de garantizar la capacidad de tolerancia a fallos.

- Agregacion de resultado. Debe de existir un mecanismo por el cual los resultados que van calculando las máquinas se puedan ir agregando para el total.


Hadoop lo que hace es intentar resolver todos estos problemas. Si lo pensamos, con un enfoque tradicional no es posible solventar algunos de los problemas mencionados.

MapReduce nos permite realizar cálculos paralelos sin preocuparnos por cuestiones como fiabilidad , tolerancia a fallos, ...  Para ello se encarga de trabajar en paralelo en un cluster de máquinas donde se han asignado una partición o subconjunto de datos.

Parte de dos 