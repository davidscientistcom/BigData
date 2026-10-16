# El Gran Misterio de las Claves SSH en Vagrant
### ¿Por qué a veces funciona `vagrant ssh`, a veces falla con `Permission denied`, y por terminal manual sí entra?

---

## 1. El Comportamiento Oculto de Vagrant con SSH

Para entender por qué este error vuelve locos a alumnos y administradores por igual, hay que entender qué hace Vagrant **por debajo del capó** cuando descargas una *box* y haces `vagrant up`:

```
┌───────────────────────────────────────────────────────────────┐
│                    TU MÁQUINA (HOST)                          │
│                                                               │
│  Clave privada insegura conocida mundialmente:                │
│  ~/.vagrant.d/insecure_private_key                            │
└───────────────────────────────┬───────────────────────────────┘
                                │  1. Vagrant conecta por primera vez
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                 MÁQUINA VIRTUAL (GUEST)                       │
│                                                               │
│  /home/vagrant/.ssh/authorized_keys                           │
│  (Contiene la clave pública insegura correspondiente)         │
└───────────────────────────────┬───────────────────────────────┘
                                │  2. ¡AQUÍ ESTÁ EL TRUCO!
                                ▼
┌───────────────────────────────────────────────────────────────┐
│              REEMPLAZO AUTOMÁTICO DE SEGURIDAD                │
│                                                               │
│  Por defecto (config.ssh.insert_key = true):                  │
│  Vagrant genera al vuelo un par de claves NUEVAS y aleatorias. │
│  - Guarda la nueva clave privada en:                          │
│    .vagrant/machines/<nombre>/virtualbox/private_key          │
│  - E inyecta la nueva clave pública en authorized_keys.       │
└───────────────────────────────────────────────────────────────┘
```

---

## 2. El Origen del Conflicto: La Condición de Carrera

En nuestras prácticas, queremos que la máquina virtual acepte **nuestra propia clave SSH** (`~/.ssh/vagrant_vm_key`), para que herramientas como **Ansible** o scripts automáticos puedan conectarse sin contraseñas.

El error típico ocurre en el script de aprovisionamiento (*shell provisioner*):

```bash
# ❌ LÍNEA PROBLEMÁTICA:
cat /home/vagrant/.ssh/vagrant_vm_key.pub > /home/vagrant/.ssh/authorized_keys
```

### ¿Qué ocurre al usar `>` (sobrescritura)?
El operador `>` borra **TODO** el contenido que tuviera `authorized_keys` y escribe únicamente tu clave pública personalizada.

Esto provoca tres situaciones desconcertantes:

| Situación | Qué hace el alumno | Qué ocurre | Por qué |
|---|---|---|---|
| **Caso A** | Hace `ssh -i ~/.ssh/vagrant_vm_key vagrant@192.168.33.10` | ✅ **Funciona** | Porque tu clave pública está en `authorized_keys`. |
| **Caso B** | Hace `vagrant ssh` | ❌ **Falla (`Permission denied`)** | Porque Vagrant intenta usar su clave generada en `.vagrant/machines/.../private_key`, ¡pero tu script la acaba de borrar! |
| **Caso C** | Hace `vagrant provision` | ❌ **Se cuelga / Falla** | Vagrant ya no puede entrar a la máquina para ejecutar los scripts porque no tiene acceso. |

> **¿Por qué a veces funcionaba y a veces no?**  
> Si la máquina se iniciaba y el provisionador corría antes o después de la inserción de claves, o si alguien reiniciaba la máquina sin recrearla, el estado de las claves cambiaba de forma impredecible.

---

## 3. Las Dos Soluciones Definitivas

### Solución 1: Coexistencia con `>>` (La más recomendada para clase)
En lugar de sobrescribir el archivo `authorized_keys` con `>`, usamos **`>>` (añadir al final)**:

```bash
# ✅ CORRECTO: Ambas claves coexisten
cat /home/vagrant/.ssh/vagrant_vm_key.pub >> /home/vagrant/.ssh/authorized_keys
```

* **Ventaja:** En `authorized_keys` estarán tanto la clave que usa Vagrant para sus comandos internos (`vagrant ssh`, `vagrant provision`) como tu clave personalizada para Ansible y conexiones directas. Todo funciona a la primera sin tocar nada más.

---

### Solución 2: Control Total desde el `Vagrantfile` (Configuración Profesional)
Si por motivos de seguridad quieres **eliminar completamente la clave por defecto** y usar exclusivamente la tuya, debes avisar a Vagrant en el `Vagrantfile` mediante dos directivas obligatorias:

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  # 1. Decirle a Vagrant que NO genere ni inserte claves nuevas
  config.ssh.insert_key = false

  # 2. Decirle a Vagrant dónde está tu clave privada para 'vagrant ssh'
  config.ssh.private_key_path = [
    "#{Dir.home}/.ssh/vagrant_vm_key",
    "#{Dir.home}/.vagrant.d/insecure_private_key"
  ]

  # 3. Evitar advertencias de known_hosts
  config.ssh.extra_args = ["-o StrictHostKeyChecking=no", "-o UserKnownHostsFile=/dev/null"]

  # ... resto de la configuración ...
end
```

#### ¿Cómo funciona este array de `private_key_path`?
1. Al arrancar la primera vez, Vagrant intentará entrar primero con `vagrant_vm_key`. Como la máquina es virgen y aún no la tiene, fallará esa clave y probará con la segunda: `insecure_private_key`.
2. Con `insecure_private_key` entra con éxito y ejecuta el script de aprovisionamiento que copia tu `vagrant_vm_key.pub`.
3. En las siguientes conexiones (o al hacer `vagrant ssh`), Vagrant usará `vagrant_vm_key` directamente.

---

## 4. Checklist Rápido de Diagnóstico para Alumnos

Si un alumno te dice: *«Profe, `vagrant ssh` no me deja entrar y me pide contraseña»*, sigue este orden:

1. **¿Existe la clave en el Host?**
   Comprobar en PowerShell / Bash:
   ```bash
   ls ~/.ssh/vagrant_vm_key*
   ```
   Deben existir tanto la privada (`vagrant_vm_key`) como la pública (`vagrant_vm_key.pub`).

2. **¿Se usó `>` o `>>`?**
   Revisar el bloque de provisionamiento en el `Vagrantfile`. Si hay un `cat ... > ...authorized_keys`, cambiarlo a `>>`.

3. **¿Tiene los permisos correctos en Linux?**
   SSH rechaza silenciosamente las claves si los permisos son demasiado abiertos:
   ```bash
   chmod 700 /home/vagrant/.ssh
   chmod 600 /home/vagrant/.ssh/authorized_keys
   chown -R vagrant:vagrant /home/vagrant/.ssh
   ```

4. **Si todo falla, entrar con contraseña:**
   El usuario por defecto de Vagrant siempre es `vagrant` con contraseña `vagrant` (a menos que se haya modificado `sshd_config` con `PasswordAuthentication no`).
