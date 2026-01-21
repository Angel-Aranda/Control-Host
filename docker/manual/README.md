# Opción Manual: Despliegue paso a paso

Esta opción permite lanzar los servicios usando imágenes ya subidas a Docker Hub o construyendo manualmente, y pasando el UUID de tu equipo de forma manual.

## ¿Cómo funciona?

- Debes obtener el UUID de tu equipo y pasarlo como variable de entorno al lanzar el contenedor backend.
- Puedes usar los archivos `Dockerfile-python` y `Dockerfile-nginx` para construir las imágenes, o usar las imágenes ya publicadas en Docker Hub.
- El archivo `docker-compose.yml` está preparado para usar imágenes remotas.

## Pasos

### 1. Obtener el UUID

- **Windows (PowerShell):**
  ```powershell
  (Get-CimInstance Win32_ComputerSystemProduct).UUID
  ```
- **Linux (Bash):**
  ```bash
  cat /sys/class/dmi/id/product_uuid
  ```

### 2. Lanzar con Docker Compose

Edita el archivo `.env` y pon:
```
PC_UUID=TU_UUID
```

Luego ejecuta:
```bash
docker compose up
```

O bien, lanza los contenedores manualmente con `docker run` usando la variable de entorno `PC_UUID`.

## Requisitos

- Docker y Docker Compose instalados.
