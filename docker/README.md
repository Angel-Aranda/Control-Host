
# Control-Host Docker

> **Opciones de despliegue:**
>
> - [Despliegue Automático (auto)](./auto/): Scripts y Docker Compose para levantar todo automáticamente.
> - [Despliegue Manual (manual)](./manual/): Instrucciones para lanzar los servicios paso a paso o usando imágenes ya subidas.


## Índice

1. [Introducción](#introducción)
2. [Requisitos previos](#requisitos-previos)
3. [Inicio rápido](#inicio-rápido)
    - [Windows (PowerShell)](#windows-powershell)
    - [Linux (Bash)](#linux-bash)
4. [¿Cómo funciona?](#cómo-funciona)
5. [Uso de la imagen preconstruida](#uso-de-la-imagen-preconstruida)
6. [Notas sobre el UUID](#notas-sobre-el-uuid)

---

## Introducción

Este proyecto permite desplegar **Control-Host** usando Docker Compose, separando el backend Python (Gunicorn) y el proxy inverso Nginx en contenedores distintos. El sistema requiere el UUID del equipo para funcionar correctamente.

## Requisitos previos

- Docker y Docker Compose instalados en tu sistema.
- Acceso a PowerShell (Windows) o Bash (Linux).

## Inicio rápido

### Windows (PowerShell)

Ejecuta el script:

```powershell
./create.ps1
```

### Linux (Bash)

Ejecuta el script:

```bash
./create.sh
```

Ambos scripts:
- Obtienen el UUID del equipo y lo guardan en el archivo `.env`.
- Construyen y levantan los contenedores con Docker Compose.

## ¿Cómo funciona?

1. El script (`create.ps1` o `create.sh`) obtiene el UUID del equipo y lo guarda en `.env`.
2. Docker Compose levanta dos servicios:
    - **python**: ejecuta la aplicación backend con Gunicorn.
    - **nginx**: actúa como proxy inverso y expone el servicio en el puerto 80.
3. Nginx redirige las peticiones al backend Python usando el nombre del servicio interno (`python`).

## Uso de la imagen preconstruida

Si prefieres no construir la imagen, puedes usar la imagen `control-host:latest` directamente. **Recuerda:** necesitas proporcionar el UUID igualmente.

Ejemplo:

```bash
docker run -d -p 80:80 -e PC_UUID=<TU_UUID> --name control-host control-host:latest
```

## Notas sobre el UUID

- El sistema requiere el UUID del equipo para funcionar correctamente.
- Si no se proporciona, la aplicación puede no comportarse como se espera.
- Los scripts de inicio (`create.ps1` y `create.sh`) automatizan la obtención y el paso de este valor.

### Obtener el UUID manualmente

Si quieres ejecutar la imagen manualmente, necesitas obtener el UUID de tu equipo y pasarlo como variable de entorno `PC_UUID`.

#### Windows (PowerShell)

Ejecuta en PowerShell:

```powershell
(Get-CimInstance Win32_ComputerSystemProduct).UUID
```

#### Linux (Bash)

Ejecuta en terminal:

```bash
cat /sys/class/dmi/id/product_uuid
```

Luego, usa ese valor al lanzar el contenedor:

```bash
docker run -d -p 80:80 -e PC_UUID=<TU_UUID> --name control-host control-host:latest
```

---