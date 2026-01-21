# Opción Automática: Despliegue rápido

Esta opción permite levantar todo el entorno (backend y Nginx) automáticamente usando Docker Compose y scripts que detectan el UUID del equipo.

## ¿Cómo funciona?

- Los scripts (`create.ps1` para Windows, `create.sh` para Linux) obtienen el UUID y lo guardan en `.env`.
- Docker Compose usa ese UUID y construye/levanta los contenedores necesarios.

## Uso

### Windows

```powershell
./create.ps1
```

### Linux

```bash
./create.sh
```

Esto construirá las imágenes (si es necesario) y levantará los servicios listos para usar.

## Requisitos

- Docker y Docker Compose instalados.
- PowerShell (Windows) o Bash (Linux).
