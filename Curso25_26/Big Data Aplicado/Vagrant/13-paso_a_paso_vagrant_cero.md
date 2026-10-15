# Resumen paso a paso (sin teoría, solo actions + qué hace)

## 0) Prep (host)

* **Instala VirtualBox** — para correr la VM.
* **Descarga ISO Ubuntu Server (amd64)** — archivo `.iso` para instalar el SO.

## 1) Crear VM en VirtualBox

1. **Nueva VM**: pon un nombre claro, p. ej. `ubuntu-25.04-base`.

   * Qué hace: crea la entrada de máquina en VirtualBox.
2. **Asignar recursos**: ≥2 GB RAM, 2 núcleos (mejor 4), disco dinámico ≥25 GB.

   * Qué hace: asegura rendimiento mínimo.
3. **Disco en formato VMDK (opcional)** — más portable.
4. **Adjuntar ISO** a la unidad óptica virtual.

   * Qué hace: permitirá arrancar el instalador.
5. **Red: Adaptador 1 = NAT**.

   * Qué hace: permite el reenvío de puerto que usa Vagrant para SSH.

## 2) Instalar Ubuntu Server (arranque desde ISO)

* Durante instalación:

  * **Crear usuario `vagrant`** con contraseña `vagrant`.

    * Qué hace: credenciales por defecto para compatibilidad Vagrant.
  * **Seleccionar “Instalar OpenSSH”**.

    * Qué hace: levanta SSH para que Vagrant pueda conectar.
  * Particionado guiado; finalizar e iniciar sesión con `vagrant:vagrant`.

## 3) Dentro de la VM — ajustes para box Vagrant

1. **Sudo sin contraseña para `vagrant`**:

   ```bash
   echo "vagrant ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/vagrant
   ```

   * Qué hace: permite aprovisionamiento sin pedir contraseña.
2. **Instalar clave pública "insegura" de Vagrant**:

   ```bash
   sudo mkdir -p /home/vagrant/.ssh
   sudo chmod 0700 /home/vagrant/.ssh
   sudo wget --no-check-certificate \
     https://raw.githubusercontent.com/hashicorp/vagrant/main/keys/vagrant.pub \
     -O /home/vagrant/.ssh/authorized_keys
   sudo chmod 0600 /home/vagrant/.ssh/authorized_keys
   sudo chown -R vagrant:vagrant /home/vagrant/.ssh
   ```

   * Qué hace: permite el bootstrap SSH con la clave pública conocida.
3. **Instalar Guest Additions (para synced folders, vboxsf)**:

   ```bash
   sudo apt-get update
   sudo apt-get install -y build-essential dkms linux-headers-$(uname -r)
   # desde la GUI de VirtualBox: Devices → Insert Guest Additions CD
   sudo mount /dev/cdrom /mnt
   sudo /mnt/VBoxLinuxAdditions.run
   sudo reboot
   ```

   * Qué hace: añade drivers/utilidades; habilita carpetas compartidas.
4. **Limpiar y compactar disco antes de empaquetar**:

   ```bash
   sudo apt-get clean
   sudo dd if=/dev/zero of=/EMPTY bs=1M || true
   sudo rm -f /EMPTY
   sudo shutdown -h now
   ```

   * Qué hace: reduce tamaño del .box.

## 4) Empaquetar VM a .box (host)

* Ejecutar desde host (PowerShell o terminal):

  ```powershell
  vagrant package --base "ubuntu-25.04-base" --output "ubuntu-25.04.box"
  ```

  * Qué hace: exporta la VM a un archivo `.box`.

## 5) Añadir el box al inventario local

* Añadir box localmente:

  ```powershell
  vagrant box add ubuntu/25.04 file:///C:/ruta/a/ubuntu-25.04.box
  vagrant box list   # verificar
  ```

  * Qué hace: registra el box para usarlo en Vagrantfiles.

## 6) Vagrantfile mínimo (lanzamiento)

* Crear directorio de proyecto y `Vagrantfile` mínimo:

  ```ruby
  Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/25.04"
  end
  ```

  * Qué hace: indica qué box usar al `vagrant up`.

