# Tutorial de Multipass: Máquinas Virtuales Ubuntu Ligeras con Hipervisores Nativos
### Para el Ciclo Superior de Big Data & Analytics (BDA)

---

## 1. Aclaración Conceptual Previa: Hipervisores Tipo 1 vs Tipo 2 vs Orquestadores

Antes de empezar, es fundamental entender qué estamos ejecutando en la máquina:

```
VIRTUALIZACIÓN CLÁSICA (Vagrant + VirtualBox)
┌─────────────────────────────────────────────────────────────┐
│ Vagrant (Orquestador / CLI en Ruby)                         │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ VirtualBox (Hipervisor Tipo 2 - Hosted)                      │
├─────────────────────────────────────────────────────────────┤
│ Sistema Operativo Anfitrión (Windows / macOS / Linux)        │
├─────────────────────────────────────────────────────────────┤
│ Hardware Físico (CPU, Memoria, Disco)                       │
└─────────────────────────────────────────────────────────────┘

VIRTUALIZACIÓN MODERNA CON MULTIPASS
┌─────────────────────────────────────────────────────────────┐
│ Multipass (CLI de Canonical)                                │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Hipervisor Nativo / Tipo 1                                  │
│ (Windows: Hyper-V | Linux: KVM | macOS: Hypervisor.framework)│
├─────────────────────────────────────────────────────────────┤
│ Hardware Físico con Soporte de Virtualización por CPU       │
└─────────────────────────────────────────────────────────────┘
```

* **Vagrant NO es un hipervisor:** Es una herramienta de automatización (*Infrastructure as Code* local). Vagrant no crea máquinas por sí mismo; le pide a un proveedor (como VirtualBox) que las cree.
* **VirtualBox es un Hipervisor Tipo 2 (Hosted):** Se instala como un programa cualquiera en tu sistema operativo. Hay una capa de traducción que genera más consumo de CPU y memoria.
* **Multipass utiliza Hipervisores Nativos (Tipo 1 / Kernel-Level):**
  * En **Windows**: utiliza **Hyper-V** (o el Hypervisor Platform nativo de Windows).
  * En **Linux**: utiliza **KVM** (módulo directo en el núcleo Linux).
  * En **macOS**: utiliza el framework nativo de Apple (*Hypervisor.framework*).
  * **Consecuencia directa:** Las máquinas arrancan en segundos, consumen significativamente menos RAM/batería y ofrecen rendimiento casi nativo.

---

## 2. ¿Qué es Multipass y por qué aprenderlo en Big Data?

**Multipass** es una herramienta desarrollada y mantenida por **Canonical** (la empresa detrás de Ubuntu). 

Su filosofía es sencilla: **la velocidad y simplicidad de la CLI de Docker, pero creando Máquinas Virtuales completas con Ubuntu**.

* Cada instancia tiene su propio **kernel independiente**, su demonio **systemd**, su pila de red y su aislamiento real de memoria.
* Para configurar el entorno, en vez de aprender la sintaxis de Ruby (como en el `Vagrantfile`), Multipass utiliza **`cloud-init`** (YAML), que es el estándar universal empleado en **Amazon AWS, Microsoft Azure y Google Cloud**.

---

## 3. Instalación

