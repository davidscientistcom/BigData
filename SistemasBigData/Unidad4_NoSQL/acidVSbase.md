## 1. ACID: El estándar de las Relacionales (SQL)

Este modelo (usado por MySQL, PostgreSQL, Oracle) está diseñado para situaciones críticas donde **no se puede perder ni un centavo**. Piensa en un banco.

Las siglas significan:

* **A - Atomicidad (Atomicity):** "Todo o nada". Una operación compleja se trata como una unidad indivisible.
* *Ejemplo:* Si transfieres dinero de la cuenta A a la B, y el sistema falla justo después de restar el dinero de A pero antes de sumarlo a B, la base de datos **deshace** todo. El dinero nunca se pierde en el limbo.


* **C - Consistencia (Consistency):** La base de datos siempre pasa de un estado válido a otro válido, respetando todas las reglas (restricciones de integridad).
* *Ejemplo:* Si una columna "Edad" no acepta números negativos, la base de datos rechazará cualquier transacción que intente guardar un "-5".


* **I - Aislamiento (Isolation):** Las operaciones simultáneas no interfieren entre sí.
* *Ejemplo:* Si dos personas intentan comprar el último asiento de un avión al mismo tiempo, el sistema las pone en "fila". Una compra, la otra recibe un error de "agotado".


* **D - Durabilidad (Durability):** Una vez que el sistema dice "Guardado", es para siempre, incluso si se va la luz un segundo después.

> **Ideal para:** Sistemas financieros, inventarios médicos, comercio electrónico (pagos).



## 2. BASE: El estándar de NoSQL (Escalabilidad)

Cuando internet creció (Google, Amazon, Facebook), ACID se volvió un problema. Es difícil mantener "consistencia perfecta" instantánea cuando tienes datos repartidos en 500 servidores por todo el mundo. Surge BASE, que sacrifica la exactitud inmediata por la velocidad y la disponibilidad.

Las siglas significan:

* **BA - Disponibilidad Básica (Basically Available):** El sistema garantiza que siempre responderá, incluso si algunos nodos o servidores fallan.
* *La trampa:* Puede que la respuesta no sea la versión más reciente del dato, pero el sistema **no se cae**.


* **S - Estado Flexible (Soft State):** El estado del sistema puede cambiar con el tiempo, incluso sin recibir nuevas órdenes, debido a la replicación de datos.
* *Traducción:* El dato no es "sólido" instantáneamente en todos lados.


* **E - Consistencia Eventual (Eventual Consistency):** Esta es la clave. Si dejas de enviar cambios, **eventualmente** todos los servidores tendrán el mismo dato.
* *Ejemplo:* Tú le das "Me gusta" a una foto. Tu amigo en Japón quizás no vea ese "Me gusta" hasta dentro de 5 segundos. No pasa nada grave; eventualmente lo verá.



> **Ideal para:** Redes sociales, análisis de big data, catálogos de productos masivos, feeds de noticias.

---

## Comparativa Rápida

| Característica | ACID (Relacional) | BASE (NoSQL) |
| --- | --- | --- |
| **Prioridad** | Consistencia y seguridad del dato. | Disponibilidad y escalabilidad. |
| **¿Cuándo falla?** | Si no puede garantizar la integridad, rechaza la operación. | Prefiere responder con datos viejos a no responder. |
| **Sincronización** | Inmediata (Strong Consistency). | Con retardo (Eventual Consistency). |
| **Escalabilidad** | Vertical (servidores más potentes). | Horizontal (más servidores baratos). |
| **Caso de uso** | Banco, Bolsa de Valores. | Contador de vistas de YouTube, Twitter. |