## 7) Automatizar creación de usuario (aprovisionamiento)

1. **Script `create_user.sh` (idempotente)** — crea usuario y contraseña:

   ```bash
   #!/bin/bash
   USERNAME=$1
   PASSWORD=$2

   if id -u "$USERNAME" >/dev/null 2>&1; then
     echo "El usuario '$USERNAME' ya existe. Omitiendo la creación."
   else
     sudo useradd -m -s /bin/bash "$USERNAME"
     echo "${USERNAME}:${PASSWORD}" | sudo chpasswd
     sudo usermod -aG sudo "$USERNAME"
     echo "Usuario '$USERNAME' creado con éxito."
   fi
   ```

   * Qué hace: crea usuario solo si no existe (idempotente).
2. **Vagrantfile que ejecuta el script** (ejemplo con variables):

   ```ruby
   NEW_USERNAME = "david"
   NEW_PASSWORD = "david"

   Vagrant.configure("2") do |config|
     config.vm.box = "ubuntu/25.04"

     config.vm.provision "shell",
       path: "create_user.sh",
       args: [NEW_USERNAME, NEW_PASSWORD]
   end
   ```

   * Qué hace: crea `david` al `vagrant up` o `vagrant provision`.

## 8) Usar tu llave SSH personal en lugar del flow automático de Vagrant

1. **Vagrantfile**: deshabilitar inserción de clave y apuntar a tu privada:

   ```ruby
   config.ssh.insert_key = false
   config.ssh.private_key_path = [File.expand_path("~/.ssh/id_rsa")]
   ```

   * Qué hace: evita que Vagrant genere/gestione la clave; usará tu privada.
2. **Aprovisionar la clave pública en la VM** (file + shell):

   * Copia la pública al invitado y muévela a `~/.ssh/authorized_keys` con permisos correctos. Ejemplo integrado:

   ```ruby
   config.vm.provision "file",
     source: File.expand_path("~/.ssh/id_rsa.pub"),
     destination: "/tmp/id_rsa.pub"

   config.vm.provision "shell", inline: <<-SHELL
     mkdir -p /home/vagrant/.ssh
     chmod 700 /home/vagrant/.ssh
     cat /tmp/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
     chmod 600 /home/vagrant/.ssh/authorized_keys
     chown -R vagrant:vagrant /home/vagrant/.ssh

     mkdir -p /home/#{NEW_USERNAME}/.ssh
     chmod 700 /home/#{NEW_USERNAME}/.ssh
     cat /tmp/id_rsa.pub >> /home/#{NEW_USERNAME}/.ssh/authorized_keys
     chmod 600 /home/#{NEW_USERNAME}/.ssh/authorized_keys
     chown -R #{NEW_USERNAME}:#{NEW_USERNAME} /home/#{NEW_USERNAME}/.ssh
   SHELL
   ```

   * Qué hace: autoriza tu clave para `vagrant` y para el nuevo usuario.

## 9) Validación final (comprobar que todo funciona)

* **Reconstruir limpio**:

  ```bash
  vagrant destroy -f
  vagrant up
  ```
* **Ver puertos reenviados**:

  ```bash
  vagrant port
  # buscar: 22 (guest) => 2222 (host)
  ```
* **Conectar desde host con tu ssh**:

  ```bash
  ssh -i ~/.ssh/id_rsa david@127.0.0.1 -p 2222
  ```

  * Qué hace: test directo de autenticación con tu llave (sin usar `vagrant ssh`).

## 10) Comandos rápidos / checklist (para no olvidar)

* Dentro de VM: `echo "vagrant ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/vagrant`
* Instalar Key Vagrant: `wget .../vagrant.pub -O /home/vagrant/.ssh/authorized_keys`
* Guest additions: instalar `build-essential dkms linux-headers-$(uname -r)` → ejecutar instalador ISO
* Limpieza antes de empaquetar: `sudo apt-get clean` + `dd if=/dev/zero of=/EMPTY bs=1M` + `rm /EMPTY`
* Empaquetar: `vagrant package --base "NOMBRE_VM" --output "mi.box"`
* Añadir box: `vagrant box add nombre file:///C:/ruta/mi.box`