### En Windows (PowerShell con Administrador):
Puedes instalarlo mediante el gestor de paquetes de Windows:
```powershell
winget install Canonical.Multipass
```
*O descargando el instalador oficial desde [https://multipass.run](https://multipass.run).*
> **Nota para Windows:** Se recomienda tener Hyper-V habilitado (en Windows Pro/Enterprise/Education) o la Plataforma de Máquina Virtual de Windows 10/11.

### En Linux (Ubuntu / Debian / Fedora):
Se instala en un solo comando mediante `snap`:
```bash
sudo snap install multipass
```

### En macOS:
```bash
brew install --cask multipass
```

---

## 4. Guía Práctica de Comandos (Cheat Sheet)

### 4.1 Ver qué versiones de Ubuntu hay disponibles
```bash
multipass find
```
*Muestra las versiones oficiales de Ubuntu listas para descargar (20.04 LTS, 22.04 LTS, 24.04 LTS, etc.).*

### 4.2 Lanzar nuestra primera máquina virtual
Para crear una máquina llamada `nodo1` con 2 CPUs, 2 GB de RAM y 10 GB de disco:
```bash
multipass launch --name nodo1 --cpus 2 --memory 2G --disk 10G 24.04
```
*En unos 20-30 segundos la máquina estará descargada, configurada y en ejecución.*

### 4.3 Ver el estado e IPs de las máquinas
```bash
multipass list
```
**Salida de ejemplo:**
```
Name                    State             IPv4             Image
nodo1                   Running           172.28.140.12    Ubuntu 24.04 LTS
nodo2                   Running           172.28.140.45    Ubuntu 24.04 LTS
```
*(Fíjate que cada máquina recibe su propia IP interna accesible desde el host).*

### 4.4 Entrar en la máquina (Acceso a Shell)
No necesitas configurar SSH ni buscar claves privadas:
```bash
multipass shell nodo1
```
*Te abrirá una terminal directamente como usuario `ubuntu` dentro de la máquina virtual.* Para salir, escribe `exit`.

### 4.5 Ejecutar comandos sin entrar en la máquina
Muy útil para automatizaciones y scripts de administración:
```bash
multipass exec nodo1 -- sudo apt-get update
multipass exec nodo1 -- df -h
```

### 4.6 Compartir carpetas entre el Host y la VM (*Mount*)
Si quieres compartir una carpeta local de tu ordenador (`./mis_datos`) con la máquina virtual:
```bash
multipass mount ./mis_datos nodo1:/home/ubuntu/datos
```
Para dejar de compartir:
```bash
multipass unmount nodo1
```

### 4.7 Transferir archivos directamente
```bash
# Del host a la máquina:
multipass transfer script.sh nodo1:/home/ubuntu/script.sh

# De la máquina al host:
multipass transfer nodo1:/var/log/syslog ./syslog_nodo1.log
```

### 4.8 Gestión del ciclo de vida (Apagar, Borrar y Purgar)
```bash
# Detener una máquina:
multipass stop nodo1

# Volver a arrancarla:
multipass start nodo1

# Marcar para borrar:
multipass delete nodo1

# IMPORTANTE: En Multipass, 'delete' solo manda a la papelera. 
# Para liberar el espacio real en el disco duro del host hay que purgar:
multipass purge
```

---

## 5. Automatización con `cloud-init` (El equivalente moderno al `Vagrantfile`)

En entornos Cloud y DevOps reales no se configuran servidores a mano. Se pasa un archivo declarativo YAML a la máquina al nacer.

Crea un archivo llamado `init-bda.yaml` en tu equipo anfitrión:

```yaml
#cloud-config

# Actualizar repositorios e instalar paquetes base automáticamente
package_update: true
package_upgrade: false
packages:
  - openjdk-17-jdk
  - python3-pip
  - htop
  - net-tools
  - curl
  - git

# Configurar usuarios y claves SSH
users:
  - name: bda_user
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQD... (pega aquí tu clave pública)

# Comandos shell a ejecutar tras el primer arranque
runcmd:
  - echo "Configurando entorno de Big Data..." > /etc/motd
  - echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> /home/bda_user/.bashrc
```

### Lanzar la máquina con esta configuración:
```bash
multipass launch --name cluster-master --cpus 2 --memory 4G --cloud-init init-bda.yaml 24.04
```
La máquina se creará, creará el usuario `bda_user`, instalará Java 17 y Python, inyectará tu clave SSH y dejará el entorno listo para usar sin tocar una sola pantalla.

---

## 6. Desplegar un Mini-Cluster de 3 Nodos en Bucle

Si quieres levantar un cluster de 3 nodos (`worker-1`, `worker-2`, `worker-3`) en cuestión de un minuto:

### En Bash (Linux / macOS):
```bash
for i in {1..3}; do
  multipass launch --name "worker-$i" --cpus 1 --memory 2G 24.04
done
multipass list
```

### En PowerShell (Windows):
```powershell
1..3 | ForEach-Object {
    multipass launch --name "worker-$_" --cpus 1 --memory 2G 24.04
}
multipass list
```

---

## 7. Tabla Comparativa para el Alumno: ¿Cuándo usar qué?

| Característica | **Vagrant + VirtualBox** | **Multipass** | **Docker / Docker Compose** |
|---|---|---|---|
| **Tecnología** | Máquina Virtual completa | Máquina Virtual completa | Contenedores (namespaces/cgroups) |
| **Hipervisor** | Tipo 2 (VirtualBox) | Tipo 1 / Nativo (Hyper-V, KVM) | Ninguno (comparte kernel del host) |
| **Sistemas Operativos** | Cualquiera (Ubuntu, Debian, Windows, RedHat...) | **Solo Ubuntu** | Cualquier Linux (imagen de contenedor) |
| **Consumo de Recursos** | Alto (RAM y CPU fija por VM) | Medio-Bajo (muy optimizado) | Mínimo (comparte memoria libre) |
| **Tiempo de Arranque** | 1 - 3 minutos | 15 - 30 segundos | Menos de 2 segundos |
| **Formato de Configuración** | `Vagrantfile` (Sintaxis Ruby) | `cloud-init` (Estándar YAML Cloud) | `Dockerfile` / `docker-compose.yml` |
| **Uso Ideal en Big Data** | Prácticas de redes complejas con IPs fijas arbitrarias y Ansible en local. | Despliegue rápido de nodos Ubuntu reales y aprendizaje de `cloud-init`. | Microservicios, pipelines de Spark/Kafka y bases de datos en producción. |

---

## 8. Ejercicio Propuesto para Clase
1. Instala Multipass en tu equipo.
2. Lanza una máquina llamada `bd-storage` con 2 vCPUs y 2 GB de RAM.
3. Entra por `multipass shell bd-storage` e instala PostgreSQL:
   ```bash
   sudo apt-get update && sudo apt-get install -y postgresql
   ```
4. Comprueba la IP asignada con `multipass list` y verifica desde tu máquina anfitriona que responde a `ping <IP>`.
5. Apaga la máquina y elimina los recursos cuando termines con `multipass stop bd-storage`, `multipass delete bd-storage` y `multipass purge`.
